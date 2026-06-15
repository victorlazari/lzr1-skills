# Product Delivery

## Table of Contents
1. Product Requirements
2. Agile Execution
3. Technical Product Management
4. Launch Planning
5. Stakeholder Management

---

## 1. Product Requirements

### PRD Template

```markdown
# [Feature Name] PRD

## Overview
One-paragraph summary of what we're building and why.

## Problem Statement
What problem are we solving? For whom? Evidence of the problem.

## Goals and Success Metrics
| Metric | Current | Target | Timeframe |
|---|---|---|---|
| [Primary metric] | X | Y | Z weeks post-launch |

## User Stories
As a [user type], I want to [action] so that [benefit].

## Requirements
### Must Have (P0)
- [Requirement with acceptance criteria]

### Should Have (P1)
- [Requirement]

### Nice to Have (P2)
- [Requirement]

## Design
Link to designs/prototypes.

## Technical Considerations
Architecture decisions, constraints, dependencies.

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## Timeline
| Milestone | Date | Dependencies |
|---|---|---|---|

## Open Questions
- [Question needing resolution]
```

### User Story Format

```
Standard: As a [user], I want to [action] so that [benefit].
Acceptance criteria:
  Given [context]
  When [action]
  Then [expected result]

Example:
As a team admin, I want to invite members via email
so that I can onboard my team quickly.

Acceptance criteria:
  Given I am on the team settings page
  When I enter a valid email and click "Invite"
  Then the user receives an invitation email within 5 minutes
  And they appear in the pending invitations list
```

---

## 2. Agile Execution

### Sprint Ceremonies

| Ceremony | Purpose | Duration | Frequency |
|---|---|---|---|
| Sprint Planning | Commit to sprint work | 1-2 hours | Start of sprint |
| Daily Standup | Sync, unblock | 15 minutes | Daily |
| Sprint Review | Demo to stakeholders | 1 hour | End of sprint |
| Retrospective | Improve process | 1 hour | End of sprint |
| Backlog Refinement | Clarify upcoming work | 1 hour | Mid-sprint |

### Estimation Approaches

| Method | Scale | Best For |
|---|---|---|
| Story points | Fibonacci (1,2,3,5,8,13) | Relative complexity |
| T-shirt sizing | XS, S, M, L, XL | Quick estimation |
| Time-based | Hours/days | Predictable work |
| No estimates | Just count stories | High-trust teams |

### Definition of Done

```
Code:
  ☐ Code reviewed and approved
  ☐ Unit tests written and passing
  ☐ Integration tests passing
  ☐ No known bugs

Quality:
  ☐ Meets acceptance criteria
  ☐ Accessibility requirements met
  ☐ Performance within SLA

Documentation:
  ☐ API documentation updated
  ☐ User-facing documentation updated
  ☐ Release notes written

Deployment:
  ☐ Deployed to staging
  ☐ QA verified in staging
  ☐ Feature flag configured
  ☐ Monitoring/alerting in place
```

---

## 3. Technical Product Management

### API Product Management

| Aspect | Consideration |
|---|---|
| Developer experience | Documentation, SDKs, sandbox |
| Versioning | Breaking changes, deprecation policy |
| Rate limiting | Fair usage, tiers |
| Authentication | API keys, OAuth, security |
| Monitoring | Usage analytics, error rates |
| Pricing | Per-call, tiered, freemium |

### Platform Product Management

| Principle | Description |
|---|---|
| Self-service | Users can accomplish goals without support |
| Extensibility | Platform can be extended without core changes |
| Backward compatibility | Don't break existing integrations |
| Documentation-first | Docs are the product for platforms |
| Dogfooding | Use your own platform internally |
| Ecosystem thinking | Enable third-party value creation |

---

## 4. Launch Planning

### Launch Checklist

| Category | Items |
|---|---|
| Product | Feature complete, QA passed, performance verified |
| Marketing | Messaging, landing page, blog post, email |
| Sales | Enablement materials, pricing, FAQ |
| Support | Documentation, training, escalation path |
| Legal | Terms updated, compliance verified |
| Engineering | Monitoring, rollback plan, on-call |
| Analytics | Tracking implemented, dashboards ready |

### Launch Tiers

| Tier | Scope | Activities |
|---|---|---|
| Tier 1 (Major) | New product, major feature | Full marketing, PR, event |
| Tier 2 (Medium) | Significant feature | Blog post, email, in-app |
| Tier 3 (Minor) | Improvement, fix | Changelog, in-app notification |

### Feature Flags Strategy

| Stage | Flag State | Audience |
|---|---|---|
| Development | Off | Developers only |
| Internal testing | On for internal | Employees |
| Beta | On for beta users | Opt-in users |
| Gradual rollout | % of users | 5% → 25% → 50% → 100% |
| GA | On for all | Everyone |
| Cleanup | Remove flag | N/A |

---

## 5. Stakeholder Management

### RACI Matrix

| Role | Description | Involvement |
|---|---|---|
| Responsible | Does the work | Active, hands-on |
| Accountable | Final decision maker | Approves, one per decision |
| Consulted | Provides input | Two-way communication |
| Informed | Kept in the loop | One-way communication |

### Communication Cadence

| Audience | Format | Frequency | Content |
|---|---|---|---|
| Engineering team | Standup, planning | Daily/weekly | Priorities, blockers |
| Design team | Sync, review | 2-3x/week | Requirements, feedback |
| Leadership | Status update | Weekly/biweekly | Progress, risks, decisions |
| Stakeholders | Review meeting | Biweekly/monthly | Demos, roadmap updates |
| Customers | Release notes | Per release | What's new, what's next |

### Saying No Effectively

| Approach | When to Use | Example |
|---|---|---|
| "Not now" | Valid but lower priority | "Great idea — let's revisit in Q3" |
| "Instead of" | Redirect to better solution | "Instead of X, what if we did Y?" |
| "Help me understand" | Need more context | "Help me understand the problem behind this request" |
| "Here's the trade-off" | Make cost visible | "We can do this, but it means delaying Z" |
| "Let's test first" | Unvalidated assumption | "Let's validate demand before building" |
