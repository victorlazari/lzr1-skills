# Security review report: `<target>`

**Review ID:** `<REV-ID>`
**Target revision:** `<immutable commit, tag, digest, or artifact identifier>`
**Review window:** `<start>` to `<end>`
**Report generated:** `<RFC 3339 timestamp>`
**Review mode:** `<complete audit | focused change | remediation validation | incident-informed | advisory | control-evidence mapping>`
**Environment:** `<local | CI | development | staging | production | offline | unknown>`
**Report owner:** `<name or team>`
**Distribution:** `<authorized audience and handling classification>`

> This report records evidence observed within the stated scope. It is not a certification, legal conclusion, penetration-test attestation, or guarantee that the target is secure or free of vulnerabilities. Unreviewed, inaccessible, excluded, generated, vendored, and opaque material remains visible in the coverage ledger.

## 1. Executive summary

Describe the target, business context, review objective, highest material risks, important strengths, and decisions required. Distinguish **confirmed**, **disputed**, **accepted-risk**, **mitigated**, and **false-positive** records. Do not convert missing evidence into reassurance.

### Decision summary

| Decision | Owner | Due date | Blocking evidence | Status |
|---|---|---:|---|---|
| `<decision>` | `<owner>` | `<YYYY-MM-DD>` | `<finding, conflict, or unknown ID>` | `<open | decided | blocked>` |

### Finding-status summary

| Status | Count | Meaning in this report |
|---|---:|---|
| Confirmed | `<n>` | Evidence and reasoning satisfy the report contract |
| Disputed | `<n>` | Material reviewer disagreement or missing deciding test remains |
| Candidate | `<n>` | Hypothesis awaiting validation; omit from a final-mode report |
| Mitigated | `<n>` | Approved remediation was applied and validation passed |
| Accepted risk | `<n>` | Named owner, rationale, controls, review date, and expiry exist |
| False positive | `<n>` | Hypothesis was disproved and the rejection reason is retained |

### Priority themes

1. **`<theme>`:** `<why it matters, affected assets, and immediate action>`
2. **`<theme>`:** `<why it matters, affected assets, and immediate action>`
3. **`<theme>`:** `<why it matters, affected assets, and immediate action>`

## 2. Authorization, constraints, and safety boundary

| Field | Record |
|---|---|
| Owner or authorizer | `<name or team>` |
| Authorized actions | `<read, local-static-analysis, local-test, write, publish>` |
| Prohibited actions | `<production tests, external uploads, mutation, etc.>` |
| Environment constraints | `<offline, regulated, rate limited, production, etc.>` |
| Sensitive-data handling | `<redaction, retention, encryption, access rules>` |
| External services | `<allowed destinations or explicitly none>` |
| Stop conditions | `<conditions that required immediate halt>` |

Record any scope or authorization changes, who approved them, and when.

## 3. Objective and scope

### Included

- `<repository, component, path, service, or artifact>`
- `<commit range or release>`
- `<configuration or infrastructure boundary>`

### Excluded

| Path or area | Reason | Approved by | Residual impact |
|---|---|---|---|
| `<area>` | `<reason>` | `<approver or unknown>` | `<what the exclusion prevents concluding>` |

### Reviewability and inventory

State how inventory was produced and whether helper scripts were reviewed before use. Reference the immutable inventory artifact and its digest when available.

| Inventory class | Count | Review treatment |
|---|---:|---|
| First-party source | `<n>` | `<review method>` |
| Tests and fixtures | `<n>` | `<review method>` |
| Configuration and policy | `<n>` | `<review method>` |
| CI, build, and release | `<n>` | `<review method>` |
| Dependency manifests and lockfiles | `<n>` | `<review method>` |
| Infrastructure, cloud, and containers | `<n>` | `<review method>` |
| Mobile or client | `<n>` | `<review method>` |
| AI, LLM, or agentic | `<n>` | `<review method>` |
| Generated | `<n>` | `<generator reviewed, sample, or exclusion>` |
| Vendored | `<n>` | `<provenance and usage treatment>` |
| Binary or opaque | `<n>` | `<digest, signature, origin, or limitation>` |
| Inaccessible | `<n>` | `<reason and impact>` |

