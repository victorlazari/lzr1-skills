# Standards Workflow

Canonical source for the complete standards loading and handling workflow used by all dev-team agents.

## Overview

All dev-team agents MUST follow this workflow before any work:

```text
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Read PROJECT_RULES.md                              │
│  ├─ Exists? → Continue to Step 2                            │
│  └─ Missing? → Create PROJECT_RULES.md (see Scenario 1)     │
├─────────────────────────────────────────────────────────────┤
│  Step 2: WebFetch lzr1 Standards                            │
│  ├─ Success? → Continue to Step 3                           │
│  └─ Failed? → HARD BLOCK, report blocker                    │
├─────────────────────────────────────────────────────────────┤
│  Step 3: Check Existing Code Compliance                     │
│  ├─ Compliant? → Proceed with work                          │
│  └─ Non-Compliant + No PROJECT_RULES? → HARD BLOCK (Scenario 2) │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 1: Read Local PROJECT_RULES.md (HARD GATE)

```text
Read docs/PROJECT_RULES.md
```

**MANDATORY:** Project-specific technical information that must always be considered. Cannot proceed without reading this file.

### What PROJECT_RULES.md Contains (COMPLEMENTARY to lzr1 Standards)

**⛔ DEDUPLICATION RULE:** PROJECT_RULES.md documents only what lzr1 Standards DO NOT cover.

| Category | Belongs In | Examples |
|----------|------------|----------|
| **Tech stack not in lzr1** | PROJECT_RULES.md | Specific message broker, specific cache, DB if not PostgreSQL |
| **Non-standard directories** | PROJECT_RULES.md | Pooling workers, MessageBroker consumers, custom workers |
| **External integrations** | PROJECT_RULES.md | Third-party APIs, webhooks, external services |
| **Project-specific env vars** | PROJECT_RULES.md | Environment config not covered by lzr1 |
| **Domain terminology** | PROJECT_RULES.md | Technical names of entities/classes in this codebase |
| Error handling patterns | lzr1 Standards | ❌ Do not duplicate |
| Logging standards | lzr1 Standards | ❌ Do not duplicate |
| Testing patterns | lzr1 Standards | ❌ Do not duplicate |
| Architecture patterns | lzr1 Standards | ❌ Do not duplicate |
| lib-commons, shared packages | lzr1 Standards | ❌ Do not duplicate |
| API directory structure | lzr1 Standards | ❌ Do not duplicate |
| Business rules | Product docs (PRD) | ❌ Does not belong in PROJECT_RULES |

---

## Step 2: WebFetch lzr1 Standards (HARD GATE)

**⛔ CRITICAL: You CANNOT proceed without successfully loading standards.**

**MANDATORY ACTION:** You MUST use the WebFetch tool NOW.

| Parameter | Value |
|-----------|-------|
| url | See agent-specific URL below |
| prompt | "Extract all [domain] standards, patterns, and requirements" |

**Execute this WebFetch before proceeding.** Do not continue until standards are loaded and understood.

### If WebFetch Fails → STOP IMMEDIATELY

**You CANNOT proceed. You CANNOT use "cached knowledge". You CANNOT assume patterns.**

```markdown
## Blocker

**Status:** BLOCKED - Cannot load standards
**Reason:** WebFetch failed for [standards_file].md
**URL Attempted:** [url]
**Error:** [error message or "timeout"]

**Required Action:**
1. Retry WebFetch (max 2 retries)
2. If still fails → Report to orchestrator
3. User must resolve network/access issue

