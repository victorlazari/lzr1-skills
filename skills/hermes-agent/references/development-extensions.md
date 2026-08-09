# Hermes Agent Development and Extensions

**Read this reference** before building or reviewing Hermes plugins, tools, providers, platform adapters, CLI extensions, memory providers, Python-library integrations, or upstream changes. **Verified:** 2026-08-08.

APIs, registries, manifests, module paths, tests, and packaging conventions are volatile. Pin the target commit and use its source, tests, and developer documentation as the controlling contract.[1] [2]

> Extensions execute with the authority of their process unless an outer boundary says otherwise. A manifest, schema, type annotation, or plugin prefix does not sandbox code.

## Define the extension contract

Before coding, write a one-page contract:

| Field | Required definition |
|---|---|
| Extension point | Plugin, tool, provider, adapter, CLI, memory provider, library embedding, or core change |
| Trigger | Registration/discovery and invocation conditions |
| Inputs | Types, size, trust, optional fields, normalization |
| Outputs | Schema, error model, streaming, artifacts, side effects |
| Authority | Files, processes, network, secrets, accounts, messages, spend |
| Boundary | Host process, terminal backend, container/VM, remote service |
| Configuration | Non-secret keys, secret names, precedence, migration |
| Lifecycle | Install, initialize, invoke, cancel, shutdown, update, remove |
| Compatibility | Hermes revision/version, Python/runtime, platforms, transports |
| Validation | Unit, integration, adversarial, negative, cancellation, rollback |

Reject designs that cannot identify where untrusted input becomes code, credentials, filesystem paths, network destinations, or external mutations.

## Establish a safe development baseline

Use a clean clone/worktree at an immutable base revision and a dedicated development profile/home. Record runtime/interpreter, dependency manager, lock/state files, enabled plugins/MCP, environment-variable names, and test commands.[1] [3]

Do not run repository-supplied setup scripts, hooks, tests, or generated code until reviewed. Keep real credentials out of tests; use fakes or least-privileged disposable accounts. Avoid global package installation.

Use source and tests to confirm behavior that documentation leaves ambiguous. Record discrepancies instead of quietly coding to whichever source is convenient.

## Build plugins safely

Hermes plugins can bundle extensions and declare configuration or secret requirements. Review the plugin manifest, entrypoints, dependencies, import-time effects, lifecycle hooks, requested secrets, network, files, subprocesses, logging, and uninstall behavior.[4] [5]

A secure plugin should:

1. Perform no network, subprocess, or destructive work at import time.
2. Validate configuration before acquiring external resources.
3. Request only named credentials and never log their values.
4. Use explicit timeouts, bounded input/output, and cancellation.
5. Avoid shell interpolation and unsafe deserialization.
6. Normalize and confine paths; reject traversal and unsafe symlinks.
7. Validate endpoint schemes/hosts and disable redirects when credentials are at risk.
8. Make side effects idempotent or expose reconciliation/compensation.
9. Shut down workers and remote resources cleanly.
10. Remove only files/state that the plugin owns.

Built-in status does not remove the need for runtime discovery or security review.[5]

## Add tools deliberately

A tool schema is part of the model-to-code boundary. Use clear descriptions, narrow typed parameters, strict validation, bounded strings/collections, explicit enums, and structured errors. Separate read-only analysis from mutation into different tools when practical.[6]

Never accept a free-form shell command, filesystem path, URL, SQL fragment, template, or destination when a constrained structured representation can work. Canonicalize before authorization. Validate after canonicalization and before effect.

For write tools, implement a preview/dry-run representation, idempotency key where applicable, explicit confirmation boundary, postcondition check, and rollback/compensation. Do not let model-supplied text change its own authorization scope.

Test malformed types, missing/extra fields, boundary sizes, Unicode, traversal, symlinks, redirects, timeouts, cancellation, duplicate requests, partial failure, injection strings, denied authorization, and secret redaction.

## Add providers and transports

Provider extensions handle sensitive prompts, credentials, tool schemas, streaming, usage, and errors. Implement only the documented contract for the pinned target revision.[7] [8]

Validate base URL and transport selection, authentication placement, message-role conversion, tool-call IDs, schema serialization, image/audio handling, token/context limits, streaming termination, timeout/cancel, usage accounting, retry classification, and redacted errors.

Do not retry authentication failures or ambiguous committed requests blindly. Preserve provider error codes while removing secrets and sensitive payloads. A provider compatibility claim must be backed by contract tests against representative features, not a single text completion.

## Add platform adapters

A messaging adapter must authenticate Hermes to the platform and authorize platform users separately. Implement stable identity extraction, allowlist/pairing, channel/thread/session mapping, normalized events, attachment limits, outbound destination validation, duplicate/replay handling, rate limits, and graceful startup/shutdown.[9] [10]

Treat display names, forwarded metadata, filenames, links, and message bodies as untrusted. Test two authorized users, one denied user, cross-session isolation, duplicate events, reordered events, malformed attachments, provider outage, restart, and token revocation.

Do not default to accept-all authorization or public listener exposure.

## Extend the CLI

CLI additions must follow the target parser/registration patterns, preserve machine-readable exit behavior, and avoid surprising side effects.[11]

Use descriptive help, validate before mutation, support explicit target/profile/home selection, and print secret metadata rather than values. Separate read-only inspection from mutating subcommands. For destructive actions, require a target-specific confirmation or an explicit non-interactive contract; do not make `--yes` bypass authorization.

