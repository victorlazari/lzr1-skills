#!/usr/bin/env bash
# Preview-first wrapper for a single CodeRabbit agent-mode review.
# It never installs software, stages files, edits code, commits, pushes, or posts.

set -uo pipefail
set +x
umask 077

SCRIPT_DIR=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
VALIDATOR="$SCRIPT_DIR/validate_findings.py"

usage() {
  cat <<'EOF'
Usage: run-review.sh [options]

Default behavior is preview only. Add --execute to start one network-backed review.

Options:
  --repo PATH                 Repository path; default: current directory
  --scope MODE               tracked|committed|uncommitted; default: tracked
  --include-untracked        Include non-ignored untracked files with explicit consent
  --base REF                  Compare against a verified base branch or ref
  --base-commit COMMIT        Compare against a verified commit on the current branch
  --config FILE              Add one authorized context file; may be repeated
  --light                    Request CodeRabbit's lighter local review policy
  --region REGION            us|eu; omit to use current authenticated/default region
  --output-dir PATH          New evidence directory; default: secure temporary directory
  --timeout-seconds N        Optional total process ceiling; minimum 60 seconds
  --use-api-key-env          Pass CODERABBIT_API_KEY to CodeRabbit after explicit consent
  --execute                  Run the review; without this flag, print a redacted preview
  -h, --help                 Show this help

The script accepts no arbitrary pass-through arguments and no literal API-key option.
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 64
}

command_display() {
  local secret_index=$1
  shift
  local index=0 argument
  for argument in "$@"; do
    if [[ $index -eq $secret_index ]]; then
      printf "'%s' " '[REDACTED]'
    else
      printf '%q ' "$argument"
    fi
    index=$((index + 1))
  done
  printf '\n'
}

canonical_existing_file() {
  local candidate=$1
  [[ -f "$candidate" && ! -L "$candidate" ]] || return 1
  realpath -e -- "$candidate"
}

repo_input=.
scope=tracked
include_untracked=0
base_ref=
base_commit=
light=0
region=
output_input=
timeout_seconds=
use_api_key_env=0
execute=0
config_inputs=()

