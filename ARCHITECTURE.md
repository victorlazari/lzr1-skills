# lzr1 Architecture Documentation

## Table of Contents

1. [Overview](#overview)
2. [Marketplace Structure](#marketplace-structure)
3. [Component Hierarchy](#component-hierarchy)
4. [Core Components](#core-components)
5. [Data & Control Flow](#data--control-flow)
6. [Integration with Claude Code](#integration-with-claude-code)
7. [Execution Patterns](#execution-patterns)
8. [Component Relationships](#component-relationships)

## Overview

lzr1 is a **Claude Code plugin marketplace** that provides a comprehensive skills library and workflow system with **4 active plugins** (77 skills, 34 agents). It extends Claude Code's capabilities through structured, reusable patterns that enforce proven software engineelzr1 practices across the software delivery value chain: Product Planning → Development → Documentation.

Beyond Claude Code, each lzr1 plugin ships native install manifests for Codex (`<plugin>/.codex-plugin/`), Cursor (`<plugin>/.cursor-plugin/`), and OpenCode (`<plugin>/.opencode/`), plus a `lzr1-install.sh` symlink installer for local-dev workflows targeting Claude Code, Factory AI, OpenCode, and Codex.

### Architecture Philosophy

lzr1 operates on three core principles:

1. **Mandatory Workflows** - Critical skills (like lzr1:using-lzr1) enforce specific behaviors
2. **Parallel Execution** - Review systems run concurrently for speed
3. **Session Context** - Skills load automatically at session start
4. **Modular Plugins** - Specialized plugins for different domains and teams

### System Boundaries

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              Claude Code                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                          lzr1 Marketplace                                  │  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                       │  │
│  │  │ lzr1-default         │  │ lzr1-dev-team        │                       │  │
│  │  │ Skills(16) Agents(3) │  │ Skills(37) Agents(24)│                       │  │
│  │  │ Hooks/Lib            │  │                      │                       │  │
│  │  └──────────────────────┘  └──────────────────────┘                       │  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                       │  │
│  │  │ lzr1-pm-team         │  │ lzr1-tw-team         │                       │  │
│  │  │ Skills(18) Agents(4) │  │ Skills(6) Agents(3)  │                       │  │
│  │  └──────────────────────┘  └──────────────────────┘                       │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│  Native Tools: Skill, Task, TodoWrite                                           │
└─────────────────────────────────────────────────────────────────────────────────┘
```

> **Multi-harness install surface:** the diagram above shows Claude Code, the source-of-truth runtime. The same plugin tree is also installable in **Codex** (`<plugin>/.codex-plugin/plugin.json`), **Cursor** (`<plugin>/.cursor-plugin/plugin.json`), and **OpenCode** (`<plugin>/.opencode/plugins/lzr1-*.js` + `INSTALL.md`) via each harness's native package manager. For local-dev workflows, `lzr1-install.sh` symlinks the source tree into Claude Code, Factory AI, OpenCode, and Codex (with `.lzr1-build/` transformations for the latter two). See [README.md § Supported Platforms](README.md#-supported-platforms).

## Marketplace Structure

lzr1 is organized as a monorepo marketplace with multiple plugin collections:

```
lzr1/                                  # Monorepo root
├── .claude-plugin/
│   └── marketplace.json              # Multi-plugin registry (4 active plugins)
├── default/                          # Core plugin: lzr1-default
├── dev-team/                         # Developer agents: lzr1-dev-team
├── pm-team/                          # Product planning: lzr1-pm-team
└── tw-team/                          # Technical writing: lzr1-tw-team
```

### Active Plugins

_Versions managed in `.claude-plugin/marketplace.json`_

| Plugin               | Description                          | Components                       |
| -------------------- | ------------------------------------ | -------------------------------- |
| **lzr1-default**     | Core skills library                  | 16 skills, 3 agents               |
| **lzr1-dev-team**    | Developer agents                     | 37 skills, 24 agents              |
| **lzr1-pm-team**     | Product planning workflows           | 18 skills, 4 agents               |
| **lzr1-tw-team**     | Technical writing specialists        | 6 skills, 3 agents                |

## Component Hierarchy

### 1. Skills (`skills/`)

**Purpose:** Core instruction sets that define workflows and best practices

**Structure:**

```
skills/
├── {skill-name}/
│   └── SKILL.md           # Skill definition with frontmatter
├── shared-patterns/       # Reusable patterns across skills
│   ├── state-tracking.md
│   ├── failure-recovery.md
│   ├── exit-criteria.md
│   └── todowrite-integration.md
```

**Key Characteristics:**

- Self-contained directories with `SKILL.md` files
- YAML frontmatter: `name`, `description`
- Invoked via Claude's `Skill` tool
- Can reference shared patterns for common behaviors

### 2. Agents (`agents/`)

**Purpose:** Specialized agents that analyze code/designs or provide domain expertise using AI models

**Structure (lzr1-default plugin):**

```
default/agents/
├── review-slicer.md           # Thematic file grouping for large PRs (`lzr1:review-slicer`)
├── write-plan.md              # Implementation planning (`lzr1:write-plan`)
└── codebase-explorer.md       # Deep architecture analysis (`lzr1:codebase-explorer`)
```

**Structure (lzr1-dev-team plugin):**

```
dev-team/agents/
├── backend-engineer-golang.md         # Go backend specialist (`lzr1:backend-engineer-golang`)
├── backend-engineer-typescript.md     # TypeScript backend specialist (`lzr1:backend-engineer-typescript`)
├── devops-engineer.md                 # DevOps and infrastructure specialist (`lzr1:devops-engineer`)
├── frontend-bff-engineer-typescript.md # BFF specialist (`lzr1:frontend-bff-engineer-typescript`)
├── frontend-designer.md               # Visual design specialist (`lzr1:frontend-designer`)
├── frontend-engineer.md               # Frontend engineer (`lzr1:frontend-engineer`)
├── helm-engineer.md                   # Helm chart specialist (`lzr1:helm-engineer`)
├── code-reviewer.md                   # Foundation review (`lzr1:code-reviewer`)
├── business-logic-reviewer.md         # Correctness review (`lzr1:business-logic-reviewer`)
├── security-reviewer.md               # Safety review (`lzr1:security-reviewer`)
├── test-reviewer.md                   # Test coverage and quality review (`lzr1:test-reviewer`)
├── nil-safety-reviewer.md             # Null/nil safety analysis (`lzr1:nil-safety-reviewer`)
├── dead-code-reviewer.md              # Dead code analysis (`lzr1:dead-code-reviewer`)
├── lib-commons-reviewer.md            # lib-commons usage review (`lzr1:lib-commons-reviewer`)
├── lib-observability-reviewer.md      # Conditional observability review (`lzr1:lib-observability-reviewer`)
├── lib-systemplane-reviewer.md        # Conditional runtime-config review (`lzr1:lib-systemplane-reviewer`)
├── lib-streaming-reviewer.md          # Conditional event producer review (`lzr1:lib-streaming-reviewer`)
├── multi-tenant-reviewer.md           # Multi-tenant usage review (`lzr1:multi-tenant-reviewer`)
├── performance-reviewer.md              # Performance review (`lzr1:performance-reviewer`)
├── prompt-quality-reviewer.md         # Prompt quality specialist (`lzr1:prompt-quality-reviewer`)
├── qa-analyst.md                      # Backend QA specialist (`lzr1:qa-analyst`)
├── qa-analyst-frontend.md             # Frontend QA specialist (`lzr1:qa-analyst-frontend`)
├── sre.md                             # Observability and reliability specialist (`lzr1:sre`)
└── ui-engineer.md                     # UI component specialist (`lzr1:ui-engineer`)
```

**Key Characteristics:**

- Invoked via Claude's `Task` tool with `subagent_type`
- Invoked with specialized subagent_type for domain-specific analysis
- Review agents run in parallel (9 defaults plus triggered specialists dispatch simultaneously via `lzr1:codereview` skill)
- Developer agents provide specialized domain expertise
- Return structured reports with severity-based findings

**Note:** Parallel review orchestration is handled by the `lzr1:codereview` skill

**Standards Compliance Output (refactor-capable dev-team agents):**

Refactor-capable lzr1-dev-team agents produce a `## Standards Compliance` section in their output schema:

```yaml
- name: "Standards Compliance"
  pattern: "^## Standards Compliance"
  required: false # In schema, but MANDATORY when invoked from lzr1:dev-refactor
  description: "MANDATORY when invoked from lzr1:dev-refactor skill"
```

**Conditional Requirement: `invoked_from_dev_refactor`**

| Invocation Context            | Standards Compliance | Detection Mechanism                       |
| ----------------------------- | -------------------- | ----------------------------------------- |
| Direct agent call             | Optional             | N/A                                       |
| Via `lzr1:dev-cycle` skill    | Optional             | N/A                                       |
| Via `lzr1:dev-refactor` skill | **MANDATORY**        | Prompt contains `**MODE: ANALYSIS ONLY**` |

**How Enforcement Works:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  User invokes: lzr1:dev-refactor skill                      │
│         ↓                                                           │
│  lzr1:dev-refactor skill dispatches agents with prompt:                  │
│  "**MODE: ANALYSIS ONLY** - Compare codebase with lzr1 standards"   │
│         ↓                                                           │
│  Agent detects "**MODE: ANALYSIS ONLY**" in prompt                  │
│         ↓                                                           │
│  Agent loads lzr1 standards via WebFetch                            │
│         ↓                                                           │
│  Agent produces Standards Compliance output (MANDATORY)             │
└─────────────────────────────────────────────────────────────────────┘
```

**Affected Agents:**

- `lzr1:backend-engineer-golang` → loads `golang.md`
- `lzr1:backend-engineer-typescript` → loads `typescript.md`
- `lzr1:frontend-bff-engineer-typescript` → loads `typescript.md`
- `lzr1:frontend-designer` → loads `frontend.md`
- `lzr1:qa-analyst-frontend` → loads `frontend/testing-*.md` (accessibility/visual/e2e/performance)

**Output Format (when non-compliant):**

```markdown
## Standards Compliance

### lzr1/lzr1 Standards Comparison

| Category | Current Pattern | Expected Pattern | Status           | File/Location |
| -------- | --------------- | ---------------- | ---------------- | ------------- |
| Logging  | fmt.Println     | lib-observability/zap  | ⚠️ Non-Compliant | service/\*.go |

### Compliance Summary

- Total Violations: N
- Critical: N, High: N, Medium: N, Low: N

### Required Changes for Compliance

1. **Category Migration**
   - Replace: `current pattern`
   - With: `expected pattern`
   - Files affected: [list]
```

**Cross-References:**

- CLAUDE.md: Standards Compliance (Conditional Output Section)
- `dev-team/skills/dev-refactor/SKILL.md`: HARD GATES defining requirement
- `dev-team/hooks/session-start.sh`: Injects guidance at session start

### 3. Hooks (`hooks/`)

**Purpose:** Session lifecycle management and automatic initialization

**Structure:**

```
default/hooks/
├── hooks.json              # Hook configuration (SessionStart)
├── session-start.sh        # Main initialization script
└── generate-skills-ref.py  # Dynamic skill reference generator
```

**Key Characteristics:**

- Triggers on SessionStart events (startup|resume, clear|compact)
- Injects skills context into Claude's memory
- Auto-generates skills quick reference from frontmatter
- Ensures mandatory workflows are loaded

### 4. Plugin Configuration (`.claude-plugin/`)

**Purpose:** Integration metadata for Claude Code marketplace

**Structure:**

```
.claude-plugin/
└── marketplace.json    # Multi-plugin registry
    ├── lzr1-default     # Core skills library
    ├── lzr1-dev-team    # Developer agents
    ├── lzr1-pm-team     # Product planning
    └── lzr1-tw-team     # Technical writing
```

**marketplace.json Schema:**

```json
{
  "name": "lzr1",
  "description": "...",
  "owner": { "name": "...", "email": "..." },
  "plugins": [
    {
      "name": "lzr1-default",
      "version": "...",
      "source": "./default",
      "keywords": ["skills", "tdd", "debugging", ...]
    },
    {
      "name": "lzr1-dev-team",
      "version": "...",
      "source": "./dev-team",
      "keywords": ["developer", "agents"]
    },
    {
      "name": "lzr1-pm-team",
      "version": "...",
      "source": "./pm-team",
      "keywords": ["product", "planning"]
    },
    {
      "name": "lzr1-tw-team",
      "version": "...",
      "source": "./tw-team",
      "keywords": ["technical-writing", "documentation"]
    }
  ]
}
```

### 5. Per-Harness Install Manifests

**Purpose:** Native install surface for non-Claude harnesses. Each lzr1 plugin ships its own per-harness manifest, so Codex, Cursor, and OpenCode install the plugin directly via their package managers — no transformation step, no central installer required.

**Structure (replicated under each of `default/`, `dev-team/`, `pm-team/`, `tw-team/`):**

```
<plugin>/
├── .codex-plugin/
│   └── plugin.json              # Codex manifest (name, version, skills/agents paths, interface)
├── .cursor-plugin/
│   └── plugin.json              # Cursor manifest (skills, agents, hooks paths)
└── .opencode/
    ├── INSTALL.md               # End-user install instructions for this plugin in OpenCode
    └── plugins/
        └── lzr1-<plugin>.js     # OpenCode runtime plugin (registers skills path; lzr1-default also injects using-lzr1 bootstrap)
```

**Key Characteristics:**

- **Decentralized vs `.claude-plugin/`:** Claude Code uses one root-level marketplace.json that enumerates all 4 plugins. Codex/Cursor/OpenCode use per-plugin manifests so each plugin is independently installable.
- **OpenCode JS specifics:** `lzr1-default/.opencode/plugins/lzr1-default.js` is the only one that injects the `using-lzr1` bootstrap into the first user message of each session (mirrors Claude Code's session-start hook). The other three plugins' JS files only register their skills directory.
- **Versioning:** all per-harness manifests carry the same version as `marketplace.json` (kept in sync via `.github/workflows/version-bump.yml`).

**Local-dev alternative:** `lzr1-install.sh` at repo root provides symlink installs (per-file for Claude Code/Factory AI; transformed `.lzr1-build/` tree for Codex/OpenCode). Best for hot-reload local development against the source tree.

## Data & Control Flow

### Session Initialization Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude Code
    participant hooks.json
    participant session-start.sh
    participant generate-skills-ref.py
    participant Claude Context

    User->>Claude Code: Start new session
    Claude Code->>hooks.json: Check SessionStart hooks
    hooks.json->>session-start.sh: Execute initialization
    session-start.sh->>generate-skills-ref.py: Generate skills overview
    generate-skills-ref.py-->>session-start.sh: Return formatted reference
    session-start.sh->>Claude Context: Inject skills + lzr1:using-lzr1 content
    Claude Context-->>User: Session ready with skills loaded
```

### Skill Invocation Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude
    participant Skill Tool
    participant SKILL.md
    participant TodoWrite

    User->>Claude: Request task
    Claude->>Claude: Check lzr1:using-lzr1 mandatory workflow
    Claude->>Skill Tool: Invoke relevant skill
    Skill Tool->>SKILL.md: Load skill instructions
    SKILL.md-->>Claude: Return structured workflow
    Claude->>TodoWrite: Create task tracking (if multi-step)
    Claude->>User: Execute skill with progress updates
```

### Parallel Review Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude
    participant Task Tool
    participant lzr1:code-reviewer
    participant lzr1:business-logic-reviewer
    participant lzr1:security-reviewer
    participant lzr1:test-reviewer
    participant lzr1:nil-safety-reviewer
    participant DCR as lzr1:dead-code-reviewer
    participant PR as lzr1:performance-reviewer
    participant MTR as lzr1:multi-tenant-reviewer
    participant LCR as lzr1:lib-commons-reviewer

    User->>Claude: Use lzr1:codereview skill
    Note over Claude: Skill provides<br/>parallel review workflow

    Claude->>Task Tool: Dispatch 9 default parallel tasks

    par Parallel Execution
        Task Tool->>lzr1:code-reviewer: Review architecture
        and
        Task Tool->>lzr1:business-logic-reviewer: Review correctness
        and
        Task Tool->>lzr1:security-reviewer: Review vulnerabilities
        and
        Task Tool->>lzr1:test-reviewer: Review test coverage
        and
        Task Tool->>lzr1:nil-safety-reviewer: Review nil safety
        and
        Task Tool->>DCR: Review dead code
        and
        Task Tool->>PR: Review performance
        and
        Task Tool->>MTR: Review multi-tenant usage
        and
        Task Tool->>LCR: Review lib-commons usage
    end

    opt Conditional specialists triggered by changed stack
        Task Tool->>Task Tool: Dispatch lib-observability/lib-systemplane/lib-streaming reviewers in same batch
    end

    lzr1:code-reviewer-->>Claude: Return findings
    lzr1:business-logic-reviewer-->>Claude: Return findings
    lzr1:security-reviewer-->>Claude: Return findings
    lzr1:test-reviewer-->>Claude: Return findings
    lzr1:nil-safety-reviewer-->>Claude: Return findings
    DCR-->>Claude: Return findings
    PR-->>Claude: Return findings
    MTR-->>Claude: Return findings
    LCR-->>Claude: Return findings

    Note over Claude: Aggregate & prioritize by severity
    Claude->>User: Consolidated report
```

## Integration with Claude Code

### Native Tool Integration

lzr1 leverages three primary Claude Code tools:

1. **Skill Tool**

   - Invokes skills by name: `skill: "lzr1:test-driven-development"`
   - Skills expand into full instructions within conversation
   - Skill content becomes part of Claude's working context

2. **Task Tool**

   - Dispatches agents to subagent instances: `Task(subagent_type="lzr1:code-reviewer")`
   - Enables parallel execution (multiple Tasks in one message)
   - Returns structured reports from independent analysis

3. **TodoWrite Tool**

   - Tracks multi-step workflows: `TodoWrite(todos=[...])`
   - Integrates with skills via shared patterns
   - Provides progress visibility to users

### Session Context Injection

At session start, lzr1 injects two critical pieces of context:

1. **Skills Quick Reference** - Auto-generated overview of all available skills
2. **lzr1:using-lzr1 Skill** - Mandatory workflow that enforces skill checking

This context becomes part of Claude's memory for the entire session, ensulzr1:

- Claude knows which skills are available
- Mandatory workflows are enforced
- Skills are checked before any task

## Execution Patterns

### Pattern 1: Mandatory Skill Checking

```
User Request → lzr1:using-lzr1 check → Relevant skill?
    ├─ Yes → Invoke skill → Follow workflow
    └─ No → Proceed with task
```

**Implementation:** The lzr1:using-lzr1 skill is loaded at session start and contains strict instructions to check for relevant skills before ANY task.

### Pattern 2: Parallel Review Execution

```
Review Request → lzr1:codereview skill → lzr1:review-slicer (classify)
    ├─ Small/focused PR → 9 default Tasks in parallel (full diff)
    └─ Large/multi-theme PR → For EACH slice:
        ├─ lzr1:code-reviewer            ─┐
        ├─ lzr1:business-logic-reviewer   │
        ├─ lzr1:security-reviewer         │
        ├─ lzr1:test-reviewer             │
        ├─ lzr1:nil-safety-reviewer       │
        ├─ lzr1:dead-code-reviewer        ┼─→ Merge + dedup → Handle by severity
        ├─ lzr1:performance-reviewer      │
        ├─ lzr1:multi-tenant-reviewer     │
        └─ lzr1:lib-commons-reviewer     ─┘

        Conditional specialists join the same batch only when triggered:
        lzr1:lib-observability-reviewer, lzr1:lib-systemplane-reviewer,
        lzr1:lib-streaming-reviewer
```

**Implementation:** The `lzr1:review-slicer` agent classifies files into thematic slices for large PRs (15+ files). For each slice, the diagrammed 9 default reviewers always dispatch in parallel via a single message. Conditional specialists (`lzr1:lib-observability-reviewer`, `lzr1:lib-systemplane-reviewer`, `lzr1:lib-streaming-reviewer`) join that same batch only when their triggers match. Results are merged and deduplicated before consolidation. Small PRs skip slicing entirely (zero overhead).

### Pattern 3: Progressive Skill Execution

```
Complex Skill → TodoWrite tracking
    ├─ Phase 1: Understanding     [in_progress]
    ├─ Phase 2: Exploration       [pending]
    ├─ Phase 3: Design           [pending]
    └─ Phase 4: Documentation    [pending]
```

**Implementation:** Multi-phase skills use TodoWrite to track progress through structured workflows.

## Component Relationships

### Skills ↔ Agents

**Difference:**

- **Skills:** Instructions executed by current Claude instance
- **Agents:** Specialized reviewers executed by separate Claude instances

**Interaction:**

- Skills can invoke agents (e.g., lzr1:codereview skill dispatches review agents)
- Agents don't typically invoke skills (they're independent analyzers)

### Skills ↔ Shared Patterns

**Relationship:** Inheritance/composition

- Skills reference shared patterns for common behaviors
- Patterns provide reusable workflows (state tracking, failure recovery)

**Example:**

```markdown
# In a skill:

See `skills/shared-patterns/todowrite-integration.md` for tracking setup
```

### Hooks ↔ Skills

**Relationship:** Initialization and context loading

- Hooks load skill metadata at session start
- generate-skills-ref.py scans all SKILL.md frontmatter
- session-start.sh injects lzr1:using-lzr1 skill content

**Data Flow:**

```
SKILL.md frontmatter → generate-skills-ref.py → formatted overview → session context
```

### Agents ↔ Orchestrator

**Relationship:** Agent dispatch via Task tool

- Agents are invoked via `Task(subagent_type: "lzr1:{agent-name}")`
- Review agents run in parallel for comprehensive analysis
- Agent specialization determines depth and quality of analysis

### TodoWrite ↔ Skills

**Relationship:** Progress tracking integration

- Multi-step skills create TodoWrite items
- Each phase updates todo status (pending → in_progress → completed)
- Provides user visibility into workflow progress

## Key Architectural Decisions

### 1. Parallel vs Sequential Reviews

**Decision:** Reviews run in parallel, not sequentially
**Rationale:** 3x faster feedback, comprehensive coverage, easier prioritization
**Implementation:** Single message with multiple Task calls

### 2. Session Context Injection

**Decision:** Load all skills metadata at session start
**Rationale:** Ensures Claude always knows available capabilities
**Trade-off:** Larger initial context vs. consistent skill awareness

### 3. Mandatory Workflows

**Decision:** Some skills (lzr1:using-lzr1) are non-negotiable
**Rationale:** Prevents common failures, enforces best practices
**Enforcement:** Loaded automatically, contains strict instructions

### 4. Skill vs Agent Separation

**Decision:** Skills for workflows, agents for analysis
**Rationale:** Different execution models (local vs. subagent)
**Benefit:** Clear separation of concerns

### 5. Frontmatter-Driven Discovery

**Decision:** All metadata in YAML frontmatter
**Rationale:** Single source of truth, easy parsing, consistent structure
**Usage:** Auto-generation of documentation, skill matching

## Extension Points

### Adding New Skills

1. Create `skills/{name}/SKILL.md` with frontmatter
2. Skills auto-discovered by generate-skills-ref.py
3. Available immediately after session restart

### Adding New Agents

1. Create `{plugin}/agents/{name}.md` with agent definition
2. Include YAML frontmatter: `name`, `description`, `version`
3. Invoke via Task tool with `subagent_type="lzr1:{name}"`
4. Review agents can run in parallel via `lzr1:codereview` skill
5. Developer agents provide domain expertise via direct Task invocation

### Adding Shared Patterns

1. Create `skills/shared-patterns/{pattern}.md`
2. Reference from skills that need the pattern
3. Maintains consistency across skills

### Adding New Plugins

1. Create plugin directory: `mkdir -p {plugin-name}/{skills,agents,hooks,lib}`
2. Register in `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "lzr1-{plugin-name}",
     "version": "0.1.0",
     "source": "./{plugin-name}",
     "keywords": [...]
   }
   ```
   (Note: Initial version is 0.1.0, then managed via version bumps)
3. Create `{plugin-name}/hooks/hooks.json` for initialization
4. Add skills/agents following same structure as `default/`

## Performance Considerations

### Parallel Execution Benefits

- **3x faster reviews** - All reviewers run simultaneously
- **No blocking** - Independent agents don't wait for each other
- **Better resource utilization** - Multiple Claude instances work concurrently

### Context Management

- **Session start overhead** - One-time loading of skills context
- **Skill invocation** - Skills expand inline, no additional calls
- **Agent invocation** - Separate instances, clean context per agent

### Optimization Strategies

1. **Selective agent usage** - Only invoke relevant reviewers
2. **Skill caching** - Skills loaded once per session
3. **Parallel by default** - Never chain reviewers sequentially
4. **Early validation** - Preflight checks prevent wasted work

## Common Patterns and Anti-Patterns

### Patterns to Follow

✅ Check for relevant skills before any task
✅ Run reviewers in parallel for speed
✅ Use TodoWrite for multi-step workflows
✅ Reference shared patterns for consistency
✅ Specify models explicitly for agents

### Anti-Patterns to Avoid

❌ Skipping skill checks (violates lzr1:using-lzr1)
❌ Running reviewers sequentially (3x slower)
❌ Implementing without tests (violates TDD)
❌ Claiming completion without verification
❌ Hardcoding workflows instead of using skills

## Troubleshooting Guide

### Skills Not Loading

1. Check hooks/hooks.json configuration
2. Verify session-start.sh is executable
3. Ensure SKILL.md has valid frontmatter

### Parallel Reviews Not Working

1. Ensure all Task calls in single message
2. Verify agent names match exactly
3. Check agent names match exactly

### Context Overflow

1. Consider selective skill loading
2. Use focused agent invocations
3. Clear completed todos regularly

## Summary

lzr1's architecture is designed for:

- **Modularity** - Independent, composable components across multiple plugins
- **Performance** - Parallel execution wherever possible (3x faster reviews)
- **Reliability** - Mandatory workflows prevent failures
- **Extensibility** - Easy to add new skills/agents/plugins
- **Scalability** - Marketplace structure supports product and team-specific plugins
- **Integration** - Seamless with Claude Code's native tools

### Current State

_Component counts reflect current state; plugin versions managed in `.claude-plugin/marketplace.json`_

| Component                 | Count      | Location               |
| ------------------------- | ---------- | ---------------------- |
| Active Plugins            | 4          | All plugin directories |
| Skills (lzr1-default)     | 16         | `default/skills/`      |
| Skills (lzr1-dev-team)    | 37         | `dev-team/skills/`     |
| Skills (lzr1-pm-team)     | 18         | `pm-team/skills/`      |
| Skills (lzr1-tw-team)     | 6          | `tw-team/skills/`      |
| **Total Skills**          | **77**     | **All plugins**        |
| Agents (lzr1-default)     | 3          | `default/agents/`      |
| Agents (lzr1-dev-team)    | 24         | `dev-team/agents/`     |
| Agents (lzr1-pm-team)     | 4          | `pm-team/agents/`      |
| Agents (lzr1-tw-team)     | 3          | `tw-team/agents/`      |
| **Total Agents**          | **34**     | **All plugins**        |
| Hooks                     | Per plugin | `{plugin}/hooks/`      |

The system achieves these goals through clear component separation, structured workflows, automatic context management, and a modular marketplace architecture, creating a robust foundation for AI-assisted software development.
