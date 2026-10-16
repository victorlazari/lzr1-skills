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
  printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\n# Alpha\nSee `references/guide.md` and `scripts/run.sh`.\n' \
    > "$r/skills/alpha/SKILL.md"
  printf '# guide\n' > "$r/skills/alpha/references/guide.md"
  printf '#!/usr/bin/env bash\ntrue\n' > "$r/skills/alpha/scripts/run.sh"
  chmod 755 "$r/skills/alpha/scripts/run.sh"
  printf -- '---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\n' \
    > "$r/skills/beta/SKILL.md"
  printf 'alpha\nbeta\n' > "$r/skills-list.txt"
  printf 'path\tlevel\treason\ttest\nskills/alpha/scripts/run.sh\tstatic\tfixture script, no safe invocation\t\n' \
    > "$r/tests/script-coverage.tsv"
  printf 'VERSION="1.2.3"\nEXPECTED_SKILL_COUNT=2\nprint_help() {\n  printf "usage\\n  --alpha  a\\n  --help   h\\n"\n}\nparse_args() {\n  case "$1" in\n    --alpha) ;;\n    --help) print_help; exit 0 ;;\n  esac\n}\nif [ "${1:-}" = "--help" ]; then\n  print_help\n  exit 0\nfi\n' > "$r/install.sh"
  printf 'EXPECTED=2\n' > "$r/tests/test-installer.sh"
  printf '![skills](https://img.shields.io/badge/skills-2-blue)\n2 curated AI skills\n\n## The Arsenal\n\n### Cat\n\n| Skill | What |\n|:--|:--|\n| `alpha` | a |\n| `beta` | b |\n\n## Equip Up\n\nRun `bash install.sh --alpha`.\n\n## Command Reference\n\n| `--alpha` | a |\n| `--help` | h |\n\n## Update & Remove\n\nRun `--alpha` again.\n\n## Other\n\nInstaller version: 1.2.3\n\n<!-- pattern-census:begin -->\nparallel-execution-protocol: 0\nmulti-specialist-spawning: 0\nrefuter-panel: 0\nconsistency-validator: 0\nconflict-resolving-synthesis: 0\n<!-- pattern-census:end -->\n' \
    > "$r/README.md"
  printf '# Changelog\n\n## [Unreleased]\n\n## [1.2.3] - 2026-01-01\n\n## [1.0.0]\n' > "$r/CHANGELOG.md"
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