while (($#)); do
  case "$1" in
    --repo)
      (($# >= 2)) || fail '--repo requires a path'
      repo_input=$2
      shift 2
      ;;
    --scope)
      (($# >= 2)) || fail '--scope requires tracked, committed, or uncommitted'
      scope=$2
      shift 2
      ;;
    --include-untracked)
      include_untracked=1
      shift
      ;;
    --base)
      (($# >= 2)) || fail '--base requires a ref'
      base_ref=$2
      shift 2
      ;;
    --base-commit)
      (($# >= 2)) || fail '--base-commit requires a commit'
      base_commit=$2
      shift 2
      ;;
    --config)
      (($# >= 2)) || fail '--config requires a file'
      config_inputs+=("$2")
      shift 2
      ;;
    --light)
      light=1
      shift
      ;;
    --region)
      (($# >= 2)) || fail '--region requires us or eu'
      region=$2
      shift 2
      ;;
    --output-dir)
      (($# >= 2)) || fail '--output-dir requires a new path'
      output_input=$2
      shift 2
      ;;
    --timeout-seconds)
      (($# >= 2)) || fail '--timeout-seconds requires an integer'
      timeout_seconds=$2
      shift 2
      ;;
    --use-api-key-env)
      use_api_key_env=1
      shift
      ;;
    --execute)
      execute=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --api-key|--api-key=*)
      fail 'literal API-key arguments are forbidden; use a secret manager and --use-api-key-env'
      ;;
    --)
      fail 'arbitrary pass-through arguments are not supported'
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

case "$scope" in
  tracked|committed|uncommitted) ;;
  *) fail '--scope must be tracked, committed, or uncommitted' ;;
esac

if [[ $scope == committed && $include_untracked -eq 1 ]]; then
  fail '--include-untracked cannot be combined with committed scope'
fi
if [[ -n $base_ref && -n $base_commit ]]; then
  fail '--base and --base-commit are mutually exclusive in this wrapper'
fi
if [[ -n $region && $region != us && $region != eu ]]; then
  fail '--region must be us or eu'
fi
if [[ -n $timeout_seconds ]]; then
  [[ $timeout_seconds =~ ^[0-9]+$ ]] || fail '--timeout-seconds must be an integer'
  ((timeout_seconds >= 60)) || fail '--timeout-seconds must be at least 60'
  command -v timeout >/dev/null 2>&1 || fail 'GNU timeout is required when --timeout-seconds is used'
fi

command -v git >/dev/null 2>&1 || fail 'git is required'
command -v realpath >/dev/null 2>&1 || fail 'realpath is required'

repo_root=$(git -C "$repo_input" rev-parse --show-toplevel 2>/dev/null) || fail 'repository path is not inside a Git worktree'
repo_root=$(realpath -e -- "$repo_root") || fail 'cannot canonicalize repository root'
[[ -d "$repo_root" && ! -L "$repo_root" ]] || fail 'canonical repository root must be a non-symlink directory'
head_revision=$(git -C "$repo_root" rev-parse --verify HEAD 2>/dev/null) || fail 'repository has no resolvable HEAD'

if [[ -n $base_ref ]]; then
  [[ $base_ref != -* && $base_ref != *$'\n'* && $base_ref != *$'\r'* ]] || fail 'unsafe --base value'
  git -C "$repo_root" rev-parse --verify --quiet "${base_ref}^{commit}" >/dev/null || fail '--base does not resolve to a local commit'
fi
if [[ -n $base_commit ]]; then
  [[ $base_commit != -* && $base_commit != *$'\n'* && $base_commit != *$'\r'* ]] || fail 'unsafe --base-commit value'
  git -C "$repo_root" rev-parse --verify --quiet "${base_commit}^{commit}" >/dev/null || fail '--base-commit does not resolve to a local commit'
fi

config_files=()
for config_input in "${config_inputs[@]}"; do
  config_file=$(canonical_existing_file "$config_input") || fail "context file is missing, symlinked, or not regular: $config_input"
  case "$config_file" in
    "$repo_root"/*) ;;
    *) fail "context file is outside the repository: $config_input" ;;
  esac
  config_files+=("$config_file")
done

if command -v coderabbit >/dev/null 2>&1; then
  coderabbit_bin=$(command -v coderabbit)
elif command -v cr >/dev/null 2>&1; then
  coderabbit_bin=$(command -v cr)
else
  fail 'CodeRabbit CLI not found; inspect current official installation guidance before installing'
fi
coderabbit_bin=$(realpath -e -- "$coderabbit_bin") || fail 'cannot canonicalize CodeRabbit executable'
[[ -x "$coderabbit_bin" && ! -L "$coderabbit_bin" ]] || fail 'resolved CodeRabbit path must be an executable regular file'

if [[ $use_api_key_env -eq 1 ]]; then
  [[ -n ${CODERABBIT_API_KEY-} ]] || fail '--use-api-key-env requires CODERABBIT_API_KEY from a secret manager'
  [[ ${CODERABBIT_API_KEY} != *$'\n'* && ${CODERABBIT_API_KEY} != *$'\r'* ]] || fail 'CODERABBIT_API_KEY contains a forbidden line break'
fi

review_cmd=("$coderabbit_bin" review --agent --dir "$repo_root")
case "$scope" in
  committed) review_cmd+=(--committed) ;;
  uncommitted) review_cmd+=(--uncommitted) ;;
  tracked) ;;
esac
((include_untracked == 1)) && review_cmd+=(--include-untracked)
((light == 1)) && review_cmd+=(--light)
[[ -n $base_ref ]] && review_cmd+=(--base "$base_ref")
[[ -n $base_commit ]] && review_cmd+=(--base-commit "$base_commit")
[[ -n $region ]] && review_cmd+=(--region "$region")
for config_file in "${config_files[@]}"; do
  review_cmd+=(--config "$config_file")
done
secret_index=-1
if [[ $use_api_key_env -eq 1 ]]; then
  review_cmd+=(--api-key "$CODERABBIT_API_KEY")
  secret_index=$((${#review_cmd[@]} - 1))
fi

version_output=$("$coderabbit_bin" --version 2>&1)
version_status=$?
((version_status == 0)) || fail 'CodeRabbit version check failed'

printf 'CodeRabbit review preview\n'
printf '  repository: %s\n' "$repo_root"
printf '  revision:   %s\n' "$head_revision"
printf '  executable: %s\n' "$coderabbit_bin"
printf '  version:    %s\n' "$version_output"
printf '  scope:      %s\n' "$scope"
printf '  untracked:  %s\n' "$([[ $include_untracked -eq 1 ]] && printf included || printf excluded)"
printf '  base:       %s\n' "${base_ref:-${base_commit:-default}}"
printf '  region:     %s\n' "${region:-authenticated/default}"
printf '  mode:       %s\n' "$([[ $light -eq 1 ]] && printf light || printf default)"
printf '  API key:    %s\n' "$([[ $use_api_key_env -eq 1 ]] && printf 'explicit environment mode' || printf 'existing auth only')"
printf '  command:    '
command_display "$secret_index" "${review_cmd[@]}"

printf '\nGit state (read-only):\n'
git -C "$repo_root" status --short --branch

if [[ $include_untracked -eq 1 ]]; then
  printf '\nAuthorized untracked paths:\n'
  git -C "$repo_root" ls-files --others --exclude-standard
fi

if [[ $execute -ne 1 ]]; then
  printf '\nPREVIEW ONLY: no network review was started. Add --execute after confirming scope and data transfer.\n'
  exit 0
fi

command -v sha256sum >/dev/null 2>&1 || fail 'sha256sum is required for evidence capture'

if [[ -n $output_input ]]; then
  [[ ! -e $output_input && ! -L $output_input ]] || fail '--output-dir must not already exist'
  output_parent=$(dirname -- "$output_input")
  output_parent=$(realpath -e -- "$output_parent") || fail 'cannot canonicalize output parent directory'
  output_dir="$output_parent/$(basename -- "$output_input")"
  mkdir -m 700 -- "$output_dir" || fail 'cannot create output directory'
else
  output_dir=$(mktemp -d "${TMPDIR:-/tmp}/coderabbit-review.XXXXXXXX") || fail 'cannot create secure temporary output directory'
  chmod 700 "$output_dir" || fail 'cannot protect output directory'
fi
output_dir=$(realpath -e -- "$output_dir") || fail 'cannot canonicalize output directory'
case "$output_dir" in
  "$repo_root"|"$repo_root"/*) fail 'evidence directory must be outside the reviewed repository' ;;
esac

stdout_file="$output_dir/stdout.ndjson"
stderr_file="$output_dir/stderr.log"
command_file="$output_dir/command.txt"
metadata_file="$output_dir/metadata.txt"
exit_file="$output_dir/process-exit-code.txt"
validation_file="$output_dir/validation.json"

command_display "$secret_index" "${review_cmd[@]}" >"$command_file"
{
  printf 'repository=%q\n' "$repo_root"
  printf 'head_revision=%q\n' "$head_revision"
  printf 'coderabbit_executable=%q\n' "$coderabbit_bin"
  printf 'coderabbit_version=%q\n' "$version_output"
  printf 'scope=%q\n' "$scope"
  printf 'include_untracked=%q\n' "$include_untracked"
  printf 'base_ref=%q\n' "$base_ref"
  printf 'base_commit=%q\n' "$base_commit"
  printf 'region=%q\n' "$region"
  printf 'light=%q\n' "$light"
  printf 'api_key_mode=%q\n' "$use_api_key_env"
} >"$metadata_file"
git -C "$repo_root" status --porcelain=v2 --branch >"$output_dir/git-status.txt"
if [[ $include_untracked -eq 1 ]]; then
  git -C "$repo_root" ls-files --others --exclude-standard >"$output_dir/untracked-paths.txt"
fi

printf '\nStarting one authorized network-backed review. Evidence: %s\n' "$output_dir"
if [[ -n $timeout_seconds ]]; then
  timeout --signal=TERM --kill-after=15s "$timeout_seconds" "${review_cmd[@]}" >"$stdout_file" 2>"$stderr_file"
  review_status=$?
else
  "${review_cmd[@]}" >"$stdout_file" 2>"$stderr_file"
  review_status=$?
fi
unset CODERABBIT_API_KEY || true
if ((secret_index >= 0)); then
  review_cmd[$secret_index]='[REDACTED]'
fi
printf '%s\n' "$review_status" >"$exit_file"
sha256sum "$stdout_file" "$stderr_file" "$command_file" "$metadata_file" >"$output_dir/sha256sums.txt"

validator_status=127
if [[ -f "$VALIDATOR" ]] && command -v python3 >/dev/null 2>&1; then
  python3 "$VALIDATOR" "$stdout_file" --process-exit-code "$review_status" --json-output >"$validation_file"
  validator_status=$?
else
  printf '{"valid":false,"errors":["validator unavailable"]}\n' >"$validation_file"
fi

printf 'Review process exit: %s\n' "$review_status"
printf 'Validator exit:      %s\n' "$validator_status"
printf 'Validation summary:  %s\n' "$validation_file"
printf 'Raw stderr remains protected at %s; inspect and redact before sharing.\n' "$stderr_file"

if ((review_status != 0)); then
  exit "$review_status"
fi
if ((validator_status != 0)); then
  exit "$validator_status"
fi
exit 0
