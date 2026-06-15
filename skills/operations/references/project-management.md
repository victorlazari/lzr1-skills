# Project & Program Management

## Table of Contents
1. Methodologies
2. Planning and Execution
3. Risk Management
4. Stakeholder Management
5. Program Management

---

## 1. Methodologies

### Methodology Comparison

| Methodology | Best For | Approach | Cadence |
|---|---|---|---|
| Scrum | Product development, small teams | Iterative sprints | 2-week sprints |
| Kanban | Continuous flow, support teams | Pull-based, WIP limits | Continuous |
| SAFe | Large enterprise, multiple teams | Scaled agile framework | PI planning (8-12 weeks) |
| Waterfall | Fixed scope, regulatory projects | Sequential phases | Milestone-based |
| Lean | Process improvement, startups | Build-Measure-Learn | Rapid iterations |
| PRINCE2 | Governance-heavy, government | Controlled stages | Stage gates |
| Hybrid | Most real-world projects | Mix of agile + planned | Flexible |

### Agile Ceremonies

| Ceremony | Purpose | Duration | Frequency |
|---|---|---|---|
| Sprint Planning | Define sprint goals and backlog | 2-4 hours | Every sprint |
| Daily Standup | Sync, blockers, coordination | 15 min | Daily |
| Sprint Review | Demo completed work | 1-2 hours | End of sprint |
| Retrospective | Process improvement | 1-1.5 hours | End of sprint |
| Backlog Refinement | Clarify and estimate stories | 1-2 hours | Mid-sprint |

---

## 2. Planning and Execution

### Project Planning Framework

| Phase | Activities | Outputs |
|---|---|---|
| Initiation | Charter, stakeholders, objectives | Project charter |
| Planning | Scope, schedule, resources, risks | Project plan |
| Execution | Deliver work, manage team | Deliverables |
| Monitoring | Track progress, manage changes | Status reports |
| Closing | Handoff, lessons learned, celebration | Final report |

### Work Breakdown Structure (WBS)

```
Project
├── Phase 1: Discovery
│   ├── Requirements gathering
│   ├── Stakeholder interviews
│   └── Current state analysis
├── Phase 2: Design
│   ├── Solution architecture
│   ├── UX design
│   └── Technical design
├── Phase 3: Build
│   ├── Sprint 1: Core features
│   ├── Sprint 2: Integration
│   └── Sprint 3: Polish
├── Phase 4: Launch
│   ├── Testing
│   ├── Migration
│   └── Go-live
└── Phase 5: Stabilize
    ├── Monitoring
    ├── Bug fixes
    └── Handoff
```

### Status Report Template

| Section | Content |
|---|---|
| Summary | One-line project health (Green/Yellow/Red) |
| Progress | What was accomplished this period |
| Next steps | What's planned for next period |
| Risks/Issues | Top 3 risks or blockers |
| Decisions needed | Items requiring stakeholder input |
| Metrics | Key project metrics (velocity, burn-down) |

---

## 3. Risk Management

### Risk Assessment Matrix

| Likelihood / Impact | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| High Likelihood | Medium | High | Critical |
| Medium Likelihood | Low | Medium | High |
| Low Likelihood | Low | Low | Medium |

### Risk Register Template

| ID | Risk | Likelihood | Impact | Score | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R1 | Key engineer leaves | Medium | High | High | Cross-train, document | PM | Active |
| R2 | API dependency delayed | High | Medium | High | Build mock, parallel path | Tech Lead | Active |
| R3 | Scope creep | High | High | Critical | Change control, backlog | PM | Monitoring |

### Risk Response Strategies

| Strategy | Description | When to Use |
|---|---|---|
| Avoid | Eliminate the risk entirely | High impact, can change approach |
| Mitigate | Reduce likelihood or impact | Most common response |
| Transfer | Shift risk to third party | Insurance, outsourcing |
| Accept | Acknowledge and monitor | Low impact, low likelihood |
| Escalate | Raise to higher authority | Beyond project team's control |

---

## 4. Stakeholder Management

### Stakeholder Matrix

| Influence / Interest | Low Interest | High Interest |
|---|---|---|
| High Influence | Keep satisfied | Manage closely |
| Low Influence | Monitor | Keep informed |

### Communication Plan

| Stakeholder | Information Need | Channel | Frequency |
|---|---|---|---|
| Executive sponsor | High-level progress, risks | 1:1, email | Bi-weekly |
| Steering committee | Decisions, status | Meeting | Monthly |
| Project team | Tasks, blockers, coordination | Standup, Slack | Daily |
| End users | Timeline, changes, training | Email, demos | As needed |
| External partners | Integration, dependencies | Meeting, email | Weekly |

---

## 5. Program Management

### Program vs Project

| Aspect | Project | Program |
|---|---|---|
| Scope | Single deliverable | Multiple related projects |
| Duration | Defined end date | Ongoing or multi-year |
| Goal | Specific output | Strategic outcome |
| Manager | Project Manager | Program Manager |
| Dependencies | Internal | Cross-project |
| Governance | Project board | Program board |

### Program Governance

| Level | Body | Responsibility | Cadence |
|---|---|---|---|
| Strategic | Steering Committee | Direction, funding, priorities | Monthly |
| Tactical | Program Board | Cross-project coordination | Bi-weekly |
| Operational | Project Teams | Delivery execution | Daily/Weekly |

### Dependency Management

| Type | Description | Management Approach |
|---|---|---|
| Finish-to-Start | B can't start until A finishes | Critical path analysis |
| Resource | Same person needed by multiple projects | Resource leveling |
| Technical | System A needed by System B | Integration planning |
| External | Third-party delivery | Contract, buffer time |
| Organizational | Approval or decision needed | Escalation path |
