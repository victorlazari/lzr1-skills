# Identity & Access Management

Verified against upstream: 2026-08-07

## Table of Contents
1. Identity Providers
2. SSO Configuration
3. SCIM Provisioning
4. Access Control
5. Zero Trust Architecture (CISA ZTMM V2.0)
6. Source Map

---

## 1. Identity Providers

### IdP Comparison

| Provider | Best For | Key Features |
|---|---|---|
| Okta | Enterprise, large orgs | Extensive integrations, lifecycle |
| Google Workspace | Google-first companies | Built-in, simple |
| Microsoft Entra ID | Microsoft ecosystem | Azure integration, hybrid |
| OneLogin | Mid-market | Simple, cost-effective |
| JumpCloud | Cross-platform, remote | Directory + MDM |
| Auth0 (Okta) | Customer identity (CIAM) | Developer-friendly |

### IdP Architecture

```
Users → Identity Provider (Okta/Google/Entra)
         ↓ SSO (SAML/OIDC)
         ↓ SCIM (Provisioning)
         ↓ MFA (Push/TOTP/WebAuthn)
         → SaaS Applications
         → Internal Applications
         → Infrastructure (AWS/GCP/Azure)
```

---

## 2. SSO Configuration

### SSO Protocols

| Protocol | Description | Use Case |
|---|---|---|
| SAML 2.0 | XML-based, enterprise standard | Enterprise SaaS apps |
| OIDC | OAuth 2.0 + identity layer | Modern apps, APIs |
| OAuth 2.0 | Authorization (not authentication) | API access |
| LDAP | Directory protocol | Legacy/on-prem apps |
| WS-Federation | Microsoft legacy | Older Microsoft apps |

### SSO Implementation Checklist

```
For each application:
□ Determine supported protocol (SAML/OIDC)
□ Configure in IdP (metadata, endpoints)
□ Configure in application (IdP metadata)
□ Map attributes (email, name, groups)
□ Configure group-based access
□ Test with pilot users
□ Enable for all users
□ Disable local authentication
□ Document configuration
□ Set up monitoring/alerting
```

---

## 3. SCIM Provisioning

### SCIM (System for Cross-domain Identity Management)

| Operation | Description | Trigger |
|---|---|---|
| Create | Provision new user account | User joins, assigned app |
| Update | Sync attribute changes | Profile update in IdP |
| Deactivate | Disable user account | User leaves, unassigned |
| Delete | Remove user account | Per retention policy |
| Group sync | Sync group membership | Group change in IdP |

### Provisioning Strategy

| Approach | Description | Best For |
|---|---|---|
| SCIM | Real-time API provisioning | Apps that support SCIM |
| JIT (Just-in-Time) | Create on first login | Apps without SCIM |
| Manual | Admin creates accounts | Legacy apps |
| API | Custom integration | Apps with API but no SCIM |
| CSV/Batch | Periodic bulk sync | Legacy systems |

---

## 4. Access Control

### RBAC (Role-Based Access Control)

| Component | Description | Example |
|---|---|---|
| User | Individual person | jane@company.com |
| Role | Collection of permissions | "Engineer", "Manager" |
| Permission | Specific action allowed | "Read repository" |
| Resource | What's being accessed | "Production database" |
| Group | Collection of users | "Engineering team" |

### Access Review Process

| Step | Activity | Frequency |
|---|---|---|
| 1 | Generate access report per application | Quarterly |
| 2 | Send to application owners for review | Quarterly |
| 3 | Owners confirm or revoke access | 2-week window |
| 4 | Remove unconfirmed access | After window |
| 5 | Document decisions and exceptions | Quarterly |
| 6 | Report to compliance/audit | Quarterly |

### Privileged Access Management

| Principle | Implementation |
|---|---|
| Just-in-time access | Request elevated access when needed, auto-expire |
| Break-glass procedures | Emergency access with audit trail |
| Session recording | Record privileged sessions |
| Approval workflows | Manager/security approval for sensitive access |
| Credential rotation | Automated rotation of service accounts |

---

## 5. Zero Trust Architecture (CISA ZTMM V2.0)

### Zero Trust Principles

| Principle | Description | Implementation |
|---|---|---|
| Verify explicitly | Always authenticate and authorize | SSO + MFA everywhere |
| Least privilege | Minimum access needed | RBAC, JIT access |
| Assume breach | Minimize blast radius | Segmentation, monitoring |
| Never trust network | Network location doesn't grant trust | Identity-based access |
| Continuous verification | Re-verify throughout session | Device posture, risk signals |

### Zero Trust Implementation (CISA ZTMM V2.0 Alignment)

| Pillar | Traditional | Advanced (Zero Trust) |
|---|---|---|
| Identity | Password-based | Phishing-resistant MFA, continuous validation |
| Devices | Managed vs Unmanaged | Device health/posture checks before access |
| Networks | Perimeter-based | Micro-segmentation, encrypted traffic |
| Applications | Static access | Dynamic, risk-based access control |
| Data | Perimeter protection | Data categorization, encryption, DLP |

---

## 6. Source Map

- **CISA Zero Trust Maturity Model V2.0**: https://www.cisa.gov/zero-trust-maturity-model
- **Identity Attack Vectors**: Haber & Hibbert (2020), Apress. IAM security.
- **Solving Identity Management in Modern Applications**: Hardt (2nd ed, 2022), Apress.
- **OAuth 2 in Action**: Richer & Sanso (2017), Manning.
- **Identity and Data Security for Web Development**: LeBlanc & Messerschmidt (2016), O'Reilly.
- **Zero Trust Networks**: Gilman & Barth (2nd ed, 2024), O'Reilly.
- **Okta Blog**: okta.com/blog. Identity management.
- **Auth0 Blog**: auth0.com/blog. Authentication and identity.
- **Microsoft Entra Blog**: techcommunity.microsoft.com. Azure AD/Entra.
- **JumpCloud Blog**: jumpcloud.com/blog. Directory and IAM.