## 4. Coverage ledger

The structured report contains aggregate counts. Attach or link the detailed file-to-specialist ledger separately.

| Coverage state | Count | Required explanation |
|---|---:|---|
| Reviewed | `<n>` | First-party content or effective configuration received substantive reasoning |
| Mechanically inventoried | `<n>` | Metadata classified; content not substantively reviewed |
| Generated | `<n>` | Generator or source reviewed and output treatment stated |
| Vendored | `<n>` | Third-party material identified and provenance or usage reviewed |
| Binary or opaque | `<n>` | Not line-reviewable; origin, digest, signature, and use recorded where possible |
| Inaccessible | `<n>` | Permission, corruption, encryption, size, or tool limit prevented review |
| Excluded | `<n>` | Explicitly outside scope with reason and approver |
| Not applicable | `<n>` | Dimension did not apply, with supporting evidence |

### Uncovered or partially covered risk

Explain what the ledger prevents this report from concluding. Include ownership and a next action for material gaps.

## 5. Architecture and threat model

### Assets

| Asset | Security objective | Owner | Criticality |
|---|---|---|---|
| `<asset>` | `<confidentiality, integrity, availability, privacy, safety, financial>` | `<owner>` | `<criticality rationale>` |

### Identities and trust boundaries

| Boundary | From | To | Authentication | Authorization | Data or authority crossing |
|---|---|---|---|---|---|
| `<boundary>` | `<origin>` | `<destination>` | `<mechanism>` | `<decision point>` | `<data or action>` |

### Entry points and privileged operations

- `<public endpoint, parser, webhook, queue, job, admin plane, tool, or IPC interface>`
- `<credential, key, workload identity, role, or privileged state transition>`

### Abuse cases and invariants

| ID | Abuse case or invariant | Assets | Reviewed by | Outcome |
|---|---|---|---|---|
| `TM-<id>` | `<attacker goal or property that must always hold>` | `<assets>` | `<specialists>` | `<finding, rejected, unknown>` |

## 6. Method and specialist coverage

State whether specialists were executed in one bounded parallel batch or sequentially with the same contract. Record the assignments and returned coverage.

| Specialist | Assigned scope | Files or surfaces reviewed | Candidate findings | Rejected hypotheses | Unknowns |
|---|---|---:|---:|---:|---:|
| Application and API | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Identity and authorization | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Secrets and cryptography | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Logging and privacy | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Business logic and distributed systems | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Supply chain and build | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Cloud, container, and IaC | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Mobile and client | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| AI, LLM, and agentic | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |
| Evidence, scoring, and remediation | `<scope>` | `<n>` | `<n>` | `<n>` | `<n>` |

### Tools and limitations

| Tool or method | Version or digest | Configuration | Evidence produced | Limitation |
|---|---|---|---|---|
| `<tool>` | `<exact version or hash>` | `<key settings>` | `<artifact path or digest>` | `<what it cannot prove>` |

Document all failed tools or unavailable dimensions. A tool failure must remain a coverage limitation unless replaced by an equivalent method.

## 7. Confirmed and active findings

Use one section per finding. Keep the stable finding ID independent of severity or ordering.

### `<SR-ID>` — `<specific violated control or invariant>`

| Field | Record |
|---|---|
| Status | `<candidate | confirmed | disputed | mitigated | accepted-risk | false-positive>` |
| Asset | `<component, service, data, identity, or artifact>` |
| Confidence | `<high | medium | low>` — `<rationale and uncertainty>` |
| Taxonomy | `<CWE; CAPEC or ATT&CK only when justified>` |
| Optional CVSS v4 | `<vector or omitted>` |
| Live context | `<CISA-KEV, EPSS, CVE, NVD, vendor-advisory, other, or none; include retrieval timestamp and URL>` |

