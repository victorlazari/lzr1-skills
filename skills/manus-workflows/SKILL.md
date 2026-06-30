---
name: manus-workflows
description: Advanced guide for Manus Workflow & Integration Specialists to architect, implement, and troubleshoot sophisticated workflows.
---

# Manus Workflows

## When to Use

Use this skill when you need to:
- Design and implement complex, multi-step workflows in Manus.
- Integrate diverse tools, APIs, and services into a cohesive automation pipeline.
- Configure advanced scheduling, including cron expressions, timezone management, and recurrence rules.
- Handle robust file operations, including cloud storage integration and secure transfers.
- Implement inter-workflow messaging patterns (Pub/Sub, Request/Reply, Event Streaming).
- Optimize workflow performance, manage state, and configure retry/recovery policies.
- Troubleshoot and diagnose workflow execution failures, data integration issues, and performance bottlenecks.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple workflows to audit | Workflow Auditor | Parallel review of workflow definitions and dependencies |
| Multiple connectors to configure | Integration Specialist | Parallel setup and validation of external API connectors |
| Multiple schedules to validate | Scheduling Expert | Parallel verification of cron expressions and timezone rules |
| Bulk log analysis | Diagnostics Agent | Parallel investigation of workflow execution logs and errors |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis**: Understand the business process, required tools, and data flow.
2. **Architecture Design**: Define the workflow structure (DAG), identifying sequential and parallel tasks.
3. **Integration Setup**: Configure necessary connectors, authentication, and data transformation mappings.
4. **Implementation**: Write the workflow definition (JSON/YAML), incorporating conditional logic and error handling.
5. **Scheduling & Triggers**: Define how the workflow is initiated (cron, webhook, event).
6. **Testing & Validation**: Use the CLI to validate the schema and run test executions.
7. **Deployment**: Deploy the workflow configuration using CI/CD practices.
8. **Monitoring & Maintenance**: Set up logging, telemetry, and alerts to monitor workflow health.

## Core Principles

- **Modularity**: Break workflows into smaller, reusable tasks.
- **Idempotency**: Ensure tasks can be safely retried without unintended side effects.
- **Resilience**: Implement comprehensive try/catch, fallback logic, and retry policies with exponential backoff.
- **Observability**: Use detailed logging and telemetry to track workflow execution and performance.
- **Security**: Apply least privilege principles, secure secret management, and encrypt sensitive data.
- **Scalability**: Design workflows to handle varying loads using parallel execution and asynchronous messaging.

## Key References

- **Global Engine Configuration**: `manus-global.yaml` controls core settings, execution engine, database, and logging.
- **Workflow Definition Schema**: `workflow-schema.json` dictates the structure of workflows, triggers, and tasks.
- **Integration Configuration**: `connectors.yaml` manages external service connections and credentials.
- **Security Configuration**: `rbac-config.yaml` defines roles, permissions, and access control.
- **CLI Tool**: `manus-workflows` CLI for initializing, running, managing, and monitoring workflows.

---

## Adversarial Verification Panel

For each significant workflow execution issue, integration failure, or performance bottleneck produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong workflow execution issues, integration failures, or performance bottlenecks from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Workflow Auditor, Integration Specialist, Scheduling Expert, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Diagnostics Agent recommends increasing retry attempts to handle transient connector failures, while the Workflow Auditor flags the same retry logic as a cascading failure risk that will amplify load on a degraded downstream service)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified workflow remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
