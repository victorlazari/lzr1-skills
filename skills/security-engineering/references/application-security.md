# Application Security

## Table of Contents
1. OWASP Top 10
2. Secure Coding Practices
3. Code Review for Security
4. Vulnerability Classes
5. API Security
6. Penetration Testing

---

## 1. OWASP Top 10 (2021)

| Rank | Category | Description | Mitigation |
|---|---|---|---|
| A01 | Broken Access Control | Unauthorized access to resources | RBAC, server-side checks, deny by default |
| A02 | Cryptographic Failures | Weak crypto, data exposure | TLS 1.3, AES-256, proper key management |
| A03 | Injection | SQL, NoSQL, OS, LDAP injection | Parameterized queries, input validation |
| A04 | Insecure Design | Missing security architecture | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Default configs, open cloud storage | Hardening, automated config scanning |
| A06 | Vulnerable Components | Known CVEs in dependencies | SCA scanning, dependency updates |
| A07 | Auth Failures | Broken authentication | MFA, rate limiting, secure session mgmt |
| A08 | Data Integrity Failures | Untrusted deserialization, CI/CD | Signed artifacts, integrity checks |
| A09 | Logging Failures | Insufficient logging/monitoring | Structured security logs, alerting |
| A10 | SSRF | Server-side request forgery | Allowlists, network segmentation |

### OWASP API Security Top 10 (2023)

| Rank | Category | Description |
|---|---|---|
| API1 | Broken Object Level Authorization | Accessing other users' objects |
| API2 | Broken Authentication | Weak auth mechanisms |
| API3 | Broken Object Property Level Authorization | Exposing sensitive properties |
| API4 | Unrestricted Resource Consumption | No rate limiting |
| API5 | Broken Function Level Authorization | Admin functions accessible |
| API6 | Unrestricted Access to Sensitive Business Flows | Automated abuse |
| API7 | Server Side Request Forgery | SSRF via API |
| API8 | Security Misconfiguration | Permissive CORS, verbose errors |
| API9 | Improper Inventory Management | Undocumented/deprecated APIs |
| API10 | Unsafe Consumption of APIs | Trusting third-party APIs |

---

## 2. Secure Coding Practices

### Input Validation

```
All input is untrusted until validated:
1. Validate type (string, number, email, UUID)
2. Validate length (min/max)
3. Validate format (regex, allowlist)
4. Validate range (numeric bounds)
5. Sanitize for output context (HTML, SQL, URL, JS)
6. Reject rather than sanitize when possible
```

### Authentication Security

| Control | Implementation | Purpose |
|---|---|---|
| Password hashing | bcrypt/scrypt/Argon2id (cost ≥12) | Protect stored passwords |
| Rate limiting | Token bucket per IP/user | Prevent brute force |
| Account lockout | Temporary lock after N failures | Prevent credential stuffing |
| MFA | TOTP, WebAuthn, push notification | Second factor |
| Session management | Secure, HttpOnly, SameSite cookies | Prevent session hijacking |
| Token rotation | Refresh token rotation | Limit token lifetime |

### Authorization Patterns

| Pattern | Description | Use Case |
|---|---|---|
| RBAC | Role-based access control | Simple permission models |
| ABAC | Attribute-based access control | Complex, dynamic policies |
| ReBAC | Relationship-based access control | Social graphs, sharing |
| PBAC | Policy-based access control | Fine-grained, centralized |

### Output Encoding

| Context | Encoding | Library |
|---|---|---|
| HTML body | HTML entity encoding | DOMPurify, bleach |
| HTML attribute | Attribute encoding | Framework auto-escaping |
| JavaScript | JS encoding | JSON.stringify for data |
| URL | Percent encoding | encodeURIComponent |
| CSS | CSS encoding | Avoid user input in CSS |
| SQL | Parameterized queries | ORM/prepared statements |

---

## 3. Code Review for Security

### Security Review Checklist

