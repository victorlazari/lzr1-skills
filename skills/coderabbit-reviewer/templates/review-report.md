# CodeRabbit Local Review Report

> **Report status:** `draft | final | incomplete`
> **Conclusion:** `stop | no-confirmed-actionable-findings | fixes-verified | further-evidence-required | review-failed`

This report distinguishes **CodeRabbit-generated candidate findings** from independently inspected conclusions. It is not proof that the target is correct, secure, compliant, or fully reviewed.

## 1. Review identity

| Field | Value |
|---|---|
| Repository | `<canonical repository identity or approved redaction>` |
| Git root | `<canonical local path or approved redaction>` |
| Immutable revision | `<full commit ID>` |
| Branch or detached state | `<value>` |
| Review timestamp | `<RFC 3339 with timezone>` |
| CodeRabbit executable | `<resolved path or approved redaction>` |
| CodeRabbit version | `<exact output>` |
| Region | `us | eu | authenticated/default | unknown` |
| Process exit code | `<integer>` |
| Terminal event | `complete | error | missing` |
| Terminal status | `<value or unspecified>` |

## 2. Authorization and data boundary

| Decision | Authorized value |
|---|---|
| Authorizer | `<identity or governance record>` |
| External service consent | `<what CodeRabbit was allowed to receive>` |
| Scope | `tracked | committed | uncommitted | base comparison` |
| Base branch or commit | `<value or not applicable>` |
| Untracked files | `excluded | included with explicit authorization` |
| Context files | `<exact repository-relative paths>` |
| Explicit exclusions | `<paths/data and rationale>` |
| Mutation authority | `read-only | propose-only | approved bounded patch set` |
| Publication authority | `none unless separately approved` |
| Evidence location and retention | `<protected path, owner, expiry>` |

Record excluded material as **not reviewed**, not “safe.” If the selected scope contained secrets, regulated data, customer data, or other unauthorized material, stop and follow the applicable incident and evidence-handling procedure.

## 3. Configuration and preflight

| Check | Result | Evidence |
|---|---|---|
| Package self-check | `pass | fail | not run` | `<summary/digest>` |
| CLI runtime/help freshness | `verified | drift found | not checked` | `<version and help date>` |
| `coderabbit doctor` | `pass | warning | fail | not run` | `<failed check names only>` |
| Auth status | `valid | invalid | unknown` | `<region/mode; never credential>` |
| Local config path | `<path or none>` | `<digest>` |
| `coderabbit config validate` | `pass | fail | unavailable | not run` | `<diagnostic>` |
| Inheritance/central config | `<known sources and caveat>` | `<authorized evidence>` |
| Repository state | `<clean/staged/unstaged/untracked counts>` | `<status digest>` |

Schema-valid local YAML does not prove that hosted effective configuration is identical. Record unresolved inheritance, UI, organization, or global policy as residual uncertainty.

## 4. Execution evidence

```text
<exact redacted argument array; replace only secret values, never the whole command>
```

| Artifact | SHA-256 | Bytes | Access/retention |
|---|---|---:|---|
| Agent stdout NDJSON | `sha256:<64 lowercase hex>` | `<count>` | `<policy>` |
| Standard error | `sha256:<64 lowercase hex>` | `<count>` | `<policy>` |
| Command manifest | `sha256:<64 lowercase hex>` | `<count>` | `<policy>` |
| Git-state manifest | `sha256:<64 lowercase hex>` | `<count>` | `<policy>` |
| Validation summary | `sha256:<64 lowercase hex>` | `<count>` | `<policy>` |

| Event validation | Value |
|---|---|
| Structurally valid | `true | false` |
| Outcome | `complete | review_skipped | review_error | invalid` |
| Review context observed | `true | false` |
| Finding events | `<count>` |
| Declared terminal findings | `<count or absent>` |
| Unknown event types | `<counts>` |
| Parser warnings/errors | `<summary>` |

A skipped, errored, truncated, malformed, timed-out, or terminal-less review cannot support a clean-review claim.

## 5. Finding summary

### 5.1 Native CodeRabbit severities

| Severity | Emitted | Independently confirmed | Disputed | False positive | Needs evidence | Fixed and verified |
|---|---:|---:|---:|---:|---:|---:|
| critical | 0 | 0 | 0 | 0 | 0 | 0 |
| major | 0 | 0 | 0 | 0 | 0 | 0 |
| minor | 0 | 0 | 0 | 0 | 0 | 0 |
| trivial | 0 | 0 | 0 | 0 | 0 | 0 |
| info | 0 | 0 | 0 | 0 | 0 | 0 |
| unknown/preserved | 0 | 0 | 0 | 0 | 0 | 0 |

