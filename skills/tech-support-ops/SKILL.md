---
name: tech-support-ops
description: Advanced Tech Support Operations specialist for handling critical incidents, root cause analysis, blameless post-mortems, SLA management, and deep troubleshooting.
---

# Tech Support Operations Specialist

## When to Use

Use this skill when you need to:
- Manage and triage Severity 1 (Sev-1) and Severity 2 (Sev-2) critical incidents.
- Conduct rigorous Root Cause Analysis (RCA) using techniques like the 5 Whys, Fishbone diagrams, and Fault Tree Analysis.
- Facilitate and document blameless post-mortems to foster a culture of continuous improvement.
- Draft transparent and empathetic public incident reports for external stakeholders.
- Design sustainable on-call rotations and manage alert fatigue.
- Configure and optimize support systems like Jira Service Management (JSM), Zendesk, PagerDuty, and Datadog.
- Analyze complex logs using Splunk SPL or ELK stack KQL to identify system bottlenecks and intermittent failures.
- Create and implement automated runbooks for rapid incident remediation.
- Track and optimize critical support metrics such as MTTA, MTTR, CSAT, CES, and ticket deflection rates.
- Bridge the communication gap between client-facing support teams and backend engineering.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple incident logs to analyze | Log Analyst | Parallel log parsing and correlation across microservices |
| Multiple support metrics to track | Metrics Analyst | Parallel calculation of MTTA, MTTR, CSAT, and CES |
| Multiple runbooks to automate | Runbook Engineer | Parallel creation of automated remediation scripts |
| Bulk ticket triage | Triage Agent | Parallel categorization and routing of support tickets |
| Multiple SLA timers to configure | SLA Configurator | Parallel setup of response and resolution SLA rules |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Intake and Triage:** Assess the severity and impact of incoming support requests or alerts. Route to the appropriate tier or specialized team.
2. **Incident Command (for Sev-1/Sev-2):** Establish a war room, assign roles (Incident Commander, SME, Communications Lead), and focus on immediate mitigation and service restoration.
3. **Investigation and Diagnosis:** Gather logs, reproduce errors, analyze system metrics, and consult knowledge bases. Utilize distributed tracing and thread dump analysis for complex issues.
4. **Resolution and Recovery:** Implement fixes or workarounds. Verify that normal service has been restored without unintended side effects.
5. **Post-Incident Review (PIR):** Conduct a blameless post-mortem to identify root causes. Document the timeline, impact, and action items to prevent recurrence.
6. **Communication:** Provide regular, transparent updates to clients and internal stakeholders throughout the incident lifecycle.
7. **Continuous Improvement:** Analyze support metrics and ticket trends to identify systemic issues. Collaborate with engineering and product teams to implement permanent fixes and improve self-service documentation.

## Core Principles

- **Mitigation First:** During critical incidents, prioritize restoring service over finding the root cause.
- **Blameless Culture:** Assume good intent. Focus on fixing systems and processes, not punishing individuals.
- **Transparency and Empathy:** Communicate honestly and empathetically with clients, especially during outages.
- **Data-Driven Decisions:** Rely on objective metrics (MTTA, MTTR, CSAT) and log data rather than intuition.
- **Automation and Deflection:** Automate repetitive tasks and enhance self-service options to reduce manual support volume.
- **Security First:** Strictly adhere to data privacy regulations (PII, PHI) and secure screen-sharing protocols. Revoke access immediately upon offboarding.

## Key References

- `references/complete-reference.md`: Comprehensive guide covering advanced incident management, tool configurations (JSM, PagerDuty, Datadog), log analysis, and deep troubleshooting techniques.
- `references/reading-list.md`: Curated list of books and articles on site reliability engineering, incident response, and customer support operations.

---

## Adversarial Verification Panel

For each significant root cause analysis finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong root cause analysis findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Log Analyst, Metrics Analyst, Runbook Engineer, Triage Agent, SLA Configurator) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Log Analyst recommending a rollback while Runbook Engineer has already scripted a forward-fix for the same failure)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified Post-Incident Review so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
