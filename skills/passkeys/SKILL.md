---
name: passkeys
description: Comprehensive expertise in FIDO2 and WebAuthn standards, covering passkey implementation, registration, authentication, recovery, and enterprise deployment strategies.
---

# Passkeys Master Specialist

## When to Use

Use this skill when tasks involve:
- Implementing passwordless authentication using FIDO2 and WebAuthn standards.
- Designing registration, authentication, and recovery workflows for passkeys.
- Configuring Conditional UI (autofill) for seamless passkey adoption.
- Managing synced (multi-device) vs. device-bound (single-device) credentials.
- Integrating passkeys with Identity Providers (IdPs) or Single Sign-On (SSO) solutions.
- Auditing passkey implementations for security vulnerabilities, compliance (NIST AAL2/AAL3, PSD2, HIPAA), and best practices.
- Troubleshooting WebAuthn API errors (e.g., `NotAllowedError`, `SecurityError`).

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple platforms to implement | Platform Integrator | Parallel implementation for iOS, Android, and Web |
| Multiple IdPs to configure | IdP Configurator | Parallel setup of OIDC and WebAuthn settings |
| Bulk credential migration | Migration Agent | Parallel processing of user credential upgrades |
| Comprehensive security audit | Security Auditor | Parallel review of registration, authentication, and recovery flows |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirements Gathering**: Determine the target platforms (Web, iOS, Android), required Authenticator Assurance Level (AAL), and fallback/recovery policies.
2. **Architecture Design**: Choose between synced passkeys (consumer apps) and device-bound passkeys (high-security enterprise). Define the Relying Party ID (RP ID) and origin rules.
3. **Implementation**:
   - **Registration**: Configure `PublicKeyCredentialCreationOptions` with secure challenges, appropriate `authenticatorSelection`, and `excludeCredentials`.
   - **Authentication**: Configure `PublicKeyCredentialRequestOptions` and implement Conditional UI (`mediation: "conditional"`).
   - **Server-Side Validation**: Implement strict verification of challenges, origins, RP ID hashes, signatures, and clone detection (sign counts).
4. **Testing**: Use virtual authenticators (e.g., via Chrome DevTools Protocol) for automated testing and perform manual testing across various devices and browsers.
5. **Deployment & Migration**: Roll out passkeys using a "Passkey First" strategy, prompting users to upgrade after password logins, and eventually deprecating passwords.

## Core Principles

- **Cryptographic Foundation**: Passkeys use asymmetric cryptography. The private key never leaves the authenticator; the server only stores the public key.
- **Phishing Resistance**: Credentials are cryptographically bound to the RP ID (domain), preventing use on fraudulent sites.
- **Data Minimization**: Store only necessary credential data (credential ID, public key, sign count, user ID). Do not store raw assertion data or full attestation objects post-verification unless required for audit.
- **Graceful Degradation**: Always provide fallback mechanisms (e.g., explicit login buttons, email/SMS recovery) for users without passkey support or who lose their devices.
- **User Experience**: Prioritize Conditional UI and clear, non-technical microcopy (e.g., "Sign in with your fingerprint or face") to drive adoption.

## Key References

- [Web Authentication: An API for accessing Public Key Credentials - Level 3](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance: Client to Authenticator Protocol (CTAP) 2.2](https://fidoalliance.org/specs/fido-v2.2-ps-20250714/fido-client-to-authenticator-protocol-v2.2-ps-20250714.html)
- [NIST Special Publication 800-63-4: Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
- [Google Identity: Passkeys developer guide for relying parties](https://developers.google.com/identity/passkeys/developer-guides)
- [FIDO Alliance: Passkey Index 2025 Performance Metrics](https://fidoalliance.org/passkeys/)
