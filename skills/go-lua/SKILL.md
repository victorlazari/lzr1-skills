---
name: go-lua
description: Advanced Go and Lua operational playbook for performance profiling, memory tuning, CGO, Redis Lua patterns, and database migrations.
---

# Go and Lua Specialist Skill

## Scope and Triggers

Use this skill when you need to:
- Diagnose and resolve performance bottlenecks in Go applications using `pprof`.
- Tune Go garbage collection (`GOGC`, `GOMEMLIMIT`) and manage memory footprints.
- Write, debug, and optimize advanced Redis Lua scripts.
- Bridge Go with C using CGO for performance-critical operations.
- Handle huge datasets in-memory efficiently.
- Perform security audits on Go dependencies and Lua scripts.
- Manage database migrations using `golang-migrate` and recover from dirty states.
- Troubleshoot worst-case scenarios like goroutine leaks, deadlocks, and OOM kills.

**Escalation Boundaries:**
- For infrastructure-level debugging (e.g., Kubernetes pod crash-looping), route to `terraform-kubernetes-ops`.
- For observability alerts (e.g., "High Memory Usage"), route to `prometheus-grafana-alerts`.
- For deep security audits, route to `security-auditing-tools`.
- For database performance tuning outside migrations, route to `postgresql-dba-guide`.

## Preconditions

Before acting, verify:
- The target environment (e.g., Go version, Redis version).
- Permissions to execute profiling tools or database migrations.
- The specific issue or trigger condition.

## Source Freshness

Volatile facts like CGO overhead and GC behavior must be verified against the deployed Go version. Consult the official Go documentation and Redis Lua documentation for the most current information.

## Workflow

1. **Identify the Issue:** Determine the specific problem (e.g., high CPU, memory leak, Redis blocking, migration failure).
2. **Gather Diagnostics:** Use appropriate tools (e.g., `go tool pprof`, Redis `SLOWLOG`, `migrate version`).
3. **Analyze Diagnostics:** Pinpoint the root cause (e.g., runaway loops, excessive allocations, blocking operations).
4. **Apply Tuning/Fixes:** Adjust Go runtime parameters (`GOGC`/`GOMEMLIMIT`), rewrite Lua scripts, or manually recover dirty migrations.
5. **Verify Fix:** Test in a safe environment or with a dry run before applying to production.
6. **Stop Condition:** The issue is resolved, and performance metrics return to normal.

## Safety

- **Read-Only Discovery:** Always gather diagnostics (e.g., `pprof`, `SLOWLOG`) before making any changes.
- **Confirmation Required:** Require confirmation before running destructive Redis Lua scripts (e.g., bulk deletes) or forcing database migration states.
- **Validation:** Validate Go memory tuning (`GOMEMLIMIT`) against container limits. Ensure Redis Lua scripts strictly use `KEYS` and `ARGV` to prevent injection. Run `govulncheck` on Go dependencies. Verify CGO calls are batched.

## Validation

- **Syntax Checks:** Run `bash -n` on shell scripts, compile Python scripts, and parse structured templates.
- **Dry Runs:** Perform dry runs for mutating scripts whenever feasible.
- **Postcondition Verification:** Verify that the applied fixes resolve the issue without introducing new problems.

## Failure Handling

- **Diagnose Errors:** Use logs and profiling data to understand why a fix failed.
- **Choose Alternatives:** If one approach fails, try another (e.g., if `GOGC` tuning doesn't work, investigate memory leaks).
- **Rollback:** Have a rollback plan for database migrations and configuration changes.
- **Avoid Repetition:** Do not repeat a failed action without modifying the approach.

## Output Contract

The result must include:
- A structured summary of the issue and the applied fixes.
- Evidence of the diagnostics gathered (e.g., `pprof` output, `SLOWLOG` entries).
- Confidence level (HIGH/MEDIUM/LOW) for the applied fixes.
- Actionable next steps for monitoring or further tuning.

## Resources

- [Go and Lua Operations Guide](references/go-lua-operations.md): Consolidated operational guide for Go profiling, memory tuning, CGO, Redis Lua patterns, and `golang-migrate` recovery.
