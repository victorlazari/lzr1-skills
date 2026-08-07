# Application Security

## Table of Contents
1. OWASP Top 10
2. Secure Coding Practices
3. Code Review for Security
4. Vulnerability Classes
5. API Security
6. Penetration Testing
7. AI/Agentic Security Concepts

---

## 1. OWASP Top 10

**Canonical Source:** [OWASP Top 10](https://owasp.org/www-project-top-ten/)
**Verification:** Verify the current OWASP Top 10 list from the canonical source at runtime. Do not rely on hardcoded lists.

### OWASP API Security Top 10

**Canonical Source:** [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
**Verification:** Verify the current OWASP API Security Top 10 list from the canonical source at runtime.

---

## 2. Secure Coding Practices

### Input Validation

All input is untrusted until validated:
1. Validate type (string, number, email, UUID)
2. Validate length (min/max)
3. Validate format (regex, allowlist)
4. Validate range (numeric bounds)
5. Sanitize for output context (HTML, SQL, URL, JS)
6. Reject rather than sanitize when possible

### Authentication Security

- Password hashing: Use current recommended algorithms (e.g., Argon2id).
- Rate limiting: Prevent brute force.
- Account lockout: Prevent credential stuffing.
- MFA: Second factor (TOTP, WebAuthn).
- Session management: Secure, HttpOnly, SameSite cookies.
- Token rotation: Limit token lifetime.

### Authorization Patterns

- RBAC: Role-based access control
- ABAC: Attribute-based access control
- ReBAC: Relationship-based access control
- PBAC: Policy-based access control

### Output Encoding

- HTML body: HTML entity encoding
- HTML attribute: Attribute encoding
- JavaScript: JS encoding
- URL: Percent encoding
- CSS: CSS encoding
- SQL: Parameterized queries

---

## 3. Code Review for Security

For exhaustive, line-by-line code security audits, route to the `security-review` skill.

### Security Review Checklist

- Authentication: Proper password handling, session management, MFA
- Authorization: Access checks on every endpoint, IDOR prevention
- Input validation: All inputs validated server-side, proper types
- Output encoding: Context-appropriate encoding, XSS prevention
- Cryptography: Strong algorithms, proper key management, no hardcoded secrets
- Error handling: No stack traces in production, generic error messages
- Logging: Security events logged, no sensitive data in logs
- Dependencies: Known vulnerabilities, pinned versions
- Configuration: No hardcoded secrets, secure defaults
- Data protection: Encryption at rest/transit, data minimization

---

## 4. Vulnerability Classes

### Injection Attacks

- SQL Injection: Parameterized queries, ORM
- NoSQL Injection: Input validation, typed queries
- Command Injection: Avoid shell; use libraries
- LDAP Injection: Input validation, escaping
- Template Injection: Sandboxed templates, no user templates
- Header Injection: Validate, reject newlines

### Cross-Site Scripting (XSS)

- Reflected: Output encoding, CSP
- Stored: Output encoding, sanitization
- DOM-based: Safe DOM APIs, no innerHTML

### Cross-Site Request Forgery (CSRF)

- Use anti-CSRF tokens (synchronizer token pattern)
- Use SameSite cookie attribute (Lax or Strict)
- Verify Origin/Referer headers
- Use custom headers for API requests (not sent cross-origin)

---

## 5. API Security

### API Security Controls

- Authentication: OAuth 2.0, API keys, JWT
- Authorization: Scope-based, RBAC
- Rate limiting: Token bucket per client
- Input validation: Schema validation (OpenAPI)
- Output filtering: Response field filtering
- Encryption: TLS 1.3+
- Logging: Request/response audit trail

### JWT Security

- Use asymmetric signing (RS256/ES256)
- Set short expiration
- Validate all claims (iss, aud, exp, nbf)
- Use refresh tokens for long sessions
- Never store sensitive data in payload
- Implement token revocation

---

## 6. Penetration Testing

### Penetration Testing Methodology

1. **Reconnaissance**: Gather information (OSINT, DNS, ports)
2. **Scanning**: Identify services, versions, vulnerabilities
3. **Exploitation**: Attempt to exploit identified vulnerabilities
4. **Post-exploitation**: Assess impact, lateral movement
5. **Reporting**: Document findings with severity and remediation

### Vulnerability Severity (CVSS)

**Canonical Source:** [FIRST CVSS](https://www.first.org/cvss/)
**Verification:** Verify current CVSS scoring guidelines from the canonical source.

---

## 7. AI/Agentic Security Concepts

**Canonical Source:** [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
**Verification:** Verify current LLM security risks from the canonical source.

- Prompt Injection: Manipulating LLM behavior via crafted inputs.
- Insecure Output Handling: Trusting LLM output without validation.
- Training Data Poisoning: Compromising the model's training data.
- Model Denial of Service: Overloading the model with complex requests.
- Supply Chain Vulnerabilities: Compromised models or dependencies.
- Sensitive Information Disclosure: LLMs revealing confidential data.
- Insecure Plugin Design: Vulnerabilities in LLM plugins/tools.
- Excessive Agency: Granting LLMs too much autonomy or permissions.
- Overreliance: Blindly trusting LLM outputs.
- Model Theft: Unauthorized access or exfiltration of models.
