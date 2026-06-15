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

| Layer | IaaS (Customer) | PaaS (Shared) | SaaS (Provider) |
|---|---|---|---|
| Data | Customer | Customer | Customer |
| Applications | Customer | Customer | Provider |
| Runtime/Middleware | Customer | Provider | Provider |
| OS | Customer | Provider | Provider |
| Virtualization | Provider | Provider | Provider |
| Network/Storage | Provider | Provider | Provider |
| Physical | Provider | Provider | Provider |

### Cloud Security Posture Management (CSPM)

| Tool | Cloud | Features |
|---|---|---|
| AWS Security Hub | AWS | Aggregated findings, compliance |
| Google SCC | GCP | Asset inventory, vulnerability |
| Microsoft Defender | Azure | Posture management, workload protection |
| Prowler | Multi-cloud | Open-source, CIS benchmarks |
| ScoutSuite | Multi-cloud | Open-source, multi-cloud audit |
| Wiz | Multi-cloud | Agentless, graph-based |

### CIS Benchmarks (Key Controls)

| Category | Control | Implementation |
|---|---|---|
| Identity | MFA for all users | Enforce MFA policy |
| Identity | No root/owner account for daily use | Use federated identity |
| Logging | CloudTrail/Audit Logs enabled | All regions, all services |
| Networking | No public access to storage | Bucket policies, ACLs |
| Networking | Security groups restrict ingress | Least privilege rules |
| Encryption | Encryption at rest enabled | Default encryption |
| Monitoring | Alerts on unauthorized API calls | CloudWatch/Alert policies |

---

## 2. Identity and Access Management

### IAM Best Practices

| Practice | Description | Implementation |
|---|---|---|
| Least privilege | Minimum required permissions | Start with zero, add as needed |
| No long-lived credentials | Use temporary credentials | IAM roles, OIDC federation |
| MFA everywhere | Multi-factor for all humans | Hardware keys for admins |
| Separate accounts/projects | Blast radius isolation | AWS Organizations, GCP folders |
| Service accounts | Dedicated identity per service | No shared credentials |
| Regular access review | Remove unused permissions | Automated access analysis |
| Break-glass procedures | Emergency access process | Documented, audited |

### AWS IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringEquals": {"aws:RequestedRegion": "us-east-1"},
        "Bool": {"aws:SecureTransport": "true"}
      }
    }
  ]
}
```

### Identity Federation

| Method | Use Case | Protocol |
|---|---|---|
| SAML 2.0 | Enterprise SSO | XML-based |
| OIDC | Modern applications | JWT-based |
| SCIM | User provisioning | REST API |
| Workload Identity | Service-to-cloud auth | OIDC (K8s → Cloud) |

---

## 3. Network Security

### Cloud Network Security Controls

| Control | Purpose | Implementation |
|---|---|---|
| VPC/VNet | Network isolation | Separate environments |
| Security Groups | Instance-level firewall | Least privilege rules |
| NACLs | Subnet-level firewall | Stateless rules |
| WAF | Web application firewall | OWASP rules, custom rules |
| DDoS protection | Volumetric attack mitigation | Shield/Armor/DDoS Protection |
| Private endpoints | No public internet traversal | PrivateLink/Private Service Connect |
| VPN/Direct Connect | Secure hybrid connectivity | Encrypted tunnels |

### Zero Trust Network Architecture

```
User/Service → Identity Verification → Policy Engine → Access Decision → Resource
                    ↓                       ↓
              Device Trust            Context (time, location, risk)
