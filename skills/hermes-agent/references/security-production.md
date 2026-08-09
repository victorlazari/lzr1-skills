# Hermes Agent Security and Production Operations

**Read this reference** for threat modeling, hardening, production readiness, security review, incident response, and vulnerability reporting. **Verified:** 2026-08-08.

The upstream security policy is the controlling source for the project security boundary. Re-read its current version before making a production or vulnerability-scope decision.[1]

> An adversarial LLM can produce arbitrary tool arguments, encode commands, invoke scripts, or exploit any privileged path available to the process. OS-level isolation is the only load-bearing boundary; in-process approvals, scanners, redaction, allowlists, and prompt rules are defense in depth.[1]

## Define the threat model

Record deployment type, users/tenants, ingress, input trust, data classification, provider/endpoints, tools, backends, host-side capabilities, plugins/MCP, memory/session stores, credentials, network, external systems, persistence, automation, and operators.

| Threat actor/source | Representative risk |
|---|---|
| Malicious user or message sender | Prompt injection, tool abuse, data exfiltration, cost exhaustion |
| Compromised webpage/repository/file | Embedded instructions, dependency substitution, credential theft |
| Model/provider failure or compromise | Malicious tool calls, retention/leakage, routing/capability mismatch |
| Skill/plugin/MCP/dependency | Supply-chain code execution, hidden network, secret access |
| Cross-tenant user | Session/memory/file/credential leakage |
| Misconfiguration/operator error | Public unauthenticated surface, broad mounts/env, approvals disabled |
| External-service attacker | Webhook replay, token theft, account mutation, callback abuse |
| Compromised update channel | Installer/package/image/source replacement |

List assets and unacceptable outcomes: credentials, private prompts and memory, source code, customer data, account control, filesystem integrity, network access, external records/messages, availability, spend, and audit evidence.

## Use the isolation hierarchy

| Posture | Appropriate use | Minimum controls |
|---|---|---|
| Local host process | Controlled personal input only with explicit risk acceptance | Dedicated unprivileged user, narrow workspace, minimal tools/credentials |
| Sandboxed terminal backend | Mixed input where terminal/code is the main hazardous path | Narrow mounts/env/network, non-root, limits, image provenance, denied-path tests |
| Outer container/VM around Hermes plus sandboxed execution | Adversarial input, shared users, gateways, production | Dedicated identity, full-process boundary, network policy, per-tenant controls, monitored services |
| Dedicated host/account | High-impact or regulated use | Strong administrative boundary, minimal services, centralized monitoring and recovery |
| No demonstrable boundary | Advisory/read-only work only | Do not enable execution or external mutation |

A terminal backend does not automatically isolate the agent loop, gateway, browser, plugin, MCP client, configuration reader, credential access, or other host-side code paths.[1] [2]

For containers/VMs, review user/root, capabilities, device/socket exposure, mounts, home/cwd, environment, secrets, network/metadata, namespaces, seccomp/MAC, resource limits, image digest, updates, persistence, logs, and escape impact. Do not use privileged mode, broad host mounts, runtime sockets, or host networking without a separately accepted risk.

## Minimize identity and authority

Use dedicated OS/service accounts, Hermes profiles, provider keys, messaging bots, external-system accounts, memory tenants, workspaces, and service credentials. Separate development, staging, and production.

Grant only required read/write scopes. Remove shell/browser/cloud/VCS credentials from the service environment unless explicitly needed. Avoid sudo and administrator/root execution. Restrict who can modify configuration, skills, plugins, service units, images, and executables.

Profiles separate Hermes state, not necessarily host credentials, filesystem, plugin state, browser sessions, or network identity. Use an outer tenancy boundary for untrusted multi-user deployments.[3]

## Secure configuration and secrets

Keep secrets out of `config.yaml`, source, templates, commands, logs, prompts, sessions, memory, fixtures, and reports. Use supported secret storage and owner-only permissions. Report key names/presence only.[2]

Review at minimum:

- Approval mode and any unrestricted/Yolo setting.
- Terminal backend, mounts, home policy, environment forwarding, credential-file access, network, and limits.
- Provider base URLs, fallback/routing, credential pools, model catalogs, and timeouts.
- Gateway/API bind, authentication, user allowlists/pairing, session routing, and services.
- Plugins, skills, MCP, hooks, memory providers, cron/goals/batch/delegation, and updater.
- Logging, session/memory retention, backups, snapshots, and permissions.

