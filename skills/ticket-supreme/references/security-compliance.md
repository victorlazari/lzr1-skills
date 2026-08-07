# Security and Compliance for Enterprise Ticketing Systems

Verified against upstream: 2026-08-07

## Access Control

- **Role-Based Access Control (RBAC):** Implement RBAC to restrict access based on user roles (e.g., agent, admin, customer).
- **Row-Level Security (RLS):** Use RLS to restrict access to specific rows in the database based on user context.

## Data Protection

- **PII Redaction:** Automatically redact Personally Identifiable Information (PII) from tickets and logs.
- **Encryption:** Encrypt data at rest and in transit using industry-standard algorithms.

## AI-Specific Security Risks

- **Prompt Injection:** Validate and sanitize all user inputs to prevent prompt injection attacks against LLMs.
- **Data Leakage:** Ensure LLMs do not expose sensitive information or PII in their outputs.
- **Model Poisoning:** Protect training data and fine-tuning processes from malicious manipulation.

## Primary Sources

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [ITIL 4 Foundation](https://www.axelos.com/certifications/itil-service-management/itil-4-foundation)
