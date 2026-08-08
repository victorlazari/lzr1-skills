# CodeRabbit Reviewer Source Ledger

**Research cutoff:** 2026-08-07
**CLI baseline:** v0.7.2, released 2026-08-05
**Policy:** Prefer first-party live documentation and current runtime help. Treat this ledger as dated evidence, not a substitute for freshness checks.

## Contents

1. [Source hierarchy](#source-hierarchy)
2. [Primary sources](#primary-sources)
3. [Integration sources](#integration-sources)
4. [Standards and packaging sources](#standards-and-packaging-sources)
5. [Observed upstream artifacts](#observed-upstream-artifacts)
6. [Refresh triggers](#refresh-triggers)
7. [Conflict resolution](#conflict-resolution)

## Source hierarchy

Use sources in this order for operational decisions:

| Rank | Source | Use |
|---:|---|---|
| 1 | Installed `coderabbit` runtime help and observed structured output | Exact behavior of the executable being invoked |
| 2 | Current official CodeRabbit command, auth, configuration, skills, and changelog documentation | Supported contract and latest product behavior |
| 3 | Current official CodeRabbit repositories and published packages | Distribution content and ownership metadata |
| 4 | Agent Skills specification and official package-manager documentation | Portable package and installation behavior |
| 5 | Examples, community material, search snippets, and historical copies | Discovery only; verify against a higher tier |

A current runtime can still contain a bug, and live documentation can lead or lag a binary release. Record both when they disagree.

## Primary sources

| ID | Source | Authority | Verified | Package use | Volatility |
|---|---|---|---|---|---|
| CR-01 | [CLI overview](https://docs.coderabbit.ai/cli) | CodeRabbit official | 2026-08-07 | Product scope, installation entrypoint, local-review positioning | High during open beta |
| CR-02 | [CLI command reference](https://docs.coderabbit.ai/cli/reference) | CodeRabbit official | 2026-08-07 | Commands, scope flags, agent events, diagnostics, config validation, skills behavior | High |
| CR-03 | [Headless CLI integration](https://docs.coderabbit.ai/cli/headless-cli-integration) | CodeRabbit official | 2026-08-07 | Agentic API keys, environment handling, persistent versus per-review auth | High |
| CR-04 | [CLI changelog](https://docs.coderabbit.ai/changelog) | CodeRabbit official | 2026-08-07 | v0.7.2 release, US/EU region behavior, saved-region status and recovery | High |
| CR-05 | [Configuration reference](https://docs.coderabbit.ai/reference/configuration) | CodeRabbit official and schema-generated | 2026-08-07 | Field types, defaults, feature-branch config, central and effective configuration | High |
| CR-06 | [YAML configuration guide](https://docs.coderabbit.ai/getting-started/yaml-configuration) | CodeRabbit official | 2026-08-07 | Repository file placement and configuration workflow | Medium |
| CR-07 | [Configuration schema v2](https://www.coderabbit.ai/integrations/schema.v2.json) | CodeRabbit official machine-readable schema | 2026-08-07 | Template and local schema checks | High; fetch current copy |
| CR-08 | [YAML validator](https://docs.coderabbit.ai/configuration/yaml-validator) | CodeRabbit official | 2026-08-07 | Browser-validator boundary and CLI validation context | Medium |
| CR-09 | [CodeRabbit Skills](https://docs.coderabbit.ai/cli/skills) | CodeRabbit official | 2026-08-07 | Interactive `cr skills`, ownership, conflict, confirmation, and non-interactive behavior | High |

The configuration reference identified itself as generated from the official schema and displayed an August 4, 2026 update date during verification. Recheck that date and the schema before changing configuration guidance.

## Integration sources

| ID | Source | Verified | Key behavior captured |
|---|---|---|---|
| CR-10 | [Codex integration](https://docs.coderabbit.ai/cli/codex-integration) | 2026-08-07 | Agent review invocation, waiting for long-running review, severity/path/impact/fix presentation |
| CR-11 | [Claude Code integration](https://docs.coderabbit.ai/cli/claude-code-integration) | 2026-08-07 | Plugin and direct CLI review patterns; agent-applied fixes remain separate actions |
| CR-12 | [Cursor integration](https://docs.coderabbit.ai/cli/cursor-integration) | 2026-08-07 | Bounded review/fix loop guidance and expected review duration |
| CR-13 | [Gemini CLI integration](https://docs.coderabbit.ai/cli/gemini-integration) | Attempted 2026-08-07 | Page was not retrievable in the research batch; do not assert details without a fresh successful read |

Integration guides are examples for particular agents, not a grant of mutation or publication authority. This package keeps its consent, evidence, and stop-condition model stricter than a convenience workflow.

## Standards and packaging sources

| ID | Source | Verified | Package use |
|---|---|---|---|
| PK-01 | [Agent Skills specification](https://agentskills.io/specification) | 2026-08-07 | `SKILL.md` frontmatter, package layout, progressive disclosure |
| PK-02 | [Skills CLI](https://github.com/vercel-labs/skills) | 2026-08-07 | Explicit package-runner installation alternative and scope selection |
| PK-03 | [CodeRabbit official skills repository](https://github.com/coderabbitai/skills) | 2026-08-07 | Upstream skill ownership and published skill content for comparison |

Do not copy stale command claims from an upstream skill when current official CLI documentation or runtime help differs. During research, the current official repository’s `code-review` skill still described behaviors that lagged the live v0.7.2 command reference. Treat repository skill text as packaging evidence, not the sole command authority.

## Observed upstream artifacts

The following artifacts were retrieved as inert text and never executed:

| Artifact | Observation date | Recorded evidence | Security interpretation |
|---|---|---|---|
| `https://cli.coderabbit.ai/install.sh` | 2026-08-07 | Local snapshot and SHA-256 in the modernization research workspace | Installer selects platform archive, writes a user binary, can modify PATH files, verifies installation, and can start authentication |
| Official schema v2 JSON | 2026-08-07 | Local snapshot and SHA-256 in the modernization research workspace | Suitable for dated offline inspection, but live `cr config validate` intentionally uses the current schema |
| `coderabbitai/skills` default branch | 2026-08-07 | Passive shallow clone and commit identity in the modernization research workspace | Useful for ownership and package comparison; no repository code was executed |

The inspected installer did not visibly verify a published archive checksum or cryptographic signature before installation. Therefore this package never executes the remote installer automatically. Preview the script, record provenance, obtain approval, and prefer an organization-approved distribution path where available.

Do not encode local snapshot paths in portable skill instructions. They are research evidence for repository maintainers, not required runtime dependencies.

## Refresh triggers

Refresh all affected references, scripts, tests, and template validation when any trigger occurs:

1. `coderabbit --version` differs from the tested baseline;
2. runtime help adds, removes, or changes a command or flag;
3. a new agent event type, severity, terminal shape, or finding field appears;
4. the official configuration schema digest changes;
5. `cr skills` changes flags, non-interactive behavior, supported agents, ownership, or confirmation semantics;
6. headless auth, key entitlements, secret transport, or regional endpoints change;
7. the installer gains or loses checksum, signature, PATH, update, or authentication behavior;
8. official integration guidance changes the recommended pass ceiling;
9. local and hosted review behavior changes materially; or
10. a security advisory affects the CLI, installer, dependency chain, or service integration.

A refresh must run the package’s self-check and fixture tests, validate the example YAML against the current schema or CLI, and update the verification dates. Never change only a version string.

## Conflict resolution

When sources disagree:

1. freeze the planned invocation;
2. capture installed version and relevant runtime help;
3. retrieve the current official page without relying on search snippets;
4. compare release dates and version applicability;
5. prefer the behavior observed from the exact installed executable for safety validation;
6. avoid a disputed or deprecated flag;
7. document the discrepancy and conservative fallback; and
8. update this package only after tests cover the resolved behavior.

Do not infer undocumented compatibility from a successful command. A command can be accepted while ignoring or changing a behavior that matters to evidence.
