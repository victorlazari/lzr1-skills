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
