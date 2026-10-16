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
| 1 | Catalog is machine-verified in CI; governance files exist; known structural defects fixed | 1.1, 1.2, 1.3 | Complete |
| 2 | Content is current, overlaps are routed, descriptions trigger reliably | 2.1, 2.2, 2.3 | Complete |
| 3 | Every shipped script has lint + smoke coverage | 3.1, 3.2 | Detailed |
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

**Elaborated 2026-10-16 against `main` at `96d439d` (Phase 1 merged).** Facts that shaped this elaboration: the stale-identifier scan found 11 hits in 5 areas (fewer than the audit estimate); 38 skills lack a trigger phrase in `description:`; `scripts/lint_catalog.py` already emits `desc-trigger` as WARN (`scripts/lint_catalog.py:135`).

**Decisions recorded (owner delegated Phase 2; conservative defaults chosen, each reversible):**
- **Overlap groups: keep all 86 skills, differentiate and cross-reference.** No merges or deprecations in this phase. Merging changes the manifest and the installer's marker-owned install state for existing users; that is a Phase 4 / release-note decision. Each skill in a group gets a description that says what it is for and names its neighbour for the other case.
- **Model identifiers: never invent them.** Claude names use the current family (Fable 5.1 `claude-fable-5-1`, Opus 5.5 `claude-opus-5-5`, Sonnet 5.5 `claude-sonnet-5-5`, Haiku 5.5 `claude-haiku-5-5`). For OpenAI and Google, replace retired names with tier descriptions plus "check the provider's current model list" rather than guessing names.
- **Thin-skill depth (`claude`, `go-lua`, `openclaw`): deferred.** Adding reference content without an authoritative source repeats the staleness problem this phase removes. Their descriptions are fixed here; depth waits for a sourced content pass.

### Epic 2.1: Stale model and version references

**Goal:** No skill recommends retired or superseded models or versions as current, and the linter keeps it that way.
**Scope:** `skills/ai-ml-engineering/references/{computer-vision,llm-applications,prompt-engineering,source-map}.md`, `skills/prompt/templates/modular-prompt.yaml`, `skills/meeting-engineering/references/{architecture_and_audio,low_latency_pipelines}.md`, `skills/frontend/references/nextjs-app-router.md`, `scripts/lint_catalog.py`, `tests/test-catalog.sh`
**Dependencies:** none
**Done when:** `python3 -I scripts/lint_catalog.py` reports no `stale-ref` hit outside the allowlist; every allowlisted mention is annotated as historical in the file; the rule has failing fixtures
**Status:** Pending

#### Task 2.1.1: Refresh stale identifiers in content

- [ ] Done

**Context:** Hits (from `git grep -niE 'claude[- ]3|gpt-4o|gemini[- ]1\.5|gpt-3\.5|text-davinci|Next\.js 1[0-3]'`): `ai-ml-engineering/references/computer-vision.md:143-145`, `llm-applications.md:21,22,213`, `prompt-engineering.md:227,257`, `source-map.md:11,12`; `meeting-engineering/references/architecture_and_audio.md:15` and `low_latency_pipelines.md:56` (GPT-4o-mini alongside gpt-5-mini); `prompt/templates/modular-prompt.yaml:11` (`model: "gpt-4o"`); `frontend/references/nextjs-app-router.md:4` ("the new paradigm ... introduced in Next.js 13").

**Implementation vision:** Read each file around the hit before editing; keep the table or example shape, change only the model/version content. Claude rows and code examples use the current family listed in the Phase 2 decisions (frontier tier: Opus 5.5 or Fable 5.1; standard: Sonnet 5.5; fast/cheap: Haiku 5.5; example API call uses `claude-sonnet-5-5`). OpenAI and Google rows become tier labels with a pointer to the provider's model docs; the `gpt-4o` template default becomes a `<provider-model-id>` placeholder with a comment, since a template must not pin a name that will rot. The `source-map.md` rows keep the doc URLs but describe "current Claude/GPT model families", not named retired models. For Next.js, state that the App Router is the standard routing model (stable since Next.js 13.4) and drop "new paradigm". Edge cases: a historical mention that is the point of the sentence (e.g. a migration note) stays but gets the annotation `(historical)` on the same line; none expected in the 11 hits.

