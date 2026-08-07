---
name: security-review
description: Performs exhaustive, evidence-backed security reviews of source code, configuration, tests, CI/CD, dependencies, infrastructure, cloud and container definitions, mobile clients, business logic, and AI or agentic integrations. Use when a user requests a deep repository audit, focused change review, architecture-informed vulnerability analysis, incident-informed review, remediation plan, or validation of security fixes. It coordinates bounded specialist reviews, validates findings adversarially, and produces traceable reports without claiming compliance or guaranteed vulnerability absence.
license: MIT
---

# Security Review

**Verified against upstream: 2026-08-07**

This skill is a defensive, evidence-driven code and system review workflow. It treats automated findings as leads, not proof, and requires every confirmed issue to connect observable evidence to an attack path, violated invariant, or control failure.

> This skill does not certify compliance, prove that a system is secure, or guarantee the absence of vulnerabilities. It reports what was reviewed, what was not reviewed, what evidence supports each conclusion, and what remains uncertain.

## When to activate

Use this skill for a complete repository security audit, a focused pull-request or change review, a threat-model-driven review, an incident-informed code investigation, a business-logic or authorization review, a supply-chain and build review, an infrastructure and cloud review, an AI or agentic-system review, or validation of proposed security fixes.

Do not use this skill as a substitute for authorized penetration testing, legal advice, privacy counsel, certification, or a production incident commander. Route specialized container, filesystem, SBOM, dependency, misconfiguration, and secret scanning to `trivy-scanner`. Route CodeRabbit CLI or pull-request review workflows to `coderabbit-reviewer`. This skill remains responsible for deep manual reasoning, cross-file chains, false-positive validation, and remediation evidence.

## Non-negotiable safety boundary

Start read-only. Do not execute target-project scripts, build hooks, package lifecycle scripts, downloaded binaries, containers, migrations, or generated commands merely because they appear in a repository. Do not upload source code, findings, secrets, logs, or proprietary artifacts to external services unless the user explicitly authorizes the exact destination and data scope.

Do not perform active tests against production by default. Require explicit authorization, a named target, a bounded method, and an agreed stop condition before any test that may alter state, consume resources, access another tenant, or trigger monitoring. Never print or reproduce a full secret. Redact evidence while preserving enough context or a digest for validation.

Do not modify the target until the user approves a bounded patch set. Separate discovery, confirmation, proposed remediation, mutation, and regression validation. Stop when authorization, scope, ownership, or environment safety is unclear.

## Required inputs

Establish the following before assigning review work:

| Input | Required record |
|---|---|
| Objective | Audit, focused review, remediation validation, incident-informed review, or evidence mapping |
| Target | Repository or artifact root, branch or commit, and expected trust boundary |
| Authorization | Who owns or controls the target and which actions are permitted |
| Environment | Local, CI, staging, production, offline, regulated, or otherwise constrained |
| Sensitive data | Secret, personal, payment, health, customer, or proprietary-data boundaries |
| Technology | Languages, frameworks, runtimes, package managers, cloud, orchestration, mobile, and AI integrations |
| Change context | Pull request, commit range, release, incident window, or full baseline |
| Exclusions | Explicitly excluded paths or tests, with reason and approver |
| Output needs | Human report, JSON findings, patch plan, control mapping, or validation evidence |
| Time and depth | Complete audit or explicitly bounded sample, with uncovered risk stated |

If an input is unavailable, record it as unknown. Never silently infer authorization or claim complete coverage from a partial target.

## Operating modes

| Mode | Use | Minimum output |
|---|---|---|
| Advisory review | Architecture, design, or proposed-code analysis without mutation | Threat model, risks, recommendations, unknowns |
| Complete repository audit | Full first-party code and configuration review | Scope manifest, coverage ledger, findings, residual risk |
| Focused change review | Commit, pull request, or release delta | Changed-surface analysis plus affected invariant review |
| Remediation validation | Verify an approved fix | Original evidence, patch reasoning, regression evidence, status |
| Incident-informed review | Trace a known indicator, behavior, or failure | Timeline assumptions, affected paths, containment and root-cause evidence |
| Control-evidence mapping | Map implementation evidence to a named framework | Evidence and gaps only; never a compliance declaration |

