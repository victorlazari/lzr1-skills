# Security Engineering

Verified against upstream: 2026-08-07

## Table of Contents
1. Application Security
2. Supply Chain Security
3. AI Security
4. Cloud Security
5. Incident Response

---

## 1. Application Security

### OWASP Top 10 (2021/2026)

1. **Broken Access Control**: Ensure users cannot act outside their intended permissions.
2. **Cryptographic Failures**: Protect data in transit and at rest.
3. **Injection**: Validate and sanitize all user input (SQL, NoSQL, OS command, LDAP).
4. **Insecure Design**: Implement threat modeling and secure design patterns.
5. **Security Misconfiguration**: Harden configurations, remove default accounts.
6. **Vulnerable and Outdated Components**: Keep dependencies updated.
7. **Identification and Authentication Failures**: Implement strong auth, MFA.
8. **Software and Data Integrity Failures**: Verify integrity of updates, CI/CD pipelines.
9. **Security Logging and Monitoring Failures**: Ensure critical events are logged and monitored.
10. **Server-Side Request Forgery (SSRF)**: Validate and restrict URLs fetched by the server.

### Secure Coding Practices

- **Input Validation**: Validate type, length, format, and range. Use allow-lists.
- **Output Encoding**: Context-aware encoding (HTML, JS, CSS, URL) to prevent XSS.
- **Authentication**: Use strong password hashing (Argon2, bcrypt), implement MFA.
- **Session Management**: Secure cookies (HttpOnly, Secure, SameSite), short timeouts.
- **Error Handling**: Do not leak sensitive information in error messages.

---

## 2. Supply Chain Security

### Securing the CI/CD Pipeline

- **Code Signing**: Sign commits and artifacts (e.g., using Sigstore).
- **SBOM (Software Bill of Materials)**: Generate and maintain SBOMs for all projects.
- **Dependency Scanning**: Use tools like Trivy, Dependabot, or Snyk to scan for vulnerabilities.
- **Provenance**: Ensure artifacts can be traced back to their source code and build environment (SLSA framework).
- **Least Privilege**: Restrict permissions for CI/CD runners and service accounts.

### Dependency Management

- Pin dependencies to specific versions.
- Use lockfiles (`package-lock.json`, `Cargo.lock`, `go.sum`).
- Audit new dependencies for security and maintenance status before adoption.
- Implement automated dependency updates with security checks.

---

## 3. AI Security

### LLM Vulnerabilities (OWASP Top 10 for LLMs)

1. **Prompt Injection**: Attackers manipulate the LLM via crafted inputs.
2. **Insecure Output Handling**: Blindly trusting LLM output without validation.
3. **Training Data Poisoning**: Malicious data introduced during training or fine-tuning.
4. **Model Denial of Service**: Resource exhaustion via complex prompts.
5. **Supply Chain Vulnerabilities**: Compromised models, datasets, or plugins.
6. **Sensitive Information Disclosure**: LLMs leaking PII or confidential data.
7. **Insecure Plugin Design**: Plugins executing unsafe actions based on LLM requests.
8. **Excessive Agency**: LLMs granted too much autonomy or privilege.
9. **Overreliance**: Over-trusting LLM outputs for critical decisions.
10. **Model Theft**: Unauthorized access or exfiltration of proprietary models.

### AI Security Best Practices

- **Input/Output Validation**: Treat LLM input and output as untrusted.
- **Sandboxing**: Execute LLM-generated code or actions in isolated environments.
- **Human-in-the-Loop**: Require human approval for high-risk actions.
- **Data Privacy**: Do not send sensitive data to public LLM APIs without agreements.
- **Monitoring**: Monitor LLM interactions for malicious prompts or anomalous behavior.

---

## 4. Cloud Security

### Cloud Security Posture Management (CSPM)

- **IAM (Identity and Access Management)**: Enforce least privilege, use roles instead of long-lived credentials.
- **Network Security**: Use VPCs, security groups, and firewalls to restrict traffic.
- **Data Protection**: Encrypt data at rest (KMS) and in transit (TLS).
- **Logging**: Enable CloudTrail, VPC Flow Logs, and centralized logging.
- **Compliance**: Continuously monitor for compliance with frameworks (CIS, SOC2, HIPAA).

### Zero Trust Architecture

- Never trust, always verify.
- Authenticate and authorize every request, regardless of origin.
- Implement micro-segmentation to limit lateral movement.
- Use device posture and user identity for access decisions.

---

## 5. Incident Response

### Incident Response Lifecycle

1. **Preparation**: Create runbooks, establish communication channels, train the team.
2. **Identification**: Detect and confirm the incident (alerts, logs, reports).
3. **Containment**: Stop the bleeding (isolate systems, revoke credentials).
4. **Eradication**: Remove the threat (patch vulnerabilities, clean systems).
5. **Recovery**: Restore services to normal operation.
6. **Lessons Learned**: Conduct a blameless post-mortem, update processes.

### Post-Mortem Best Practices

- Focus on systemic failures, not human error.
- Identify root causes using the "5 Whys" technique.
- Create actionable, prioritized remediation tasks.
- Share findings transparently with the organization.
