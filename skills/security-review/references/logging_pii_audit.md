# Log, Exception, and PII Auditing

This reference document outlines rules and patterns for identifying sensitive data leaks in logs, preventing log injection attacks, and auditing exception handling mechanisms. It incorporates guidelines from **OWASP Logging Cheat Sheet** [1] and **GDPR compliance standards** [2].

---

## 1. Preventing Sensitive Data Exposure in Logs

Logs are frequently stored in less secure, centralized systems (e.g., SIEMs, Elasticsearch, S3) and are accessible to a wider group of engineers. Therefore, logging sensitive data represents a critical vulnerability [3].

### Data Prohibited from Application Logs
Ensure that the application does not log any of the following sensitive fields:

| Category | Sensitive Fields (Prohibited in Logs) |
| :--- | :--- |
| **Credentials & Secrets** | Passwords, API keys, OAuth tokens, session IDs, private keys, MFA backup codes, JWT signatures |
| **Personally Identifiable Info (PII)** | Social Security Numbers (SSNs), national IDs, full names, email addresses, phone numbers, home addresses |
| **Financial Data** | Credit card numbers (PANs), CVVs, bank account numbers, routing numbers, transaction details |
| **Protected Health Info (PHI)** | Medical record numbers, health conditions, prescription details, insurance details |

### Code Audit Steps:
- [ ] **Scan Logger Invocations**: Look for logging statements (e.g., `console.log()`, `logger.info()`, `print()`, `log.Debugf()`) that dump entire request bodies, database models, or user objects (e.g., `logger.info(req.body)` or `logger.debug(user)`).
- [ ] **Check Log Masking/Redaction**: Verify that logging utilities or middleware have redaction rules configured to automatically mask high-risk keys (e.g., replacing `password: "admin123"` with `password: "********"`).
- [ ] **Check URL Parameter Logging**: Ensure that sensitive tokens or credentials are not passed via URL query parameters (e.g., `/api/reset?token=xyz`), as web servers (Nginx, Apache) automatically log complete request paths.

---

## 2. Preventing Log Injection Attacks (CWE-117)

If user-controlled data is written directly to logs without sanitization, an attacker can inject malicious content. This can lead to **log forging** (writing fake log entries to cover up malicious actions) or exploiting vulnerabilities in log viewers (such as the infamous **Log4Shell** vulnerability) [4].

### Log Injection Example (Vulnerable Code):
```javascript
// Vulnerable: Direct logging of unvalidated input
app.get('/login', (req, res) => {
    const username = req.query.username;
    logger.info("User login attempt: " + username); // Attacker can inject CRLF (\r\n) characters
});
```

If an attacker passes `username = "admin\r\n[INFO] User login success: admin"`, they can forge log entries to deceive administrators.

### Code Audit Steps:
- [ ] **Verify CRLF Stripping**: Ensure that any user-controlled input written to logs has newline (`\n`) and carriage return (`\r`) characters stripped or escaped.
- [ ] **Check Log Encoding**: Ensure that log formatting libraries automatically escape special characters or encode output in structured formats like JSON (which naturally escapes newlines).

---

## 3. Exception Handling & Stack Trace Leaks (OWASP A10, CWE-209)

Mishandling exceptions can lead to information disclosure or "fail open" logical conditions [5].

### Stack Trace Leaks (CWE-209)
- [ ] **Check Error Response Handlers**: Look for exception handlers that return raw error messages or stack traces directly to the client (e.g., `res.status(500).send(err.stack)` or `res.json({ error: err.message })`). Stack traces expose internal paths, database schemas, and framework versions, helping attackers plan exploits.
- [ ] **Verify Graceful Error Handling**: Ensure that the application catches exceptions and returns generic, user-friendly error messages (e.g., `"An unexpected error occurred. Please try again later."`) while logging the detailed stack trace internally for developers.

### Failing Open vs. Failing Closed
- [ ] **Audit Try-Catch Logical Blocks**: Ensure that if an exception occurs inside an authorization or payment check, the block fails closed (e.g., denying access or rolling back the transaction) rather than bypassing the check.

```javascript
// Vulnerable: Failing Open on Exception
try {
    const isAuthorized = checkAuth(user);
    if (!isAuthorized) {
        return res.status(403).send("Forbidden");
    }
} catch (err) {
    logger.error("Auth check failed: " + err.message);
    // VULNERABILITY: Execution continues, allowing access even if auth server is down!
}
proceedToSensitiveResource();
```

---

## References

* [1] [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
* [2] [GDPR Compliance: Protecting Personal Data in Log Files](https://lantern.splunk.com/Security_Use_Cases/Compliance/Detecting_PII_in_log_data_for_GDPR_compliance)
* [3] [OWASP MASWE-0001: Insertion of Sensitive Data into Logs](https://mas.owasp.org/MASWE-0001/)
* [4] [OWASP Community: Log Injection Vulnerability](https://owasp.org/www-community/attacks/Log_Injection)
* [5] [OWASP Top 10 2025: A10 - Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/0x00_2025-Introduction/)
