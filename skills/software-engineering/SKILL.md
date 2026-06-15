---
name: software-engineering
description: Comprehensive software engineering skill covering backend, frontend, fullstack, mobile, API design, systems architecture, database engineering, performance engineering, and language-specific expertise (Go, Rust, blockchain, embedded systems, game development). Use when writing production code, designing systems, building APIs, optimizing performance, or making architectural decisions.
---

# Software Engineering

Expert-level software engineering covering the full stack: backend services, frontend applications, mobile development, API design, systems architecture, database engineering, performance optimization, and specialized domains including blockchain, embedded systems, and game development.

## When to Use

- Writing or reviewing production code in any language
- Designing system architecture or making technology decisions
- Building APIs (REST, GraphQL, gRPC)
- Database schema design, query optimization, migrations
- Frontend development (React, Next.js, Vue, Angular)
- Mobile development (React Native, Flutter, Swift, Kotlin)
- Performance engineering and optimization
- Systems programming (Go, Rust, C/C++)
- Blockchain/smart contract development
- Embedded systems and firmware

## Workflow

1. **Understand requirements** — Clarify functional and non-functional requirements
2. **Select reference** — Choose the appropriate domain reference:
   - Backend services and APIs → `references/backend-engineering.md`
   - Frontend and UI development → `references/frontend-engineering.md`
   - System design and architecture → `references/systems-architecture.md`
   - Database engineering → `references/database-engineering.md`
   - Performance optimization → `references/performance-engineering.md`
   - Language-specific guidance → `references/language-guides.md`
3. **Design the solution** — Apply architectural patterns and best practices
4. **Implement** — Write clean, tested, production-ready code
5. **Review and optimize** — Apply code review standards and performance analysis
6. **Document** — Record decisions, trade-offs, and usage instructions

## Core Principles (All Engineering Work)

- Write code for humans first, computers second — clarity over cleverness
- Design for change: loose coupling, high cohesion, clear interfaces
- Test at the right level: unit tests for logic, integration tests for contracts, e2e for critical paths
- Fail fast, fail loudly: validate inputs early, use typed errors, never swallow exceptions
- Automate everything repeatable: builds, tests, deployments, formatting
- Measure before optimizing: profile first, optimize the bottleneck, verify improvement
- Security by default: validate all inputs, use parameterized queries, follow least privilege
- Document the "why" not the "what": code shows what, comments explain why

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Backend Engineer | Services, APIs, data processing, distributed systems | `references/backend-engineering.md` |
| Frontend Engineer | UI/UX implementation, state management, accessibility | `references/frontend-engineering.md` |
| Fullstack Engineer | End-to-end feature development | Both backend + frontend |
| Systems Architect | Large-scale design, trade-offs, technology selection | `references/systems-architecture.md` |
| Database Engineer | Schema design, query optimization, migrations | `references/database-engineering.md` |
| API Engineer | API design, versioning, documentation | `references/backend-engineering.md` |
| Performance Engineer | Profiling, optimization, load testing | `references/performance-engineering.md` |
| Mobile Engineer | iOS, Android, cross-platform development | `references/frontend-engineering.md` |
| Go Engineer | Go services, concurrency, stdlib patterns | `references/language-guides.md` |
| Rust Engineer | Systems programming, safety, performance | `references/language-guides.md` |
| Blockchain Engineer | Smart contracts, DeFi, consensus | `references/language-guides.md` |
| Embedded Systems Engineer | Firmware, RTOS, hardware interfaces | `references/language-guides.md` |
| Game Developer | Game engines, real-time systems, ECS | `references/language-guides.md` |

## Key References

- **Backend engineering**: See `references/backend-engineering.md` for service design, API patterns, distributed systems, and microservices.
- **Frontend engineering**: See `references/frontend-engineering.md` for React, Next.js, state management, accessibility, and mobile.
- **Systems architecture**: See `references/systems-architecture.md` for large-scale design, patterns, and trade-offs.
- **Database engineering**: See `references/database-engineering.md` for schema design, optimization, and migrations.
- **Performance engineering**: See `references/performance-engineering.md` for profiling, optimization, and load testing.
- **Language guides**: See `references/language-guides.md` for Go, Rust, blockchain, embedded, and game development.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.