Never set `approvals.mode: off`, enable YOLO/unrestricted execution, accept all gateway users, or bind an unauthenticated API publicly as a convenience fix.[1] [2]

Use `scripts/hermes_preflight.py` only as an offline heuristic scan. Review every finding manually; absence of a finding is not proof of safety.

## Protect network surfaces

Default listeners to loopback. Put approved non-local access behind TLS, firewall/network policy, strong authentication, authorization, body/time/rate limits, monitoring, and a reverse proxy or equivalent perimeter.[4] [5]

Use deny-by-default platform users and explicit session mapping. Authenticate webhooks with signed/token verification plus replay controls where supported. Restrict outbound network to approved provider, integration, package, and control-plane destinations. Block cloud metadata, internal management planes, and private networks unless required.

Validate URL scheme, host, port, DNS behavior, redirects, and resolved destination before credential-bearing requests. Do not forward authorization headers across redirects.

## Review tools and side effects

Inventory actual tools and handlers at runtime. For each, map authorization, input trust, boundary, filesystem, network, secrets, external effects, audit, and rollback. Do not approve a toolset as a unit without reviewing members.[6]

Separate read-only inspection from mutation. Require target-specific confirmation for destructive actions, public exposure, package/code execution, credential access, messages, purchases, deployments, account changes, and broad data disclosure.

Model-generated code or arguments are untrusted. Canonicalize and validate paths/URLs before authorization. Reject traversal, unsafe symlinks, device/proc paths, shell interpolation, unsafe deserialization, and unbounded input/output.

## Secure extensions and supply chain

Review every skill, plugin, MCP server, provider/adapter extension, dependency, installer, image, and update as code. Pin immutable revisions/digests where practical, verify official integrity evidence, inspect lifecycle/install scripts, record hashes/inventory, and test removal.[7] [8]

Do not auto-install content suggested by a model, webpage, repository instruction, message, or tool output. Do not treat a marketplace/catalog listing as a security review.

Protect the update path with backups, release/security review, dependency-state capture, service drain, staged validation, and rollback. Mutable-branch installation is not reproducible production change control.[9]

## Bound data and persistence

Classify prompts, attachments, files, tool results, sessions, memory, logs, traces, backups, media, and generated artifacts. Minimize collection and provider disclosure. Define retention, deletion, export, and owner.

Memory and session stores can preserve prompt injection and sensitive tool output. Validate per-user/profile isolation and permissions. External memory requires explicit disclosure and tenant mapping.[10] [11]

Redaction is defense in depth. It can miss custom formats or encoded values. Prevent secret generation in outputs and avoid logging raw prompts/tool payloads by default.

## Control automation

Cron, hooks, goals, delegation, Kanban, batch, and gateway services require dedicated identities, narrow tools, deterministic gates, time/cost/concurrency/retry limits, idempotency, audit, expiry, and a tested kill switch.[12]

No unattended job may grant itself more authority, expand targets, install dependencies, expose a service, send consequential messages, merge/deploy, or spend beyond its approved contract. Revalidate scope and environment at resume.

## Establish a production gate

Use `templates/production-readiness.md`. A deployment is **no-go** until each applicable item has evidence or a named risk owner and explicit exception.

| Gate | Minimum evidence |
|---|---|
| Version/provenance | Pinned release/commit, installer/dependency/image review, inventory |
| Threat model | Ingress, tenants, data, tools, boundaries, external effects, abuse cases |
| Isolation | Full-process and terminal boundary maps plus denied-path tests |
| Identity | Dedicated least-privileged users/profiles/credentials and rotation |
| Configuration | Redacted review, config check, no literal secrets, safe approvals |
| Network | Listener inventory, loopback/perimeter/TLS/auth/rate limits, egress policy |
| Multi-tenancy | Per-user sessions/workspaces/memory plus cross-user negative tests |
| Extensions | Reviewed/pinned skills, plugins, MCP, hooks, dependencies |
| Automation | Contracts, budgets, idempotency, kill switch, reconciliation |
| Monitoring | Health, auth denials, errors, spend, queues, listeners, secret-safe logs |
| Recovery | Tested backups, rollback, credential revocation, incident owner |

Avoid binary “secure” claims. Record tested revision, scope, assumptions, untested paths, exceptions, and expiry date.

