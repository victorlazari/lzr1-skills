# Identity & Access Management

## Table of Contents
1. Identity Providers
2. SSO Configuration
3. SCIM Provisioning
4. Access Control
5. Zero Trust Architecture

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

## 5. Zero Trust Architecture

### Zero Trust Principles

| Principle | Description | Implementation |
|---|---|---|
| Verify explicitly | Always authenticate and authorize | SSO + MFA everywhere |
| Least privilege | Minimum access needed | RBAC, JIT access |
| Assume breach | Minimize blast radius | Segmentation, monitoring |
| Never trust network | Network location doesn't grant trust | Identity-based access |
| Continuous verification | Re-verify throughout session | Device posture, risk signals |

### Zero Trust Implementation

| Layer | Traditional | Zero Trust |
|---|---|---|
| Network | VPN, firewall perimeter | Identity-aware proxy, micro-segmentation |
| Identity | Username/password | MFA, continuous auth, risk-based |
| Device | Corporate network = trusted | Device posture check, MDM compliance |
| Application | Network access = app access | Per-app authorization |
| Data | Perimeter protection | Classification, DLP, encryption |
