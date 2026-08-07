# Logging, Exceptions, and Privacy Audit

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries

This reference document defines the deterministic rules for auditing application code and configuration to prevent the exposure of sensitive data, personally identifiable information (PII), and internal system details through logging, exception handling, and telemetry mechanisms. It establishes the boundaries for privacy threat modeling and safe incident evidence collection, ensuring that logging practices do not inadvertently violate privacy frameworks or expose the system to log injection attacks.

This document is defensive code-review guidance, not an exploitation manual. It does not declare legal compliance or guarantee the absence of vulnerabilities. It supports the Privacy Agent in the bounded parallel protocol and can be followed sequentially when parallel execution is unavailable. The authorization, evidence, conflict, and synthesis rules in `../SKILL.md` remain controlling in both modes.

## Table of Contents

1. [Scope and Threat Assumptions](#scope-and-threat-assumptions)
2. [Deterministic Review Procedure](#deterministic-review-procedure)
3. [Sensitive Data Minimization](#sensitive-data-minimization)
4. [Log Injection Prevention](#log-injection-prevention)
5. [Exception Handling and Stack Traces](#exception-handling-and-stack-traces)
6. [Privacy Threat Modeling and Boundaries](#privacy-threat-modeling-and-boundaries)
7. [Validation and Regression Checks](#validation-and-regression-checks)
8. [Finding Evidence Requirements](#finding-evidence-requirements)
9. [Stop and Escalation Rules](#stop-and-escalation-rules)
10. [References](#references)

## Scope and Threat Assumptions

The scope of this audit includes all application logging statements, exception handling blocks, telemetry and tracing configurations, and audit event generation mechanisms across the codebase.

The primary threat assumptions are:
- Log storage systems (e.g., SIEMs, centralized logging platforms) are accessible to a wider audience than the application itself and may be compromised.
- Attackers can control input data that is subsequently logged, enabling log injection or forging.
- Unhandled exceptions or verbose error messages can leak internal system details, aiding attackers in reconnaissance.
- Telemetry and tracing data may inadvertently capture sensitive user information or credentials.

## Deterministic Review Procedure

The review procedure consists of the following deterministic steps, which must be executed sequentially for every file in the scope:

1. **Identify Log Sources:** Locate all instances of logging frameworks, custom logging functions, and telemetry/tracing integrations. This includes standard libraries, third-party packages, and custom wrappers.
2. **Analyze Log Content:** Examine the data being logged to ensure no sensitive information is included. Pay special attention to variables that may contain complex objects or dictionaries.
3. **Verify Input Sanitization:** Check that user-controlled input is sanitized or encoded before being written to logs to prevent injection. This applies to all input vectors, including HTTP headers, query parameters, and request bodies.
4. **Audit Exception Handling:** Review `try-catch` blocks and global error handlers to ensure stack traces and internal details are not exposed to users. Ensure that exceptions fail closed and do not bypass security controls.
5. **Assess Privacy Boundaries:** Evaluate logging against the applicable, user-supplied jurisdictional and organizational requirements plus the NIST Privacy Framework. Trace purpose, minimization, access, retention, deletion, legal hold, and data-subject workflows without declaring legal compliance. Where deletion or access rights apply, verify that relevant log records can be found and handled through an authorized process.
6. **Review Telemetry and Tracing:** Audit telemetry and tracing configurations to ensure they do not inadvertently capture sensitive user information or credentials. This includes reviewing the configuration of tools like OpenTelemetry, Datadog, and New Relic.
7. **Check Audit Events:** Verify that audit events are generated for critical actions (e.g., authentication, authorization, data access) and that they contain sufficient information for forensic analysis without exposing sensitive data.
8. **Evaluate Log Integrity and Availability:** Ensure that logs are protected against unauthorized modification or deletion and that they are reliably transmitted to centralized logging platforms.

## Sensitive Data Minimization

Applications must not log sensitive data, including credentials, PII, financial information, or protected health information (PHI).

### Prohibited Data Categories

| Category | Examples |
| :--- | :--- |
| **Credentials** | Passwords, API keys, OAuth tokens, session IDs, private keys, JWT signatures |
| **PII** | Social Security Numbers (SSNs), national IDs, full names, email addresses, phone numbers |
| **Financial Data** | Credit card numbers (PANs), CVVs, bank account numbers, routing numbers |
| **PHI** | Medical record numbers, health conditions, prescription details |

### Code Patterns and Anti-Patterns

**Anti-Pattern (Vulnerable):** Logging entire request bodies or user objects.
```javascript
// Vulnerable: Dumps the entire request body, potentially including passwords or PII.
logger.info("Received request: ", req.body);
```

**Pattern (Secure):** Logging specific, non-sensitive fields or using automated redaction.
```javascript
// Secure: Logs only the action and user ID, avoiding sensitive data.
logger.info(`User ${req.user.id} initiated password reset.`);
```

### False-Positive Controls

- Ensure that redaction mechanisms are correctly configured and do not inadvertently mask non-sensitive data required for debugging.
- Verify that logging of hashed or encrypted identifiers (e.g., user IDs) is permitted and does not constitute a privacy violation.

## Log Injection Prevention

User-controlled data must be sanitized or encoded before being written to logs to prevent log injection attacks (CWE-117).

### Code Patterns and Anti-Patterns

**Anti-Pattern (Vulnerable):** Direct logging of unvalidated input.
```java
// Vulnerable: Attacker can inject CRLF characters to forge log entries.
String username = request.getParameter("username");
log.info("Failed login attempt for user: " + username);
```

**Pattern (Secure):** Encoding or sanitizing input before logging.
```java
// Secure: Input is sanitized to remove CRLF characters.
String username = request.getParameter("username");
String sanitizedUsername = username.replaceAll("[\r\n]", "");
log.info("Failed login attempt for user: " + sanitizedUsername);
```

## Exception Handling and Stack Traces

Exception handling mechanisms must fail closed and must not expose raw stack traces or internal system details to users (CWE-209).

### Code Patterns and Anti-Patterns

**Anti-Pattern (Vulnerable):** Returning raw stack traces to the client.
```python
# Vulnerable: Exposes internal paths and framework versions.
@app.errorhandler(500)
def internal_error(error):
    return str(error), 500
```

**Pattern (Secure):** Returning generic error messages and logging details internally.
```python
# Secure: Returns a generic message to the user and logs the stack trace internally.
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}")
    return "An unexpected error occurred. Please try again later.", 500
```

## Privacy Threat Modeling and Boundaries

Logging practices must align with privacy frameworks such as GDPR and the NIST Privacy Framework. This includes adhering to principles of data minimization, purpose limitation, and storage limitation.

- **Data Minimization:** Only log the minimum amount of data necessary for debugging, auditing, or security monitoring.
- **Purpose Limitation:** Ensure that logs are used only for their intended purpose and are not repurposed for unauthorized tracking or profiling.
- **Storage Limitation:** Implement log retention policies to automatically delete or anonymize logs after a specified period.
- **Rights, Deletion, and Legal Hold:** Determine whether applicable rights require search, access, correction, restriction, or deletion of log data; confirm that authorized workflows can locate records while respecting security evidence, retention, and legal-hold constraints. Escalate jurisdiction-specific conclusions rather than treating this reference as legal advice.

## Validation and Regression Checks

- **Automated Scanning:** Use static analysis tools to detect hardcoded secrets and sensitive data patterns in log statements.
- **Authorized Dynamic Testing:** Only when the user has explicitly authorized the target and environment, use synthetic data in an isolated test system to verify structured logging and control-character handling. Never inject test records into production, shared telemetry, or third-party systems by default.
- **Code Review:** Manually review changes to logging configurations and exception handlers to ensure compliance with this reference.

## Canonical finding evidence requirements

Every report must conform to `../templates/finding.schema.json`. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`.

Do not require or reproduce a raw proof of concept containing personal data, credentials, production log records, stack traces, or forged events. Prefer a short redacted code excerpt, configuration evidence, a schema-level demonstration, or an authorized synthetic local fixture. Record the data category, source, transformations, destinations, audiences, retention, and relevant privacy boundary without copying the underlying value. A remediation code block is optional and must be accurate for the specific logging framework; the canonical remediation and validation fields are mandatory.

## Stop and Escalation Rules

- **Completion condition:** Mark this dimension complete only when the authorized inventory is accounted for and every uncovered logger, telemetry sink, exception path, generated configuration, or external collector is recorded as a coverage gap.
- **Escalation:** If actual secrets, regulated data, production log samples, active compromise indicators, or out-of-scope material appear, stop the affected action, minimize and redact evidence, and notify the coordinator or user-designated Phase 0 contact. Do not contact an assumed security team or external provider. Independent authorized read-only review may continue only when it does not increase exposure or interfere with incident handling.

## Authoritative references

Use the full version and freshness map in `sources.md`. Primary anchors for this dimension are the [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), [OWASP MASWE-0005: Insertion of Sensitive Data into Logs](https://mas.owasp.org/MASWE/MASVS-STORAGE/MASWE-0005/) and [MASTG-TEST-0296: Sensitive Data Exposure in Logs](https://mas.owasp.org/MASTG/tests/ios/MASVS-STORAGE/MASTG-TEST-0296/), [OWASP Log Injection guidance](https://owasp.org/www-community/attacks/Log_Injection), [OWASP Top 10:2025](https://owasp.org/Top10/2025/), the [NIST Privacy Framework](https://www.nist.gov/privacy-framework), [CWE-117](https://cwe.mitre.org/data/definitions/117.html), [CWE-209](https://cwe.mitre.org/data/definitions/209.html), and the official [EU GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj). Legal obligations depend on jurisdiction and facts; this reference identifies technical evidence and questions but does not provide legal conclusions.
