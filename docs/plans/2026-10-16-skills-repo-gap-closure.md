# lzr1-skills Gap Closure Implementation Plan

> **For implementers:** Use ring:dispatching-workflows (rolling-phase: elaborate
> the current phase against the real code, run it as a reviewed multi-agent
> workflow, then elaborate the next phase — repeat), or ring:running-dev-cycle
> for the full subagent-orchestrated workflow.
> This document is the living source of truth — task elaboration for later
> phases is written back into it during execution.

**Goal:** Close the governance, validation, test, freshness, overlap and distribution gaps found in the 2026-10-16 audit of lzr1-skills, so the 86-skill catalog is machine-verified, current and safely distributable.

**Architecture:** Guardrails first. Phase 1 adds a stdlib-only catalog linter, CI and the missing repo-governance files, and fixes the defects the linter immediately finds, so every later content change is protected by a gate. Later phases then use that gate to refresh stale content, resolve overlapping skills, deepen script tests, and harden the install path.

**Tech Stack:** Bash 3.2+ (install.sh, tests), Python 3 stdlib (linter, run with `-I`), GitHub Actions, shellcheck.

## Audit Summary (evidence for this plan)

Scope of the audit: structure, metadata, links, scripts, tests, installer, README claims, and keyword scans across all 86 skills (596 tracked files under `skills/`, plus `install.sh`, `tests/`, `skills-list.txt`, `README.md`). It did NOT read every reference file's prose for technical correctness; Phase 2 covers that by sampling and by targeted scans.

| # | Gap | Evidence | Phase |
|---|-----|----------|-------|
| G1 | No `LICENSE` although README badge claims MIT; no CI; no CONTRIBUTING, SECURITY or CHANGELOG | `git ls-files` shows only `.gitattributes`, `README.md`, `install.sh`, `skills-list.txt`, `tests/` at root | 1 |
| G2 | No catalog-level validation. Frontmatter, link, orphan-reference and exec-bit checks are manual | Tests only cover the installer (`tests/test-installer.sh`, `tests/test-adversarial-remediations.sh`) | 1 |
| G3 | Skill count 86 is hardcoded in several places that can drift | `install.sh:12`, `tests/test-installer.sh:9`, README badge and headline | 1 |
| G4 | `legendary-readme` lists 11 reference files but `SKILL.md` names 2; 9 are undiscoverable orphans | audit script: 9 orphan refs, all in `legendary-readme` | 1 |
| G5 | `skills/gcalendar/scripts/batch_updater.py` is mode 100644 while sibling scripts are 100755 | `git ls-files -s skills/gcalendar/scripts` | 1 |
| G6 | Script test coverage is thin: 90 files under `scripts/` (55 sh, 31 py, plus one each js, mts, sql, txt) and only 4 skills ship tests (`coderabbit-reviewer`, `hermes-agent`, `security-review`, `yaml-specialist`); `shellcheck` is not installed locally and not run anywhere | file census | 3 |
| G7 | Stale model/version content | `ai-ml-engineering/references/{llm-applications,prompt-engineering,computer-vision,source-map}.md` cite Claude 3.5, GPT-4o, Gemini 1.5, `claude-3-5-sonnet-20240620`; `frontend/references/nextjs-app-router.md:4` frames App Router as "new paradigm ... Next.js 13" | 2 |
| G8 | Overlapping skills with no routing guidance: `redis-valkey`/`valkey-redis`, `devops`/`devops-infrastructure`, `prompt`/`prompt-master`, `masterclaw`/`openclaw`/`nemoclaw`/`bot`, `postgres-15`/`sql-partitioning`/`database`, `docker`/`dockerfile` | `skills-list.txt` and README tables | 2 |
| G9 | Uneven trigger quality: several `description:` lines are one-line feature blurbs with no "Use when" trigger (e.g. `legendary-readme`); thin skills (`claude`, `go-lua`, `openclaw` have 2 files each) | frontmatter scan | 2 |
| G10 | Only one Lerian-specific skill (`lerian-helm`) despite Lerian stack depth (Go/Fiber/Huma, Midaz, multi-tenancy). Needs an owner decision on scope vs. the separate ring plugin | org context, `git grep Lerian` | 4 |
| G11 | Distribution trust: installer pulls the mutable `main` tarball (`install.sh:5-6`), no release tags, no checksum | `install.sh` header | 4 |

