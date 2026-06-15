# Compliance Programs

## Table of Contents
1. SOC 2
2. ISO 27001
3. HIPAA
4. PCI DSS
5. Building a Compliance Program

---

## 1. SOC 2

### Trust Service Criteria

| Criteria | Description | Required |
|---|---|---|
| Security (Common Criteria) | Protection against unauthorized access | Always (required) |
| Availability | System is available for operation | Optional |
| Processing Integrity | Processing is complete, accurate, timely | Optional |
| Confidentiality | Information designated as confidential is protected | Optional |
| Privacy | Personal information handling | Optional |

### SOC 2 Type I vs Type II

| Aspect | Type I | Type II |
|---|---|---|
| Scope | Design of controls at a point in time | Design AND operating effectiveness over time |
| Duration | Single date | Typically 6-12 month observation period |
| Evidence | Control descriptions, design assessment | Control descriptions + testing evidence |
| Value | "We have controls" | "Our controls work consistently" |
| Timeline to achieve | 2-4 months | 6-12 months |
| Customer preference | Acceptable for early-stage | Preferred by enterprise customers |

### SOC 2 Common Controls

| Category | Controls |
|---|---|
| Access control | SSO, MFA, RBAC, access reviews, least privilege |
| Change management | Code review, testing, approval workflows, rollback |
| Incident response | Detection, response plan, communication, post-mortem |
| Risk assessment | Annual risk assessment, vendor management |
| Monitoring | Logging, alerting, SIEM, anomaly detection |
| Data protection | Encryption (at rest + in transit), backup, retention |
| HR | Background checks, security training, onboarding/offboarding |
| Physical | Data center security (if applicable) |

---

## 2. ISO 27001

### ISO 27001 Structure

| Clause | Title | Content |
|---|---|---|
| 4 | Context of the organization | Scope, stakeholders, ISMS scope |
| 5 | Leadership | Management commitment, policy, roles |
| 6 | Planning | Risk assessment, risk treatment, objectives |
| 7 | Support | Resources, competence, awareness, communication |
| 8 | Operation | Risk assessment execution, risk treatment |
| 9 | Performance evaluation | Monitoring, internal audit, management review |
| 10 | Improvement | Nonconformity, corrective action, continual improvement |

### Annex A Controls (ISO 27001:2022)

| Theme | Controls | Examples |
|---|---|---|
| Organizational (37) | Policies, roles, responsibilities | Information security policy, asset management |
| People (8) | HR security | Screening, awareness, disciplinary |
| Physical (14) | Physical security | Secure areas, equipment, clear desk |
| Technological (34) | Technical controls | Access control, cryptography, logging |

---

## 3. HIPAA

### HIPAA Rules

| Rule | Scope | Key Requirements |
|---|---|---|
| Privacy Rule | Use and disclosure of PHI | Minimum necessary, patient rights, notices |
| Security Rule | Electronic PHI (ePHI) safeguards | Administrative, physical, technical safeguards |
| Breach Notification | Reporting breaches | 60-day notification, HHS reporting |
| Enforcement | Penalties and investigations | Tiered penalties up to $1.5M per violation |

### HIPAA Safeguards

| Category | Safeguard | Examples |
|---|---|---|
| Administrative | Risk analysis | Annual risk assessment |
| Administrative | Workforce training | Security awareness training |
| Administrative | Incident procedures | Breach response plan |
| Physical | Facility access | Badge access, visitor logs |
| Physical | Workstation security | Screen locks, clean desk |
| Technical | Access control | Unique user IDs, emergency access |
| Technical | Audit controls | Activity logging, review |
| Technical | Transmission security | Encryption in transit |

### Business Associate Agreement (BAA)

```
Required when:
- A vendor handles PHI on behalf of a covered entity
- Cloud providers storing/processing ePHI
- IT service providers with PHI access

Must include:
- Permitted uses and disclosures
- Safeguards requirement
- Breach notification obligations
- Return/destruction of PHI at termination
- Subcontractor requirements
```

---

## 4. PCI DSS

### PCI DSS Requirements (v4.0)

| Requirement | Description |
|---|---|
| 1 | Install and maintain network security controls |
| 2 | Apply secure configurations to all system components |
| 3 | Protect stored account data |
| 4 | Protect cardholder data with strong cryptography during transmission |
| 5 | Protect all systems and networks from malicious software |
| 6 | Develop and maintain secure systems and software |
| 7 | Restrict access to system components and cardholder data by business need to know |
| 8 | Identify users and authenticate access to system components |
| 9 | Restrict physical access to cardholder data |
| 10 | Log and monitor all access to system components and cardholder data |
| 11 | Test security of systems and networks regularly |
| 12 | Support information security with organizational policies and programs |

---

## 5. Building a Compliance Program

### Program Components

| Component | Description | Activities |
|---|---|---|
| Governance | Leadership, structure, accountability | Board oversight, compliance officer |
| Risk assessment | Identify and prioritize risks | Annual assessment, risk register |
| Policies | Written rules and expectations | Policy library, annual review |
| Training | Employee awareness | Annual training, role-specific |
| Monitoring | Ongoing compliance checking | Audits, testing, metrics |
| Reporting | Communication of compliance status | Board reports, dashboards |
| Response | Handling violations and incidents | Investigation, remediation |
| Improvement | Continuous enhancement | Lessons learned, updates |

### Compliance Maturity Model

| Level | Description | Characteristics |
|---|---|---|
| 1 - Ad hoc | No formal program | Reactive, inconsistent |
| 2 - Developing | Basic policies exist | Some documentation, manual processes |
| 3 - Defined | Formal program established | Documented, trained, monitored |
| 4 - Managed | Measured and optimized | Metrics, continuous improvement |
| 5 - Optimized | Industry-leading | Automated, predictive, embedded |

### Audit Preparation

| Phase | Activities | Timeline |
|---|---|---|
| Readiness | Gap assessment, remediation plan | 3-6 months before |
| Evidence collection | Gather documentation, screenshots | 1-2 months before |
| Pre-audit | Internal audit, dry run | 1 month before |
| Audit | Auditor interviews, evidence review | 2-4 weeks |
| Remediation | Address findings | 30-90 days after |
| Certification | Report issued | After remediation |
