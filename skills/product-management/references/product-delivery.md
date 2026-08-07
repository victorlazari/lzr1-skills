# Product Delivery

**Verified against upstream: 2026-08-07**

## Table of Contents
1. Product Requirements
2. Agile Execution
3. Technical Product Management
4. Launch Planning
5. Stakeholder Management

---

## 1. Product Requirements

### PRD Creation Procedure
1. Use the `templates/prd-template.md` to draft the PRD.
2. Ensure all sections are filled out, especially Goals, Success Metrics, and Requirements.
3. Validate the PRD using `scripts/validate-prd.py`.
4. Address any validation errors before proceeding to delivery planning.

### User Story Format

```
Standard: As a [user], I want to [action] so that [benefit].
Acceptance criteria:
  Given [context]
  When [action]
  Then [expected result]
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

### Definition of Done Checklist

- [ ] Code reviewed and approved
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] No known bugs
- [ ] Meets acceptance criteria
- [ ] Accessibility requirements met
- [ ] Performance within SLA
- [ ] API documentation updated
- [ ] User-facing documentation updated
- [ ] Release notes written
- [ ] Deployed to staging
- [ ] QA verified in staging
- [ ] Feature flag configured
- [ ] Monitoring/alerting in place

---

## 3. Technical Product Management

### API Product Management Checklist

- [ ] Developer experience (Documentation, SDKs, sandbox)
- [ ] Versioning (Breaking changes, deprecation policy)
- [ ] Rate limiting (Fair usage, tiers)
- [ ] Authentication (API keys, OAuth, security)
- [ ] Monitoring (Usage analytics, error rates)
- [ ] Pricing (Per-call, tiered, freemium)

---

## 4. Launch Planning

### Launch Checklist

- [ ] **Product:** Feature complete, QA passed, performance verified
- [ ] **Marketing:** Messaging, landing page, blog post, email
- [ ] **Sales:** Enablement materials, pricing, FAQ
- [ ] **Support:** Documentation, training, escalation path
- [ ] **Legal:** Terms updated, compliance verified
- [ ] **Engineering:** Monitoring, rollback plan, on-call
- [ ] **Analytics:** Tracking implemented, dashboards ready

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
