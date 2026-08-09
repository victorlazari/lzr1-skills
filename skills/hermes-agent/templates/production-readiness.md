# Hermes Agent Production Readiness Gate

**Deployment ID:** `{{deployment_id}}`

**Owner:** `{{owner}}`

**Review date:** `{{yyyy-mm-dd}}`

**Target revision/version:** `{{immutable_revision_or_version}}`
**Decision:** `{{go | conditional-go | no-go}}`

> Mark an item **pass** only with recorded evidence. Mark untested or ambiguous items **fail** or **blocked**, not “assumed.” Exceptions require an owner, compensating control, and expiry.

## Decision summary

{{Summarize the deployment purpose, users, data, ingress, enabled capabilities, material findings, exceptions, and release decision.}}

| Gate | Status | Evidence owner | Blocking issue / exception |
|---|---|---|---|
| Provenance and lifecycle | `{{pass_fail_blocked_not-applicable}}` | `{{owner}}` | `{{item}}` |
| Threat model and scope | `{{status}}` | `{{owner}}` | `{{item}}` |
| Full-process and execution isolation | `{{status}}` | `{{owner}}` | `{{item}}` |
| Identity and authorization | `{{status}}` | `{{owner}}` | `{{item}}` |
| Configuration and credentials | `{{status}}` | `{{owner}}` | `{{item}}` |
| Network, gateway, and API | `{{status}}` | `{{owner}}` | `{{item}}` |
| Data, sessions, and memory | `{{status}}` | `{{owner}}` | `{{item}}` |
| Extensions and supply chain | `{{status}}` | `{{owner}}` | `{{item}}` |
| Automation and external effects | `{{status}}` | `{{owner}}` | `{{item}}` |
| Validation and abuse testing | `{{status}}` | `{{owner}}` | `{{item}}` |
| Monitoring and operations | `{{status}}` | `{{owner}}` | `{{item}}` |
| Recovery and incident response | `{{status}}` | `{{owner}}` | `{{item}}` |

## 1. Provenance and lifecycle

| Check | Status | Evidence |
|---|---|---|
| Canonical upstream, release/commit, package, installer, and image sources are recorded. | `{{status}}` | `{{evidence}}` |
| Code, dependencies, lock/state files, images, and build artifacts are pinned or reproducibly identified. | `{{status}}` | `{{evidence}}` |
| Installation and update scripts were reviewed before execution. | `{{status}}` | `{{evidence}}` |
| Backup, staged update, health checks, rollback, and uninstall ownership are tested. | `{{status}}` | `{{evidence}}` |
| Security policy and version-scoped documentation were refreshed. | `{{status}}` | `{{evidence}}` |

## 2. Threat model and scope

| Check | Status | Evidence |
|---|---|---|
| Users, tenants, entrypoints, inputs, data classes, tools, services, and external systems are inventoried. | `{{status}}` | `{{evidence}}` |
| Untrusted content paths include messages, repositories, webpages, files, tool output, skills, memory, and MCP. | `{{status}}` | `{{evidence}}` |
| Unacceptable outcomes and trust transitions are documented. | `{{status}}` | `{{evidence}}` |
| Tested scope, untested paths, assumptions, exceptions, and revalidation triggers are explicit. | `{{status}}` | `{{evidence}}` |

## 3. Full-process and execution isolation

| Check | Status | Evidence |
|---|---|---|
| The whole Hermes process is isolated for mixed/untrusted input, or execution is disabled. | `{{status}}` | `{{evidence}}` |
| Terminal/code backend user, mounts, environment, network, image, limits, persistence, and cleanup are reviewed. | `{{status}}` | `{{evidence}}` |
| Host-side browser, gateway, plugins, MCP, files, credentials, and services are mapped separately. | `{{status}}` | `{{evidence}}` |
| No privileged mode, runtime socket, broad host mount, host networking, or unnecessary device/capability is present. | `{{status}}` | `{{evidence}}` |
| Denied path, symlink, environment, metadata, egress, resource, timeout, and cancellation tests pass. | `{{status}}` | `{{evidence}}` |

