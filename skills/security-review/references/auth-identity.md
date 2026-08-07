# Authentication and Identity Security Review Reference

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries

This reference provides deterministic, line-by-line code review guidance for authentication, authorization, session lifecycle, and identity management. It is designed to support the **identity and authorization specialist** in the parallel security-review protocol. The guidance focuses on identifying logical flaws, missing access controls, and insecure identity implementations across modern application architectures.

**Boundaries:** This is defensive code-review guidance, not an exploitation manual. It does not guarantee the absence of vulnerabilities or certify compliance. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization. The review must rely on static analysis and architectural understanding rather than active probing.

## Table of Contents

1. [Threat Assumptions](#threat-assumptions)
2. [Review Procedure](#review-procedure)
3. [Authentication & MFA](#authentication--mfa)
4. [Session Lifecycle & Tokens](#session-lifecycle--tokens)
5. [Authorization & Privilege Boundaries](#authorization--privilege-boundaries)
6. [Identity Evidence & False Positives](#identity-evidence--false-positives)
7. [Validation & Regression Checks](#validation--regression-checks)
8. [Stop & Escalation Rules](#stop--escalation-rules)
9. [Official References](#official-references)

## Threat Assumptions

The security review operates under a strict Zero Trust assumption, meaning network location does not imply trust. Every request must be explicitly authenticated and authorized, regardless of whether it originates from an internal network or the public internet.

We assume that passwords and bearer tokens may be stolen or intercepted. Therefore, multi-factor authentication (MFA) and step-up authentication are critical defenses. Attackers will actively attempt to hijack sessions by intercepting or fixating session identifiers. Furthermore, attackers will systematically attempt to bypass horizontal privilege boundaries (BOLA/IDOR) and vertical privilege boundaries to escalate their access.

In modern federated architectures, we must also assume that services acting on behalf of a user may be tricked into misusing their privileges, leading to confused deputy attacks. Token theft is a constant threat, as JWTs and OAuth tokens can be extracted from insecure storage or intercepted in transit. Finally, attackers will leverage automated tools to perform brute-force attacks and credential stuffing, exploiting weak account recovery mechanisms to gain unauthorized access.

## Review Procedure

The review procedure follows a structured, deterministic path to ensure comprehensive coverage of identity and access management controls.

First, identify all identity boundaries by mapping every entry point, API, and service that handles authentication or authorization. This includes both user-facing interfaces and machine-to-machine communication channels.

Next, trace the session state by following the lifecycle of session tokens, such as JWTs or cookies, from their creation upon successful authentication to their eventual revocation or expiration.

Verify access controls by ensuring that every endpoint enforces explicit authorization checks. The application must adhere to a default-deny posture, where access is blocked unless explicitly granted.

Assess the implementation of MFA and passkeys, validating that multi-factor authentication is robust and that modern passkey support aligns with current standards.

Check OAuth and OIDC flows for potential confused deputy vulnerabilities and token validation flaws. Scrutinize account recovery mechanisms, such as password resets, for potential bypasses or information leakage.

Review service identities to ensure that machine-to-machine communication uses secure, short-lived credentials with least privilege access. Finally, document all findings meticulously, recording the evidence, severity, and actionable remediation steps for any identified gaps.

## Authentication & MFA

### Passwords and Account Recovery

Passwords must be hashed using strong, modern algorithms such as Argon2id or bcrypt, with unique salts applied to each password. Account recovery flows must be designed to not reveal account existence, preventing user enumeration. These flows must use secure, time-limited, single-use tokens.

Applications must implement robust rate limiting and account lockout mechanisms to prevent brute-force and credential stuffing attacks.

| Requirement | Description |
|---|---|
| Password Hashing | Use Argon2id or bcrypt with unique salts. |
| Account Recovery | Use secure, time-limited, single-use tokens. Do not reveal account existence. |
| Rate Limiting | Implement rate limiting and account lockout mechanisms. |

**Anti-patterns:** Using predictable security questions or sending plaintext passwords via email are critical anti-patterns. Allowing unlimited password guess attempts without rate limiting or account lockout mechanisms is unacceptable. Returning different error messages for valid versus invalid usernames during login or password reset enables username enumeration and must be avoided.

### MFA and Passkeys

Multi-factor authentication should be enabled by default for all accounts, with a particular emphasis on administrative roles. Applications must support syncable authenticators, such as passkeys, aligned with NIST SP 800-63-4 guidelines. Ensure that MFA bypass mechanisms, like backup codes, are securely generated, stored, and transmitted.

It is highly recommended to implement step-up authentication for sensitive actions, such as changing passwords or executing financial transactions.

| Requirement | Description |
|---|---|
| Default MFA | Enable MFA by default, especially for administrative roles. |
| Passkeys | Support syncable authenticators aligned with NIST SP 800-63-4. |
| Step-up Auth | Implement step-up authentication for sensitive actions. |

**Anti-patterns:** Relying solely on SMS-based OTPs without offering stronger alternatives like TOTP or FIDO2 is an anti-pattern. Allowing users to disable MFA without requiring re-authentication poses a significant security risk.

## Session Lifecycle & Tokens

### JWT and Bearer Tokens

JSON Web Tokens (JWTs) must be signed using strong algorithms, such as RS256, and the signature must be explicitly verified on every request. Tokens must have a short expiration time (`exp`) and include audience (`aud`) and issuer (`iss`) claims to prevent misuse. Implement token revocation mechanisms, such as blocklists or short-lived access tokens paired with refresh tokens.

| Requirement | Description |
|---|---|
| Signature Verification | Sign JWTs with strong algorithms (e.g., RS256) and verify signatures on every request. |
| Token Claims | Include `exp`, `aud`, and `iss` claims. |
| Revocation | Implement token revocation mechanisms. |

**Anti-patterns:** Accepting the `alg: none` header or relying solely on symmetric keys (HS256) when asymmetric keys are appropriate are critical vulnerabilities. Storing sensitive data, such as PII or passwords, in the JWT payload is an anti-pattern, as the payload is merely encoded, not encrypted. Failing to validate the `exp`, `nbf`, and `iat` claims allows expired or invalid tokens to be accepted.

### Session Management

Session identifiers must be cryptographically random and must be regenerated upon any privilege level changes, such as logging in or escalating privileges. Implement robust device and session revocation mechanisms to allow users and administrators to terminate active sessions. Set secure cookie attributes, including `HttpOnly`, `Secure`, and `SameSite`, for all session cookies.

| Requirement | Description |
|---|---|
| Session IDs | Use cryptographically random session identifiers and regenerate them upon privilege changes. |
| Revocation | Implement robust device and session revocation mechanisms. |
| Cookie Attributes | Set `HttpOnly`, `Secure`, and `SameSite` attributes for session cookies. |

**Anti-patterns:** Storing sensitive session data in local storage instead of secure, HttpOnly cookies exposes the data to cross-site scripting (XSS) attacks. Failing to invalidate sessions on the server side upon user logout leaves the session active and vulnerable to hijacking. Allowing concurrent sessions from multiple devices without providing user visibility or control is an anti-pattern.

## Authorization & Privilege Boundaries

### RBAC, ABAC, and ReBAC

Applications must implement explicit, centralized authorization logic, such as Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), or Relationship-Based Access Control (ReBAC), rather than relying on scattered, ad-hoc checks. Enforce default-deny route coverage, ensuring that all endpoints require authorization unless explicitly marked as public. Authorization checks must be performed on the server side, not just on the client side.

| Requirement | Description |
|---|---|
| Centralized Logic | Implement explicit, centralized authorization logic (RBAC, ABAC, ReBAC). |
| Default-Deny | Enforce default-deny route coverage. |
| Server-Side Checks | Perform authorization checks on the server side. |

**Anti-patterns:** Hardcoding role checks directly in business logic instead of using a dedicated authorization service or middleware makes the authorization model brittle and difficult to audit. Relying on hidden fields or client-side state to determine user privileges is a fundamental security flaw.

### BOLA/IDOR and Confused Deputy

Validate that the authenticated user has explicit permission to access the specific resource requested to prevent Broken Object Level Authorization (BOLA) and Insecure Direct Object Reference (IDOR) vulnerabilities. In OAuth and OIDC flows, validate the `aud` and `azp` claims to prevent confused deputy attacks. Ensure that service-to-service communication uses dedicated service identities with least privilege access.

| Requirement | Description |
|---|---|
| Resource Validation | Validate user permission to access specific resources (BOLA/IDOR prevention). |
| Claim Validation | Validate `aud` and `azp` claims in OAuth/OIDC flows. |
| Service Identities | Use dedicated service identities with least privilege access. |

**Anti-patterns:** Trusting client-provided user IDs without server-side validation is a primary cause of BOLA vulnerabilities. Using predictable, sequential IDs for sensitive resources instead of UUIDs or opaque identifiers facilitates resource enumeration. Allowing a service to act on behalf of a user without verifying the user's consent and the service's authorization leads to confused deputy attacks.

## Identity evidence and false-positive control

Emit reports through the canonical contract in [`../templates/finding.schema.json`](../templates/finding.schema.json). The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. Put unresolved review questions in the report-level `unknowns` array and finding-specific uncertainty in `confidence.uncertainties`; do not convert missing gateway, middleware, token, tenant, or policy context into a confirmed finding.

Before confirming a missing control, trace whether authentication or authorization is enforced at an API gateway, service mesh, middleware layer, policy engine, data-access layer, or downstream service. Verify that the higher-level control actually covers the route, method, object, tenant, and failure mode. A custom token may provide equivalent properties, but equivalence must be supported by its issuer, verifier, audience, algorithm, replay, rotation, expiry, and revocation behavior. Clearly synthetic placeholders are not live credentials; ambiguous values remain redacted candidates until provenance is established.

When specialists disagree about control coverage or exploitability, create a conflict object, link the affected finding IDs, record both evidence paths, and use `disputed` while the conflict remains material. Never suppress the competing evidence.

## Validation and regression checks

Map the root cause to relevant CWE and OWASP categories, but do not let taxonomy replace reasoning. Recommend or perform only validation allowed by the authorization record. Safe examples include decision-table review and, when explicitly authorized, isolated tests covering allowed and denied principals, cross-tenant object access, token audience and issuer mismatches, expiration, replay, privilege changes, recovery, and policy-service failure. Use synthetic identities and data; do not test real credentials or production accounts.

A proposed test is recorded as `not-performed`. A performed test may be `passed`, `failed`, or `inconclusive`, with sanitized evidence and environment details. A finding may move to `mitigated` only when `validation.performed` is `true` and `validation.result` is `passed`. Monitoring and policy-review recommendations are operational follow-ups, not proof that the code-level root cause was removed.

## Stop and escalation rules

Stop the affected review path when the authentication design cannot be interpreted safely, code is materially obfuscated, active compromise is suspected, a real credential or universal bypass appears, or validation would require unauthorized execution, network access, identity use, or production interaction. Minimize secret exposure and preserve only redacted evidence.

Notify the coordinator or the Phase 0 user-designated contact; do not assume a particular security team exists. Independent read-only specialist work may continue when it remains authorized and safe. Do not test a discovered credential, revoke or rotate it, contact a vendor, publish a finding, or change a system without explicit authorization.

## Official References

1. [NIST SP 800-63-4 Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
2. [RFC 8725 JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html)
3. [RFC 9700 Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
4. [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/)
5. [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
6. [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
7. [NIST SP 800-204 Security Strategies for Microservices-based Application Systems](https://csrc.nist.gov/pubs/sp/800/204/final)
