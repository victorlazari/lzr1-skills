---
name: go
description: Advanced Go Specialist for troubleshooting, scaling, security, and complex patterns in Go applications.
---

# Go Specialist

## When to Use

Use this skill when you need to:
- Troubleshoot complex Go runtime issues, including goroutine leaks, deadlocks, and memory leaks.
- Scale Go applications using advanced concurrency patterns (e.g., fan-out/fan-in, worker pools).
- Perform security audits on Go codebases, including race condition detection and cryptographic practices.
- Optimize Go application performance using `pprof`, escape analysis, and garbage collection tuning (`GOGC`).
- Implement enterprise patterns such as Clean Architecture, Dependency Injection, and gRPC integration.
- Manage Go modules, workspaces, and complex configuration schemas.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Go services to audit | Security Auditor | Parallel security review of each service's codebase |
| Multiple packages to profile | Performance Profiler | Parallel execution of `pprof` and escape analysis |
| Multiple modules to update | Dependency Manager | Parallel updating and tidying of `go.mod` files |
| Bulk goroutine leak investigation | Diagnostics Agent | Parallel analysis of goroutine dumps across instances |

### Spawning Rules
- Spawn when 3+ independent items (services, packages, modules) need the same operation.
- Each sub-agent receives: context, specific target (e.g., service path), success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Assessment & Context Gathering**:
   - Identify the specific Go domain (e.g., performance, security, architecture).
   - Review existing `go.mod`, `go.work`, and configuration files.
   - Analyze runtime metrics or error logs if troubleshooting.

2. **Diagnostics & Profiling** (If applicable):
   - Run `go test -race` to detect race conditions.
   - Use `pprof` to capture CPU, memory, and goroutine profiles.
   - Analyze escape analysis output (`go build -gcflags="-m"`).

3. **Implementation & Remediation**:
   - Apply appropriate concurrency patterns (e.g., channels, `sync.Pool`).
   - Fix memory/goroutine leaks by ensuring proper channel closure and context cancellation.
   - Implement security best practices (e.g., input validation, secure TLS configuration).
   - Refactor code to adhere to Clean Architecture or Dependency Injection principles.

4. **Validation & Testing**:
   - Run unit and benchmark tests (`go test -bench=.`).
   - Verify that performance metrics have improved or security vulnerabilities are resolved.
   - Ensure the application builds successfully across target OS/Arch (`GOOS`/`GOARCH`).

## Core Principles

- **Simplicity and Readability**: Favor clear, idiomatic Go code over clever but complex solutions.
- **Concurrency Safety**: Always synchronize access to shared memory using channels or `sync` primitives. Avoid race conditions.
- **Resource Management**: Prevent goroutine leaks by using `context.Context` for cancellation and timeouts.
- **Performance Awareness**: Understand the cost of heap allocations and use escape analysis to keep variables on the stack when possible.
- **Robust Error Handling**: Treat errors as values. Use error wrapping (`fmt.Errorf("... %w", err)`) to provide context.

## Key References

- [Complete Reference](./references/complete-reference.md): Exhaustive guide on Go architecture, troubleshooting, security, and enterprise patterns.
- [Reading List](./references/reading-list.md): Curated list of books and articles for advanced Go developers.

---

## Adversarial Verification Panel

For each significant security vulnerabilities, performance bottlenecks, and diagnostic findings produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong security vulnerabilities, performance bottlenecks, and diagnostic findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Security Auditor, Performance Profiler, Dependency Manager, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Auditor recommending disabling a feature for security while Performance Profiler recommends enabling it for throughput)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
