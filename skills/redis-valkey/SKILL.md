---
name: redis-valkey
description: Advanced Redis and Valkey production operations, troubleshooting, and migration guide. Triggers on latency, memory, hot keys, Lua script issues, or migration tasks.
---

# Redis and Valkey Operations Skill

## Scope and Triggers

Use this skill when tasked with:
- Troubleshooting Redis or Valkey performance issues (latency, memory exhaustion, CPU spikes).
- Identifying and mitigating hot keys in large-scale deployments.
- Planning, executing, or validating a migration from Redis to Valkey.
- Performing advanced CLI operations for data manipulation, cluster management, and incident response.
- Reviewing Lua scripts for atomic operations.

**Non-goals:** This skill does not cover application-level code changes outside of Lua scripts, nor does it cover network infrastructure setup.

## Preconditions

Before acting, the agent must:
1. Detect the target environment (Redis or Valkey) and its version.
2. Verify permissions to execute CLI commands.
3. Confirm user intent, especially for destructive actions or migrations.
4. For migrations, explicitly verify that the source Redis version is 7.2 or earlier. Valkey is incompatible with Redis CE 7.4+ RDB files.

## Source Freshness

Volatile facts (e.g., supported versions, specific command flags) must be verified against official documentation. See `references/complete-reference.md` for verified primary sources. Always check current upstream documentation before applying production-impacting actions.

## Workflow

1. **Assess the Situation:** Run `scripts/redis-health-check.sh` to gather deterministic metrics (memory, latency, basic health).
2. **Identify the Bottleneck:** Use appropriate CLI tools (`--latency`, `--bigkeys`, `--hotkeys`, `SLOWLOG`) to pinpoint the root cause.
3. **Formulate a Plan:** Develop a mitigation or migration strategy. Consult `references/complete-reference.md` for advanced strategies.
4. **Pre-Migration Validation (If applicable):** Run `scripts/valkey-migration-check.sh` to verify version compatibility and module availability.
5. **Execute with Safety:** Apply changes. Require confirmation for destructive actions. Use dry-runs where applicable.
6. **Validate and Monitor:** Validate post-conditions and monitor system health.
7. **Stop:** Stop when the issue is resolved or the migration is successfully completed and validated.

## Safety

- **Read-Only Discovery:** Always perform read-only discovery (e.g., `INFO`, `MEMORY STATS`) before any mutations.
- **Confirmation Required:** Require explicit user confirmation for destructive actions (e.g., `FLUSHALL`, `SCRIPT KILL`, `SHUTDOWN`), external network changes, or production-impacting migrations.
- **Dry Runs:** Use dry-runs for migration scripts and bulk data operations where feasible.

## Validation

- **Syntax Checks:** Validate Lua scripts before deployment.
- **Postcondition Verification:** After a migration, verify data integrity (key counts, memory usage) and performance metrics.
- **Rollback:** If a migration fails, revert to the original Redis instance (if using Replica Promotion) or restore from the original RDB backup.

## Failure Handling

- If a command fails, diagnose the error using the output and logs.
- Do not repeat a failed action unchanged.
- If a migration step fails, consult the rollback guidance and restore the system to its previous state.

## Output Contract

The final output must include:
- **Structure:** A clear summary of the issue, actions taken, and current status.
- **Evidence:** Output from health checks and validation scripts.
- **Severity/Confidence:** Confidence level in the resolution (High/Medium/Low).
- **Actionable Next Steps:** Recommendations for future monitoring or architectural changes.

## Resources

- `references/complete-reference.md`: Advanced topics, caching patterns, Lua scripting, messaging, and CLI reference.
- `scripts/redis-health-check.sh`: Deterministic script for basic health checks, memory stats, and latency measurements.
- `scripts/valkey-migration-check.sh`: Deterministic script to verify Redis version compatibility before migration.

## Orchestration (Parallel Sub-Agents)

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple shards/nodes to analyze | Node Analyzer | Parallel performance and health checks of individual nodes |
| Multiple Lua scripts to review | Script Reviewer | Parallel review of Lua scripts for performance and safety |
| Multiple keyspaces to scan | Keyspace Scanner | Parallel scanning for big keys or hot keys |
| Bulk data migration tasks | Migration Agent | Parallel data transfer and validation across instances |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant performance bottleneck and operational issue produced by the parallel sub-agents:
1. Spawn 3 independent Refuter Agents per finding.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.

### Cross-System Consistency Validator
Run one Consistency Validator Agent with all parallel outputs to flag logical contradictions and note prerequisites.

### Synthesis Agent
The synthesis step actively resolves contradictions, re-orders based on prerequisites, calibrates confidence, and notes blind spots.
