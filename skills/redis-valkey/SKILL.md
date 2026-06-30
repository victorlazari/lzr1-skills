---
name: redis-valkey
description: Advanced Redis and Valkey production operations, troubleshooting, and migration guide.
---

# Redis and Valkey Operations Skill

## When to Use

Use this skill when tasked with:
- Troubleshooting Redis or Valkey performance issues, such as high latency, memory exhaustion, or CPU spikes.
- Designing or reviewing advanced caching strategies (Cache Aside, Write-Through, Write-Behind).
- Implementing or debugging Lua scripts for atomic operations.
- Choosing between or troubleshooting messaging paradigms (Pub/Sub vs. Streams).
- Managing document data with RedisJSON and mitigating associated memory overhead.
- Identifying and mitigating hot keys in large-scale deployments.
- Planning, executing, or validating a migration from Redis to Valkey.
- Performing advanced CLI operations for data manipulation, cluster management, and incident response.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple shards/nodes to analyze | Node Analyzer | Parallel performance and health checks of individual nodes |
| Multiple Lua scripts to review | Script Reviewer | Parallel review of Lua scripts for performance and safety |
| Multiple keyspaces to scan | Keyspace Scanner | Parallel scanning for big keys or hot keys |
| Bulk data migration tasks | Migration Agent | Parallel data transfer and validation across instances |

### Spawning Rules
- Spawn when 3+ independent items (nodes, scripts, keyspaces) need the same operation.
- Each sub-agent receives: context, specific target (e.g., node IP/port, script content), success criteria.
- Results are aggregated and cross-referenced for conflicts or cluster-wide patterns.
- Maximum concurrent sub-agents: 10.

## Workflow

1.  **Assess the Situation:** Determine the core issue (e.g., latency, memory, migration planning). Gather initial metrics using `INFO`, `MEMORY STATS`, or continuous stat mode (`--stat`).
2.  **Identify the Bottleneck:** Use appropriate CLI tools (`--latency`, `--bigkeys`, `--hotkeys`, `SLOWLOG`) to pinpoint the root cause.
3.  **Formulate a Mitigation Plan:** Based on the findings, develop a strategy. For example, implement client-side caching for hot keys, optimize Lua scripts, or adjust eviction policies.
4.  **Execute and Monitor:** Apply the changes carefully, especially in production. Monitor the system closely to ensure the issue is resolved and no new problems are introduced.
5.  **Post-Incident Review:** Document the incident, the root cause, and the steps taken to resolve it. Update runbooks and monitoring alerts as necessary.

## Core Principles

-   **Protect the Single Thread:** Redis and Valkey are primarily single-threaded. Avoid long-running commands (`KEYS`, complex Lua scripts) that block the event loop.
-   **Memory is King:** Monitor memory usage closely. Choose the right eviction policy and data structures to optimize memory consumption.
-   **Measure Before Acting:** Always gather data before making changes. Use the CLI's diagnostic tools to understand the system's behavior.
-   **Plan for Failure:** Implement robust error handling, retries, and fallback mechanisms in application code. Understand the implications of network partitions and node failures.
-   **Embrace Automation:** Script repetitive tasks and use the CLI's non-interactive modes for bulk operations.

## Key References

-   **Advanced Caching:** Understand Cache Aside, Write-Through, Write-Behind, and eviction policies (LRU, LFU).
-   **Lua Scripting:** Ensure atomicity but avoid blocking the server. Use `EVALSHA` and parameterize scripts.
-   **Messaging:** Choose Pub/Sub for ephemeral, low-latency broadcasting, and Streams for persistent, acknowledged messaging.
-   **RedisJSON:** Leverage in-place updates but monitor memory overhead.
-   **Hot Keys:** Identify using `--hotkeys` or client metrics. Mitigate with client-side caching or key sharding.
-   **Valkey Migration:** Assess compatibility (fork of Redis 7.2.4). Use Replica Promotion for zero downtime or Backup and Restore for simpler setups.
-   **CLI Mastery:** Utilize `--stat`, `--latency`, `--bigkeys`, `--pipe`, and cluster management commands for effective administration.

---

## Adversarial Verification Panel

For each significant performance bottleneck and operational issue produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong performance bottlenecks and operational issues from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Node Analyzer, Script Reviewer, Keyspace Scanner, Migration Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Node Analyzer recommends increasing `maxmemory` to reduce eviction pressure while Keyspace Scanner recommends aggressively evicting large keys to free memory)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified operational report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