## Execute adversarial validation

Use synthetic data and disposable accounts/profiles. Test:

1. Prompt injection in user input, repository context, webpages, tool output, memory, skill, and attachment.
2. Path traversal and symlink escape against read/write tools.
3. Secret-file, cloud-metadata, and unapproved environment access.
4. Disallowed network, redirect, internal-service, and exfiltration attempts.
5. Approval bypass attempts through scripts, encoding, aliases, and indirect tools.
6. Unauthorized gateway/API/webhook users and cross-session access.
7. Malformed, oversized, slow, duplicate, replayed, and reordered requests.
8. Provider fallback to an unapproved destination.
9. Timeout/cancel with child/remote-process and side-effect reconciliation.
10. Resource exhaustion, concurrency, retry storm, and spend ceiling.
11. Service restart, credential expiry, state corruption, and backup restoration.
12. Kill switch and token revocation while work is active.

A failed attack test is a release blocker for that boundary. A passed test supports only the exact tested path.

## Monitor without creating a second data leak

Monitor process/service health, listeners, authorization denials, errors by class, queue/run age, retry rates, provider usage/spend, tool denials, storage growth, and update drift. Alert on public bind changes, approvals weakening, new extensions/MCP, secret-file permission drift, unknown users, cross-session anomalies, and runaway automation.

Do not send raw prompts, credentials, private attachments, or full tool results to centralized logs by default. Protect logs/backups with access controls and retention.

## Respond to incidents

1. **Contain:** stop ingress and automation; revoke/disable high-risk credentials; isolate network/process without destroying evidence.
2. **Preserve:** record time, version/commit, configuration metadata, processes, listeners, extensions, sessions/run IDs, logs, and hashes with secrets redacted.
3. **Scope:** identify users, data, credentials, tools, external systems, and persistence reached.
4. **Eradicate:** remove the confirmed cause, not merely its symptom; review skills/plugins/MCP/hooks/update path.
5. **Recover:** restore a known-good code/config/state set, rotate credentials, and validate positive and denied paths.
6. **Monitor:** watch for recurrence and reconcile external effects.
7. **Learn:** add deterministic regression tests, update threat model/runbooks, and assign follow-up owners.

Do not delete sessions, logs, containers, workspaces, or unknown files during initial containment unless required to stop ongoing harm and approved.

## Report vulnerabilities responsibly

Follow the current upstream security policy's reporting channel and scope. Do not publish credentials, exploit details, private data, or an uncoordinated zero-day. Distinguish project vulnerabilities from unsafe deployment configurations and heuristic-bypass reports that the policy explicitly treats outside its guaranteed boundary.[1]

When testing a live third-party deployment, obtain authorization and avoid destructive or privacy-impacting actions.

## Failure handling

| Finding | Required response |
|---|---|
| Adversarial input with local host execution | No-go; add whole-process isolation or disable execution |
| Public unauthenticated listener | Stop/bind loopback; add perimeter and auth before exposure |
| Shared identity/session leakage | Stop shared ingress; preserve evidence; isolate tenants and rotate affected secrets |
| Literal secret in config/log/session | Revoke/rotate; sanitize authorized copies; repair source and logging |
| Unreviewed plugin/skill/MCP | Disable/quarantine; inventory and review before enablement |
| Approvals disabled/Yolo enabled | Restore safer mode; determine whether any execution occurred |
| Broad mount/env/credential passthrough | Stop execution; narrow boundary; rotate exposed credentials if needed |
| Kill switch ineffective | No-go; repair process/remote-work ownership and retest |
| Backup not restorable | No-go for risky change; create and test a recovery point |
| Security claim conflicts with policy/runtime | Stop; record conflict and refresh first-party evidence |

## References

[1]: https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md "Hermes Agent security policy"
[2]: https://hermes-agent.nousresearch.com/docs/user-guide/configuration "Configuration"
[3]: https://hermes-agent.nousresearch.com/docs/user-guide/profiles "Profiles"
[4]: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/index "Messaging gateway"
[5]: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server "API server"
[6]: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools "Tools and toolsets"
[7]: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins "Plugins"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp "MCP"
[9]: https://hermes-agent.nousresearch.com/docs/getting-started/updating "Updating and uninstalling"
[10]: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory "Persistent memory"
[11]: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage "Session storage"
[12]: https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron "Automate with cron"
