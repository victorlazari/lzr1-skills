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

---

## Adversarial Verification Panel

For each significant security vulnerability produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong security vulnerabilities from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Platform Integrator, IdP Configurator, Migration Agent, Security Auditor) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Auditor recommending device-bound credentials while Platform Integrator implements synced passkeys for a target platform)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified passkey implementation and security audit report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
