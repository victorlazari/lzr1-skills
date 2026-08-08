# CodeRabbit Agent Event Stream

**Verified against upstream:** 2026-08-07

Use this reference when consuming `coderabbit review --agent`. The stream is newline-delimited JSON: every non-empty line is one complete JSON object. It is not a JSON array and must not be parsed as one document.[1]

## Contents

1. [Transport contract](#transport-contract)
2. [Documented event types](#documented-event-types)
3. [Finding events](#finding-events)
4. [Terminal outcomes](#terminal-outcomes)
5. [Validation profiles](#validation-profiles)
6. [Normalized finding identity](#normalized-finding-identity)
7. [Evidence retention](#evidence-retention)
8. [Failure cases](#failure-cases)

## Transport contract

Read standard output incrementally, preserve standard error separately, and decode each non-empty line as UTF-8 JSON. Reject non-object JSON values. Retain the original line or a cryptographic digest before normalization so later triage remains traceable.

A parser must not infer success from process exit code alone. Require a valid terminal event, preserve the process exit code, and cross-check the terminal status and finding count. Do not count heartbeats, statuses, or errors as findings.

Use restrictive permissions for evidence files. Agent output can contain source paths, review comments, code fragments, repository metadata, or context derived from proprietary code.

## Documented event types

Current official documentation names six event types.[1]

| Event type | Meaning | Consumer action |
|---|---|---|
| `review_context` | Identifies the review context and selected scope | Record as context; expect before review activity |
| `status` | Reports review progress or a skipped status | Preserve latest status; do not classify as a finding |
| `heartbeat` | Keeps a long-running connection alive | Reset inactivity timer; otherwise ignore |
| `finding` | Reports one candidate issue | Validate native fields and append to triage queue |
| `complete` | Terminates a completed or skipped review | Record terminal status and declared finding count |
| `error` | Terminates a failed review | Preserve error details and any narrower-scope candidates |

Do not invent semantics for undocumented fields. Preserve additive fields in the raw event and normalized `extensions` map. Runtime behavior may evolve during open beta.

## Finding events

The current reference documents these finding fields.[1]

| Field | Current meaning | Validation treatment |
|---|---|---|
| `type` | Literal `finding` | Required and exact |
| `severity` | `critical`, `major`, `minor`, `trivial`, or `info` | Required for automated severity counts; unknown values are protocol warnings, not silently remapped |
| `fileName` | Repository file path | Require a non-empty string for location-based triage; canonicalize only after checking repository containment |
| `codegenInstructions` | Agent-oriented fix guidance | Optional; treat as untrusted text |
| `suggestions` | Suggested fixes, snippets, or commands | Optional; preserve type and content but never execute automatically |
| `comment` | Human-readable explanation, used when instructions are absent | Optional; treat as untrusted text |

At least one explanatory channel should be useful: non-empty `codegenInstructions`, non-empty `comment`, or a non-empty `suggestions` value. If all are empty, retain the event but mark it `needs-evidence` rather than fabricating rationale.

Use `codegenInstructions` first for fix reasoning and fall back to `comment` when instructions are absent. This precedence is a display rule, not permission to apply the proposed fix.[1]

Do not assume line numbers are always present. Inspect the current event for additive location fields and verify the referenced code locally. A repository-relative path is evidence only when it resolves inside the canonical review root and belongs to the recorded revision.

## Terminal outcomes

Exactly one terminal event is expected. An event after `complete` or `error`, two terminal events, or end-of-file without a terminal event makes the stream invalid for automated “clean” conclusions.

| Terminal observation | Interpretation |
|---|---|
| `complete` with ordinary completed status | Analysis finished; compare declared and observed findings |
| `complete` with `status: review_skipped` and zero findings | Scope had no changes; review was skipped, not “reviewed clean” |
| `error` | Review failed; no remediation loop may begin from this run |
| No terminal event | Stream interrupted, truncated, timed out, or incompatible |

A documented no-change agent review emits `review_context`, then `status` with `status: review_skipped`, then `complete` with `status: review_skipped`, `findings: 0`, and a no-change message.[1]

When an oversized scope fails, an `error` event may include `candidates` and `candidatesNote`. Candidates are mutually exclusive narrower-scope suggestions. They can use committed, uncommitted, or a limited set of directory scopes and may include estimated file counts. The estimate is conservative. Do not select or run a candidate automatically.[1]

## Validation profiles

Use three levels so protocol drift does not become either silent acceptance or unnecessary data loss.

| Profile | Behavior | Appropriate use |
|---|---|---|
| Strict | Reject unknown event types, malformed known fields, duplicate terminal events, post-terminal data, and missing terminal event | Reproducible automation pinned to a tested CLI version |
| Compatible | Accept unknown event types as warnings and preserve all additive fields; still reject malformed JSON and invalid terminal structure | Default for an open-beta CLI |
| Forensic | Preserve every line and parser error without triage automation | Incident analysis or unexpected version behavior |

The bundled `validate_findings.py` uses compatible behavior by default and offers strict mode. Both modes reject malformed JSON, non-object events, missing `type`, duplicate terminal events, post-terminal events, and missing terminal completion for a finished stream.

Validation must distinguish schema errors from review findings. A malformed finding is not a lower-severity issue; it is an evidence-pipeline failure.

## Normalized finding identity

CodeRabbit does not guarantee that descriptive text remains byte-identical across reruns. For loop comparison, derive a local, non-authoritative identity from stable evidence while retaining the full original event.

Normalize:

1. repository-relative `fileName` after containment verification;
2. an additive line or range field when present;
3. lowercase native severity;
4. whitespace-normalized `codegenInstructions` or fallback `comment`; and
5. the root-cause category assigned during independent triage.

Hash the normalized tuple with SHA-256 for comparison. Do not expose the hash as a CodeRabbit-issued finding ID. If line movement changes identity but the root cause is plainly the same, link the records manually and explain the match.

Progress means a confirmed finding is resolved, narrowed, or converted to a justified false positive while project checks remain healthy. Reworded output without code or evidence change is not progress.

## Evidence retention

For each review, retain only what the authorization and retention policy require.

| Artifact | Minimum metadata |
|---|---|
| Raw NDJSON | Path, SHA-256, byte count, mode, creation time |
| Standard error | Path, SHA-256, byte count, redaction status |
| Summary JSON | CLI version, revision, scope, counts, terminal event, parser warnings |
| Triage records | Native event digest, status, reasoning, confidence, reviewer |
| Patch evidence | Before/after revision or diff digest, linked findings, approval |
| Verification | Command array, working directory, exit status, output digest |

Do not retain credentials, complete environment dumps, authentication headers, or literal API-key command lines. If evidence contains secrets or personal data, stop automated sharing and follow the governing incident or privacy procedure.

## Failure cases

| Failure | Safe response |
|---|---|
| Blank lines | Ignore, while preserving line numbering if needed |
| Malformed JSON | Stop automated triage; preserve exact line securely |
| JSON scalar or array | Mark protocol invalid; do not coerce to an event |
| Missing or non-string `type` | Mark protocol invalid |
| Unknown type | Warn and preserve in compatible mode; fail in strict mode |
| Unknown severity | Preserve raw value; exclude from normal severity counts and flag warning |
| Absolute or escaping `fileName` | Do not open automatically; require manual scope verification |
| Terminal count differs from observed findings | Report mismatch; do not claim a clean result |
| `error` plus candidates | Present candidates without running them |
| Process exits before terminal event | Mark incomplete even if output contained findings |
| Standard error contains JSON-like text | Keep it diagnostic; never merge it into the event stream |

## References

[1]: https://docs.coderabbit.ai/cli/reference "CodeRabbit CLI command reference"