## Phase 0 — authorization and scope gate

Before reading sensitive contents or invoking tools:

1. Confirm target ownership or explicit authorization.
2. Classify the environment and prohibit active production tests unless separately approved.
3. Record whether external network access, external APIs, or hosted analysis are allowed.
4. Define allowed read, execute, test, write, and publish actions separately.
5. Establish secret-redaction, evidence-retention, and report-distribution rules.
6. Define the target revision so findings are reproducible.
7. Record stop conditions and a contact for ambiguous scope.

If the gate fails, provide a safe planning response and stop. Do not compensate for missing authorization with technical assumptions.

## Phase 1 — read-only inventory

Use reviewed, local, non-networking inspection only. The optional [inventory helper](scripts/inventory.py) classifies paths and metadata without reading file contents or executing the target. Review that script before use.

The inventory must account for:

- first-party source and generated source;
- tests, fixtures, fuzzers, and benchmarks;
- CI workflows, build scripts, release definitions, and hooks;
- package manifests, lockfiles, vendored dependencies, and registries;
- runtime configuration, feature flags, policies, and environment templates;
- database schemas, migrations, seeds, queues, and scheduled work;
- infrastructure as code, containers, Kubernetes, cloud permissions, and network policy;
- public APIs, internal APIs, webhooks, event schemas, and client contracts;
- mobile clients, desktop clients, browser extensions, and local storage;
- AI models, prompts, retrieval stores, tools, plugins, MCP servers, memory, and evaluation code;
- documentation that changes security behavior;
- binaries, archives, large media, inaccessible files, and submodules.

Produce a scope manifest with path, type, ownership if known, generated or vendored status, reviewability, and planned reviewer. Do not interpret a filename as evidence of a vulnerability.

## Phase 2 — threat model and coverage plan

Follow [threat modeling and evidence](references/threat-modeling-evidence.md). Identify assets, trust boundaries, identities, data classes, entry points, privileged operations, state transitions, external dependencies, administrative planes, tenant boundaries, and failure modes.

Create abuse cases and invariants before looking for defects. Examples include “a user can modify only resources in the authorized tenant,” “a payment transition occurs at most once,” “untrusted model output cannot authorize a tool call,” and “release artifacts are traceable to a reviewed build.”

Map each first-party reviewable file to one or more specialist dimensions. Map non-text, generated, vendored, inaccessible, or excluded material to an explicit coverage class rather than pretending it received line-by-line review.

## Phase 3 — specialist review protocol

### Conditional parallel execution

Use one bounded parallel batch only when all of the following are true:

- parallel execution is available;
- at least five specialist dimensions are genuinely independent for the target;
- every assignment has a complete input set and the same output schema;
- the full assignment list is known before dispatch;
- sensitive material remains within the authorized environment;
- synthesis and conflict ownership remain with one coordinator.

Dispatch all independent assignments in one batch. Do not split the same required batch into arbitrary waves. Parallelism reduces elapsed time; it does not relax evidence or coverage requirements.

If these conditions are not met, run the same applicable specialists sequentially in the table order. The sequential fallback must use identical inputs, evidence rules, output fields, and acceptance criteria.

### Ten-specialist roster

