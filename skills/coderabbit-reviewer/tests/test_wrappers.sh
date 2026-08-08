#!/usr/bin/env bash
# Deterministic wrapper tests. No network access and no real CodeRabbit invocation.

set -euo pipefail
umask 077

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
RUNNER="$ROOT/scripts/run-review.sh"
INSTALLER="$ROOT/scripts/install-coderabbit.sh"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/coderabbit-wrapper-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_contains() {
  local file=$1 expected=$2
  grep -F -- "$expected" "$file" >/dev/null || fail "$file does not contain: $expected"
}

assert_not_contains() {
  local file=$1 forbidden=$2
  if grep -F -- "$forbidden" "$file" >/dev/null; then
    fail "$file contains forbidden text: $forbidden"
  fi
}

mkdir -p "$WORK/bin" "$WORK/repo" "$WORK/evidence-parent"
cat >"$WORK/bin/coderabbit" <<'FAKE'
#!/usr/bin/env bash
set -eu
if [[ ${1-} == --version ]]; then
  printf 'coderabbit 0.7.2-test\n'
  exit 0
fi
if [[ ${1-} == review ]]; then
  printf '%s\n' '{"type":"review_context","repository":"fixture","scope":"uncommitted"}'
  printf '%s\n' '{"type":"finding","severity":"major","fileName":"tracked.txt","comment":"Confirm the invariant."}'
  printf '%s\n' '{"type":"complete","status":"completed","findings":1}'
  printf 'fake diagnostic\n' >&2
  exit 0
fi
printf 'unsupported fake invocation\n' >&2
exit 9
FAKE
chmod 0755 "$WORK/bin/coderabbit"

(
  cd "$WORK/repo"
  git init -q
  git config user.name 'Fixture User'
  git config user.email 'fixture@example.invalid'
  printf 'base\n' >tracked.txt
  git add tracked.txt
  git commit -qm 'fixture baseline'
  printf 'changed\n' >>tracked.txt
  printf 'new\n' >untracked.txt
)

PATH="$WORK/bin:$PATH" "$RUNNER" --repo "$WORK/repo" --scope uncommitted >"$WORK/preview.out"
assert_contains "$WORK/preview.out" 'PREVIEW ONLY: no network review was started.'
[[ ! -e "$WORK/evidence-parent/preview" ]] || fail 'preview created an evidence directory'

if PATH="$WORK/bin:$PATH" "$RUNNER" --repo "$WORK/repo" --scope committed --include-untracked >"$WORK/conflict.out" 2>&1; then
  fail 'contradictory scope unexpectedly succeeded'
fi
assert_contains "$WORK/conflict.out" '--include-untracked cannot be combined with committed scope'

if PATH="$WORK/bin:$PATH" "$RUNNER" --repo "$WORK/repo" --api-key literal-secret >"$WORK/key.out" 2>&1; then
  fail 'literal API key unexpectedly succeeded'
fi
assert_contains "$WORK/key.out" 'literal API-key arguments are forbidden'

test_key="TEST_ONLY_$(printf 'X%.0s' {1..24})"
export CODERABBIT_API_KEY="$test_key"
PATH="$WORK/bin:$PATH" "$RUNNER" \
  --repo "$WORK/repo" \
  --scope uncommitted \
  --include-untracked \
  --use-api-key-env \
  --output-dir "$WORK/evidence-parent/review" \
  --execute >"$WORK/execute.out"
unset CODERABBIT_API_KEY

for required in stdout.ndjson stderr.log command.txt metadata.txt process-exit-code.txt validation.json sha256sums.txt git-status.txt untracked-paths.txt; do
  [[ -f "$WORK/evidence-parent/review/$required" ]] || fail "missing evidence file: $required"
done
assert_contains "$WORK/evidence-parent/review/validation.json" '"valid": true'
assert_contains "$WORK/evidence-parent/review/command.txt" '[REDACTED]'
assert_contains "$WORK/evidence-parent/review/untracked-paths.txt" 'untracked.txt'
if grep -R -F -- "$test_key" "$WORK/evidence-parent/review" >/dev/null; then
  fail 'API key leaked into evidence'
fi
unset test_key

"$INSTALLER" >"$WORK/install-preview.out"
assert_contains "$WORK/install-preview.out" 'No network request or installation was performed.'

cat >"$WORK/reviewed-installer.sh" <<'INSTALL'
#!/usr/bin/env bash
set -eu
printf 'executed\n' >"${INSTALL_TEST_MARKER:?}"
INSTALL
chmod 0600 "$WORK/reviewed-installer.sh"
digest=$(sha256sum "$WORK/reviewed-installer.sh" | awk '{print $1}')
export INSTALL_TEST_MARKER="$WORK/install-marker"
if "$INSTALLER" --execute-reviewed "$WORK/reviewed-installer.sh" --expected-sha256 "$(printf '0%.0s' {1..64})" --ack-installer-side-effects >"$WORK/bad-digest.out" 2>&1; then
  fail 'mismatched installer digest unexpectedly succeeded'
fi
[[ ! -e "$WORK/install-marker" ]] || fail 'installer ran despite digest mismatch'

"$INSTALLER" --execute-reviewed "$WORK/reviewed-installer.sh" --expected-sha256 "$digest" --ack-installer-side-effects >"$WORK/install-execute.out"
[[ -f "$WORK/install-marker" ]] || fail 'reviewed installer did not execute after exact digest approval'
unset INSTALL_TEST_MARKER

printf 'PASS: wrapper tests completed without network access\n'
