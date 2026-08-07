---
name: roles-permissions
description: Advanced roles, permissions, and access control management using Casbin, Casdoor, ABAC, ReBAC, and OWASP best practices.
---

# Roles & Permissions Advanced Skill

## Scope and Triggers

Use this skill when you need to design, implement, audit, or troubleshoot access control systems. This includes:
- Designing Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), or Relationship-Based Access Control (ReBAC) models.
- Implementing authorization using Apache Casbin and Casdoor.
- Managing multi-tenant authorization architectures (domains).
- Preventing Broken Access Control, Insecure Direct Object References (IDOR), and privilege escalation.
- Enforcing Separation of Duties (SoD) and cardinality constraints.
- Designing enterprise-grade authorization APIs.

**Cross-Skill Routing:**
- `security-review` — Route when performing a comprehensive application security audit beyond just access control.
- `trivy-scanner` — Route when scanning container images or infrastructure for vulnerabilities.

## Preconditions

Before acting, detect the target environment, versions, permissions, inputs, constraints, and user intent.
- Verify the target application's current access control model.
- Identify the authorization layer (API, Database, Audit, ABAC, ReBAC).

## Source Freshness

Volatile facts, such as specific OWASP Top 10 rankings, must be verified against current upstream documentation.
- **Verified against upstream:** 2026-08-07
- Check current OWASP guidelines, NIST SP 800-162, and Apache Casbin/Casdoor documentation.

## Workflow

1. **Analyze Requirements:** Determine the appropriate access control model (RBAC, ABAC, ReBAC) based on organizational structure, multi-tenancy needs, and resource complexity.
2. **Design Model:** Define the authorization model using Casbin, incorporating domain isolation and resource roles as needed. Use `templates/casbin-rebac-model.conf` for ReBAC.
3. **Define Policies:** Create specific policy rules mapping users to roles and roles to permissions.
4. **Implement Enforcement:** Integrate the authorization engine (e.g., Casbin enforcer) into the application's API or middleware layer.
5. **Configure IAM:** Set up the Identity and Access Management system (e.g., Casdoor) for user lifecycle management and SSO.
6. **Validate Policies:** Validate policies using `scripts/validate-policies.sh` to detect conflicts or misconfigurations.
7. **Audit & Test:** Audit the implementation against OWASP best practices and NIST standards.
8. **Stop Condition:** Stop when all policies are validated, enforcement is confirmed, and no actionable security findings remain.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- Do not download or execute untrusted artifacts.

## Validation

- Run safe local syntax checks on files created (`bash -n`, Python compilation, JSON/YAML parsing).
- Use `scripts/validate-policies.sh` to validate Casbin policies.
- Ensure API endpoints enforce authorization checks before processing requests.
- Log authorization failures with detailed context.

## Failure Handling

- If validation fails, diagnose errors using the output of `scripts/validate-policies.sh`.
- Do not repeat a failed action unchanged.
- Roll back changes if a destructive action fails or causes unintended consequences.

## Output Contract

The result must include:
- A structured summary of the access control model designed or audited.
- Evidence of policy validation (e.g., output from `validate-policies.sh`).
- Actionable next steps for any remaining security findings.

## Resources

- [Complete Reference](./references/complete-reference.md): Comprehensive guide on RBAC, ABAC, ReBAC, Casbin, Casdoor, and OWASP best practices.
- [Casbin ReBAC Model Template](./templates/casbin-rebac-model.conf): A template for a Zanzibar-inspired ReBAC model in Casbin.
- [Validate Policies Script](./scripts/validate-policies.sh): A script to automatically validate Casbin policies against common misconfigurations.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple microservices to audit | Security Auditor | Parallel access control review of each service |
| Multiple Casbin models to validate | Policy Validator | Parallel schema and policy validation |
| Multiple tenants/domains to check | Tenant Auditor | Parallel domain isolation verification |
| Bulk permission troubleshooting | Diagnostics Agent | Parallel issue investigation for multiple users |

### Spawning Rules
- Spawn when 3+ independent items (services, models, tenants, users) need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Multi-Specialist Protocol

When multiple authorization domains are involved, spawn all relevant specialists simultaneously.

| Task Signal (examples) | Domain | Specialist Agent | Reference (Focus Section) |
|---|---|---|---|
| `endpoint`, `middleware`, `JWT`, `OAuth`, `API gateway`, `authorization header`, `Casbin enforcer`, `RBAC middleware`, `HTTP policy` | **API-Level Authorization** | API Auth Specialist | `references/complete-reference.md` (API enforcement, Casbin policy, RBAC/ABAC at the request layer) |
| `database`, `row-level security`, `RLS`, `PostgreSQL policy`, `column permission`, `schema permission`, `database role`, `tenant isolation` | **Database-Level Policies** | DB Policy Specialist | `references/complete-reference.md` (DB-level enforcement, RLS rules, multi-tenant schema isolation) |
| `audit log`, `access event`, `authorization failure`, `SIEM`, `compliance trail`, `SOC2`, `who accessed what`, `access history` | **Audit & Compliance Logging** | Audit Trail Specialist | `references/complete-reference.md` (logging requirements, audit event schema, compliance mapping) |
| `ABAC`, `attribute`, `context-aware`, `dynamic policy`, `resource attribute`, `environmental condition` | **Attribute-Based Access Control** | ABAC Specialist | `references/complete-reference.md` (ABAC model design, attribute sources, policy evaluation) |
| `ReBAC`, `relationship`, `Zanzibar`, `graph permission`, `owner`, `member`, `viewer`, `fine-grained` | **Relationship-Based Access Control** | ReBAC Specialist | `references/complete-reference.md` (ReBAC model, Casbin g2 rules, relationship traversal) |

**Cross-Domain Synthesizer:**
After all specialists complete, run one **Privilege Architecture Synthesizer** with all outputs to identify contradictions, privilege escalation paths, map ABAC/ReBAC to enforcement, and verify audit completeness.
