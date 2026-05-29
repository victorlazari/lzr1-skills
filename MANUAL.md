# lzr1 Marketplace Manual

Quick reference guide for the lzr1 skills library and workflow system. This monorepo provides 4 plugins with 77 skills and 34 agents for enforcing proven software engineelzr1 practices across the entire software delivery value chain.

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              MARKETPLACE (4 PLUGINS)                               │
│                     (monorepo: .claude-plugin/marketplace.json)                    │
│                                                                                    │
│  ┌───────────────┐  ┌───────────────┐                                              │
│  │ lzr1-default  │  │ lzr1-dev-team │                                              │
│  │  Skills(16)   │  │  Skills(37)   │                                              │
│  │  Agents(3)    │  │  Agents(24)   │                                              │
│  └───────────────┘  └───────────────┘                                              │
│  ┌───────────────┐  ┌───────────────┐                                              │
│  │ lzr1-pm-team  │  │ lzr1-tw-team  │                                              │
│  │  Skills(18)   │  │  Skills(6)    │                                              │
│  │  Agents(4)    │  │  Agents(3)    │                                              │
│  └───────────────┘  └───────────────┘                                              │
└────────────────────────────────────────────────────────────────────────────────────┘

                              HOW IT WORKS
                              ────────────

    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │   SESSION    │         │    USER      │         │  CLAUDE CODE │
    │    START     │────────▶│   PROMPT     │────────▶│   WORKING    │
    └──────────────┘         └──────────────┘         └──────────────┘
           │                        │                        │
           ▼                        ▼                        ▼
    ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
    │    HOOKS     │         │    SKILLS    │         │    AGENTS    │
    │ auto-inject  │         │   primary    │         │  dispatched  │
    │   context    │         │  invocation  │         │  for work    │
    └──────────────┘         └──────────────┘         └──────────────┘
           │                        │                        │
           │                        ▼                        │
           │                 ┌──────────────┐                │
           └────────────────▶│   RESULTS    │◀───────────────┘
                             │  aggregated  │
                             │  & reported  │
                             └──────────────┘

                            COMPONENT ROLES
                            ───────────────

    ┌────────────┬──────────────────────────────────────────────────┐
    │ Component  │ Purpose                                          │
    ├────────────┼──────────────────────────────────────────────────┤
    │ MARKETPLACE│ Monorepo containing all plugins                  │
    │ PLUGIN     │ Self-contained package (skills+agents+hooks)     │
    │ HOOK       │ Auto-runs at session events (injects context)    │
    │ SKILL      │ Primary invocation (user or Claude Code)          │
    │ AGENT      │ Specialized subprocess (Task tool dispatch)      │
    └────────────┴──────────────────────────────────────────────────┘
```

---

## 🎯 Quick Start

lzr1 is auto-loaded at session start. Two ways to invoke lzr1 capabilities:

1. **Skills** – `Skill tool: "lzr1:skill-name"` (primary invocation method)
2. **Agents** – `Task tool with subagent_type: "lzr1:agent-name"`

### Multi-harness install

Beyond Claude Code (source of truth), lzr1 is installable in Codex, Cursor, and OpenCode via per-plugin native manifests (`<plugin>/.codex-plugin/`, `<plugin>/.cursor-plugin/`, `<plugin>/.opencode/`). For local-dev symlinks across Claude Code, Factory AI, OpenCode, and Codex, use `bash lzr1-install.sh` at repo root. See [README § Supported Platforms](README.md#-supported-platforms) and [README § Quick Start](README.md#-quick-start) for full instructions.

---

## 💡 About Skills

Skills (77) are the primary invocation mechanism for lzr1. They can be invoked directly by users (`Skill tool: "lzr1:skill-name"`) or applied automatically by Claude Code when it detects they're applicable. They handle testing, debugging, verification, planning, code review enforcement, and more.

Examples: lzr1:test-driven-development, lzr1:codereview, lzr1:production-readiness-audit (44-dimension audit, up to 10 explorers per batch, incremental report 0-430, max 440 with multi-tenant; see [default/skills/production-readiness-audit/SKILL.md](default/skills/production-readiness-audit/SKILL.md)), etc.

### Skill Selection Criteria

See [docs/FRONTMATTER_SCHEMA.md](docs/FRONTMATTER_SCHEMA.md) for the canonical schema. Skill selection now relies on the condensed `description` field plus body sections like `## When to use` / `## Skip when` / `## Sequence` / `## Related`.

Claude Code matches user intent against the skill's `description` field at SessionStart; body sections provide additional context once the skill is invoked.

---

## 🤖 Available Agents

