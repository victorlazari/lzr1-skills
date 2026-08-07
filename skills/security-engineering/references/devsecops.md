# DevSecOps

## Table of Contents
1. DevSecOps Principles
2. Pipeline Security
3. Supply Chain Security
4. Infrastructure as Code (IaC) Security

---

## 1. DevSecOps Principles

DevSecOps integrates security practices into the DevOps software delivery lifecycle. The goal is to "shift left," identifying and addressing security issues as early as possible.

- **Automation:** Automate security testing and compliance checks to keep pace with rapid deployment cycles.
- **Continuous Monitoring:** Continuously monitor applications and infrastructure for vulnerabilities and misconfigurations.
- **Collaboration:** Foster collaboration between development, security, and operations teams.
- **Security as Code:** Define security policies and controls as code, allowing them to be version-controlled and automatically enforced.

---

## 2. Pipeline Security

Integrate security tools into the CI/CD pipeline to automatically detect vulnerabilities.

### Testing Types

- **Static Application Security Testing (SAST):** Analyzes source code for vulnerabilities without executing it. Run early in the pipeline (e.g., on pull requests).
- **Dynamic Application Security Testing (DAST):** Analyzes running applications for vulnerabilities by simulating attacks. Run in staging or testing environments.
- **Software Composition Analysis (SCA):** Identifies known vulnerabilities in third-party dependencies and open-source libraries.
- **Interactive Application Security Testing (IAST):** Combines SAST and DAST techniques, analyzing code from within the running application.
- **Secret Scanning:** Scans code repositories and commits for hardcoded secrets (API keys, passwords).

### Pipeline Hardening

- Secure the CI/CD infrastructure itself (e.g., Jenkins, GitLab CI, GitHub Actions).
- Implement least privilege for pipeline service accounts.
- Require multi-factor authentication for access to pipeline configuration.
- Audit pipeline execution logs.

---

## 3. Supply Chain Security

Securing the software supply chain is critical to prevent the introduction of vulnerabilities or malicious code through dependencies or build processes.

**Canonical Source:** [SLSA (Supply-chain Levels for Software Artifacts)](https://slsa.dev/)
**Verification:** Verify current SLSA requirements and levels from the canonical source.

**Canonical Source:** [NIST Secure Software Development Framework (SSDF)](https://csrc.nist.gov/projects/ssdf)
**Verification:** Verify current SSDF practices from the canonical source.

### Key Practices

- **Software Bill of Materials (SBOM):** Generate and maintain an SBOM for all applications to track dependencies.
- **Dependency Pinning:** Pin dependencies to specific versions to prevent unexpected updates that may introduce vulnerabilities.
- **Artifact Signing:** Sign build artifacts (e.g., container images, binaries) to ensure integrity and provenance. Verify signatures before deployment.
- **Vulnerability Management:** Continuously monitor dependencies for known vulnerabilities and apply patches promptly.

---

## 4. Infrastructure as Code (IaC) Security

IaC allows infrastructure to be defined and managed programmatically. Security must be integrated into the IaC lifecycle.

- **IaC Scanning:** Scan IaC templates (e.g., Terraform, CloudFormation, Kubernetes manifests) for misconfigurations and compliance violations before deployment.
- **Policy as Code:** Define security policies as code (e.g., using OPA/Rego) and enforce them during the CI/CD pipeline.
- **Drift Detection:** Monitor deployed infrastructure for configuration drift from the defined IaC templates.
- **Least Privilege:** Ensure IaC execution roles have only the permissions necessary to provision the defined resources.