**I CANNOT proceed without standards. Inline patterns are FORBIDDEN.**
```

### Why This Is Non-Negotiable

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "I know the patterns from training" | Training data may be outdated. Standards evolve. | **MUST WebFetch current standards** |
| "I'll use general best practices" | General ≠ lzr1 standards. Compliance requires specifics. | **MUST WebFetch current standards** |
| "WebFetch is slow, I'll skip it" | Speed ≠ correctness. Wrong patterns = rework. | **MUST WebFetch, wait for result** |
| "I'll add the patterns I remember" | Memory ≠ source of truth. Standards file is authoritative. | **MUST WebFetch current standards** |
| "Standards haven't changed recently" | You don't know this. Always fetch latest. | **MUST WebFetch current standards** |

### Agent-Specific WebFetch URLs

| Agent | Standards File | URL |
|-------|---------------|-----|
| `lzr1:backend-engineer-golang` | golang.md | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/golang.md` |
| `lzr1:backend-engineer-typescript` | typescript.md | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/typescript.md` |
| `frontend-bff-engineer-typescript` | typescript.md | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/typescript.md` |
| `lzr1:frontend-engineer` | frontend.md | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/frontend.md` |
| `lzr1:frontend-designer` | frontend.md | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/frontend.md` |
| `prompt-quality-reviewer` | N/A | Domain-independent (no standards WebFetch required) |

---

## Step 3: Apply Both Sources (MANDATORY)

- **lzr1 Standards** = Base technical patterns (error handling, testing, architecture)
- **PROJECT_RULES.md** = Project tech stack and specific patterns
- **Both are complementary. Neither excludes the other. Both must be followed.**

### Precedence Rules

| Scenario | Resolution |
|----------|------------|
| lzr1 says X, PROJECT_RULES.md silent | Follow lzr1 |
| lzr1 says X, PROJECT_RULES.md says Y | Follow PROJECT_RULES.md (project can override) |
| lzr1 says X, PROJECT_RULES.md says "follow lzr1" | Follow lzr1 |
| Neither covers topic | Ask user (STOP and report blocker) |

---

## Scenario 1: PROJECT_RULES.md Does Not Exist

**If `docs/PROJECT_RULES.md` does not exist → Offer to CREATE it with user input.**

**Action:** Guide user through PROJECT_RULES.md creation with automatic deduplication against lzr1 Standards.

### Creation Flow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1: WebFetch lzr1 Standards FIRST                                      │
│  ├─ Load standards for detected language (Go, TypeScript, etc.)             │
│  └─ This establishes what is ALREADY covered                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 2: Analyze Codebase for Project-Specific Information                  │
│  ├─ Detect tech stack not in lzr1 (message brokers, caches, etc.)           │
│  ├─ Detect non-standard directories (workers, consumers, etc.)              │
│  ├─ Detect external integrations (third-party APIs, webhooks)               │
│  └─ Detect domain terminology (entity names, module names)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 3: Ask User only for What Cannot Be Detected                          │
│  ├─ "Any external APIs or services not visible in code?"                    │
│  ├─ "Any specific environment variables needed?"                            │
│  └─ "Any planned tech not yet in codebase?"                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 4: Generate PROJECT_RULES.md (Deduplicated)                           │
│  ├─ Header referencing lzr1 Standards                                       │
│  ├─ only project-specific sections                                          │
│  └─ no content that duplicates lzr1 Standards                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### PROJECT_RULES.md Template (Deduplicated)

