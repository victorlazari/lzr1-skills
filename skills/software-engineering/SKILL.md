---
name: software-engineering
description: Comprehensive software engineering skill covering backend, frontend, fullstack, mobile, API design, systems architecture, database engineering, performance engineering, security, and language-specific expertise. Use when writing production code, designing systems, building APIs, optimizing performance, or making architectural decisions. Triggers on tasks involving software development, system design, or code review.
---

# Software Engineering

Expert-level software engineering covering the full stack: backend services, frontend applications, mobile development, API design, systems architecture, database engineering, performance optimization, security, and specialized domains including blockchain, embedded systems, and game development.

## Scope and Triggers

- **Handles**: Writing or reviewing production code, designing system architecture, building APIs, database schema design, frontend/mobile development, performance optimization, and security engineering.
- **Activates**: When tasks involve software development, system design, code review, or architectural decisions.
- **Non-goals**: Not for general IT support, hardware troubleshooting, or non-technical project management.
- **Escalation boundaries**: Route to `security-review` for deep security auditing, `trivy-scanner` for container/dependency vulnerability scanning, `legendary-readme` for project documentation, and `coderabbit-reviewer` for automated code review.

## Preconditions

1. Detect the target domains based on task signals (e.g., backend, frontend, database, security).
2. Identify the environment, language versions, and permissions required.
3. Clarify functional and non-functional requirements before acting.

## Source Freshness

Volatile facts (e.g., supported versions, specific API endpoints) must be verified against official current documentation or the bundled verified references. Each reference includes a `Verified against upstream` date.

## Workflow

1. **Understand requirements** — Clarify functional and non-functional requirements.
2. **Detect domains** — Scan the task for signals indicating which domains apply.
3. **Spawn specialists** — If multiple domains are detected, spawn relevant domain specialists concurrently (up to 6).
4. **Apply guidance** — Each specialist applies domain-specific guidance from its reference file.
5. **Synthesize** — Run the Stack Synthesizer to identify contradictions, gaps, and dependencies.
6. **Produce recommendation** — Generate a unified recommendation with explicit trade-off annotations.
7. **Stop condition** — Stop when a complete, consistent implementation plan is generated.

## Safety

- **Read-only discovery**: Always perform read-only discovery (e.g., reading code, checking configurations) before making any mutations.
- **Confirmation required**: Require user confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.

## Validation

- Define syntax checks for generated code (e.g., `bash -n` for shell scripts, compilation for compiled languages).
- Run a dry run on a full-stack task to confirm end-to-end functionality.
- Capture evidence of successful execution (e.g., test results, logs).

## Failure Handling

- If an action fails, diagnose the error using logs and error messages.
- Choose alternative approaches or tools; do not repeat the same failed action unchanged.
- Roll back any partial changes if a multi-step process fails.

## Output Contract

- **Structure**: A unified implementation plan or code artifacts.
- **Evidence**: Test results, validation checks, or logs demonstrating success.
- **Actionable next steps**: Clear instructions for deployment, further testing, or maintenance.

## Resources

- **Backend engineering**: `references/backend-engineering.md`
- **Frontend engineering**: `references/frontend-engineering.md`
- **Systems architecture**: `references/systems-architecture.md`
- **Database engineering**: `references/database-engineering.md`
- **Performance engineering**: `references/performance-engineering.md`
- **Security engineering**: `references/security-engineering.md`
- **Language guides**: `references/language-guides.md`

## Orchestration (Multi-Specialist Protocol)

When multiple domains are detected, spawn all relevant specialists simultaneously (up to 6).

### Domain Detection Table

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `backend`, `API`, `service`, `REST`, `gRPC`, `microservice` | **Backend Engineering** | Backend Specialist | `references/backend-engineering.md` |
| `frontend`, `UI`, `React`, `Next.js`, `Vue`, `Angular` | **Frontend Engineering** | Frontend Specialist | `references/frontend-engineering.md` |
| `architecture`, `system design`, `distributed`, `scalability` | **Systems Architecture** | Architecture Specialist | `references/systems-architecture.md` |
| `database`, `SQL`, `schema`, `migration`, `query`, `index` | **Database Engineering** | DB Specialist | `references/database-engineering.md` |
| `performance`, `profiling`, `latency`, `throughput` | **Performance Engineering** | Performance Specialist | `references/performance-engineering.md` |
| `security`, `vulnerability`, `auth`, `encryption` | **Security Engineering** | Security Specialist | `references/security-engineering.md` |
| `Go`, `Rust`, `blockchain`, `embedded`, `game engine` | **Language-Specific Guidance** | Language Specialist | `references/language-guides.md` |

### Cross-Domain Synthesizer

After all specialists complete, run one **Stack Synthesizer** with all specialist outputs that:
1. Identifies contradictions between specialist recommendations.
2. Identifies gaps (requirements addressed by no specialist).
3. Identifies dependencies between domains.
4. Produces a unified recommendation with explicit trade-off annotations.