| Specialist | Governing reference | Required inputs | Minimum evidence and output |
|---|---|---|---|
| Application and API | [Application and API](references/application-api.md) | Route and parser inventory, trust boundaries, data flows, API contracts | Source-to-sink or invariant reasoning, exact location, safe validation, regression test |
| Identity and authorization | [Authentication and identity](references/auth-identity.md) | Identity model, session lifecycle, authorization graph, tenant boundaries | Principal, resource, action, policy decision, bypass preconditions, negative test |
| Secrets and cryptography | [Secrets and cryptography](references/secrets-cryptography.md) | Secret stores, key lifecycle, algorithms, protocols, artifact history | Redacted evidence or digest, exposure path, rotation need, crypto rationale |
| Logging and privacy | [Logging and privacy](references/logging-privacy.md) | Data classification, telemetry paths, retention, audit requirements | Sensitive field flow, purpose and access boundary, redacted log evidence |
| Business logic and distributed systems | [Business logic and distributed systems](references/business-logic-distributed.md) | State machines, invariants, transactions, queues, webhooks, retries | Violated invariant, interleaving or replay path, impact and concurrency test |
| Supply chain and build | [Supply chain and build](references/supply-chain-build.md) | Manifests, lockfiles, CI, build and release graph, provenance | Dependency or build trust path, immutable evidence, provenance gap, containment |
| Cloud, container, and IaC | [Cloud, container, and IaC](references/cloud-container-iac.md) | IAM, network, storage, workload identities, IaC and cluster policy | Effective privilege or exposure path, resource evidence, least-privilege fix |
| Mobile and client | [Mobile and client](references/mobile-client.md) | Client trust model, storage, IPC, links, network, update path | Device assumption, platform boundary, API impact, client and server remediation |
| AI, LLM, and agentic | [AI, LLM, and agentic](references/ai-llm-agentic.md) | Prompts, tools, retrieval, memory, model/data supply chain, approvals | Untrusted-data path, authority transition, tool boundary, evaluation and guardrail test |
| Evidence, scoring, and remediation | [Scoring](references/scoring-prioritization.md) and [remediation](references/remediation-validation.md) | Candidate findings, source freshness, environment, test evidence | Schema validation, conflict list, justified priority, bounded fix and validation plan |

Threat modeling is the coordinator’s preliminary pass, not an eleventh independent finding stream. The coordinator owns scope, coverage, deduplication, chained findings, conflict resolution, and final assertions.

### Assignment contract

Every specialist receives:

- immutable target revision and allowed paths;
- relevant threat-model assets, boundaries, abuse cases, and invariants;
- coverage entries assigned to that specialist;
- environment and authorization limits;
- current source-freshness record;
- the canonical finding schema;
- explicit exclusions and stop conditions.

Every specialist returns a structured record containing reviewed coverage entries, candidate findings, rejected hypotheses with reason, unknowns, conflicts, sources used, and validation not performed. Empty findings are valid only when coverage and testable hypotheses are recorded.

## Canonical finding contract

Use [the finding schema](templates/finding.schema.json) and validate the final JSON with [the report validator](scripts/validate_report.py). A finding is not confirmed merely because a tool, regex, checklist, or model flagged it.

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier independent of severity ordering |
| `title` | Specific violated control or invariant, not a generic category |
| `status` | Candidate, confirmed, disputed, mitigated, accepted-risk, or false-positive |
| `asset` | Component, service, data, identity, or artifact affected |
| `locations` | Exact file and line, configuration path, artifact digest, or reason unavailable |
| `evidence` | Minimal redacted excerpt, digest, trace, or reproducible observation |
| `reasoning` | Source-to-sink path, authorization decision, state invariant, or trust-chain failure |
| `preconditions` | Access, state, timing, deployment, feature, or attacker capability required |
| `impact` | Confidentiality, integrity, availability, privacy, financial, safety, or supply-chain effect |
| `taxonomy` | CWE where applicable; CAPEC or ATT&CK only when justified |
| `confidence` | High, medium, or low with uncertainty explanation |
| `cvss_v4` | Optional vector plus rationale for every selected metric; omit when unsupported |
| `live_context` | Optional KEV, EPSS, CVE, or advisory data with source and retrieval timestamp |
| `remediation` | Root-cause fix, alternatives, compatibility impact, and rollout constraints |
| `validation` | Negative test, regression test, configuration check, or evidence needed |
| `residual_risk` | Remaining exposure, compensating controls, and ownership |
| `conflicts` | IDs of top-level conflict objects that preserve contradictory evidence and reviewer positions |

Do not invent CVSS precision. Use [scoring and prioritization](references/scoring-prioritization.md), and record unknown metrics when evidence is insufficient. Refresh CISA KEV, EPSS, CVE, NVD, vendor advisories, and current tool or framework versions at execution time when they affect a decision.

