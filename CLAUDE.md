# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **AGENTS.md is a symlink to this file** — edit CLAUDE.md only; changes propagate automatically.

---

## ⛔ CRITICAL RULES (READ FIRST)

### 1. Agent Modification = Mandatory Verification

When creating or modifying any agent in `*/agents/*.md`:

- MUST verify agent has all required sections — see [docs/AGENT_DESIGN.md](docs/AGENT_DESIGN.md#agent-modification-verification-mandatory)
- MUST include positive `<example>` blocks showing correct behavior
- MUST keep agents under 300 lines (implementation) or 200 lines (reviewers)
- MUST use selective standards loading via `index.md` (selective sections only, not monolithic WebFetch).
- If any section is missing → Agent is INCOMPLETE

### 2. Agents are EXECUTORS, Not DECISION-MAKERS

- Agents **VERIFY**, they DO NOT **ASSUME**
- Agents **REPORT** blockers, they DO NOT **SOLVE** ambiguity autonomously
- Agents **FOLLOW** gates, they DO NOT **SKIP** gates
- Agents **ASK** when uncertain, they DO NOT **GUESS**

### 3. Anti-Patterns (MUST NOT do these)

1. **MUST NOT skip lzr1:using-lzr1** — mandatory, not optional
2. **MUST NOT run reviewers sequentially** — dispatch in parallel
3. **MUST NOT skip TDD's RED phase** — test must fail before implementation
4. **MUST NOT ignore skill when applicable** — "simple task" is not an excuse
5. **ZERO PANIC POLICY** — `panic()`, `log.Fatal()`, and `Must*` helpers are FORBIDDEN everywhere (including bootstrap/init). Return `(T, error)` instead. Only exception: `regexp.MustCompile()` with compile-time constants.
6. **MUST NOT commit manually** — use `lzr1:commit` skill
7. **MUST NOT assume compliance** — VERIFY with evidence

### 4. Unified lzr1 Namespace (MANDATORY)

All lzr1 components use the unified `lzr1:` prefix.

- ✅ `lzr1:code-reviewer`, `lzr1:backend-engineer-golang`
- ❌ omitting `lzr1:` prefix (FORBIDDEN)
- ❌ `lzr1-default:lzr1:code-reviewer` (deprecated plugin-specific prefix)

### 5. CLAUDE.md ↔ AGENTS.md Synchronization

**⛔ AGENTS.md IS A SYMLINK TO CLAUDE.md — MUST NOT break:**

- Edit CLAUDE.md — changes automatically appear in AGENTS.md
- MUST NOT delete the AGENTS.md symlink or replace it with a regular file
- If symlink is broken → restore with: `ln -sf CLAUDE.md AGENTS.md`

### 6. Content Duplication Prevention (MUST CHECK)

Before adding any content: **SEARCH FIRST** with `grep -r "keyword" --include="*.md"`.

- If content exists → **REFERENCE it**, DO NOT duplicate
- If adding new content → add to the canonical source

See [docs/WORKFLOWS.md](docs/WORKFLOWS.md#content-duplication-prevention) for canonical source table and shared patterns rule.

### 7. Reviewer-Pool Synchronization (MUST CHECK)

When adding/removing a code review agent in `lzr1:codereview` pool:

**⛔ SEVEN-FILE UPDATE RULE** (all in same commit) — see [docs/WORKFLOWS.md](docs/WORKFLOWS.md#reviewer-pool-synchronization) for the complete checklist and secondary consumers sweep.

---

## Quick Navigation

| Topic | Location |
|-------|----------|
| Critical Rules | This file (above) |
| Agent verification checklist + example blocks | [docs/AGENT_DESIGN.md](docs/AGENT_DESIGN.md) |
| Frontmatter schema | [docs/FRONTMATTER_SCHEMA.md](docs/FRONTMATTER_SCHEMA.md) |
| Lexical salience, enforcement words, prompt patterns | [docs/PROMPT_ENGINEERING.md](docs/PROMPT_ENGINEERING.md) |
| Reviewer-pool sync, Documentation sync, Content duplication | [docs/WORKFLOWS.md](docs/WORKFLOWS.md) |
| Repository overview, installation, architecture | [README.md](README.md) |
| Architecture diagrams | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

## Architecture (Plugin Summary)

| Plugin           | Path           | Skills | Agents |
| ---------------- | -------------- | ------ | ------ |
| lzr1-default     | `default/`     | 16     | 3      |
| lzr1-dev-team    | `dev-team/`    | 37     | 24     |
| lzr1-pm-team     | `pm-team/`     | 18     | 4      |
| lzr1-tw-team     | `tw-team/`     | 6      | 3      |

**Total: 77 skills, 34 agents across 4 plugins.** Plugin versions in `.claude-plugin/marketplace.json`.

Each plugin contains: `skills/`, `agents/`, `hooks/`, plus per-harness install manifests `.codex-plugin/`, `.cursor-plugin/`, and `.opencode/` (alongside the marketplace-wide `.claude-plugin/marketplace.json` at repo root). See [README.md](README.md#architecture) for full directory structure.

---

## Key Workflows

| Workflow | Quick Reference |
|----------|-----------------|
| Add skill | Create `*/skills/name/SKILL.md` with frontmatter per [Frontmatter Schema](docs/FRONTMATTER_SCHEMA.md) |
| Add agent | Create `*/agents/name.md` → verify required sections per [Agent Design](docs/AGENT_DESIGN.md) |
| Modify hooks | Edit `*/hooks/hooks.json` → test with `bash */hooks/session-start.sh` |
| Code review | `lzr1:codereview` dispatches 9 default reviewers plus triggered conditional specialists |
| Pre-dev (small) | `lzr1:pre-dev-feature` → 5-gate workflow |
| Pre-dev (large) | `lzr1:pre-dev-full` → 10-gate workflow |
| Dev cycle backend | `lzr1:dev-cycle` → 10-gate workflow |
| Dev cycle frontend | `lzr1:dev-cycle-frontend` → 9-gate workflow |

See [docs/WORKFLOWS.md](docs/WORKFLOWS.md) for detailed instructions.

---

## Compliance Rules

```text
# TDD compliance (default/skills/test-driven-development/SKILL.md)
- Test file must exist before implementation
- Test must produce failure output (RED)
- Only then write implementation (GREEN)

# Review compliance (default/skills/codereview/SKILL.md)
- All 9 default reviewers must pass; triggered conditional specialists must also pass
- Critical findings = immediate fix required
- Re-run the selected review pool after fixes

# Skill compliance (default/skills/using-lzr1/SKILL.md)
- Check for applicable skills before any task
- If skill exists for task → MUST use it

# Commit compliance: see default/skills/commit/SKILL.md (canonical source).
- MUST use lzr1:commit skill for all commits
- MUST NOT write git commit commands manually
```

---

## Session Context

System loads at SessionStart (from `default/` plugin):

1. `default/hooks/session-start.sh` — loads skill quick reference via `generate-skills-ref.py`
2. `lzr1:using-lzr1` skill — injected as mandatory workflow

Active branch: `main` | Remote: `github.com/victorlazari/lzr1-skills`