Test help output, invalid/missing arguments, exit codes, non-interactive input, service-user environment, Unicode paths, and errors without stack/secret leakage.

## Implement memory providers cautiously

A memory provider controls durable prompt context and may disclose conversations externally. Define tenant identity, create/search/update/delete semantics, consistency, retention, encryption, export/deletion, outage/fallback, redaction, and migration.[12]

Never derive a global tenant solely from a display name. Keep provider credentials separate by environment/tenant, and test cross-user denial. Do not silently fall back between local and remote stores when doing so changes data handling.

## Embed Hermes as a Python library

Library embedding makes the host responsible for lifecycle, authorization, tool registry, configuration, cancellation, logging, and isolation. Use the documented high-level API for the pinned version rather than importing private internals.[13]

Construct explicit configuration, inject only reviewed tools, handle structured errors, close resources, and propagate cancellation. Do not reuse a mutable agent/session across tenants without a proven isolation design. Avoid module-global credentials or tool registries.

Test repeated initialization/shutdown, concurrent callers, cancellation, provider/tool failure, memory/session separation, and host log redaction.

## Preserve architecture boundaries

Before changing core runtime code, map prompt assembly, provider resolution, agent loop, tool dispatch, session storage, compression, gateway routing, and plugin discovery. Cross-cutting changes need regression tests at each affected boundary.[14]

Do not patch security or approval behavior with string matching alone. Model-generated code and arguments can bypass superficial patterns. Use least authority and OS isolation as primary controls.[15]

## Validate the supply chain

For every dependency, plugin, server, image, or generated artifact, record canonical source, version/revision/digest, lockfile change, maintainer/release evidence, license, install scripts, native code, transitive risk, and update policy.

Do not add dependencies by model-generated package name without verifying identity. Pin or lock reproducibly where the ecosystem permits. Review package-manager lifecycle scripts and container build context. Keep secret-bearing files out of build artifacts.

Generate an SBOM or dependency inventory when required by the deployment, and scan it with a separately maintained security workflow. Scanner output is triage evidence, not proof of safety.

## Use deterministic tests

The upstream contribution guide documents test and quality expectations; execute only reviewed project commands in an isolated development environment.[3]

Minimum test matrix:

| Layer | Required tests |
|---|---|
| Pure logic | Unit and property/boundary cases |
| Schema/parser | Valid, invalid, unknown, malicious, oversized inputs |
| Authorization | Allowed and denied identities/actions |
| Filesystem | Traversal, symlink, permissions, atomic write, rollback |
| Network | Host/scheme allowlist, TLS, redirects, timeout, replay |
| Secrets | No values in args, logs, errors, fixtures, artifacts |
| Lifecycle | Init, repeated init, cancel, shutdown, restart, uninstall |
| Compatibility | Pinned Hermes versions/transports/platforms |
| Integration | Fake/local service first; bounded live test only with approval |
| Regression | Every confirmed defect gets a deterministic test |

Avoid flaky sleeps and unrestricted live network in default tests. Use bounded fixtures, fake clocks, mock servers, and deterministic IDs.

## Review and release

Use separate implementation and adversarial review passes. Review every changed line plus manifest/dependency/lock changes. Run formatting, type/static checks, tests, package self-checks, secret scans, and whitespace/mode checks.

Release notes must state compatibility, configuration migration, new permissions/data flow, breaking changes, validation, and rollback. Sign or attest releases where the project workflow supports it. Do not claim upstream support until merged or documented by upstream.

## Failure handling

| Failure | Safe response |
|---|---|
| API/registry differs from docs | Stop; pin and inspect target source/tests |
| Extension requests undeclared secret | Deny; update contract/manifest and re-review |
| Tool performs an unpreviewed effect | Disable; preserve evidence; add regression and compensation |
| Provider leaks payload in error | Stop live tests; rotate exposed credentials; fix redaction |
| Adapter mixes users/sessions | Disable ingress; isolate state; treat as incident |
| Plugin import has side effects | Quarantine; redesign lifecycle before enablement |
| Dependency identity uncertain | Do not install; use canonical source or remove dependency |
| Cancellation leaves work running | Fix ownership/cleanup; reconcile remote state before retry |
| Test requires production credentials | Replace with fake/disposable scoped integration environment |

## Required report

Report the extension contract, target revision, files/dependencies, authority and data flow, configuration/secrets, implementation, deterministic tests, adversarial findings, compatibility, installation/update/removal, validation, residual risks, and rollback.

## References

[1]: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture "Architecture"
[2]: https://github.com/NousResearch/hermes-agent "Hermes Agent repository"
[3]: https://hermes-agent.nousresearch.com/docs/developer-guide/contributing "Contributing"
[4]: https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin "Build a Hermes plugin"
[5]: https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins "Built-in plugins"
[6]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-tools "Adding tools"
[7]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers "Adding providers"
[8]: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime "Provider runtime resolution"
[9]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters "Adding a platform adapter"
[10]: https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals "Gateway internals"
[11]: https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli "Extending the CLI"
[12]: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers "Memory providers"
[13]: https://hermes-agent.nousresearch.com/docs/guides/python-library "Using Hermes as a Python library"
[14]: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop "Agent loop internals"
[15]: https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md "Hermes Agent security policy"