## Phase Overview

| Phase | Milestone | Epics | Status |
|-------|-----------|-------|--------|
| 1 | Catalog is machine-verified in CI; governance files exist; known structural defects fixed | 1.1, 1.2, 1.3 | Detailed |
| 2 | Content is current, overlaps are routed, descriptions trigger reliably | 2.1, 2.2, 2.3 | Epic-level |
| 3 | Every shipped script has lint + smoke coverage | 3.1, 3.2 | Epic-level |
| 4 | Install path is pinned and verifiable; Lerian skill scope decided and delivered | 4.1, 4.2 | Epic-level |

---

## Phase 1: Guardrails and governance

### Epic 1.1: Catalog linter

**Goal:** `python3 -I scripts/lint_catalog.py` verifies the structural invariants of the whole catalog and exits non-zero on any violation.
**Scope:** `scripts/` (new), `tests/`
**Dependencies:** none
**Done when:** linter runs clean on the current tree after Epic 1.3 lands; a negative-fixture test proves each rule can fail; `tests/test-catalog.sh` runs both
**Status:** Pending

#### Task 1.1.1: Write the linter

- [ ] Done

**Context:** The audit was done with an ad-hoc script; its rules must become a permanent gate. Skills live at `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`). The installer already enforces manifest sync at `install.sh:361-398` (sorted, no duplicates, exact match to `skills/*/SKILL.md`), so the linter must not re-implement the installer, only add checks the installer lacks. No `scripts/` directory exists at repo root yet.

