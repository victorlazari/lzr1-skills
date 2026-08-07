---
name: tech-support-ops
description: Advanced Tech Support Operations specialist for handling critical incidents, AI-assisted triage, root cause analysis, blameless post-mortems, SLO/SLI tracking, error budgets, and deep troubleshooting.
---

# Tech Support Operations Specialist

## Scope and Triggers

Use this skill when you need to:
- Manage and triage Severity 1 (Sev-1) and Severity 2 (Sev-2) critical incidents using AI-assisted triage.
- Conduct rigorous Root Cause Analysis (RCA) using automated anomaly detection, distributed tracing, and techniques like the 5 Whys and Fault Tree Analysis.
- Facilitate and document blameless post-mortems to foster a culture of continuous improvement.
- Track and optimize critical support metrics such as MTTA, MTTR, CSAT, CES, and error budget burn rates.
- Define and track Service Level Objectives (SLOs) and Service Level Indicators (SLIs).
- Configure and optimize support systems like Jira Service Management (JSM), Zendesk AI, PagerDuty, and Datadog Incident Management.
- Create and implement automated runbooks for rapid incident remediation.

**Escalation Boundaries:**
- For writing customer-facing incident post-mortems or designing post-mortem slide decks, route to `post-mortem-master`.
- For incidents involving a potential security breach, vulnerability, or requiring exhaustive code security review, route to `security-review`.

## Preconditions

Before acting, ensure:
- Target environment and incident scope are clearly defined.
- Required permissions for accessing logs, metrics, and incident management tools are available.
- For automated remediation, explicit user confirmation is obtained before modifying production resources.

## Source Freshness

Volatile facts such as specific tool features or API endpoints for Datadog, PagerDuty, and Zendesk are verified against upstream documentation as of **2026-08-07**. Always verify current upstream documentation before applying tool-specific configurations or destructive actions.

## Workflow

1. **Intake and Triage:** Assess severity and impact using AI-assisted triage; route to appropriate tier.
2. **Incident Command:** Establish war room, assign roles, focus on mitigation.
3. **Investigation and Diagnosis:** Gather logs, analyze metrics, utilize distributed tracing and automated anomaly detection.
4. **Resolution and Recovery:** Implement fixes or workarounds; verify service restoration.
5. **Post-Incident Review:** Conduct blameless post-mortem using `templates/postmortem-template.md`; identify root causes.
6. **Metrics Tracking:** Calculate MTTA, MTTR, and error budget burn rates using `scripts/metrics-calculator.py`.
7. **Continuous Improvement:** Analyze metrics, update SLOs/SLIs, and implement permanent fixes. Stop when action items are assigned and tracked.

## Safety

- **Read-only discovery:** Always perform read-only discovery (e.g., log analysis, metric gathering) before attempting any mutations.
- **Confirmation required:** Require explicit user confirmation before executing any automated remediation scripts that modify production resources.
- **Dry-run:** Use dry-run support for `scripts/metrics-calculator.py` when testing metric calculations.

## Validation

- Verify that the skill correctly parses and categorizes incident logs.
- Validate that sub-agent spawning logic does not exceed concurrency limits (max 10).
- Ensure the consistency validator correctly identifies conflicting recommendations.
- Test the synthesis agent's ability to resolve contradictions and calibrate confidence levels.

## Failure Handling

- If an automated remediation script fails, do not repeat the same action unchanged. Diagnose the error using logs, consider alternative workarounds, and escalate if necessary.
- If metric calculation fails, verify the input data format and ensure dependencies are met.

## Output Contract

The result must include:
- A structured summary of the incident, including severity, impact, and timeline.
- Evidence of root cause analysis findings, categorized by confidence level (HIGH/MEDIUM/LOW).
- Calculated metrics (MTTA, MTTR, error budget burn rate) if applicable.
- Actionable next steps and assigned action items for continuous improvement.

## Resources

- `references/complete-reference.md`: Comprehensive guide covering advanced incident management, SLO/SLI tracking, error budgets, automated remediation workflows, and tool configurations (JSM, PagerDuty, Datadog, Zendesk).
- `templates/postmortem-template.md`: Standardized blameless post-mortem template based on Google SRE and PagerDuty best practices.
- `scripts/metrics-calculator.py`: Script to automatically calculate MTTA, MTTR, and error budget burn rates.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple incident logs to analyze | Log Analyst | Parallel log parsing and correlation across microservices |
| Multiple support metrics to track | Metrics Analyst | Parallel calculation of MTTA, MTTR, CSAT, and CES |
| Multiple runbooks to automate | Runbook Engineer | Parallel creation of automated remediation scripts |
| Bulk ticket triage | Triage Agent | Parallel categorization and routing of support tickets |
| Multiple SLA timers to configure | SLA Configurator | Parallel setup of response and resolution SLA rules |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant root cause analysis finding produced by parallel sub-agents:
1. Spawn 3 independent Refuter Agents per finding.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.
4. When a confirmed finding had 1 successful refuter, include the dissenting argument with a `CONTESTED` label.

### Cross-System Consistency Validator
After all parallel agents complete, but before synthesis:
Run one Consistency Validator Agent to flag logical contradictions (`MUST_RESOLVE`) and missing prerequisites (`SEQUENCING_REQUIRED`).

### Synthesis Agent
The synthesis step actively resolves:
1. `MUST_RESOLVE` contradictions: Pick the better recommendation, annotate reasoning.
2. `SEQUENCING_REQUIRED` items: Re-order the unified Post-Incident Review.
3. Confidence calibration: Label each finding HIGH/MEDIUM/LOW.
4. Gap analysis: Note any analysis dimension not covered.
