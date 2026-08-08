# Helm Chart Engineering Workflow

## Establish the Chart Contract

Record the chart type, chart API version, chart version, application version, Kubernetes compatibility range, supported Helm majors, dependency state, and values sources before changing files. Helm 4.2.3 is current as of the source verification date, but some topic documentation remains partly Helm 3-oriented; the installed binary and its versioned command reference control exact behavior.[1][2]

| Field or artifact | Required interpretation |
|---|---|
| `apiVersion: v2` | Helm 3/4 chart format and dependencies in `Chart.yaml` |
| `type: application` | Installable chart expected to render resources in relevant scenarios |
| `type: library` | Non-installable helper chart; validate through reviewed consumer charts |
| `version` | Chart package version; SemVer-compatible and distinct from app version |
| `appVersion` | Informational application version; quote string-like values |
| `kubeVersion` | Declared compatibility constraint, not proof of successful validation |
| `values.yaml` | Canonical defaults and public configuration contract |
| `values.schema.json` | Machine-enforced values constraints for a declared JSON Schema dialect |
| `Chart.lock` and `charts/` | Resolved dependency evidence and packaged dependency state |

Custom chart metadata belongs under `annotations`; do not impose organization-specific annotation keys as universal Helm requirements. Preserve repository policy only when it is explicitly documented as a local overlay.

## Inventory Before Mutation

Run read-only discovery first. `chart_metadata.py`, `list_dependency_repositories.py`, `values_contract_lint.py`, `scan_template_values.py`, and `build_refactor_inventory.py` do not contact networks or clusters and do not edit the chart.

```bash
python3 scripts/chart_metadata.py --chart ./chart --format json
python3 scripts/list_dependency_repositories.py --chart ./chart --format json
python3 scripts/values_contract_lint.py --chart ./chart --format json
python3 scripts/scan_template_values.py --chart ./chart --format json
python3 scripts/build_refactor_inventory.py --chart ./chart --format json
```

| Discovery result | Required disposition |
|---|---|
| Application chart | Define lint/render scenarios and expected resources |
| Library chart | Identify consumer charts and exported helper tests |
| Static `.Values` path | Reconcile with values, comments, schema, overlay, and consumers |
| Dynamic `index`, `tpl`, `lookup`, file access, or capability branch | Record incomplete static coverage and add targeted render tests |
| Concrete secret-like default | Remove the secret and replace with a reference/injection contract |
| Undocumented or unconsumed value | Confirm compatibility intent before removing or repurposing it |
| Dependency alias/local/vendored form | Resolve provenance and availability in the target build environment |

## Values Precedence and Type Stability

Helm merges chart defaults, parent values, user values files, and command-line setters according to its documented precedence. The workflow records the exact ordered values inputs for every scenario. Prefer reviewed values files to shell setters; if setters are required, use typed forms deliberately and capture the effective input without exposing sensitive values.[3]

| Risk | Required control |
|---|---|
| Boolean/string ambiguity | Use unambiguous YAML and enforce the type in schema |
| Integer/string identifier drift | Quote lexical identifiers and constrain with a string schema |
| Deeply nested optional values | Prefer stable structures and test absent, empty, and populated cases |
| List replacement semantics | Test complete overrides; do not assume element-wise merge |
| `null` versus omission | Declare schema and template behavior explicitly |
| Multiple `-f` files | Record order and test expected winner for overlapping keys |
| `--set` parsing | Prefer typed setters or files; never expose secrets in process arguments |

## Contract and Schema

Every public value should have a Helm-style adjacent comment beginning with the property name. This package adds local tags such as `@type`, `@required`, `@accepted`, `@default`, `@example`, and `@security` for deterministic coverage. Those tags are a package convention, not a Helm feature.

Use `values.schema.json` for machine constraints. Require an explicit `$schema`, validate the schema itself, keep references local by default, and state that JSON Schema annotations do not create Helm defaults. Reconcile values, schema, template use, documentation, and compatibility dispositions as one contract.

| Contract source | Purpose | Conflict resolution |
|---|---|---|
| `values.yaml` | Canonical defaults and comments | Do not infer all legal runtime values from examples alone |
| `values.schema.json` | Accepted data model and constraints | Schema failure is authoritative for schema-enabled Helm operations |
| Templates | Actual consumption and defaults | Static analysis gaps require rendering, not assumptions |
| Operator overlay | Curated environment/scenario input | Must declare whether active or a commented skeleton |
| Existing releases/users | Backward-compatibility evidence | Require migration and rollback decisions |

