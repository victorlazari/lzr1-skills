# Hermes Agent Operating Model

**Read this reference** for installation, setup, profiles, entrypoints, updates, uninstallation, and lifecycle recovery. **Verified:** 2026-08-08.

Specific commands, paths, prerequisites, and installer behavior are volatile. Confirm them with the target version's `hermes --help`, official documentation, and inspected installer before acting.[1] [2]

> Start read-only. Installation, updates, dependency resolution, PATH changes, service creation, and uninstallation can execute third-party code or alter persistent state. Preview these effects and obtain explicit consent.

## Establish the target

Record the OS, architecture, shell, user, privilege model, `HERMES_HOME`, profile, current version/commit, installation method, desired channel/revision, network restrictions, state size, and recovery point. Do not mix source installs, package installs, application bundles, root installs, and user installs without mapping their different paths and launchers.

Hermes stores configuration and state under `~/.hermes` by default; `HERMES_HOME` and profiles can create separate state roots. Profiles isolate Hermes configuration, memory, sessions, and skills, but host tools may still share the normal account home and credentials depending on terminal home policy.[3] [4]

| Decision | Prefer | Escalate when |
|---|---|---|
| Personal evaluation | Per-user install, controlled input, no public listener | Execution reaches sensitive host data |
| Reproducible environment | Immutable commit/release plus recorded dependency state | Installer resolves a mutable branch |
| Shared or production use | Dedicated account and outer containment | Multiple users, external ingress, or adversarial content exists |
| Multiple identities | Separate profiles and dedicated external credentials | Host-level CLI credentials remain shared |
| Offline/restricted network | Pre-stage inspected artifacts and document integrity evidence | Installer or runtime fetches undocumented resources |

## Perform discovery before installation

Inspect the official installation guide and the installer source at the chosen revision. Download first, compare the expected origin, inspect privileges and destinations, then execute only after approval. Piping a mutable network response directly to a shell removes the inspect-before-execute control.[1] [5]

Verify prerequisites without installing them automatically. Record who owns each prerequisite, its source, version, license constraints, and whether a compiler, container runtime, browser dependency, or system package changes the trust boundary.

For an existing installation, collect read-only evidence:

```bash
command -v hermes
hermes version
hermes --help
hermes doctor
hermes config check
```

Do not assume `hermes doctor` is side-effect-free on every release; inspect runtime help or source when operating under strict change control.[2] [6]

## Plan installation

Use `templates/change-plan.md`. Include the following items in the approval packet:

| Area | Required preview |
|---|---|
| Source | Repository/release, immutable revision when practical, integrity mechanism |
| Code | Install directory, launcher, virtual environment, application bundle |
| Dependencies | Package manager, lock/state files, native packages, images, browser components |
| State | `HERMES_HOME`, profile, config, secrets, auth, sessions, memory, skills, logs |
| Shell | PATH edits, completion, startup-file changes |
| Services | Gateway/API units, autostart, user/system scope, listeners |
| Privilege | User versus root operations and created ownership |
| Network | Download hosts, provider endpoints, telemetry or model-catalog access |
| Recovery | Backup/checkpoint, old revision, uninstall path, state retention decision |

Do not run root mode, system package installation, service enablement, Playwright/system dependency installation, image pulls, or shell-profile mutation under generic “install Hermes” consent.

## Set up without exposing credentials

Prefer supported setup and configuration commands only after verifying them in runtime help. The documentation presents `hermes setup --portal` as one setup path and `hermes config` subcommands for configuration; these may initiate OAuth or network activity.[3]

Have the user enter credentials through the intended interactive or secret-management path. Never place a real credential in a command example, shell history, transcript, generated Markdown, or `config.yaml`. Validate presence and permissions without reading the value.

After setup, validate the selected profile, model/provider availability, configuration check, and a harmless non-tool interaction. Do not enable external tools, gateways, cron, hooks, MCP, plugins, or memory providers as implicit setup steps.

## Choose an entrypoint

Hermes exposes multiple entrypoints, including CLI/TUI, gateway, ACP, API server, batch processing, and Python-library integration. Each entrypoint has a different ingress, identity, persistence, and authorization surface.[2] [7] [8] [9]