| Category | What to Check |
|---|---|
| Authentication | Proper password handling, session management, MFA |
| Authorization | Access checks on every endpoint, IDOR prevention |
| Input validation | All inputs validated server-side, proper types |
| Output encoding | Context-appropriate encoding, XSS prevention |
| Cryptography | Strong algorithms, proper key management, no hardcoded secrets |
| Error handling | No stack traces in production, generic error messages |
| Logging | Security events logged, no sensitive data in logs |
| Dependencies | Known vulnerabilities, pinned versions |
| Configuration | No hardcoded secrets, secure defaults |
| Data protection | Encryption at rest/transit, data minimization |

### Common Vulnerability Patterns in Code

```python
# BAD: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_input}"

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))

# BAD: Path traversal
file_path = f"/uploads/{user_input}"

# GOOD: Validate and restrict path
safe_name = secure_filename(user_input)
file_path = os.path.join(UPLOAD_DIR, safe_name)
assert os.path.commonpath([UPLOAD_DIR, file_path]) == UPLOAD_DIR

# BAD: Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# GOOD: Environment variable or secrets manager
API_KEY = os.environ["API_KEY"]
```

---

## 4. Vulnerability Classes

### Injection Attacks

| Type | Vector | Prevention |
|---|---|---|
| SQL Injection | User input in SQL queries | Parameterized queries, ORM |
| NoSQL Injection | User input in NoSQL queries | Input validation, typed queries |
| Command Injection | User input in OS commands | Avoid shell; use libraries |
| LDAP Injection | User input in LDAP queries | Input validation, escaping |
| Template Injection | User input in templates | Sandboxed templates, no user templates |
| Header Injection | User input in HTTP headers | Validate, reject newlines |

### Cross-Site Scripting (XSS)

| Type | Description | Prevention |
|---|---|---|
| Reflected | Input reflected in response | Output encoding, CSP |
| Stored | Input stored and displayed | Output encoding, sanitization |
| DOM-based | Client-side DOM manipulation | Safe DOM APIs, no innerHTML |

### Cross-Site Request Forgery (CSRF)

- Use anti-CSRF tokens (synchronizer token pattern)
- Use SameSite cookie attribute (Lax or Strict)
- Verify Origin/Referer headers
- Use custom headers for API requests (not sent cross-origin)

---

## 5. API Security

### API Security Controls

| Control | Implementation | Purpose |
|---|---|---|
| Authentication | OAuth 2.0, API keys, JWT | Identify callers |
| Authorization | Scope-based, RBAC | Limit access |
| Rate limiting | Token bucket per client | Prevent abuse |
| Input validation | Schema validation (OpenAPI) | Reject malformed requests |
| Output filtering | Response field filtering | Prevent data leakage |
| Encryption | TLS 1.3 | Protect in transit |
| Logging | Request/response audit trail | Detection, forensics |

### JWT Security

| Best Practice | Description |
|---|---|
| Use asymmetric signing (RS256/ES256) | Verify without sharing secret |
| Set short expiration (15 min) | Limit window of compromise |
| Validate all claims | iss, aud, exp, nbf |
| Use refresh tokens for long sessions | Rotate and revoke |
| Never store sensitive data in payload | JWTs are base64, not encrypted |
| Implement token revocation | Blacklist or short-lived tokens |

---

## 6. Penetration Testing

### Penetration Testing Methodology

1. **Reconnaissance**: Gather information (OSINT, DNS, ports)
2. **Scanning**: Identify services, versions, vulnerabilities
3. **Exploitation**: Attempt to exploit identified vulnerabilities
4. **Post-exploitation**: Assess impact, lateral movement
5. **Reporting**: Document findings with severity and remediation

### Common Tools

| Category | Tools | Purpose |
|---|---|---|
| Recon | Nmap, Amass, Shodan | Discovery and enumeration |
| Web testing | Burp Suite, ZAP, ffuf | Web application testing |
| Exploitation | Metasploit, SQLmap | Vulnerability exploitation |
| Password | Hashcat, John the Ripper | Password cracking |
| Network | Wireshark, Responder | Network analysis |
| Cloud | ScoutSuite, Prowler | Cloud security assessment |

### Vulnerability Severity (CVSS)

| Score | Severity | Response Time |
|---|---|---|
| 9.0-10.0 | Critical | Immediate (24 hours) |
| 7.0-8.9 | High | 1 week |
| 4.0-6.9 | Medium | 1 month |
| 0.1-3.9 | Low | Next release |