Invoke via `Task tool with subagent_type: "..."`.

### Code Review pool (dev-team)

**Always dispatch all 9 defaults in parallel** (single message), plus triggered conditional specialists:

| Agent                                | Purpose                                      |
| ------------------------------------ | -------------------------------------------- |
| `lzr1:code-reviewer`                 | Architecture, patterns, maintainability      |
| `lzr1:business-logic-reviewer`       | Domain correctness, edge cases, requirements |
| `lzr1:security-reviewer`             | Vulnerabilities, OWASP, auth, validation     |
| `lzr1:test-reviewer`                 | Test coverage, quality, and completeness     |
| `lzr1:nil-safety-reviewer`           | Nil/null pointer safety analysis             |
| `lzr1:dead-code-reviewer`            | Unused code, unreachable paths, dead exports          |
| `lzr1:performance-reviewer`          | Performance hotspots, allocations, goroutine leaks, N+1 queries |
| `lzr1:multi-tenant-reviewer`         | lib-commons/multitenancy patterns, tenant isolation, tenantId propagation |
| `lzr1:lib-commons-reviewer`          | lib-commons package usage and reinvented-wheel opportunities |

Conditional specialists run only when their stack is touched:

| Agent | Trigger |
| ----- | ------- |
| `lzr1:lib-observability-reviewer` | tracing, metrics, logging, runtime recovery/panic safety, redaction, constants, SafeGo/recover implications |
| `lzr1:lib-systemplane-reviewer` | runtime config, hot-reload knobs, admin config surface, tenant-scoped settings, systemplane imports/config |
| `lzr1:lib-streaming-reviewer` | business events, outbox, event producers, broker publishing, CloudEvents, manifests/catalogs |

**Example:** Before merging, run the 9 default reviewers plus any triggered specialists via `lzr1:codereview` skill

### Orchestration (lzr1-default)

| Agent                  | Purpose                                                            |
| ---------------------- | ------------------------------------------------------------------ |
| `lzr1:review-slicer`   | Groups large multi-themed PRs into thematic slices for focused review |

### Planning & Analysis (lzr1-default)

| Agent                    | Purpose                                                  |
| ------------------------ | -------------------------------------------------------- |
| `lzr1:write-plan`        | Generate implementation plans for zero-context execution |
| `lzr1:codebase-explorer` | Deep architecture analysis (vs `Explore` for speed)      |

### Developer Specialists (lzr1-dev-team)

Use when you need expert depth in specific domains:

| Agent                                   | Specialization               | Technologies                                       |
| --------------------------------------- | ---------------------------- | -------------------------------------------------- |
| `lzr1:backend-engineer-golang`          | Go microservices & APIs      | Fiber, gRPC, PostgreSQL, MongoDB, Kafka, OAuth2    |
| `lzr1:backend-engineer-typescript`      | TypeScript/Node.js backend   | Express, NestJS, Prisma, TypeORM, GraphQL          |
| `lzr1:devops-engineer`                  | DevOps & infrastructure      | Docker, Kubernetes, CI/CD, cloud operations         |
| `lzr1:frontend-bff-engineer-typescript` | BFF & React/Next.js frontend | Next.js API Routes, Clean Architecture, DDD, React |
| `lzr1:frontend-designer`                | Visual design & aesthetics   | Typography, motion, CSS, distinctive UI            |
| `lzr1:frontend-engineer`                | General frontend development | React, TypeScript, CSS, component architecture     |
| `lzr1:helm-engineer`                    | Helm chart specialist        | Helm charts, Kubernetes, lzr1 conventions        |
| `lzr1:prompt-quality-reviewer`          | AI prompt quality review     | Prompt engineelzr1, clarity, effectiveness         |
| `lzr1:qa-analyst`                       | Backend QA specialist        | Unit, integration, load, chaos, regression testing  |
| `lzr1:qa-analyst-frontend`              | Frontend QA specialist       | Accessibility, visual regression, E2E, performance |
| `lzr1:sre`                              | SRE specialist               | Observability, reliability, SLOs, incident readiness |
| `lzr1:performance-reviewer`             | Performance review           | Go, TypeScript, Python, GOMAXPROCS, GC tuning      |
| `lzr1:multi-tenant-reviewer`            | Multi-tenant usage review    | lib-commons/multitenancy, tenant isolation, JWT tenantId |
| `lzr1:lib-commons-reviewer`             | lib-commons usage review | lifecycle, tenancy, http, idempotency, security, database, messaging |
| `lzr1:lib-observability-reviewer`       | Conditional observability review | tracing, metrics, logging, runtime, redaction |
| `lzr1:lib-systemplane-reviewer`         | Conditional runtime-config review | lib-systemplane, hot reload, admin config, tenant settings |
| `lzr1:lib-streaming-reviewer`           | Conditional event producer review | lib-streaming, outbox, CloudEvents, manifests |
| `lzr1:ui-engineer`                      | UI component specialist      | Design systems, accessibility, React               |

