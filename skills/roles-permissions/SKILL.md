---
name: roles-permissions
description: Advanced roles, permissions, and access control management using Casbin, Casdoor, ABAC, ReBAC, and OWASP best practices.
---

# Roles & Permissions Advanced Skill

## When to Use

Use this skill when you need to design, implement, audit, or troubleshoot access control systems. This includes:
- Designing Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), or Relationship-Based Access Control (ReBAC) models.
- Implementing authorization using Apache Casbin and Casdoor.
- Managing multi-tenant authorization architectures (domains).
- Preventing Broken Access Control, Insecure Direct Object References (IDOR), and privilege escalation.
- Enforcing Separation of Duties (SoD) and cardinality constraints.
- Designing enterprise-grade authorization APIs.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple microservices to audit | Security Auditor | Parallel access control review of each service |
| Multiple Casbin models to validate | Policy Validator | Parallel schema and policy validation |
| Multiple tenants/domains to check | Tenant Checker | Parallel tenant isolation health checks |
| Bulk permission troubleshooting | Diagnostics Agent | Parallel issue investigation for multiple users |

### Spawning Rules
- Spawn when 3+ independent items (services, models, tenants, users) need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Analyze Requirements:** Determine the access control model needed (RBAC, ABAC, ReBAC) based on organizational structure, multi-tenancy needs, and resource complexity.
2. **Design Model:** Define the authorization model (e.g., Casbin model definition) including subjects, objects, actions, domains, and role hierarchies.
3. **Define Policies:** Create the specific policy rules that map users to roles and roles to permissions.
4. **Implement Enforcement:** Integrate the authorization engine (e.g., Casbin enforcer) into the application's API or middleware layer.
5. **Configure IAM:** Set up the Identity and Access Management system (e.g., Casdoor) for user lifecycle management and SSO.
6. **Audit & Test:** Verify policies against OWASP best practices, ensuring default deny, least privilege, and protection against IDOR and privilege escalation.
7. **Monitor & Refine:** Implement logging for authorization failures and refine policies to prevent role explosion using ABAC/ReBAC techniques.

## Core Principles

- **Deny by Default:** Authorization should default to denying access unless explicitly granted.
- **Least Privilege:** Users receive only the minimal permissions necessary for their roles.
- **Server-Side Enforcement:** Access control checks must be performed exclusively on the server side.
- **Separation of Duties (SoD):** Conflicting duties must not be assigned to the same user to prevent fraud or error.
- **Context-Awareness:** Use ABAC and ReBAC to make dynamic, fine-grained access decisions based on attributes and relationships, mitigating role explosion.
- **Centralized Enforcement:** Concentrate authorization logic in a dedicated service or middleware layer for uniform policy enforcement and auditing.

## Key References

- [Complete Reference](./references/complete-reference.md)
- [Reading List](./references/reading-list.md)

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple authorization domains are involved, spawn all relevant specialists simultaneously — do not serialize them.
>
> **Single-reference note:** This skill uses one comprehensive reference file (`references/complete-reference.md`). Each specialist receives the full reference but is scoped to a specific authorization layer — they analyze independently without sharing findings during their run.

### Domain Detection Table

Scan the task for signals that indicate which authorization layers apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference (Focus Section) |
|---|---|---|---|
| `endpoint`, `middleware`, `JWT`, `OAuth`, `API gateway`, `authorization header`, `Casbin enforcer`, `RBAC middleware`, `HTTP policy` | **API-Level Authorization** | API Auth Specialist | `references/complete-reference.md` (API enforcement, Casbin policy, RBAC/ABAC at the request layer) |
| `database`, `row-level security`, `RLS`, `PostgreSQL policy`, `column permission`, `schema permission`, `database role`, `tenant isolation` | **Database-Level Policies** | DB Policy Specialist | `references/complete-reference.md` (DB-level enforcement, RLS rules, multi-tenant schema isolation) |
| `audit log`, `access event`, `authorization failure`, `SIEM`, `compliance trail`, `SOC2`, `who accessed what`, `access history` | **Audit & Compliance Logging** | Audit Trail Specialist | `references/complete-reference.md` (logging requirements, audit event schema, compliance mapping) |
| `ABAC`, `attribute`, `context-aware`, `dynamic policy`, `resource attribute`, `environmental condition` | **Attribute-Based Access Control** | ABAC Specialist | `references/complete-reference.md` (ABAC model design, attribute sources, policy evaluation) |
| `ReBAC`, `relationship`, `Zanzibar`, `graph permission`, `owner`, `member`, `viewer`, `fine-grained` | **Relationship-Based Access Control** | ReBAC Specialist | `references/complete-reference.md` (ReBAC model, Casbin g2 rules, relationship traversal) |

### Spawning Logic

**Single domain detected** → Fall back to direct reference consultation (no spawning needed).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + the full `complete-reference.md` with instruction to focus only on its designated section
- No specialist waits for another — all start at the same time
- Maximum concurrent domain specialists: 5 (separate from the existing bulk sub-agent cap of 10 for multi-service operations)

### Cross-Domain Synthesizer

After all specialists complete, run one **Privilege Architecture Synthesizer** with all outputs that:

1. **Identifies contradictions** — e.g., the API Auth Specialist grants a role access to an endpoint while the DB Policy Specialist has an RLS rule blocking that same role from the underlying table
2. **Identifies privilege escalation paths** — where combining API permissions + DB permissions + a ReBAC relationship creates an unintended elevated access path
3. **Maps ABAC/ReBAC to enforcement** — ensures dynamic attribute or relationship decisions are enforced at both API and DB layers, not just one
4. **Verifies audit completeness** — confirms every permission boundary identified by API Auth, DB Policy, ABAC, and ReBAC specialists has a corresponding audit log event

> Synthesis focus for this skill: Catches RBAC/ABAC/ReBAC policy gaps where a Casbin rule at the API layer is not mirrored by an RLS policy at the database layer, leaving a direct-DB-access bypass. Ensures Casdoor identity attributes feeding ABAC decisions are correctly propagated to all enforcement points in a multi-tenant domain.
