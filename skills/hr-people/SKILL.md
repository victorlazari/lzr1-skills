---
name: hr-people
description: Comprehensive HR and people operations skill covering talent acquisition, people operations, organizational development, compensation and benefits, employee experience, and HR analytics. Use when designing hiring processes, building org structures, creating compensation frameworks, developing culture programs, or managing people operations.
---

# HR & People Operations

Expert-level HR covering talent acquisition, people operations, organizational development, compensation, employee experience, and HR analytics for technology companies.

## When to Use

- Designing hiring processes and job descriptions
- Building organizational structures and career frameworks
- Creating compensation and equity programs
- Developing culture and employee experience programs
- Managing performance review processes
- HR compliance and policy creation
- People analytics and workforce planning
- Onboarding and offboarding processes

## Workflow

1. **Understand the context** — What stage, size, culture, and people challenge?
2. **Select reference** — Choose the appropriate domain:
   - Hiring and recruiting → `references/talent-acquisition.md`
   - Org design and development → `references/org-development.md`
   - Compensation and equity → `references/compensation.md`
   - People ops and compliance → `references/people-ops.md`
3. **Research** — Benchmarks, best practices, legal requirements
4. **Design** — Create frameworks, processes, and policies
5. **Implement** — Roll out with communication and training
6. **Measure** — Track effectiveness, iterate

## Core Principles (All People Work)

- People-first: Treat employees as whole humans, not resources
- Fairness: Consistent, equitable treatment across the organization
- Transparency: Clear expectations, processes, and decisions
- Data-informed: Use metrics to identify issues and measure impact
- Legal compliance: Stay current with employment law
- Culture-aligned: All programs should reinforce desired culture
- Scalable: Design processes that work at 2x current size
- Manager-enabling: Equip managers to lead their teams effectively

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Recruiter/TA | Sourcing, interviewing, closing | `references/talent-acquisition.md` |
| HR Business Partner | Org design, performance, coaching | `references/org-development.md` |
| Compensation Analyst | Pay, equity, benefits | `references/compensation.md` |
| People Ops | Compliance, systems, processes | `references/people-ops.md` |
| L&D Specialist | Training, development, growth | `references/org-development.md` |

## Key References

- **Talent acquisition**: See `references/talent-acquisition.md` for hiring and recruiting.
- **Org development**: See `references/org-development.md` for structure and growth.
- **Compensation**: See `references/compensation.md` for pay, equity, and benefits.
- **People ops**: See `references/people-ops.md` for compliance and operations.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `hiring`, ... | **Hiring & Recruiting** | Hiring Specialist | `references/complete-reference.md` |
| `compensation`, ... | **Compensation** | Compensation Specialist | `references/complete-reference.md` |
| `org design`, ... | **Org Design** | Org Design Specialist | `references/complete-reference.md` |
| `culture`, ... | **Culture & Retention** | Culture Specialist | `references/complete-reference.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **People Strategy Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Catches where a compensation change conflicts with retention strategy. Ensures org design changes are feasible given the hiring plan timeline.
