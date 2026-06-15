# Compliance & Governance

## Table of Contents
1. Compliance Frameworks
2. SOC 2
3. ISO 27001
4. PCI DSS
5. Privacy Regulations
6. Security Governance

---

## 1. Compliance Frameworks Overview

| Framework | Scope | Industry | Certification |
|---|---|---|---|
| SOC 2 | Service organizations | SaaS, Cloud | Type I/II report |
| ISO 27001 | Information security management | Any | Certified |
| PCI DSS | Payment card data | Financial, E-commerce | Validated |
| HIPAA | Protected health information | Healthcare | Self-assessed |
| GDPR | Personal data (EU residents) | Any (EU data) | Self-assessed |
| FedRAMP | US government cloud services | Government | Authorized |
| NIST CSF | Cybersecurity framework | Any (US focus) | Self-assessed |
| CIS Controls | Security best practices | Any | Self-assessed |

---

## 2. SOC 2

### Trust Service Criteria

| Criteria | Description | Key Controls |
|---|---|---|
| Security (Common) | Protection against unauthorized access | Firewalls, encryption, access control |
| Availability | System uptime and performance | Redundancy, DR, monitoring |
| Processing Integrity | Accurate, complete processing | Validation, reconciliation |
| Confidentiality | Protection of confidential info | Encryption, classification, DLP |
| Privacy | Personal information handling | Consent, retention, access rights |

### SOC 2 Type I vs Type II

| Aspect | Type I | Type II |
|---|---|---|
| Scope | Control design at a point in time | Control effectiveness over time |
| Duration | Single date | 6-12 month observation period |
| Value | Controls exist | Controls work consistently |
| Typical use | First audit, new companies | Ongoing compliance, enterprise sales |

### Common SOC 2 Controls

| Category | Control | Evidence |
|---|---|---|
| Access Control | Role-based access, MFA | IAM policies, MFA enrollment |
| Change Management | Code review, approval process | PR history, deployment logs |
| Monitoring | Security alerting, log review | Alert configurations, review records |
| Incident Response | Documented IR process | IR plan, incident records |
| Vendor Management | Third-party risk assessment | Vendor reviews, contracts |
| Data Protection | Encryption at rest and in transit | KMS configs, TLS certificates |
| Business Continuity | DR plan, backup testing | DR test results, RTO/RPO |

---

## 3. ISO 27001

### ISO 27001 Structure

| Clause | Requirement | Key Activities |
|---|---|---|
| 4 | Context of the organization | Scope, interested parties |
| 5 | Leadership | Policy, roles, commitment |
| 6 | Planning | Risk assessment, objectives |
| 7 | Support | Resources, competence, awareness |
| 8 | Operation | Risk treatment, controls |
| 9 | Performance evaluation | Monitoring, internal audit |
| 10 | Improvement | Nonconformity, continual improvement |

### Annex A Controls (ISO 27001:2022)

| Category | Controls | Examples |
|---|---|---|
| Organizational (37) | Policies, roles, threat intelligence | Information security policy |
| People (8) | Screening, awareness, termination | Security awareness training |
| Physical (14) | Perimeters, equipment, media | Secure areas, clear desk |
| Technological (34) | Access, crypto, network, development | MFA, encryption, secure SDLC |

---

## 4. PCI DSS

### PCI DSS v4.0 Requirements

| Requirement | Description | Key Controls |
|---|---|---|
| 1 | Network security controls | Firewalls, segmentation |
| 2 | Secure configurations | Hardening, no defaults |
| 3 | Protect stored account data | Encryption, tokenization, masking |
| 4 | Protect data in transit | TLS 1.2+, no weak ciphers |
| 5 | Protect from malicious software | Anti-malware, vulnerability management |
| 6 | Develop secure systems | Secure SDLC, code review |
| 7 | Restrict access | Need-to-know, least privilege |
| 8 | Identify and authenticate | Strong auth, MFA |
| 9 | Restrict physical access | Physical security controls |
| 10 | Log and monitor | Audit trails, log review |
| 11 | Test security regularly | Vulnerability scans, pen tests |
| 12 | Information security policy | Policies, risk assessment |

### PCI Scope Reduction

| Strategy | Description | Benefit |
|---|---|---|
| Tokenization | Replace card data with tokens | Remove systems from scope |
| Network segmentation | Isolate cardholder data environment | Reduce scope boundary |
| P2PE | Point-to-point encryption | Remove merchant systems from scope |
| Third-party processing | Use PCI-compliant processor | Transfer scope to processor |

---

## 5. Privacy Regulations

### GDPR Key Requirements

| Principle | Description | Implementation |
|---|---|---|
| Lawfulness | Legal basis for processing | Consent, contract, legitimate interest |
| Purpose limitation | Specific, explicit purposes | Privacy policy, data mapping |
| Data minimization | Only necessary data | Review data collection |
| Accuracy | Keep data correct | Update mechanisms |
| Storage limitation | Don't keep longer than needed | Retention policies, auto-deletion |
| Integrity/Confidentiality | Protect data appropriately | Encryption, access control |
| Accountability | Demonstrate compliance | Records, DPIAs, audits |

### Data Subject Rights

| Right | Description | Response Time |
|---|---|---|
| Access | Obtain copy of personal data | 30 days |
| Rectification | Correct inaccurate data | 30 days |
| Erasure | Delete personal data | 30 days |
| Portability | Receive data in machine-readable format | 30 days |
| Restriction | Limit processing | 30 days |
| Object | Object to processing | 30 days |

---

## 6. Security Governance

### Security Program Components

| Component | Purpose | Cadence |
|---|---|---|
| Security policy | Define security requirements | Annual review |
| Risk assessment | Identify and prioritize risks | Annual + trigger-based |
| Security awareness | Train all employees | Annual + onboarding |
| Vulnerability management | Find and fix vulnerabilities | Continuous |
| Incident response | Handle security incidents | Continuous + annual test |
| Third-party risk | Assess vendor security | Per vendor + annual review |
| Business continuity | Ensure service continuity | Annual test |
| Access review | Verify access appropriateness | Quarterly |

### Risk Assessment Framework

```
Risk = Likelihood × Impact

Likelihood: 1 (Rare) → 5 (Almost Certain)
Impact: 1 (Negligible) → 5 (Catastrophic)

Risk Rating:
- 1-5: Low (Accept or Monitor)
- 6-12: Medium (Mitigate within quarter)
- 13-19: High (Mitigate within month)
- 20-25: Critical (Immediate action required)
```