## 4. Identity and authorization

| Check | Status | Evidence |
|---|---|---|
| A dedicated unprivileged OS/service identity and Hermes profile are used. | `{{status}}` | `{{evidence}}` |
| Provider, platform, external-system, and memory identities are least privileged and environment-specific. | `{{status}}` | `{{evidence}}` |
| Gateway users are deny-by-default with explicit allowlist/pairing and session mapping. | `{{status}}` | `{{evidence}}` |
| Two authorized users and one denied user were tested without cross-session/file/memory leakage. | `{{status}}` | `{{evidence}}` |
| Consequential tools require target-specific consent or an independently approved automation contract. | `{{status}}` | `{{evidence}}` |

## 5. Configuration and credentials

| Check | Status | Evidence |
|---|---|---|
| Effective profile/home, config paths, precedence, and service environment are recorded. | `{{status}}` | `{{evidence}}` |
| `hermes config check` or the target-version equivalent passes. | `{{status}}` | `{{evidence}}` |
| No literal secrets are stored in YAML, source, commands, prompts, sessions, templates, or logs. | `{{status}}` | `{{evidence}}` |
| Secret files/stores have owner-only access; credential scopes, rotation, revocation, and expiry are documented. | `{{status}}` | `{{evidence}}` |
| Approvals are not disabled, unrestricted/Yolo mode is off, and environment/credential forwarding is minimal. | `{{status}}` | `{{evidence}}` |

## 6. Network, gateway, and API

| Check | Status | Evidence |
|---|---|---|
| Listener inventory matches the approved design; loopback is the default. | `{{status}}` | `{{evidence}}` |
| Non-local access has TLS, firewall/network policy, authentication, authorization, and rate/body/time limits. | `{{status}}` | `{{evidence}}` |
| API server uses a high-entropy key and does not expose sensitive logs. | `{{status}}` | `{{evidence}}` |
| Webhooks verify identity/signature/token and replay where supported. | `{{status}}` | `{{evidence}}` |
| Egress is limited to approved providers/integrations; metadata and internal management planes are blocked. | `{{status}}` | `{{evidence}}` |
| Redirect and destination handling prevents credential forwarding to unapproved hosts. | `{{status}}` | `{{evidence}}` |

## 7. Data, sessions, and memory

| Check | Status | Evidence |
|---|---|---|
| Prompt, attachment, tool-output, session, memory, log, media, and backup data classes are documented. | `{{status}}` | `{{evidence}}` |
| Provider and external-memory disclosure, region, retention, deletion/export, and tenant mapping are approved. | `{{status}}` | `{{evidence}}` |
| Session/memory stores and workspaces have least-privilege permissions and tested tenant separation. | `{{status}}` | `{{evidence}}` |
| Memory writes preserve provenance and exclude credentials or unverified inferences. | `{{status}}` | `{{evidence}}` |
| Retention and secure deletion/revocation procedures are assigned and tested where applicable. | `{{status}}` | `{{evidence}}` |

## 8. Extensions and supply chain

| Check | Status | Evidence |
|---|---|---|
| Every skill, plugin, MCP server, hook, provider/adapter extension, and dependency is inventoried. | `{{status}}` | `{{evidence}}` |
| Origin, immutable revision/digest, integrity, license, requested secrets, network, subprocesses, and lifecycle were reviewed. | `{{status}}` | `{{evidence}}` |
| No extension was installed or executed solely because untrusted content requested it. | `{{status}}` | `{{evidence}}` |
| Changes in tool/resource/prompt schemas require review before enablement. | `{{status}}` | `{{evidence}}` |
| Uninstall/disable and state-ownership behavior are tested. | `{{status}}` | `{{evidence}}` |