## Evidence quality ladder

Prefer direct, reproducible evidence over inference:

1. reviewed code or configuration plus a complete path or violated invariant;
2. a safe local test against a synthetic or explicitly approved non-production target;
3. deterministic analyzer output corroborated by code reasoning;
4. dependency or artifact metadata verified against an authoritative source;
5. architecture documentation corroborated by implementation;
6. an unverified hypothesis, which must remain a candidate rather than a confirmed finding.

Preserve original evidence securely. Reports should contain the least sensitive redacted form that still allows another reviewer to validate the conclusion. Record hashes when exact content cannot be reproduced safely.

## Coverage accounting

Maintain a coverage ledger with one of these states for every inventoried item:

| State | Meaning |
|---|---|
| Reviewed | Human or specialist reasoning completed against file contents or effective configuration |
| Mechanically inventoried | Metadata classified, content not substantively reviewed |
| Generated | Generator or source reviewed; generated output sampled or excluded with reason |
| Vendored | Third-party material identified; provenance and usage reviewed separately |
| Binary or opaque | Not line-reviewable; origin, signature, digest, and use recorded where possible |
| Inaccessible | Permission, corruption, size, encryption, or tool limitation prevented review |
| Excluded | Explicitly out of scope with reason and approver |
| Not applicable | Dimension does not apply, with evidence supporting that conclusion |

A “complete” review means every inventory item has an honest state and every reviewable first-party item is mapped to a specialist. It never means that opaque or excluded material was silently treated as safe.

## Phase 4 — synthesis, deduplication, and conflict resolution

Normalize candidate findings to the canonical schema. Deduplicate by root cause, affected trust boundary, violated invariant, and overlapping evidence—not title similarity alone. Retain all contributing locations and specialist IDs.

Create a chained finding when multiple individually limited weaknesses produce a materially different attack path. Keep the component findings linked so remediation can break the chain at the correct point.

When reviewers disagree, record both positions, evidence, and the deciding test. Mark the finding `disputed` until the coordinator resolves it. Do not publish a final severity for an unresolved material conflict. Escalate when resolution requires production access, unavailable business rules, legal interpretation, or specialist expertise.

## Phase 5 — adversarial validation

For each candidate, try to disprove it safely:

- verify the effective code path and deployment condition;
- search for upstream validation, encoding, authorization, or compensating controls;
- distinguish test fixtures and documentation from runtime behavior;
- verify language, framework, and library semantics against current official documentation;
- check whether attacker-controlled data actually reaches the sink or invariant;
- test the negative case in a synthetic or explicitly authorized environment when feasible;
- confirm that the proposed fix addresses the root cause rather than the symptom;
- classify untestable assumptions and lower confidence rather than overstating certainty.

False positives remain in the audit trail with rejection reason. They do not appear as active vulnerabilities in the executive summary.

## Phase 6 — priority and remediation plan

Use the [scoring reference](references/scoring-prioritization.md) to combine technical severity, exposure, asset criticality, preconditions, exploit maturity, compensating controls, and environment. KEV or EPSS may affect urgency only when retrieved live and timestamped; neither replaces code evidence.

Use [remediation and validation](references/remediation-validation.md) to propose the smallest root-cause patch set. State compatibility effects, migration needs, rollout order, rollback, monitoring, and tests. Do not edit until the user approves the exact bounded patch set.

## Phase 7 — bounded remediation loop

After approval, run at most three remediation passes unless the user changes scope:

1. capture pre-change evidence and relevant tests;
2. apply one bounded patch set;
3. run targeted negative and regression tests;
4. re-review the changed path and adjacent invariants;
5. validate report state and residual risk;
6. stop or propose the next bounded pass.

Stop immediately on an unexpected critical finding, scope expansion, destructive migration, secret exposure, failed rollback, production impact, or lost authorization. Stop after two materially identical failures or when a pass makes no measurable progress. Do not weaken a test, suppression, policy, or security control merely to make a check pass.

Accepted risk requires owner, rationale, compensating controls, review date, and expiry. A finding without these remains unresolved.

