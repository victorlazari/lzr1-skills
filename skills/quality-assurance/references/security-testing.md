# Security Testing

**Verified against upstream: 2026-08-07**
**Normative Guidance**: OWASP Web Security Testing Guide (WSTG)

## Table of Contents
1. Security Testing Strategy
2. OWASP Top 10 Integration
3. Security Testing Tools
4. Vulnerability Assessment

---

## 1. Security Testing Strategy

### Shift-Left Security

| Phase | Security Activity | Tools |
|---|---|---|
| Design | Threat modeling | Draw.io, Microsoft Threat Modeling Tool |
| Development | SAST (Static Analysis), IDE plugins | SonarQube, Snyk, Checkmarx |
| Build/CI | SCA (Software Composition Analysis) | Dependabot, Trivy |
| Testing | DAST (Dynamic Analysis), IAST | OWASP ZAP, Burp Suite |
| Deployment | Infrastructure as Code (IaC) scanning | Checkov, tfsec |
| Production | Penetration testing, Bug bounty | HackerOne, Bugcrowd |

### Security Testing Types

| Type | Description | When to Use |
|---|---|---|
| SAST | Analyzes source code for vulnerabilities | During development, CI/CD |
| DAST | Analyzes running application from outside | During testing, staging |
| IAST | Combines SAST and DAST from inside app | During testing |
| SCA | Analyzes third-party dependencies | Continuous |
| Pen Testing | Manual exploitation by experts | Pre-release, periodic |

---

## 2. OWASP Top 10 Integration

Ensure test plans cover the latest OWASP Top 10 vulnerabilities.

| Vulnerability | Testing Approach |
|---|---|
| Broken Access Control | Test role-based access, IDOR, forced browsing |
| Cryptographic Failures | Verify TLS, check sensitive data storage |
| Injection | Test SQLi, XSS, Command Injection inputs |
| Insecure Design | Review threat models, business logic flaws |
| Security Misconfiguration | Check default accounts, error messages, headers |
| Vulnerable and Outdated Components | Run SCA tools, check dependency trees |
| Identification and Authentication Failures | Test brute force, session management, MFA |
| Software and Data Integrity Failures | Verify CI/CD pipeline security, signed commits |
| Security Logging and Monitoring Failures | Verify audit logs, alert triggers |
| Server-Side Request Forgery (SSRF) | Test URL inputs, internal network access |

---

## 3. Security Testing Tools

| Tool | Category | Best For |
|---|---|---|
| OWASP ZAP | DAST | Automated web scanning, CI/CD integration |
| Burp Suite | DAST / Manual | Deep manual testing, proxy interception |
| SonarQube | SAST | Continuous code quality and security |
| Snyk | SCA / SAST | Developer-friendly dependency scanning |
| Trivy | Container / IaC | Scanning Docker images and Kubernetes |
| Nmap | Network | Port scanning, service discovery |

---

## 4. Vulnerability Assessment

### Vulnerability Report Template

```
Vulnerability: [Name of vulnerability, e.g., Stored XSS]
Severity: Critical/High/Medium/Low (CVSS Score)
Endpoint: [URL or API endpoint]
Parameter: [Vulnerable parameter]

Description:
[Detailed explanation of the vulnerability and its impact]

Steps to Reproduce:
1. [Step]
2. [Step]
3. [Step]

Proof of Concept:
[Payload or screenshot demonstrating the exploit]

Remediation:
[Actionable steps to fix the vulnerability]
```

### CVSS Scoring

Use the Common Vulnerability Scoring System (CVSS) to assess severity based on:
- **Attack Vector**: Network, Adjacent, Local, Physical
- **Attack Complexity**: Low, High
- **Privileges Required**: None, Low, High
- **User Interaction**: None, Required
- **Scope**: Unchanged, Changed
- **Confidentiality Impact**: None, Low, High
- **Integrity Impact**: None, Low, High
- **Availability Impact**: None, Low, High
