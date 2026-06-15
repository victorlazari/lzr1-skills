# Endpoint Management

## Table of Contents
1. MDM and Device Management
2. SaaS Administration
3. IT Onboarding/Offboarding
4. Helpdesk Operations
5. Asset Management

---

## 1. MDM and Device Management

### MDM Solutions

| Solution | Platform | Best For |
|---|---|---|
| Jamf | macOS/iOS | Apple-first companies |
| Kandji | macOS/iOS | Modern Apple MDM |
| Intune | Windows/macOS | Microsoft ecosystem |
| Mosyle | macOS/iOS | Education + business |
| Fleet | Cross-platform | Open-source, osquery-based |
| Hexnode | Cross-platform | Multi-platform SMB |

### Device Configuration Baseline

| Setting | macOS | Windows |
|---|---|---|
| Disk encryption | FileVault enabled | BitLocker enabled |
| Firewall | Enabled, stealth mode | Windows Defender Firewall |
| Auto-updates | Enabled, enforced | WSUS/Intune managed |
| Screen lock | 5 min timeout | 5 min timeout |
| Password policy | 12+ chars, complexity | 12+ chars, complexity |
| Antivirus | XProtect + EDR | Defender + EDR |
| Remote wipe | Enabled | Enabled |

### Device Lifecycle

| Phase | Activities | Tools |
|---|---|---|
| Procurement | Order, configure, inventory | Vendor portal, asset DB |
| Provisioning | Zero-touch enrollment, apps, config | MDM, DEP/Autopilot |
| Management | Patches, compliance, monitoring | MDM, EDR |
| Support | Troubleshooting, repairs | Helpdesk, remote access |
| Retirement | Wipe, recycle, decommission | MDM, asset DB |

---

## 2. SaaS Administration

### SaaS Stack (Typical Tech Company)

| Category | Tools | Admin Tasks |
|---|---|---|
| Productivity | Google Workspace / Microsoft 365 | Users, groups, policies |
| Communication | Slack / Teams | Channels, integrations, retention |
| Code | GitHub / GitLab | Repos, teams, permissions |
| Project | Jira / Linear / Asana | Projects, workflows, integrations |
| Design | Figma | Teams, libraries, permissions |
| HR | Rippling / BambooHR | Employee data, workflows |
| Security | Okta / Google Identity | SSO, MFA, provisioning |
| Finance | Brex / Ramp | Cards, policies, approvals |

### SaaS Management Best Practices

| Practice | Description |
|---|---|
| Centralized inventory | Track all SaaS tools, owners, costs |
| SSO enforcement | All tools behind SSO where possible |
| SCIM provisioning | Automated user provisioning/deprovisioning |
| License optimization | Regular audit of unused licenses |
| Access reviews | Quarterly review of who has access to what |
| Shadow IT detection | Monitor for unauthorized tool adoption |
| Vendor consolidation | Reduce overlapping tools |

---

## 3. IT Onboarding/Offboarding

### Onboarding Checklist

| Day | Task | System |
|---|---|---|
| Day -5 | Create accounts (email, SSO) | IdP, Google/M365 |
| Day -3 | Ship laptop (pre-configured) | MDM, shipping |
| Day -1 | Add to groups, channels | Slack, Google Groups |
| Day 1 | Welcome, verify access | Helpdesk |
| Day 1 | Security training enrollment | LMS |
| Day 3 | Verify all tools accessible | Checklist |
| Day 7 | Follow-up, resolve issues | Helpdesk |

### Offboarding Checklist

| Timing | Task | System |
|---|---|---|
| Immediate | Disable SSO/email | IdP |
| Immediate | Revoke all sessions | IdP, critical apps |
| Immediate | Change shared passwords | Password manager |
| Within 24h | Transfer file ownership | Google Drive, GitHub |
| Within 24h | Remove from groups/channels | Slack, email groups |
| Within 48h | Retrieve hardware | Shipping, MDM wipe |
| Within 7d | Archive accounts | Per retention policy |
| Within 30d | Delete accounts | Per retention policy |

---

## 4. Helpdesk Operations

### Ticket Categories

| Category | Examples | SLA |
|---|---|---|
| Access | Can't login, need access to tool | 1 hour |
| Hardware | Laptop issue, peripheral needed | 4 hours |
| Software | App not working, need installation | 4 hours |
| Security | Phishing report, suspicious activity | 30 minutes |
| Network | VPN, WiFi, connectivity | 2 hours |
| Account | Password reset, MFA issue | 1 hour |
| New request | New tool, new hardware | 24 hours |

---

## 5. Asset Management

### Asset Tracking

| Field | Description |
|---|---|
| Asset tag | Unique identifier |
| Type | Laptop, monitor, phone, etc. |
| Make/Model | Manufacturer and model |
| Serial number | Manufacturer serial |
| Assigned to | Current user |
| Status | Active, spare, retired |
| Purchase date | When acquired |
| Warranty end | When warranty expires |
| Cost | Purchase price |
| Location | Office, remote, storage |
