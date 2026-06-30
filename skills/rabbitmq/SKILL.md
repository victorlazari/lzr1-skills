---
name: rabbitmq
description: Advanced RabbitMQ operations, troubleshooting, and architecture design for tech support specialists and SREs.
---

# RabbitMQ Tech Support Operations Specialist

This skill provides comprehensive expertise in managing, troubleshooting, and optimizing RabbitMQ in high-stakes production environments. It covers advanced operations, cluster management, high availability patterns, and worst-case scenario mitigation.

## When to Use

Use this skill when you need to:
- Diagnose and resolve RabbitMQ production incidents (memory/disk alarms, network partitions).
- Troubleshoot massive message backlogs and consumer starvation.
- Design or audit RabbitMQ topologies (exchanges, queues, bindings, DLX).
- Configure and tune RabbitMQ for high throughput or low latency.
- Perform security audits on RabbitMQ clusters (TLS, RBAC, LDAP).
- Migrate from Classic Mirrored Queues to Quorum Queues.
- Analyze Erlang VM (BEAM) performance and memory fragmentation.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple clusters to audit | Security Auditor | Parallel security review of each RabbitMQ cluster |
| Multiple vhosts to validate | Topology Validator | Parallel validation of exchanges, queues, and bindings |
| Multiple nodes to check | Health Checker | Parallel diagnostics and log analysis of cluster nodes |
| Bulk queue troubleshooting | Diagnostics Agent | Parallel investigation of queues with massive backlogs |

### Spawning Rules
- Spawn when 3+ independent items (clusters, vhosts, nodes, queues) need the same operation.
- Each sub-agent receives: context, specific target (e.g., node IP, vhost name), success criteria.
- Results are aggregated and cross-referenced for cluster-wide insights.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Information Gathering:** Assess the current state using `rabbitmq-diagnostics` and `rabbitmqctl`. Check alarms, cluster status, memory breakdown, and top queues.
2. **Emergency Mitigation:** Take immediate action to restore service (e.g., unblock publishers, kill rogue clients, resolve partitions) based on business SLAs.
3. **Deep Dive Diagnostics:** Analyze Erlang VM stats, RabbitMQ logs, and consumer application behavior to identify the root cause.
4. **Topology & Configuration Review:** Audit `rabbitmq.conf`, `advanced.config`, and `definitions.json` for optimal settings and security compliance.
5. **Remediation & Optimization:** Implement long-term fixes such as migrating to Quorum Queues, applying policies (e.g., max-length, DLX), and tuning prefetch counts.
6. **Documentation & Guidance:** Provide actionable feedback to engineering teams on connection management, publisher confirms, and consumer acknowledgements.

## Core Principles

- **Visibility First:** Rely on metrics (Prometheus/Grafana) and CLI diagnostics before making changes.
- **Protect the Broker:** Respect memory and disk alarms; they are self-preservation mechanisms. Do not blindly restart nodes under load.
- **Quorum Queues Default:** Advocate for Quorum Queues over Classic Mirrored Queues for data safety and predictable performance.
- **Declarative Management:** Use `definitions.json` and policies for reproducible and dynamic configuration.
- **Consumer Responsibility:** 95% of issues are caused by misbehaving applications (connection leaks, slow consumers, lack of ACKs). Hold consumers accountable.

## Key References

- [Complete Reference](./references/complete-reference.md): Exhaustive guide on RabbitMQ internals, CLI tools, configuration, security, and troubleshooting.
- [Reading List](./references/reading-list.md): Curated list of books and articles for continuous learning in distributed systems and RabbitMQ operations.

---

## Adversarial Verification Panel

For each significant production incident and optimization finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong production incidents and optimization findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Security Auditor, Topology Validator, Health Checker, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Auditor recommending disabling a vhost while Topology Validator marks its bindings as healthy and required)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified remediation and optimization plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
