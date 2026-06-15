# DevSecOps

## Table of Contents
1. Security in CI/CD
2. Security Testing Tools
3. Vulnerability Management
4. Infrastructure Security Scanning
5. Runtime Security

---

## 1. Security in CI/CD

### Security Pipeline Integration

```
Code Commit → Pre-commit Hooks → Build → SAST → SCA → Container Scan → DAST → Deploy
     ↓              ↓                         ↓        ↓          ↓          ↓
  Secrets scan   Lint security rules    Code vulns  Dep vulns  Image vulns  Runtime vulns
```

### Pipeline Security Controls

| Stage | Control | Tool Examples | Blocking? |
|---|---|---|---|
| Pre-commit | Secret detection | gitleaks, detect-secrets | Yes |
| Pre-commit | Security linting | semgrep, eslint-security | Yes |
| Build | SAST (static analysis) | Semgrep, CodeQL, SonarQube | Critical/High |
| Build | SCA (dependency scan) | Snyk, Dependabot, Trivy | Critical |
| Build | License compliance | FOSSA, Snyk | Policy-based |
| Package | Container image scan | Trivy, Grype, Snyk | Critical/High |
| Package | Image signing | Cosign, Notary | Yes |
| Deploy | IaC scanning | Checkov, tfsec, KICS | High |
| Deploy | DAST (dynamic testing) | ZAP, Nuclei | Critical |
| Runtime | Runtime protection | Falco, Sysdig | Alert |

### Shift-Left Security

The earlier a vulnerability is found, the cheaper it is to fix:

| Stage Found | Relative Cost to Fix |
|---|---|
| Design/Architecture | 1x |
| Development (IDE) | 5x |
| Build/CI | 10x |
| Testing/QA | 25x |
| Production | 100x |
| Post-breach | 1000x+ |

---

## 2. Security Testing Tools

### SAST (Static Application Security Testing)

| Tool | Languages | Strengths |
|---|---|---|
| Semgrep | 30+ languages | Fast, custom rules, low false positives |
| CodeQL | Major languages | Deep analysis, GitHub-native |
| SonarQube | 25+ languages | Quality + security, enterprise |
| Bandit | Python | Python-specific, lightweight |
| gosec | Go | Go-specific security scanner |
| Brakeman | Ruby | Rails-specific |

### SCA (Software Composition Analysis)

| Tool | Features | Integration |
|---|---|---|
| Snyk | Vulns + fix PRs + license | IDE, CI, registry |
| Dependabot | Auto-update PRs | GitHub-native |
| Trivy | Vulns + misconfig + secrets | CLI, CI, K8s |
| Grype | Container + filesystem scan | CLI, CI |
| OWASP Dependency-Check | Java-focused, CVSS scoring | CI, Maven/Gradle |

### DAST (Dynamic Application Security Testing)

| Tool | Type | Best For |
|---|---|---|
| OWASP ZAP | Open-source | CI integration, API testing |
| Burp Suite | Commercial | Manual + automated testing |
| Nuclei | Template-based | Custom vulnerability checks |
| Nikto | Web server scanner | Quick server assessment |

---

## 3. Vulnerability Management

### Vulnerability Lifecycle

```
Discovery → Triage → Prioritize → Remediate → Verify → Close
```

### Prioritization Framework

| Factor | Weight | Consideration |
|---|---|---|
| CVSS score | High | Base severity |
| Exploitability | Critical | Is there a public exploit? |
| Asset criticality | High | Is this a crown jewel system? |
| Exposure | High | Internet-facing vs internal? |
| Data sensitivity | High | What data is at risk? |
| Compensating controls | Medium | Are there mitigations in place? |

### SLA by Severity

| Severity | Internet-Facing | Internal | Non-Production |
|---|---|---|---|
| Critical (9.0-10.0) | 24 hours | 72 hours | 1 week |
| High (7.0-8.9) | 1 week | 2 weeks | 1 month |
| Medium (4.0-6.9) | 1 month | 2 months | 3 months |
| Low (0.1-3.9) | 3 months | 6 months | Best effort |

---

## 4. Infrastructure Security Scanning

### IaC Security Scanning

| Tool | Supported IaC | Features |
|---|---|---|
| Checkov | Terraform, K8s, CloudFormation, Helm | 1000+ policies, custom rules |
| tfsec/Trivy | Terraform | Fast, focused on Terraform |
| KICS | Terraform, K8s, Docker, Ansible | Multi-IaC, comprehensive |
| Terrascan | Terraform, K8s, Helm | OPA-based policies |
| Snyk IaC | Terraform, K8s, CloudFormation | Fix suggestions |

### Cloud Security Scanning

| Tool | Clouds | Type |
|---|---|---|
| Prowler | AWS, GCP, Azure | CIS benchmarks, compliance |
| ScoutSuite | AWS, GCP, Azure | Multi-cloud audit |
| CloudSploit | AWS, GCP, Azure, Oracle | Open-source, continuous |
| AWS Config | AWS | Compliance rules, remediation |
| Security Command Center | GCP | Asset inventory, vulnerabilities |

---

## 5. Runtime Security

### Runtime Detection

| Tool | Type | Detection Method |
|---|---|---|
| Falco | Cloud-native | System call monitoring |
| Sysdig Secure | Enterprise | System calls + network |
| Aqua Security | Container | Runtime policies |
| CrowdStrike | Endpoint/Cloud | Agent-based, AI detection |
| Wiz Defend | Cloud workload | Agentless, cloud-native |

### Runtime Security Rules (Falco Examples)

```yaml
# Detect shell spawned in container
- rule: Terminal shell in container
  desc: A shell was spawned in a container
  condition: >
    spawned_process and container and
    proc.name in (bash, sh, zsh) and
    not proc.pname in (allowed_parent_processes)
  output: >
    Shell spawned in container
    (user=%user.name container=%container.name shell=%proc.name)
  priority: WARNING

# Detect sensitive file access
- rule: Read sensitive file
  desc: Attempt to read sensitive files
  condition: >
    open_read and container and
    fd.name in (/etc/shadow, /etc/passwd, /proc/*/environ)
  output: >
    Sensitive file read (file=%fd.name container=%container.name)
  priority: CRITICAL
```

### Security Monitoring and SIEM

| Component | Purpose | Tools |
|---|---|---|
| Log aggregation | Centralize security logs | ELK, Splunk, Loki |
| SIEM | Correlation, detection rules | Splunk, Elastic SIEM, Sentinel |
| SOAR | Automated response | Phantom, XSOAR, Tines |
| Threat intelligence | IOC feeds, context | MISP, OTX, VirusTotal |
| UEBA | User behavior anomaly detection | Exabeam, Securonix |