**Files:**
- Modify: `skills/ai-ml-engineering/references/computer-vision.md`, `skills/ai-ml-engineering/references/llm-applications.md`, `skills/ai-ml-engineering/references/prompt-engineering.md`, `skills/ai-ml-engineering/references/source-map.md`, `skills/prompt/templates/modular-prompt.yaml`, `skills/meeting-engineering/references/architecture_and_audio.md`, `skills/meeting-engineering/references/low_latency_pipelines.md`, `skills/frontend/references/nextjs-app-router.md`

**Verification:** `git grep -niE 'claude[- ]3|claude-3|gpt-4o|gemini[- ]1\.5|gpt-3\.5|text-davinci|Next\.js 1[0-3]\b' -- skills` prints nothing (or only `(historical)`-annotated lines); `python3 -I scripts/lint_catalog.py` still reports 0 errors; the YAML template still parses (`python3 -I -c "import sys; print(open('skills/prompt/templates/modular-prompt.yaml').read()[:1])"` is not enough, so use `ruby -ryaml -e 'YAML.load_file(ARGV[0])' skills/prompt/templates/modular-prompt.yaml`).

**Done when:** the grep is clean and no file was changed outside the listed hits' tables, examples and prose.

#### Task 2.1.2: `stale-ref` linter rule

- [ ] Done

**Context:** `scripts/lint_catalog.py` has an ERROR/WARN `add(level, skill, rule, msg)` pattern (see `scripts/lint_catalog.py:135`), and `tests/test-catalog.sh` builds fixtures with `make_fixture` and asserts with `expect_only_rule`.

**Implementation vision:** New rule `stale-ref` (ERROR): scan every `*.md`, `*.yaml`, `*.yml`, `*.json`, `*.sh`, `*.py` under each skill for the case-insensitive pattern list in a module constant `STALE_PATTERNS`: `claude[- ]?3`, `claude-(instant|2)`, `gpt-4o`, `gpt-4-turbo`, `gpt-3\.5`, `text-davinci`, `gemini[- ]?1\.5`, `Next\.js 1[0-3]\b`. A line is exempt if it contains the literal marker `(historical)`. Skip the pattern constant's own file (`scripts/lint_catalog.py` is outside `skills/`, so no special case is needed). Report `file:line`. Fixtures: a file with `gpt-4o` fails; the same line with `(historical)` passes; a clean file passes. This rule is an ERROR from the start because Task 2.1.1 clears the tree first (order: 2.1.1 then 2.1.2).

**Files:**
- Modify: `scripts/lint_catalog.py`, `tests/test-catalog.sh`

**Verification:** `bash tests/test-catalog.sh` exits 0 and prints `PASS: stale-ref`; `python3 -I scripts/lint_catalog.py` reports 0 errors on the real tree.

**Done when:** a regression of any stale pattern fails CI.

### Epic 2.2: Overlap routing

