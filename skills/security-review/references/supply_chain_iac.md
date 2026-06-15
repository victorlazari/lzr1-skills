# Supply Chain, Container, and IaC Hardening

This reference document outlines rules and patterns for identifying software supply chain vulnerabilities, container security misconfigurations, and Infrastructure as Code (IaC) flaws during a line-by-line code review. It maps directly to **OWASP Top 10 2025: A03 - Software Supply Chain Failures** [1] and **CWE-1399** [2].

---

## 1. Software Supply Chain Failures (OWASP A03)

Recent major incidents (such as the **Red Hat GitLab breach** [3] and the **@redhat-cloud-services npm compromise** [4]) highlight that modern applications are highly vulnerable to supply chain attacks.

### Dependency Confusion Attacks
- [ ] **Audit Package Registry Scopes**: Look for private package dependencies in package lockfiles (`package.json`, `requirements.txt`, `Pipfile`, `go.mod`). Ensure that internally developed, private packages are correctly scoped under a private registry namespace (e.g., `@myorg/private-pkg`) to prevent attackers from registering the same name on public registries (npm, PyPI) and forcing dependency confusion.
- [ ] **Check Lockfile Integrity**: Ensure lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`) are committed to version control and that integrity hashes (SHA-512) are verified during automated builds.

### Typosquatting & Malicious Packages
- [ ] **Check Package Names**: Scan dependencies for suspicious typos or minor spelling variations of popular libraries (e.g., `reqeusts` instead of `requests` or `lodash-es` vs `lodash`).
- [ ] **Audit Post-Install Scripts**: Look for package installation configurations that run custom scripts automatically during installation (e.g., npm's `preinstall` or `postinstall` hooks), as these are common vectors for executing malicious payload downloaders.

---

## 2. Container Security & Dockerfile Hardening

Misconfigured container images can lead to container escape, host compromise, and privilege escalation [5].

### Dockerfile Code Audit Checklist:
- [ ] **Verify Non-Root User**: Ensure that the Dockerfile does not run processes as the `root` user. Look for the explicit declaration of a non-privileged user (e.g., `USER node` or `USER appuser`). Running as root inside a container increases the risk of host-level privilege escalation in the event of a container breakout.
- [ ] **Verify Minimal Base Images**: Ensure that the Dockerfile uses minimal, hardened base images (e.g., Alpine Linux, Debian-slim, or Distroless) rather than full operating system distributions. This minimizes the attack surface and reduces the number of pre-installed vulnerable packages.
- [ ] **Check Multi-Stage Builds**: Verify that multi-stage builds are utilized to separate compile-time build dependencies (which may contain sensitive keys or tools) from the final runtime image.
- [ ] **Audit Exposed Ports**: Ensure that only necessary application ports are exposed (e.g., `EXPOSE 8080`) and that administrative or debug ports are never exposed.

---

## 3. Infrastructure as Code (IaC) & Cloud Security

Misconfigurations in Terraform, CloudFormation, or Kubernetes manifests are the leading cause of cloud data breaches [6].

### Terraform Security Checklist:
- [ ] **Check Publicly Accessible Buckets**: Ensure that S3 buckets or storage containers are not configured with public read/write access (e.g., `acl = "public-read"` or `public_access_block` disabled).
- [ ] **Audit Security Group Rules**: Look for firewall or security group rules that expose sensitive ports to the entire internet (e.g., opening port 22 for SSH or port 3306 for MySQL with CIDR block `0.0.0.0/0`).
- [ ] **Check Hardcoded Cloud Credentials**: Verify that cloud provider configurations do not hardcode access keys or secrets (e.g., `access_key = "AKIA..."` in AWS provider block).

### Kubernetes Manifests Checklist:
- [ ] **Check Privileged Containers**: Ensure that containers do not run with privileged access (e.g., `securityContext.privileged: true` must be omitted or set to `false`).
- [ ] **Audit RBAC Bindings**: Verify that ServiceAccounts or Users are not granted over-privileged ClusterRoles (such as `cluster-admin`) unless absolutely necessary. Follow the principle of least privilege.
- [ ] **Check Host Namespace Sharing**: Ensure that pods do not share the host's network, PID, or IPC namespaces (e.g., `hostNetwork: true` or `hostPID: true`).

---

## References

* [1] [OWASP Top Ten Web Application Security Risks 2025: A03 - Software Supply Chain Failures](https://owasp.org/Top10/2025/0x00_2025-Introduction/)
* [2] [CISA & NSA: Guidance on Software Supply Chain Security](https://community.f5.com/kb/technicalarticles/memory-safety-cisa-and-nsa-guidance-on-cwe-1399/325590)
* [3] [Guardz: Red Hat GitLab Breach and Customer Impact](https://guardz.com/blog/top-recent-data-breaches/)
* [4] [Palo Alto Networks Unit 42: @redhat-cloud-services npm Supply Chain Attack](https://unit42.paloaltonetworks.com/monitoring-npm-supply-chain-attacks/)
* [5] [Wiz Academy: Container Escape Detection and Prevention](https://www.wiz.io/academy/container-security/container-escape)
* [6] [Medium: Terraform Nightmares and Misconfigured IaC](https://medium.com/@instatunnel/terraform-nightmares-how-a-misconfigured-iac-can-expose-everything-09c4206864dd)
