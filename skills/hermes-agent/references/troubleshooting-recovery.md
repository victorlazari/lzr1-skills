# Hermes Agent Troubleshooting and Recovery

**Read this reference** for failed installation, configuration, providers, tools, sessions, gateways, automation, updates, or recovery. **Verified:** 2026-08-08.

Commands, log locations, safe-mode behavior, schemas, and migration details are volatile. Verify them against `hermes --help`, the target-version documentation, and the installed source before use.[1] [2]

> Diagnose read-only first. Preserve the first failure, redact secrets, minimize in a disposable profile, and restore a complete known-good state. Never weaken approvals or isolation to “see whether it works.”

## Stabilize before diagnosis

For production, shared, or externally reachable deployments, first stop new ingress and unattended work when continued operation can cause harm. Do not destroy the failing state.

Record:

| Area | Evidence |
|---|---|
| Time and scope | First/last observed, users/tenants, affected entrypoints |
| Runtime | `command -v hermes`, version/commit, install method, interpreter/environment |
| State selection | User, profile, `HERMES_HOME`, cwd, service user/environment |
| Configuration | File paths, hashes, permissions, non-secret keys, config-check result |
| Extensions | Skills, plugins, MCP servers, hooks, memory providers, recent changes |
| Execution | Terminal backend, mounts/env/network, running child/remote jobs |
| Services | Processes, units, listeners, gateway/API state, restart counts |
| Persistence | Sessions, memory, logs, checkpoints, backups, output artifacts |
| External effects | Messages, files, branches, records, deployments, charges |

Collect values only when authorized. Never paste `.env`, `auth.json`, authorization headers, provider tokens, raw sensitive prompts, or private session content into reports.

## Run bounded discovery

Use only commands confirmed by runtime help. Typical read-only starting points are:

```bash
command -v hermes
hermes version
hermes --help
hermes doctor
hermes config check
hermes config
```

Inspect subcommand help before additional actions. Diagnostics can make provider/network calls or reveal environment details in some releases; understand behavior first.[1] [3]

Correlate service and shell environments. A common class of failure is launching the same executable under a different user, profile/home, working directory, PATH, virtual environment, or service environment.

## Classify the failing layer

| Symptom | Primary layer | First comparison |
|---|---|---|
| Command missing/wrong version | Installation/launcher | Resolved path, environment, source revision |
| Import/dependency failure | Runtime environment | Interpreter, virtualenv, dependency state |
| Unknown config key/type | Configuration/migration | Target version, example/docs, backup diff |
| Provider authentication/model error | Provider routing | Endpoint, credential presence/scope, model/transport |
| Repeated tool error | Tool/handler/backend | Tool schema, handler source, backend permissions |
| Wrong instructions/personality | Prompt/context | Context files, SOUL, memory, skill, session |
| Lost/mixed history | Session/profile | Session identity, profile/home, gateway mapping |
| Gateway user denied/accepted wrongly | Authorization | Allowlist/pairing, normalized identity, tenant |
| Service crash/restart loop | Service lifecycle | First error, user/env/cwd, listener conflict |
| Automation repeats/duplicates | Scheduler/idempotency | Run IDs, trigger history, retries, external state |
| Update regression | Code/config/state compatibility | Old/new revision, migration, dependency diff |
| Performance/context degradation | Provider/compression/storage | Model limits, compression, history size, I/O |

Avoid changing multiple layers simultaneously.

## Minimize safely

Create a disposable profile/home and synthetic workspace. Remove optional layers in a controlled order: public gateway/API, cron/goals/batch, hooks, third-party plugins/MCP, optional skills, external memory, custom context/SOUL, tools, fallback/routing, then provider complexity.

Use safe mode where the target version documents it, but verify exactly which customizations it disables.[2] A “safe” label is not an OS sandbox.

Reproduce with one entrypoint, one provider/model, no write tools, no real secrets beyond a disposable scoped credential if unavoidable, and a harmless prompt. Add one layer back at a time. Record the first layer that reintroduces failure.

Do not reproduce suspected cross-user, exfiltration, destructive, or physical-device issues against real data or production accounts.

## Diagnose installation and updates

Compare the launcher path with the intended install directory and interpreter. Determine whether multiple source/package/application installations exist. Capture source status and local changes before any update or reset.[4] [5]

For update failures, preserve the pre-update backup/checkpoint, old/new revisions, dependency state, migration output, and service logs. Do not run a force update, clean/reset, global reinstall, or directory deletion as an exploratory step.

Rollback code, dependencies, configuration schema, and compatible state together. Re-run config, import, health, listener, authorization, and controlled functional tests before restoring ingress.

## Diagnose configuration without exposing secrets

Run the supported configuration check and inspect keys/types with values redacted. Confirm YAML structure, environment-substitution syntax, selected profile/home, service environment, and file permissions.[6]

If a placeholder is unresolved, verify variable name and presence in the correct process environment without printing the value. If a secret may have appeared in YAML, logs, history, sessions, or reports, rotate it and review copies/backups.

For migrations, back up the file, apply a reviewed minimal change, validate, and preserve comments/unknown keys unless the official migration explicitly removes them.

## Diagnose providers and models

Record model identifier, provider, endpoint host, transport, credential source class, fallback/routing, timeout/retry, and exact redacted error. Distinguish authentication, authorization, model-not-found, capability/schema, rate-limit, server, network/TLS, timeout, and client-parse failures.[7] [8]

Do not switch to an arbitrary provider or custom base URL to bypass an error. A fallback can change data handling, cost, and capabilities. Test with a harmless non-tool prompt and disposable credentials where possible.

