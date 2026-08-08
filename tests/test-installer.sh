#!/usr/bin/env bash
# End-to-end tests for install.sh. Uses an isolated HOME and local source only.

set -euo pipefail
umask 077

ROOT=$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
INSTALLER="$ROOT/install.sh"
EXPECTED=86
WORK=$(mktemp -d "${TMPDIR:-/tmp}/lzr1-installer-test.XXXXXXXX")
cleanup() {
  rm -rf -- "$WORK"
}
trap cleanup EXIT HUP INT TERM

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_file() {
  [[ -f $1 && ! -L $1 ]] || fail "missing regular file: $1"
}

assert_absent() {
  [[ ! -e $1 && ! -L $1 ]] || fail "path should be absent: $1"
}

assert_contains() {
  grep -F -- "$2" "$1" >/dev/null || fail "$1 does not contain: $2"
}

run_installer() {
  local home=$1
  shift
  HOME="$home" LZR1_SOURCE_DIR="$ROOT" bash "$INSTALLER" "$@"
}

mkdir -p "$WORK/home"
run_installer "$WORK/home" --codex --cursor --yes >"$WORK/install.out"

codex="$WORK/home/.codex/skills"
cursor="$WORK/home/.cursor/rules"
package_count=$(find "$codex" -mindepth 2 -maxdepth 2 -type f -name .lzr1-managed | wc -l | tr -d ' ')
flat_count=$(find "$cursor/.lzr1-managed" -mindepth 1 -maxdepth 1 -type f | wc -l | tr -d ' ')
[[ $package_count -eq $EXPECTED ]] || fail "Codex package count is $package_count, expected $EXPECTED"
[[ $flat_count -eq $EXPECTED ]] || fail "Cursor marker count is $flat_count, expected $EXPECTED"

assert_file "$codex/coderabbit-reviewer/SKILL.md"
assert_file "$codex/coderabbit-reviewer/references/cli-commands.md"
assert_file "$codex/coderabbit-reviewer/scripts/validate_findings.py"
assert_file "$cursor/coderabbit-reviewer.md"
assert_file "$cursor/.lzr1-skill-resources/coderabbit-reviewer/SKILL.md"
assert_file "$cursor/.lzr1-skill-resources/coderabbit-reviewer/references/cli-commands.md"
assert_contains "$cursor/coderabbit-reviewer.md" '](.lzr1-skill-resources/coderabbit-reviewer/references/'
if grep -F -- '](references/' "$cursor/coderabbit-reviewer.md" >/dev/null; then
  fail 'flat CodeRabbit entrypoint retained a broken references/ link'
fi

assert_file "$codex/yaml-specialist/SKILL.md"
assert_file "$codex/yaml-specialist/references/yaml-language.md"
assert_file "$codex/yaml-specialist/scripts/validate_chart.sh"
assert_file "$codex/yaml-specialist/templates/values.schema.example.json"
assert_file "$codex/yaml-specialist/tests/fixtures/duplicate-key.yaml"
[[ -x $codex/yaml-specialist/scripts/validate_chart.sh ]] || fail 'native yaml-specialist wrapper lost executable mode'
assert_file "$cursor/yaml-specialist.md"
assert_file "$cursor/.lzr1-skill-resources/yaml-specialist/SKILL.md"
assert_file "$cursor/.lzr1-skill-resources/yaml-specialist/references/yaml-language.md"
assert_file "$cursor/.lzr1-skill-resources/yaml-specialist/scripts/validate_chart.sh"
assert_file "$cursor/.lzr1-skill-resources/yaml-specialist/templates/values.schema.example.json"
assert_contains "$cursor/yaml-specialist.md" '](.lzr1-skill-resources/yaml-specialist/references/'
if grep -F -- '](references/' "$cursor/yaml-specialist.md" >/dev/null; then
  fail 'flat yaml-specialist entrypoint retained a broken references/ link'
fi

assert_file "$WORK/home/.lzr1-skills-state"
printf 'codex\ncursor\n' >"$WORK/expected-state"
cmp -s "$WORK/expected-state" "$WORK/home/.lzr1-skills-state" || fail 'initial state does not list both installed targets'

run_installer "$WORK/home" doctor >"$WORK/doctor.out"
assert_contains "$WORK/doctor.out" 'Codex                86/86 managed skills'
assert_contains "$WORK/doctor.out" 'Cursor               86/86 managed skills'

run_installer "$WORK/home" update --codex --yes >"$WORK/update.out"
cmp -s "$WORK/expected-state" "$WORK/home/.lzr1-skills-state" || fail 'subset update discarded another installed target from state'

run_installer "$WORK/home" remove --codex --yes >"$WORK/remove-codex.out"
assert_absent "$codex/coderabbit-reviewer"
assert_absent "$codex/yaml-specialist"
printf 'cursor\n' >"$WORK/expected-state"
cmp -s "$WORK/expected-state" "$WORK/home/.lzr1-skills-state" || fail 'subset removal did not preserve Cursor state'

run_installer "$WORK/home" remove --cursor --yes >"$WORK/remove-cursor.out"
assert_absent "$cursor/coderabbit-reviewer.md"
assert_absent "$cursor/.lzr1-skill-resources/coderabbit-reviewer"
assert_absent "$cursor/yaml-specialist.md"
assert_absent "$cursor/.lzr1-skill-resources/yaml-specialist"
assert_absent "$WORK/home/.lzr1-skills-state"

mkdir -p "$WORK/collision-home/.codex/skills/coderabbit-reviewer"
printf 'preserve me\n' >"$WORK/collision-home/.codex/skills/coderabbit-reviewer/sentinel.txt"
if run_installer "$WORK/collision-home" --codex --yes >"$WORK/collision.out" 2>&1; then
  fail 'unowned collision unexpectedly succeeded without --force'
fi
assert_contains "$WORK/collision-home/.codex/skills/coderabbit-reviewer/sentinel.txt" 'preserve me'
assert_absent "$WORK/collision-home/.codex/skills/accessibility-testing"

run_installer "$WORK/collision-home" --codex --yes --force >"$WORK/force.out" 2>&1
assert_file "$WORK/collision-home/.codex/skills/coderabbit-reviewer/SKILL.md"
backup=$(find "$WORK/collision-home/.codex/skills/.lzr1-backups" -type f -path '*/coderabbit-reviewer/package/sentinel.txt' -print -quit)
[[ -n $backup ]] || fail 'forced unowned collision was not backed up'
assert_contains "$backup" 'preserve me'

mkdir -p "$WORK/symlink-home" "$WORK/outside"
ln -s "$WORK/outside" "$WORK/symlink-home/.codex"
if run_installer "$WORK/symlink-home" --codex --yes >"$WORK/symlink.out" 2>&1; then
  fail 'symlinked target parent unexpectedly succeeded'
fi
assert_contains "$WORK/symlink.out" 'Target path contains a symbolic-link component'
assert_absent "$WORK/outside/skills"

mkdir -p "$WORK/empty-home"
if run_installer "$WORK/empty-home" --yes >"$WORK/no-target.out" 2>&1; then
  fail '--yes without a target unexpectedly succeeded'
fi
assert_contains "$WORK/no-target.out" 'Non-interactive mode requires --detected or explicit target flags'

if run_installer "$WORK/empty-home" --not-a-real-option >"$WORK/unknown.out" 2>&1; then
  fail 'unknown option unexpectedly succeeded'
fi
assert_contains "$WORK/unknown.out" 'Unknown argument'

printf 'PASS: installer end-to-end tests completed for %d skills without network access\n' "$EXPECTED"
