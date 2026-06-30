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

---

## Adversarial Verification Panel

For each significant performance bottlenecks and security vulnerabilities produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong performance bottlenecks and security vulnerabilities from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Profiling Agent, Lua Auditor, Dependency Scanner, Migration Validator) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Profiling Agent recommends increasing GOGC to reduce GC overhead while Migration Validator recommends reducing memory usage before running a large migration)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified unified optimization and security report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