| Entrypoint | Additional review |
|---|---|
| Interactive CLI/TUI | Launch directory, profile, terminal backend, context files, local user authority |
| Gateway/messaging | User authorization, session isolation, inbound content, outbound delivery, service lifecycle |
| API server | Bind address, API key, perimeter, request limits, logs, multi-user separation |
| ACP host | Host authorization, approval semantics, workspace boundary, protocol peer trust |
| Batch/trajectory | Dataset trust, concurrency, spend, output path, resume semantics, timeout |
| Python library | Caller identity, exception handling, tool registry, lifecycle, dependency pinning |

Do not treat an entrypoint as equivalent to another merely because each invokes the agent loop.

## Operate profiles deliberately

Use runtime profile help before creating, deleting, copying, or selecting profiles. Record the effective `HERMES_HOME`, profile-specific ports or services, and external credentials. A separate profile does not by itself create an OS-user, network, provider-account, or host-credential boundary.[4]

For shared deployments, assign dedicated external identities and explicitly test cross-profile and cross-session denial. Avoid symlinking secret or state directories between profiles unless the sharing is intentional, documented, and protected.

## Update safely

The documented update workflow can alter source, dependencies, configuration, application assets, and service behavior. The configuration supports pre-update snapshots/backups and policies for local source changes; inspect the actual target version before relying on a specific default.[3] [10]

Use this sequence:

1. Record version, commit, install method, profile, service state, and health evidence.
2. Inventory local modifications and untracked files without discarding them.
3. Back up critical state and verify that recovery material is readable.
4. Review release notes, security policy changes, migrations, dependencies, and installer/update changes.
5. Stop or drain external ingress when required.
6. Apply the update through the approved path.
7. Run syntax/import, configuration, health, listener, authorization, and controlled smoke tests.
8. Re-test denied users, denied tools, and rollback.
9. Re-enable ingress only after acceptance criteria pass.

Do not use `--yes`, force, discard, or unattended-update behavior until its exact effect on local changes, backups, configuration prompts, and services is approved.

## Roll back and uninstall

A rollback must cover code, dependencies, configuration schema, state compatibility, services, and external side effects. A source checkout alone may not restore a working deployment. Prefer an immutable prior revision plus a verified state snapshot and documented dependency restoration.[10]

Before uninstalling, ask whether to retain or destroy configuration, credentials, OAuth state, sessions, memory, skills, cron definitions, logs, caches, containers, images, and service units. Destruction is irreversible and requires separate consent.

After rollback or uninstall, verify process termination, listeners, services/autostart, launchers, PATH changes, ownership, containers, state retention, and credential revocation where appropriate.

## Failure handling

| Symptom | Read-only diagnosis | Safe response |
|---|---|---|
| Command not found | Resolve launcher and PATH; identify install method | Repair only the approved launcher/path |
| Version mismatch | Compare launcher target, source revision, and environment | Stop; do not mix installations |
| Dependency/import failure | Record interpreter, environment, and package state | Restore approved dependency state |
| Configuration rejected | Run config check and compare migration docs | Back up, preview migration, obtain consent |
| Update failure | Preserve logs, source status, snapshot, and service state | Restore known-good code and state together |
| Gateway fails after update | Keep ingress disabled; inspect redacted logs and ports | Roll back or repair under a new plan |
| State appears missing | Confirm profile and `HERMES_HOME` before writing | Stop to avoid initializing the wrong home |

Do not repeat a failed mutation unchanged. Do not “fix” an unknown install by deleting directories, reinstalling globally, or overwriting state.

## References

[1]: https://hermes-agent.nousresearch.com/docs/getting-started/installation "Installation"
[2]: https://hermes-agent.nousresearch.com/docs/reference/cli-commands "CLI commands reference"
[3]: https://hermes-agent.nousresearch.com/docs/user-guide/configuration "Configuration"
[4]: https://hermes-agent.nousresearch.com/docs/user-guide/profiles "Profiles"
[5]: https://github.com/NousResearch/hermes-agent/blob/3e6a081d60e8d04a03d37008464f44555bc88832/install.sh "Installer at the research snapshot"
[6]: https://hermes-agent.nousresearch.com/docs/reference/faq "FAQ and troubleshooting"
[7]: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server "API server"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp "ACP host integration"
[9]: https://hermes-agent.nousresearch.com/docs/guides/python-library "Python library"
[10]: https://hermes-agent.nousresearch.com/docs/getting-started/updating "Updating and uninstalling"