## 9. Automation and external effects

| Check | Status | Evidence |
|---|---|---|
| Cron, hooks, goals, delegation, Kanban, batch, and background services have written execution contracts. | `{{status}}` | `{{evidence}}` |
| Time, token/cost, concurrency, output, retry, and scope limits are enforced. | `{{status}}` | `{{evidence}}` |
| Idempotency, duplicate-trigger handling, partial-failure reconciliation, and compensation are tested. | `{{status}}` | `{{evidence}}` |
| External messages, records, deployments, purchases, or deletes require preview and approved authorization. | `{{status}}` | `{{evidence}}` |
| Kill switch, expiry, orphan cleanup, and credential revocation were tested while work was active. | `{{status}}` | `{{evidence}}` |

## 10. Validation and abuse testing

| Test | Status | Evidence |
|---|---|---|
| Read-only discovery, configuration check, service health, and harmless functional path | `{{status}}` | `{{evidence}}` |
| Prompt injection through user, repository, webpage, file, tool output, memory, skill, and attachment | `{{status}}` | `{{evidence}}` |
| Path traversal, symlink, secret-file, environment, metadata, and unapproved-network denial | `{{status}}` | `{{evidence}}` |
| Unauthorized user/tool, cross-session access, malformed/oversized/slow/replayed request | `{{status}}` | `{{evidence}}` |
| Provider fallback, timeout/cancel, resource exhaustion, retry storm, and spend ceiling | `{{status}}` | `{{evidence}}` |
| Restart, credential expiry, update/rollback, state restore, and kill switch | `{{status}}` | `{{evidence}}` |

## 11. Monitoring and operations

| Check | Status | Evidence |
|---|---|---|
| Health, listeners, authentication denials, errors, queues, retries, cost, storage, and service restarts are monitored. | `{{status}}` | `{{evidence}}` |
| Alerts cover public-bind changes, approval weakening, new extensions, unknown users, and runaway automation. | `{{status}}` | `{{evidence}}` |
| Logs exclude credentials and minimize prompt, attachment, and tool-result content. | `{{status}}` | `{{evidence}}` |
| Retention, access control, clock/timezone, capacity, and on-call ownership are documented. | `{{status}}` | `{{evidence}}` |

## 12. Recovery and incident response

| Check | Status | Evidence |
|---|---|---|
| Code, dependencies, configuration, services, sessions/memory, data, and external-state recovery are documented. | `{{status}}` | `{{evidence}}` |
| Backups and checkpoints have integrity evidence and successful restore tests. | `{{status}}` | `{{evidence}}` |
| Credential revocation, ingress stop, process/network isolation, and evidence preservation are rehearsed. | `{{status}}` | `{{evidence}}` |
| Incident roles, escalation, security reporting, and post-incident regression workflow are assigned. | `{{status}}` | `{{evidence}}` |

## Exceptions

| Exception ID | Failed requirement | Risk | Compensating control | Owner | Approval | Expiry |
|---|---|---|---|---|---|---|
| `{{EX-001}}` | `{{requirement}}` | `{{impact}}` | `{{control}}` | `{{owner}}` | `{{approver_date}}` | `{{date_or_trigger}}` |

An exception cannot override an unknown identity, unauthenticated public access, demonstrated cross-user leakage, exposed credential, uncontrolled host execution with adversarial input, or an untested kill switch for consequential automation.

## Final decision

{{Explain the decision, conditions, and exact scope approved for release.}}

| Role | Name | Decision | Date |
|---|---|---|---|
| Deployment owner | `{{name}}` | `{{go_no-go}}` | `{{yyyy-mm-dd}}` |
| Security reviewer | `{{name}}` | `{{go_no-go_conditions}}` | `{{yyyy-mm-dd}}` |
| Operations owner | `{{name}}` | `{{ready_not-ready}}` | `{{yyyy-mm-dd}}` |
