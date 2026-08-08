# Layered Validation and Evidence Semantics

A YAML file is not correct merely because it parses. Validation must identify the consumer, compatibility target, scenario, source of truth, and unresolved coverage. Each layer answers a different question and must retain its own result.

## Outcome Contract

Every automated stage returns one of three assessment outcomes. An orchestration error, policy violation, invalid document, broken reference, or failed command is **failed**. A skipped, unavailable, missing-schema, dynamic-expression, untested-scenario, unresolved-alias, CRD-schema, or target-cluster gap is **incomplete**. Only fully executed declared coverage with no findings is **complete**.

| Outcome | Meaning | Permitted conclusion |
|---|---|---|
| `complete` | All declared checks executed and passed for the exact recorded scope | The recorded scope passed; no broader claim |
| `incomplete` | No proven failure, but at least one declared or necessary check lacks evidence | Do not call the input valid or release-ready |
| `failed` | At least one validity, security, reference, execution, or policy check failed | Remediate or obtain an explicit, documented disposition |

Exit codes follow the same convention: `0` complete, `1` failed, `2` incomplete or invalid assessment invocation. A failed result dominates incomplete coverage in final aggregation, while reports retain both counts.

## Validation Stack

| Layer | Question | Representative evidence | What it does not prove |
|---|---|---|---|
| Transport and path safety | Is the intended regular file inside the reviewed root and within bounds? | Canonical path, symlink rejection, size and count limits | YAML validity |
| YAML lexical/syntactic parse | Is the stream parseable under the declared YAML profile? | Parser/version, document count, parse diagnostics | Application meaning |
| Construction and data model | Are tags, keys, aliases, duplicate keys, depth, and types safe and supported? | Safe-loader mode, duplicate-key policy, JSON compatibility | Domain rules |
| Style lint | Does the document satisfy the repository’s style policy? | yamllint version, effective config, ignored paths | Schema or consumer acceptance |
| Application schema | Does the parsed value satisfy its declared schema dialect? | `$schema`, validator version, schema validity, instance errors | Runtime behavior or format assertions unless enabled |
| Domain semantics | Are required relationships and invariants satisfied? | Contract checks, reference checks, policy findings | External system state |
| Template/static analysis | Which inputs are discoverably consumed and which expressions are dynamic? | Static paths, dynamic snippets redacted, coverage gaps | All possible runtime paths |
| Render/lint matrix | Can declared Helm scenarios lint and render for a target? | Helm version, target version, ordered values inputs, outputs | API-server acceptance |
| Kubernetes schema | Do rendered objects match exact target-version and CRD schemas? | kubeconform version, strict mode, schema sources/digests | Admission, defaulting, controller behavior |
| Policy/security | Do rendered workloads satisfy the selected policy profile? | Versioned rules, profile, per-object findings | Cluster-specific admission policy |
| API-server dry-run | Does the authorized target server accept the objects without persistence? | Exact context, server version, admission response | Controller reconciliation or live rollout success |
| Runtime verification | Does the deployed system behave correctly? | Separate authorized deployment/test evidence | Covered by this skill’s default workflow |

## Evidence Minimums

A report records immutable inputs or digests, tool versions, exact commands with secrets removed, compatibility targets, environment isolation, scenario ordering, schema sources, result artifacts, findings, coverage gaps, authorization, and whether any network or cluster was contacted. Rendered manifests can contain resolved sensitive data and remain private artifacts unless separately sanitized.

| Evidence field | Required content |
|---|---|
| Scope | Repository root, chart path, file set, and Git commit or dirty-state disclosure |
| Compatibility | YAML profile, Helm version, Kubernetes minors, API versions, and schema dialect |
| Inputs | Canonical values file order, flags, local policy, CRD schemas, and dependency state |
| Tools | Executable versions and provenance; never only “latest” |
| Results | Per-stage exit, status, counts, bounded diagnostics, and artifact path |
| Gaps | Missing schema, dynamic template, external reference, skipped scenario, and unavailable target |
| Side effects | Network, dependency mutation, cluster contact, files changed, and rollback status |
| Publication boundary | Local evidence versus hosted review, target-server acceptance, or runtime result |

