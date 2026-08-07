---
name: it-administration
description: Comprehensive IT administration skill covering endpoint management, identity and access management, IT security, SaaS administration, and IT operations for technology companies. Use when managing IT infrastructure, configuring identity providers, administering SaaS tools, handling IT security, or building IT policies and procedures.
---

# IT Administration

Expert-level IT administration covering endpoint management, identity and access management, IT security, SaaS administration, and IT operations for technology companies.

## Scope and Triggers

**Use this skill when:**
- Managing endpoints (laptops, devices, MDM)
- Configuring identity and access management (SSO, SCIM)
- Administering SaaS tools and licenses
- IT security hardening and compliance
- IT onboarding and offboarding automation
- Network and infrastructure management
- IT policy development and enforcement
- Helpdesk and IT support operations

**Escalation Boundaries:**
- For deep application or code-level security analysis, route to `security-review`.
- For building complex automated IT workflows or background processes, route to `automation-and-scheduling`.

## Preconditions

Before acting, detect the target environment, permissions, and user intent:
1. Identify the specific IT domain (endpoint, identity, security) based on the task context.
2. Verify current state and identify gaps against the latest frameworks (NIST CSF 2.0, CIS v8.1, CISA ZTMM V2.0).
3. Check required permissions and access levels for the target systems.

## Source Freshness

Volatile facts must be verified against current official documentation. Key authoritative sources include:
- NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
- CISA Zero Trust Maturity Model V2.0: https://www.cisa.gov/zero-trust-maturity-model
- CIS Critical Security Controls v8.1: https://www.cisecurity.org/controls/v8-1

## Workflow

1. **Detect Domain:** Identify the specific IT domain (endpoint, identity, security) based on the task context.
2. **Load Reference:** Load the corresponding updated reference file:
   - Endpoint and device management → `references/endpoint-management.md`
   - Identity and access management → `references/identity-access.md`
   - IT security and compliance → `references/it-security.md`
3. **Assess:** Verify the current state and identify gaps against the latest frameworks (NIST CSF 2.0, CIS v8.1, CISA ZTMM V2.0).
4. **Plan:** Formulate a plan with explicit safety checks and confirmation boundaries for any destructive actions.
5. **Execute:** Execute the plan, validating configurations against official documentation.
6. **Stop:** Stop when the IT administration task is complete and verified, outputting a structured report of changes made.

## Safety

- **Read-only discovery precedes mutation:** Always assess the current state before making changes.
- **Require confirmation:** Require confirmation before executing any destructive or production-impacting actions (e.g., wiping devices, revoking access, changing firewall rules).
- **Dry-run capabilities:** Ensure dry-run capabilities for automated provisioning/deprovisioning scripts.

## Validation

- Validate all configuration changes against current official documentation.
- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.

## Failure Handling

- If an action fails, diagnose the error using logs and documentation.
- Choose alternative methods or tools if the primary approach fails.
- Roll back changes if a critical failure occurs.
- Do not repeat a failed action unchanged.

## Output Contract

The result must include:
- A structured report of changes made.
- Evidence of validation and testing.
- Actionable next steps or recommendations.

## Resources

- `references/endpoint-management.md`: Endpoint and device management.
- `references/identity-access.md`: Identity and access management.
- `references/it-security.md`: IT security and compliance.

## Orchestration

Use parallel work only for independent dimensions. Define inputs, schemas, conflict handling, synthesis, and termination conditions.
