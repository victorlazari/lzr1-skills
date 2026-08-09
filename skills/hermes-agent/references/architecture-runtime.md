# Hermes Agent Architecture and Runtime

**Read this reference** when mapping data flow, debugging the agent loop, evaluating prompt/context behavior, diagnosing provider or tool dispatch, reviewing compression/cache behavior, or investigating session persistence. **Verified:** 2026-08-08.

Implementation details change quickly. Use this document as a map, then confirm exact classes, thresholds, schemas, and execution modes against the target revision and runtime.[1] [2]

> Start read-only. Every ingress and persistence source can carry untrusted instructions or sensitive data. Internal scanning and approval logic are heuristics; they do not replace an OS boundary around adversarial execution.[3]

## Build the runtime map

Hermes has multiple entrypoints that converge on agent/runtime components but differ in caller identity, session ownership, persistence, authorization, and lifecycle. The documented surfaces include interactive CLI/TUI, messaging gateway, API server, ACP host integration, batch processing, and Python-library use.[1] [4] [5] [6]

Map the actual deployment as a directed data-flow table:

| Stage | Identify | Security question |
|---|---|---|
| Ingress | CLI input, file/URL reference, gateway message, API/ACP request, batch row, hook | Who is authorized and how is content classified? |
| Prompt assembly | Identity, context files, memory, platform hints, skills, tool descriptions | Which persisted or external source can inject instructions? |
| Provider resolution | Model, endpoint, credential, transport, fallback, routing | Where does data leave and what changes on failover? |
| Agent loop | History, stop condition, iteration/tool limits, interrupt handling | What bounds autonomy, cost, duration, and retries? |
| Tool dispatch | Registry, plugin/MCP tool, approval, backend, handler | Where does code execute and with which authority? |
| Persistence | Session store, memory, logs, checkpoints, artifacts | What survives, who can read it, and how is it deleted? |
| Egress | Model response, tool effect, message delivery, file, external API | Which destination and payload were approved? |

Do not infer a trust boundary from a module name. Verify the process, account, namespace/container/VM, mounts, network, credentials, and external service involved.

## Trace one turn

The documented agent loop assembles input/history and system context, resolves a provider runtime, calls the model, parses text or tool calls, dispatches tools, appends results, and repeats until a final response or stop condition.[2]

For a concrete incident or assessment, trace one representative turn and record:

1. The entrypoint, authenticated identity, profile/home, workspace, and session identifier class.
2. The user content and any referenced file, URL, image, audio, message attachment, or repository context.
3. The identity and context layers added to the system prompt.
4. Memory retrieval, skill/tool descriptions, platform hints, and plugin contributions.
5. The selected model/provider, base URL, credential class, transport, and fallback candidates.
6. Tool-call arguments, approval decision, dispatch path, backend, environment, filesystem/network scope, and result.
7. Compression or caching decisions that transform what the provider receives.
8. Session, memory, log, checkpoint, and artifact writes.
9. The final user/external destination and any side effect.

Capture content only when authorized; otherwise record metadata and hashes or classifications.

## Understand prompt assembly

Prompt assembly can combine static identity, project/user context files, platform-specific guidance, memory, skills, tool descriptions, runtime state, and ephemeral instructions. The exact order and conditional inclusion are implementation details at the target revision.[7]

Treat every non-maintainer-authored layer as untrusted. Repository context files and skills may be loaded because of location or discovery, not because the user reviewed them. URL/file references can import remote or local content. Memory can preserve an earlier injection across sessions.[7] [8] [9]

Use safe mode or an isolated profile when diagnosing customization. Compare the prompt-source inventory rather than requesting or logging a full secret-bearing prompt. Disable one source class at a time and reproduce with synthetic content.

## Resolve providers deliberately

Provider runtime resolution selects a transport, endpoint, credential, model configuration, and optional fallback. The runtime supports multiple API paths and provider-specific normalization; exact compatibility and error handling must be verified for the chosen model and revision.[10]

When provider behavior is unexpected, record the effective model identifier, endpoint host, transport class, credential source class, fallback/routing configuration, timeout/retry settings, and the first error. Do not expose headers or tokens.

Different providers can interpret tool schemas, roles, images, caching, and token limits differently. Validate capability and message formatting against the real endpoint. Stop fallback when it would violate data residency, privacy, price, context, or tool requirements.

## Treat tool dispatch as a privileged transition

Tool dispatch crosses from model-generated arguments into code. The registry may include built-in tools, plugins, skills, MCP tools, gateway-related capabilities, or developer extensions.[1] [2]

