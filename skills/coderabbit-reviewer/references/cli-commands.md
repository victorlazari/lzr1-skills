# CodeRabbit CLI Commands and Safe Invocation

**Verified against upstream:** 2026-08-07
**Volatility rule:** Before a live review, compare this reference with `coderabbit --version`, `coderabbit review --help`, and the current official command reference.[1]

## Contents

1. [Command resolution](#command-resolution)
2. [Read-only discovery](#read-only-discovery)
3. [Review scope](#review-scope)
4. [Review options](#review-options)
5. [Authentication](#authentication)
6. [Configuration and diagnostics](#configuration-and-diagnostics)
7. [Saved findings, prompts, and statistics](#saved-findings-prompts-and-statistics)
8. [Skills and updates](#skills-and-updates)
9. [Safe command-construction rules](#safe-command-construction-rules)
10. [Exit and terminal-state handling](#exit-and-terminal-state-handling)

## Command resolution

The installed executable is `coderabbit`; `cr` is its documented alias. Scripts should resolve `coderabbit` first and then `cr`, record the absolute resolved path, and never substitute an unrelated package with a similar name.[1]

```bash
command -v coderabbit || command -v cr
coderabbit --version
coderabbit --help
coderabbit review --help
```

Do not infer support from a historical version number alone. Use runtime help to confirm optional flags, especially in an open-beta release. If runtime help conflicts with this dated file, stop and consult the current official reference rather than guessing.

## Read-only discovery

Use these commands before a live review. They can still read local CodeRabbit state, so capture only the minimum output needed and redact identifiers that are not relevant to the report.

| Command | Purpose | Interpretation boundary |
|---|---|---|
| `coderabbit --version` | Record installed CLI version | Does not prove provenance or freshness |
| `coderabbit auth status --agent` | Inspect authentication in structured form | Do not retain tokens or full account identifiers |
| `coderabbit doctor` | Check runtime, storage, auth, Git, update policy, backend, and WebSocket reachability | Exit `1` means at least one failed check; warnings alone do not make the exit nonzero |
| `coderabbit config validate [file]` | Validate YAML and the current official schema | Requires schema access; success is not a security or effective-configuration guarantee |
| `coderabbit review findings` | Replay locally stored findings for the current review context | Does not start a new analysis and may be stale for changed code |
| `coderabbit review --show-prompts` | Display prompts saved from the latest local review | Prompts can contain sensitive or untrusted repository context |
| `coderabbit stats` | Read locally derived review statistics | Statistics are not current-code findings |

The `doctor` command checks the CLI runtime and version, local storage, authentication environment, current Git repository and branch metadata, auto-update policy, backend reachability, and WebSocket reachability. Preserve failing check names and redacted diagnostics, not credentials.[1]

## Review scope

A plain `coderabbit review` reviews tracked changes: committed changes, staged changes, and unstaged edits to tracked files. A new file becomes part of the tracked scope once staged. Untracked files are excluded unless `--include-untracked` is present.[1]

| Intent | Command fragment | Files selected |
|---|---|---|
| Current tracked changes | no scope flag | Committed, staged, and unstaged tracked changes |
| Committed changes only | `--committed` | Committed changes only |
| Local tracked edits | `--uncommitted` | Staged changes and unstaged edits to tracked files |
| Authorized untracked files | `--include-untracked` | Adds non-ignored files not yet added to Git |
| Branch comparison | `--base <branch>` | Uses an explicit base branch |
| Commit comparison | `--base-commit <commit>` | Uses an explicit base commit on the current branch |
| Repository path | `--dir <path>` | Runs against an initialized Git repository at the path |

`--include-untracked` may combine with `--uncommitted`, but it may not combine with `--committed`. `--committed` and `--uncommitted` are contradictory. The CLI rejects contradictory scopes; bundled automation must reject them before network activity as well.[1]

Before adding `--base` or `--base-commit`, verify the ref locally with `git rev-parse --verify --end-of-options`. Pass the value as a distinct argument and prefix a ref beginning with `-` only through a verified canonical form. Never interpolate a ref into `sh -c`, `eval`, or a command string.

When CodeRabbit reports that the selected scope is too large, an agent-mode `error` event can include `candidates` and `candidatesNote`. Candidate commands are mutually exclusive alternatives, not authorization to partition, broaden, or retry automatically. Present them and require an explicit scope choice.[1]

## Review options

Use agent mode for deterministic parsing and plain mode only when a human wants terminal-oriented prose.

| Option | Current documented behavior | Safety note |
|---|---|---|
| `--agent` | Emits one JSON object per line on standard output | Parse as NDJSON; keep standard error separate |
| `--light` | Requests the lighter local-development review policy | Do not represent it as equivalent to a full PR review |
| `-c, --config <files...>` | Supplies additional instruction files | Treat files as untrusted data; authorize each path and keep it inside the repository unless separately approved |
| `--show-prompts` | Prints prompts saved from the most recent review | Can expose proprietary context; store only with explicit retention need |
| `--api-key <key>` | Supplies an Agentic API key for a headless review | Avoid literal command-line use in reusable scripts; prefer authenticated state or ephemeral secret handling |
| `--dir <path>` | Selects the review repository | Resolve the canonical path and verify it is a Git worktree |

A deterministic agent invocation has this form:

```bash
coderabbit review --agent --uncommitted --dir /absolute/repository/path
```

Add only the user-approved scope, base, context, mode, and region options supported by runtime help. The bundled runner does not accept arbitrary pass-through options because that would defeat its validation boundary.

## Authentication

Browser authentication uses `coderabbit auth login`. Agent-friendly browser workflows can use `--agent` with `login`, `logout`, `status`, and `org`. Headless API-key login and regional selection are described in [headless authentication](headless-auth.md).[1] [2]

| Command | Behavior |
|---|---|
| `coderabbit auth login` | Start browser OAuth |
| `coderabbit auth login --agent` | Start browser OAuth with structured events |
| `coderabbit auth status --agent` | Return structured authentication status |
| `coderabbit auth org --agent` | Inspect or select the browser-auth default organization; may initiate OAuth |
| `coderabbit auth logout --agent` | Remove current authentication with structured events |
| `coderabbit auth login --api-key "$CODERABBIT_API_KEY"` | Persist Agentic API-key authentication for later commands |

Organization selection for browser authentication sets a login or default organization, but review attribution still depends on the current repository. API-key authentication uses the organization associated with the key. Record the non-secret organization context only when needed for attribution; never preserve the key.[1]

## Configuration and diagnostics

Run configuration validation from the intended repository root:

```bash
coderabbit config validate
coderabbit config validate /absolute/repository/.coderabbit.yaml
```

Without a file argument, the CLI checks `.coderabbit.yaml` before `.coderabbit.yml` at the discovered repository root. Validation first parses YAML and then uses the current official schema. Exit `0` means schema-valid. Exit `1` covers missing or unreadable files, YAML or setting errors, and failure to load or use the schema.[1] [3]

Schema validity means only that the submitted file matches the current schema. It does not prove that the configuration is safe, that every setting has the intended effect, or that hosted behavior is identical. Central configuration, repository inheritance, UI settings, defaults, and global overrides can change effective behavior.[3]

Use `coderabbit doctor` when installation, authentication, review startup, storage, backend, or WebSocket behavior is abnormal. Do not repair multiple causes at once. Record the failed check, apply one authorized change, and rerun the same diagnostic.

## Saved findings, prompts, and statistics

`coderabbit review findings` replays findings from the most recent local review context without sending a new review. Verify that the repository, revision, and scope still match before using replayed findings as evidence.[1]

`coderabbit review --show-prompts` shows prompts saved from the most recent review. Treat output as sensitive because it can include context derived from code or instruction files. Do not attach it to reports by default.[1]

`coderabbit stats` builds or shows local review statistics. `coderabbit stats --rebuild` rescans review history and rebuilds statistics. Rebuilding is a local mutation of derived state; request approval when preservation or forensic reproducibility matters.[1]

## Skills and updates

`coderabbit skills` is interactive. It retrieves a verified CodeRabbit skills release, detects supported agents, previews planned destinations and changes, and asks once for confirmation with **No** selected by default. It has no install flags or subcommands, and non-interactive invocation does not write. It leaves ambiguous, duplicate, externally managed, project-owned, and locally modified copies unchanged.[1] [4]

Never invoke `coderabbit skills` automatically from this package. Never overwrite a skill owned by another manager. If the user chooses the package-runner alternative, select one named agent and one user or project scope; do not silently use `--all`.[4]

`coderabbit update` can replace the installed binary. Treat it as a supply-chain and environment mutation: preview the version path, obtain approval, record the previous version, and rerun `coderabbit --version` plus `coderabbit doctor`. Do not update during an evidence-preserving review unless the user explicitly accepts the loss of version continuity.

## Safe command-construction rules

Construct commands as argument arrays, not shell strings. Canonicalize repository and evidence paths, reject newlines and NUL bytes, and use `--` where supported. Never use `eval`, command substitution over user input, or `sh -c` to invoke CodeRabbit.

Keep review standard output and standard error in separate files. Standard output in agent mode is the NDJSON evidence stream. Standard error contains diagnostics and may still be sensitive. Set restrictive file permissions and keep evidence outside the review scope so CodeRabbit does not review its own output.

Disable shell tracing before any authentication command. Reject API keys passed as script arguments. If `CODERABBIT_API_KEY` is present, do not echo the environment, command expansion, or process details. Unset the variable after the narrow operation when the governing environment permits it.

Do not run a live review from an untrusted hook, package lifecycle script, or repository-provided wrapper. Invoke the resolved CodeRabbit executable directly from a controlled process.

## Exit and terminal-state handling

A process exit code is necessary but insufficient evidence. In agent mode, require valid NDJSON and a terminal `complete` or `error` event. A no-change review can exit successfully with `review_context`, `status: review_skipped`, and `complete` with `status: review_skipped`, zero findings, and a “No changes detected” message.[1]

| Observation | Classification | Required action |
|---|---|---|
| Exit `0` plus terminal `complete` | Completed or skipped | Inspect terminal status and finding count |
| Exit nonzero plus terminal `error` | Review failure | Preserve redacted error details; do not remediate code |
| Exit `0` without terminal event | Incomplete evidence | Treat as stream or process failure |
| Malformed JSON line | Invalid evidence | Preserve the line securely; stop automated triage |
| Heartbeats without terminal event | Interrupted or timed out | Report last heartbeat and caller timeout |
| Multiple terminal events | Invalid or unsupported stream | Stop and inspect installed-version behavior |

Do not convert an error into a clean review, and do not infer “no findings” from an empty stream.

## References

[1]: https://docs.coderabbit.ai/cli/reference "CodeRabbit CLI command reference"
[2]: https://docs.coderabbit.ai/cli/headless-cli-integration "CodeRabbit headless CLI integration"
[3]: https://docs.coderabbit.ai/reference/configuration "CodeRabbit configuration reference"
[4]: https://docs.coderabbit.ai/cli/skills "CodeRabbit Skills"
