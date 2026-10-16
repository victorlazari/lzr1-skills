#!/usr/bin/env bash
# Offline test for scripts/build-release.sh: builds a release pair in a temp
# git repo and checks structure, checksum and tag refusals. No network.

set -euo pipefail
umask 077

# git commit/tag need an identity even without global user config.
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=t@example.invalid
export GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=t@example.invalid

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
SCRIPT=$ROOT/scripts/build-release.sh
WORK=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-release-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

[[ -f $SCRIPT ]] || fail "missing $SCRIPT"

REPO=$WORK/repo
mkdir -p "$REPO/skills/demo"
(
  cd "$REPO"
  git init -q .
  git config user.email t@example.invalid
  git config user.name test
  git config commit.gpgsign false
  printf 'VERSION="9.9.9"\n' >install.sh
  printf '# Changelog\n\n## [9.9.9]\n\n- x\n' >CHANGELOG.md
  printf 'demo\n' >skills/demo/SKILL.md
  git add install.sh CHANGELOG.md skills
  git commit -q -m init
  git tag v9.9.9
  git tag v9.9.8
)

OUT=$WORK/out
(cd "$REPO" && bash "$SCRIPT" v9.9.9 "$OUT") >"$WORK/ok.log" 2>&1 \
  || { cat "$WORK/ok.log" >&2; fail "valid tag was refused"; }

[[ -f $OUT/lzr1-skills.tar.gz ]] || fail "tarball not produced"
[[ -f $OUT/SHA256SUMS ]] || fail "SHA256SUMS not produced"

roots=$(tar -tzf "$OUT/lzr1-skills.tar.gz" | cut -d/ -f1 | sort -u)
[[ $roots == "lzr1-skills-v9.9.9" ]] || fail "expected one top-level dir lzr1-skills-v9.9.9, got: $roots"

[[ $(wc -l <"$OUT/SHA256SUMS" | tr -d ' ') == 1 ]] || fail "SHA256SUMS must have exactly one line"
if command -v sha256sum >/dev/null 2>&1; then
  (cd "$OUT" && sha256sum -c SHA256SUMS >/dev/null) || fail "sha256sum -c failed"
else
  (cd "$OUT" && shasum -a 256 -c SHA256SUMS >/dev/null) || fail "shasum -c failed"
fi

expect_refused() {
  local tag=$1 pattern=$2 log=$WORK/refuse.log
  if (cd "$REPO" && bash "$SCRIPT" "$tag" "$WORK/out-bad") >"$log" 2>&1; then
    fail "tag '$tag' was accepted"
  fi
  grep -q -- "$pattern" "$log" || { cat "$log" >&2; fail "tag '$tag': expected message '$pattern'"; }
}
expect_refused 9.9.9 'invalid tag'
expect_refused v9.9.8 'does not match'
expect_refused v1.2.3 'not found'

# The release workflow's first step must reject tags that only match the loose glob.
WF=$ROOT/.github/workflows/release.yml
[[ -f $WF ]] || fail "missing release workflow"
step=$(awk '/- name: Validate tag name/{f=1;next} f&&/- uses:/{exit} f' "$WF")
[[ -n $step ]] || fail "release.yml lacks the Validate tag name step"
first=$(grep -n -- '- name:\|- uses:' "$WF" | head -n 1)
case $first in *'Validate tag name'*) ;; *) fail "tag validation must be the first step: $first" ;; esac
for t in v1.2.3garbage v1.2.3-rc1 v1.2 v1.2.3.4 vx.y.z 'v1.2.3 '; do
  if (GITHUB_REF_NAME=$t bash -c "$(printf '%s\n' "$step" | sed 's/^ *run: |$//')") >/dev/null 2>&1; then
    fail "tag '$t' passed workflow validation"
  fi
done
GITHUB_REF_NAME=v1.2.3 bash -c "$(printf '%s\n' "$step" | sed 's/^ *run: |$//')" >/dev/null 2>&1 || fail "v1.2.3 rejected by workflow validation"
printf 'PASS: release tag validation step\n'

printf 'PASS: release packaging\n'