## Scenario Matrices

A default render is not a matrix. Enumerate meaningful values precedence, feature gates, ingress/service variants, security modes, API capabilities, and supported Kubernetes minors. Use `templates/validation-matrix.example.yaml` to declare expected results before running commands.

| Scenario property | Required decision |
|---|---|
| Label | Stable, non-secret identifier |
| Ordered values files | Exact precedence from lowest to highest |
| Command-line setters | Prefer reviewed files; record typed setters when unavoidable |
| Target Kubernetes minor | Explicit and currently supported or deliberately legacy |
| Expected objects | Required and forbidden kinds or names |
| Expected outcome | Complete, known failure, or intentionally incomplete |
| External references | Explicit kind/name or kind/namespace/name allowlist |

A scenario that unexpectedly renders no documents is failed for an application chart. A library chart can render no installable resources by design, but its exported helpers require validation through one or more reviewed consumer charts. Dynamic template use, `tpl`, `lookup`, file reads, capabilities branches, and plugin/post-renderer behavior remain explicit coverage items.

## Schema Discipline

JSON Schema validation begins only after duplicate-key rejection and JSON-data-model checks. Require an explicit supported `$schema`, validate the schema itself, prohibit implicit network reference retrieval, confine local references to the reviewed root, and state whether `format` assertions ran. JSON Schema metadata such as `default`, `examples`, and `deprecated` is annotation unless application logic gives it additional meaning.[1][2]

For Kubernetes, use exact target-version schemas and strict validation. Missing built-in or CRD schemas are incomplete coverage; do not use `-ignore-missing-schemas` to manufacture a clean result. Record local schema snapshot digests or commit-pinned remote sources and never treat a mutable third-party catalog as target-server authority.[3]

## Server Dry-Run Boundary

`kubectl apply --dry-run=server` contacts a real API server and can invoke defaulting, validation, and admission webhooks without persisting the object.[4] It therefore requires the user’s explicit authorization, exact context confirmation, and careful treatment of manifest contents. A server dry-run is stronger than offline validation but does not prove controller reconciliation, external dependency availability, rollout health, or production safety.

| Mode | Network/cluster | Default |
|---|---|---|
| Static package analyzers | None | Allowed |
| Helm lint/template in isolated local state | None unless dependencies or special features require it | Allowed |
| Kubeconform with reviewed local schemas | None | Allowed |
| Dependency build, remote schema, registry, or plugin | Network and possible mutation | Explicit consent required |
| API-server dry-run | Cluster contact and possible admission webhook processing | Explicit consent and context required |
| Install, upgrade, apply, delete, push, or publish | Mutating remote operation | Outside default workflow; separate confirmation required |

## Failure Triage

Fix transport and parse failures before schema findings, schema failures before semantic findings, render failures before rendered-object checks, and target-version schema failures before API-server claims. Do not suppress a diagnostic merely because a later tool produces a cleaner result; reconcile the semantic difference and document the disposition.

| Conflict | Required response |
|---|---|
| Parser A accepts, parser B rejects | Identify the consumer profile; make the document portable or constrain support explicitly |
| Schema passes, application fails | Add missing semantic constraints or application tests |
| Helm renders, kubeconform fails | Correct target-version or CRD schemas and rendered fields |
| Kubeconform passes, server rejects | Preserve admission/defaulting evidence and fix target-specific behavior |
| Local checks pass, runtime fails | Treat as a separate deployment/runtime defect; do not revise local evidence retroactively |

[1]: https://json-schema.org/draft/2020-12/json-schema-core
[2]: https://json-schema.org/draft/2020-12/json-schema-validation
[3]: https://github.com/yannh/kubeconform
[4]: https://kubernetes.io/blog/2019/01/14/apiserver-dry-run-and-kubectl-diff/
