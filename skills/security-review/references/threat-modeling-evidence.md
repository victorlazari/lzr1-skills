# Threat Modeling and Evidence Review

## Purpose and Boundaries

This document provides defensive code-review guidance for threat modeling and evidence gathering. It is designed to support a bounded specialist agent in the parallel protocol and can also be followed sequentially. This is not an exploitation manual. Do not execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization. The primary objective is to systematically identify, document, and mitigate security risks through rigorous threat modeling and evidence-based review practices.

The scope of this document encompasses the entire lifecycle of threat modeling within the context of a security review. It provides actionable, deterministic procedures for identifying threats, gathering evidence, and reporting findings. It is intended to be used as a reference by security reviewers, developers, and automated agents to ensure a consistent and thorough approach to security assessments.

Verified against upstream: 2026-08-07

## Table of Contents

- [Purpose and Boundaries](#purpose-and-boundaries)
- [Review Inputs](#review-inputs)
- [Threat Assumptions](#threat-assumptions)
- [Deterministic Review Procedure](#deterministic-review-procedure)
  - [Define Authorization and Scope Gates](#define-authorization-and-scope-gates)
  - [Asset, Data, and Trust-Boundary Inventory](#asset-data-and-trust-boundary-inventory)
  - [Abuse Cases and Attacker Goals](#abuse-cases-and-attacker-goals)
  - [Data-Flow and State-Machine Modeling](#data-flow-and-state-machine-modeling)
  - [Line-Coverage Accounting](#line-coverage-accounting)
  - [Exclusion Classes](#exclusion-classes)
  - [Evidence Handling and Redaction](#evidence-handling-and-redaction)
  - [Chain-of-Custody](#chain-of-custody)
  - [Finding Schema and Confidence](#finding-schema-and-confidence)
  - [Conflicts and Threat-Model-Driven Review Planning](#conflicts-and-threat-model-driven-review-planning)
- [Code and Configuration Patterns](#code-and-configuration-patterns)
- [False-Positive Controls](#false-positive-controls)
- [Validation and Regression Checks](#validation-and-regression-checks)
- [Finding Evidence Requirements](#finding-evidence-requirements)
- [Stop and Escalation Rules](#stop-and-escalation-rules)
- [Official References](#official-references)

## Review Inputs

The review process requires a comprehensive set of inputs to ensure a thorough evaluation. These inputs form the foundation upon which the threat model is built and the security review is conducted. Without these inputs, the review may be incomplete or inaccurate.

The primary input is the application source code and configuration files. This includes all backend code, frontend code, infrastructure-as-code (IaC) templates, and deployment configurations. The reviewer must have access to the exact version of the code that is being deployed or evaluated.

Architecture diagrams and data flow models are essential for understanding the system's structure and how data moves through it. These diagrams should illustrate the various components of the system, their interactions, and the boundaries between different trust zones. If these diagrams do not exist, they must be created as part of the review process.

Existing threat models and risk assessments provide historical context and highlight previously identified concerns. Reviewing these documents helps the reviewer understand the evolution of the system's security posture and identify areas that may require further scrutiny.

Use live catalogs such as CISA KEV, EPSS, NVD, and CVE only when a finding concerns a specific vulnerable product, version, or identifier and the context may change prioritization. Refresh them at execution time, record the retrieval timestamp and identifier, and preserve “not found” as absence from that catalog—not proof of safety. Threat modeling for design and business-logic weaknesses does not require a CVE lookup.

## Threat Assumptions

A robust threat model relies on realistic assumptions about potential attackers and their capabilities. These assumptions guide the review process and help focus efforts on the most likely and impactful threats.

It is assumed that attackers have access to the application's public interfaces and will attempt to exploit any available entry points. This includes web interfaces, APIs, and any other exposed services. Attackers are assumed to be motivated and capable of discovering and exploiting vulnerabilities in these interfaces.

Attackers may actively attempt to bypass authorization and scope gates to gain unauthorized access to sensitive functions or data. This includes attempting to escalate privileges, access data belonging to other users, or perform actions outside of their intended scope. The review must carefully examine all authorization mechanisms to ensure they are robust and consistently applied.

Furthermore, attackers may exploit vulnerabilities in data-flow and state-machine implementations to manipulate the application's behavior. This includes injecting malicious data, manipulating state transitions, or exploiting race conditions. The review must analyze how data is processed and how the application manages state to identify potential weaknesses.

Insider threats and compromised credentials are also considered in scope, necessitating a defense-in-depth approach that does not rely solely on perimeter security. The review must consider scenarios where an attacker has already gained some level of access to the system, either through compromised credentials or as a malicious insider.

## Deterministic Review Procedure

The review procedure must be executed deterministically to ensure consistent and reliable results. The following steps outline the required process in detail.

### Define Authorization and Scope Gates

The reviewer must identify all entry points into the application and verify that authorization checks are consistently and correctly applied. This includes validating that users can only access resources and perform actions permitted by their assigned roles. The review must examine the implementation of role-based access control (RBAC) or attribute-based access control (ABAC) to ensure it aligns with the principle of least privilege.

### Asset, Data, and Trust-Boundary Inventory

A complete inventory of all sensitive assets, data flows, and trust boundaries must be mapped. This mapping is crucial for understanding where data is stored, how it is transmitted, and where it crosses boundaries between different levels of trust. The inventory should include databases, file systems, external APIs, and any other components that handle sensitive information.

### Abuse Cases and Attacker Goals

The review must define potential abuse cases and the specific goals an attacker might pursue. Understanding these goals helps prioritize the review efforts on the most critical areas of the application. Abuse cases should describe how an attacker might attempt to subvert the system's intended functionality, such as bypassing authentication, stealing data, or causing a denial of service.

### Data-Flow and State-Machine Modeling

The reviewer must analyze data flows and state transitions for potential vulnerabilities. This involves examining how data is processed and how the application transitions between different states, looking for flaws that could be exploited. The review should identify any instances where untrusted data is used to make critical decisions or where state transitions are not properly validated.

### Line-Coverage Accounting

Account for the authorized inventory using the coverage ledger in `../SKILL.md`: mechanically inventoried, manually reviewed, tool-only, excluded with rationale, or uncovered. Runtime test-coverage percentages are not a substitute for review coverage and must not be generated by executing target code without authorization. Record generated, vendored, binary, inaccessible, and out-of-scope components explicitly.

### Exclusion Classes

Any components or areas of the application that are excluded from the review must be explicitly identified and documented, along with the rationale for their exclusion. This transparency is essential for understanding the scope and limitations of the review. Exclusions may include third-party libraries, legacy systems, or components that are out of scope for the current assessment.

### Evidence Handling and Redaction

Evidence collected during the review must be handled securely. Any sensitive information, such as credentials or personally identifiable information (PII), must be redacted before the evidence is stored or shared. The reviewer must ensure that the evidence collection process does not inadvertently expose sensitive data or create new security risks.

### Chain-of-Custody

A clear chain of custody must be maintained for all evidence collected. This ensures the integrity and reliability of the evidence, which is essential for subsequent remediation efforts or incident response. The chain of custody should document who collected the evidence, when it was collected, and how it has been stored and handled.

### Finding Schema and Confidence

All reports must conform to `../templates/finding.schema.json`. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. Accepted risk additionally requires the governed `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at` record.

### Conflicts and Threat-Model-Driven Review Planning

Represent contradictory evidence as top-level conflict objects and link them from affected findings. The coordinator attempts resolution using evidence quality and scope context; unresolved conflicts remain explicit, and affected findings use `disputed` when appropriate. Do not force agreement or silently discard a specialist position. The resulting threat model may guide later reviews, but changing system documentation or policy remains a separate authorized action.

## Code and Configuration Patterns

### Patterns

Secure code and configuration patterns are essential for mitigating risks. The consistent use of parameterized queries is a critical pattern for preventing SQL injection vulnerabilities. This ensures that user input is treated as data rather than executable code.

Furthermore, the implementation of the principle of least privilege for all services and users ensures that entities only have the access necessary to perform their required tasks. This minimizes the potential impact of a compromised account or service.

Secure storage of secrets using dedicated secret management solutions, rather than hardcoding them, is another fundamental pattern that must be observed. Secrets should be injected into the application at runtime and should never be stored in source control.

### Anti-Patterns

Conversely, certain anti-patterns indicate potential security flaws. A credential-like literal is a severe anti-pattern that requires redacted evidence and careful classification. Do not authenticate with it, transmit it, contact its issuer, or include it in a live probe. Classify it only from already-authorized local context such as variable names, fixture markers, documentation labels, history already in scope, and non-sensitive provenance metadata; never reproduce the value. If classification would require use or external contact, leave it as an uncertainty and follow the package escalation path.

Missing or inconsistent authorization checks across different endpoints or functions suggest a systemic failure in access control. This can allow attackers to bypass security controls and access sensitive data or functionality.

Additionally, the improper handling of sensitive data in logs, such as logging passwords or PII in plaintext, is a significant anti-pattern that violates privacy and security requirements. Logs should be carefully reviewed to ensure they do not contain sensitive information.

## False-Positive Controls

To maintain the credibility of the review, false-positive controls must be implemented. Use the strongest safe evidence available and seek independent corroboration for high-impact or ambiguous claims. Static code and configuration evidence can be sufficient; live exploitation is not required. Manual or dynamic testing requires explicit authorization for the exact target and environment, and subject-matter consultation must not disclose proprietary material without approval.

Where possible, deterministic scripts should be used to validate findings, reducing the reliance on manual interpretation. These scripts can help automate the verification process and ensure consistent results.

Furthermore, findings should be cross-referenced with known false-positive patterns to filter out inaccurate results before they are reported. This helps ensure that the review focuses on genuine security risks rather than false alarms.

## Validation and Regression Checks

Validation and regression checks are necessary to ensure that vulnerabilities are effectively remediated and that new issues are not introduced. Automated tests should be implemented to validate fixes, providing a reliable mechanism for verifying that the vulnerability has been addressed.

Regression testing must be performed to ensure that the fix does not inadvertently break other functionality or introduce new vulnerabilities. This is particularly important for complex systems where changes can have unintended consequences.

Continuous monitoring for new threats and vulnerabilities is also required to maintain the application's security posture over time. This includes monitoring threat intelligence feeds, vulnerability databases, and security advisories.

## Finding Evidence Requirements

Every finding must use the canonical schema described above. Reproduction guidance must be the smallest safe validation plan and must not require exploitation, production traffic, untrusted-code execution, secret use, or external disclosure. Include repository-relative locations or immutable artifact digests, minimally sufficient redacted evidence, preconditions, explicit unknowns, alternative explanations, and the evidence needed to raise confidence. Impact and likelihood are reasoned separately; CVSS, EPSS, KEV, ATT&CK, CAPEC, or scanner output provide context but do not replace the reasoning record.

## Stop and Escalation Rules

Stop the affected action and notify the coordinator or user-designated Phase 0 contact when authorization is unclear, scope expansion is required, required evidence is unavailable, actual secrets or regulated data appear, material appears malicious, or validation could affect production, third parties, availability, or real data. Preserve redacted evidence and record coverage gaps or unknowns. A severe finding does not automatically halt independent authorized read-only dimensions, and it never authorizes contacting an assumed stakeholder or external party.

## Authoritative references

Use the complete source-to-check, version, and freshness matrix in `sources.md`. Primary anchors for this dimension include [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final), [NIST CSF 2.0](https://www.nist.gov/cyberframework), [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/), [OWASP SAMM](https://owasp.org/www-project-samm/), [MITRE ATT&CK](https://attack.mitre.org/), [MITRE CAPEC](https://capec.mitre.org/), and [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final). Refresh living taxonomies and catalogs only when they affect a conclusion and record their retrieval timestamps.
