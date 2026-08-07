---
name: passkeys
description: Implement passwordless authentication using FIDO2 and WebAuthn standards, including registration, authentication, and recovery workflows.
---

# Passkeys Master Specialist

## Scope and Triggers

Use this skill when tasks involve:
- Implementing passwordless authentication using FIDO2 and WebAuthn standards.
- Designing registration, authentication, and recovery workflows for passkeys.
- Configuring Conditional UI (autofill) for seamless passkey adoption.
- Managing synced (multi-device) vs. device-bound (single-device) credentials.
- Integrating passkeys with Identity Providers (IdPs) or Single Sign-On (SSO) solutions.
- Auditing passkey implementations for security vulnerabilities and compliance (NIST AAL2/AAL3).

**Cross-Skill Routes:**
- `security-review` — Route when performing a comprehensive security audit of an application's authentication flow.
- `identity-management` — Route when integrating passkeys with broader Identity and Access Management (IAM) or SSO solutions.

## Preconditions

Before acting, verify:
- Target platforms and AAL requirements.
- Fallback policies and recovery mechanisms.
- User intent regarding synced vs. device-bound passkeys.

## Source Freshness

Volatile facts, such as supported algorithms and attestation formats, must be verified against current upstream documentation.
*Verified against upstream: 2026-08-07*

## Workflow

1. **Assess requirements:** Determine target platforms, AAL requirements, and fallback policies.
2. **Design architecture:** Choose between synced and device-bound passkeys; define RP ID and origin rules.
3. **Implement registration:** Configure creation options with secure challenges and appropriate authenticator selection.
4. **Implement authentication:** Configure request options and implement Conditional UI.
5. **Validate server-side:** Implement strict verification of challenges, origins, signatures, and clone detection.
6. **Test and deploy:** Use virtual authenticators for testing; roll out using a "Passkey First" strategy.

## Safety and Validation

- **Safety:** Require confirmation before modifying existing credential storage schemas. Validate WebAuthn options against current specifications. Ensure fallback mechanisms are implemented before enforcing passkey-only authentication. Verify attestation requirements align with organizational policy.
- **Validation:** Implement strict verification of challenges, origins, signatures, and clone detection.

## Failure Handling

- If WebAuthn API errors occur (e.g., `NotAllowedError`, `SecurityError`), diagnose the issue using the error message and context.
- If unresolved, try alternative methods or tools, but NEVER repeat the same action.
- Ensure fallback mechanisms are available.

## Output Contract

The result must include:
- A clear explanation of the implemented passkey workflow.
- Evidence of successful registration and authentication.
- Actionable next steps for deployment and monitoring.

## Resources

- [Architecture](references/architecture.md): Detailed guidance on multi-tenant architecture, related origins (WebAuthn Level 3), and Zero Trust integration.
- [Security](references/security.md): Threat models, security checklists, and NIST SP 800-63-4 compliance for syncable and device-bound authenticators.
- [API Reference](references/api-reference.md): WebAuthn JavaScript API, server-side endpoints, and database schemas.
- [Implementation Patterns](references/implementation-patterns.md): Code templates for Node.js, Python, Go, and well-known files configuration.

## Package resource index

| Resource | Purpose |
|---|---|
| [scripts/validate-webauthn-config.sh](scripts/validate-webauthn-config.sh) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