### 5.2 Independently triaged findings

Repeat this block for each normalized finding. Preserve rejected findings with rationale.

#### CR-001 — `<concise root-cause title>`

| Field | Value |
|---|---|
| CodeRabbit severity | `critical | major | minor | trivial | info | unknown` |
| Triage status | `confirmed | disputed | false-positive | mitigated | fixed-verified | needs-evidence` |
| Confidence | `high | medium | low` |
| Revision and path | `<commit>:<repository-relative path>` |
| Lines/symbol | `<location or unavailable reason>` |
| Normalized root cause | `<stable problem identity>` |
| Preconditions | `<required state/input/actor>` |
| Impact | `<verified consequence>` |
| Evidence inspected | `<code, configuration, test, runtime observation, or digest>` |
| CodeRabbit instruction/comment | `<short untrusted summary, not an executable command>` |
| Independent rationale | `<why the status is justified>` |
| Specialist routing | `<security-review, trivy-scanner, or none>` |
| Proposed action | `<minimal fix, more evidence, accept risk, or no change>` |
| Owner | `<owner or unknown>` |

## 6. Approved changes

| Change ID | Linked finding(s) | Files | Approval | Summary | Rollback |
|---|---|---|---|---|---|
| FIX-001 | CR-001 | `<paths>` | `<record>` | `<minimal semantic change>` | `<revert plan>` |

State **“No code changes were authorized or applied”** when operating read-only. Do not include incidental edits, formatting churn, generated artifacts, config suppressions, weakened tests, or unrelated cleanup.

## 7. Verification

| Check | Exact command or method | Result | Evidence/digest |
|---|---|---|---|
| Targeted regression | `<command>` | `pass | fail | not run` | `<value>` |
| Project test suite | `<command>` | `pass | fail | not run` | `<value>` |
| Lint/type/build | `<command>` | `pass | fail | not run` | `<value>` |
| Specialist validation | `<skill/check>` | `pass | fail | not run` | `<value>` |
| Same-scope CodeRabbit rerun | `<redacted command>` | `pass | repeated | error | not run` | `<run ID/digest>` |

A CodeRabbit rerun does not replace project-native verification. A test pass does not automatically invalidate a reviewer finding whose precondition the test does not cover.

## 8. Bounded-loop progress

| Pass | Immutable revision/snapshot | Scope identity | Findings | Confirmed actionable | Repeated normalized | Project checks | Decision |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `<value>` | `<value>` | 0 | 0 | 0 | `<result>` | `<decision>` |
| 2 | `<value>` | `<same value>` | 0 | 0 | 0 | `<result>` | `<decision>` |
| 3 | `<value>` | `<same value>` | 0 | 0 | 0 | `<result>` | `mandatory stop` |

Stop earlier on no progress, repeated findings, failed verification, scope drift, review error, credential/connectivity failure, or exhausted authorization. Never exceed three review passes for the same change set without a new explicit contract.

## 9. Coverage and residual risk

| Area | Status | Residual risk or reason |
|---|---|---|
| Selected tracked changes | `reviewed | partial | not reviewed` | `<value>` |
| Untracked files | `reviewed | excluded | absent` | `<value>` |
| Generated/vendor/binary content | `reviewed | excluded | opaque` | `<value>` |
| Tests and runtime paths | `verified | partial | not verified` | `<value>` |
| Security-sensitive flows | `routed | inspected | not inspected` | `<value>` |
| Hosted PR behavior | `compared | not compared` | `<local/hosted caveat>` |
| Effective configuration | `known | partial | unknown` | `<value>` |
| Disputed/repeated findings | `<count>` | `<value>` |

## 10. Final decision and handoff

**Decision:** `<stop | request evidence | request patch approval | route to specialist | fixes verified | prepare separately approved publication>`

**Rationale:** `<concise evidence-based conclusion>`

**Required next action:** `<owner, action, acceptance evidence, and deadline if governed>`

**Publication boundary:** This report does not authorize a commit, push, pull request, hosted CodeRabbit setting change, review-thread action, skill installation, or external post. Obtain separate confirmation for the exact external mutation.