```

**Principles**:
- Verify explicitly (authenticate and authorize every request)
- Use least privilege access (just-in-time, just-enough)
- Assume breach (minimize blast radius, segment access)
- Encrypt all traffic (even internal, east-west)
- Continuous validation (not just at connection time)

---

## 4. Data Protection

### Data Classification

| Level | Description | Controls |
|---|---|---|
| Public | No impact if disclosed | Basic integrity controls |
| Internal | Business impact if disclosed | Access control, encryption in transit |
| Confidential | Significant impact | Encryption at rest/transit, audit logging |
| Restricted | Severe impact (PII, financial) | All above + DLP, tokenization, masking |

### Encryption Strategy

| Layer | Method | Key Management |
|---|---|---|
| At rest (storage) | AES-256-GCM | KMS (AWS KMS, Cloud KMS, Key Vault) |
| In transit | TLS 1.3 | Certificate management (ACM, Let's Encrypt) |
| In use | Confidential computing | Hardware enclaves (SGX, SEV) |
| Application-level | Envelope encryption | Application-managed DEKs, KMS-managed KEKs |
| Database | TDE or column-level | Database-native or application-level |

### Secrets Management

| Tool | Type | Best For |
|---|---|---|
| HashiCorp Vault | Self-hosted/managed | Multi-cloud, dynamic secrets |
| AWS Secrets Manager | Managed | AWS-native, rotation |
| GCP Secret Manager | Managed | GCP-native |
| Azure Key Vault | Managed | Azure-native |
| External Secrets Operator | K8s-native | Sync secrets to K8s |

---

## 5. Container and Kubernetes Security

### Container Security Layers

| Layer | Control | Tools |
|---|---|---|
| Image | Vulnerability scanning, signing | Trivy, Cosign, Snyk |
| Build | Secure base images, multi-stage | Distroless, scratch |
| Registry | Private registry, access control | Harbor, ECR, GCR |
| Runtime | Read-only FS, non-root, seccomp | Pod Security Standards |
| Network | Network policies, service mesh | Calico, Istio, Cilium |
| Secrets | External secrets, encryption | Sealed Secrets, Vault |
| Admission | Policy enforcement | OPA Gatekeeper, Kyverno |

### Kubernetes Security Checklist

| Category | Control | Priority |
|---|---|---|
| Authentication | OIDC integration, no static tokens | Critical |
| Authorization | RBAC with least privilege | Critical |
| Pod Security | Restricted Pod Security Standard | High |
| Network | Default deny network policies | High |
| Secrets | External secrets management | High |
| Images | Signed, scanned, from trusted registry | High |
| Audit | API server audit logging enabled | Medium |
| Runtime | Falco or similar runtime detection | Medium |
| Admission | Gatekeeper/Kyverno policies | Medium |

---

## 6. Incident Response

### Cloud Incident Response Process

1. **Preparation**: Runbooks, access, tools, communication plan
2. **Detection**: Alerts, anomaly detection, threat intelligence
3. **Containment**: Isolate affected resources, preserve evidence
4. **Eradication**: Remove threat, patch vulnerability
5. **Recovery**: Restore services, verify integrity
6. **Lessons Learned**: Post-mortem, improve controls

### Cloud Forensics

| Action | AWS | GCP | Azure |
|---|---|---|---|
| Preserve logs | CloudTrail, VPC Flow Logs | Audit Logs, VPC Flow Logs | Activity Log, NSG Flow Logs |
| Snapshot evidence | EBS snapshots, AMI | Disk snapshots | Disk snapshots |
| Isolate instance | Remove from SG, add deny SG | Remove from network | NSG deny all |
| Memory capture | SSM, EC2 serial console | Serial console | Serial console |
| Timeline | Athena + CloudTrail | BigQuery + Audit Logs | Log Analytics |

### Containment Actions

```bash
# AWS: Isolate compromised EC2 instance
# 1. Create forensic security group (no inbound, no outbound)
aws ec2 create-security-group --group-name forensic-isolation \
  --description "Forensic isolation - no traffic"

# 2. Replace instance security groups
aws ec2 modify-instance-attribute --instance-id i-xxx \
  --groups sg-forensic-isolation

# 3. Snapshot the instance for evidence
aws ec2 create-snapshot --volume-id vol-xxx --description "Forensic evidence"

# 4. Disable compromised IAM credentials
aws iam update-access-key --access-key-id AKIA... --status Inactive --user-name compromised-user
```
