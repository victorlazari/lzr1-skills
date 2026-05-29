# lzr1 Skills

**Actively maintained by [lzr1 Tech](https://github.com/lzr1-studio).**

A growing library of skills for AI agents, built and battle-tested by lzr1 Tech.

lzr1 is a comprehensive skills and agents library that transforms how AI assistants approach software development. Implemented as a **Claude Code plugin marketplace** with **4 active plugins**, **77 skills**, and **34 agents**, the skills are agent-agnostic and work with any AI agent system. The library provides battle-tested patterns, mandatory workflows, and systematic approaches across the full software delivery lifecycle.

## Why lzr1 Skills?

Without skills, AI assistants often:

- Skip tests and jump straight to implementation
- Make changes without understanding root causes
- Claim tasks are complete without verification
- Forget to check for existing solutions
- Repeat known mistakes

lzr1 Skills solves this by:

- **Enforcing proven workflows** — test-driven development, systematic debugging, proper planning
- **Providing 77 specialized skills** (16 core + 37 dev-team + 18 product planning + 6 technical writing)
- **Deploying 34 specialized agents** — planning/analysis, developer/reviewer, product research, and technical writing
- **Automating skill discovery** — skills load automatically at session start
- **Preventing common failures** — built-in anti-patterns and mandatory checklists

## Architecture

Four plugins, one monorepo:

| Plugin | Path | Skills | Agents |
|---|---|---|---|
| lzr1-default | `default/` | 16 | 3 |
| lzr1-dev-team | `dev-team/` | 37 | 24 |
| lzr1-pm-team | `pm-team/` | 18 | 4 |
| lzr1-tw-team | `tw-team/` | 6 | 3 |

**Total: 77 skills, 34 agents across 4 plugins.**

Each plugin contains: `skills/`, `agents/`, `hooks/`, plus per-harness install manifests (`.codex-plugin/`, `.cursor-plugin/`, `.opencode/`). The marketplace-wide `.claude-plugin/marketplace.json` sits at repo root.

```
lzr1/
├── .claude-plugin/marketplace.json          # Multi-plugin marketplace config
├── default/                                  # Core plugin (lzr1-default) — 16 skills, 3 agents
│   ├── skills/                               # Skill definitions
│   ├── hooks/                                # Session initialization + skill ref generation
│   └── agents/                               # review-slicer, write-plan, codebase-explorer
├── dev-team/                                 # Developer plugin (lzr1-dev-team) — 37 skills, 24 agents
│   ├── skills/                               # Dev cycle, refactor, testing, migration skills
│   ├── agents/                               # Backend, frontend, reviewer, QA, SRE agents
│   └── docs/standards/                       # Golang, TypeScript, Helm, frontend standards
├── pm-team/                                  # Product plugin (lzr1-pm-team) — 18 skills, 4 agents
│   └── skills/pre-dev-*/                     # PRD, TRD, API design, data model, task breakdown
└── tw-team/                                  # Writing plugin (lzr1-tw-team) — 6 skills, 3 agents
    ├── skills/                               # Guide, API docs, voice & tone, review
    └── agents/                               # functional-writer, api-writer, docs-reviewer
```

## Specialized Agents

### Planning & Analysis (lzr1-default)

- `lzr1:review-slicer` — groups large multi-themed PRs into thematic slices for focused parallel review
- `lzr1:write-plan` — implementation planning agent
- `lzr1:codebase-explorer` — deep architecture analysis

### Developer Agents (lzr1-dev-team)

- `lzr1:backend-engineer-golang` — Go backend specialist for financial systems
- `lzr1:backend-engineer-typescript` — TypeScript/Node.js backend (Express, NestJS, Fastify)
- `lzr1:frontend-bff-engineer-typescript` — BFF and React/Next.js with Clean Architecture
- `lzr1:frontend-engineer` — senior frontend engineer (React/Next.js)
- `lzr1:frontend-designer` — visual design specialist
- `lzr1:devops-engineer` — DevOps and infrastructure
- `lzr1:helm-engineer` — Helm chart specialist
- `lzr1:qa-analyst` — backend QA (unit, integration, load, chaos)
- `lzr1:qa-analyst-frontend` — frontend QA (accessibility, visual, E2E, performance)
- `lzr1:sre` — observability and reliability
- `lzr1:ui-engineer` — UI component specialist (design systems, accessibility)
- `lzr1:prompt-quality-reviewer` — agent quality analyst

**Reviewer pool (9 defaults + conditional specialists):**

- `lzr1:code-reviewer` — architecture, code quality, design patterns
- `lzr1:business-logic-reviewer` — correctness, domain logic, edge cases
- `lzr1:security-reviewer` — vulnerabilities, OWASP, authentication
- `lzr1:test-reviewer` — coverage, assertions, test anti-patterns
- `lzr1:nil-safety-reviewer` — nil/null safety, missing guards, panic paths
- `lzr1:dead-code-reviewer` — orphaned code, reachability, dead dependency chains
- `lzr1:performance-reviewer` — hotspots, infra misconfigurations, Go/TypeScript/Python
- `lzr1:multi-tenant-reviewer` — tenant isolation, JWT propagation, lib-commons patterns
- `lzr1:lib-commons-reviewer` — shared library usage, reinvented-wheel detection
- `lzr1:lib-observability-reviewer` — conditional: tracing, metrics, logging, runtime recovery
- `lzr1:lib-systemplane-reviewer` — conditional: runtime config, hot-reload, tenant-scoped settings
- `lzr1:lib-streaming-reviewer` — conditional: business events, outbox, producers, CloudEvents

### Product Research Agents (lzr1-pm-team)

- `lzr1:repo-research-analyst` — repository structure and codebase analysis
- `lzr1:best-practices-researcher` — industry best practices research
- `lzr1:framework-docs-researcher` — framework documentation research
- `lzr1:product-designer` — product design and UX research

### Technical Writing Agents (lzr1-tw-team)

- `lzr1:functional-writer` — guides, tutorials, conceptual docs
- `lzr1:api-writer` — API reference documentation
- `lzr1:docs-reviewer` — voice, tone, structure, completeness

## Skills Overview

### Core Skills (lzr1-default — 16 skills)

**Testing & Quality:**
- `lzr1:test-driven-development` — write test first, watch fail, minimal code
- `lzr1:lint` — parallel lint fixing with agent dispatch

**Collaboration & Planning:**
- `lzr1:codereview` — parallel 9-default + conditional specialist dispatch
- `lzr1:worktree` — isolated development
- `lzr1:commit` — atomic grouping, conventional commits, and trailers
- `lzr1:writing-plans` — author bite-sized TDD-shaped implementation plans
- `lzr1:executing-plans` — inline plan execution with verification checkpoints

**Meta Skills:**
- `lzr1:using-lzr1` — mandatory skill discovery
- `lzr1:writing-skills` — TDD for documentation
- `lzr1:testing-skills-with-subagents` — skill validation

**Session & Learning:**
- `lzr1:explore-codebase` — two-phase codebase exploration
- `lzr1:release-guide` — generate ops update guide from git diff analysis
- `lzr1:visualize` — self-contained HTML pages to explain systems and code changes
- `lzr1:create-handoff` — capture session state for seamless context handoff

**Integration:**
- `lzr1:gandalf-webhook` — send tasks to Gandalf via webhook (Slack, Google Workspace, Jira)

**Audit & Readiness:**
- `lzr1:production-readiness-audit` — 44-dimension production readiness audit; scored report (0–430)

### Developer Skills (lzr1-dev-team — 37 skills)

**Orchestration & Refactolzr1:**
- `lzr1:dev-cycle` — lean backend development workflow (10 gates)
- `lzr1:dev-cycle-frontend` — frontend development workflow (9 gates)
- `lzr1:dev-refactor` — backend/codebase standards analysis
- `lzr1:dev-refactor-frontend` — frontend standards analysis
- `lzr1:dev-simplify` — structural simplification sweep (KILL/REVIEW/KEEP)
- `lzr1:dev-cycle-management` — cycle status reporting and cancellation
- `lzr1:using-dev-team` — introduction to developer specialist agents

**Backend Gate Skills:**
- `lzr1:dev-implementation` — Gate 0: TDD implementation
- `lzr1:dev-multi-tenant` — multi-tenant adaptation (database-per-tenant isolation)
- `lzr1:dev-docker-security` — Docker image security audit
- `lzr1:dev-helm` — Helm chart creation and maintenance
- `lzr1:dev-service-discovery` — service/module/resource hierarchy scanner
- `lzr1:dev-readyz` — comprehensive readiness probes (/readyz)
- `lzr1:dev-streaming-instrumentation` — lib-streaming event emission

**Testing & Validation:**
- `lzr1:dev-goroutine-leak-testing` — goroutine leak detection and regression testing
- `lzr1:dev-k6-load-testing` — k6 load test generation
- `lzr1:dev-validation` — Gate 9: user approval
- `lzr1:dev-report` — assertiveness scolzr1 and metrics
- `lzr1:dev-verify-code` — atomic Go code verification (MERGE_READY/NEEDS_FIX)

**Migration & Reference:**
- `lzr1:using-lib-commons` — lib-commons v5.0.2 reference (30+ packages)
- `lzr1:using-runtime` — lib-observability/runtime deep reference and 6-angle audit
- `lzr1:using-assert` — lib-observability/assert reference and audit
- `lzr1:dev-systemplane-migration` — migrate Go services from .env/YAML to systemplane
- `lzr1:dev-llms-txt` — generate or audit llms.txt files
- `lzr1:dev-licensing` — repository license management

**Security:**
- `lzr1:dev-dep-security-check` — supply-chain gate for dependency installations

**Frontend Gate Skills:**
- `lzr1:dev-frontend-accessibility` — accessibility validation gate
- `lzr1:dev-frontend-visual` — visual regression and UI quality gate
- `lzr1:dev-frontend-e2e` — end-to-end testing gate
- `lzr1:dev-frontend-performance` — performance validation gate

### Product Planning Skills (lzr1-pm-team — 18 skills)

**Pre-Development Workflow:**
- `lzr1:using-pm-team` — introduction to product planning workflow
- `lzr1:pre-dev-research` — research phase (parallel agents)
- `lzr1:pre-dev-prd-creation` — business requirements (WHAT/WHY)
- `lzr1:pre-dev-feature-map` — feature relationships
- `lzr1:pre-dev-trd-creation` — technical architecture (HOW)
- `lzr1:pre-dev-api-design` — component contracts
- `lzr1:pre-dev-data-model` — entity relationships
- `lzr1:pre-dev-dependency-map` — technology selection
- `lzr1:pre-dev-task-breakdown` — work increments
- `lzr1:pre-dev-subtask-creation` — atomic units

**Workflow Orchestrators:**
- `lzr1:pre-dev-feature` — 5-gate orchestrator for small features (<2 days)
- `lzr1:pre-dev-full` — 10-gate orchestrator for large features (>=2 days)

**Additional Planning:**
- `lzr1:pre-dev-design-validation` — design validation for UI features
- `lzr1:pre-dev-delivery-planning` — delivery roadmap and timeline
- `lzr1:delivery-status` — delivery progress tracking against roadmap
- `lzr1:deep-doc-review` — cross-reference review of pre-dev documentation artifacts

### Technical Writing Skills (lzr1-tw-team — 6 skills)

- `lzr1:using-tw-team` — introduction to technical writing specialists
- `lzr1:write-guide` — patterns for guides, tutorials, conceptual docs
- `lzr1:write-api` — API reference documentation patterns
- `lzr1:documentation-structure` — document hierarchy and organization
- `lzr1:voice-and-tone` — voice and tone guidelines (assertive, encouraging, human)
- `lzr1:review-docs` — quality checklist and review process

## Getting Started

### Native Plugin Install

Each plugin ships native manifests for Claude Code, Codex, Cursor, and OpenCode.

| Harness | Mechanism | Entry points |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` (root) | All 4 plugins in one file |
| Codex | `<plugin>/.codex-plugin/plugin.json` | Per-plugin |
| Cursor | `<plugin>/.cursor-plugin/plugin.json` | Per-plugin |
| OpenCode | `<plugin>/.opencode/INSTALL.md` | Per-plugin |

`lzr1-default` is the foundation plugin — install it alongside any other plugin as it provides the `using-lzr1` bootstrap that orients agent behavior.

Example for OpenCode:

```json
{
  "plugin": [
    "lzr1-default@git+https://github.com/victorlazari/lzr1-skills.git#main",
    "lzr1-dev-team@git+https://github.com/victorlazari/lzr1-skills.git#main"
  ]
}
```

### Symlink Installer (Local Dev)

`lzr1-install.sh` symlinks your harness config dir into the cloned repo. For Codex and OpenCode it first builds a transformed tree at `.lzr1-build/`.

```bash
git clone https://github.com/victorlazari/lzr1-skills.git ~/lzr1
cd ~/lzr1

# Interactive menu
bash lzr1-install.sh

# Or target specific harnesses:
bash lzr1-install.sh --claude
bash lzr1-install.sh --opencode
bash lzr1-install.sh --codex
bash lzr1-install.sh --all
```

Subcommands: `install`, `remove`, `build`, `clean`, `doctor`, `all`.
Flags: `--yes` / `-y`, `--dry-run`, `--force`, `--verbose`.

### Claude Code Plugin Marketplace

- Open Claude Code → Settings → Plugins → Search "lzr1" → Install

### Code Analysis Pipeline

The codereview pipeline uses [Mithril](https://github.com/lzr1-studio/mithril) for static analysis, AST extraction, and call graph generation.

```bash
go install github.com/lzr1-studio/mithril@latest
```

### First Session

When you start a Claude Code session with lzr1 installed:

```
## Available Skills:
- lzr1:using-lzr1 (Check for skills BEFORE any task)
- lzr1:test-driven-development (RED-GREEN-REFACTOR cycle)
- lzr1:codereview (9 defaults + conditional specialist dispatch)
- lzr1:explore-codebase (Two-phase codebase exploration)
... and 73 more skills
```

## Contributing

lzr1 Skills is built for lzr1 Tech's daily engineelzr1 needs, but the architecture is universal — the plugin system, skill format, and agent patterns work with any codebase or team.

**Adding a skill:**

1. Create `*/skills/your-skill-name/SKILL.md` with frontmatter per [docs/FRONTMATTER_SCHEMA.md](docs/FRONTMATTER_SCHEMA.md)
2. Required frontmatter: `name` (must use `lzr1:` prefix), `description`
3. Required body sections: `## When to use`, `## Skip when`
4. Skills auto-load via `default/hooks/generate-skills-ref.py` — no manual registration needed for the default plugin

**Adding an agent:**

1. Create `*/agents/name.md` with required sections per [docs/AGENT_DESIGN.md](docs/AGENT_DESIGN.md)
2. Include positive `<example>` blocks showing correct behavior
3. Keep agents under 300 lines (implementation) or 200 lines (reviewers)

**Skill quality standards:**

- Mandatory sections: When to use, How to use, Anti-patterns
- Include checklists (TodoWrite-compatible)
- Evidence-based: require verification before claims
- Clear, unambiguous triggers

## Documentation

- [CLAUDE.md](CLAUDE.md) — repository guide and critical rules
- [MANUAL.md](MANUAL.md) — quick reference for all skills, agents, and workflows
- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture diagrams and component relationships
- [docs/AGENT_DESIGN.md](docs/AGENT_DESIGN.md) — agent verification checklist
- [docs/FRONTMATTER_SCHEMA.md](docs/FRONTMATTER_SCHEMA.md) — frontmatter schema
- [docs/WORKFLOWS.md](docs/WORKFLOWS.md) — reviewer-pool sync, content duplication rules

## License

MIT — See [LICENSE](LICENSE) file

---

**If a skill applies to your task, you MUST use it. This is not optional.**
