# Cloud Security

## Table of Contents
1. Cloud Security Posture
2. Identity and Access Management
3. Network Security
4. Data Protection
5. Container and Kubernetes Security
6. Incident Response

---

## 1. Cloud Security Posture

### Shared Responsibility Model

The shared responsibility model dictates the security obligations of the cloud provider and the customer. This varies by service model (IaaS, PaaS, SaaS). Always verify the specific shared responsibility model for the cloud provider in use.

**Canonical Sources:**
- [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [Azure Shared Responsibility Model](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
- [GCP Shared Responsibility Model](https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)

### Cloud Security Posture Management (CSPM)

CSPM involves continuously monitoring cloud environments for misconfigurations and compliance violations. Focus on principles such as automated scanning, continuous compliance, and remediation.

---

## 2. Identity and Access Management (IAM)

IAM is the perimeter in cloud environments.

- **Least Privilege:** Grant only the permissions necessary to perform a task.
- **Role-Based Access Control (RBAC):** Assign permissions to roles, not individual users.
- **Multi-Factor Authentication (MFA):** Require MFA for all human access, especially privileged accounts.
- **Temporary Credentials:** Use short-lived credentials (e.g., STS, temporary tokens) instead of long-lived access keys.
- **Identity Federation:** Integrate with centralized identity providers (IdP) using SAML or OIDC.

---

## 3. Network Security

- **Virtual Private Clouds (VPCs):** Isolate resources in private networks.
- **Security Groups / Network Security Groups:** Implement stateful firewalls at the instance level.
- **Network ACLs:** Implement stateless firewalls at the subnet level.
- **Zero Trust Network Access (ZTNA):** Do not trust internal networks; authenticate and authorize every request.
- **DDoS Protection:** Utilize cloud-native DDoS mitigation services.
- **Web Application Firewalls (WAF):** Protect web applications from common exploits.

---

## 4. Data Protection

- **Encryption at Rest:** Encrypt all data stored in databases, object storage, and block storage. Use customer-managed keys (CMK) where appropriate.
- **Encryption in Transit:** Enforce TLS 1.3+ for all network communication.
- **Data Classification:** Classify data based on sensitivity and apply appropriate controls.
- **Data Loss Prevention (DLP):** Implement mechanisms to detect and prevent the exfiltration of sensitive data.
- **Secrets Management:** Store secrets (API keys, passwords) in dedicated secrets management services, never in code or configuration files.

---

## 5. Container and Kubernetes Security

**Canonical Source:** [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
**Verification:** Verify current Kubernetes security best practices from the canonical source.

- **Image Scanning:** Scan container images for vulnerabilities before deployment.
- **Minimal Base Images:** Use minimal base images (e.g., distroless, Alpine) to reduce the attack surface.
- **Runtime Security:** Monitor container runtime behavior for anomalies.
- **RBAC:** Implement strict RBAC for Kubernetes API access.
- **Network Policies:** Restrict communication between pods using network policies.
- **Pod Security Admission:** Enforce security standards for pods (e.g., restricting privileged containers).

---

## 6. Incident Response

Cloud incident response requires specific strategies due to the dynamic nature of cloud environments.

- **Preparation:** Enable comprehensive logging (e.g., CloudTrail, Azure Monitor, Cloud Audit Logs) and centralize logs in a secure, immutable location.
- **Detection:** Implement automated alerting based on security events.
- **Containment:** Isolate compromised resources (e.g., changing security groups, revoking IAM roles) rather than shutting them down, to preserve evidence.
- **Eradication:** Identify and remove the root cause of the incident.
- **Recovery:** Restore services from known good backups or redeploy from infrastructure as code (IaC).
- **Lessons Learned:** Conduct a post-mortem analysis to improve future response. For customer-facing incident reports, route to the `post-mortem-master` skill.
