---
name: manus
description: Mastering Manus Autonomous Agent Platform, Sandbox Environments, Browser Automation, Web Development Scaffolds, MCP Integration, File Management, and Scheduling
---

# Manus Specialist Skill

## When to Use

Use this skill when you need to architect, scale, secure, or troubleshoot complex solutions using the Manus autonomous agent platform. This includes:
- Orchestrating complex agent pipelines and parallel clusters.
- Configuring and troubleshooting sandboxed execution environments.
- Managing robust browser automation at scale.
- Building and extending web development scaffolds (frontend and backend).
- Integrating with the Manus Control Plane (MCP) for scheduling and state management.
- Handling complex file management and synchronization patterns.
- Diagnosing and resolving agent execution, connectivity, and automation failures.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple agents in a pipeline | Pipeline Orchestrator | Parallel execution of independent pipeline stages |
| High-throughput browser automation | Browser Automation Agent | Parallel scraping or interaction across multiple URLs |
| Bulk file processing/transfer | File Management Agent | Parallel chunk uploads or delta synchronization |
| Distributed health checks | Diagnostics Agent | Parallel monitoring of MCP components and sandboxes |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., scraping multiple sites, processing multiple files).
- Each sub-agent receives: context, specific target (e.g., URL, file chunk), success criteria.
- Results are aggregated and cross-referenced for conflicts or errors.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Architecture & Orchestration**: Define the agent workflow (chained pipelines, event-driven, or parallel clusters).
2. **Sandbox Configuration**: Set up isolation mechanisms (namespaces, cgroups) and fine-grained permissions (filesystem whitelisting, network policies).
3. **Browser Automation Setup**: Implement browser pooling, session isolation, and robust waiting strategies for dynamic content.
4. **Web Scaffold Integration**: Extend frontend dashboards and backend APIs, integrating with MCP for event handling.
5. **MCP & Scheduling**: Configure cron-like schedules, dependency scheduling, and retry policies. Ensure MCP components are scaled horizontally.
6. **File Management**: Set up volume mounts, object storage integration, and secure file transfer mechanisms.
7. **Troubleshooting**: Monitor logs, metrics, and traces to diagnose execution failures, connectivity issues, or automation errors.

## Core Principles

- **Security First**: Enforce strict sandbox isolation, capability dropping, and secure credential injection.
- **Scalability**: Utilize horizontal scaling for MCP components and parallel agent clusters for high throughput.
- **Resilience**: Implement retry logic, dead letter queues, and high availability configurations to handle transient failures.
- **Efficiency**: Optimize resource utilization through browser pooling, lazy initialization, and incremental file synchronization.
- **Observability**: Maintain comprehensive logging, metrics collection, and tracing for rapid troubleshooting.

## Key References

- [Manus Platform Official Documentation](https://docs.manus-platform.io)
- [Manus GitHub Repository](https://github.com/manus-platform)
- [Puppeteer Documentation](https://pptr.dev)
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [PostgreSQL Clustering Best Practices](https://www.postgresql.org/docs/current/high-availability.html)
- [AWS S3 Multipart Upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)

---

## Adversarial Verification Panel

For each significant agent execution diagnosis and remediation recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong agent execution diagnoses and remediation recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Pipeline Orchestrator, Browser Automation Agent, File Management Agent, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Pipeline Orchestrator recommends increasing max concurrent sub-agents beyond 10 for throughput, while the Diagnostics Agent flags resource exhaustion on the sandbox nodes and recommends reducing concurrency)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified agent pipeline execution report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
