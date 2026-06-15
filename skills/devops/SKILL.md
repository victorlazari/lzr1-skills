---
name: devops
description: Advanced DevOps specialist skill covering AWS, Kubernetes, EKS, Helm, Git, VPC, Networking, and CI/CD pipelines.
---

# DevOps Specialist

## When to Use
Use this skill when you need to:
- Architect, deploy, and maintain scalable and resilient cloud-native systems.
- Manage infrastructure using Infrastructure as Code (IaC) tools like Terraform and CloudFormation.
- Orchestrate containerized applications using Kubernetes and Amazon EKS.
- Automate software delivery through CI/CD pipelines (e.g., GitHub Actions, GitLab CI, AWS CodePipeline).
- Design secure and scalable Virtual Private Cloud (VPC) networks.
- Implement GitOps workflows and advanced deployment strategies (Blue/Green, Canary).
- Troubleshoot complex networking, deployment, or infrastructure issues.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple microservices to deploy | Deployment Agent | Parallel deployment of independent services |
| Multiple environments to provision | Infrastructure Provisioner | Parallel IaC execution across environments |
| Multiple repositories to configure | CI/CD Configurator | Parallel setup of CI/CD pipelines |
| Bulk infrastructure auditing | Security/Compliance Auditor | Parallel security review of cloud resources |
| Multi-cluster health checks | Cluster Diagnostics Agent | Parallel Kubernetes cluster investigation |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., deploying 3+ microservices).
- Each sub-agent receives: context, specific target (e.g., service name, environment), and success criteria.
- Results are aggregated and cross-referenced for conflicts or shared dependencies.
- Maximum concurrent sub-agents: 10.

## Workflow
1. **Requirement Analysis:** Understand the deployment, infrastructure, or troubleshooting requirements. Identify the target environment and constraints.
2. **Architecture & Design:** Design the solution using appropriate AWS services, Kubernetes resources, and networking configurations.
3. **Infrastructure Provisioning:** Use IaC (Terraform/CloudFormation) to provision or update the required infrastructure.
4. **Pipeline Configuration:** Set up or modify CI/CD pipelines to automate the build, test, and deployment processes.
5. **Deployment & Orchestration:** Deploy applications using Helm, Kubernetes manifests, or GitOps tools (Argo CD/Flux). Implement advanced deployment strategies if needed.
6. **Validation & Monitoring:** Verify the deployment success, monitor system health, and ensure observability (metrics, logs, traces).
7. **Documentation:** Document the architecture, deployment steps, and any rollback procedures.

## Core Principles
- **Infrastructure as Code (IaC):** All infrastructure must be defined declaratively and version-controlled.
- **Automation First:** Automate repetitive tasks, including testing, deployment, and scaling.
- **Security by Design (DevSecOps):** Implement least privilege IAM, secure secrets management, and continuous security scanning.
- **Immutability:** Prefer replacing infrastructure and containers over modifying them in place.
- **Observability:** Ensure comprehensive monitoring, logging, and tracing for all components.
- **Resilience & High Availability:** Design for failure across multiple Availability Zones and implement autoscaling.
- **GitOps:** Use Git as the single source of truth for infrastructure and application state.

## Key References
For detailed technical guidance, refer to the following resources:
- [Complete Reference](references/complete-reference.md): In-depth guide on AWS, Kubernetes, EKS, Helm, Git, VPC, CI/CD, and configuration schemas.
- [Reading List](references/reading-list.md): Curated list of recent books and articles on advanced DevOps practices.
