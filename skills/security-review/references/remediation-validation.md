# Remediation Design and Validation

**Verified against upstream: 2026-08-07**

## Purpose and boundary

This reference governs **proposed or authorized remediation** after a security finding has been triaged. It helps a reviewer determine whether a change addresses the root cause, preserves required behavior, can be rolled out and rolled back safely, and has enough evidence to change finding status. It does not authorize code mutation, command execution, deployment, production testing, credential use, or publication.

Use the authorization record established by [`../SKILL.md`](../SKILL.md). A review-only scope may produce a patch plan and validation plan, but must not edit the target. A scope containing `write` may permit local changes within the approved paths. `local-test`, `publish`, and production actions are separate permissions; none is implied by another.

> A proposed fix is not a validated fix. A passing test is not proof that every exploit path is closed. A mitigated status requires performed validation with a `passed` result under the canonical report contract.

## Inputs and preconditions

Before designing or validating a remediation, establish the exact target revision, affected assets and locations, violated security invariant, evidence and reasoning, exploit or failure preconditions, impact, uncertainty, and conflicts. Record the allowed actions, environment, included and excluded paths, compatibility constraints, service-level objectives, data-migration constraints, and the user’s rollout policy.

Do not invent missing deployment context, owner approval, tests, architectural intent, or regulatory requirements. A signed commit or approved pull request may be useful provenance, but it is not universally required and does not replace explicit task authorization.

| Input | Required treatment |
| :--- | :--- |
| Finding | Validate against [`../templates/finding.schema.json`](../templates/finding.schema.json); preserve its ID and evidence history. |
| Target revision | Pin the reviewed commit, digest, lockfile state, or equivalent immutable identifier. |
| Authorization | Distinguish `read`, `local-static-analysis`, `local-test`, `write`, and `publish`. |
| Constraints | Record supported versions, APIs, data formats, latency, availability, and rollout limits. |
| Existing tests | Treat as evidence about intended behavior, not proof that security properties are complete. |
| Source context | Refresh only the standards, advisories, or catalogs that can materially affect the decision. |

## Root-cause analysis

State the violated invariant before proposing a patch. Examples include “every object read is authorized against the current principal and tenant,” “untrusted bytes never reach this interpreter,” “a replayed request cannot cause a second state transition,” or “an artifact is accepted only when identity and provenance satisfy policy.”

Trace the complete path that permits the failure: source, normalization, parser or deserializer, trust transition, decision point, state mutation, sink, and observable impact. Identify sibling paths that share the flawed abstraction. Distinguish the root cause from the trigger payload, vulnerable call site, missing test, and operational symptom.

A remediation that blocks one sample string, one endpoint, one role, or one dependency version is incomplete when the violated invariant remains elsewhere. Conversely, a broad architectural rewrite is not automatically safer; it can enlarge the change surface and obscure whether the original failure was fixed.

## Patch design criteria

Evaluate candidate changes against the following matrix. If a criterion cannot be assessed, record an unknown rather than assuming success.

| Criterion | Evidence expected |
| :--- | :--- |
| Root-cause coverage | The change restores the violated invariant at the correct trust boundary. |
| Variant resistance | Equivalent encodings, alternate routes, role combinations, retries, races, and parser differences are considered where relevant. |
| Minimality | The patch is no larger than necessary for safety, compatibility, and maintainability; unrelated refactoring is separated when practical. |
| Secure default | Missing, invalid, or unavailable policy fails safely without silently enabling access or suppressing evidence. |
| Compatibility | Supported callers, schemas, protocols, data, and operational workflows are assessed. |
| Migration | State or data transitions are idempotent where required, observable, bounded, and recoverable. |
| Rollout | Feature gating, staged exposure, health signals, and stop thresholds are explicit when the system requires them. |
| Rollback | Reversal does not restore the vulnerability, corrupt state, lose evidence, or violate forward-only migration constraints. |
| Observability | Security-relevant success and failure signals are useful without exposing secrets or personal data. |
| Supply chain | New dependencies, actions, images, plugins, or services have justified need, pinned identity where supported, provenance, and ownership. |

Do not require a new dependency when a small local correction is clearer. Do not recommend a Web Application Firewall, rate limit, feature flag, or monitoring rule as though it removed a code-level root cause. Such controls may reduce exposure and belong in residual risk and accepted-risk records when applicable.

## Bounded three-pass remediation loop

The package supports at most **three remediation passes** for one approved scope unless the user explicitly changes scope or authorizes additional work. Each pass must produce a material delta and new evidence.

