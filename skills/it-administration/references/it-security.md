# IT Security

## Table of Contents
1. Security Hardening
2. Email Security
3. Endpoint Detection and Response
4. Security Monitoring
5. Compliance and Audit

---

## 1. Security Hardening

### CIS Benchmark Essentials

| Category | Controls |
|---|---|
| Inventory | Hardware and software inventory |
| Configuration | Secure configuration baselines |
| Vulnerability | Continuous vulnerability management |
| Access | Controlled use of admin privileges |
| Maintenance | Maintenance, monitoring, analysis of audit logs |
| Email/Browser | Email and web browser protections |
| Malware | Malware defenses |
| Recovery | Data recovery capabilities |

### macOS Hardening

| Setting | Configuration |
|---|---|
| FileVault | Enabled, recovery key escrowed |
| Firewall | Enabled, stealth mode on |
| Gatekeeper | App Store + identified developers |
| SIP | System Integrity Protection enabled |
| Auto-updates | Enabled, critical updates automatic |
| Remote login | Disabled (unless needed) |
| Screen sharing | Disabled (unless needed) |
| Guest account | Disabled |

### Windows Hardening

| Setting | Configuration |
|---|---|
| BitLocker | Enabled, TPM + PIN |
| Windows Defender | Enabled, real-time protection |
| Windows Firewall | Enabled, all profiles |
| UAC | Enabled, highest level |
| PowerShell | Constrained language mode |
| Remote Desktop | Disabled (unless needed) |
| Auto-updates | Managed via WSUS/Intune |
| Local admin | Disabled or LAPS managed |

---

## 2. Email Security

### Email Security Layers

| Layer | Technology | Purpose |
|---|---|---|
| Authentication | SPF | Authorize sending servers |
| Authentication | DKIM | Sign emails cryptographically |
| Authentication | DMARC | Policy for failed auth |
| Filtering | Spam filter | Block unwanted email |
| Filtering | Phishing detection | Block malicious links |
| Filtering | Attachment scanning | Block malware |
| Protection | Link rewriting | Safe links inspection |
| Protection | Sandboxing | Detonate suspicious attachments |
| Training | Phishing simulation | Test and train users |

### DMARC Configuration

```
# DNS TXT record for _dmarc.example.com
v=DMARC1; p=reject; rua=mailto:dmarc@example.com; ruf=mailto:dmarc@example.com; pct=100

Progression:
1. p=none (monitor only, collect reports)
2. p=quarantine (send failures to spam)
3. p=reject (block failures entirely)
```

---

## 3. Endpoint Detection and Response

### EDR Solutions

| Solution | Strengths | Best For |
|---|---|---|
| CrowdStrike Falcon | Market leader, AI-powered | Enterprise |
| SentinelOne | Autonomous response | Mid-market to enterprise |
| Microsoft Defender for Endpoint | Integrated with M365 | Microsoft shops |
| Carbon Black (VMware) | Behavioral analysis | Enterprise |
| Huntress | Managed detection | SMB |

### EDR Capabilities

| Capability | Description |
|---|---|
| Prevention | Block known malware, exploits |
| Detection | Identify suspicious behavior |
| Investigation | Timeline, process tree, forensics |
| Response | Isolate, kill process, remediate |
| Hunting | Proactive threat hunting |
| Reporting | Compliance, executive dashboards |

---

## 4. Security Monitoring

### Security Monitoring Stack

| Component | Tool Options | Purpose |
|---|---|---|
| SIEM | Splunk, Elastic, Panther | Log aggregation, correlation |
| EDR | CrowdStrike, SentinelOne | Endpoint detection |
| Cloud security | Wiz, Orca, Prisma Cloud | Cloud posture |
| Identity | IdP logs, Okta | Authentication monitoring |
| Network | Zeek, Suricata | Network traffic analysis |
| Vulnerability | Qualys, Tenable, Snyk | Vulnerability scanning |

### Alert Priority

| Priority | Description | Response |
|---|---|---|
| Critical | Active breach, data exfiltration | Immediate (24/7) |
| High | Malware detected, compromised account | Within 1 hour |
| Medium | Policy violation, suspicious activity | Within 4 hours |
| Low | Informational, minor policy deviation | Next business day |

---

## 5. Compliance and Audit

### IT Controls for SOC 2

| Control Area | IT Admin Responsibility |
|---|---|
| Access control | SSO, MFA, access reviews, least privilege |
| Change management | Approval workflows, audit trails |
| System operations | Monitoring, alerting, incident response |
| Risk management | Vulnerability scanning, patching |
| Data protection | Encryption, backup, retention |
| Physical security | Endpoint encryption, remote wipe |
| HR security | Onboarding/offboarding, training |

### Audit Evidence Collection

| Control | Evidence |
|---|---|
| MFA enforcement | IdP configuration screenshot, policy |
| Access reviews | Review completion records, revocations |
| Patching | MDM compliance reports, patch status |
| Encryption | FileVault/BitLocker compliance report |
| Offboarding | Deprovisioning logs, timeline proof |
| Training | Completion records, phishing sim results |
| Monitoring | Alert configurations, response records |