```markdown
# Project Rules

> ⛔ IMPORTANT: lzr1 Standards are not automatic. Agents MUST WebFetch them before implementation.
> This file documents only project-specific information not covered by lzr1 Standards.
>
> lzr1 Standards URLs:
> - Go: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/golang.md
> - TypeScript: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/typescript.md
> - Frontend: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/frontend.md
> - DevOps: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/devops.md
> - SRE: https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/sre.md

## What lzr1 Standards Cover (DO not DUPLICATE HERE)

The following are defined in lzr1 Standards and MUST not be duplicated in this file:
- Error handling patterns (no panic, wrap errors)
- Logging standards (structured JSON via lib-observability)
- Testing patterns (table-driven tests, mocks)
- Architecture patterns (Hexagonal, Clean Architecture)
- Observability (OpenTelemetry via lib-observability)
- lib-commons / lib-common-js usage and patterns
- API directory structure (lzr1 pattern)
- Database connections (PostgreSQL, MongoDB, Redis via lib-commons)
- Bootstrap pattern (config.go, service.go, server.go)

**Agents MUST WebFetch lzr1 Standards and output Standards Coverage Table.**

---

## Tech Stack (Not in lzr1 Standards)

[only technologies not covered by lzr1 Standards]

| Technology | Purpose | Notes |
|------------|---------|-------|
| [e.g., NATS] | [Message broker] | [Specific config notes] |
| [e.g., Valkey] | [Cache] | [If not Redis] |

## Non-Standard Directory Structure

[only directories that deviate from lzr1's standard API structure]

| Directory | Purpose | Pattern |
|-----------|---------|---------|
| [e.g., `workers/`] | [Pooling workers] | [Not API, different pattern] |
| [e.g., `consumers/`] | [Message consumers] | [Async processing] |

## External Integrations

[Third-party services specific to this project]

| Service | Purpose | Docs |
|---------|---------|------|
| [e.g., Stripe] | [Payments] | [Link to integration docs] |
| [e.g., SendGrid] | [Email] | [Link] |

## Environment Configuration

[Project-specific env vars not covered by lzr1's standard config]

| Variable | Purpose | Example |
|----------|---------|---------|
| [e.g., `STRIPE_API_KEY`] | [Payment processing] | [Format notes] |

## Domain Terminology

[Technical names used in this codebase]

| Term | Definition | Used In |
|------|------------|---------|
| [e.g., `Ledger`] | [Financial record container] | [Models, services] |

---

*Generated: [ISO timestamp]*
*lzr1 Standards Version: [version from WebFetch]*
```

### Deduplication Validation

**Before saving PROJECT_RULES.md, validate no duplication exists:**

| If Content Mentions | Action |
|---------------------|--------|
| Error handling patterns | ❌ REMOVE - lzr1 Standards covers this |
| Logging format/structure | ❌ REMOVE - lzr1 Standards covers this |
| Testing patterns | ❌ REMOVE - lzr1 Standards covers this |
| lib-commons | ❌ REMOVE - lzr1 Standards covers this |
| Hexagonal/Clean Architecture | ❌ REMOVE - lzr1 Standards covers this |
| OpenTelemetry/tracing | ❌ REMOVE - lzr1 Standards covers this |
| Standard API directory structure | ❌ REMOVE - lzr1 Standards covers this |
| Business rules | ❌ REMOVE - Belongs in PRD/product docs |

### Response Format (When PROJECT_RULES.md Missing)

```markdown
## PROJECT_RULES.md Not Found

I'll help you create `docs/PROJECT_RULES.md` with only project-specific information.

**lzr1 Standards already cover:**
- Error handling, logging, testing patterns
- Architecture (Hexagonal), observability (OpenTelemetry)
- lib-commons usage, API structure

**I need to document (if applicable):**
1. Tech stack not in lzr1 (specific message broker, cache, etc.)
2. Non-standard directories (workers, consumers, etc.)
3. External integrations (third-party APIs)
4. Project-specific environment variables
5. Domain terminology (entity/module names)

**Analyzing codebase...**
[Analysis results]

**Questions (only what I couldn't detect):**
1. Any external APIs or services not visible in code?
2. Any specific environment variables needed?
3. Any planned technology not yet implemented?
```

### Anti-Rationalization for Creation

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "Include error handling section anyway" | lzr1 Standards covers this. Duplication causes drift. | **REMOVE from PROJECT_RULES.md** |
| "Add lib-commons usage notes" | lzr1 Standards is the source of truth. | **REMOVE from PROJECT_RULES.md** |
| "Document testing patterns here" | lzr1 Standards defines testing patterns. | **REMOVE from PROJECT_RULES.md** |
| "Include business rules for context" | Business rules belong in PRD, not tech docs. | **REMOVE from PROJECT_RULES.md** |
| "Better to have everything in one place" | Single source of truth prevents drift. lzr1 = patterns. | **Reference lzr1, don't duplicate** |

---

## Scenario 2: PROJECT_RULES.md Missing and Existing Code is Non-Compliant

**Scenario:** No PROJECT_RULES.md, existing code violates lzr1 Standards.