**Standards Compliance Output:** Refactor-capable lzr1-dev-team agents produce a `## Standards Compliance` output section with conditional requirement:

| Invocation Context      | Standards Compliance | Trigger                                   |
| ----------------------- | -------------------- | ----------------------------------------- |
| Direct agent call       | Optional             | N/A                                       |
| Via `lzr1:dev-cycle`    | Optional             | N/A                                       |
| Via `lzr1:dev-refactor` | **MANDATORY**        | Prompt contains `**MODE: ANALYSIS ONLY**` |

**How it works:**

1. `lzr1:dev-refactor` dispatches agents with `**MODE: ANALYSIS ONLY**` in prompt
2. Agents detect this pattern and load lzr1 standards via WebFetch
3. Agents produce comparison tables: Current Pattern vs Expected Pattern
4. Output includes severity, location, and migration recommendations

**Example output when non-compliant:**

```markdown
## Standards Compliance

| Category | Current     | Expected        | Status | Location      |
| -------- | ----------- | --------------- | ------ | ------------- |
| Logging  | fmt.Println | lib-observability/zap | ⚠️     | service/\*.go |
```

**Cross-references:** CLAUDE.md (Standards Compliance section), `dev-team/skills/dev-refactor/SKILL.md`

### Product Planning Research (lzr1-pm-team)

For best practices research and repository analysis:

| Agent                            | Purpose                          | Use For                                 |
| -------------------------------- | -------------------------------- | --------------------------------------- |
| `lzr1:best-practices-researcher` | Best practices research          | Industry patterns, framework standards  |
| `lzr1:framework-docs-researcher` | Framework documentation research | Official docs, API references, examples |
| `lzr1:repo-research-analyst`     | Repository analysis              | Codebase patterns, structure analysis   |
| `lzr1:product-designer`          | Product design and UX research   | UX specifications, user validation, design review |

### Technical Writing (lzr1-tw-team)

For documentation creation and review:

| Agent                    | Purpose                      | Use For                              |
| ------------------------ | ---------------------------- | ------------------------------------ |
| `lzr1:functional-writer` | Functional documentation     | Guides, tutorials, conceptual docs   |
| `lzr1:api-writer`        | API reference documentation  | Endpoints, schemas, examples         |
| `lzr1:docs-reviewer`     | Documentation quality review | Voice, tone, structure, completeness |

---

## 📖 Common Workflows

### New Feature Development

1. **Plan** → Use `lzr1:pre-dev-feature` skill (or `lzr1:pre-dev-full` if complex)
2. **Isolate** → Use `lzr1:worktree` skill
3. **Implement** → Use `lzr1:test-driven-development` skill
4. **Review** → Use `lzr1:codereview` skill (dispatches 9 defaults plus triggered specialists)
5. **Commit** → Use `lzr1:commit` skill

### Bug Investigation

1. **Implement fix** → Use `lzr1:test-driven-development` skill
2. **Review & Merge** → Use `lzr1:codereview` + `lzr1:commit` skills

### Code Review

```
lzr1:codereview skill
    ↓
Runs in parallel:
  • lzr1:code-reviewer
  • lzr1:business-logic-reviewer
  • lzr1:security-reviewer
  • lzr1:test-reviewer
  • lzr1:nil-safety-reviewer
  • lzr1:dead-code-reviewer
  • lzr1:performance-reviewer
  • lzr1:multi-tenant-reviewer
  • lzr1:lib-commons-reviewer
  • conditionally: lzr1:lib-observability-reviewer
  • conditionally: lzr1:lib-systemplane-reviewer
  • conditionally: lzr1:lib-streaming-reviewer
    ↓
Consolidated report with recommendations
```

---

## 🎓 Mandatory Rules

These enforce quality standards:

1. **TDD is enforced** – Test must fail (RED) before implementation
2. **Skill check is mandatory** – Use `lzr1:using-lzr1` before any task
3. **Reviewers run parallel** – Never sequential review (use `lzr1:codereview` skill)
4. **Verification required** – Don't claim complete without evidence
5. **No incomplete code** – No "TODO" or placeholder comments
6. **Error handling required** – Don't ignore errors

---

## 💡 Best Practices

### Skill & Command Selection