## Package tools

All package tools are optional and local. Review them before execution.

| Tool | Purpose | Boundary |
|---|---|---|
| [Inventory helper](scripts/inventory.py) | Read-only path classification and JSON scope seed | Does not read contents, execute target code, or access the network |
| [Report validator](scripts/validate_report.py) | Validate findings JSON, statuses, evidence, conflicts, and optional CVSS shape | Does not judge whether a vulnerability is real |
| [Package self-check](scripts/self_check.py) | Validate metadata, links, JSON resources, and synthetic fixtures | Operates on this skill package only |

Never treat script success as proof of security. Never install a dependency or execute a repository-provided tool solely because this workflow mentions it.

## Deliverables

A complete engagement produces, as applicable:

1. authorization and scope record;
2. immutable target revision;
3. inventory and scope manifest;
4. threat model and abuse-case register;
5. coverage plan and final coverage ledger;
6. structured findings JSON;
7. rejected-hypothesis and unresolved-conflict log;
8. human-readable report based on [the report template](templates/security-report.md);
9. prioritized remediation and patch plan;
10. validation and regression evidence;
11. residual-risk and accepted-risk register;
12. source-freshness record with retrieval timestamps for volatile data.

The human report must distinguish confirmed findings, disputed findings, accepted risk, false positives, and unknowns. Its executive summary must reflect coverage limits and must not convert missing evidence into reassurance.

## Final quality gate

Before delivery, confirm that:

- authorization and environment constraints are documented;
- every inventory item has a coverage state;
- every confirmed finding satisfies the evidence contract;
- secrets and sensitive data are redacted;
- live intelligence is sourced and timestamped;
- CVSS vectors, when used, include metric rationale;
- duplicates and chains are resolved without losing locations;
- material reviewer conflicts are resolved or explicitly blocked;
- remediation is root-cause oriented and bounded;
- regression evidence is attached or marked not performed;
- accepted risk has owner and expiry;
- unknowns and exclusions are visible;
- no compliance, breach, or vulnerability-absence guarantee is made;
- the JSON report passes the local validator;
- the package passes its [self-check](scripts/self_check.py).

## Failure handling and stop conditions

Diagnose a failed action before choosing an alternative; do not repeat it unchanged. Preserve the last known-good evidence and patch state. If a tool is unavailable, continue with manual review or state the uncovered dimension. If evidence is contradictory, keep the finding disputed. If sensitive data appears unexpectedly, stop, minimize exposure, and follow the user’s incident-handling instructions.

End the review when the approved scope is accounted for, confirmed findings are reported, conflicts and unknowns are visible, and the agreed remediation or validation passes are complete. Do not continue looping merely to produce a cleaner-looking report.

## Resource index

### Governing sources and methods

- [Authoritative source map](references/sources.md)
- [Threat modeling and evidence](references/threat-modeling-evidence.md)
- [Scoring and prioritization](references/scoring-prioritization.md)
- [Remediation and validation](references/remediation-validation.md)

### Specialist references

- [Application and API](references/application-api.md)
- [Authentication, identity, and authorization](references/auth-identity.md)
- [Secrets and cryptography](references/secrets-cryptography.md)
- [Logging and privacy](references/logging-privacy.md)
- [Business logic and distributed systems](references/business-logic-distributed.md)
- [Supply chain and build](references/supply-chain-build.md)
- [Cloud, container, and infrastructure as code](references/cloud-container-iac.md)
- [Mobile and client](references/mobile-client.md)
- [AI, LLM, and agentic systems](references/ai-llm-agentic.md)

### Schemas, templates, and tests

- [Finding schema](templates/finding.schema.json)
- [Security report template](templates/security-report.md)
- [Expected synthetic findings](tests/expected-findings.json)
- [Synthetic fixture guide](tests/fixtures/README.md)
- [Synthetic vulnerable sample](tests/fixtures/vulnerable_sample.py)

### Local validation tools

- [Read-only inventory helper](scripts/inventory.py)
- [Findings report validator](scripts/validate_report.py)
- [Package self-check](scripts/self_check.py)