#### Locations

- `<path>:<line range>` — `<symbol or artifact digest>`

If a line location is unavailable, state why. Do not fabricate line precision.

#### Minimal evidence

Provide a redacted excerpt, deterministic observation, artifact digest, or test reference. Never reproduce a complete secret, token, private key, personal record, or proprietary payload.

> `<minimal redacted evidence>`

#### Reasoning

**Model:** `<source-to-sink | authorization-decision | state-invariant | trust-chain | supply-chain | configuration-exposure | other>`

1. `<attacker-controlled or untrusted origin>`
2. `<transformations, checks, state, and trust-boundary transitions>`
3. `<sink, policy decision, invariant failure, or artifact trust failure>`
4. `<why compensating controls do or do not break the path>`

#### Preconditions

- `<required access, state, timing, feature, deployment, or attacker capability>`

#### Impact

Explain realistic effects using the canonical dimensions—`confidentiality`, `integrity`, `availability`, `privacy`, `financial`, `safety`, `supply-chain`, and `compliance-evidence`—and separate technical possibility from demonstrated business effect.

#### Remediation

**Recommended root-cause fix:** `<fix>`

**Alternatives:**

- `<alternative and trade-off>`

**Compatibility:** `<API, data, behavior, deployment, or migration impact>`
**Rollout:** `<bounded sequence, monitoring, and ownership>`
**Rollback:** `<safe rollback that does not restore the vulnerable invariant>`

#### Validation

| Field | Record |
|---|---|
| Method | `<negative test, regression test, static proof, configuration check, or required evidence>` |
| Expected | `<observable safe result>` |
| Performed | `<yes | no>` |
| Result | `<not-performed | passed | failed | inconclusive>` |
| Evidence | `<test name, artifact, digest, or output reference>` |

#### Residual risk

`<remaining exposure, compensating controls, owner, and review date>`

#### Related findings and conflicts

- Findings: `<IDs or none>`
- Conflict: `<CONFLICT-ID or none>`

## 8. Chained findings

Describe attack paths whose material impact depends on multiple component weaknesses. Link each component finding and identify which remediation breaks the chain most effectively.

| Chain ID | Ordered finding IDs | Combined impact | Preferred break point | Validation |
|---|---|---|---|---|
| `CHAIN-<id>` | `<SR-A → SR-B>` | `<impact>` | `<control>` | `<test>` |

## 9. Disputed findings and conflict log

Do not hide disagreement. A material unresolved conflict blocks a definitive severity or confirmation decision; it may remain in a delivered report only as an explicitly blocked `disputed` finding linked to an open conflict record.

| Conflict ID | Finding IDs | Position A | Position B | Deciding evidence or test | Status | Resolution |
|---|---|---|---|---|---|---|
| `CONFLICT-<id>` | `<IDs>` | `<claim and evidence>` | `<claim and evidence>` | `<test or missing information>` | `<open | resolved>` | `<resolution or blocked>` |

## 10. Rejected hypotheses and false positives

| Finding or hypothesis ID | Trigger | Disproving evidence | Validation method | Suppression scope | Revisit condition |
|---|---|---|---|---|---|
| `<ID>` | `<tool, pattern, or reviewer lead>` | `<why it is not active>` | `<method>` | `<exact path/rule or none>` | `<expiry or change>` |

Suppressions must be narrow, owned, reviewable, and time-bound. Never suppress a broad category merely to make a gate pass.

## 11. Remediation roadmap

Group by dependency and risk reduction rather than severity label alone.

| Sequence | Finding IDs | Change set | Owner | Prerequisites | Regression evidence | Rollback | Target date |
|---:|---|---|---|---|---|---|---:|
| 1 | `<IDs>` | `<bounded patch>` | `<owner>` | `<prerequisite>` | `<tests>` | `<plan>` | `<date>` |

### Remediation-loop record