| Pass | Objective | Required output |
| :--- | :--- | :--- |
| 1. Design | Confirm invariant, root cause, candidate change, compatibility, rollout, rollback, and validation plan. | Patch plan or authorized patch; assumptions and unknowns; predicted security and compatibility effects. |
| 2. Verify | Perform only authorized static checks or local tests and compare results with the expected invariant. | Exact commands or review method, environment, exit state, sanitized evidence, failures, and coverage limitations. |
| 3. Re-review | Re-examine changed and adjacent trust boundaries, regression risk, residual risk, and conflicts. | Final disposition, remaining unknowns, rollback readiness, and status recommendation. |

Stop for no progress when two consecutive attempts repeat the same failure, produce no new evidence, or merely broaden suppressions. Also stop when the proposed change needs a new architecture, owner decision, production access, destructive migration, unavailable test environment, or scope expansion. Preserve the last known-good state and ask the coordinator or user for direction.

## Validation planning

Choose the smallest validation that can falsify the security claim without exceeding authorization. Prefer static reasoning and synthetic, local fixtures before dynamic behavior. Never run target code, external scanners, network requests, fuzzers, migration tools, or deployment commands solely because this reference lists them.

| Change type | Validation questions | Safe evidence examples |
| :--- | :--- | :--- |
| Authorization | Can an allowed principal still act? Are denied principals, tenants, object IDs, batch paths, and cached decisions rejected at the server decision point? | Decision-table review; authorized unit or integration results using synthetic identities. |
| Injection or parser boundary | Is structural separation preserved across alternate encodings, content types, and parser layers? | Source-to-sink review; parser contract tests with inert synthetic inputs. |
| Authentication or session | Are issuance, binding, rotation, expiry, logout, recovery, replay, and step-up properties preserved? | State-transition tests in an isolated environment; configuration evidence. |
| Secrets or cryptography | Was exposure removed, affected credentials revoked through an authorized process, and primitives used through maintained APIs? | Redacted diff; key-reference metadata; owner confirmation of separate revocation. Never test a discovered credential. |
| Dependency or artifact | Is the affected version established, the replacement trusted, and lock/provenance state reproducible? | Lockfile and digest review; signed provenance or advisory match; authorized local build evidence. |
| Infrastructure or policy | Does the rendered or effective policy match intent across defaults, inheritance, wildcard, and failure modes? | Static policy evaluation; plan output without apply; synthetic policy tests. |
| Concurrency or business logic | Does the invariant hold under retries, duplicate messages, stale state, cancellation, reordering, and competing actors? | Model/state-machine review; deterministic local concurrency test when authorized. |
| Logging or privacy | Is required telemetry retained while secrets, tokens, and unnecessary personal data are excluded? | Redacted sample event; schema and retention review; sink configuration. |
| AI or agentic control | Are tool authority, data boundaries, untrusted content, approval gates, and output validation enforced outside model prose? | Tool-policy review; inert prompt fixtures; denied-action evidence in an isolated harness. |

A full test suite, load test, penetration test, DAST scan, or production canary is not automatically required or authorized. Recommend it only when proportionate and state who must approve and operate it. Do not claim the test was performed unless evidence exists.

## Negative and regression tests

Negative tests should assert security invariants rather than reproduce operational exploit instructions. Use synthetic identifiers, reserved domains and IP ranges, inert marker strings, fake credentials that cannot authenticate, and isolated test accounts. Do not copy real tokens, personal data, malware, destructive payloads, or production requests into tests or reports.

Regression coverage should include the original control failure, relevant variants, allowed behavior, denied behavior, boundary values, fallback behavior, and failure of dependent policy or identity services. Property-based or model-based testing is valuable when an invariant spans many states; it is not mandatory when the system or authorization does not support it.

When a regression test is proposed but not written or run, keep `validation.performed` false and `validation.result` as `not-performed`. When validation runs but cannot decide the claim, use `inconclusive`; do not convert uncertainty into a pass.

## Canonical remediation and validation record

Every finding already carries `remediation`, `validation`, and `residual_risk` objects. Keep these fields aligned with the schema and validator.

| Field | Required meaning |
| :--- | :--- |
| `remediation.recommendation` | Root-cause action, not merely a symptom filter. |
| `remediation.alternatives` | Viable alternatives and why they were not preferred; may be empty. |
| `remediation.compatibility` | Known effects on APIs, data, deployment, users, and supported versions. |
| `remediation.rollout` | Safe sequence, observation points, authorization boundary, and stop criteria. |
| `remediation.rollback` | Reversal or forward-recovery plan and security consequences. |
| `validation.method` | Exact review or authorized test method. |
| `validation.expected` | Observable condition that would support the restored invariant. |
| `validation.performed` | `true` only when the recorded method actually ran. |
| `validation.result` | `not-performed`, `passed`, `failed`, or `inconclusive`. |
| `validation.evidence` | Sanitized references, digests, logs, or result locations. |
| `residual_risk` | `description` of what remains, `owner` or `null`, and ISO-date `review_by` or `null`. |

