## Step 0: Verify PROJECT_RULES.md Exists (HARD GATE)

**NON-NEGOTIABLE. Cycle CANNOT proceed without project standards.**

### Step 0 Flow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  Check: Does docs/PROJECT_RULES.md exist?                                   │
│                                                                             │
│  ├── YES → Proceed to Step 1 (Initialize or Resume)                        │
│  │                                                                          │
│  └── no → ASK: "Is this a LEGACY project (created without PM workflow)?"   │
│       │                                                                     │
│       ├── YES (legacy project) → LEGACY PROJECT ANALYSIS:                   │
│       │   Step 1: Dispatch lzr1:codebase-explorer (technical info only)          │
│       │   Step 2: Ask 3 questions (what agent can't determine):             │
│       │     1. What do you need help with?                                  │
│       │     2. Any external APIs not visible in code?                       │
│       │     3. Any specific technology not in lzr1 Standards?               │
│       │   Step 3: Generate PROJECT_RULES.md (deduplicated from lzr1)        │
│       │   Note: Business rules belong in PRD, not in PROJECT_RULES          │
│       │   → Proceed to Step 1                                               │
│       │                                                                     │
│       └── no (new project) → ASK: "Do you have PRD, TRD, or Feature Map?"  │
│           │                                                                 │
│           ├── YES (has PM docs) → "Please provide the file path(s)"        │
│           │   → Read PRD/TRD/Feature Map → Extract info                    │
│           │   → Generate PROJECT_RULES.md                                  │
│           │   → Ask supplementary questions if info is incomplete          │
│           │   → Save and proceed to Step 1                                 │
│           │                                                                 │
│           └── no (no PM docs) → ⛔ HARD BLOCK:                              │
│               "PM documents are REQUIRED for new projects.                  │
│                Run /lzr1:pre-dev-full or /lzr1:pre-dev-feature first."               │
│               → STOP (cycle cannot proceed)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Step 0.1: Check for PROJECT_RULES.md

```yaml
# Check if file exists
Read tool:
  file_path: "docs/PROJECT_RULES.md"

# If file exists and has content → Proceed to Step 1
# If file does not exist or is empty → Continue to Step 0.2
```

### Step 0.2: Check if Legacy Project

#### Ask the User

Use AskUserQuestion:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 PROJECT_RULES.md not FOUND                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I need to create docs/PROJECT_RULES.md to understand your       │
│ project's specific conventions and domain.                      │
│                                                                 │
│ First, I need to know: Is this a LEGACY project?                │
│                                                                 │
│ A legacy project is one that was created WITHOUT using the      │
│ PM team workflow (no PRD, TRD, or Feature Map documents).       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Question

"Is this a legacy project (created without PM team workflow)?"

#### Options

(a) Yes, this is a legacy project (b) No, this is a new project following lzr1 workflow

#### If YES (legacy)

Go to Step 0.2.1 (Legacy Project Analysis)

#### If no (new project)

Go to Step 0.3 (Check for PM Documents)

### Step 0.2.1: Legacy Project Analysis (Technical Only)

#### Overview

For legacy projects, analyze codebase for TECHNICAL information only:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 LEGACY PROJECT ANALYSIS                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Since this is a legacy project, I'll analyze the codebase       │
│ for TECHNICAL information (not business rules).                 │
│                                                                 │
│ Step 1: Automated analysis (lzr1:codebase-explorer)                  │
│ Step 2: Ask for project-specific tech not in lzr1 Standards     │
│ Step 3: Generate PROJECT_RULES.md (deduplicated)                │
│                                                                 │
│ Note: Business rules belong in PRD/product docs, not here.      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Step 0.2.1a: Automated Codebase Analysis (MANDATORY)

**⛔ You MUST use the Task tool to dispatch lzr1:codebase-explorer. This is not implicit.**

#### Dispatch Agent

Dispatch lzr1:codebase-explorer to analyze the legacy project for TECHNICAL information:

```text
Action: Use Task tool with EXACTLY these parameters:

┌─────────────────────────────────────────────────────────────────────────────────┐
│  ⛔ If Task tool not used → Analysis does not happen → PROJECT_RULES.md INVALID │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```yaml
# Agent 1: Codebase Explorer - Technical Analysis
Task tool:
  subagent_type: "lzr1:codebase-explorer"
  description: "Analyze legacy project for PROJECT_RULES.md"
  prompt: |
    Analyze this LEGACY codebase to extract technical information for PROJECT_RULES.md.
    
    This is an existing project created without PM documentation.
    Your job is to understand what exists in the code.
    
    **Extract:**
    1. **Project Structure:** Directory layout, module organization
    2. **Technical Stack:** Languages, frameworks, databases, external services
    3. **Architecture Patterns:** Clean Architecture, MVC, microservices, etc.
    4. **Existing Features:** Main modules, endpoints, capabilities
    5. **Internal Libraries:** Shared packages, utilities
    6. **Configuration:** Environment variables, config patterns
    7. **Database:** Schema patterns, migrations, ORM usage
    8. **External Integrations:** APIs consumed, message queues
    
    **Output format:**
    ## Technical Analysis (Legacy Project)
    
    ### Project Overview
    [What this project appears to do based on code analysis]
    
    ### Technical Stack
    - Language: [detected]
    - Framework: [detected]
    - Database: [detected]
    - External Services: [detected]
    
    ### Architecture Patterns
    [Detected patterns]
    
    ### Existing Features
    [List of features/modules found]
    
    ### Project Structure
    [Directory layout explanation]
    
    ### Configuration
    [Env vars, config files found]
    
    ### External Integrations
    [APIs, services detected]

```

**Note:** Business logic analysis is not needed for PROJECT_RULES.md. Business rules belong in PRD/product docs, not technical project rules.

#### Verification (MANDATORY)

After agent completes, confirm:
- [ ] `lzr1:codebase-explorer` returned "## Technical Analysis (Legacy Project)" section
- [ ] Output contains non-empty content for: Tech Stack, External Integrations, Configuration

**If agent failed or returned empty output → Re-dispatch. Cannot proceed without technical analysis.**

#### Step 0.2.1b: Supplementary Questions (Only What Agents Can't Determine)

#### Post-Analysis Questions

After agents complete, ask only what they couldn't determine from code:

```text
┌─────────────────────────────────────────────────────────────────┐
│ ✓ Codebase Analysis Complete                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I've analyzed your codebase. Now I need a few details that      │
│ only you can provide (not visible in the code).                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Questions to Ask

Use AskUserQuestion for each:

| # | Question | Why Agents Can't Determine This |
|---|----------|--------------------------------|
| 1 | **What do you need help with?** (Current task/feature/fix) | Future intent, not in code |
| 2 | **Any external APIs or services not visible in code?** (Third-party integrations planned) | Planned integrations, not yet in code |
| 3 | **Any specific technology not in lzr1 Standards?** (Message broker, cache, etc.) | Project-specific tech not in lzr1 |

**Note:** Business rules belong in PRD/product docs, not in PROJECT_RULES.md.

#### Step 0.2.1c: Generate PROJECT_RULES.md

#### Combine Agent Outputs and User Answers

```yaml
Create tool:
  file_path: "docs/PROJECT_RULES.md"
  content: |
    # Project Rules
    
    > lzr1 Standards apply automatically. This file documents only what lzr1 does not cover.
    > For error handling, logging, testing, architecture, lib-commons, lib-observability, lib-systemplane, lib-streaming → See lzr1 Standards (auto-loaded by agents)
    > Generated from legacy project analysis.
    
    ## What lzr1 Standards Already Cover (DO not ADD HERE)
    
    The following are defined in lzr1 Standards and MUST not be duplicated:
    - Error handling patterns (no panic, wrap errors)
    - Logging standards (structured JSON via lib-observability `log`/`zap` adapters)
    - Testing patterns (table-driven tests, mocks)
    - Architecture patterns (Hexagonal, Clean Architecture)
    - Observability (OpenTelemetry tracing/metrics, panic recovery, assertions, redaction) — via lib-observability
    - lib-commons usage and patterns (lifecycle, outbox repository, circuit breakers, tenant management, HTTP, idempotency)
    - lib-observability usage and patterns (tracing, metrics, logging, assert, runtime, redaction) — see [[using-lib-observability]]
    - lib-systemplane usage and patterns (hot-reloadable runtime config: log levels, feature flags, rate limits, timeouts) — see [[using-lib-systemplane]]
    - lib-streaming usage and patterns (past-tense business event emission to per-tenant SaaS subscribers) — see [[using-lib-streaming]]
    - API directory structure
    
    ---
    
    ## Tech Stack (Not in lzr1 Standards)
    
    [From lzr1:codebase-explorer: Technologies not covered by lzr1 Standards]
    [e.g., specific message broker, specific cache, DB if not PostgreSQL]
    
    | Technology | Purpose | Notes |
    |------------|---------|-------|
    | [detected] | [purpose] | [notes] |
    
    ## Non-Standard Directory Structure
    
    [From lzr1:codebase-explorer: Directories that deviate from lzr1's standard API structure]
    [e.g., workers/, consumers/, polling/]
    
    | Directory | Purpose | Pattern |
    |-----------|---------|---------|
    | [detected] | [purpose] | [pattern] |
    
    ## External Integrations
    
    [From lzr1:codebase-explorer: Third-party services specific to this project]
    
    | Service | Purpose | Docs |
    |---------|---------|------|
    | [detected] | [purpose] | [link] |
    
    ## Environment Configuration
    
    [From lzr1:codebase-explorer: Project-specific env vars not covered by lzr1]
    
    | Variable | Purpose | Example |
    |----------|---------|---------|
    | [detected] | [purpose] | [example] |
    
    ## Domain Terminology
    
    [From codebase analysis: Technical names used in this codebase]
    
    | Term | Definition | Used In |
    |------|------------|---------|
    | [detected] | [definition] | [location] |
    
    ---
    
    *Generated: [ISO timestamp]*
    *Source: Legacy project analysis (lzr1:codebase-explorer)*
    *lzr1 Standards Version: [version from WebFetch]*
```

#### Present to User

```text
┌─────────────────────────────────────────────────────────────────┐
│ ✓ PROJECT_RULES.md Generated for Legacy Project                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ I analyzed your codebase using:                                 │
│   • lzr1:codebase-explorer (technical patterns, stack, structure)    │
│                                                                 │
│ Combined with your input on:                                    │
│   • Current development goal                                    │
│   • External integrations                                       │
│   • Project-specific technology                                 │
│                                                                 │
│ Generated: docs/PROJECT_RULES.md                                │
│                                                                 │
│ Note: lzr1 Standards (error handling, logging, testing, etc.)   │
│ are not duplicated - agents load them automatically via WebFetch│
│                                                                 │
│ Please review the file and make any corrections needed.         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Ask for Approval

Use AskUserQuestion:
- Question: "PROJECT_RULES.md has been generated. Would you like to review it before proceeding?"
- Options: (a) Proceed (b) Open for editing first

#### After Approval

Proceed to Step 1

### Step 0.3: Check for PM Documents (PRD/TRD/Feature Map)

#### Check for PM Documents

For NEW projects (not legacy), ask about PM documents:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 📋 NEW PROJECT - PM DOCUMENTS CHECK                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Since this is a new project following lzr1 workflow, you        │
│ should have PM documents from the pre-dev workflow.             │
│                                                                 │
│ Do you have any of these PM documents?                          │
│   • PRD (Product Requirements Document)                         │
│   • TRD (Technical Requirements Document)                       │
│   • Feature Map (from lzr1:pre-dev-feature-map skill)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Question

"Do you have PRD, TRD, or Feature Map documents for this project?"

#### Options

(a) Yes, I have PM documents (b) No, I don't have these documents

#### If YES - Ask for File Paths

```text
"Please provide the file path(s) to your PM documents:
 - PRD path (or 'skip' if none): 
 - TRD path (or 'skip' if none): 
 - Feature Map path (or 'skip' if none): "
```

#### Example Paths

Typical PM team output structure:

```text
docs/pre-dev/{feature-name}/
├── prd.md              → PRD path: docs/pre-dev/auth-system/prd.md
├── trd.md              → TRD path: docs/pre-dev/auth-system/trd.md
├── feature-map.md      → Feature Map path: docs/pre-dev/auth-system/feature-map.md
├── api-design.md
├── data-model.md
└── tasks.md
```

#### Common Patterns

- `/lzr1:pre-dev-full` output: `docs/pre-dev/{feature}/prd.md`, `trd.md`, `feature-map.md`
- `/lzr1:pre-dev-feature` output: `docs/pre-dev/{feature}/prd.md`, `feature-map.md`
- Custom locations: User may have docs in different paths (e.g., `requirements/`, `specs/`)

#### Then

Go to Step 0.3.1 (Generate from PM Documents)

#### If no

HARD BLOCK (Step 0.3.2)

### Step 0.3.1: Generate from PM Documents (PRD/TRD/Feature Map)

#### Read the Provided Documents

```yaml
# Read PRD if provided
Read tool:
  file_path: "[user-provided PRD path]"

# Read TRD if provided  
Read tool:
  file_path: "[user-provided TRD path]"

# Read Feature Map if provided
Read tool:
  file_path: "[user-provided Feature Map path]"
```

#### Extract PROJECT_RULES.md Content from PM Documents

**⛔ DEDUPLICATION RULE:** Extract only what lzr1 Standards DO NOT cover.

| From PRD | Extract For PROJECT_RULES.md | Note |
|----------|------------------------------|------|
| Domain terms, entities | Domain Terminology | Technical names only |
| External service mentions | External Integrations | Third-party APIs |
| ~~Business rules~~ | ~~N/A~~ | ❌ Stays in PRD, not PROJECT_RULES |
| ~~Architecture~~ | ~~N/A~~ | ❌ lzr1 Standards covers this |

| From TRD | Extract For PROJECT_RULES.md | Note |
|----------|------------------------------|------|
| Tech stack not in lzr1 | Tech Stack (Not in lzr1) | Only non-standard tech |
| External APIs | External Integrations | Third-party services |
| Non-standard directories | Non-Standard Directory Structure | Workers, consumers, etc. |
| ~~Architecture decisions~~ | ~~N/A~~ | ❌ lzr1 Standards covers this |
| ~~Database patterns~~ | ~~N/A~~ | ❌ lzr1 Standards covers this |

| From Feature Map | Extract For PROJECT_RULES.md | Note |
|------------------|------------------------------|------|
| Technology choices not in lzr1 | Tech Stack (Not in lzr1) | Only if not in lzr1 |
| External dependencies | External Integrations | Third-party services |
| ~~Architecture~~ | ~~N/A~~ | ❌ lzr1 Standards covers this |

#### Generate PROJECT_RULES.md

```yaml
Create tool:
  file_path: "docs/PROJECT_RULES.md"
  content: |
    # Project Rules
    
    > ⛔ IMPORTANT: lzr1 Standards are not automatic. Agents MUST WebFetch them before implementation.
    > This file documents only project-specific information not covered by lzr1 Standards.
    > Generated from PM documents (PRD/TRD/Feature Map).
    >
    > lzr1 Standards URLs:
    > - Go: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/golang.md
    > - TypeScript: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/typescript.md
    
    ## What lzr1 Standards Cover (DO not DUPLICATE HERE)
    
    The following are defined in lzr1 Standards and MUST not be duplicated in this file:
    - Error handling patterns (no panic, wrap errors)
    - Logging standards (structured JSON via lib-observability `log`/`zap` adapters)
    - Testing patterns (table-driven tests, mocks)
    - Architecture patterns (Hexagonal, Clean Architecture)
    - Observability (OpenTelemetry tracing/metrics, panic recovery, assertions, redaction) — via lib-observability
    - lib-commons / lib-common-js usage and patterns (lifecycle, outbox repository, circuit breakers, tenant management, HTTP, idempotency)
    - lib-observability usage and patterns (tracing, metrics, logging, assert, runtime, redaction) — see [[using-lib-observability]]
    - lib-systemplane usage and patterns (hot-reloadable runtime config: log levels, feature flags, rate limits, timeouts) — see [[using-lib-systemplane]]
    - lib-streaming usage and patterns (past-tense business event emission to per-tenant SaaS subscribers) — see [[using-lib-streaming]]
    - API directory structure (lzr1 pattern)
    - Database connections (PostgreSQL, MongoDB, Redis via lib-commons)
    - Bootstrap pattern (config.go, service.go, server.go)
    
    **Agents MUST WebFetch lzr1 Standards and output Standards Coverage Table.**
    
    ---
    
    ## Tech Stack (Not in lzr1 Standards)
    
    [From TRD/Feature Map: only technologies not covered by lzr1 Standards]
    
    | Technology | Purpose | Notes |
    |------------|---------|-------|
    | [detected] | [purpose] | [notes] |
    
    ## Non-Standard Directory Structure
    
    [From TRD: Directories that deviate from lzr1's standard API structure]
    
    | Directory | Purpose | Pattern |
    |-----------|---------|---------|
    | [detected] | [purpose] | [pattern] |
    
    ## External Integrations
    
    [From TRD/PRD: Third-party services specific to this project]
    
    | Service | Purpose | Docs |
    |---------|---------|------|
    | [detected] | [purpose] | [link] |
    
    ## Environment Configuration
    
    [From TRD: Project-specific env vars not covered by lzr1]
    
    | Variable | Purpose | Example |
    |----------|---------|---------|
    | [detected] | [purpose] | [example] |
    
    ## Domain Terminology
    
    [From PRD: Technical names used in this codebase]
    
    | Term | Definition | Used In |
    |------|------------|---------|
    | [detected] | [definition] | [location] |
    
    ---
    
    *Generated from: [PRD path], [TRD path], [Feature Map path]*
    *lzr1 Standards Version: [version from WebFetch]*
    *Generated: [ISO timestamp]*
```

#### Check for Missing Information

If any section is empty or incomplete, ask supplementary questions:

| Missing Section | Supplementary Question |
|-----------------|------------------------|
| Tech Stack (Not in lzr1) | "Any technology not covered by lzr1 Standards (message broker, cache, etc.)?" |
| External Integrations | "Any third-party APIs or external services?" |
| Domain Terminology | "What are the main entities/classes in this codebase?" |
| Non-Standard Directories | "Any directories that don't follow standard API structure (workers, consumers)?" |

**Note:** Do not ask about architecture, error handling, logging, testing - lzr1 Standards covers these.

#### After Generation

Present to user for review, then proceed to Step 1.

### Step 0.3.2: HARD BLOCK - No PM Documents (New Projects Only)

#### When User Has No PM Documents

```text
┌─────────────────────────────────────────────────────────────────┐
│ ⛔ CANNOT PROCEED - PM DOCUMENTS REQUIRED                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Development cannot start without PM documents.                  │
│                                                                 │
│ You MUST create PRD, TRD, and/or Feature Map documents first    │
│ using PM team skills:                                           │
│                                                                 │
│   /lzr1:pre-dev-full     → For features ≥2 days (9 gates)           │
│   /lzr1:pre-dev-feature  → For features <2 days (4 gates)           │
│                                                                 │
│ These commands will guide you through creating:                 │
│   • PRD (Product Requirements Document)                         │
│   • TRD (Technical Requirements Document)                       │
│   • Feature Map (technology choices, feature relationships)     │
│                                                                 │
│ After completing pre-dev workflow, run /lzr1:dev-cycle again.        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Action

STOP EXECUTION. Do not proceed to Step 1.

### Step 0 Anti-Rationalization

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Skip PM docs, I'll add them later" | Later = never. No PM docs = no project context = agents guessing. | **Run /lzr1:pre-dev-full or /lzr1:pre-dev-feature NOW** |
| "Project is simple, doesn't need PM docs" | Simple projects still need domain context defined upfront. | **Create PM documents first** |
| "I know what I want to build" | Your knowledge ≠ documented knowledge agents can use. | **Document in PRD/TRD/Feature Map** |
| "PM workflow takes too long" | PM workflow takes 30-60 min. Rework from unclear requirements takes days. | **Invest time upfront** |
| "Just let me start coding" | Coding without requirements = building the wrong thing. | **Requirements first, code second** |
| "It's legacy but I don't want to answer questions" | Legacy analysis takes ~5 min. Without it, agents have zero context. | **Answer the 4 questions** |
| "Legacy project is too complex to explain" | Start with high-level answers. PROJECT_RULES.md can be refined later. | **Provide what you know NOW** |

### Pressure Resistance

| User Says | Your Response |
|-----------|---------------|
| "Just skip this, I'll create PM docs later" | "PM documents are REQUIRED for new projects. Without them, agents cannot understand your project's domain context or technical requirements. Run `/lzr1:pre-dev-full` or `/lzr1:pre-dev-feature` first." |
| "I don't need formal documents" | "PM documents are the source of truth for PROJECT_RULES.md. Development cannot start without documented requirements." |
| "This is just a quick prototype" | "Even prototypes need clear requirements. `/lzr1:pre-dev-feature` takes ~30 minutes and prevents hours of rework." |
| "I already explained what I want verbally" | "Verbal explanations cannot be used by agents. Requirements MUST be documented in PRD/TRD/Feature Map files." |
| "It's a legacy project but skip the questions" | "The legacy analysis (lzr1:codebase-explorer + 3 questions) is the only way I can understand your project. It takes ~5 minutes and enables me to help you effectively." |
| "I'll fill in PROJECT_RULES.md myself" | "That works! Create `docs/PROJECT_RULES.md` with: Tech Stack (not in lzr1), External Integrations, Domain Terminology. Do not duplicate lzr1 Standards content. Then run `/lzr1:dev-cycle` again." |

---
