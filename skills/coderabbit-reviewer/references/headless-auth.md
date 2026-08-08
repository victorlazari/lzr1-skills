# Headless Authentication and Regional Execution

**Verified against upstream:** 2026-08-07
**Version-sensitive baseline:** CodeRabbit CLI v0.7.2, released 2026-08-05.[1] [2]

Use this reference for CI jobs, bots, remote development environments, and coding agents that cannot complete interactive browser OAuth. Headless operation requires an Agentic API key associated with a CodeRabbit organization and an assigned user seat.[1]

## Contents

1. [Choose an authentication mode](#choose-an-authentication-mode)
2. [Secret handling](#secret-handling)
3. [Regional consistency](#regional-consistency)
4. [Ephemeral single-review mode](#ephemeral-single-review-mode)
5. [Persisted CLI authentication](#persisted-cli-authentication)
6. [CI and agent isolation](#ci-and-agent-isolation)
7. [Verification and failure handling](#verification-and-failure-handling)
8. [Rotation and cleanup](#rotation-and-cleanup)

## Choose an authentication mode

The official CLI supports a key on a single review and a key-based login reused by later commands.[1]

| Mode | Current command pattern | Persistence | Primary risk |
|---|---|---|---|
| Browser OAuth | `coderabbit auth login` | Local CLI auth state | Interactive account and organization selection |
| Ephemeral API-key review | `coderabbit review --api-key "$CODERABBIT_API_KEY" ...` | No intended reusable login | Secret expands into child-process arguments |
| Persisted API-key login | `coderabbit auth login --api-key "$CODERABBIT_API_KEY" ...` | Reusable local auth state | Secret appears in login process arguments and resulting auth state persists |

Prefer browser OAuth for a trusted interactive workstation. Prefer an ephemeral API-key review in an isolated, short-lived runner when process visibility and log controls are strong. Use persisted login only when repeated reviews justify local credential state and its storage lifecycle is governed.

Do not accept an API key as a positional argument to any bundled script. Do not write it to a configuration file, shell history, command transcript, report, artifact, cache, or debug log.

## Secret handling

Store the key in the platform’s secret manager and expose it as `CODERABBIT_API_KEY` only to the narrow review step, as recommended by the official headless guide.[1]

Before use, verify only that the variable exists and does not contain a newline or NUL-equivalent input. Never print its length, prefix, suffix, digest, or validation error containing the value. A digest can still become a correlatable secret identifier.

Disable shell tracing before expansion:

```bash
set +x
: "${CODERABBIT_API_KEY:?CODERABBIT_API_KEY is required}"
```

The official command places the expanded key in the child process argument vector. On multi-user or weakly isolated systems, process inspection may expose it. Environment variables can also be exposed by diagnostics, crash reports, container inspection, or CI metadata. Use a dedicated runner identity, restrict process inspection, disable core dumps where policy permits, and avoid concurrent untrusted jobs.

Do not run `env`, `set`, `printenv`, shell debug mode, process listings, or broad support bundles while the key is present. Redact the entire argument following `--api-key` from evidence.

## Regional consistency

CLI v0.7.2 added explicit `--region us` and `--region eu` support for authentication and API-key review flows. US remains the documented default. Saved authentication retains the selected region, and authentication status reports it.[2]

Select the region from organizational policy and key provisioning, not from convenience. Record the region as non-secret metadata. Use the same region for login, status verification, and review. Never retry against another region automatically after an authentication error.

| State | Safe action |
|---|---|
| Region explicitly provided by owner | Use and record it |
| Saved auth reports a region | Confirm it matches the review contract |
| API key region is unknown | Ask the owner or secret administrator; do not probe both regions |
| Wrong-region error | Preserve the redacted recovery guidance and require an explicit corrected region |
| Installed CLI lacks `--region` | Stop and consult current runtime help or upgrade through an approved process |

## Ephemeral single-review mode

Use this pattern only in a protected runner after accepting the process-argument exposure described above:

```bash
set +x
umask 077
: "${CODERABBIT_API_KEY:?CODERABBIT_API_KEY is required}"
coderabbit review \
  --agent \
  --api-key "$CODERABBIT_API_KEY" \
  --region eu \
  --uncommitted
status=$?
unset CODERABBIT_API_KEY
exit "$status"
```

Choose `us` or `eu` deliberately and select exactly one review scope. Do not save the expanded command. In CI configuration, use the platform’s native argument or step representation when possible and confirm masking does not depend only on literal string replacement.

A wrapper may read the key from the environment, but it must never accept `--api-key VALUE`, echo the invocation, or expose arbitrary pass-through arguments. The bundled `run-review.sh` intentionally relies on existing authenticated state unless its current help explicitly documents an approved key-env mode.

## Persisted CLI authentication

For repeated headless reviews, current upstream guidance permits:

```bash
set +x
: "${CODERABBIT_API_KEY:?CODERABBIT_API_KEY is required}"
coderabbit auth login --api-key "$CODERABBIT_API_KEY" --region eu
unset CODERABBIT_API_KEY
coderabbit auth status --agent
```

Persisted login creates or updates local CodeRabbit authentication state. Protect the CLI storage directory, isolate it from unrelated jobs, prevent it from entering a cache or artifact, and define logout and runner-destruction behavior.

Do not persist auth in a shared developer image, reusable public runner, repository directory, or container layer. Do not copy the storage directory between regions or organizations.

## CI and agent isolation

A headless job should use an immutable source revision, least-privilege repository credentials, an isolated workspace, restrictive evidence permissions, no untrusted concurrent workload, and an explicit outbound-network policy.

| Control | Required behavior |
|---|---|
| Source | Checkout the exact revision and verify expected repository identity |
| Secret scope | Expose the key only to the auth or review step |
| Forks | Do not provide organization secrets to untrusted fork code |
| Hooks | Disable or avoid untrusted repository hooks and lifecycle scripts |
| Logs | Disable command echo and inspect redaction before retention |
| Cache | Exclude CodeRabbit auth state and raw review evidence unless explicitly governed |
| Artifacts | Upload only redacted summaries or protected evidence with defined retention |
| Egress | Allow only required CodeRabbit endpoints according to current documentation and policy |
| Cleanup | Unset the key, logout when appropriate, and destroy the ephemeral workspace |

Repository code is untrusted even when the organization owns the repository. Do not source repository shell files or run project commands before the review unless the workflow separately approves them.

## Verification and failure handling

After persisted login, use `coderabbit auth status --agent` and verify authenticated state, organization context, and region without retaining unnecessary identity details. Run `coderabbit doctor` to distinguish authentication from backend, WebSocket, storage, version, or Git problems.[3]

On any auth failure:

1. stop without retrying another key or region;
2. preserve the error category with the secret removed;
3. verify CLI version and runtime help;
4. verify the configured region and organization out of band;
5. confirm the secret was injected into the intended step;
6. rotate the key if disclosure is possible; and
7. rerun only after one identified cause is corrected.

Never paste a key into a support ticket or chat. If the CLI prints a credential unexpectedly, quarantine the log, restrict access, rotate the key, and follow the organization’s incident procedure.

## Rotation and cleanup

Rotate Agentic API keys according to organizational policy and immediately after suspected exposure, job compromise, personnel changes, or accidental logging. Test the replacement in an isolated workflow before revoking the old key when continuity matters.

For ephemeral review, unset `CODERABBIT_API_KEY` immediately after the child process starts or completes according to shell requirements, then destroy the runner. For persisted login, run the current `coderabbit auth logout --agent` when reuse is no longer needed and remove the isolated CLI state according to current upstream storage guidance.

A successful logout does not erase CI logs, process telemetry, crash dumps, shell history, caches, or external secret-manager audit events. Review each channel separately.

## References

[1]: https://docs.coderabbit.ai/cli/headless-cli-integration "CodeRabbit headless CLI integration"
[2]: https://docs.coderabbit.ai/changelog "CodeRabbit CLI changelog"
[3]: https://docs.coderabbit.ai/cli/reference "CodeRabbit CLI command reference"