# expect_only_rule NAME RULE ROOT: like expect_rule, and no OTHER ERROR rule id may appear.
expect_only_rule() {
  local name=$1 rule=$2 r=$3 out rc=0 others
  out=$(python3 -I "$LINT" --root "$r" 2>&1) || rc=$?
  [[ $rc -eq 1 ]] || fail "$name: expected exit 1, got $rc (mutation not detected)"
  printf '%s\n' "$out" | grep -E "^ERROR .*: $rule( |\$)" >/dev/null \
    || fail "$name: output lacks rule $rule: $out"
  others=$(printf '%s\n' "$out" | grep -E '^ERROR ' \
    | sed -E 's/^ERROR [^:]*: ([A-Za-z-]+).*/\1/' | grep -vx -- "$rule" || true)
  [[ -z "$others" ]] || fail "$name: unexpected extra rule(s): $others: $out"
  printf 'PASS: %s (only)\n' "$rule"
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
expect_only_rule "missing SKILL.md" fm-missing "$m"

m=$WORK/m2; make_fixture "$m"
printf -- '---\nname: wrong\ndescription: Use when x.\n---\n' > "$m/skills/beta/SKILL.md"
expect_only_rule "renamed frontmatter name" fm-name "$m"

m=$WORK/m3; make_fixture "$m"
printf -- '---\nname: beta\n---\n# Beta\n' > "$m/skills/beta/SKILL.md"
expect_only_rule "missing description" fm-desc "$m"

m=$WORK/m4; make_fixture "$m"
rm "$m/skills/alpha/references/guide.md"
expect_only_rule "deleted referenced file" link-broken "$m"

m=$WORK/m5; make_fixture "$m"
printf 'x\n' > "$m/skills/alpha/references/unused.md"
expect_only_rule "unreferenced reference file" ref-orphan "$m"

m=$WORK/m6; make_fixture "$m"
chmod 644 "$m/skills/alpha/scripts/run.sh"
expect_only_rule "script not executable" exec-bit "$m"

m=$WORK/m7; make_fixture "$m"
mkdir "$m/skills/gamma"
printf -- '---\nname: gamma\ndescription: Use when testing gamma.\n---\n' > "$m/skills/gamma/SKILL.md"
# expect_rule: the extra skill also desyncs README/install counts (count-sync).
expect_rule "skill absent from manifest" manifest-sync "$m"

m=$WORK/m8; make_fixture "$m"
sed -i.bak 's/^EXPECTED_SKILL_COUNT=.*/EXPECTED_SKILL_COUNT=3/' "$m/install.sh"; rm -f "$m/install.sh.bak"
expect_only_rule "count constant changed" count-sync "$m"

m=$WORK/m9; make_fixture "$m"
ln -s ../beta/SKILL.md "$m/skills/alpha/link.md"
expect_only_rule "symlink added" symlink "$m"

# expect_clean NAME ROOT: linter must exit 0.
expect_clean() {
  local name=$1 r=$2 out rc=0
  out=$(python3 -I "$LINT" --root "$r" 2>&1) || rc=$?
  [[ $rc -eq 0 ]] || fail "$name: expected exit 0, got $rc: $out"
  printf 'PASS: %s\n' "$name"
}

m=$WORK/m10; make_fixture "$m"
ln -s beta "$m/skills/gamma"
printf 'alpha\nbeta\ngamma\n' > "$m/skills-list.txt"
# expect_rule: the symlinked entry also bumps the on-disk count (count-sync).
expect_rule "skill dir is symlink" symlink "$m"

m11n=0
for bs in '>' '|' '>-' '|-' '>+' '|+'; do
  m11n=$((m11n + 1)); m=$WORK/m11_$m11n; make_fixture "$m"
  printf -- '---\nname: beta\ndescription: %s\n  Use when testing beta.\n---\n# Beta\n' "$bs" \
    > "$m/skills/beta/SKILL.md"
  expect_only_rule "block scalar description '$bs'" fm-desc "$m"
done

m=$WORK/m12; make_fixture "$m"
printf -- '---\nname: beta\ndescription: Use when x.\n  continued line\n---\n# Beta\n' \
  > "$m/skills/beta/SKILL.md"
expect_only_rule "indented continuation line" fm-desc "$m"

m=$WORK/m13; make_fixture "$m"
printf '\357\273\277---\nname: beta\ndescription: Use when testing beta.\n# a comment\n\n---\n# Beta\n' \
  > "$m/skills/beta/SKILL.md"
expect_clean "BOM and comment/blank frontmatter" "$m"

m=$WORK/m14; make_fixture "$m"
printf -- '---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\nSee [g](../alpha/references/gone.md).\n' \
  > "$m/skills/beta/SKILL.md"
expect_only_rule "broken ../ link" link-broken "$m"

m=$WORK/m15; make_fixture "$m"
printf -- '---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\nSee `skills/alpha/references/gone.md`.\n' \
  > "$m/skills/beta/SKILL.md"
expect_only_rule "broken skills/ backtick path" link-broken "$m"

m=$WORK/m16; make_fixture "$m"
printf -- '---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\nSee [g](../alpha/references/guide.md#top), `skills/alpha/references/guide.md`, `../alpha/scripts/run.sh`!\nSee [x](../alpha/references/guide.md#sec) and `../alpha/SKILL.md`. Prose mention of references/nope.md is ignored.\n' \
  > "$m/skills/beta/SKILL.md"
expect_clean "valid ../ skills/ anchor punctuation and prose" "$m"

m=$WORK/m17; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee scripts/run.sh and `references/guide.md#top`, then references/gone.md#x.\n' \
  > "$m/skills/alpha/SKILL.md"
expect_clean "prose-only broken path is WARN not ERROR, anchored link ok" "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee [x](references/gone.md#x)\n' \
  > "$m/skills/alpha/SKILL.md"
printf 'x\n' > "$m/skills/alpha/references/guide.md"
# expect_rule: SKILL.md no longer mentions guide.md, so ref-orphan also fires.
expect_rule "anchor stripped before existence check" link-broken "$m"

m=$WORK/m18; make_fixture "$m"
printf 'x\n' > "$m/skills/alpha/references/a.md"
printf 'x\n' > "$m/skills/alpha/references/data.md"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md` and `references/data.md`.\n' \
  > "$m/skills/alpha/SKILL.md"
expect_only_rule "a.md not satisfied by data.md" ref-orphan "$m"

m=$WORK/m19; make_fixture "$m"
printf 'alpha\nbeta\nbeta\n' > "$m/skills-list.txt"
expect_only_rule "duplicate manifest line" manifest-sync "$m"

m=$WORK/m20; make_fixture "$m"
printf 'beta\nalpha\n' > "$m/skills-list.txt"
expect_only_rule "unsorted manifest" manifest-sync "$m"

# --- Phase 1 review coverage gaps ---

# (a) CRLF frontmatter must not error.
m=$WORK/g1; make_fixture "$m"
printf -- '---\r\nname: beta\r\ndescription: Use when testing beta.\r\n---\r\n# Beta\r\n' \
  > "$m/skills/beta/SKILL.md"
expect_clean "CRLF frontmatter" "$m"

# (b) description longer than 1024 chars.
m=$WORK/g2; make_fixture "$m"
long=$(python3 -I -c 'print("Use when " + "x" * 1030)')
printf -- '---\nname: beta\ndescription: %s\n---\n# Beta\n' "$long" > "$m/skills/beta/SKILL.md"
expect_only_rule "description over 1024 chars" fm-desc "$m"

# (c) no trigger words: ERROR, exit 1.
m=$WORK/g3; make_fixture "$m"
printf -- '---\nname: beta\ndescription: A plain description.\n---\n# Beta\n' > "$m/skills/beta/SKILL.md"
rc=0
out=$(python3 -I "$LINT" --root "$m" 2>&1) || rc=$?
[[ $rc -eq 1 ]] || fail "desc-trigger: expected exit 1, got $rc: $out"
printf '%s\n' "$out" | grep -E '^ERROR beta: desc-trigger' >/dev/null \
  || fail "desc-trigger: ERROR missing: $out"
printf '%s\n' "$out" | grep -E '^WARN beta: desc-trigger' >/dev/null && fail "desc-trigger: still a WARN: $out"
printf 'PASS: desc-trigger error\n'
# desc-trigger positive: "Use when" passes.
printf -- '---\nname: beta\ndescription: A plain description. Use when testing.\n---\n# Beta\n' > "$m/skills/beta/SKILL.md"
rc=0
out=$(python3 -I "$LINT" --root "$m" 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "desc-trigger positive: expected exit 0, got $rc: $out"
printf 'PASS: desc-trigger accepts use when\n'

# (d) README badge drift.
m=$WORK/g4; make_fixture "$m"
sed -i.bak 's/skills-2-blue/skills-3-blue/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README badge drift" count-sync "$m"

# (e) README phrase missing entirely.
m=$WORK/g5; make_fixture "$m"
sed -i.bak '/curated AI skills/d' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README phrase missing" count-sync "$m"
printf '%s\n' "$(python3 -I "$LINT" --root "$m" 2>&1 || true)" | grep -F 'pattern for' | grep -F 'not found' >/dev/null \
  || fail "README phrase missing: no 'pattern ... not found' message"

# (f) stale manifest entry (no directory).
m=$WORK/g6; make_fixture "$m"
printf 'alpha\nbeta\nzeta\n' > "$m/skills-list.txt"
expect_only_rule "stale manifest entry" manifest-sync "$m"

# (g) --skill mode checks only that skill, skips manifest-sync/count-sync.
m=$WORK/g7; make_fixture "$m"
printf 'alpha\nbeta\nzeta\n' > "$m/skills-list.txt"
sed -i.bak 's/^EXPECTED_SKILL_COUNT=.*/EXPECTED_SKILL_COUNT=9/' "$m/install.sh"; rm -f "$m/install.sh.bak"
printf -- '---\nname: wrong\ndescription: Use when x.\n---\n' > "$m/skills/beta/SKILL.md"
rc=0
out=$(python3 -I "$LINT" --root "$m" --skill alpha 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "--skill alpha: expected exit 0, got $rc: $out"
printf '%s\n' "$out" | grep -E 'manifest-sync|count-sync|beta' >/dev/null \
  && fail "--skill alpha: leaked other checks: $out"
printf '%s\n' "$out" | grep -F 'Summary: 1 skill(s) checked, 0 error(s)' >/dev/null \
  || fail "--skill alpha: unexpected summary: $out"
rc=0
out=$(python3 -I "$LINT" --root "$m" --skill beta 2>&1) || rc=$?
[[ $rc -eq 1 ]] || fail "--skill beta: expected exit 1, got $rc: $out"
printf '%s\n' "$out" | grep -E '^ERROR beta: fm-name' >/dev/null || fail "--skill beta: no fm-name: $out"
printf '%s\n' "$out" | grep -E 'manifest-sync|count-sync' >/dev/null \
  && fail "--skill beta: repo-level rule ran: $out"
printf 'PASS: --skill mode\n'

# (h) BOM-prefixed frontmatter must not yield fm-missing.
m=$WORK/g8; make_fixture "$m"
printf '\357\273\277---\nname: beta\ndescription: Use when testing beta.\n---\n# Beta\n' \
  > "$m/skills/beta/SKILL.md"
expect_clean "BOM frontmatter (no fm-missing)" "$m"

# --- Gap closure fixtures ---

# expect_warn NAME RULE ROOT: exit 0, a WARN line with the rule, and no ERROR.
expect_warn() {
  local name=$1 rule=$2 r=$3 out rc=0
  out=$(python3 -I "$LINT" --root "$r" 2>&1) || rc=$?
  [[ $rc -eq 0 ]] || fail "$name: expected exit 0, got $rc: $out"
  printf '%s\n' "$out" | grep -E "^WARN .*: $rule( |\$)" >/dev/null \
    || fail "$name: WARN $rule missing: $out"
  printf '%s\n' "$out" | grep -E '^ERROR ' >/dev/null && fail "$name: unexpected ERROR: $out"
  printf 'PASS: %s (warn)\n' "$rule"
}

m=$WORK/n1; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md` and [x](./references/missing.md).\n' \
  > "$m/skills/alpha/SKILL.md"
expect_only_rule "./ markdown link broken" link-broken "$m"

m=$WORK/n2; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md` and [x](./references/guide.md#a).\n' \
  > "$m/skills/alpha/SKILL.md"
expect_clean "valid ./ markdown link" "$m"

m=$WORK/n3; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md`. Also see references/gone.md, please.\n' \
  > "$m/skills/alpha/SKILL.md"
expect_warn "bare prose path broken" link-broken-prose "$m"

m=$WORK/n4; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md`.\n```\ncat scripts/gone.sh\n```\n' \
  > "$m/skills/alpha/SKILL.md"
expect_warn "fenced path broken" link-broken-prose "$m"

m=$WORK/n5; make_fixture "$m"
printf -- '---\nname: alpha\ndescription: Use when testing alpha.\n---\nSee `references/guide.md`, other/references/x.md, references/*.md, references/<n>.md and references/guide.md.\n```\ncp scripts/run.sh assets/${X}\n```\n' \
  > "$m/skills/alpha/SKILL.md"
rc=0
out=$(python3 -I "$LINT" --root "$m" 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "prose false-positive guards: exit $rc: $out"
printf '%s\n' "$out" | grep -E 'link-broken' >/dev/null && fail "prose false-positive guards: $out"
printf 'PASS: prose word-boundary and skip chars\n'

m=$WORK/n6; make_fixture "$m"
ln -s nowhere "$m/skills/dangling"
printf 'alpha\nbeta\ndangling\n' > "$m/skills-list.txt"
sed -i.bak 's/^EXPECTED_SKILL_COUNT=.*/EXPECTED_SKILL_COUNT=3/' "$m/install.sh"; rm -f "$m/install.sh.bak"
printf 'EXPECTED=3\n' > "$m/tests/test-installer.sh"
sed -i.bak 's/skills-2-blue/skills-3-blue/; s/^2 curated/3 curated/; s/^| `beta` | b |/| `beta` | b |\n| `dangling` | x |/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "dangling symlink under skills/" symlink "$m"

m=$WORK/n7; make_fixture "$m"
ln -s beta/SKILL.md "$m/skills/file-link"
printf 'alpha\nbeta\nfile-link\n' > "$m/skills-list.txt"
sed -i.bak 's/^EXPECTED_SKILL_COUNT=.*/EXPECTED_SKILL_COUNT=3/' "$m/install.sh"; rm -f "$m/install.sh.bak"
printf 'EXPECTED=3\n' > "$m/tests/test-installer.sh"
sed -i.bak 's/skills-2-blue/skills-3-blue/; s/^2 curated/3 curated/; s/^| `beta` | b |/| `beta` | b |\n| `file-link` | x |/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "symlink-to-file under skills/" symlink "$m"

m=$WORK/n8; make_fixture "$m"
printf -- '---\nname: beta\ndescription: Use when x.\n  more text\n  and more\n---\n# Beta\n' \
  > "$m/skills/beta/SKILL.md"
out=$(python3 -I "$LINT" --root "$m" 2>&1 || true)
printf '%s\n' "$out" | grep -F 'multi-line/block description not supported' >/dev/null \
  || fail "multi-line description: message missing: $out"
[[ $(printf '%s\n' "$out" | grep -c '^ERROR ') -eq 1 ]] || fail "multi-line description: want exactly 1 ERROR: $out"
printf 'PASS: multi-line description single error\n'

# --- stale-ref fixtures ---
m=$WORK/s1; make_fixture "$m"
printf 'Use model gpt-4o here.\n' > "$m/skills/beta/notes.md"
expect_only_rule "stale model ref" stale-ref "$m"
printf '%s\n' "$(python3 -I "$LINT" --root "$m" 2>&1 || true)" | grep -E 'notes\.md:1' >/dev/null \
  || fail "stale-ref: file:line missing"

m=$WORK/s2; make_fixture "$m"
printf 'Use model gpt-4o here. (historical)\n' > "$m/skills/beta/notes.md"
expect_clean "stale ref with (historical) marker" "$m"

m=$WORK/s3; make_fixture "$m"
printf 'Use <provider-model-id> here.\n' > "$m/skills/beta/notes.md"
expect_clean "clean file no stale ref" "$m"

m=$WORK/s4; make_fixture "$m"
printf 'ok\nbuilt on Next.js 12 and CLAUDE-3 too\n' > "$m/skills/alpha/scripts/x.py"
chmod 755 "$m/skills/alpha/scripts/x.py"
printf 'path\tlevel\treason\ttest\nskills/alpha/scripts/run.sh\tstatic\tfixture\t\nskills/alpha/scripts/x.py\tstatic\tfixture\t\n' \
  > "$m/tests/script-coverage.tsv"
expect_only_rule "stale ref in .py, case-insensitive" stale-ref "$m"
printf 'PASS: stale-ref\n'

# --- stale-ref hardening fixtures ---
stale_case() { # name expect(fail|pass) content
  local d="$WORK/sh_$1"; make_fixture "$d"
  printf '%s\n' "$3" > "$d/skills/beta/notes.md"
  if [[ $2 == fail ]]; then expect_only_rule "stale-hard $1" stale-ref "$d"
  else expect_clean "stale-hard $1" "$d"; fi
}
stale_case v1 pass 'Use claude-fable-5-1 here.'
stale_case v2 pass 'Use claude-opus-5-5 here.'
stale_case v3 pass 'Use claude-sonnet-5-5 here.'
stale_case v4 pass 'Use claude-haiku-5-5 here.'
stale_case r1 fail 'Use claude-opus-5 here.'
stale_case r2 fail 'Use claude-mythos-5 here.'
stale_case r3 pass 'Use claude-opus-5 here. (Historical)'
stale_case g1 pass 'a claude3d scene and https://x.io/aclaude-3'
stale_case c2 fail 'Use Claude 2 here.'
stale_case c3 fail 'Use claude-2 here.'
stale_case c4 fail 'Use claude-instant here.'
stale_case n1 fail 'Built on Next.js 12.3 today.'
stale_case n2 fail 'Built on Next.js 13 today.'
stale_case n3 pass 'Built on Next.js 13.4 today.'
stale_case n4 pass 'Built on Next.js 14 today.'
d=$WORK/sh_ext; make_fixture "$d"
printf 'const m = "gpt-4o";\n' > "$d/skills/beta/a.ts"
expect_only_rule "stale-hard .ts scanned" stale-ref "$d"
d=$WORK/sh_multi; make_fixture "$d"
printf 'gpt-4o and claude-mythos-5\n' > "$d/skills/beta/notes.md"
[[ $(python3 -I "$LINT" --root "$d" 2>&1 | grep -c '^ERROR .*stale-ref') -eq 2 ]] || fail "stale-hard: want 2 matches on one line"
printf 'PASS: stale-ref hardening\n'

# --- model-id allow-list fixtures ---
stale_case m1 pass 'Use claude-opus-5-5-20260101 here.'
stale_case m2 fail 'Use claude-opus-5-1 here.'
stale_case m3 fail 'Use claude-opus-4-5 here.'
stale_case m4 fail 'Use claude-mythos-5 here.'
stale_case m5 pass 'Use claude-opus-4-5 here. (historical)'
stale_case m6 fail 'Use claude-sonnet-5-5-beta here.'
stale_case m7 fail 'Ask Claude Mythos about it.'
stale_case m8 fail 'Use claude_3_opus here.'
stale_case m10 pass 'See claude-opus-5-5.md for details.'
stale_case m11 pass 'Pinned to claude-opus-5-5.'
stale_case m12 pass 'Pinned (claude-opus-5-5) here.'
stale_case m13 pass 'Use claude-sonnet-5-5-v2 here.'
stale_case m14 fail 'Use claude-opus-5-5-20269999 here.'
stale_case m15 fail 'Use claude-opus-5.5 here.'
stale_case m9 pass 'Use claude-haiku-5-5. Then claude-fable-5-1, done.'
printf 'PASS: model-id allow-list\n'

# --- skill-ref fixtures ---
skill_case() { # name expect(fail|pass) skillmd-body ; description fixed unless 4th arg
  local d=$WORK/sr_$1; make_fixture "$d"
  printf -- '---\nname: beta\ndescription: %s\n---\n# Beta\n%s\n' \
    "${4:-Use when testing beta.}" "$3" > "$d/skills/beta/SKILL.md"
  if [[ $2 == fail ]]; then expect_only_rule "skill-ref $1" skill-ref "$d"
  else expect_clean "skill-ref $1" "$d"; fi
}
skill_case s1 fail '**Related skills:** `ghost-skill`'
skill_case s2 pass '**Related skills:** `alpha`'
skill_case s3 fail 'x' 'Use when testing beta. Not for X: use `ghost-skill`.'
skill_case s4 pass 'x' 'Use when testing beta. Not for X: use `alpha`.'
skill_case s5 pass 'Run `docker-compose up` first.'
skill_case s6 fail 'For that, route to `ghost-skill` instead.'
skill_case s7 pass 'Instead run `docker-compose` or `kubectl`.'
skill_case s8 pass 'x' 'Use when testing beta. Use `kubectl` to deploy.'
mkdir -p "$WORK/sr_s9/skills/beta/references" 2>/dev/null; make_fixture "$WORK/sr_s9"; mkdir -p "$WORK/sr_s9/skills/beta/references"; : > "$WORK/sr_s9/skills/beta/references/a.md"
skill_case_keep() { printf -- '---\nname: beta\ndescription: %s\n---\n# Beta\nx\n' "$1" > "$WORK/sr_s9/skills/beta/SKILL.md"; expect_clean "skill-ref s9" "$WORK/sr_s9"; }
skill_case_keep 'Use when testing beta. See `references/a.md`.'
skill_case s10 pass 'Run `kubectl-neat` instead.'
skill_case s11 pass 'Set `max-retries` and `read-only` instead of defaults.'
skill_case s12 fail 'Please use `ghost-skill` instead.'
skill_case s13 pass 'x' 'Use when testing beta. Use `docker-compose` locally.'
printf 'PASS: skill-ref\n'

# script-untested: registry tests/script-coverage.tsv (path<TAB>level<TAB>reason<TAB>test).
SC_HDR='path\tlevel\treason\ttest\n'
add_script() { # add_script ROOT RELPATH
  printf '#!/usr/bin/env bash\ntrue\n' > "$1/$2"; chmod 755 "$1/$2"
}
m=$WORK/su1; make_fixture "$m"; add_script "$m" skills/alpha/scripts/extra.sh
expect_only_rule "unregistered script" script-untested "$m"

m=$WORK/su2; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/gone.sh\tstatic\tx\t\nskills/alpha/scripts/run.sh\tstatic\tfixture\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "stale registry row" script-untested "$m"

m=$WORK/su3; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tstatic\t\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "static without reason" script-untested "$m"

m=$WORK/su4; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tsmoke\tx\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "unknown level" script-untested "$m"

m=$WORK/su5; make_fixture "$m"; rm "$m/tests/script-coverage.tsv"
expect_only_rule "missing registry" script-untested "$m"

m=$WORK/su6; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "behavior without test" script-untested "$m"

m=$WORK/su7; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\ttests/nope.sh\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "behavior test file missing" script-untested "$m"

m=$WORK/su8; make_fixture "$m"; printf 'echo other\n' > "$m/tests/t.sh"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\ttests/t.sh\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "behavior test lacks basename" script-untested "$m"

m=$WORK/su9; make_fixture "$m"; printf 'bash skills/alpha/scripts/run.sh\n' > "$m/tests/t.sh"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\ttests/t.sh\n' > "$m/tests/script-coverage.tsv"
expect_clean "script-untested behavior row valid" "$m"

m=$WORK/su10; make_fixture "$m"; add_script "$m" skills/alpha/scripts/b.sh
printf "$SC_HDR"'skills/alpha/scripts/b.sh\thelp\t\t\nskills/alpha/scripts/run.sh\tstatic\tfixture\t\n' > "$m/tests/script-coverage.tsv"
expect_clean "script-untested help+static valid" "$m"

m=$WORK/su11; make_fixture "$m"; add_script "$m" skills/alpha/scripts/b.sh
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tstatic\tfixture\t\nskills/alpha/scripts/b.sh\thelp\t\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "unsorted registry" script-untested "$m"

m=$WORK/su12; make_fixture "$m"; mkdir -p "$m/skills/alpha/scripts/__pycache__" "$m/skills/alpha/tests"
: > "$m/skills/alpha/scripts/__pycache__/x.pyc"; : > "$m/skills/alpha/tests/test_x.py"
expect_clean "pycache and skill tests dir ignored" "$m"
printf 'PASS: script-untested\n'

m=$WORK/su13; make_fixture "$m"; printf '# run.sh is not tested here\n' > "$m/tests/t.sh"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\ttests/t.sh\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "behavior mention only in comment" script-untested "$m"

m=$WORK/su14; make_fixture "$m"; printf '  # run.sh here\nbash skills/alpha/scripts/run.sh\n' > "$m/tests/t.sh"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\ttests/t.sh\n' > "$m/tests/script-coverage.tsv"
expect_clean "behavior real invocation passes" "$m"

m=$WORK/su15; make_fixture "$m"; printf 'bash skills/alpha/scripts/run.sh\n' > "$WORK/t.sh"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\t../t.sh\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "test path with .." script-untested "$m"

m=$WORK/su16; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/../scripts/run.sh\tstatic\tfixture\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "unnormalized registry path" script-untested "$m"

m=$WORK/su17; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tstatic\tfixture\t\nskills/alpha/scripts/run.sh\tstatic\tfixture\t\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "duplicate registry row" script-untested "$m"

m=$WORK/su18; make_fixture "$m"
printf "$SC_HDR"'skills/alpha/scripts/run.sh\tbehavior\t\t/etc/hosts\n' > "$m/tests/script-coverage.tsv"
expect_only_rule "absolute test path" script-untested "$m"
printf 'PASS: script-untested hygiene\n'

# readme-skills and version-sync.
m=$WORK/rs1; make_fixture "$m"
sed -i.bak '/^| `beta`/d' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "skill missing from README arsenal" readme-skills "$m"

m=$WORK/rs2; make_fixture "$m"
sed -i.bak 's/^| `beta` | b |/| `beta` | b |\n| `beta` | again |/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "skill duplicated in README arsenal" readme-skills "$m"

m=$WORK/rs3; make_fixture "$m"
sed -i.bak 's/^| `beta` | b |/| `beta` | b |\n| `ghost` | g |/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README row for nonexistent skill" readme-skills "$m"

m=$WORK/rs4; make_fixture "$m"
sed -i.bak 's/^## Other/## Other\n\nSee `ghost` and `beta`./' "$m/README.md"; rm -f "$m/README.md.bak"
expect_clean "backticked names outside arsenal ignored" "$m"

m=$WORK/rs5; make_fixture "$m"
sed -i.bak '/^## The Arsenal/d' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README arsenal section missing" readme-skills "$m"

m=$WORK/vs1; make_fixture "$m"
printf '# Changelog\n\n## [Unreleased]\n\n## [1.2.2] - 2026-01-01\n' > "$m/CHANGELOG.md"
expect_only_rule "VERSION != CHANGELOG" version-sync "$m"

m=$WORK/vs2; make_fixture "$m"
sed -i.bak 's/^Installer version: 1.2.3/Installer version: 1.2.2/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README installer version mismatch" version-sync "$m"

m=$WORK/vs3; make_fixture "$m"
printf '# Changelog\n\n## [Unreleased]\n' > "$m/CHANGELOG.md"
expect_only_rule "CHANGELOG has no release section" version-sync "$m"

m=$WORK/vs4; make_fixture "$m"
sed -i.bak '/^Installer version/d' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README lacks installer version phrase" version-sync "$m"

m=$WORK/vs5; make_fixture "$m"
sed -i.bak '/^VERSION=/d' "$m/install.sh"; rm -f "$m/install.sh.bak"
expect_only_rule "install.sh lacks VERSION" version-sync "$m"
printf 'PASS: readme-skills and version-sync fixtures\n'

# readme-patterns and readme-flags.
m=$WORK/rp1; make_fixture "$m"
sed -i.bak 's/^refuter-panel: 0/refuter-panel: 5/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "census number mismatch" readme-patterns "$m"

m=$WORK/rp2; make_fixture "$m"
sed -i.bak '/pattern-census:begin/,/pattern-census:end/d' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "census block missing" readme-patterns "$m"

m=$WORK/rp3; make_fixture "$m"
printf '# Beta\nRun one Consistency Validator Agent.\n' >> "$m/skills/beta/SKILL.md"
sed -i.bak 's/^consistency-validator: 0/consistency-validator: 1/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_clean "census numbers match a real hit" "$m"

m=$WORK/rf1; make_fixture "$m"
sed -i.bak 's/--help   h\\n"/--help   h\\n  --beta  b\\n"/' "$m/install.sh"; rm -f "$m/install.sh.bak"
expect_only_rule "installer flag undocumented in README" readme-flags "$m"

m=$WORK/rf2; make_fixture "$m"
sed -i.bak 's/^Run `--alpha` again\./Run `--alpha` and `--ghost`./' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README flag unknown to install.sh" readme-flags "$m"

m=$WORK/rf3; make_fixture "$m"
expect_clean "README flags consistent with install.sh" "$m"
m=$WORK/rf4; make_fixture "$m"
printf '# supports --ghost soon\n' >> "$m/install.sh"
sed -i.bak 's/^Run `--alpha` again\./Run `--alpha` and `--ghost`./' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README flag present only in an install.sh comment" readme-flags "$m"

m=$WORK/rf5; make_fixture "$m"
sed -i.bak 's/^Run `--alpha` again\./Run `--alpha` and `--alp`./' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "README flag is only a prefix of a real flag" readme-flags "$m"

m=$WORK/rp4; make_fixture "$m"
sed -i.bak 's/$/\r/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_clean "CRLF README census block passes" "$m"

m=$WORK/rp5; make_fixture "$m"
sed -i.bak 's/^refuter-panel: 0/refuter-panel: 0\nrefuter-panel: 0/' "$m/README.md"; rm -f "$m/README.md.bak"
expect_only_rule "duplicate census key" readme-patterns "$m"
printf 'PASS: readme-patterns and readme-flags fixtures\n'

# Real repo must be clean.
rc=0
out=$(python3 -I "$LINT" --root "$ROOT" 2>&1) || rc=$?
[[ $rc -eq 0 ]] || fail "real repo lint failed (exit $rc): $out"
printf 'PASS: real repo clean\n'
