# Security Review: Scoring and Prioritization

This reference document defines the deterministic scoring and prioritization matrix for security findings during line-by-line code reviews. It establishes the rules for evaluating finding status, confidence, severity, and exploitability, ensuring consistent and actionable results across all parallel review agents.

## Purpose and Boundaries

This document provides defensive code-review guidance for prioritizing identified vulnerabilities. It is **not** an exploitation manual. The scoring matrix is designed to support a bounded specialist agent in the parallel protocol and can also be followed sequentially. It must be used to evaluate findings objectively, without claiming certification or guaranteed absence of vulnerabilities. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization.

**Coordinator contract:** The coordinator validates and deduplicates structured findings, preserves contradictory evidence, applies the canonical schema, and produces a transparent priority view. CWE is required by the current schema; CAPEC, ATT&CK, CVSS v4, EPSS, KEV, NVD, CVE, and vendor advisories are added only when relevant and source-backed. Priority context never rewrites a CVSS base vector or silently changes finding evidence.

**Verified against upstream:** 2026-08-07

## Table of Contents
1. [Review Inputs and Threat Assumptions](#review-inputs-and-threat-assumptions)
2. [Deterministic Review Procedure](#deterministic-review-procedure)
3. [Finding Status and Confidence](#finding-status-and-confidence)
4. [Vulnerability Classification Mappings](#vulnerability-classification-mappings)
5. [CVSS v4 Scoring and Rationale](#cvss-v4-scoring-and-rationale)
6. [Runtime Context: EPSS and CISA KEV](#runtime-context-epss-and-cisa-kev)
7. [Exploit Preconditions and Compensating Controls](#exploit-preconditions-and-compensating-controls)
8. [Chained Findings and Deduplication](#chained-findings-and-deduplication)
9. [Severity Overrides and Uncertainty](#severity-overrides-and-uncertainty)
10. [SLA Policy Boundaries](#sla-policy-boundaries)
11. [False-Positive Controls and Validation](#false-positive-controls-and-validation)
12. [Stop and Escalation Rules](#stop-and-escalation-rules)
13. [Code and Configuration Patterns](#code-and-configuration-patterns)
14. [Authoritative References](#authoritative-references)

## Review Inputs and Threat Assumptions

Inputs are the canonical structured findings and coverage ledgers from the authorized specialist dimensions defined in `../SKILL.md`, plus the target revision, declared environment, applicable policy, and user-provided business context. The coordinator must not infer deployment, exposure, asset criticality, or compensating controls when they are unknown.

Threat assumptions are system-specific. Treat external and cross-tenant input as untrusted, model compromised identities and internal paths where plausible, and record every assumption that materially changes severity or priority. “Zero trust” is an architectural principle, not evidence that every input is adversary-controlled or every internal boundary is exposed.

## Deterministic Review Procedure

The coordinator first validates each record, links conflicts bidirectionally, and separates findings, unknowns, and coverage gaps. It then deduplicates only when records describe the same control failure, asset, affected path or invariant, and remediation unit; merged records retain all distinct locations, evidence, authorship context, and disagreements.

Map the most specific supported CWE. Add CAPEC or ATT&CK only when an actual attack pattern or technique is relevant. Calculate CVSS v4 only for a vulnerability with sufficient system context, preserve the exact vector and per-metric rationale, and leave the object absent when scoring would be misleading. Add timestamped live context only for a specific identifier.

Prioritize using exploit preconditions, reachability, affected asset, blast radius, data and safety impact, chain effects, compensating controls, source freshness, and uncertainty. Keep the CVSS base score immutable; priority changes belong in the synthesis narrative or downstream policy system. Remediation dates come from the user’s policy, contract, or regulator—not this skill.

## Finding Status and Confidence

Each finding must be assigned a specific status and a confidence level to guide remediation efforts.

| Canonical status | Meaning |
| :--- | :--- |
| `candidate` | Evidence warrants review, but a material premise or validation step is missing. |
| `confirmed` | Evidence and reasoning support the control failure in the reviewed scope. |
| `disputed` | Material contradictory evidence remains in a linked open conflict. |
| `mitigated` | A control or fix was validated as passed; residual risk remains explicit. |
| `accepted-risk` | An authorized owner accepted the risk with `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. |
| `false-positive` | Evidence and validation show the original claim is not applicable or incorrect. |

| Canonical confidence | Meaning |
| :--- | :--- |
| `high` | Direct, internally consistent evidence supports the finding with no material unresolved alternative. |
| `medium` | Evidence supports the finding, but one or more contextual premises remain uncertain. |
| `low` | Heuristic or incomplete evidence suggests the issue and the record states what would raise confidence. |

Status and confidence are distinct. A confirmed finding can have medium confidence, and a high-confidence observation can still be disputed by equally strong contradictory evidence.

## Vulnerability Classification Mappings

The canonical schema requires at least one specific CWE. Use CAPEC only when an attack-pattern mapping is evidenced and ATT&CK only when an enterprise technique meaningfully describes the observed path; these taxonomies are not interchangeable. Verify identifiers against current upstream catalogs and do not select a broad mapping solely to fill a field. When no precise CWE exists, use the narrowest defensible category and explain the limitation in the reasoning or uncertainty record.

## CVSS v4 Scoring and Rationale

Use CVSS v4.0 only when a finding describes a scorable vulnerability and sufficient system context exists. Preserve the exact vector, optional base score, and a non-empty rationale for every selected metric; do not use CVSS as a general business-risk or policy-compliance score.

The required metrics include Attack Vector (AV), Attack Complexity (AC), Attack Requirements (AT), Privileges Required (PR), and User Interaction (UI). Evaluate Vulnerable System Impact with `VC`, `VI`, and `VA`, and Subsequent System Impact with `SC`, `SI`, and `SA`; do not collapse the two impact groups.

**When NOT to score:** A CVSS score should not be calculated for findings that are purely informational, represent defense-in-depth recommendations without a clear exploit path, or are confirmed false positives.

## Runtime Context: EPSS and CISA KEV

Live context is optional and identifier-specific. EPSS is a modelled probability that a published CVE will be exploited in the next 30 days; record both probability and percentile when retrieved and avoid a universal threshold. CISA KEV is strong evidence of known exploitation for a listed CVE, but it does not alter the CVSS vector, automatically make every deployment critical, or impose a remediation deadline on organizations outside an applicable mandate.

Query KEV, EPSS, CVE, NVD, or a vendor advisory only when the affected product and version are established. Record source, identifier, status, retrieval timestamp, and HTTPS URL. Preserve mismatches—such as a disputed affected version or conflicting vendor advisory—as uncertainty or conflict. Absence from a catalog is not evidence of no exploitation.

## Exploit Preconditions and Compensating Controls

The specific conditions required for an attacker to exploit the vulnerability must be carefully evaluated.

This includes assessing reachability and exposure to determine if the vulnerable code path is accessible from untrusted networks or unauthenticated users. Asset criticality must also be considered, evaluating whether the vulnerability affects a critical system, sensitive data repository, or core business function. Finally, the presence of compensating controls, such as a Web Application Firewall (WAF), network segmentation, or strict IAM policies, must be evaluated to determine if they mitigate the risk or increase the attack complexity.

## Chained Findings and Deduplication

The coordinator cross-references specialist findings to identify interaction effects. For example, an information disclosure combined with a missing authorization decision may form a distinct exploit chain. Preserve the contributing findings and create a separate chain finding only when its preconditions, reasoning steps, combined impact, remediation, and evidence can be stated independently. Score that chain only if CVSS v4 applies to the combined vulnerability and the required context is known.

A path-line-CWE tuple is a useful candidate fingerprint, not a sufficient merge key: one flaw may span several files, and separate authorization boundaries may share a line or CWE. Merge only after comparing asset, violated invariant, source/sink or decision path, preconditions, remediation unit, and evidence. Preserve all locations and evidence, choose no “most severe” position merely because it is larger, and create a conflict when material interpretations differ.

## Severity Overrides and Uncertainty

Never override or mutate a CVSS base vector to encode business criticality, KEV, EPSS, or compensating controls. Preserve the score as calculated and express environmental assumptions, priority changes, and uncertainty separately. If exploitability or impact is uncertain, use `medium` or `low` confidence as justified, list the missing facts and alternative explanations, and define the smallest safe validation that could raise confidence.

## SLA Policy Boundaries

This skill does not invent normative remediation SLAs. Record the applicable organization policy, contractual term, regulatory deadline, CISA BOD obligation, or user-approved risk process and cite it. If no policy is supplied, provide a relative priority with reasons and label any example timeframe as non-binding. Accepted risk is not a synonym for low severity: it requires the governed record defined by the schema and must expire or be reviewed.

## False-Positive Controls and Validation

Confirmation requires sufficient evidence and reasoning, not an exploit payload. Prefer direct code or configuration evidence, an immutable artifact digest, an authorized synthetic test result, or a current advisory matched to an established affected version. Never reproduce live secrets or production payloads.

For remediation, define a validation method, expected result, whether it was performed, result, and evidence. Propose regression coverage when appropriate, but do not edit tests, rules, baselines, or repositories without authorization. A false-positive record requires rejection rationale and a validation method; changing detection rules is a separate reviewed change that must not create a broad suppression.

## Stop and Escalation Rules

When encrypted, obfuscated, binary, generated, or unsupported material prevents review, mark that component as opaque or uncovered and notify the coordinator; continue independent authorized areas when safe. If actual secrets, regulated data, active compromise indicators, or an imminent production hazard appear, stop the affected action, preserve only redacted evidence, and notify the coordinator or user-designated Phase 0 contact. Do not validate credentials, contact an assumed security team, or take containment action without authorization.

## Code and Configuration Patterns

When evaluating findings, the agent must consider specific code and configuration patterns across relevant languages and platforms.

| Pattern Type | Description | Examples |
| :--- | :--- | :--- |
| Anti-Patterns | Code structures that frequently introduce vulnerabilities. | Raw SQL concatenation, hardcoded secrets in source files, disabled TLS verification. |
| Secure Patterns | Recommended approaches for mitigating specific risks. | Parameterized queries, secrets management via environment variables or vaults, strict input validation. |
| Configuration Flaws | Misconfigurations in infrastructure or deployment settings. | Open S3 buckets, overly permissive IAM roles, exposed management interfaces. |

## Authoritative references

Use the complete source-to-check, version, and freshness matrix in `sources.md`; record runtime retrieval timestamps for living catalogs.

*   [1] [FIRST CVSS v4.0 Specification Document](https://www.first.org/cvss/v4.0/specification-document)
*   [2] [FIRST Exploit Prediction Scoring System (EPSS)](https://www.first.org/epss/)
*   [3] [CISA Known Exploited Vulnerabilities (KEV) Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
*   [4] [MITRE Common Weakness Enumeration (CWE)](https://cwe.mitre.org/)
*   [5] [MITRE Common Attack Pattern Enumeration and Classification (CAPEC)](https://capec.mitre.org/)
*   [6] [MITRE ATT&CK Framework](https://attack.mitre.org/)
*   [7] [NIST National Vulnerability Database (NVD)](https://nvd.nist.gov/)
*   [8] [CVE Program](https://www.cve.org/)

This is a living reference. Refresh FIRST, CISA, MITRE, NIST, CVE, and vendor material when it can affect a conclusion, record retrieval time for runtime context, and route schema or scoring-policy changes through review. The coordinator’s output remains an evidence-backed assessment, not a guarantee or certification.

The procedure is designed to make inputs, metric rationales, assumptions, and decisions reproducible. Independent reviewers may still disagree about evidence or context; preserve those positions as conflicts rather than forcing identical scores or priority. Repeatability means another reviewer can trace the result, not that judgment is eliminated.

Runtime context such as EPSS and KEV may change relative priority over time, but this package performs point-in-time review rather than continuous monitoring. Record the context and timestamp used for the report; any recurring refresh belongs in a separately authorized automation with explicit ownership and failure handling.

In addition to applicable scoring metrics, the coordinator considers only the business context supplied or evidenced for the reviewed scope when prioritizing findings. For example, a vulnerability in a legacy system that is scheduled for decommissioning may be assigned a lower priority than a similar vulnerability in a newly deployed, mission-critical application. This contextual awareness ensures that remediation resources are allocated where they will have the greatest impact on reducing overall risk.

The prioritization process must remain transparent. Never override the recorded CVSS base vector or score; document any separate business-priority decision, policy-derived target date, assumptions, source timestamps, and approver so stakeholders can trace the result without conflating vulnerability severity with organizational risk treatment.
