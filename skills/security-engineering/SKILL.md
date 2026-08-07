---
name: security-engineering
description: Comprehensive cybersecurity skill covering application security, cloud security, DevSecOps, security architecture, and compliance. Use when performing security reviews, designing secure systems, implementing security controls, conducting threat modeling, or responding to security incidents. Routes deep code review to security-review and incident communication to post-mortem-master.
---

# Security Engineering

Expert-level cybersecurity covering the full security spectrum: application security, cloud security, security architecture, DevSecOps, and compliance.

## Scope and Triggers

**Use this skill for:**
- Threat modeling and security architecture design
- Cloud security posture management
- DevSecOps pipeline implementation
- Compliance frameworks (SOC 2, ISO 27001, PCI DSS, HIPAA)
- Application security principles and vulnerability assessment

**Escalation Boundaries:**
- For exhaustive, line-by-line code security audits, secret scanning, or IaC checks, route to `security-review`.
- For writing customer-facing incident reports or communication slide decks, route to `post-mortem-master`.
- For adopting a specific security persona (e.g., penetration-tester) for a broader workflow, route to `ai-teammates`.

## Preconditions

Before executing security tasks, detect the target environment, permissions, and user intent.
- **Read-only vs. Mutation:** Identify if the task requires read-only discovery (scanning, auditing) or mutation (remediation, blocking, policy changes).
- **Permissions:** Ensure sufficient permissions are available for the required actions.

## Source Freshness

Security standards and vulnerabilities evolve rapidly. Do not rely on hardcoded facts (e.g., specific OWASP Top 10 versions or crypto algorithms).
- Always verify current standards and best practices from the canonical sources linked in the references.
- Record the verification date during execution.

## Workflow

1. **Detect Domain:** Identify the specific security domain(s) required by the task (AppSec, Cloud, DevSecOps, Architecture, Compliance).
2. **Load References:** Load the corresponding reference file(s) to understand the principles and required controls.
3. **Verify Standards:** Verify current standards and best practices from the canonical sources linked in the references.
4. **Discovery:** Perform read-only discovery or assessment based on the verified standards.
5. **Plan & Confirm:** If remediation or mutation is required, generate a plan and request explicit user confirmation before executing any destructive or production-impacting actions.
6. **Execute:** Apply changes using dry-runs where possible (e.g., `terraform plan`), stopping if errors occur.
7. **Synthesize:** Synthesize findings into a structured output contract detailing risks, evidence, and actionable recommendations.

## Safety

- **Separate Discovery from Mutation:** Always perform read-only discovery before attempting any mutation.
- **User Confirmation:** Require explicit user confirmation before executing any destructive, external, privileged, or production-impacting actions (e.g., isolating instances, changing IAM policies).

## Validation

- Validate all IaC/policy changes with dry-runs before applying.
- Ensure all scripts or commands fail securely and return non-zero exit codes on error.

## Failure Handling

- If an action fails, diagnose the error, choose an alternative approach, or roll back changes.
- Do not repeat a failed action unchanged.

## Output Contract

The final output must be a structured synthesis detailing:
- Identified risks and vulnerabilities
- Evidence supporting the findings
- Severity and confidence levels
- Actionable remediation recommendations

## Resources

- `references/application-security.md`: Application security principles, secure coding, and API security.
- `references/cloud-security.md`: Cloud security posture, IAM, and network security.
- `references/security-architecture.md`: Threat modeling, zero trust, and cryptography.
- `references/devsecops.md`: Security automation, pipeline integration, and supply chain security.
- `references/compliance.md`: Compliance frameworks, audits, and governance.

## Orchestration

When multiple domains are involved, process them logically. If parallel processing is used for independent dimensions, ensure a synthesis step maps compliance requirements to architectural gaps to DevSecOps pipeline holes, constructing the full kill chain across domains.

## Source freshness

Package guidance was **verified against upstream on 2026-08-07**. Re-check linked official sources at runtime before relying on volatile versions, flags, limits, prices, lifecycle dates, or hosted-service behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [scripts/verify-owasp.sh](scripts/verify-owasp.sh) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
