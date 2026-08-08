# CodeRabbit CLI Troubleshooting

**Verified against upstream:** 2026-08-07

Troubleshoot by preserving the failing contract, changing one cause at a time, and rerunning the narrowest diagnostic. Never convert an operational failure into a clean code-review result.

## Contents

1. [First-response sequence](#first-response-sequence)
2. [Diagnostic matrix](#diagnostic-matrix)
3. [Installation and version](#installation-and-version)
4. [Authentication and region](#authentication-and-region)
5. [Repository and scope](#repository-and-scope)
6. [Configuration validation](#configuration-validation)
7. [Event-stream failures](#event-stream-failures)
8. [Connectivity and long-running reviews](#connectivity-and-long-running-reviews)
9. [Oversized reviews](#oversized-reviews)
10. [Repeated or contradictory findings](#repeated-or-contradictory-findings)
11. [Evidence for escalation](#evidence-for-escalation)

## First-response sequence

Before changing anything:

1. stop automatic retries;
2. record the resolved executable and `coderabbit --version`;
3. preserve the redacted argument array, repository root, immutable revision, scope, region, and timestamp;
4. preserve standard output and standard error separately with restrictive permissions;
5. inspect the process exit code and terminal event;
6. run `coderabbit doctor` when startup, auth, storage, backend, or WebSocket behavior is implicated;
7. compare runtime help with [the command reference](cli-commands.md); and
8. change one identified cause, then rerun the same narrow diagnostic.

Do not upgrade, relogin, change region, change scope, delete local state, and edit configuration simultaneously. That destroys causal evidence.

## Diagnostic matrix

| Symptom | Likely category | First safe check | Do not do |
|---|---|---|---|
| Command not found | Installation or PATH | `command -v coderabbit; command -v cr` | Execute a remote installer blindly |
| Unknown flag | Version drift | `coderabbit --version`; current subcommand `--help` | Guess a replacement flag |
| `doctor` exits `1` | One or more failed checks | Read named failed checks | Treat warnings alone as fatal without reading report |
| Auth failure | Missing, expired, wrong organization, or wrong region | `coderabbit auth status --agent` with secrets absent | Probe both regions or multiple keys automatically |
| No changes detected | Empty selected scope | Git status and scope manifest | Broaden to untracked files silently |
| Too many files | Service scope limit | Inspect `candidates` or plain narrower-scope block | Auto-shard or run every candidate |
| Config exit `1` | File, YAML, setting, or schema-access failure | Read exact validator diagnostic | Call YAML-only parsing “schema valid” |
| Malformed NDJSON | Version, truncation, mixed output, or proxy corruption | Inspect exact failing stdout line and stderr separately | Merge stderr into stdout |
| Heartbeats then timeout | Caller deadline or lost terminal event | Compare last heartbeat and total timeout | Claim zero findings |
| Same finding returns | Root cause missed, nondeterminism, or scope drift | Compare revision, scope, normalized identity, and patch | Keep editing indefinitely |
| Local and PR findings differ | Different product context | Compare head/base, files, config, context, and identity | Assert either result is wrong without input comparison |

## Installation and version

Resolve both documented entrypoints:

```bash
command -v coderabbit || command -v cr
coderabbit --version
coderabbit --help
coderabbit review --help
```

If no command resolves, inspect the current official installation documentation and the installer as inert text before running it. The installer observed during this package’s research downloaded a platform archive, modified user PATH files, could initiate authentication, and did not visibly verify a published archive checksum or signature. Preview side effects and obtain approval before execution.[1]

If runtime help differs from this package, assume upstream drift. Use current official documentation, record the installed version, and update the package through its governed maintenance process. Do not force flags intended for v0.7.2 onto another version.

Treat `coderabbit update` as an environment and supply-chain mutation. Record the prior version, obtain approval, update once, and rerun version plus `doctor`. Do not update in the middle of an evidence-comparison loop.

## Authentication and region

Run:

```bash
coderabbit auth status --agent
coderabbit doctor
```

Remove or redact account details not needed for diagnosis. For headless auth, verify that the secret manager injected `CODERABBIT_API_KEY` into the intended trusted step without printing it. Confirm that the key’s organization has the required entitlement and user seat.[2]

CLI v0.7.2 supports `--region us` and `--region eu`; saved auth retains the chosen region, and auth status reports it. A wrong-region error must be corrected from organizational records. Do not try both regions because that creates unnecessary secret exposure and can obscure the real configuration.[3]

If disclosure is possible, quarantine logs and artifacts, rotate the key, and follow the organization’s incident procedure. Logging out does not revoke a leaked key or erase logs.

## Repository and scope

Verify repository identity and selected changes without mutating Git:

```bash
git rev-parse --show-toplevel
git rev-parse HEAD
git status --porcelain=v2 --branch
git diff --name-status
git diff --cached --name-status
```

A default review includes tracked committed, staged, and unstaged changes. New files are included after staging; untracked files require `--include-untracked`. Do not stage a file merely to bypass the untracked consent decision.[4]

Reject contradictory scope flags before invoking the CLI. `--committed` conflicts with `--uncommitted`, and `--committed` cannot combine with `--include-untracked`. Verify base branches and commits locally before passing them.

If `--dir` fails, canonicalize the path, verify it is a Git worktree, and ensure the invoking identity can read it. Do not fall back to the current directory silently.

## Configuration validation

`coderabbit config validate` can exit `1` for several distinct reasons: missing or unreadable file, invalid YAML, invalid settings, or inability to load or use the official schema.[4]

Run with an explicit path to remove discovery ambiguity:

```bash
coderabbit config validate /absolute/repository/.coderabbit.yaml
```

If YAML parses but schema retrieval fails, report schema validation unavailable. Do not disable TLS verification, substitute an untrusted schema, or copy a stale schema silently. If both `.coderabbit.yaml` and `.coderabbit.yml` exist, remove ambiguity through a reviewed repository change rather than assuming every consumer uses the CLI’s discovery order.

For hosted-behavior discrepancies, compare the effective resolved configuration, including central, UI, default, and global layers, through an authorized PR workflow.[5]

## Event-stream failures

Agent mode writes one JSON object per line to standard output. Standard error is not part of the event stream.[4]

| Failure | Interpretation | Response |
|---|---|---|
| Non-JSON stdout line | Mixed output, corruption, or incompatible version | Preserve line; stop automated triage |
| JSON array or scalar | Invalid event shape | Do not coerce |
| Missing `type` | Invalid event | Preserve and fail validation |
| Unknown event type | Forward drift | Warn and preserve in compatible mode; fail strict mode |
| Duplicate terminal event | Invalid state sequence | Stop; inspect version and raw stream |
| Event after terminal | Invalid state sequence | Stop; preserve evidence |
| EOF without terminal | Truncated, cancelled, or timed out | Mark incomplete even if exit is `0` |
| `complete` count mismatch | Contract anomaly | Report mismatch; do not claim clean |
| `error` event | Review failure | Do not enter remediation loop |

Run the bundled `validate_findings.py` against the raw standard-output file. Keep standard error separate and redact only in a derived copy, preserving protected raw evidence when policy permits.

## Connectivity and long-running reviews

`coderabbit doctor` checks backend and WebSocket reachability. Diagnose DNS, proxy, certificate, firewall, and service reachability according to organizational policy. Never disable TLS verification to make the check pass.[4]

Heartbeats are valid activity. Reset inactivity timeouts on them, but retain a separate total-duration ceiling. First-party agent guidance notes that reviews can take several minutes and may take approximately 7–30 minutes or longer for large changes.[6]

On cancellation, terminate gracefully, preserve the last valid event, and mark the run incomplete unless a terminal event already arrived. Retry only a diagnosed transient infrastructure failure, with a bounded policy and the exact same review contract.

## Oversized reviews

An oversized-scope `error` may include `candidates` and `candidatesNote`. In plain mode, a narrower-scope block can provide equivalent commands. The CLI does not choose, partition, or retry automatically.[4]

Present candidate scopes with their estimated local file counts and fit indicators. Require the user to select one. A candidate marked over the limit may still fit because estimates are conservative, but that does not authorize trial-and-error over every option.

Do not interpret candidate directories as a complete partition of the original review. Record that the remaining scope was not reviewed.

## Repeated or contradictory findings

When a finding repeats after a patch:

1. confirm repository, base, scope, context files, region, and CLI version are unchanged;
2. compare the normalized root cause rather than comment wording;
3. verify the patch actually reaches the reported path;
4. rerun the targeted regression test;
5. inspect whether a test or configuration was weakened;
6. classify the finding as confirmed, disputed, false-positive, or needs-evidence; and
7. stop on no progress or at the configured pass ceiling.

When CodeRabbit conflicts with project tests, neither automatically wins. Examine whether the tests cover the invariant, whether the reviewer assumed an impossible state, and whether deployment behavior differs from the test environment. Escalate security-sensitive uncertainty to `security-review`.

## Evidence for escalation

Provide a concise, redacted support packet:

| Include | Exclude |
|---|---|
| CLI version and resolved executable path | API keys, auth tokens, cookies |
| Operating system and architecture | Full environment dumps |
| Timestamp and selected region | Unnecessary account or personal data |
| Repository type and redacted identity if needed | Proprietary source unless explicitly authorized |
| Exact redacted argument array | Literal value following `--api-key` |
| Process exit code | Shell history |
| Terminal event and parser warnings | Raw prompts by default |
| `doctor` failed check names | Unredacted network headers |
| Minimal reproducible configuration | Full central configuration without approval |
| Evidence digests and byte counts | Unrelated logs |

If contacting upstream support or opening an issue is requested, prepare the packet first and obtain confirmation before posting it externally.

## References

[1]: https://docs.coderabbit.ai/cli "CodeRabbit CLI overview"
[2]: https://docs.coderabbit.ai/cli/headless-cli-integration "CodeRabbit headless CLI integration"
[3]: https://docs.coderabbit.ai/changelog "CodeRabbit CLI changelog"
[4]: https://docs.coderabbit.ai/cli/reference "CodeRabbit CLI command reference"
[5]: https://docs.coderabbit.ai/reference/configuration "CodeRabbit configuration reference"
[6]: https://docs.coderabbit.ai/cli/cursor-integration "CodeRabbit Cursor integration"