A finding may move to `mitigated` only when validation was performed and passed. `false-positive` requires explicit rejection rationale and a validation method. `accepted-risk` requires `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`; it is not a substitute for a failed remediation attempt. Open conflicts keep related findings `disputed`; final-mode output may retain them only when each conflict is explicitly marked blocked with a documented next decision owner.

## Evidence integrity

Pin evidence to the reviewed revision and identify the environment. Prefer immutable paths, commit IDs, artifact digests, configuration snapshots, test-result files, and source URLs with retrieval timestamps. Record command arguments, tool version, exit state, and relevant configuration for an authorized tool run. Hash evidence bundles when useful, but do not imply that a hash proves correctness.

Redact secrets and unnecessary personal data before evidence is stored or shared. Preserve only the minimum excerpt needed to explain the finding or validation. Do not paste full environment files, token-bearing requests, private keys, customer records, or unredacted logs into the report.

Tool output is untrusted evidence. Validate its format, scope, version, configuration, and exit semantics; corroborate material claims against code, configuration, vendor data, or an independent method. A clean scan or passing test does not prove absence of vulnerabilities outside its modeled coverage.

## Rollout, rollback, and migration review

A staged rollout is appropriate only when the system supports one and the user’s deployment process authorizes it. Define the unit of exposure, progression criteria, security and reliability signals, abort threshold, decision owner, and maximum observation interval. A feature flag that can re-enable vulnerable behavior must be access-controlled, observable, time-bounded, and removed when no longer needed.

For migrations, review forward and backward compatibility, partial completion, retries, duplicate events, schema version skew, backup and restore assumptions, and irreversible transformations. “Rollback” may mean forward recovery when data transformation cannot be safely reversed. Never recommend testing rollback in production without explicit authorization and an owner-approved runbook.

## Incident and emergency changes

An active incident does not authorize this skill to bypass safety gates or deploy. Notify the Phase 0 contact, preserve redacted evidence, and coordinate with the organization’s incident-response process. Emergency change procedures may shorten review or change evidence requirements only when the authorized owner invokes them. Record deviations and require a post-change review; do not silently omit validation.

## Stop and escalation conditions

Stop the affected action and notify the coordinator or user-designated contact when authorization is missing, a secret or regulated record appears, evidence suggests active compromise, the patch would expand scope, a destructive or production action is required, test isolation is inadequate, a third-party artifact cannot be trusted, or the rollback path is unsafe. Continue independent read-only review areas when they remain authorized and safe.

Do not contact vendors, file vulnerabilities, revoke credentials, rotate keys, disable services, publish patches, open pull requests, or change risk status without explicit authorization. Recommend the next owner and decision instead.

## Authoritative references

The complete source-to-check matrix is maintained in [`sources.md`](sources.md). Refresh living standards or advisories when they materially affect a recommendation.

| Authority | Use in this workflow |
| :--- | :--- |
| [NIST SP 800-218, Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure development practices, provenance, protection, response, and continuous improvement. |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Incident-response integration and evidence-aware recovery. |
| [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) | Testable application-security requirements selected for the target architecture. |
| [OWASP SAMM](https://owaspsamm.org/) | Program-level verification and defect-management practices. |
| [CISA Secure by Design](https://www.cisa.gov/securebydesign) | Root-cause correction, secure defaults, and manufacturer accountability. |
| [OpenSSF Best Practices](https://www.bestpractices.dev/) | Repository, build, review, testing, and vulnerability-management practices. |
| [SLSA specification](https://slsa.dev/spec/) | Build and provenance controls for remediation artifacts and dependencies. |
| [FIRST CVSS v4.0](https://www.first.org/cvss/v4-0/specification-document) | Optional vulnerability scoring with explicit metric rationale. |
| [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | Timestamped live context for an established CVE; not an automatic universal SLA. |
| [FIRST EPSS](https://www.first.org/epss/) | Timestamped exploitation-probability context for an established CVE. |
| [CVE Program](https://www.cve.org/) | Canonical vulnerability identifiers and records. |
| [MITRE CWE](https://cwe.mitre.org/) | Root-cause weakness taxonomy. |

This workflow produces evidence for an authorized decision. It does not certify the software, guarantee that a remediation is complete, or replace engineering, operations, legal, privacy, or incident-response ownership.