## Dependencies and Registries

Classify every repository form instead of requiring HTTPS blindly. Helm supports HTTPS/HTTP indexes, `@name` or `alias:` repository aliases, `file://` dependencies, OCI repositories, blank repositories for vendored charts, and plugin-defined schemes.[4][5]

| Repository form | Default disposition |
|---|---|
| HTTPS index | Verify host trust, version constraint, lock, provenance, and TLS behavior |
| HTTP index | Fail; replace with HTTPS or a reviewed internal mirror |
| Alias | Incomplete until the exact repository configuration is supplied |
| `file://` | Confine path, review source contents, and test build portability |
| OCI | Verify registry trust, authentication isolation, immutable digest/provenance where supported |
| Blank/vendored | Verify matching package exists and digest/provenance is recorded |
| Plugin scheme | Treat as executable extension; separately review and authorize the plugin |
| Inline credentials | Fail and redact; move authentication to approved credential storage |

`helm dependency build` may contact repositories and write packaged dependencies. Without a lock file, its behavior can resolve versions like update. `helm dependency update` negotiates versions, downloads packages, removes some old dependencies, and writes a lock.[6][7] Run either only in an isolated chart copy after explicit network approval; record before/after inventory, lock changes, package digests, and Git diff.

## Isolated Lint and Render

The bundled `validate_chart.sh` creates a private evidence directory, copies the chart, uses isolated Helm config/cache/data paths, disables implicit cluster configuration, and defaults to no network and no cluster. It runs strict linting and render scenarios, then static manifest checks and strict kubeconform when exact schema inputs are supplied.

```bash
scripts/validate_chart.sh \
  --chart ./chart \
  --kube-version 1.36.0 \
  --schema-location /reviewed/schemas \
  --pod-security-profile restricted \
  --output-dir ./private-evidence
```

| Option | Effect | Gate |
|---|---|---|
| `--values LABEL=PATH` | Adds a named render scenario | Regular non-symlink file copied into evidence |
| `--kube-version VERSION` | Sets Helm capabilities and kubeconform target | Exact minor/patch recorded |
| `--schema-location PATH` | Supplies schema source | Local reviewed path by default |
| `--build-dependencies` | Builds in copied chart | Also requires `--allow-network` |
| `--server-dry-run` | Sends rendered objects to target API server | Also requires `--allow-cluster --context NAME` |
| `--skip-contract`, `--skip-schema`, `--skip-template` | Assessment-only exception | Forces incomplete result |

Do not add `--skip-schema-validation`, `-ignore-missing-schemas`, DNS lookup, post-renderers, plugins, remote values URLs, or arbitrary `--api-versions` silently. Each changes coverage or executes/contacts additional components and requires a documented decision.

## Library Charts

An empty resource stream is expected for a library chart but is not validation success by itself. Test exported helpers from representative consumer charts, including default, override, missing input, type error, and collision behavior. Record every consumer’s Helm and Kubernetes target.

| Library-chart evidence | Minimum requirement |
|---|---|
| Exported helper inventory | Name, inputs, outputs, and documented stability |
| Consumer fixtures | At least one realistic caller per supported integration shape |
| Values/schema contract | Caller inputs validated independently |
| Render assertions | Expected snippets/resources and failure cases |
| Compatibility | Helm majors and caller migration notes |

## Release Decision

A release-ready claim requires a clean declared worktree or acknowledged diff, complete contract analysis, strict lint, successful scenario renders, exact target-version schema coverage including CRDs, policy checks, dependency provenance, and authorized server evidence when required by the user’s acceptance criteria. Preserve `REPORT.md`, `results/steps.tsv`, tool versions, schema digests, and sanitized logs; do not commit rendered files that may contain resolved secrets.

[1]: https://helm.sh/docs/
[2]: https://helm.sh/docs/topics/charts/
[3]: https://helm.sh/docs/topics/chart_best_practices/values/
[4]: https://helm.sh/docs/topics/chart_best_practices/dependencies/
[5]: https://helm.sh/docs/topics/registries/
[6]: https://helm.sh/docs/helm/helm_dependency_build/
[7]: https://helm.sh/docs/helm/helm_dependency_update/
