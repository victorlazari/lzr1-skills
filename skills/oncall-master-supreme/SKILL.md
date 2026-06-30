---
name: oncall-master-supreme
description: Advanced guide to modern on-call systems, covering high availability, ChatOps, postmortems, runbook automation, SLO tracking, and multi-region handoffs.
---

# On-Call Master Supreme

## When to Use

Use this skill when you need to:
- Design or audit high availability (HA) and disaster recovery (DR) architectures for on-call systems.
- Integrate ChatOps (Slack, Microsoft Teams) for incident war rooms and automated notifications.
- Conduct blameless post-incident reviews (postmortems) and integrate with tools like Jeli.
- Automate runbooks and implement auto-remediation workflows to reduce MTTR.
- Define, track, and report on Service Level Objectives (SLOs) and Service Level Indicators (SLIs).
- Implement and manage follow-the-sun multi-region on-call schedules and handoffs.
- Utilize the `oncall-master-supreme` CLI for incident management, scheduling, and configuration.
- Manage JSON-based configuration schemas for notifications, escalations, users, integrations, and security.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple services to configure | Configuration Agent | Parallel setup of service integrations and policies |
| Multiple incidents to analyze | Incident Analyst | Parallel root cause analysis and postmortem generation |
| Multiple regions to schedule | Scheduling Agent | Parallel creation of follow-the-sun rotations |
| Bulk runbook automation | Automation Engineer | Parallel scripting of auto-remediation workflows |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Assessment & Planning**: Evaluate the current on-call architecture, identify gaps in HA/DR, and define SLOs/SLIs.
2. **Configuration Management**: Use the CLI or JSON schemas to configure global settings, schedules, notifications, and escalations.
3. **Integration Setup**: Connect monitoring tools (Datadog, Prometheus) and ChatOps platforms (Slack, Teams) to the on-call system.
4. **Automation Implementation**: Develop and deploy runbook automation and auto-remediation scripts for common incidents.
5. **Incident Response**: Utilize the CLI and ChatOps war rooms to acknowledge, investigate, and resolve active incidents.
6. **Post-Incident Review**: Conduct blameless postmortems, leverage Jeli for timeline reconstruction, and track remediation actions.
7. **Continuous Improvement**: Review SLO compliance, adjust alert thresholds, and refine follow-the-sun handoff protocols.

## Core Principles

- **High Availability**: On-call systems must be resilient, utilizing multi-zone deployments and automated failover.
- **Blameless Culture**: Postmortems focus on systemic failures, not human error, to foster continuous learning.
- **Automation First**: Reduce manual toil and MTTR through runbook automation and auto-remediation.
- **Data-Driven Reliability**: Use SLOs and SLIs to objectively measure service health and prioritize engineering efforts.
- **Sustainable Operations**: Implement follow-the-sun models to prevent burnout and ensure continuous global coverage.

## Key References

- **Google Site Reliability Engineering** (2016). Betsy Beyer et al.
- **The DevOps Handbook** (2016). Gene Kim et al.
- **ChatOps: Collaboration at Scale** (2016). Paul Hammond.
- **Service Level Objectives: A Practical Guide** (2020). Cindy Sridharan.
- **Incident Management at Scale** (2020). Charity Majors et al.

---

## Parallel Execution Protocol

> **All 4 agents launch simultaneously.** Do not wait for one to finish before starting the next. Each agent receives the full task context and its dedicated reference file only.

### Agent Roster

| Agent | Dimension | Scope | Reference |
|---|---|---|---|
| **Infra Investigator** | Infrastructure Layer | Network, DNS, load balancers, node health, disk I/O, CPU/memory saturation | `references/complete-reference.md` |
| **App Investigator** | Application Layer | Error rates, latency percentiles, dependency failures, deploy correlation, code regression | `references/complete-reference.md` |
| **Data Investigator** | Data Layer | Database saturation, replication lag, slow queries, lock contention, connection pool exhaustion | `references/complete-reference.md` |
| **Runbook Lookup** | Runbook & Historical Correlation | Match error signatures to known incidents, retrieve applicable runbooks, check recent changes | `references/complete-reference.md` |

### Spawning Rules

- **Trigger**: Every invocation of this skill — no exceptions
- **Concurrency**: All 4 agents launch in a single `parallel()` call
- **Context per agent**: Full task input + its dedicated reference file only (no cross-agent sharing during analysis)
- **Maximum concurrent agents**: 4

### Synthesis Agent

After all 4 agents report, run one **Synthesis Agent** with all reports that:

1. **Cross-references** findings across dimensions for interaction effects that no single agent could see
2. **Deduplicates** overlapping findings (same issue detected by multiple agents → one canonical entry)
3. **Prioritizes** the merged set by severity/impact
4. **Produces** a single unified output document

> Synthesis note for this skill: Produce a unified blast radius map. Cross-reference Infra, App, and Data findings to determine whether the infra signal is root cause or a cascade from the app or data layer. Link matched runbooks to the confirmed root cause.

### Quality Gate

A finding from one agent that **contradicts** a finding from another agent must be flagged as `CONFLICT` and passed to the Synthesis Agent as a `MUST_RESOLVE` item — never silently dropped.
