#!/usr/bin/env bash
# Build the release assets for a tag: lzr1-skills.tar.gz and SHA256SUMS.
# Usage: scripts/build-release.sh <vX.Y.Z> <out-dir>
# Run from inside the git repository (the tag must exist locally).

set -euo pipefail

fail() {
  printf 'build-release: %s\n' "$*" >&2
  exit 1
}

usage() {
  printf 'Usage: %s <vX.Y.Z> <out-dir>\n' "${0##*/}"
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi
[ $# -eq 2 ] || { usage >&2; exit 2; }

TAG=$1
OUT=$2

if ! printf '%s' "$TAG" | grep -Eq '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
  fail "invalid tag '${TAG}': expected vMAJOR.MINOR.PATCH"
fi
git rev-parse -q --verify "refs/tags/${TAG}^{commit}" >/dev/null \
  || fail "tag '${TAG}' not found"

TAG_VERSION=$(git show "${TAG}:install.sh" | sed -n 's/^VERSION="\([^"]*\)".*/\1/p' | head -n 1)
[ -n "$TAG_VERSION" ] || fail "no VERSION found in install.sh at ${TAG}"
[ "$TAG_VERSION" = "${TAG#v}" ] \
  || fail "install.sh VERSION '${TAG_VERSION}' does not match tag '${TAG}'"

sha256_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    fail "sha256sum or shasum is required"
  fi
}

ASSET=lzr1-skills.tar.gz
mkdir -p "$OUT"
rm -f "${OUT}/${ASSET}" "${OUT}/SHA256SUMS"

git archive --format=tar.gz --prefix="lzr1-skills-${TAG}/" -o "${OUT}/${ASSET}" "$TAG"

HASH=$(sha256_file "${OUT}/${ASSET}")
printf '%s  %s\n' "$HASH" "$ASSET" >"${OUT}/SHA256SUMS"

# Verify the pair by re-reading the checksum file.
LISTED=$(awk -v n="$ASSET" '$2 == n {print $1}' "${OUT}/SHA256SUMS")
[ "$LISTED" = "$(sha256_file "${OUT}/${ASSET}")" ] || fail "checksum verification failed"

printf 'Built %s/%s (%s)\n' "$OUT" "$ASSET" "$HASH"