For ambiguous timeouts on write-capable calls, reconcile provider/downstream state before retrying.

## Diagnose tools and execution

Identify the tool source, schema, arguments class, approval result, handler, backend, user, cwd, mounts, environment variable names, network, timeout, and result/exit state.[9]

Reproduce with synthetic files inside a disposable workspace. Do not enable YOLO, disable approvals, switch from a sandbox to local execution, broaden mounts/environment, or add privileges as a diagnostic shortcut.

If cancellation or timeout may have left children or remote work, inspect through the approved control plane and terminate deliberately. Reconcile file/external effects before retry.

## Diagnose sessions, memory, and context

Confirm profile/home and entrypoint session mapping before opening stores. Work on a copy for repair. Inspect metadata, schema/version, permissions, size, and hashes before content.[10]

For wrong behavior, inventory prompt-affecting sources: user/project context, file/URL references, SOUL, memory, skills, plugins, platform hints, and session history. Disable one class at a time in a disposable profile.

Do not truncate databases or delete memory/session files because a lookup fails. Use documented interfaces or a tested migration/recovery path.

For cross-user leakage, stop shared ingress, preserve evidence, identify affected identities/data, rotate exposed credentials if necessary, and treat recovery as an incident.

## Diagnose gateways and services

Check service user, executable, profile/home, cwd, environment variable names, listeners, port ownership, restart policy, platform credential scope, allowlists/pairing, session mapping, queue state, and redacted first error.[11]

Test authorized and denied identities with synthetic content. Do not broaden authorization or bind publicly to solve connectivity. Verify firewall/reverse-proxy/TLS/auth layers independently.

When restarting, first understand queue/retry behavior to avoid duplicate external deliveries. Reconcile platform event/message IDs.

## Diagnose automation

Pause new triggers without deleting definitions. Record schedule/event, run IDs, identities, tools, budgets, retries, child/remote jobs, outputs, and external effects.[12]

Classify whether the job is not starting, overlapping, stuck, retrying, duplicating effects, exceeding budgets, or failing delivery. Validate the kill switch and stop all layers. Do not replay a partially committed write until remote state is reconciled.

## Preserve useful logs safely

Increase verbosity only for the minimum duration and understand what it records. Use bounded time windows and line/size limits. Redact credentials, authorization headers, cookies, private prompt/session content, personal identifiers, internal URLs, and sensitive paths before sharing.

Preserve original authorized evidence separately; do not edit the only copy. Record command, time, source path, hash, and redaction method. Disable temporary debug logging after diagnosis.

## Restore from checkpoints and backups

Hermes documents checkpoints and rollback for file changes during a session; verify target-version scope and limitations.[13] Checkpoints do not necessarily cover configuration, dependencies, databases, external systems, messages, or remote side effects.

A complete recovery plan may require:

1. Code/release revision.
2. Dependency/lock/environment state.
3. Configuration and service environment.
4. Credentials or rotation.
5. Session/memory/database compatibility.
6. Workspace/files/checkpoints.
7. Gateway/API/service units and listeners.
8. External-system reconciliation or compensation.

Restore into an isolated validation environment first when possible. Test read, write, denied paths, restart, and rollback again before production cutover.

## Escalate incidents

Escalate when there is credential exposure, unauthorized user/tool access, cross-tenant data, public unauthenticated exposure, malicious extension/update, persistent unknown process, external mutation, physical-device effect, or inability to stop work.

Contain, preserve, scope, eradicate, recover, monitor, and add a deterministic regression. Follow the upstream security policy for project-vulnerability reporting.[14]

## Failure handling

| Diagnostic failure | Safe response |
|---|---|
| Command not in runtime help | Do not run it; use target docs/source or alternative read-only evidence |
| Diagnostic reveals a secret | Stop capture; rotate/revoke; sanitize authorized copies and logs |
| Reproduction requires production data | Build a synthetic case or obtain explicit bounded authorization |
| Safe mode changes failure unexpectedly | Compare disabled layers; do not assume root cause yet |
| Backup cannot be read/restored | Stop risky repair; create/verify another recovery path |
| Service restart creates duplicates | Stop; reconcile queue and remote state before another restart |
| Root cause remains ambiguous | Preserve evidence; narrow further; do not apply speculative mutation |
| Recovery test fails | Keep ingress disabled and restore the last known-good state |

## Required report

Report timeline, target/version/environment, affected scope, first error, collected evidence and redactions, layer classification, minimal reproduction, root cause versus hypotheses, approved repair, validation including denied paths, external reconciliation, rollback status, residual risk, and follow-up regression.

## References

[1]: https://hermes-agent.nousresearch.com/docs/reference/cli-commands "CLI commands reference"
[2]: https://hermes-agent.nousresearch.com/docs/reference/faq "FAQ and troubleshooting"
[3]: https://hermes-agent.nousresearch.com/docs/user-guide/cli "CLI interface"
[4]: https://hermes-agent.nousresearch.com/docs/getting-started/installation "Installation"
[5]: https://hermes-agent.nousresearch.com/docs/getting-started/updating "Updating and uninstalling"
[6]: https://hermes-agent.nousresearch.com/docs/user-guide/configuration "Configuration"
[7]: https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models "Configuring models"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers "Fallback providers"
[9]: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools "Tools and toolsets"
[10]: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage "Session storage"
[11]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/index "Messaging gateway"
[12]: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron "Scheduled tasks"
[13]: https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback "Checkpoints and rollback"
[14]: https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md "Hermes Agent security policy"
