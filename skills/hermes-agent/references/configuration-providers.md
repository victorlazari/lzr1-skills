# Hermes Agent Configuration and Providers

**Read this reference** for `config.yaml`, `.env`, `auth.json`, models, providers, credential pools, fallback chains, routing, timeouts, and safe configuration changes. **Verified:** 2026-08-08.

Configuration keys, defaults, provider catalogs, models, and transport behavior are volatile. Confirm them with the installed version's help, `hermes config`, configuration example, and first-party docs before writing.[1] [2]

> Start read-only. Never print or diff secret values. Treat custom endpoints, model catalogs, provider plugins, fallback routes, OAuth flows, and copied configuration fragments as trust-boundary changes.

## Map configuration sources

Hermes documents the following precedence for ordinary settings: CLI arguments, `config.yaml`, `.env` fallback, then built-in defaults. Secrets belong in `.env` or supported credential storage rather than literal YAML. `hermes config set` routes recognized secret keys to `.env` and non-secret settings to `config.yaml`.[1]

| Source | Use | Primary risk |
|---|---|---|
| CLI argument | Per-invocation override | Shell history, process listing, undocumented drift |
| `config.yaml` | Non-secret behavior | Literal secrets, unsafe copied keys, YAML ambiguity |
| `.env` | Secret variables and fallback values | Permissions, logs, inheritance, accidental commits |
| `auth.json` and provider stores | OAuth or managed credentials | Token theft, cross-profile reuse, backup leakage |
| Built-in default | Unset behavior | Default changes across releases |
| Managed/system scope | Administrator-pinned settings when supported | Operator/user policy conflict |

`HERMES_HOME` changes the state root. Profiles can select separate Hermes state, but subprocesses may still use the real account home unless terminal home policy is changed.[1] [3]

## Discover before changing

Use runtime help and read-only configuration views. Do not assume every command is side-effect-free; inspect its help in high-assurance environments.

```bash
hermes version
hermes --help
hermes config --help
hermes config
hermes config check
hermes model --help
```

Collect configuration **keys and classifications**, not raw secret values. Record the selected profile/home, model identifier, provider/base URL, terminal backend, approval mode, memory provider, enabled plugins/MCP/gateways, fallback/routing settings, and process-only overrides.[2] [4]

Run `scripts/hermes_preflight.py` for a bounded offline metadata scan. Its conservative scalar parser is not a YAML-schema validator and cannot prove the effective runtime configuration.

## Separate secrets from behavior

Use placeholders such as `${PROVIDER_API_KEY}` or `${env:PROVIDER_API_KEY}` where the installed version supports them. Hermes documents environment substitution in YAML; unresolved placeholders remain unresolved and unknown prefix forms are not silently expanded.[1]

Apply the following rules:

1. Have the user or secret manager supply values directly; do not request credentials in chat.
2. Keep secret files owner-only on POSIX where operationally possible.
3. Do not place secrets in YAML, command arguments, templates, logs, reports, screenshots, test fixtures, or version control.
4. Report only key name, presence, source class, scope, age/rotation status, and permission result.
5. Map each credential to an exact provider/base URL and prevent fallback to an unintended endpoint.
6. Use separate credentials for environments, profiles, tenants, users, and unattended jobs when the provider supports them.
7. Revoke and rotate exposed values; deletion from a file does not remove shell history, logs, backups, or remote copies.

Do not assume redaction catches every custom token shape. Avoid generating the sensitive value in the first place.

## Plan a safe change

Copy `templates/change-plan.md` and include a redacted before/after diff. Prefer verified `hermes config get`, `set`, and `unset` operations over ad hoc text replacement because the supported command can route secrets and preserve structure.[1]

| Change | Review before approval |
|---|---|
| Model/provider | Capability, context, data policy, region, cost, transport, endpoint identity |
| Custom base URL | TLS, ownership, authentication scope, logging, compatibility, egress policy |
| Fallback chain | Trigger conditions, credential availability, data transfer, capability mismatch, cost |
| Credential pool | Identity mapping, rotation, rate-limit behavior, failure and lockout handling |
| Provider routing | Allowed providers/models, privacy/data-collection controls, ordering, auditability |
| Timeout/retry | Idempotency, duplicate effects, stale-call behavior, maximum spend and duration |
| Auxiliary model | Data disclosed to auxiliary tasks, provider, model, and failure behavior |
| Model catalog | Origin, schema, integrity, cache/fallback, influence over model selection |

