---
name: it-administration
description: Comprehensive IT administration skill covering endpoint management, identity and access management, IT security, SaaS administration, and IT operations for technology companies. Use when managing IT infrastructure, configuring identity providers, administering SaaS tools, handling IT security, or building IT policies and procedures.
---

# IT Administration

Expert-level IT administration covering endpoint management, identity and access management, IT security, SaaS administration, and IT operations for technology companies.

## When to Use

- Managing endpoints (laptops, devices, MDM)
- Configuring identity and access management (SSO, SCIM)
- Administering SaaS tools and licenses
- IT security hardening and compliance
- IT onboarding and offboarding automation
- Network and infrastructure management
- IT policy development and enforcement
- Helpdesk and IT support operations

## Workflow

1. **Understand the context** — What IT challenge, environment, and scale?
2. **Select reference** — Choose the appropriate domain:
   - Endpoint and device management → `references/endpoint-management.md`
   - Identity and access management → `references/identity-access.md`
   - IT security and compliance → `references/it-security.md`
3. **Assess** — Current state, gaps, risks
4. **Plan** — Solution design, migration path
5. **Implement** — Configure, test, deploy
6. **Operate** — Monitor, maintain, optimize

## Core Principles (All IT Work)

- Security-first: Every decision considers security impact
- Zero trust: Never trust, always verify
- Automated: Automate provisioning, deprovisioning, compliance
- Documented: Runbooks for every process
- Least privilege: Minimum access needed for the job
- Scalable: Solutions that work at 10x headcount
- User experience: Security shouldn't impede productivity
- Compliant: Meet regulatory and audit requirements

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| IT Administrator | Endpoints, SaaS, helpdesk | `references/endpoint-management.md` |
| IT Security Admin | Hardening, compliance, monitoring | `references/it-security.md` |
| Identity Admin | SSO, SCIM, access management | `references/identity-access.md` |

## Key References

- **Endpoint management**: See `references/endpoint-management.md` for devices and MDM.
- **Identity and access**: See `references/identity-access.md` for SSO and provisioning.
- **IT security**: See `references/it-security.md` for hardening and compliance.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `identity`, ... | **Identity & Access** | Identity Specialist | `references/complete-reference.md` |
| `network`, ... | **Network Administration** | Network Specialist | `references/complete-reference.md` |
| `endpoint`, ... | **Endpoint Management** | Endpoint Specialist | `references/complete-reference.md` |
| `compliance`, ... | **IT Compliance** | Compliance Specialist | `references/complete-reference.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **IT Change Risk Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Ensures a firewall change does not break an identity policy or trigger a compliance audit flag. Maps endpoint management policies to network access control implications.
