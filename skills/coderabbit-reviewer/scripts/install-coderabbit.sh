#!/usr/bin/env bash
# Safely stage or execute a reviewed snapshot of the official CodeRabbit installer.
# The default action performs no network request and no installation.

set -uo pipefail
set +x
umask 077

INSTALLER_URL='https://cli.coderabbit.ai/install.sh'
mode=preview
fetch_dir=
reviewed_file=
expected_sha256=
ack_side_effects=0

usage() {
  cat <<'EOF'
Usage: install-coderabbit.sh [mode]

Modes are mutually exclusive. With no mode, print an offline preview only.

  --fetch-preview DIR
      Download the current official installer as inert text into a new directory,
      compute its SHA-256 digest, and do not execute it.

  --execute-reviewed FILE --expected-sha256 HEX --ack-installer-side-effects
      Execute only the exact local, non-symlink installer snapshot whose digest
      was reviewed and supplied. The snapshot can download a platform archive,
      write a user binary, modify shell PATH files, and initiate authentication.

  -h, --help
      Show this help.

This wrapper never uses `curl | bash`, never accepts an unchecked URL, and never
claims that a matching digest proves upstream authenticity. Establish provenance
through your organization’s software-acquisition process.
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 64
}

while (($#)); do
  case "$1" in
    --fetch-preview)
      (($# >= 2)) || fail '--fetch-preview requires a new directory path'
      [[ $mode == preview ]] || fail 'installation modes are mutually exclusive'
      mode=fetch
      fetch_dir=$2
      shift 2
      ;;
    --execute-reviewed)
      (($# >= 2)) || fail '--execute-reviewed requires a local file path'
      [[ $mode == preview ]] || fail 'installation modes are mutually exclusive'
      mode=execute
      reviewed_file=$2
      shift 2
      ;;
    --expected-sha256)
      (($# >= 2)) || fail '--expected-sha256 requires 64 lowercase hexadecimal characters'
      expected_sha256=$2
      shift 2
      ;;
    --ack-installer-side-effects)
      ack_side_effects=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

if [[ $mode == preview ]]; then
  cat <<EOF
CodeRabbit installer offline preview

Official installer URL: $INSTALLER_URL

No network request or installation was performed.

Recommended sequence:
  1. Run this script with --fetch-preview NEW_DIRECTORY.
  2. Read the complete downloaded installer as untrusted source text.
  3. Verify its provenance and assess archive verification, download hosts,
     binary destination, PATH-file edits, update behavior, and auth prompts.
  4. Record the displayed SHA-256 through a trusted review channel.
  5. If approved, run --execute-reviewed FILE with that exact digest and the
     explicit --ack-installer-side-effects flag.

The installer inspected during package research did not visibly verify a
published archive checksum or cryptographic signature. Prefer an
organization-approved distribution channel when available.
EOF
  exit 0
fi

command -v sha256sum >/dev/null 2>&1 || fail 'sha256sum is required'
command -v realpath >/dev/null 2>&1 || fail 'realpath is required'

if [[ $mode == fetch ]]; then
  command -v curl >/dev/null 2>&1 || fail 'curl is required for --fetch-preview'
  [[ ! -e $fetch_dir && ! -L $fetch_dir ]] || fail 'fetch directory must not already exist'
  parent=$(dirname -- "$fetch_dir")
  parent=$(realpath -e -- "$parent") || fail 'cannot canonicalize fetch-directory parent'
  destination="$parent/$(basename -- "$fetch_dir")"
  mkdir -m 700 -- "$destination" || fail 'cannot create protected fetch directory'
  installer="$destination/coderabbit-install.sh"
  headers="$destination/response-headers.txt"
  metadata="$destination/metadata.txt"

  curl --fail --silent --show-error --location \
    --proto '=https' --tlsv1.2 \
    --max-redirs 5 --connect-timeout 15 --max-time 60 \
    --dump-header "$headers" \
    --output "$installer" \
    "$INSTALLER_URL" || {
      status=$?
      printf 'Download failed; protected partial evidence remains at %s\n' "$destination" >&2
      exit "$status"
    }

  [[ -s $installer && ! -L $installer ]] || fail 'downloaded installer is empty or unsafe'
  chmod 600 "$installer" "$headers"
  digest=$(sha256sum "$installer" | awk '{print $1}')
  {
    printf 'source_url=%s\n' "$INSTALLER_URL"
    printf 'sha256=%s\n' "$digest"
    printf 'bytes=%s\n' "$(wc -c <"$installer")"
    printf 'executed=false\n'
  } >"$metadata"
  chmod 600 "$metadata"

  printf 'Downloaded inert installer snapshot; it was NOT executed.\n'
  printf '  file:   %s\n' "$installer"
  printf '  sha256: %s\n' "$digest"
  printf '  bytes:  %s\n' "$(wc -c <"$installer")"
  printf '\nRead the entire file and verify provenance before considering execution.\n'
  exit 0
fi

[[ $mode == execute ]] || fail 'internal mode error'
[[ $ack_side_effects -eq 1 ]] || fail '--execute-reviewed requires --ack-installer-side-effects'
[[ $expected_sha256 =~ ^[a-f0-9]{64}$ ]] || fail '--expected-sha256 must be 64 lowercase hexadecimal characters'
[[ -f $reviewed_file && ! -L $reviewed_file ]] || fail 'reviewed installer must be a regular non-symlink file'
reviewed_file=$(realpath -e -- "$reviewed_file") || fail 'cannot canonicalize reviewed installer path'
actual_sha256=$(sha256sum "$reviewed_file" | awk '{print $1}')
[[ $actual_sha256 == "$expected_sha256" ]] || fail "digest mismatch: expected $expected_sha256, got $actual_sha256"

first_line=$(head -n 1 -- "$reviewed_file")
case "$first_line" in
  '#!'*) ;;
  *) fail 'reviewed file does not begin with an interpreter line' ;;
esac

cat <<EOF
Executing reviewed local installer snapshot
  file:   $reviewed_file
  sha256: $actual_sha256

Acknowledged possible effects: remote archive download, user-binary write,
PATH-profile edits, version check, and authentication prompt.
EOF

bash -- "$reviewed_file"
install_status=$?

printf 'Installer exit status: %s\n' "$install_status"
if ((install_status == 0)); then
  if command -v coderabbit >/dev/null 2>&1; then
    coderabbit --version
  elif command -v cr >/dev/null 2>&1; then
    cr --version
  else
    printf 'WARNING: installer returned success, but coderabbit/cr is not currently resolvable on PATH.\n' >&2
  fi
fi
exit "$install_status"