Back up the affected files without broadening their permissions. For complex YAML, use a YAML-aware editor and preserve comments/structure. Do not silently coerce unknown values or replace the entire file for a one-key change.

## Configure models and providers

Hermes supports provider/model configuration through documented top-level and provider-scoped settings. The exact catalog and supported transports change; discover the target version rather than copying a provider block from another release.[4] [5]

Validate a provider in stages:

1. Confirm the provider and model are supported by the selected runtime path.
2. Verify the endpoint identity and TLS/perimeter expectations.
3. Add the credential through the approved secret path.
4. Set the model/provider with a redacted diff.
5. Run configuration validation.
6. Perform a harmless non-tool prompt with bounded tokens/cost.
7. Test the expected failure path using a non-sensitive invalid configuration in an isolated profile.
8. Confirm logs, errors, and reports do not disclose the credential.

A model with tool calling, vision, audio, long context, or a specific wire protocol must be validated for that capability. A catalog label is not runtime proof.[6]

## Control fallbacks and routing

Fallback providers improve availability but can silently change jurisdiction, privacy, model capability, cost, context size, tool semantics, and credential use. The documented fallback mechanism can react to authentication, rate-limit, and server failures; verify current triggers and retry behavior before production use.[7]

Require all fallback destinations to be pre-approved. Test the chain with synthetic data, record which events trigger movement, cap retries and total duration, and surface the chosen provider in operational evidence. Fail closed when a fallback would violate data classification or capability requirements.

Provider routing and aggregator controls can constrain provider/model choices and data policies. Treat these settings as defense in depth; verify the effective route through provider-side evidence where possible.[8]

## Configure timeouts and retries

Provider-wide and model-specific timeout settings are documented, with legacy environment fallbacks and transport-specific limitations. Do not assume one timeout controls DNS, connection, streaming, stale-call detection, model execution, tool execution, or gateway response deadlines.[1]

Document the timeout hierarchy and maximum wall-clock duration. For write-capable workflows, do not blindly retry an ambiguous request: determine whether the provider or downstream tool may already have committed an effect.

## Protect model catalogs and plugins

The model catalog influences model identifiers and capabilities. Treat remote or self-hosted catalogs as privileged configuration input. Validate origin, schema, cache/fallback behavior, and change control before use.[6]

Provider plugins execute in the Hermes process and may request credentials or change runtime routing. Review code, manifest, dependencies, lifecycle, endpoints, data handling, and uninstall path. A plugin manifest is not a sandbox.[9]

## Validate and roll back

After a change, run the target version's configuration check, read back non-secret effective settings, perform a bounded smoke test, inspect redacted logs, and verify denied/unconfigured paths. Recheck file permissions and listeners if the change can affect services or exposure.

Rollback must restore the prior files, environment/service settings, credentials, and provider selection. If a credential may have been disclosed, restore configuration **and** rotate the credential.

| Failure | Response |
|---|---|
| Unknown key or type | Stop; compare target-version docs and migration guidance |
| Placeholder unresolved | Stop; confirm variable name/source without printing its value |
| Provider authentication fails | Do not echo token; verify key presence, scope, endpoint, and clock |
| Model rejected | Confirm identifier, transport, account access, and capabilities |
| Fallback chooses wrong destination | Disable the chain, preserve evidence, repair allowlist/order |
| Timeout causes duplicate risk | Stop automatic retry; reconcile provider/downstream state |
| Configuration differs across service and shell | Compare profile, home, service environment, user, and working directory |
| Secret appears in output/history | Contain, revoke/rotate, scrub authorized copies, and review logs/backups |

## References

[1]: https://hermes-agent.nousresearch.com/docs/user-guide/configuration "Configuration"
[2]: https://hermes-agent.nousresearch.com/docs/reference/cli-commands "CLI commands reference"
[3]: https://hermes-agent.nousresearch.com/docs/user-guide/profiles "Profiles"
[4]: https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models "Configuring models"
[5]: https://hermes-agent.nousresearch.com/docs/integrations/providers "AI providers"
[6]: https://hermes-agent.nousresearch.com/docs/reference/model-catalog "Model catalog"
[7]: https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers "Fallback providers"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/provider-routing "Provider routing"
[9]: https://hermes-agent.nousresearch.com/docs/developer-guide/adding-providers "Adding providers"
