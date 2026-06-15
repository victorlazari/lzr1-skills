---
name: security-review
description: Exhaustive, line-by-line code security review skill. Use for validating application code against security breaches, logical flaws, hardcoded credentials, sensitive logging leaks, and supply chain vulnerabilities. Informed by OWASP, CWE, SANS, and latest real-world incident analyses.
license: MIT
---

# Security Review Skill: Line-by-Line Code Auditor

This skill provides an exhaustive, systematic, and line-by-line code auditing workflow to identify, isolate, and remediate application security breaches, structural flaws, hardcoded secrets, and logging leaks. It integrates industry-standard frameworks including the **OWASP Top 10 2025** [1], **CWE Top 25 2025** [2], **OWASP API Security Top 10 2023** [3], and lessons learned from the most significant recent security incidents [4] [5].

## Core Audit Principles

When running this skill, you must adopt the persona of a paranoid Principal Security Engineer and SRE. Do not make assumptions about the safety of any line of code. Every line of code must be validated under the assumption that its inputs are controlled by an active adversary.

1. **Verify Every Single Row**: Do not skip boilerplate, utility functions, or test files. Misconfigured test files or sandbox environments are frequent catalysts for real-world breaches [5].
2. **Zero-Trust Input & Boundaries**: Any variable coming from an external boundary (HTTP request, database query, environment variable, third-party API, or message queue) is considered hostile and untrusted.
3. **Fail-Safe Defaults**: Ensure that all logical operations and access controls fail closed, not open.
4. **Information Minimization**: Ensure that no internal implementation details, credentials, or personally identifiable information (PII) are leaked through logs, error messages, or API responses.

---

## Exhaustive Security Review Workflow

The security review process is divided into five rigorous phases. You must execute each phase in sequence and document findings meticulously.

```
┌─────────────────────────────────────────────────────────┐
│              PHASE 1: Static Secret Scanning            │
│  - Run regex matching for API keys, tokens, & hashes    │
│  - Scan .env, lockfiles, and git history configuration  │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│              PHASE 2: Data Flow & Sink Auditing         │
│  - Trace user inputs from Sources to Sinks              │
│  - Validate SQLi, XSS, Path Traversal, OS Injection     │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│           PHASE 3: Logical & Auth Review (IDOR/BOLA)    │
│  - Verify horizontal/vertical privilege enforcement     │
│  - Validate state transitions, multi-step workflows     │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│          PHASE 4: Logging, Exceptions & PII Audit       │
│  - Audit log statements for plaintext credential leaks  │
│  - Prevent log injection and raw stack trace leaks      │
└────────────────────────────┬────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────┐
│           PHASE 5: Supply Chain & IaC Security          │
│  - Check lockfiles, dependency confusion, and versions  │
│  - Audit Dockerfiles, Terraform, and K8s manifests      │
└─────────────────────────────────────────────────────────┘
```

---

## Audit Reference Directories

To keep this skill lean and highly effective, the detailed check-patterns, detection rules, and automated scripts are split into specialized child reference files. You must read and apply the patterns defined in these references during the audit:

1. **Secret & Credential Leakage Patterns**: Refer to [`references/secrets_patterns.md`](references/secrets_patterns.md) for exhaustive regular expressions and entropy-based rules to detect hardcoded API keys, OAuth tokens, and private keys.
2. **Vulnerability Detection Checklists**: Refer to [`references/vulnerability_checklists.md`](references/vulnerability_checklists.md) for a line-by-line code audit guide covering OWASP Top 10 2025, CWE Top 25, and API Security risks.
3. **Log, Exception, and PII Auditing**: Refer to [`references/logging_pii_audit.md`](references/logging_pii_audit.md) for rules on preventing PII leaks, credential logging, and log injection attacks.
4. **Supply Chain, Container, and IaC Hardening**: Refer to [`references/supply_chain_iac.md`](references/supply_chain_iac.md) for dependency confusion, typosquatting, Docker, and Terraform security audits.

---

## Execution Guidelines for the Auditor

When executing a code audit, you must generate a structured **Security Audit Report** containing:

1. **Executive Summary**: A high-level assessment of the application's security posture and critical risks.
2. **Vulnerability Table**: A structured pipe table mapping discovered issues to their CWE/OWASP identifiers, severity, affected files/lines, and impact.
3. **Line-by-Line Findings**: Detailed analysis of each vulnerable line of code, explaining the exploit scenario and providing the exact remediated code block.
4. **Remediation & Hardening Roadmap**: Concrete, actionable steps to secure the application, including dependency updates, configuration changes, and secure coding practices.

> "Security is not a product, but a process." Ensure that every line of code is held to the highest standard of verification. Use this skill to protect, guard, and harden our applications against the world's most sophisticated threat vectors.

---

## References

* [1] [OWASP Top Ten Web Application Security Risks 2025](https://owasp.org/Top10/2025/en/)
* [2] [MITRE 2025 CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html)
* [3] [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
* [4] [Hornetsecurity: Major Security Incidents of 2025 and Lessons Learned](https://www.hornetsecurity.com/en/blog/cybersecurity-incidents/)
* [5] [Guardz: Top 10 Data Breaches of 2025 and What Caused Them](https://guardz.com/blog/top-recent-data-breaches/)
