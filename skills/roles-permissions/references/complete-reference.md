# Roles & Permissions Advanced Reference

**Verified against upstream:** 2026-08-07

## 1. Foundations: Understanding Roles, Permissions, and Access Control Models

### 1.1 Role-Based Access Control (RBAC)
Role-Based Access Control (RBAC) associates permissions with roles rather than directly with users. Users are assigned roles based on their job functions, and these roles aggregate permissions necessary to perform specific operations on resources.

### 1.2 Attribute-Based Access Control (ABAC)
To address RBAC limitations (role explosion), OWASP and NIST SP 800-162 recommend augmenting or replacing it with ABAC. ABAC bases access decisions on attributes of subjects, objects, and environment conditions.

### 1.3 Relationship-Based Access Control (ReBAC)
ReBAC considers relationships between entities, enabling richer, context-aware policies (e.g., a user can access documents they own or that belong to their department). Google Zanzibar is the industry standard for ReBAC.

## 2. Apache Casbin: Advanced RBAC with Resource Roles, Domains, and Implicit Roles

Apache Casbin is a powerful access control library supporting multiple models and languages. Its architecture cleanly separates the **model** (authorization logic) from the **policy** (rules).

### 2.1 RBAC Model with Resource Roles and Domains
Casbin extends classical RBAC by supporting resource roles and domains (tenants). In this model, both users and resources can have roles, and permissions may be scoped within domains.

### 2.2 Model Definition Example: RBAC with Domains and Resource Roles
```ini
[request_definition]
r = sub, dom, obj, act

[policy_definition]
p = sub, dom, obj, act, eft

[role_definition]
g = _, _, _               # user-role-domain (user, role, domain)
g2 = _, _, _              # resource-role-domain (resource, role, domain)

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub, r.dom) && g2(r.obj, p.obj, r.dom) && r.act == p.act
```

## 3. Casdoor: UI-First IAM and Integration with Casbin

Casdoor is an open-source Identity and Access Management (IAM) system designed with a UI-first philosophy. It provides end-to-end user lifecycle management, SSO, and multi-protocol support, integrating tightly with Casbin for authorization.

## 4. Preventing Broken Access Control: OWASP Best Practices

Broken Access Control ranks as the top security risk in the OWASP Top 10 (2025).

### 4.1 Deny by Default and Least Privilege
Authorization should default to denying access unless explicitly granted. Users receive only the minimal permissions necessary for their roles.

### 4.2 Server-Side Enforcement and Logging
Access control checks must be performed exclusively on the server side. Every authorization failure should be logged with detailed context.

### 4.3 IDOR Prevention
APIs should enforce resource ownership checks or relationship-based access (ReBAC). Object identifiers should be non-predictable (e.g., UUIDs).

## 5. Enterprise-Grade Authorization API Design

### 5.1 Centralized Enforcement Point
Authorization logic should be concentrated in a dedicated service or middleware layer.

### 5.2 Model-Policy Architecture
Casbin’s separation of model and policy files facilitates flexibility.

## 6. Advanced Concepts: Separation of Duties and Cardinality Constraints

### 6.1 Separation of Duties (SoD)
SoD enforces that conflicting duties are not assigned to the same user.

### 6.2 Cardinality Constraints
Cardinality constraints limit the number of users assigned to a role or the number of roles a user can hold.

## 7. Managing Complex Authorization Scenarios with Casbin and Casdoor

### 7.1 Multi-Tenancy and Domain Scoping
Casbin’s domain support allows policies and role mappings to be tenant-aware.

## 8. Preventing Role Explosion: ABAC and ReBAC Integration

### 8.1 ABAC for Attribute-Aware Access Control
Casbin supports ABAC by allowing arbitrary attributes in the request and policy definitions.

### 8.2 ReBAC for Relationship-Based Access Control
Casbin can encode relationships in role definitions or policies, enabling dynamic access control decisions based on Google Zanzibar principles.

## 9. Source Map (Formerly Reading List)

- **Apache Casbin Documentation:** https://casbin.org/docs/overview/ (Use for Casbin model/policy syntax and API usage)
- **Casdoor Documentation:** https://casdoor.github.io/docs/overview/ (Use for IAM configuration and SSO integration)
- **OWASP Authorization Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html (Use for general authorization best practices)
- **NIST SP 800-162 (ABAC):** https://csrc.nist.gov/pubs/sp/800/162/upd2/final (Use for ABAC definitions and considerations)
- **OWASP Top 10: Broken Access Control (2025):** https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/ (Use for mitigating BAC and IDOR)
- **Google Zanzibar Paper:** https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/ (Use for ReBAC architecture and relationship traversal)
