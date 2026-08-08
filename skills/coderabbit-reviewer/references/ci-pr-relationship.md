# Local CLI, CI, and Pull-Request Boundaries

**Verified against upstream:** 2026-08-07

Use this reference when CodeRabbit local review participates in CI or when users compare local output with hosted pull-request review. The products optimize for different contexts and can produce different findings on the same code.[1]

## Contents

1. [Boundary summary](#boundary-summary)
2. [Why results differ](#why-results-differ)
3. [CI quality-gate design](#ci-quality-gate-design)
4. [Pull-request operations](#pull-request-operations)
5. [Evidence correlation](#evidence-correlation)
6. [Failure and fallback](#failure-and-fallback)

## Boundary summary

| Dimension | Local CLI review | Hosted pull-request review |
|---|---|---|
| Primary purpose | Immediate development feedback | Team collaboration and broader repository review |
| Input | Selected local Git scope and optional context files | Pull-request head/base plus hosted repository and organization context |
| Configuration | Feature-branch repository file plus CLI-visible inputs | Resolved repository, central, UI, default, and global configuration |
| Output | Plain text or local NDJSON event stream | Hosted comments, walkthroughs, statuses, and platform integrations |
| Identity | CLI authentication organization and region | Installed app, repository, and organization context |
| Mutation | None implied by a review | Comments, labels, reviewers, statuses, or approvals may be configured |
| Reproducibility | Depends on captured local state and version | Depends on hosted state, service version, and platform context |

Do not claim that a local clean result predicts a clean pull-request review. Do not use a local CLI finding ID as if it were a hosted thread identifier.[1]

## Why results differ

Differences can arise from the compared revision, base branch, staged or untracked files, CLI review policy, hosted collaboration context, repository knowledge, central or UI configuration, model or service evolution, and optional instruction files.

Before investigating a mismatch, create a comparison table:

| Evidence | Local | Hosted |
|---|---|---|
| Head revision | Exact `HEAD` plus worktree digest | Pull-request head SHA |
| Base | Explicit flag or documented default | Pull-request base SHA |
| Included files | Scope manifest | Hosted changed-file list |
| Configuration | Local file digest and validation | Resolved configuration export when authorized |
| Context files | Exact paths and digests | Hosted instructions and knowledge sources |
| CLI/service | CLI version and timestamp | Hosted review timestamp and available version metadata |
| Identity | Organization and region | Repository installation and organization |

Resolve input differences before treating output variation as a defect.

## CI quality-gate design

CodeRabbit CLI is network-backed and open beta. Design CI so a service interruption, protocol change, quota issue, or authentication failure cannot be confused with “no findings.”

A CI job should expose distinct outcomes:

| Outcome | Suggested gate behavior |
|---|---|
| Valid `complete` with zero findings | Pass the CodeRabbit gate, subject to other checks |
| Valid `complete` with findings | Apply an organization-defined policy after independent triage; do not equate all native severities with release blockers automatically |
| `review_skipped` | Neutral or explicitly skipped; never call it reviewed clean |
| Terminal `error` | Infrastructure/review failure, distinct from a code-quality failure |
| Invalid or truncated stream | Evidence-pipeline failure |
| Authentication or connectivity failure | Infrastructure failure; do not retry indefinitely |
| Project tests fail | Code gate failure independent of CodeRabbit result |

Keep CodeRabbit separate from deterministic tests, linters, type checks, dependency scans, and security review. A reviewer outage should not erase their results.

For untrusted forks, do not expose Agentic API keys. Use the CI platform’s protected-secret rules, explicit event allowlists, and a trusted checkout. Never run fork-provided scripts before the review merely because the job needs setup.

Set a pass ceiling and retry policy. Retry only transient infrastructure errors with bounded backoff and only when the same review contract remains valid. Never retry code findings.

## Pull-request operations

A local review does not authorize any hosted action. Posting a comment, requesting a review, resolving a thread, applying a label, assigning a reviewer, changing a status, approving, merging, or pushing a fix requires separate explicit approval.

Before a remote mutation:

1. open the exact pull request and verify repository, number, head SHA, and base;
2. show the proposed content or action;
3. remove secrets, local paths, raw prompts, and unnecessary source excerpts;
4. obtain confirmation for the exact mutation;
5. perform it once;
6. verify the resulting hosted state; and
7. record the URL or platform identifier.

Do not convert every local finding into a hosted comment. Consolidate validated issues, respect existing threads, and avoid duplicating CodeRabbit’s own hosted output.

## Evidence correlation

Correlate local and hosted findings by root cause, normalized path, code region, revision, and remediation—not by comment wording alone. Preserve each system’s native evidence separately.

A correlation record should include:

| Field | Purpose |
|---|---|
| Local event digest | Trace to NDJSON evidence |
| Hosted URL or identifier | Trace to the PR review artifact |
| Head/base revisions | Prove comparable code |
| Root cause | Explain why records represent the same issue |
| Differences | Severity, path, wording, context, or recommendation differences |
| Resolution | Patch revision and verification evidence |

If the revisions or scopes differ, label the relationship as related rather than duplicate.

## Failure and fallback

When the local CLI fails, preserve the error and continue deterministic project checks if authorized. Do not silently fall back to a hosted review because that changes data scope and can create remote artifacts.

When hosted review is unavailable, do not post local output through another integration without approval. Provide a local evidence package and state that hosted collaboration was not performed.

When outputs conflict on a security-sensitive issue, route the code and both evidence sets to `security-review`. When the issue concerns dependencies, images, SBOMs, secrets, Kubernetes, or infrastructure scanning, route it to `trivy-scanner`.

## References

[1]: https://docs.coderabbit.ai/cli/reference "CodeRabbit CLI command reference"
[2]: https://docs.coderabbit.ai/reference/configuration "CodeRabbit configuration reference"
[3]: https://docs.coderabbit.ai/cli/headless-cli-integration "CodeRabbit headless CLI integration"