| Situation                                              | Use This                       |
| ------------------------------------------------------ | ------------------------------ |
| Feature will take < 2 days                             | `lzr1:pre-dev-feature` (skill) |
| Feature will take ≥ 2 days or has complex dependencies | `lzr1:pre-dev-full` (skill)    |
| Need implementation tasks                              | `lzr1:write-plan` (skill)      |
| Before merging code                                    | `lzr1:codereview` (skill)      |
| Start development cycle                                | `lzr1:dev-cycle` (skill)       |

### Agent Selection

| Need                              | Agent to Use                                |
| --------------------------------- | ------------------------------------------- |
| General code quality review       | 9 default reviewers plus triggered specialists via `lzr1:codereview` skill |
| Large PR review (15+ files)       | Auto-sliced via `lzr1:review-slicer`        |
| Implementation planning           | `lzr1:write-plan`                           |
| Deep codebase analysis            | `lzr1:codebase-explorer`                    |
| Go backend expertise              | `lzr1:backend-engineer-golang`              |
| TypeScript/Node.js backend        | `lzr1:backend-engineer-typescript`          |
| React/Next.js frontend & BFF      | `lzr1:frontend-bff-engineer-typescript`     |
| General frontend development      | `lzr1:frontend-engineer`                    |
| Visual design & aesthetics        | `lzr1:frontend-designer`                    |
| DevOps and infrastructure         | `lzr1:devops-engineer`                      |
| Helm charts & Kubernetes          | `lzr1:helm-engineer`                        |
| UI component development          | `lzr1:ui-engineer`                          |
| AI prompt quality review          | `lzr1:prompt-quality-reviewer`              |
| Backend quality assurance         | `lzr1:qa-analyst`                           |
| Frontend quality assurance         | `lzr1:qa-analyst-frontend`                  |
| Observability and reliability     | `lzr1:sre`                                  |
| Performance review                | `lzr1:performance-reviewer`                 |
| Multi-tenant usage review         | `lzr1:multi-tenant-reviewer`                |
| lib-commons usage review          | `lzr1:lib-commons-reviewer`                 |
| Best practices research           | `lzr1:best-practices-researcher`            |
| Framework documentation research  | `lzr1:framework-docs-researcher`            |
| Repository analysis               | `lzr1:repo-research-analyst`                |
| Product design & UX research      | `lzr1:product-designer`                     |
| Functional documentation (guides) | `lzr1:functional-writer`                    |
| API reference documentation       | `lzr1:api-writer`                           |
| Documentation quality review      | `lzr1:docs-reviewer`                        |

---

## 🔧 How lzr1 Works

### Session Startup

1. SessionStart hook runs automatically
2. All 77 skills are auto-discovered and available
3. `lzr1:using-lzr1` workflow is activated (skill checking is now mandatory)

### Agent Dispatching

```
Task tool:
  subagent_type: "lzr1:code-reviewer"
  prompt: [context]
    ↓
Runs agent
    ↓
Returns structured markdown output per the agent's documented sections
```

### Parallel Review Pattern

```
Single message with the selected review pool (not sequential):

Task #1: lzr1:code-reviewer
Task #2: lzr1:business-logic-reviewer
Task #3: lzr1:security-reviewer
Task #4: lzr1:test-reviewer
Task #5: lzr1:nil-safety-reviewer
Task #6: lzr1:dead-code-reviewer
Task #7: lzr1:performance-reviewer
Task #8: lzr1:multi-tenant-reviewer
Task #9: lzr1:lib-commons-reviewer
Conditional: lzr1:lib-observability-reviewer / lzr1:lib-systemplane-reviewer / lzr1:lib-streaming-reviewer when triggered
    ↓
All run in parallel (saves ~15 minutes vs sequential)
    ↓
Consolidated report
```

### Environment Variables

| Variable                | Default | Purpose                                                |
| ----------------------- | ------- | ------------------------------------------------------ |
| `CLAUDE_PLUGIN_ROOT`    | (auto)  | Path to installed plugin directory                     |

---

## 📚 More Information

- **Full Documentation** → `default/skills/*/SKILL.md` files
- **Agent Definitions** → `default/agents/*.md` and `dev-team/agents/*.md` files
- **Plugin Config** → `.claude-plugin/marketplace.json`
- **CLAUDE.md** → Project-specific instructions (checked into repo)

---

## ❓ Need Help?

- **How to use Claude Code?** → Ask about Claude Code features, MCP servers, skills
- **How to use lzr1?** → Check skill names in this manual or in `lzr1:using-lzr1` skill
- **Feature/bug tracking?** → https://github.com/victorlazari/lzr1-skills/issues
