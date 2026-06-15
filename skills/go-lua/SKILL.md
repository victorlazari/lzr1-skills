---
name: go-lua
description: Advanced Go and Lua topics including performance profiling, memory management, CGO, Redis Lua patterns, and handling huge datasets.
---

# Go and Lua Specialist Skill

## When to Use

Use this skill when you need to:
- Diagnose and resolve performance bottlenecks in Go applications using `pprof`.
- Tune Go garbage collection (`GOGC`, `GOMEMLIMIT`) and manage memory footprints.
- Write, debug, and optimize advanced Redis Lua scripts.
- Bridge Go with C using CGO for performance-critical operations.
- Handle huge datasets in-memory efficiently.
- Perform security audits on Go dependencies and Lua scripts.
- Manage database migrations using `golang-migrate` and recover from dirty states.
- Troubleshoot worst-case scenarios like goroutine leaks, deadlocks, and OOM kills.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Go services to profile | Profiling Agent | Parallel CPU/Memory profiling of each service |
| Multiple Redis Lua scripts to audit | Lua Auditor | Parallel security and performance review of scripts |
| Multiple Go dependencies to scan | Dependency Scanner | Parallel vulnerability scanning using `govulncheck` |
| Bulk database migrations to verify | Migration Validator | Parallel validation of migration scripts and rollback plans |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Information Gathering**: Identify the specific issue (e.g., high CPU, memory leak, Redis blocking).
2. **Profiling and Diagnostics**: Use `go tool pprof` to capture CPU, heap, goroutine, or block profiles. For Redis, use `SLOWLOG` to identify problematic Lua scripts.
3. **Analysis**: Analyze the profiles or logs to pinpoint the root cause (e.g., runaway loops, excessive allocations, blocking operations).
4. **Tuning and Optimization**: Adjust Go runtime parameters (`GOGC`, `GOMAXPROCS`) or rewrite Lua scripts for better performance (e.g., using `SCAN` instead of `KEYS`).
5. **Security Audit**: Run `govulncheck` for Go dependencies and ensure Lua scripts use parameterized execution (`KEYS` and `ARGV`) to prevent injection.
6. **Verification**: Test the optimizations or fixes in a staging environment under load before deploying to production.

## Core Principles

- **Measure Before Optimizing**: Always use profiling tools (`pprof`, `trace`) to identify actual bottlenecks rather than guessing.
- **Manage Memory Proactively**: Understand Go's garbage collector and tune it appropriately. Avoid large object allocations and use object pooling when necessary.
- **Keep Lua Scripts Short and Atomic**: Redis is single-threaded; long-running Lua scripts block all other operations. Use iterative commands (`SSCAN`, `HSCAN`) for large datasets.
- **Secure by Default**: Never trust user input. Use parameterized execution in Lua and regularly scan Go dependencies for vulnerabilities.
- **Prepare for the Worst**: Have runbooks ready for scenarios like goroutine leaks, dirty database migrations, and Redis overload.

## Key References

- [Go Performance Profiling with pprof](references/complete-reference.md#1-go-performance-profiling-with-pprof)
- [Go Memory Management and Garbage Collection Tuning](references/complete-reference.md#2-go-memory-management-and-garbage-collection-tuning)
- [Advanced Redis Lua Patterns](references/complete-reference.md#3-advanced-redis-lua-patterns)
- [CGO: Bridging Go with C](references/complete-reference.md#4-cgo-bridging-go-with-c-for-performance-critical-operations)
- [Handling Huge Datasets In-Memory](references/complete-reference.md#5-handling-huge-datasets-in-memory)
- [Comprehensive CLI Reference](references/complete-reference.md#comprehensive-cli-reference-go-toolchain-golang-migrate-and-lua-interpreters)
- [Security Audit Procedures](references/complete-reference.md#security-audit-procedures-for-go-and-lua)
