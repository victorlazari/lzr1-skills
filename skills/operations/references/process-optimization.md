# Process Optimization

**Verified against upstream:** 2026-08-07
**Primary Sources:**
- ITIL 4 Foundation (https://www.axelos.com/certifications/itil-service-management/itil-4-foundation)

## Table of Contents
1. Process Design
2. Lean Methodology
3. Automation Strategy
4. Change Management
5. Operational Playbooks

---

## 1. Process Design (ITIL 4 Service Value System Integration)

### Process Documentation Framework

| Component | Description | Format |
|---|---|---|
| Process name | Clear, descriptive title | Title |
| Owner | Accountable person | Name + role |
| Trigger | What starts the process | Event description |
| Inputs | What's needed to begin | List |
| Steps | Sequential activities | Numbered steps |
| Decision points | Where choices are made | If/then logic |
| Outputs | What the process produces | Deliverables |
| Metrics | How to measure success | KPIs |
| SLA | Expected completion time | Time target |

### Process Mapping Symbols

| Symbol | Meaning | Use |
|---|---|---|
| Rectangle | Activity/Task | Standard process step |
| Diamond | Decision | Yes/No branch point |
| Oval | Start/End | Process boundaries |
| Arrow | Flow | Direction of process |
| Parallelogram | Input/Output | Data or documents |
| Circle | Connector | Links between pages |

---

## 2. Lean Methodology

### Eight Wastes (DOWNTIME)

| Waste | Description | Tech Company Example |
|---|---|---|
| Defects | Errors requiring rework | Bugs, incorrect data |
| Overproduction | Making more than needed | Features nobody uses |
| Waiting | Idle time between steps | Approval bottlenecks |
| Non-utilized talent | Underusing people's skills | Senior engineers on routine tasks |
| Transportation | Unnecessary movement | Data moving between systems |
| Inventory | Excess work in progress | Too many open projects |
| Motion | Unnecessary steps | Context switching |
| Extra processing | More work than needed | Over-engineering, gold-plating |

### Value Stream Mapping

```
Current State:
Request → [Wait 2d] → Triage → [Wait 1d] → Assign → [Work 3d] → Review → [Wait 1d] → Deploy
Total lead time: 7 days
Value-add time: 3 days
Efficiency: 43%

Future State:
Request → Auto-triage → [Work 2d] → Auto-review → Auto-deploy
Total lead time: 2.5 days
Value-add time: 2 days
Efficiency: 80%
```

---

## 3. Automation Strategy

### Automation Decision Framework

| Factor | Automate | Don't Automate |
|---|---|---|
| Frequency | >10 times/week | Once a quarter |
| Complexity | Rule-based, predictable | Requires judgment |
| Error rate | High when manual | Low risk |
| Volume | High volume | Low volume |
| Cost | High labor cost | Low labor cost |
| Stability | Process is stable | Process is changing |

### Automation Tools by Category

| Category | Tools | Use Case |
|---|---|---|
| Workflow | Zapier, Make, n8n | Connect apps, trigger actions |
| RPA | UiPath, Automation Anywhere | Legacy system automation |
| CI/CD | GitHub Actions, GitLab CI | Code deployment |
| Document | DocuSign, PandaDoc | Contract workflows |
| Communication | Slack workflows, Teams Power Automate | Notifications, approvals |
| Data | Fivetran, Airbyte | Data pipeline automation |
| IT | Okta, Rippling | User provisioning |

---

## 4. Change Management

### ADKAR Model

| Phase | Description | Activities |
|---|---|---|
| Awareness | Why change is needed | Communication, business case |
| Desire | Want to participate | WIIFM, address resistance |
| Knowledge | How to change | Training, documentation |
| Ability | Implement the change | Practice, support, coaching |
| Reinforcement | Sustain the change | Metrics, recognition, accountability |

### Change Readiness Assessment

| Factor | Assessment Questions | Score (1-5) |
|---|---|---|
| Sponsorship | Is leadership visibly supporting? | |
| Urgency | Is there a compelling reason to change? | |
| Impact | How many people/processes affected? | |
| Complexity | How complex is the change? | |
| History | Have past changes succeeded? | |
| Culture | Is the culture change-friendly? | |
| Resources | Are resources available? | |

---

## 5. Operational Playbooks

### Playbook Structure

```
# [Process Name] Playbook

## Overview
- Purpose: Why this process exists
- Owner: Who's accountable
- Last updated: Date

## When to Use
- Trigger conditions
- Scope (what's included/excluded)

## Prerequisites
- Access needed
- Tools required
- Information needed

## Steps
1. [Step 1 with details]
2. [Step 2 with details]
   - If [condition]: [alternative path]
3. [Step 3 with details]

## Escalation
- When to escalate
- Who to escalate to
- What information to include

## Metrics
- SLA: [target time]
- Quality: [success criteria]

## FAQ
- Common questions and answers
```

### SOP Categories for Tech Companies

| Category | SOPs Needed |
|---|---|
| Engineering | Incident response, deployment, on-call rotation |
| Sales | Lead qualification, deal review, handoff to CS |
| Customer Success | Onboarding, QBR, escalation, churn prevention |
| HR | Hiring, onboarding, offboarding, performance review |
| Finance | Expense approval, vendor payment, month-end close |
| Legal | Contract review, NDA processing, compliance check |
| IT | Access provisioning, equipment, security incident |

## Recommended Reading (Source Map)
- **The Lean Startup** — Eric Ries (2011), Crown. Lean methodology for startups.
- **Lean Thinking** — James Womack & Daniel Jones (2003), Free Press. Lean principles.
- **The Toyota Way** — Jeffrey Liker (2nd ed, 2021), McGraw-Hill. Toyota production system.
- **Value Stream Mapping** — Karen Martin & Mike Osterling (2014), McGraw-Hill.
- **This Is Lean** — Niklas Modig & Par Ahlstrom (2012). Lean fundamentals.
- **The Machine That Changed the World** — Womack, Jones & Roos (2007), Free Press.
- **Switch** — Chip Heath & Dan Heath (2010), Crown. Change methodology.
- **Leading Change** — John Kotter (2012), HBR Press. Change leadership.
- **The Lean Change Method** — Jeff Anderson (2013). Agile change management.
- **Accelerate** — John Kotter (2014), HBR Press. Dual operating system.
- **Lean Enterprise Institute** — lean.org. Lean resources.
- **Process Street Blog** — process.st/blog. Process documentation.
- **Tallyfy Blog** — tallyfy.com/blog. Workflow automation.
- **Kissflow Blog** — kissflow.com/blog. Process management.
- **Zapier Blog** — zapier.com/blog. Automation ideas and guides.
- **Make (Integromat) Blog** — make.com/blog. Workflow automation.
- **n8n Blog** — n8n.io/blog. Open-source automation.
- **UiPath Blog** — uipath.com/blog. RPA and automation.
- **Prosci** — prosci.com. ADKAR change management.
- **McKinsey Operations** — mckinsey.com/business-functions/operations. Operations research.