| Pass | Approved scope | Pre-change evidence | Changes | Tests | Re-review result | Stop or continue reason |
|---:|---|---|---|---|---|---|
| 1 | `<scope>` | `<artifact>` | `<summary>` | `<results>` | `<status>` | `<reason>` |
| 2 | `<if used>` | `<artifact>` | `<summary>` | `<results>` | `<status>` | `<reason>` |
| 3 | `<if used>` | `<artifact>` | `<summary>` | `<results>` | `<status>` | `<reason>` |

Do not exceed three passes without an explicit scope decision. Stop on production impact, lost authorization, destructive migration, unexpected critical evidence, failed rollback, or repeated non-progress.

## 12. Accepted risk

| Finding ID | Owner | Rationale | Compensating controls | Review by | Expires | Approval evidence |
|---|---|---|---|---:|---:|---|
| `<ID>` | `<owner>` | `<rationale>` | `<controls>` | `<date>` | `<date>` | `<record>` |

An accepted-risk entry without owner, rationale, controls, review date, and expiry remains unresolved.

## 13. Unknowns and residual limitations

| Unknown ID | Description | Potential impact | Owner | Resolution path |
|---|---|---|---|---|
| `UNKNOWN-<id>` | `<unknown>` | `<impact on conclusions>` | `<owner or null>` | `<evidence or access required>` |

Include inaccessible systems, unavailable runtime evidence, missing business rules, unreviewed binaries, stale documentation, or tests not performed.

## 14. Source freshness and governing references

List volatile sources actually used for decisions, including retrieval timestamp. Do not cite a checklist merely because it exists in the package.

| Source | Edition or status | URL | Retrieved at | Used for |
|---|---|---|---|---|
| `<authority>` | `<edition>` | `<HTTPS URL>` | `<RFC 3339 timestamp>` | `<finding, method, or control>` |

The package’s broader authority map is in [the source reference](../references/sources.md). Refresh release status, advisories, KEV, EPSS, CVE, NVD, framework documentation, and tool versions at execution time when they affect a conclusion.

## 15. Validation statement

Record whether the machine-readable report passed [the local validator](../scripts/validate_report.py), including the exact command and artifact digest.

```text
Command: python3 scripts/validate_report.py --final --as-of <YYYY-MM-DD> <report.json>
Result: <exit code and summary>
Report SHA-256: <digest>
```

Structural validation does not prove finding correctness. State which findings received independent reproduction, negative tests, regression tests, or only static reasoning.

## 16. Final quality checklist

- [ ] Authorization and environment constraints are recorded.
- [ ] The target revision is immutable or its limitation is explicit.
- [ ] Every inventory item has a coverage state.
- [ ] Every confirmed finding has minimal redacted evidence and complete reasoning.
- [ ] Secrets and sensitive data are not reproduced.
- [ ] Live context is sourced and timestamped.
- [ ] CVSS v4 is omitted when metric evidence is insufficient.
- [ ] Duplicates and chained findings retain all contributing evidence.
- [ ] Material conflicts are resolved or delivery is explicitly blocked.
- [ ] Remediation addresses root cause and includes compatibility, rollout, rollback, and tests.
- [ ] Accepted risks have owner and expiry.
- [ ] Unknowns and exclusions are visible.
- [ ] No claim of certification, breach absence, or vulnerability absence is made.
- [ ] The JSON report validates locally.

## Appendix A — evidence manifest

| Artifact | Purpose | SHA-256 | Access control | Retention |
|---|---|---|---|---|
| `<artifact>` | `<purpose>` | `<digest>` | `<who can access>` | `<retention>` |

## Appendix B — change and test evidence

| Revision | Test or check | Environment | Result | Evidence | Reviewer |
|---|---|---|---|---|---|
| `<revision>` | `<test>` | `<environment>` | `<result>` | `<artifact>` | `<reviewer>` |

## Appendix C — glossary

Define target-specific identities, roles, resources, tenants, trust boundaries, state names, and risk vocabulary used in this report.
