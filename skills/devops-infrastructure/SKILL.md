---
name: devops-infrastructure
description: Comprehensive DevOps and infrastructure engineering skill covering cloud architecture (AWS, GCP, Azure), Kubernetes, CI/CD pipelines, Infrastructure as Code (Terraform, Pulumi), site reliability engineering (SRE), platform engineering, networking, and database administration. Use when designing cloud infrastructure, managing Kubernetes clusters, building CI/CD pipelines, implementing IaC, troubleshooting production systems, or making infrastructure decisions.
---

# DevOps & Infrastructure Engineering

Expert-level DevOps, cloud infrastructure, and platform engineering covering the full operational spectrum: cloud architecture, Kubernetes orchestration, CI/CD automation, Infrastructure as Code, site reliability engineering, networking, database administration, and platform engineering.

## When to Use

- Designing or managing cloud infrastructure (AWS, GCP, Azure)
- Kubernetes cluster management, deployment, and troubleshooting
- Building or optimizing CI/CD pipelines
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- Site reliability engineering and incident management
- Platform engineering and developer experience
- Network architecture and troubleshooting
- Database administration and operations

## Workflow

1. **Assess the situation** — Understand the infrastructure requirement or issue
2. **Select reference** — Choose the appropriate domain:
   - Cloud architecture → `references/cloud-architecture.md`
   - Kubernetes → `references/kubernetes.md`
   - CI/CD and automation → `references/cicd-automation.md`
   - SRE and reliability → `references/sre-reliability.md`
   - Networking → `references/networking.md`
   - Database operations → `references/database-operations.md`
3. **Read the relevant reference** — Load domain-specific guidance
4. **Design or troubleshoot** — Apply patterns and best practices
5. **Implement** — Write IaC, configs, scripts, or runbooks
6. **Validate** — Test in staging, verify with monitoring

## Core Principles (All Infrastructure Work)

- Infrastructure as Code: All infrastructure must be version-controlled and reproducible
- Immutable infrastructure: Replace, don't patch; rebuild, don't repair
- Least privilege: Minimum permissions for every service, user, and role
- Defense in depth: Multiple security layers, never trust a single control
- Observe everything: Metrics, logs, and traces for every component
- Automate toil: If you do it more than twice, automate it
- Plan for failure: Everything fails; design for graceful degradation
- Document runbooks: Every alert must have a corresponding runbook

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| Cloud Architect | Multi-cloud design, cost optimization, well-architected | `references/cloud-architecture.md` |
| Kubernetes Engineer | K8s operations, Helm, service mesh, operators | `references/kubernetes.md` |
| DevOps Engineer | CI/CD, automation, GitOps, developer experience | `references/cicd-automation.md` |
| Site Reliability Engineer | SLOs, incident management, capacity planning | `references/sre-reliability.md` |
| Platform Engineer | Internal developer platforms, self-service, golden paths | `references/cicd-automation.md` |
| Network Engineer | Load balancing, DNS, VPN, firewall, service mesh | `references/networking.md` |
| Database Administrator | Replication, backup, performance, high availability | `references/database-operations.md` |

## Key References

- **Cloud architecture**: See `references/cloud-architecture.md` for multi-cloud design, cost optimization, and well-architected patterns.
- **Kubernetes**: See `references/kubernetes.md` for cluster operations, workload management, and troubleshooting.
- **CI/CD and automation**: See `references/cicd-automation.md` for pipeline design, GitOps, and platform engineering.
- **SRE and reliability**: See `references/sre-reliability.md` for SLOs, incident management, and capacity planning.
- **Networking**: See `references/networking.md` for network design, load balancing, and security.
- **Database operations**: See `references/database-operations.md` for DBA tasks, replication, and HA.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Parallel Execution Protocol

> **All 5 agents launch simultaneously.** Do not wait for one to finish before starting the next. Each agent receives the full task context and its dedicated reference file only.

### Agent Roster

| Agent | Dimension | Scope | Reference |
|---|---|---|---|
| **CI/CD Agent** | CI/CD & Automation | Pipeline configuration, secret management, artifact handling, deployment strategies | `references/cicd-automation.md` |
| **Cloud Arch Agent** | Cloud Architecture | Resource configuration, IAM policies, cost optimization, resilience patterns | `references/cloud-architecture.md` |
| **K8s Agent** | Kubernetes | Workload configuration, networking, resource limits, RBAC, cluster health | `references/kubernetes.md` |
| **Networking Agent** | Networking | DNS, load balancing, ingress, service mesh, firewall rules, latency | `references/networking.md` |
| **SRE Agent** | SRE & Reliability | SLOs/SLAs, alerting, runbooks, error budgets, incident management | `references/sre-reliability.md` |

### Spawning Rules

- **Trigger**: Every invocation of this skill — no exceptions
- **Concurrency**: All 5 agents launch in a single `parallel()` call
- **Context per agent**: Full task input + its dedicated reference file only (no cross-agent sharing during analysis)
- **Maximum concurrent agents**: 5

### Synthesis Agent

After all 5 agents report, run one **Synthesis Agent** with all reports that:

1. **Cross-references** findings across dimensions for interaction effects that no single agent could see
2. **Deduplicates** overlapping findings (same issue detected by multiple agents → one canonical entry)
3. **Prioritizes** the merged set by severity/impact
4. **Produces** a single unified output document

> Synthesis note for this skill: Build a cross-layer dependency graph: map how a networking misconfiguration cascades into K8s scheduling failures, and how those trigger SRE alerts. Identify single points of failure spanning multiple layers.

### Quality Gate

A finding from one agent that **contradicts** a finding from another agent must be flagged as `CONFLICT` and passed to the Synthesis Agent as a `MUST_RESOLVE` item — never silently dropped.
