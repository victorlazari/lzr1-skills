---
name: devops
description: Advanced DevOps specialist skill covering AWS, Kubernetes, EKS, Helm, GitOps, VPC, Networking, and CI/CD pipelines. Triggers on infrastructure provisioning, deployment, or troubleshooting tasks.
---

# DevOps Specialist

## Scope and Triggers
Use this skill when you need to:
- Architect, deploy, and maintain scalable and resilient cloud-native systems.
- Manage infrastructure using Infrastructure as Code (IaC) tools like Terraform and CloudFormation.
- Orchestrate containerized applications using Kubernetes and Amazon EKS.
- Automate software delivery through CI/CD pipelines with ephemeral testing environments.
- Implement modern GitOps workflows (trunk-based development, directory-based environment separation, pull-based deployments).
- Troubleshoot complex networking, deployment, or infrastructure issues.

**Non-goals:** Do not use this skill for application code development or deep security vulnerability scanning (route to `security-review` or `trivy-scanner`).

## Preconditions
Before executing any action, verify:
1. **Target Environment:** Identify the target cloud provider, cluster, or repository.
2. **Permissions:** Ensure necessary IAM roles, Kubernetes RBAC, or Git credentials are available.
3. **Tool Versions:** Check installed versions of `terraform`, `kubectl`, `helm`, `kustomize`, etc.
4. **User Intent:** Confirm whether the task is a read-only audit or a mutating deployment.

## Source Freshness
Volatile facts (e.g., supported Kubernetes versions, Helm chart syntax, AWS service limits) must be verified against authoritative sources before executing actions. Record the verification date in the output.
- See `references/source-map.md` for canonical URLs.

## Workflow
1. **Requirement Analysis:** Identify target environment, constraints, and required resources.
2. **Precondition Check:** Verify access, permissions, and tool versions against authoritative sources.
3. **Architecture Design:** Design solution using IaC and modern GitOps practices (trunk-based, directory separation).
4. **Infrastructure Provisioning:** Run `scripts/validate-iac.sh`, request confirmation, then apply.
5. **Pipeline Configuration:** Set up CI/CD with ephemeral testing environments and pull-based deployments.
6. **Deployment:** Run `scripts/dry-run-deploy.sh`, request confirmation, then deploy using Helm/Kustomize.
7. **Validation:** Verify deployment success, monitor health, and run Cross-System Consistency Validator if sub-agents were used.
8. **Output Generation:** Produce structured output with evidence, confidence levels, and rollback procedures. Stop when all requirements are met and validated.

## Safety
- **Read-only Discovery:** Always perform read-only discovery (e.g., `terraform plan`, `kubectl get`) before any mutation.
- **Confirmation Required:** Explicit user confirmation is REQUIRED for any infrastructure provisioning, modification, or deletion, and for any production-impacting actions.

## Validation
- Validate IaC templates (Terraform/CloudFormation) before execution using `scripts/validate-iac.sh`.
- Verify Kubernetes manifests using `kubeval` or similar tools.
- Implement dry-run capabilities for all deployment scripts (`scripts/dry-run-deploy.sh`).
- Ensure rollback procedures are documented and tested.

## Failure Handling
- Fail fast on script errors with clear diagnostic output.
- If a deployment fails, do not repeat the same action unchanged. Diagnose the error using logs and events.
- Execute documented rollback procedures if a deployment leaves the system in an unstable state.

## Output Contract
The final output must include:
- **Action Summary:** What was deployed or modified.
- **Evidence:** Links to PRs, deployment logs, or infrastructure state.
- **Confidence Level:** HIGH/MEDIUM/LOW based on validation results.
- **Rollback Procedures:** Clear steps to revert the changes if necessary.
- **Next Steps:** Actionable recommendations for the user.

## Resources
- [Source Map](references/source-map.md): Mapping of authoritative sources to specific DevOps domains.
- [Complete Reference](references/complete-reference.md): In-depth guide on AWS, Kubernetes, GitOps, and CI/CD.
- [Validate IaC Script](scripts/validate-iac.sh): Syntax and smoke tests for Terraform/CloudFormation.
- [Dry-Run Deploy Script](scripts/dry-run-deploy.sh): Dry-run execution for Helm/Kubernetes deployments.
- [GitOps Repo Structure Template](templates/gitops-repo-structure.md): Template for directory-based environment separation.

## Orchestration (Parallel and Loop Protocol)

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed (e.g., deploying multiple microservices, provisioning multiple environments).

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant infrastructure and deployment finding produced by parallel sub-agents:
1. Spawn **3 independent Refuter Agents** per finding.
2. A finding is **confirmed** only if ≥2 refuters fail to refute it.
3. A finding is **discarded** if ≥2 refuters succeed.
4. Include dissenting arguments in the output with a `CONTESTED` label.

### Cross-System Consistency Validator
After all parallel agents complete, run one **Consistency Validator Agent** to:
- Flag logical contradictions between recommendations (`MUST_RESOLVE`).
- Note missing prerequisites (`SEQUENCING_REQUIRED`).

### Synthesis Agent
- Resolve `MUST_RESOLVE` contradictions.
- Re-order plan based on `SEQUENCING_REQUIRED` items.
- Calibrate confidence (HIGH/MEDIUM/LOW).
- Note any analysis blind spots.