**Goal:** For each of the six overlap groups, a reader (or an agent choosing a skill) can tell from the description alone which one to pick.
**Scope:** `SKILL.md` frontmatter and the first screen of body for the 15 skills below
**Dependencies:** none (descriptions only; the linter's `desc-trigger` rule is promoted in Epic 2.3 after these land)
**Done when:** every skill in every group has a `description:` under 1024 characters containing a trigger phrase ("Use when") and a "Not for X: use `<neighbour>`" clause; a "Related skills" line under the title links the neighbours
**Status:** Pending

#### Task 2.2.1: Route the six overlap groups

- [ ] Done

**Context:** Current descriptions (read at elaboration): `redis-valkey` "Advanced Redis and Valkey production operations, troubleshooting, and migration" vs `valkey-redis` "managing Valkey ... valkey.conf ... migrations from Redis OSS to Valkey" (both claim migration); `devops` (AWS/K8s/EKS/Helm/GitOps) vs `devops-infrastructure` (cloud architecture, K8s, CI/CD, IaC, SRE, FinOps); `prompt` (prompt architecture and security) vs `prompt-master` (CoT/ToT/ReAct, RAG, context size); `masterclaw`, `openclaw` (OpenClaw Node.js and ZeroClaw Rust runtimes), `nemoclaw` (NVIDIA NemoClaw), `bot` ("Advanced Bot Engineering with OpenClaw, NemoClaw, and OpenShell"); `postgres-15`, `sql-partitioning`, `database`; `docker`, `dockerfile`.

**Implementation vision:** Assign each skill one lane and write the descriptions to match. Lanes: `redis-valkey` = operating and troubleshooting Redis or Valkey (latency, memory, hot keys, Lua); `valkey-redis` = Valkey-specific config (`valkey.conf`) and Redis OSS to Valkey migration; `devops` = hands-on AWS/EKS/Helm/GitOps/VPC provisioning and troubleshooting; `devops-infrastructure` = cross-cloud architecture, IaC, SRE, platform engineering and FinOps decisions; `prompt` = designing, hardening and debugging prompts and prompt systems; `prompt-master` = prompting techniques, RAG pipelines and context-size reduction; `openclaw` = deploying and troubleshooting OpenClaw/ZeroClaw runtimes; `nemoclaw` = NVIDIA NemoClaw platform deployment and credential handling; `masterclaw` = the combined operational playbook when a task spans both or needs gateway plus prompt architecture; `bot` = building bots on those runtimes (channels, OpenShell), deferring runtime ops to `openclaw`/`nemoclaw`; `postgres-15` = PostgreSQL 15+ operations and tuning; `sql-partitioning` = partitioning and sharding design; `database` = engine-agnostic design (PostgreSQL and MongoDB) and security; `docker` = running and operating containers and Compose; `dockerfile` = authoring and optimizing Dockerfiles. Do not change skill names or directory names. Each description: one sentence of scope, "Use when ...", and "Not for X: use `<skill>`". Add one line `**Related skills:** \`a\`, \`b\`` directly under the H1 in each SKILL.md. Check that the Related lines name only skills that exist in `skills-list.txt`. Also update the README catalog table rows for any skill whose one-line purpose changed (keep rows short).

**Files:**
- Modify: `skills/{redis-valkey,valkey-redis,devops,devops-infrastructure,prompt,prompt-master,masterclaw,openclaw,nemoclaw,bot,postgres-15,sql-partitioning,database,docker,dockerfile}/SKILL.md`, `README.md` (only affected table rows)

**Verification:** `python3 -I scripts/lint_catalog.py` reports 0 errors; `python3 -I - <<'PY'` check (inline) that each of the 15 descriptions has length under 1024, contains "use when" (case-insensitive) and names at least one neighbour in backticks that exists in `skills-list.txt`; prints `ok 15/15`.

**Done when:** the inline check prints `ok 15/15`.

### Epic 2.3: Description triggers and enforcement

**Goal:** Every `description:` carries a trigger and the linter enforces it.
**Scope:** the 31 skills from the 38 `desc-trigger` warnings that are not in Epic 2.2, plus `scripts/lint_catalog.py`, `tests/test-catalog.sh`, `CONTRIBUTING.md`
**Dependencies:** Epics 2.1 and 2.2 (so the promotion lands on a clean tree)
**Done when:** `desc-trigger` is an ERROR rule, `python3 -I scripts/lint_catalog.py` reports 0 errors and 0 warnings, CONTRIBUTING.md states the rule
**Status:** Pending

#### Task 2.3.1: Add triggers to the remaining 23 descriptions

- [ ] Done

**Context:** The 38 warnings are: accessibility-testing, bot, claude, docker, french-teacher, frontend, frontend-menu-design, go-lua, jira-field-schemas, jira-jsm-oncall, jira-status-workflows, lerian-helm, lua, manus, manus-workflows, meeting-engineering, nemoclaw, openai, openclaw, otel-collector, passkeys, playwright, postgres-15, rabbitmq, rabbitmq-documentdb, rag, roles-permissions, seaweedfs, slack, spanish-teacher, sql-partitioning, tech-support-ops, ticket-reports, ticket-supreme, valkey-redis, vitest, voip-oncall, web-tester-supreme. Task 2.2.1 covers bot, docker, nemoclaw, openclaw, postgres-15, sql-partitioning, valkey-redis, so 31 remain; of those, the batch below lists them all.

**Implementation vision:** For each of the 31 skills not handled in Task 2.2.1, read its `SKILL.md` (title, first section) and rewrite only the `description:` line to: one-sentence scope, then "Use when <concrete trigger conditions the user would phrase>", under 1024 characters, single line, no YAML block scalars, quoted if it contains a colon. Do not change body text. Preserve any distinguishing detail already in the description (e.g. the Claude model list in `claude`, "Lerian conventions" in `lerian-helm`). Work in 3 batches of about 10 for sizing; batches are independent and may run in parallel because they touch disjoint files.

**Files:**
- Modify: `skills/<each of the 31 skills>/SKILL.md` (frontmatter line only)

**Verification:** `python3 -I scripts/lint_catalog.py | grep -c desc-trigger` prints `0`; 0 errors.

**Done when:** no skill lacks a trigger phrase.

#### Task 2.3.2: Promote `desc-trigger` to ERROR

- [ ] Done

**Context:** `desc-trigger` is a WARN at `scripts/lint_catalog.py:135` and documented in its docstring at line 5; `CONTRIBUTING.md` lists the authoring contract.

**Implementation vision:** Change the level to ERROR, update the docstring, add a fixture (description without trigger words fails; with "Use when" passes) and flip the Phase 1 fixture that asserted the WARN-only behavior (`tests/test-catalog.sh` fixture "desc-trigger WARN exit 0") to assert ERROR and exit 1. Add one sentence to `CONTRIBUTING.md` stating the rule and the accepted phrases (`use when`, `use for`, `triggers`).

**Files:**
- Modify: `scripts/lint_catalog.py`, `tests/test-catalog.sh`, `CONTRIBUTING.md`

**Verification:** `bash tests/test-catalog.sh` exits 0 under `/bin/bash` and bash 5; `python3 -I scripts/lint_catalog.py` prints `0 error(s), 0 warning(s)`.

**Done when:** a skill without a trigger fails the linter and CI.

---

## Phase 3: Script test depth

**Elaborated 2026-10-16 against `main` at `90f3711` (Phases 1 and 2 merged).** Measured facts: `shellcheck -x --severity=warning` over all 58 shell files under `skills/` reports 0 warnings or errors (16 info/style notes only); `ruff check --select E9,F` over `skills/` reports 8 F401 unused-import findings (7 auto-fixable); 61 of 88 files under `skills/*/scripts/` are not referenced by any test; the Phase 1 CI limits the installer and remediation suites to ubuntu because `skills/coderabbit-reviewer/scripts/{run-review,install-coderabbit}.sh` and `skills/coderabbit-reviewer/tests/test_wrappers.sh` use GNU `sha256sum` and `realpath -e`.

**Decisions recorded:**
- **Smoke coverage is explicit, not guessed.** A registry file `tests/script-coverage.tsv` lists every `skills/*/scripts/*` file with a coverage level: `behavior` (an existing or new test exercises it), `help` (the script has a `--help` handler that is safe to run; the smoke test runs it in an isolated environment), or `static` (syntax, shebang and exec-bit checks only, with a written reason for scripts that need a browser, audio stack, network, calendar credentials, or start a server). The linter fails if a script has no registry row. This avoids blindly executing 61 unknown scripts.
- **Static analysis gates only on what is already clean.** shellcheck at warning severity and ruff `E9,F` become blocking in CI; info-level shellcheck notes stay out of scope.
- **macOS parity is a goal of this phase.** The coderabbit scripts get portable helpers; afterwards the macOS CI leg runs the full suites.

### Epic 3.1: Static analysis gate and macOS parity

**Goal:** CI blocks on shellcheck (warning) and ruff (E9,F) for all skill scripts, and every suite runs on both ubuntu and macOS.
**Scope:** `skills/*/scripts/*.py`, `skills/hermes-agent/tests/test_hermes_preflight.py`, `skills/coderabbit-reviewer/{scripts,tests}/`, `tests/`, `.github/workflows/ci.yml`
**Dependencies:** none
**Done when:** `ruff check --select E9,F skills` and `shellcheck -x --severity=warning` over all skill shell files exit 0; `bash tests/test-installer.sh` and `bash tests/test-adversarial-remediations.sh` exit 0 on macOS (run locally on this Darwin host) and on ubuntu CI; the CI macOS leg runs them
**Status:** Pending

#### Task 3.1.1: Clear the ruff findings

- [ ] Done

**Context:** `ruff check --select E9,F --output-format concise skills` (ruff 0.8.6) reports F401 at `skills/coderabbit-reviewer/scripts/validate_findings.py:14` (`os`), `skills/hermes-agent/tests/test_hermes_preflight.py:10` (`stat`), `skills/legal-compliance/scripts/validate-compliance-checklist.py:4` (`re`), `skills/prompt/scripts/evaluate-prompt.py:15` (`os`), `skills/yaml-specialist/scripts/build_refactor_inventory.py:7` (`json`), `skills/yaml-specialist/scripts/chart_metadata.py:7` (`json`), `skills/yaml-specialist/scripts/scan_template_values.py:13` (`typing.Any`), `skills/yaml-specialist/scripts/yaml_common.py:23` (`CommentedSeq`).

**Implementation vision:** Remove each unused import. For `yaml_common.py` first `grep -rn CommentedSeq skills/yaml-specialist`: if another module does `from yaml_common import CommentedSeq`, keep it and mark it a deliberate re-export (`# noqa: F401  re-exported for importers`); otherwise remove it. Do not auto-fix blindly: confirm each name is truly unused (e.g. not referenced in a string annotation or `__all__`). Edge case: self_check scripts hash or list files, so after editing run the yaml-specialist, hermes-agent, coderabbit-reviewer and security-review `self_check.py` scripts (they check file inventories) with the pinned venv deps installed as in CI, and update any inventory/checksum they keep if a changed file is listed there.

**Files:**
- Modify: the 8 files above (plus a self_check inventory file only if one lists them with hashes)

**Verification:** `docker run --rm -v "$PWD":/mnt -w /mnt python:3.12-slim sh -c 'pip install -q ruff==0.8.6 && ruff check --select E9,F skills'` exits 0; `bash tests/test-installer.sh` still passes the self-check steps (full run is Task 3.1.3's gate; here run the per-skill `self_check.py` scripts in the pinned venv).

**Done when:** ruff reports "All checks passed" and the self-checks still pass.

#### Task 3.1.2: Portable sha256 and path canonicalization

- [ ] Done

**Context:** On macOS `sha256sum` and `realpath -e` do not exist. Usages: `skills/coderabbit-reviewer/scripts/install-coderabbit.sh:104,111,131,152,153`, `skills/coderabbit-reviewer/scripts/run-review.sh:60,174,204,263,268,275,319`, `skills/coderabbit-reviewer/tests/test_wrappers.sh:110`, `tests/test-adversarial-remediations.sh` (runs with `PATH="$fakebin:/usr/bin:/bin"`, lines ~69,103,122,255,259). `install.sh:263-264` already falls back to another hasher; read it for the house pattern. These scripts are security-hardened (canonicalization rejects symlink tricks), so behavior must stay identical.

**Implementation vision:** Add two small functions to each of the two coderabbit scripts (they must stay self-contained single files, so do not introduce a shared sourced lib): `sha256_file` (prefers `sha256sum`, falls back to `shasum -a 256`, else `fail`) and `canonical_existing` (replacement for `realpath -e`: succeeds only if the path exists; resolves with `cd -P -- "$(dirname -- "$p")" && printf '%s/%s' "$(pwd -P)" "$(basename -- "$p")"` for files, `cd -P` for directories, and resolves a final-component symlink with a bounded `readlink` loop (max 40 hops) to preserve realpath semantics; an alternative is `python3 -I -c 'import os,sys; ...os.path.realpath' with an exists check` if python3 is already a hard dependency of the script, decide by reading it). The "required tool missing" messages (`sha256sum is required`) become "sha256sum or shasum is required". Update `sha256sums.txt` generation so the file format is identical on both hashers (`<hash>  <name>` two spaces); `shasum -a 256` already prints that. Keep `test_wrappers.sh` and the remediation test using the same fallback. Edge cases that are reachable: path with spaces, path that is a dangling symlink (must fail like `realpath -e`), relative path argument, trailing slash, hasher missing entirely (existing fail path).

**Files:**
- Modify: `skills/coderabbit-reviewer/scripts/install-coderabbit.sh`, `skills/coderabbit-reviewer/scripts/run-review.sh`, `skills/coderabbit-reviewer/tests/test_wrappers.sh`, `tests/test-adversarial-remediations.sh`
- Test: the same two suites

**Verification:** on this macOS host: `bash tests/test-adversarial-remediations.sh` and `bash tests/test-installer.sh` both exit 0 (the yaml-specialist self-check needs the pinned deps: create a venv under the scratchpad, `pip install -r skills/yaml-specialist/scripts/requirements.txt PyYAML==6.0.2`, and put its `bin` first on PATH). Also run both in `python:3.12-bookworm` (Linux) with the same venv approach to prove no Linux regression.

**Done when:** both suites pass on macOS and Linux with no behavior change on Linux.

#### Task 3.1.3: Blocking static analysis and full suites on macOS in CI

- [ ] Done

**Context:** `.github/workflows/ci.yml` runs the installer and remediation suites under `if: runner.os == 'Linux'` with a comment pointing to this epic; the venv step is also Linux-only; the skill-script shellcheck step has `continue-on-error: true`.

**Implementation vision:** Remove the Linux-only conditions and the stale comment; the venv step runs on both OSes (macOS runners ship `python3`, `jq`, `node`; install `shellcheck` is unnecessary on macOS for tests, but the yaml-specialist self-check wants it: add a `brew install shellcheck` step guarded by `runner.os == 'macOS'`). Make the skill-script shellcheck step blocking (`--severity=warning`, drop `continue-on-error`, keep the nullglob form). Add a `ruff` step in the ubuntu job: `pip install ruff==0.8.6` into the same venv then `ruff check --select E9,F skills`; add `python3 -m compileall -q skills` with `PYTHONDONTWRITEBYTECODE` unset in a temp copy or accept the generated `__pycache__` (it is git-ignored after Task 3.1.4, so just run it and then delete caches). Add a top-level `.gitignore` containing `__pycache__/`, `*.pyc`, `.DS_Store`. Validate the workflow with `actionlint` through `docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:latest`.

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `.gitignore`

**Verification:** `docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:latest` exits 0; after push, `gh pr checks` shows `test (ubuntu-latest)`, `test (macos-latest)` and `shellcheck` all passing with the suites running on both (confirm in the logs that the macOS leg printed the installer suite's PASS lines).

**Done when:** CI is green with the suites on both OSes and static analysis blocking.

### Epic 3.2: Script coverage registry and smoke tests

**Goal:** Every file under `skills/*/scripts/` is registered with a coverage level, and a test enforces the level.
**Scope:** `tests/script-coverage.tsv` (new), `tests/test-scripts.sh` (new), `scripts/lint_catalog.py`, `tests/test-catalog.sh`, `.github/workflows/ci.yml`, `CONTRIBUTING.md`
**Dependencies:** Epic 3.1 (CI parity first)
**Done when:** `python3 -I scripts/lint_catalog.py` has an ERROR rule `script-untested` that passes; `bash tests/test-scripts.sh` exits 0 on macOS and ubuntu; CI runs it
**Status:** Pending

#### Task 3.2.1: Build the registry and the `script-untested` rule

- [ ] Done

**Context:** 88 files match `skills/*/scripts/*.{sh,py,js,mts}` plus other extensions in those directories (`git ls-files 'skills/*/scripts/*' | wc -l` gives the exact set, 90 at the audit; use it). 61 are not referenced by any test; those 27 that are referenced (e.g. via `tests/test-adversarial-remediations.sh`, skill-local `tests/`) are `behavior`.

**Implementation vision:** TSV, columns `path<TAB>level<TAB>reason`, header row, sorted by path, `reason` required for `static` and empty otherwise. Generate the first version with a one-off script, then classify by reading each script: `behavior` if some test in `tests/` or `skills/*/tests/` invokes it by basename; `help` only if the source has a real `--help`/`-h` branch that exits 0 before doing any work (confirm by reading, never by guessing); everything else `static` with a short true reason (e.g. "needs Chrome and PulseAudio", "starts a local server", "writes to Google Calendar", "mutates database; dry-run flag required"). Scripts that already document a `--dry-run` or validate-only mode and exit 0 on missing input may be classified `help` only if `--help` itself is safe. Linter rule `script-untested` (ERROR): every non-test file under `skills/*/scripts/` must have a row; every row must point at an existing file; levels must be one of the three; `static` needs a reason; `behavior` rows must name a test file that mentions the basename (column 4 `test`). Fixtures in `tests/test-catalog.sh`: missing row fails, stale row fails, static without reason fails, valid registry passes. Edge case: files in skill subfolders other than `scripts/` (references, templates) are out of scope; `tests/` dirs inside skills are tests, not scripts.

**Files:**
- Create: `tests/script-coverage.tsv`
- Modify: `scripts/lint_catalog.py`, `tests/test-catalog.sh`, `CONTRIBUTING.md` (one paragraph: new scripts need a registry row and why)

**Verification:** `python3 -I scripts/lint_catalog.py` prints 0 errors, 0 warnings; `bash tests/test-catalog.sh` exits 0 under bash and `/bin/bash`.

**Done when:** adding an unregistered script to any skill fails the linter.

#### Task 3.2.2: `tests/test-scripts.sh` enforces the registry

- [ ] Done

**Context:** `tests/test-installer.sh` shows the house style (isolated `HOME`, `mktemp -d`, trap cleanup, `fail()`). macOS has no `timeout`; use a `python3 -I` one-liner wrapper (`subprocess.run(..., timeout=N)`) for the time bound. Scripts must never run against the real `HOME` or repo as cwd.

**Implementation vision:** For every registry row, in all levels: the file exists, is a regular file, is executable if it has a shebang or lives under `scripts/` with `.sh`/`.py` extension (matches the linter), passes the syntax check by extension (`bash -n`; `python3 -I -m py_compile` writing to a temp `PYTHONPYCACHEPREFIX`; `node --check` for `.js` when `node` exists, otherwise skip with a printed notice; `.mts` and other types skip the syntax step). For `help` rows additionally: run `<script> --help` with `env -i HOME=<tmp> PATH=<safe path> TMPDIR=<tmp>`, cwd = a fresh temp dir, stdin from `/dev/null`, 15-second bound, and require exit 0 with non-empty output; any other result fails the test with the captured output. For `behavior` rows: assert the named test file exists (the test itself runs elsewhere). Print one PASS line per level summary, not per file, plus a final count line `scripts: N static, M help, K behavior`. Python scripts needing optional deps (ruamel.yaml, jsonschema) are `behavior` or `static`, never `help`, so the smoke test needs no venv. Edge cases reachable: a `help` script that prompts on stdin (the bound plus `/dev/null` stops hangs, and the registry must not classify such a script `help`); a script that writes files in cwd (cwd is a throwaway temp dir).

**Files:**
- Create: `tests/test-scripts.sh` (mode 755)
- Modify: `.github/workflows/ci.yml` (add step `Script smoke tests` on both OSes, after the catalog tests)

**Verification:** `bash tests/test-scripts.sh` exits 0 on this macOS host and inside `python:3.12-bookworm` (install `nodejs` via apt there or accept the node skip notice); mutating the registry (change a `help` row for a script without `--help`) makes it fail (do this by hand once and report).

**Done when:** `test-scripts.sh` is green on both OSes and a wrongly classified script fails it.

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