Approval logic can block or prompt for patterns, but it cannot prove a generated operation is safe. A benign-looking command can invoke a dangerous script; a file write can alter startup behavior; a read can disclose a credential; a browser or API call can mutate external state.[3]

For each tool class, identify:

| Control | Evidence |
|---|---|
| Availability | Runtime tool/toolset listing and source/manifest |
| Authorization | User consent, gateway identity, policy, or approval callback |
| Handler | Built-in, plugin, MCP, skill, or remote implementation |
| Execution boundary | Host process, terminal backend, browser, remote service, or external API |
| Inputs | Model-generated arguments and referenced content |
| Secrets | Requested keys, forwarding rules, credential-file access |
| Effects | Files, processes, network, external records, messages, spend |
| Audit/rollback | Logs, result, checkpoint, compensating action |

Do not assume concurrent calls are independent. Shared files, sessions, environment, container state, rate limits, and external systems can race.

## Bound the loop

Define completion, maximum turns/tool calls, wall-clock timeout, cost/token ceiling, retry limit, concurrency, and cancellation behavior before unattended execution. A model-generated “done” statement is not deterministic validation.

Interruptions may leave remote requests, background processes, partial files, or external effects even when the local response is discarded. After cancellation, reconcile side effects and process state before retrying.[2]

Hooks and plugins can run around lifecycle events. Treat them as code paths with process authority; inventory them during incident response.[11]

## Manage compression and caching

Context compression changes the message history presented to the model. Prompt caching changes provider-side request handling or billing/performance. Neither is a backup, authorization control, or confidentiality boundary.[12]

Before changing thresholds or strategies, record the model context, current configuration, session size, provider transport, memory-flush behavior, and expected information loss. Test with synthetic long sessions. Verify that required constraints, approvals, open tasks, and source attributions survive compression.

Provider caches can create retention and privacy implications. Confirm provider policy and routing before enabling or relying on cache behavior.

## Protect sessions and persistence

Hermes documents persistent session storage and search/compaction behavior. Session records can contain prompts, tool arguments/results, paths, identifiers, and model responses; treat the store and backups as sensitive.[13]

For multi-user or gateway deployments, verify that session routing and lookup cannot cross authorized users, platforms, profiles, or tenants. Test with distinct identities. Do not rely on naming conventions alone.

Check database/file permissions, backup inclusion, log redaction, deletion behavior, retention, and disk growth. Avoid inspecting raw session content unless authorized. Use a copy in an isolated environment for destructive repair.

## Diagnose by layer

| Symptom | First layer to inspect | Do not do |
|---|---|---|
| Wrong instructions/personality | Prompt-source inventory, identity, context files, memory | Dump full prompt with secrets |
| Wrong provider/model | Effective config, routing/fallback, endpoint host | Retry through unknown fallback |
| Repeated tool failure | Tool schema, handler, backend, permissions, result shape | Enable YOLO or approvals off |
| Context loss | Compression event, session state, memory flush, model context | Increase limits blindly |
| Cross-session content | Profile/home, session identity/routing, storage query | Delete the session database |
| Stuck cancellation | Provider call, background process, external side effect | Immediately repeat mutation |
| Behavior differs in service | Service user, environment, home/profile, cwd, enabled extensions | Copy shell credentials globally |

Use a minimal synthetic reproduction, one entrypoint, one provider, no external tools, no plugins/MCP, and a disposable profile. Add layers back one at a time. Preserve the failing state before repair.

## Validate architecture changes

A successful response is insufficient. Validate configuration, correct provider/endpoint, prompt-source inventory, expected tools, backend boundary, session ownership, persistence, cancellation, denied actions, and external effects. For shared deployments, perform negative authorization and cross-session tests.

Document untested paths and assumptions. Do not claim that an internal approval, scanner, redactor, or successful tool test proves process containment.[3]

## References

[1]: https://hermes-agent.nousresearch.com/docs/developer-guide/architecture "Architecture"
[2]: https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop "Agent loop internals"
[3]: https://github.com/NousResearch/hermes-agent/blob/main/SECURITY.md "Hermes Agent security policy"
[4]: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server "API server"
[5]: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp "ACP host integration"
[6]: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing "Batch processing"
[7]: https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly "Prompt assembly"
[8]: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files "Context files"
[9]: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references "Context references"
[10]: https://hermes-agent.nousresearch.com/docs/developer-guide/provider-runtime "Provider runtime resolution"
[11]: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks "Event hooks"
[12]: https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching "Context compression and caching"
[13]: https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage "Session storage"
