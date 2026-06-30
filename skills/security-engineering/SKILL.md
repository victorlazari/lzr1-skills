---
name: security-engineering
description: Comprehensive cybersecurity skill covering application security (AppSec), cloud security, penetration testing, security architecture, DevSecOps, compliance frameworks, threat modeling, incident response, and identity/access management. Use when performing security reviews, designing secure systems, implementing security controls, conducting threat modeling, or responding to security incidents.
---

# Security Engineering

Expert-level cybersecurity covering the full security spectrum: application security, cloud security, penetration testing, security architecture, DevSecOps, compliance, threat modeling, incident response, and identity management.

## When to Use

- Security code review and vulnerability assessment
- Threat modeling and security architecture design
- Cloud security posture management
- Penetration testing and red team operations
- DevSecOps pipeline implementation
- Compliance frameworks (SOC 2, ISO 27001, PCI DSS, HIPAA)
- Incident response and forensics
- Identity and access management (IAM)
- Cryptography and data protection

## Workflow

1. **Understand the context** — What system, data classification, threat landscape?
2. **Select reference** — Choose the appropriate security domain:
   - Application security → `references/application-security.md`
   - Cloud security → `references/cloud-security.md`
   - Security architecture → `references/security-architecture.md`
   - DevSecOps → `references/devsecops.md`
   - Compliance and governance → `references/compliance.md`
3. **Assess threats** — Identify threat actors, attack vectors, and risk
4. **Design controls** — Implement defense-in-depth countermeasures
5. **Validate** — Test controls through review, scanning, or penetration testing
6. **Document** — Record findings, risks, and remediation guidance

## Core Principles (All Security Work)

- Defense in depth: Never rely on a single security control
- Least privilege: Minimum permissions for every entity
- Zero trust: Never trust, always verify (even internal traffic)
- Secure by default: Systems should be secure out of the box
- Fail securely: Failures should not expose data or bypass controls
- Assume breach: Design systems assuming attackers are already inside
- Shift left: Find and fix security issues as early as possible
- Measure and monitor: Continuous security posture assessment

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Security Engineer | AppSec, code review, SAST/DAST | `references/application-security.md` |
| Cloud Security Engineer | Cloud posture, IAM, network security | `references/cloud-security.md` |
| Security Architect | Threat modeling, security design | `references/security-architecture.md` |
| DevSecOps Engineer | Pipeline security, automation | `references/devsecops.md` |
| Penetration Tester | Offensive security, red team | `references/application-security.md` |
| Compliance Analyst | Frameworks, audits, governance | `references/compliance.md` |

## Key References

- **Application security**: See `references/application-security.md` for OWASP, code review, and vulnerability classes.
- **Cloud security**: See `references/cloud-security.md` for cloud-native security controls and posture management.
- **Security architecture**: See `references/security-architecture.md` for threat modeling, zero trust, and cryptography.
- **DevSecOps**: See `references/devsecops.md` for security automation and pipeline integration.
- **Compliance**: See `references/compliance.md` for frameworks, audits, and governance.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `application`, ... | **Application Security** | AppSec Specialist | `references/application-security.md` |
| `cloud`, ... | **Cloud Security** | CloudSec Specialist | `references/cloud-security.md` |
| `DevSecOps`, ... | **DevSecOps** | DevSecOps Specialist | `references/devsecops.md` |
| `compliance`, ... | **Compliance** | Compliance Specialist | `references/compliance.md` |
| `architecture`, ... | **Security Architecture** | Architecture Specialist | `references/security-architecture.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 5

### Cross-Domain Synthesizer

After all specialists complete, run one **Kill Chain Mapper** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Maps compliance requirements to architectural gaps to DevSecOps pipeline holes — constructing the full kill chain across domains. Surfaces where a compliance requirement is architecturally unenforceable.