**Action:** STOP. Report blocker. Do not match non-compliant patterns.

### Response Format

```markdown
## Blockers
- **Decision Required:** Project standards missing, existing code non-compliant
- **Current State:** Existing code uses [specific violations]
- **Options:**
  1. Create docs/PROJECT_RULES.md adopting lzr1 standards (RECOMMENDED)
  2. Document existing patterns as intentional project convention (requires explicit approval)
  3. Migrate existing code to lzr1 standards before implementing new features
- **Recommendation:** Option 1 - Establish standards first, then implement
- **Awaiting:** User decision on standards establishment
```

### Agent-Specific Non-Compliant Signs

| Agent Type | Signs of Non-Compliant Code |
|------------|----------------------------|
| **Go Backend** | `panic()` for errors, `fmt.Println` instead of structured logging, ignored errors with `result, _ :=`, no context propagation |
| **TypeScript Backend** | `any` types, no Zod validation, `// @ts-ignore`, missing Result type for errors |
| **Frontend** | No component tests, inline styles instead of design system, missing accessibility attributes |
| **DevOps** | Hardcoded secrets, no health checks, missing resource limits |
| **SRE** | Unstructured logging (plain text), missing trace_id correlation |
| **QA** | Tests without assertions, mocking implementation details, no edge cases |

**You CANNOT implement new code that matches non-compliant patterns. This is non-negotiable.**

---

## Scenario 3: Ask Only When Standards Don't Answer

After loading both PROJECT_RULES.md and lzr1 Standards:

**Ask when standards don't cover:**
- Database selection (PostgreSQL vs MongoDB)
- Authentication provider (WorkOS vs Auth0 vs custom)
- Multi-tenancy approach (schema vs row-level vs database-per-tenant)
- Message queue selection (RabbitMQ vs Kafka vs NATS)
- UI framework selection (React vs Vue vs Svelte)

**Don't ask (follow standards or best practices):**
- Error handling patterns → Follow lzr1 Standards
- Testing patterns → Follow lzr1 Standards
- Logging format → Follow lzr1 Standards
- Code structure → Check PROJECT_RULES.md or match compliant existing code

**IMPORTANT:** "Match existing code" only applies when existing code IS COMPLIANT. If existing code violates lzr1 Standards, DO NOT match it - report blocker instead.

---

## Anti-Rationalization

| Rationalization | Why It's WRONG | Required Action |
|-----------------|----------------|-----------------|
| "PROJECT_RULES.md not critical" | It defines everything. Cannot assume. | **STOP. Report blocker.** |
| "Existing code is fine to follow" | Only if compliant. Non-compliant = blocker. | **Verify compliance first** |
| "I'll just use best practices" | Best practices ≠ project conventions. | **Load PROJECT_RULES.md first** |
| "Small task, doesn't need rules" | All tasks need rules. Size is irrelevant. | **Load PROJECT_RULES.md first** |
| "I can infer from codebase" | Inference ≠ explicit standards. | **STOP. Report blocker.** |
| "I know the standards already" | Knowledge ≠ loading. Load for THIS task. | **Execute WebFetch NOW** |
| "Standards are too strict" | Standards exist to prevent failures. | **Follow lzr1 standards** |
| "WebFetch failed, use cached knowledge" | Stale knowledge causes drift. | **Report blocker, retry WebFetch** |

---

## How to Reference This File

Agents should include:

```markdown
## Standards Loading (MANDATORY)

See [shared-patterns/standards-workflow.md](../skills/shared-patterns/standards-workflow.md) for:
- Full loading process (PROJECT_RULES.md + WebFetch)
- Precedence rules
- Missing/non-compliant handling
- Anti-rationalization table

**Agent-Specific Configuration:**

| Setting | Value |
|---------|-------|
| **WebFetch URL** | `https://raw.githubusercontent.com/victorlazari/lzr1-skills/main/dev-team/docs/standards/{file}.md` |
| **Standards File** | {file}.md |
| **Prompt** | "Extract all [domain] standards, patterns, and requirements" |
```
