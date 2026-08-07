---
name: go
description: Advanced Go Specialist for troubleshooting, scaling, security auditing (including govulncheck), and complex patterns in Go applications. Triggers on Go performance issues, memory/goroutine leaks, security reviews, and codebase modernization.
---

# Go Specialist

## Scope and Triggers

Use this skill when you need to:
- Troubleshoot complex Go runtime issues, including goroutine leaks, deadlocks, and memory leaks.
- Scale Go applications using advanced concurrency patterns (e.g., fan-out/fan-in, worker pools).
- Perform security audits on Go codebases, including race condition detection, cryptographic practices, and vulnerability scanning with `govulncheck`.
- Optimize Go application performance using `pprof`, escape analysis, and garbage collection tuning (including Go 1.26 Green Tea GC).
- Modernize Go codebases using the revamped `go fix` command.
- Implement enterprise patterns such as Clean Architecture, Dependency Injection, and gRPC integration.
- Manage Go modules, workspaces, and complex configuration schemas.

**Escalation Boundaries:**
- For comprehensive security audits across multiple languages or deep vulnerability analysis beyond Go-specific tools, route to `security-review`.
- For scanning container images or dependencies for known vulnerabilities, route to `trivy-scanner`.

## Preconditions

Before acting, verify:
- The target is a Go project (presence of `go.mod` or `.go` files).
- The installed Go version (`go version`) to ensure compatibility with features like Go 1.26 Green Tea GC or the experimental goroutine leak profile.
- Permissions to run diagnostic tools (`go test`, `pprof`, `govulncheck`).
- User intent regarding destructive actions (e.g., applying `go fix` or updating dependencies).

## Source Freshness

Volatile facts, such as supported versions, specific command flags, and security best practices, must be verified against official documentation.
- Check [Go Release Notes](https://go.dev/doc/devel/release) for the latest features and deprecations.
- Consult the [OWASP Go Secure Coding Practices Guide](https://owasp.org/www-project-go-secure-coding-practices-guide/) for current security recommendations.
- See `references/complete-reference.md` for verified facts (Verified against upstream: 2026-08-07).

## Workflow

1. **Assessment & Context Gathering**:
   - Identify the specific Go domain (e.g., performance, security, architecture).
   - Review existing `go.mod`, `go.work`, and configuration files.
   - Analyze runtime metrics or error logs if troubleshooting.

2. **Diagnostics & Profiling**:
   - Run `go test -race` to detect race conditions.
   - Run `govulncheck ./...` to identify known vulnerabilities in dependencies and code.
   - Use `pprof` to capture CPU, memory, and goroutine profiles (including the Go 1.26 experimental goroutine leak profile).
   - Analyze escape analysis output (`go build -gcflags="-m"`).

3. **Implementation & Remediation**:
   - Apply appropriate concurrency patterns (e.g., channels, `sync.Pool`).
   - Fix memory/goroutine leaks by ensuring proper channel closure and context cancellation.
   - Implement security best practices (e.g., input validation, secure TLS configuration).
   - Use `go fix` to modernize the codebase and apply automated refactoring.
   - Refactor code to adhere to Clean Architecture or Dependency Injection principles.

4. **Validation & Testing**:
   - Run unit and benchmark tests (`go test -bench=.`).
   - Verify that performance metrics have improved or security vulnerabilities are resolved.
   - Ensure the application builds successfully across target OS/Arch (`GOOS`/`GOARCH`).
   - **Stop Condition**: All identified issues are resolved, tests pass, and no new vulnerabilities are reported by `govulncheck`.

## Safety

- **Read-only Discovery**: Always perform diagnostics (`go test -race`, `govulncheck`, `pprof`) before making any code changes.
- **Confirmation Required**: Require explicit user confirmation before applying `go fix`, updating dependencies (`go get -u`), or making destructive/production-impacting changes.
- **Dry Runs**: Use dry runs or preview modes where applicable (e.g., reviewing `go fix` changes before committing).

## Validation

- **Syntax Checks**: Ensure all Go code compiles (`go build ./...`).
- **Tests**: Run `go test ./...` to verify functionality.
- **Evidence Capture**: Save `pprof` profiles, `govulncheck` output, and test results as evidence of remediation.

## Failure Handling

- If `go test` fails, diagnose the compilation or logic error, fix it, and re-run.
- If `govulncheck` reports unfixable vulnerabilities, document the risk and suggest mitigations (e.g., replacing the dependency).
- If `go fix` introduces breaking changes, roll back the changes using version control (`git restore .`) and apply fixes manually.
- Do not repeat a failed action unchanged; analyze the error output and adjust the approach.

## Output Contract

The final result must include:
- A summary of the assessment and diagnostics performed.
- A detailed list of remediations applied (e.g., vulnerabilities fixed, performance optimizations, code modernization).
- Evidence of validation (e.g., `go test` passing, `govulncheck` clean output).
- Any remaining risks or limitations (e.g., unfixable vulnerabilities, performance bottlenecks requiring architectural changes).
- Actionable next steps for the user.

## Resources

- [Complete Reference](./references/complete-reference.md): Exhaustive guide on Go architecture, troubleshooting, security, and enterprise patterns.
- [Reading List](./references/reading-list.md): Curated list of books, articles, and official documentation for advanced Go developers.
- [Security Audit Script](./scripts/security-audit.sh): Deterministic script to run `govulncheck` and `go test -race`.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Go services to audit | Security Auditor | Parallel security review of each service's codebase |
| Multiple packages to profile | Performance Profiler | Parallel execution of `pprof` and escape analysis |
| Multiple modules to update | Dependency Manager | Parallel updating and tidying of `go.mod` files |
| Bulk goroutine leak investigation | Diagnostics Agent | Parallel analysis of goroutine dumps across instances |

### Spawning Rules
- Spawn when 3+ independent items (services, packages, modules) need the same operation.
- Each sub-agent receives: context, specific target (e.g., service path), and expected output schema.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant security vulnerability, performance bottleneck, and diagnostic finding produced by the parallel sub-agents:
1. Spawn **3 independent Refuter Agents** per finding, each with the finding and instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
2. A finding is **confirmed** only if ≥2 refuters fail to refute it.
3. A finding is **discarded** if ≥2 refuters succeed.
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label.

### Cross-System Consistency Validator
After all parallel agents complete, but **before** synthesis, run one **Consistency Validator Agent** to flag logical contradictions and missing prerequisites. Pass these to the Synthesis Agent as `MUST_RESOLVE` and `SEQUENCING_REQUIRED` items.

### Synthesis Agent
The synthesis step actively resolves contradictions, re-orders the remediation plan based on prerequisites, calibrates confidence (`HIGH`/`MEDIUM`/`LOW`), and notes any analysis blind spots.
