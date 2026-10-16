#!/usr/bin/env bash
# Negative-fixture tests for scripts/lint_catalog.py. Bash 3.2 compatible.

set -euo pipefail
umask 077

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
LINT="$ROOT/scripts/lint_catalog.py"
WORK=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-catalog-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

# Build a clean two-skill fixture root at $1.
make_fixture() {
  local r=$1
  mkdir -p "$r/skills/alpha/references" "$r/skills/alpha/scripts" \
    "$r/skills/beta" "$r/tests"
  printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\n# Alpha\nSee references/guide.md and scripts/run.sh.\n' \
    > "$r/skills/alpha/SKILL.md"
  printf '# guide\n' > "$r/skills/alpha/references/guide.md"
  printf '#!/usr/bin/env bash\ntrue\n' > "$r/skills/alpha/scripts/run.sh"
  chmod 755 "$r/skills/alpha/scripts/run.sh"
  printf -- '---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\n' \
    > "$r/skills/beta/SKILL.md"
  printf 'alpha\nbeta\n' > "$r/skills-list.txt"
  printf 'EXPECTED_SKILL_COUNT=2\n' > "$r/install.sh"
  printf 'EXPECTED=2\n' > "$r/tests/test-installer.sh"
  printf '![skills](https://img.shields.io/badge/skills-2-blue)\n2 curated AI skills\n' \
    > "$r/README.md"
}

# expect_rule NAME RULE ROOT: linter must exit 1 and print the rule id.
expect_rule() {
  local name=$1 rule=$2 r=$3 out rc=0
  out=$(python3 -I "$LINT" --root "$r" 2>&1) || rc=$?
  [[ $rc -eq 1 ]] || fail "$name: expected exit 1, got $rc (mutation not detected)"
  printf '%s\n' "$out" | grep -E "^ERROR .*: $rule( |\$)" >/dev/null \
    || fail "$name: output lacks rule $rule: $out"
  printf 'PASS: %s\n' "$rule"
}

# Baseline: clean fixture passes.
BASE="$WORK/base"
make_fixture "$BASE"
rc=0
out=$(python3 -I "$LINT" --root "$BASE" 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "clean fixture should pass, got $rc: $out"
printf 'PASS: clean fixture\n'

m=$WORK/m1; make_fixture "$m"
rm "$m/skills/beta/SKILL.md"
expect_rule "missing SKILL.md" fm-missing "$m"

m=$WORK/m2; make_fixture "$m"
printf -- '---\nname: wrong\ndescription: Use when x.\n---\n' > "$m/skills/beta/SKILL.md"
expect_rule "renamed frontmatter name" fm-name "$m"

m=$WORK/m3; make_fixture "$m"
printf -- '---\nname: beta\n---\n# Beta\n' > "$m/skills/beta/SKILL.md"
expect_rule "missing description" fm-desc "$m"

m=$WORK/m4; make_fixture "$m"
rm "$m/skills/alpha/references/guide.md"
expect_rule "deleted referenced file" link-broken "$m"

m=$WORK/m5; make_fixture "$m"
printf 'x\n' > "$m/skills/alpha/references/unused.md"
expect_rule "unreferenced reference file" ref-orphan "$m"

m=$WORK/m6; make_fixture "$m"
chmod -x "$m/skills/alpha/scripts/run.sh"
expect_rule "script not executable" exec-bit "$m"

m=$WORK/m7; make_fixture "$m"
mkdir "$m/skills/gamma"
printf -- '---\nname: gamma\ndescription: Use when testing gamma.\n---\n' > "$m/skills/gamma/SKILL.md"
expect_rule "skill absent from manifest" manifest-sync "$m"

m=$WORK/m8; make_fixture "$m"
printf 'EXPECTED_SKILL_COUNT=3\n' > "$m/install.sh"
expect_rule "count constant changed" count-sync "$m"

m=$WORK/m9; make_fixture "$m"
ln -s ../beta/SKILL.md "$m/skills/alpha/link.md"
expect_rule "symlink added" symlink "$m"

# Real repo must be clean.
rc=0
out=$(python3 -I "$LINT" --root "$ROOT" 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "real repo lint failed (exit $rc): $out"
printf 'PASS: real repo clean\n'
