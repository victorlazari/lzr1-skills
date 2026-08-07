---
name: devops-infrastructure
description: Comprehensive DevOps and infrastructure engineering skill covering cloud architecture, Kubernetes, CI/CD pipelines, Infrastructure as Code, SRE, platform engineering, networking, database administration, AI/MLOps, and FinOps. Use when designing cloud infrastructure, managing Kubernetes clusters, building CI/CD pipelines, implementing IaC, troubleshooting production systems, or making infrastructure decisions.
---

# DevOps & Infrastructure Engineering

Expert-level DevOps, cloud infrastructure, and platform engineering covering the full operational spectrum: cloud architecture, Kubernetes orchestration, CI/CD automation, Infrastructure as Code, site reliability engineering, networking, database administration, platform engineering, AI/MLOps, and FinOps.

## Scope and Triggers

- **Triggers**: Designing or managing cloud infrastructure, Kubernetes cluster management, building CI/CD pipelines, implementing IaC, site reliability engineering, platform engineering, network architecture, database operations, AI/MLOps infrastructure, and FinOps cost optimization.
- **Non-goals**: Application code development, frontend design, or business logic implementation.

## Preconditions

- Detect the target environment (AWS, GCP, Azure, on-prem).
- Verify installed tool versions (Terraform, kubectl, helm, etc.) against current official documentation.
- Ensure appropriate permissions are granted for the intended operations.

## Source Freshness

- Volatile facts (e.g., supported versions, specific tool commands) must be verified against upstream documentation.
- Check the `Verified against upstream` date in reference files.

## Workflow

1. **Assess the situation** — Understand the infrastructure requirement or issue.
2. **Select reference** — Choose the appropriate domain(s):
   - Cloud architecture → `references/cloud-architecture.md`
   - Kubernetes → `references/kubernetes.md`
   - CI/CD and automation → `references/cicd-automation.md`
   - SRE and reliability → `references/sre-reliability.md`
   - Networking → `references/networking.md`
   - Database operations → `references/database-operations.md`
   - Platform engineering → `references/platform-engineering.md`
   - FinOps → `references/finops-cost-optimization.md`
   - AI/MLOps → `references/ai-mlops-infrastructure.md`
3. **Parallel Execution (if multiple domains)** — Trigger the parallel execution protocol with relevant agents.
4. **Read the relevant reference** — Load domain-specific guidance.
5. **Design or troubleshoot** — Apply patterns and best practices.
6. **Implement** — Write IaC, configs, scripts, or runbooks.
7. **Validate** — Test in staging, verify with monitoring.
8. **Stop** — When the infrastructure requirement is met or the issue is resolved.

## Safety

- **Read-only discovery** must precede any mutation.
- **Destructive actions** (e.g., deleting resources, modifying production databases) require explicit user confirmation.
- Commands must use current syntax and quote user-controlled values.

## Validation

- Run syntax checks on IaC files (e.g., `terraform validate`, `helm lint`).
- Use dry runs (e.g., `terraform plan`, `kubectl apply --dry-run=client`) before applying changes.
- Verify postconditions using monitoring and observability tools.

## Failure Handling

- Diagnose errors using logs and traces.
- Do not repeat a failed action unchanged.
- Roll back to the previous known good state if a deployment fails.

## Output Contract

- Provide a structured implementation plan or troubleshooting report.
- Include evidence of validation (e.g., test results, dry run outputs).
- Specify actionable next steps.

## Resources

- `references/cloud-architecture.md`: Multi-cloud design, cost optimization, well-architected patterns.
- `references/kubernetes.md`: Cluster operations, workload management, troubleshooting.
- `references/cicd-automation.md`: Pipeline design, GitOps, platform engineering.
- `references/sre-reliability.md`: SLOs, incident management, capacity planning.
- `references/networking.md`: Network design, load balancing, security.
- `references/database-operations.md`: DBA tasks, replication, HA.
- `references/platform-engineering.md`: IDP best practices, Backstage, Humanitec.
- `references/finops-cost-optimization.md`: Cost benchmarking, rightsizing.
- `references/ai-mlops-infrastructure.md`: AI/ML workloads, GPU orchestration.

## Orchestration: Parallel Execution Protocol

> **All relevant agents launch simultaneously.** Do not wait for one to finish before starting the next. Each agent receives the full task context and its dedicated reference file only.

### Agent Roster

| Agent | Dimension | Scope | Reference |
|---|---|---|---|
| **CI/CD Agent** | CI/CD & Automation | Pipeline configuration, secret management, artifact handling | `references/cicd-automation.md` |
| **Cloud Arch Agent** | Cloud Architecture | Resource configuration, IAM policies, resilience patterns | `references/cloud-architecture.md` |
| **K8s Agent** | Kubernetes | Workload configuration, networking, resource limits, RBAC | `references/kubernetes.md` |
| **Networking Agent** | Networking | DNS, load balancing, ingress, service mesh, firewall rules | `references/networking.md` |
| **SRE Agent** | SRE & Reliability | SLOs/SLAs, alerting, runbooks, incident management | `references/sre-reliability.md` |
| **Platform Agent** | Platform Engineering | IDP setup, developer portals, self-service infrastructure | `references/platform-engineering.md` |
| **FinOps Agent** | FinOps | Cost analysis, rightsizing, budget alerts | `references/finops-cost-optimization.md` |
| **AI/MLOps Agent** | AI/MLOps | GPU provisioning, model serving infrastructure | `references/ai-mlops-infrastructure.md` |

### Spawning Rules

- **Trigger**: When multiple infrastructure domains are involved.
- **Concurrency**: All relevant agents launch in a single `parallel()` call.
- **Context per agent**: Full task input + its dedicated reference file only.

### Synthesis Agent

After all agents report, run one **Synthesis Agent** with all reports that:

1. **Cross-references** findings across dimensions.
2. **Deduplicates** overlapping findings.
3. **Prioritizes** the merged set by severity/impact.
4. **Produces** a single unified output document.

> Synthesis note: Build a cross-layer dependency graph. Identify single points of failure spanning multiple layers. Contradictory findings must be flagged as `CONFLICT` and resolved.

## Cross-Skill Routing

- `security-review`: Route when deep security validation, vulnerability scanning, or compliance auditing is required.
- `trivy-scanner`: Route when container image scanning or SBOM generation is needed.
- `automation-and-scheduling`: Route when setting up recurring tasks, background jobs, or external API integrations.
- `persistent-computing`: Route when deploying stateful services, game servers, or heavy compute workloads.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
| [scripts/check-versions.sh](scripts/check-versions.sh) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
