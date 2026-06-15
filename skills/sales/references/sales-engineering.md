# Sales Engineering

## Table of Contents
1. Technical Discovery
2. Demos and Presentations
3. Proof of Concept (POC)
4. Technical Objection Handling
5. Solution Architecture

---

## 1. Technical Discovery

### Technical Discovery Framework

| Area | Questions | Goal |
|---|---|---|
| Current architecture | What's your current stack? Integrations? | Understand technical landscape |
| Pain points | What breaks? What's slow? What's manual? | Identify technical pain |
| Requirements | Must-have vs nice-to-have capabilities? | Scope the solution |
| Constraints | Security, compliance, performance needs? | Identify blockers early |
| Evaluation criteria | How will you evaluate technically? | Align demo/POC |
| Decision process | Who's involved technically? | Map technical stakeholders |
| Timeline | Implementation timeline and resources? | Set realistic expectations |

### Technical Stakeholder Map

| Stakeholder | Concerns | How to Win |
|---|---|---|
| CTO/VP Engineering | Architecture, scalability, team impact | Strategic vision, roadmap |
| Engineering Manager | Implementation effort, team adoption | Easy integration, support |
| Individual Developer | API quality, docs, DX | Great docs, sandbox, SDKs |
| Security/Compliance | Data handling, certifications | SOC2, encryption, audit logs |
| IT/Ops | Deployment, monitoring, maintenance | SLA, support, operations |

---

## 2. Demos and Presentations

### Demo Structure

```
1. Recap and Agenda (2 min)
   - "Based on our discovery, you mentioned [pain points]..."
   - Set expectations for what you'll show

2. Before State (3 min)
   - Show the problem (their current painful workflow)
   - Build empathy and urgency

3. Solution Demo (15-20 min)
   - Show 3-4 key workflows that solve their pain
   - Use THEIR data/scenarios when possible
   - Pause for reactions and questions

4. Differentiation (5 min)
   - Show unique capabilities competitors lack
   - Connect to their specific requirements

5. Architecture/Integration (5 min)
   - How it fits their stack
   - Implementation approach

6. Q&A and Next Steps (5 min)
   - Address concerns
   - Propose POC or next step
```

### Demo Best Practices

| Practice | Description |
|---|---|
| Tell, Show, Tell | Explain what you'll show, show it, summarize what they saw |
| Use their language | Mirror their terminology, not yours |
| Pause for reactions | "How does that compare to what you do today?" |
| Handle the unexpected | If something breaks, acknowledge and move on |
| Personalize | Use their company name, data, scenarios |
| Focus on outcomes | "This saves your team 4 hours per week" not "Click here" |
| Leave breadcrumbs | Show enough to excite, not everything |

---

## 3. Proof of Concept (POC)

### POC Planning

| Component | Description | Owner |
|---|---|---|
| Success criteria | Measurable outcomes that define success | Joint (SE + customer) |
| Scope | What's included and excluded | SE |
| Timeline | Duration (typically 2-4 weeks) | Joint |
| Resources | Who's involved from both sides | Joint |
| Environment | Where it runs, data used | Customer + SE |
| Evaluation | How results will be measured | Joint |
| Decision | What happens after POC | AE + customer |

### POC Success Criteria Template

```markdown
## POC Success Criteria

### Must Pass (Required for success)
1. [Specific, measurable criterion] — Target: [number/outcome]
2. [Specific, measurable criterion] — Target: [number/outcome]
3. [Specific, measurable criterion] — Target: [number/outcome]

### Should Pass (Important but not blocking)
1. [Criterion] — Target: [number/outcome]
2. [Criterion] — Target: [number/outcome]

### Timeline
- Setup: [dates]
- Testing: [dates]
- Review: [date]

### Decision
If all "Must Pass" criteria are met, [customer] will proceed to [next step].
```

---

## 4. Technical Objection Handling

### Common Technical Objections

| Objection | Response Strategy |
|---|---|
| "Doesn't integrate with X" | Show API/webhook capabilities, discuss custom integration |
| "Not scalable enough" | Share architecture, benchmarks, customer examples at scale |
| "Security concerns" | SOC2, encryption, compliance certifications, security whitepaper |
| "We could build this ourselves" | Total cost of ownership, time-to-value, ongoing maintenance |
| "Too complex to implement" | Phased approach, professional services, time-to-value data |
| "Performance won't meet our needs" | Benchmarks, SLA guarantees, architecture discussion |
| "Vendor lock-in" | Data portability, open standards, export capabilities |

### Build vs Buy Analysis

| Factor | Build | Buy |
|---|---|---|
| Time to value | 6-18 months | 2-8 weeks |
| Upfront cost | Engineering time (expensive) | License fee |
| Ongoing cost | Maintenance, updates, on-call | Subscription |
| Customization | Unlimited | Within platform limits |
| Risk | Scope creep, key-person dependency | Vendor dependency |
| Opportunity cost | Engineers not building core product | Budget allocation |

---

## 5. Solution Architecture

### Integration Patterns

| Pattern | Description | Use Case |
|---|---|---|
| API (REST/GraphQL) | Direct programmatic access | Real-time data exchange |
| Webhooks | Event-driven notifications | Async updates |
| ETL/ELT | Batch data movement | Analytics, reporting |
| Native integration | Pre-built connectors | Common tools (Salesforce, Slack) |
| iPaaS | Integration platform (Zapier, Workato) | Non-technical users |
| SDK/Library | Embedded in their code | Developer-centric products |

### Architecture Diagram Components

```
Customer Environment:
  [Their App] ←→ [API/SDK] ←→ [Your Platform]
                                    ↓
                              [Data Store]
                                    ↓
                          [Analytics/Reporting]

Key considerations:
- Data residency (where data lives)
- Authentication (SSO, API keys, OAuth)
- Network (VPN, IP allowlisting, private link)
- High availability (SLA, failover)
- Disaster recovery (RPO, RTO)
```
