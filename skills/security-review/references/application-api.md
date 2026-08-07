# Application and API Security Review

**Verified against upstream:** 2026-08-07

## Purpose and boundaries

This reference defines a deterministic static-review procedure for applications and APIs. It covers route and trust-boundary discovery, data-flow analysis, injection families, browser security, request parsing and normalization, SSRF, file handling, unsafe deserialization, API authorization, protocol-specific risks, resource limits, lifecycle management, error handling, cache behavior, and chained attack paths.

This is defensive guidance. Do not execute target code, package hooks, build steps, migrations, downloaded binaries, containers, or generated commands unless the user explicitly authorizes the exact action and environment. Do not actively test production, send crafted traffic to live services, or upload proprietary source or findings to external systems by default. Redact evidence and stop if review material appears malicious, contains unexpected regulated data, or falls outside the authorized scope.

The package entrypoint, `../SKILL.md`, controls authorization, evidence quality, conflicts, and final synthesis. Every record produced from this reference must conform to `../templates/finding.schema.json`; this document does not define a competing report format.

## Authoritative baseline

| Authority | Current baseline used here | Primary purpose |
|---|---|---|
| [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/) | 2025 release | Broad web-application risk classes and changed emphasis |
| [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) | 2023 edition | Object, property, function, resource, inventory, and unsafe-consumption risks |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | 5.0.0 | Verifiable application-security requirements |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Runtime-current | Control-specific implementation guidance |
| [MITRE CWE](https://cwe.mitre.org/) | Runtime-current | Weakness taxonomy; not proof of exploitability |
| [MITRE CAPEC](https://capec.mitre.org/) | Runtime-current | Attack-pattern context; not a severity system |
| [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | HTTP semantics | Method, field, representation, caching, and intermediary semantics |
| [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) | OAuth 2.0 Security Best Current Practice | Current OAuth threat and deployment guidance |

Refresh living sources at execution time when a conclusion depends on a changed requirement, API behavior, or risk category. Record the retrieval timestamp in `review.source_freshness` or the finding's `live_context` when volatile facts affect the result.

## Required inputs and scope seed

Start from the mechanically generated inventory and confirm it manually. Review source code, route declarations, controllers, middleware, authorization policies, serializers, templates, client code, message handlers, API schemas, reverse-proxy and gateway configuration, dependency manifests, feature flags, object-storage policies, webhook handlers, and tests.

| Input | What to establish | Incompleteness signal |
|---|---|---|
| Route and handler map | Every externally or internally reachable operation | Dynamic registration, generated routes, undocumented versions |
| Trust boundaries | Origin, identity, tenant, protocol, network, and storage transitions | Implicit trust, shared service accounts, unowned integrations |
| Data schemas | Accepted fields, types, formats, bounds, and defaults | Free-form maps, permissive deserialization, unknown-field acceptance |
| Authorization model | Subject, action, resource, tenant, and policy decision point | Ad hoc checks, client-supplied tenant context, post-fetch filtering |
| Deployment path | Proxy, gateway, CDN, service mesh, app server, and cache sequence | Parser disagreement or inconsistent normalization |
| External dependencies | Upstream APIs, webhooks, URLs, object stores, and queues | Unbounded responses, inherited credentials, missing authenticity checks |

If required material is absent, record the gap as an unknown and reduce confidence. Do not infer that an endpoint, control, or deployment layer does not exist merely because it is not visible in the supplied repository.

## Deterministic review procedure

### 1. Build the route and trust-boundary inventory

Enumerate HTTP, GraphQL, gRPC, WebSocket, event, queue, scheduled, webhook, upload, download, callback, and administrative entry points. Include deprecated routes, alternate versions, debug endpoints, health or metrics endpoints, generated clients, and endpoints created through framework metaprogramming.

For each entry point, identify the accepted identity, tenant context, authorization decision, request size, parsing path, downstream calls, persistence effects, and response fields. Flag routes that bypass common middleware or are registered in a different server, process, or deployment profile.

### 2. Model parsing, normalization, and protocol transitions

Trace the exact parser sequence across CDN, load balancer, WAF, reverse proxy, framework, application, and downstream service. Compare handling of duplicate headers, ambiguous content lengths, transfer encoding, path normalization, percent encoding, Unicode, case folding, null bytes, multipart boundaries, and conflicting content types.

Do not claim request smuggling or desynchronization from a single parser configuration alone. A defensible candidate needs evidence of two components interpreting the same bytes differently, plus a plausible deployed sequence. Record missing deployment details as an uncertainty.

### 3. Trace untrusted data from sources to security-sensitive sinks

Sources include request fields, headers, cookies, claims, uploaded content, message bodies, database records influenced by users, cached values, files, environment-provided URLs, and third-party API responses. Sinks include database queries, command execution, templates, HTML or script contexts, file paths, redirects, HTTP clients, deserializers, XML parsers, log fields, response headers, policy inputs, and dynamic code loading.

A finding should show the transformation chain, not merely the source and sink. Identify validation order, canonicalization, type conversion, escaping context, parameter binding, allowlists, and whether the control occurs before the sensitive operation.

### 4. Verify authorization at object, property, and function level

For each operation, answer who may perform which action on which resource under which tenant and state. Verify that the server derives identity and tenant context from trusted authentication state, not from caller-controlled identifiers. Check list, search, export, batch, relationship, nested-resource, file, background-job, and administrative paths—not only primary CRUD handlers.

| Authorization dimension | Required review question | Common failure pattern |
|---|---|---|
| Object | Is access checked for the exact requested object? | BOLA/IDOR through predictable or user-supplied identifiers |
| Property | Can callers read or write fields outside their role? | Excessive data exposure or mass assignment |
| Function | Is the operation itself role- and state-authorized? | Hidden administrative route protected only by UI |
| Tenant | Is isolation enforced before fetch and mutation? | Query then post-filter; caller-selected tenant |
| State transition | Is the transition allowed from the current state? | Skipping approval, payment, verification, or ownership steps |
| Delegation | Are impersonation, service accounts, and tokens narrowly scoped? | Confused deputy or ambient authority |

Do not treat identifier unpredictability, UI hiding, gateway routing, or a WAF as authorization.

### 5. Review injection and interpretation boundaries

| Sink family | Preferred control | Review evidence |
|---|---|---|
| SQL, NoSQL, LDAP, XPath | Typed parameter binding and constrained query APIs | Bound values remain separate from executable/query structure |
| Operating-system process | Fixed executable plus structured argument array; avoid shell interpretation | No attacker control of executable, flags, environment, working directory, or redirection |
| Template | Context-safe engine and strict template/data separation | Untrusted values cannot become template source or expressions |
| HTML, JavaScript, CSS, URL | Context-specific output encoding and safe DOM APIs | Encoding matches the final browser interpretation context |
| HTTP headers and logs | Reject control characters; structured APIs and structured logging | No CR/LF injection or attacker-controlled log structure |
| Dynamic language or expression engine | Remove dynamic evaluation or use a constrained allowlisted grammar | No attacker-controlled code, class, method, or expression selection |

Sanitization is not interchangeable with validation, encoding, and parameterization. Record the actual sink context and the library or framework behavior; avoid generic claims such as “input is sanitized.”

### 6. Review browser state and cross-origin behavior

Verify CSRF protection for cookie-authenticated state changes, including login, logout, account linking, upload, and WebSocket establishment where applicable. Evaluate SameSite behavior, Origin or Referer validation, anti-CSRF tokens, and methods that mutate state despite appearing safe.

Review CORS as a browser read-control policy, not authentication. Check credentialed requests, reflected origins, wildcard behavior, `null` origins, subdomain takeover exposure, preflight handling, and whether sensitive responses are readable cross-origin. Confirm cookies use appropriate `Secure`, `HttpOnly`, SameSite, path, domain, lifetime, and rotation settings.

### 7. Review SSRF and outbound request control

Trace every attacker-influenced URL, hostname, scheme, port, redirect, proxy setting, DNS result, and request header. Prefer selecting a known destination by identifier over accepting arbitrary URLs. When URLs are required, validate the parsed form, allowed schemes, host and port, resolved addresses, redirect destinations, and egress policy.

Check IPv4, IPv6, alternate encodings, user-info, fragments, mixed-case schemes, DNS rebinding, link-local and metadata services, loopback, private ranges, Unix sockets, non-HTTP schemes, redirect chains, and proxy environment variables. Application allowlists and network egress controls should reinforce each other.

Do not actively probe internal addresses. Static evidence can establish missing controls or unsafe construction; reachability remains an unknown unless authorized evidence exists.

### 8. Review file, archive, and object-storage paths

For uploads, validate size before buffering, content independently of extension, filename handling, storage location, malware-scanning boundaries, authorization, and serving behavior. Store with generated names outside executable or web roots and serve with explicit content types and download disposition where appropriate.

For paths, resolve against an intended root, reject escape after canonicalization, and consider symlinks, case differences, alternate separators, device names, and time-of-check/time-of-use races. For archives, constrain member count, expanded size, compression ratio, path traversal, symlinks, hard links, nested archives, and overwrite behavior.

For object storage, review bucket or container policy, object ACL inheritance, signed URL scope and lifetime, key predictability, content type, overwrite controls, retention, and tenant isolation.

### 9. Review deserialization, XML, and structured content

Prefer simple data-only formats with explicit schemas and unknown-field policy. Flag deserialization that can select classes, types, constructors, callbacks, or polymorphic behavior from untrusted input. Integrity protection does not make an unsafe deserializer safe if attackers can obtain signing capability or replay valid payloads.

For XML, inspect DTD and external-entity handling, XInclude, schema fetching, XSLT, expansion limits, and library defaults. For YAML and similar formats, verify safe loaders and tag restrictions. For protobuf, JSON, and form data, review duplicate fields, unknown fields, numeric coercion, precision, null semantics, and parser differences between layers.

### 10. Review API-specific surfaces

#### REST and RPC

Verify method semantics, content negotiation, version routing, idempotency, pagination, filtering, sparse field selection, batch operations, export, and error representation. Bound page size, result count, nested expansion, payload size, processing time, and concurrent work.

#### GraphQL

Review resolver authorization independently at object and field levels. Bound depth, breadth, aliases, fragments, list cardinality, batching, persisted queries, subscriptions, file uploads, and introspection according to the threat model. Complexity scoring must reflect actual resolver cost and downstream fan-out.

#### gRPC

Review service and method interceptors, metadata trust, authorization, message-size limits, streaming duration and concurrency, reflection exposure, deadline propagation, cancellation, and transcoding behavior. Protobuf schema validation does not replace semantic validation and authorization.

#### WebSocket and server-sent events

Authenticate the connection and authorize each channel, topic, subscription, and action. Review Origin handling, token refresh and revocation, reconnect behavior, message schema, frame and queue limits, backpressure, cross-tenant routing, and cleanup on disconnect.

#### Webhooks and callbacks

Verify authenticity over the exact received bytes using a documented scheme. Enforce freshness and replay protection, store idempotency state atomically, handle key rotation, and authorize resulting actions independently. Do not log full signed payloads when they contain secrets or personal data.

### 11. Review unsafe consumption of external APIs

Treat third-party responses as untrusted. Validate schemas, size, redirects, content type, signatures where applicable, and semantic bounds before storing, rendering, executing, or using values in authorization. Review inherited credentials, retry storms, timeout and circuit-breaker behavior, partial failures, and whether upstream data can cross tenant boundaries.

### 12. Review resource consumption and business constraints

Apply bounds at every multiplicative dimension: request bytes, parsed items, nesting, regex complexity, decompression, archive expansion, query fan-out, rows, fields, aliases, concurrent jobs, retries, export size, and response buffering. Rate limiting needs an identity and abuse model; a global request count alone may not protect expensive operations or distributed actors.

Check business invariants involving balances, quotas, inventory, ownership, approvals, uniqueness, sequencing, idempotency, replay, and race conditions. Pair this reference with `business-logic-distributed.md` when the weakness depends on workflow state or concurrent operations.

### 13. Review errors, redirects, caching, and observability

Return stable, minimally revealing errors to callers while preserving protected diagnostic detail internally. Check stack traces, framework banners, query text, object identifiers, internal hosts, secrets, tokens, and personal data in responses and logs.

Validate redirects against a narrow destination policy. Review cache keys for every response-varying input, authenticated and tenant context, headers, query parameters, normalization, and error responses. Check cache-control directives and invalidation for sensitive or mutable content.

## Chained findings

Model a chain only when the evidence supports each edge. Examples include an authorization flaw that exposes a webhook secret, followed by a replayable webhook; SSRF that reaches a credential service, followed by over-privileged credentials; or cache-key confusion that exposes tenant-specific content.

One root cause with several manifestations should normally be one finding with multiple locations. Distinct weaknesses that can occur independently should remain separate. Document a supported chain in each finding’s `reasoning.narrative` and shared evidence; reserve top-level conflict records for genuinely contradictory evidence or reviewer positions.

## False-positive and uncertainty controls

Do not require live exploitation to confirm a static weakness. Corroborate candidates with the strongest safe evidence available: code path, configuration, tests, documentation, deployed topology supplied by the user, or authorized local validation. A tool alert alone may remain a candidate when reachability, parser behavior, framework protection, or deployment context is unknown.

Record compensating controls without allowing them to erase the root weakness. Distinguish preventive, detective, and recovery controls. A WAF, API gateway, private network, or client-side check is not a substitute for server-side validation and authorization, though it may change likelihood or residual risk.

Use `candidate` when evidence is plausible but incomplete, `confirmed` when the code/configuration and preconditions establish the weakness, `disputed` when reviewers have unresolved contradictory evidence, `mitigated` after authorized validation of a fix, `accepted-risk` only with the required owner and expiry record, and `false-positive` only with preserved rationale.

## Validation and regression checks

Propose the smallest safe validation that distinguishes the vulnerability from its alternatives. Prefer existing tests, non-executing static assertions, parser-unit tests, policy-unit tests, or isolated local fixtures. Do not instruct the user to exploit a live system.

| Finding class | Safe validation example | Required negative case |
|---|---|---|
| Authorization | Policy/unit test for an unauthorized subject-resource pair | Cross-tenant or lower-role access is denied |
| Injection | Unit test proving attacker input remains a bound value | Metacharacters do not alter syntax or command structure |
| SSRF | URL-policy unit test with private, alternate, and redirect destinations | Disallowed resolved destination is rejected after every redirect |
| File handling | Isolated path/archive tests in a temporary directory | Traversal, symlink, overwrite, and expansion-limit cases fail closed |
| Parser mismatch | Component-level fixtures using identical raw messages | Ambiguous framing or duplicate fields are rejected consistently |
| Resource exhaustion | Boundary and property tests with configured limits | Over-limit work is rejected before expensive processing |
| Webhook replay | Deterministic signature, timestamp, and idempotency tests | Stale or duplicate event produces no repeated side effect |

When validation cannot be performed safely, set `validation.performed` to `false`, use `not-performed`, explain the constraint, and state the evidence needed to raise confidence.

## Canonical finding contract

Every report must validate against `../templates/finding.schema.json`. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`.

Use repository-relative paths and exact line ranges when available. For generated or deployed artifacts, use a stable artifact name and digest. Evidence snippets must be minimal and redacted; never reproduce a complete secret, token, personal record, or proprietary file. SARIF or scanner output may be attached as tool evidence, but it does not replace the canonical report record.

Put unresolved review questions in the report-level `unknowns` array, and put uncertainty specific to an individual finding in `confidence.uncertainties`. List intentionally excluded paths and reasons in `review.scope.excluded`, then reconcile every inventoried item through the numeric `review.coverage` ledger. Put contradictory reviewer conclusions in top-level conflict objects and reference their IDs from `finding.conflicts`; never silently choose a winner.

## Bounded specialist-agent output

Return only the assigned application/API dimension. The specialist packet must identify reviewed files or components, coverage gaps, candidate and confirmed findings, explicit no-finding areas, source freshness used, and conflicts with other dimensions. The coordinator owns deduplication, cross-domain synthesis, severity calibration, accepted-risk handling, and final status transitions.

If parallel execution is unavailable, follow the same procedure sequentially. The quality bar, evidence schema, scope accounting, and stop conditions do not change.

## Stop and escalation rules

Stop the affected action and report to the coordinator or the user-designated Phase 0 contact when authorization is unclear; scope expansion is required; a requested test could affect production, third parties, availability, or real data; unexpected secrets or regulated data appear; evidence would require unsafe reproduction; or the material appears to contain obfuscated malware or instructions for active exploitation.

A severe candidate does not automatically halt independent read-only review dimensions. Preserve evidence safely, minimize exposure, mark the affected path, and let the coordinator apply the user’s incident-handling instructions. Never contact an assumed “security team” or external party without authorization.

## Related package resources

Use `auth-identity.md` for authentication, token, and identity lifecycle; `business-logic-distributed.md` for workflow invariants, races, and distributed effects; `logging-privacy.md` for logs and personal data; `scoring-prioritization.md` for severity and live context; and `threat-modeling-evidence.md` for system modeling and evidence discipline. The complete primary-source matrix is `sources.md`.