**Implementation vision:** One file, Python 3 stdlib only, no PyYAML (parse the frontmatter by hand: the block between the first two `---` lines, `key: value` lines only; reject a skill whose frontmatter needs anything fancier, since the installer's own tooling treats it the same way). Walk `skills/` with `os.walk`, not subprocess, so it works outside git. Accept `--root PATH` (default: repo root derived from the script location) so tests can point it at fixtures. Rules, each emitting `ERROR <skill>: <rule-id> <detail>` or `WARN ...`, with a final summary and exit 1 if any ERROR:
- `fm-missing`: no frontmatter block. `fm-name`: `name` absent or not equal to the directory name. `fm-desc`: `description` absent, empty, or over 1024 characters.
- `link-broken`: any `references/`, `scripts/`, `templates/`, `assets/` path in a markdown link or backtick span inside SKILL.md that does not exist on disk. Skip tokens containing `*`, `<`, `{`, `$` (placeholders and globs).
- `ref-orphan`: a file under `references/` whose basename does not appear anywhere in that skill's SKILL.md.
- `exec-bit`: a `*.sh` or `*.py` under `scripts/` that is not executable (`os.access(path, os.X_OK)` on the working tree).
- `manifest-sync`: set of skill directories differs from lines in `skills-list.txt` (message lists both diffs).
- `count-sync`: the integer `EXPECTED_SKILL_COUNT` in `install.sh`, `EXPECTED` in `tests/test-installer.sh`, the `skills-<N>-` badge in README.md, and the `<N> curated AI skills` phrase in README.md must all equal the directory count. Extract each with a regex; a missing pattern is itself an ERROR (so a README rewrite cannot silently disable the check).
- `desc-trigger` (WARN only in Phase 1): description does not contain `use when` or `use for` or `triggers`, case-insensitive. Phase 2 promotes it to ERROR.
Edge cases reachable: a skill dir without SKILL.md (report `fm-missing`, skip other rules for it); symlinks inside `skills/` (report `symlink` ERROR; the installer rejects them at copy time, so the linter should catch them earlier); CRLF line endings in frontmatter (strip `\r` before parsing, do not error).

**Files:**
- Create: `scripts/lint_catalog.py` (mode 100755)

**Verification:** `python3 -I scripts/lint_catalog.py` on the unmodified tree must report exactly the defects from G3-G5 that are real at that moment: 9 `ref-orphan` for `legendary-readme`, 1 `exec-bit` for `gcalendar/scripts/batch_updater.py`, WARNs for `desc-trigger`, and no other ERROR. If it reports anything else, either the rule is wrong or there is a defect the audit missed; investigate before proceeding.

**Done when:** the linter reproduces the audit's findings and nothing it flags is a false positive.

#### Task 1.1.2: Negative-fixture tests for the linter

- [ ] Done

**Context:** A linter that has never failed is unproven. `tests/test-installer.sh` shows the house style: `set -euo pipefail`, `mktemp -d` work dir with a trap cleanup, `fail()` helper, no external deps.

**Implementation vision:** `tests/test-catalog.sh` builds a minimal fixture root in a temp dir (two skills, a manifest, stub `install.sh` and `tests/test-installer.sh` carrying the count constants, a stub README with the badge and phrase), asserts the linter passes on it, then for each rule mutates the fixture in one way and asserts the linter exits 1 and prints that rule id. Mutations: rename frontmatter name; delete a referenced file; add an unreferenced reference file; `chmod -x` a script; add a skill dir absent from the manifest; change one count constant; add a symlink. Finally run the real linter against the real repo root and assert exit 0 (this assertion is expected to fail until Epic 1.3 lands; order tasks accordingly, see Dependencies on 1.3).

**Files:**
- Create: `tests/test-catalog.sh` (mode 100755)

**Verification:** `bash tests/test-catalog.sh` prints one PASS line per rule and exits 0 once Epic 1.3 is done; before that, only the final real-repo assertion fails.

**Done when:** every ERROR rule has a fixture that triggers it.

### Epic 1.2: CI and governance files

**Goal:** Every push and PR runs the test suite on Linux and macOS, and the repo carries the files a public repo is expected to have.
**Scope:** `.github/workflows/`, repo root docs
**Dependencies:** Epic 1.1 (CI runs the linter)
**Done when:** the workflow file passes `actionlint` locally or on its first run; LICENSE, CONTRIBUTING.md, SECURITY.md and CHANGELOG.md exist and are linked from README
**Status:** Pending

#### Task 1.2.1: CI workflow

- [ ] Done

**Context:** There is no `.github/` directory. `install.sh` targets macOS and Linux with Bash 3.2+, so the matrix must include macOS (ships Bash 3.2) and Ubuntu. Tests are plain bash scripts that need no setup. `shellcheck` is not installed on the author's machine.

**Implementation vision:** `.github/workflows/ci.yml`, triggers `push` to `main` and `pull_request`. Single job `test` with matrix `os: [ubuntu-latest, macos-latest]`, `permissions: contents: read`. Steps: `actions/checkout` pinned to a full commit SHA (look the SHA up at implementation time and record the tag in a trailing comment), then `python3 -I scripts/lint_catalog.py`, `bash tests/test-catalog.sh`, `bash tests/test-installer.sh`, `bash tests/test-adversarial-remediations.sh`. A second job `shellcheck` on ubuntu runs `shellcheck -x install.sh tests/*.sh` and, as a non-blocking informational step for now, `shellcheck` over `skills/*/scripts/*.sh` (Phase 3 makes that blocking). No secrets, no network beyond checkout. Set `concurrency` to cancel superseded runs on the same ref.

**Files:**
- Create: `.github/workflows/ci.yml`

**Verification:** `actionlint .github/workflows/ci.yml` (install via `brew install actionlint` if absent) exits 0. First real run is confirmed green on a PR in Task 1.3.3.

**Done when:** workflow lints clean and encodes the four test commands plus shellcheck.

#### Task 1.2.2: LICENSE and governance docs

- [ ] Done

**Context:** README line 6 shows `license-MIT` linking to `LICENSE`, which does not exist, so the badge is a dead link and the repo is legally all-rights-reserved. The git author is Victor Hugo Lazari. Contributing guidance currently lives only in a README "Contributing" section.

**Implementation vision:** Decision already made: MIT, matching the README claim; copyright line `Copyright (c) 2026 Victor Hugo Lazari`. Add `CONTRIBUTING.md` documenting the skill authoring contract the linter enforces (frontmatter rules, every reference named in SKILL.md, scripts executable, how to add a skill: create dir, add to `skills-list.txt` in sorted order, bump the count in the four places the linter checks, run the three test commands). Add `SECURITY.md` with a private-report channel (GitHub private vulnerability reporting, enabled in repo settings as a manual step noted in the file) and a statement of scope: installer integrity and skill scripts. Add `CHANGELOG.md` in Keep a Changelog format seeded with `## [Unreleased]` and a `## [2.0.0]` entry matching `VERSION="2.0.0"` at `install.sh:10`. Link all four from the README footer. Do not restate the linter rules in prose beyond a short list pointing at `scripts/lint_catalog.py` as the source of truth.

**Files:**
- Create: `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`
- Modify: `README.md` (footer links; existing "Contributing" section points to `CONTRIBUTING.md`)

**Verification:** `test -f LICENSE && grep -q 'MIT License' LICENSE && grep -q 'CONTRIBUTING.md' README.md` exits 0.

**Done when:** badge link resolves, and a new contributor can add a skill using only CONTRIBUTING.md.

### Epic 1.3: Fix the defects the linter finds

**Goal:** The linter passes with zero ERRORs on the real tree.
**Scope:** `skills/legendary-readme/SKILL.md`, `skills/gcalendar/scripts/`, `tests/test-installer.sh`
**Dependencies:** Task 1.1.1 (so findings are reproducible); must land before the final assertion in Task 1.1.2 and before CI is enforced
**Done when:** `python3 -I scripts/lint_catalog.py` exits 0; `bash tests/test-catalog.sh` exits 0
**Status:** Pending

#### Task 1.3.1: Make legendary-readme references discoverable

- [ ] Done

**Context:** `skills/legendary-readme/SKILL.md` is 35 lines and names only `visual-arsenal.md`, `sections-encyclopedia.md` and two templates. Nine of its eleven reference files are never mentioned, so an agent following the skill cannot know they exist: `complete-reference.md`, `tone-and-voice.md`, `universal-readability.md`, `visual-style-system.md`, `reading-list.md`, `theme-engine.md`, `char-art-and-animation.md`, `hall-of-fame.md`, `tables-diagrams-workflows.md`. The recent commit `f26ad0e` added the char-art/animation toolkit and visual references without wiring them in. The skill also has six templates under `templates/`; confirm the template list in SKILL.md matches them.

**Implementation vision:** Open each of the nine files, read its first heading and opening paragraph, and add a "Reference Map" section to SKILL.md: one line per file stating the task that should trigger reading it (e.g. char-art-and-animation: when the user asks for ASCII/animated banners). Keep "Required References" limited to the two that are always needed; the new map is on-demand. Rewrite the `description:` so it contains a trigger ("Use when ... README ...") while keeping it under 1024 characters. Update the Workflow step 3 and 4 to point at the relevant map entries (theme-engine for light/dark, tables-diagrams-workflows for diagrams). Reconcile the templates list with `ls skills/legendary-readme/templates`.

**Files:**
- Modify: `skills/legendary-readme/SKILL.md`

**Verification:** `python3 -I scripts/lint_catalog.py --skill legendary-readme` (add a `--skill NAME` filter in Task 1.1.1, which is cheap and used here) reports no `ref-orphan` and no `desc-trigger` for this skill.

**Done when:** all 11 reference files and all templates are named in SKILL.md with a when-to-read hint.

#### Task 1.3.2: Fix gcalendar exec bit and single-source the count

- [ ] Done

**Context:** `skills/gcalendar/scripts/batch_updater.py` is 100644, its sibling `validate_events.py` is 100755. The count `86` appears in `install.sh:12`, `tests/test-installer.sh:9`, and the README; the installer's constant is a deliberate tamper check and stays.

**Implementation vision:** `chmod +x` the script and `git update-index --chmod=+x` so the mode is recorded. Leave `install.sh` and the README count as they are; the `count-sync` rule is what prevents drift. Change `tests/test-installer.sh:9` to derive `EXPECTED` from `wc -l < "$ROOT/skills-list.txt"` (trimmed) instead of a literal, so only the installer constant and the README need manual bumps; note this in CONTRIBUTING.md (Task 1.2.2) and update the linter's `count-sync` rule to treat that line as "derived" (skip it) only if it matches the derivation pattern, otherwise still compare a literal. Verify `test-adversarial-remediations.sh` does not also hardcode a count (it had none in the grep, confirm).

**Files:**
- Modify: `skills/gcalendar/scripts/batch_updater.py` (mode only), `tests/test-installer.sh:9`, `scripts/lint_catalog.py` (derivation-aware count rule)

**Verification:** `git ls-files -s skills/gcalendar/scripts` shows 100755 for both scripts; `bash tests/test-installer.sh` exits 0.

**Done when:** exec-bit rule clean and the test count is derived.

#### Task 1.3.3: First green CI run

- [ ] Done

**Context:** Tasks 1.1-1.3 produce a branch that should pass everything. CI has never run.

**Implementation vision:** Push the Phase 1 branch (never directly to `main`; the repo's HEAD is `main`, so branch first), open a PR, and confirm both matrix legs and the shellcheck job. Expected first-run failure modes to handle: macOS Bash 3.2 incompatibilities in the new `tests/test-catalog.sh` (no `mapfile`, no associative arrays), Linux/macOS `sed -i` and `mktemp` differences, and shellcheck findings in `install.sh` and existing tests. Fix findings in the file that caused them. Do not blanket-disable shellcheck codes; a targeted `# shellcheck disable=SCxxxx` with a one-line reason is acceptable only where the construct is intentional.

**Files:**
- Modify: whichever files CI flags (expected: `tests/test-catalog.sh`, possibly `install.sh` and existing tests)

**Verification:** `gh pr checks` shows `test (ubuntu-latest)`, `test (macos-latest)` and `shellcheck` all passing.

**Done when:** PR is green on all three checks; the branch protection recommendation (require these checks on `main`) is noted in the PR body for the repo owner to apply.

---

## Phase 2: Content freshness and routing

### Epic 2.1: Stale model and version references

**Goal:** No skill recommends retired or superseded models or versions as current.
**Scope:** `skills/ai-ml-engineering/references/`, `skills/claude/`, `skills/openai/`, `skills/prompt*/`, `skills/frontend/references/`, `skills/go*/`, `skills/database/`, `skills/postgres-15/`
**Dependencies:** Phase 1
**Done when:** a repo-wide scan for known-stale identifiers (Claude 3.x, `claude-3-*`, GPT-4o, Gemini 1.5, Next.js 13-framing, Go versions below the supported set) returns only intentional historical mentions, each annotated; the scan is a linter rule so it cannot regress
**Status:** Pending

### Epic 2.2: Overlap resolution and routing

**Goal:** For each overlapping skill group (G8), the owner decision is applied and each skill's description states when to choose it over its neighbours.
**Scope:** `redis-valkey`/`valkey-redis`, `devops`/`devops-infrastructure`, `prompt`/`prompt-master`, `masterclaw`/`openclaw`/`nemoclaw`/`bot`, `postgres-15`/`sql-partitioning`/`database`, `docker`/`dockerfile`, README tables, `skills-list.txt`, installer count
**Dependencies:** Phase 1; an owner decision per group (merge, keep-and-differentiate, or deprecate). Merging changes the skill count in four places, which the `count-sync` rule will enforce.
**Done when:** each group has a recorded decision in CHANGELOG.md and no two skills have interchangeable descriptions
**Status:** Pending

### Epic 2.3: Description and depth pass

**Goal:** Every `description:` carries a trigger, and thin skills (`claude`, `go-lua`, `openclaw` at two files each, plus the smallest SKILL.md files) reach the catalog's median depth or are folded into a neighbour.
**Scope:** all 86 `SKILL.md` frontmatter; the thin skills named above
**Dependencies:** Epic 2.2 (do not deepen a skill that is about to be merged)
**Done when:** `desc-trigger` is promoted from WARN to ERROR and passes
**Status:** Pending

---

## Phase 3: Script test depth

### Epic 3.1: Static analysis gate for all scripts

**Goal:** `shellcheck` (sh) and `python3 -m py_compile` plus a pinned linter (ruff) (py) pass on all 55 shell and 31 Python scripts, blocking in CI.
**Scope:** `skills/*/scripts/`, `.github/workflows/ci.yml`; macOS portability of `coderabbit-reviewer` scripts and installer tests (`sha256sum` with `shasum -a 256` fallback, replace `realpath -e`) so the installer suites can return to the macOS CI leg
**Dependencies:** Phase 1 (CI exists)
**Done when:** the informational shellcheck step from Task 1.2.1 is made blocking and green
**Status:** Pending

### Epic 3.2: Smoke tests per script

**Goal:** Every script has a `--help` or dry-run smoke test and, for scripts that mutate state or touch credentials (`nemoclaw`, `gcalendar`, `tomate-pos80`, `meeting-engineering`), a test of the safe path in an isolated `HOME`, following the pattern in `tests/test-adversarial-remediations.sh` (mode assertions on credential files).
**Scope:** `tests/`, per-skill `tests/` where a skill already has one
**Dependencies:** Epic 3.1
**Done when:** the catalog linter gains a `script-untested` WARN listing any script not referenced by a test, and the list is empty
**Status:** Pending

---

## Phase 4: Distribution and Lerian coverage

### Epic 4.1: Pinned, verifiable install

**Goal:** `curl | bash` installs a tagged release with a verified checksum instead of the mutable `main` tarball.
**Scope:** `install.sh` (`BRANCH`, `ARCHIVE_URL`, `download_file`, `validate_archive_listing`), release workflow, README install section, CHANGELOG
**Dependencies:** Phase 1 (CI, CHANGELOG); decision on signing (checksum only vs. checksum plus signature)
**Done when:** a tag push publishes a tarball and `SHA256SUMS`; installer defaults to the latest tag, verifies the checksum before extracting, and keeps an explicit `--ref main` escape hatch; the installer tests cover a corrupted-archive failure
**Status:** Pending

### Epic 4.2: Lerian skill scope

**Goal:** A decision, then delivery, on which Lerian-specific skills belong in this public catalog versus the separate ring plugin.
**Scope:** `skills/lerian-helm`, candidate new skills (Go service conventions, Midaz ledger modelling, multi-tenancy), licensing review of anything derived from non-public Lerian material
**Dependencies:** owner decision; confirmation that the content is publishable under the MIT license added in Task 1.2.2 (Midaz and Tracer are ELv2, Lerian products are mostly closed source, so copying their internals into an MIT repo is a legal question, not a technical one)
**Done when:** decision recorded in CHANGELOG.md; any approved skills pass the linter and ship with tests
**Status:** Pending

---

## Self-Review

- **Spec coverage:** the request was "find all gaps and how to fix them". G1-G11 each map to an epic: G1 to 1.2, G2/G3 to 1.1 and 1.3.2, G4/G5 to 1.3, G6 to 3.1/3.2, G7 to 2.1, G8 to 2.2, G9 to 2.3, G10 to 4.2, G11 to 4.1.
- **Vagueness scan:** Phase 1 tasks name exact files, rule ids and commands. Phase 2-4 are epic-level by design; their open decisions (merge vs. differentiate, signing, Lerian scope) are listed under Dependencies, not hidden.
- **Contract consistency:** rule ids (`fm-name`, `ref-orphan`, `exec-bit`, `count-sync`, `desc-trigger`) are defined in Task 1.1.1 and referenced by 1.1.2, 1.3.1, 1.3.2, 2.3 and 3.2. Task 1.3.1 depends on a `--skill NAME` flag that is part of Task 1.1.1's scope.
- **Ordering hazard:** Task 1.1.2's real-repo assertion fails until Epic 1.3 lands. Execute 1.1.1, then 1.3.1 and 1.3.2, then 1.1.2, then Epic 1.2.
- **Phase boundaries:** each phase leaves the repo installable and green.
- **Known limitation:** the audit verified structure, metadata, links, scripts and stale-keyword scans, not the technical accuracy of every reference file. The README's "Pattern A/B/C" parallel-agent claims were not machine-verified; Epic 2.3 should add a check that skills claiming a protocol actually contain it.

---

## Deviations

- **Task 1.2.1 CI matrix (decided in fix pass):** the pre-existing `skills/coderabbit-reviewer` scripts and the installer tests use `sha256sum` and `realpath -e`, which are absent on stock macOS, so `tests/test-installer.sh` and `tests/test-adversarial-remediations.sh` fail on the macOS leg. Decision: the hardened coderabbit scripts are not modified in Phase 1. The macOS leg runs only the portable checks (`python3 -I scripts/lint_catalog.py`, `bash tests/test-catalog.sh`); the installer and remediation suites run on ubuntu only; the shellcheck job is kept. The portability work (`sha256sum` to `shasum -a 256` fallback, `realpath -e` replacement) is an explicit item in Epic 3.1 scope.
