# Helm Values Contract

## Contract Surfaces

Treat Helm values as a public API. The canonical contract spans defaults, adjacent documentation, JSON Schema, template consumers, operator overlays, downstream parent charts, release-time inputs, and compatibility commitments. No single surface is sufficient.

| Surface | Role | Typical defect |
|---|---|---|
| `values.yaml` | Canonical defaults and human documentation | Undocumented or ambiguous type/default |
| `values.schema.json` | Machine constraints | Missing path, wrong type, undeclared dialect, unsafe reference |
| Templates | Actual consumers and runtime defaults | Dynamic path, stale key, implicit fallback |
| Operator overlay | Curated deployment scenario | Partial/stale key set or unclear active/commented mode |
| Parent/subchart values | Cross-chart API | Import/export or prefix mismatch |
| CLI/release input | Highest-precedence runtime override | Type coercion or secret exposure |
| Compatibility policy | Rename/removal/default-change rules | Breaking change without migration |

## Adjacent Documentation Convention

Helm recommends documenting each defined value with a comment beginning with that property name.[1] This package adds deterministic tags for contract linting. These tags are a **local convention**, not Helm syntax.

```yaml
# -- service.type selects the Kubernetes Service type.
# @type string
# @required true
# @accepted ClusterIP | NodePort | LoadBalancer
# @default ClusterIP
# @example LoadBalancer
# @security Public exposure depends on provider and network policy.
service:
  type: ClusterIP
```

| Tag | Requirement |
|---|---|
| `# -- path ...` | Human summary beginning with the full logical path |
| `@type` | Stable JSON-compatible type, such as string, integer, boolean, object, or array |
| `@required` | Whether the key must exist in the canonical contract |
| `@accepted` | Enumerated, ranged, patterned, or prose constraint |
| `@default` | Human-readable semantic default, not an executable directive |
| `@example` | Non-secret representative input |
| `@security` | Required for secret-like, exposure, privilege, identity, or trust-sensitive values |

The linter checks completeness and consistency but does not treat comments as machine enforcement. Encode enforceable rules in `values.schema.json` and application tests.

## Path and Type Rules

Use lower camel case for Helm value names unless an established compatibility contract requires another form.[1] Prefer string keys, stable types, and structures that are easy to override. Do not change a value’s type between defaults and overlays.

| Pattern | Preferred treatment |
|---|---|
| Identifier resembling number/date | Quote and schema as string |
| Boolean | Canonical `true`/`false` and schema boolean |
| Optional scalar | Define absence/null/empty semantics explicitly |
| Open labels/annotations map | Document as an open map and constrain value types |
| List of objects | Define item schema and test whole-list replacement |
| Deep optional tree | Flatten when it improves override ergonomics without breaking compatibility |
| Secret material | Do not store concrete values; use reference metadata |

## Secret References

A reference name or key is metadata, not the secret value. The package exempts recognized reference paths such as `existingSecret.name`, `existingSecret.key`, and `secretKeyRef.key` from concrete-secret-value rules, while still treating `password`, `apiToken`, `clientSecret`, and similar material paths as sensitive.

```yaml
# -- existingSecret.name identifies a pre-created Secret.
# @type string
# @required false
# @accepted Kubernetes DNS-compatible name or empty
# @default empty
# @example app-credentials
# @security The referenced Secret must be provisioned separately.
existingSecret:
  name: ""
  key: token
```

| Safe evidence | Forbidden evidence |
|---|---|
| Secret object name after contextual review | Password/token/private-key value |
| Secret data key name | Decoded Secret payload |
| Required/optional relationship | Credential-bearing URL |
| External provider reference metadata | Live account identifier when sensitive |
| Rule result and path | Hash of a low-entropy secret presented as anonymization |

## JSON Schema Reconciliation

Require a declared supported `$schema`, validate the schema itself, enforce the JSON data model, and keep references local and repository-confined by default. The package pins a tested Draft 2020-12 implementation but does not auto-install it.[2][3]

| Reconciliation | Required outcome |
|---|---|
| Value exists, schema absent | Finding unless explicitly open under an ancestor schema |
| Schema property exists, value absent | Allowed only when optional and default/runtime behavior is documented |
| Type differs | Failure |
| Required differs from comment | Failure or explicit compatibility disposition |
| Enum/range differs from `@accepted` | Failure |
| Schema default differs from values default | Finding; schema annotation does not apply a Helm default |
| Remote `$ref` | Refuse by default; review and snapshot locally |
| Unknown dialect | Fail rather than silently select a validator |
| `format` keyword | Report whether assertions were enabled |

`additionalProperties: false` is appropriate for closed contract objects. For intentionally open metadata maps, declare `additionalProperties` with the intended value schema and document the path as open.

## Operator Overlay Modes

An operator template must declare whether it is an **active overlay** or a **commented skeleton**. An active overlay parses as YAML and participates in type/key reconciliation. A commented skeleton requires a separate conservative parser and is inherently incomplete when nested structures or anchors cannot be reconstructed safely.

| Mode | Contract |
|---|---|
| `# @mode active-overlay` | All active keys must exist in canonical values and preserve types |
| `# @mode commented-skeleton` | Commented paths are advisory; unresolved structure is reported incomplete |
| Missing/unknown mode | Failure until intent is explicit |

The portable example uses active-overlay mode. Do not silently turn commented documentation into active configuration or vice versa.

## Static Consumer Analysis

`scan_template_values.py` discovers common `.Values.path` and literal `index .Values "key"` forms. It reports dynamic expressions rather than guessing. Static discovery cannot prove behavior involving `tpl`, computed keys, file contents, helper indirection, subchart imports, plugins, `lookup`, or all capability branches.

| Static result | Disposition |
|---|---|
| Declared and consumed | Retain with scenario coverage |
| Declared but not statically consumed | Investigate compatibility, indirect use, and parent-chart API |
| Consumed but undeclared | Add contract/schema or fix stale template |
| Dynamic expression | Add targeted lint/render/integration scenarios |
| Open map ancestor | Permit dynamic descendants only under the documented open-map contract |

## Refactor Inventory

`build_refactor_inventory.py` combines canonical paths, types, comments, schema presence, overlay presence, static use, security classification, and an explicit disposition. It intentionally does not include scalar default values in its machine-readable output.

| Field | Meaning |
|---|---|
| `path` | Canonical logical values path |
| `type` | Parsed JSON-compatible type |
| `documented` | Required adjacent metadata present |
| `schema` | Path covered by schema or declared open ancestor |
| `template` | Present in operator overlay |
| `static_consumers` | Deterministically discovered template references |
| `security_sensitive` | Path requires secret/exposure review |
| `disposition` | Preserve/add/rename/migrate/deprecate/remove/internalize/investigate |

Default every unknown disposition to `investigate`. A lack of static consumers is not removal authority.

## Commands and Outcomes

```bash
python3 scripts/values_contract_lint.py --chart ./chart --format json
python3 scripts/scan_template_values.py --chart ./chart --format json
python3 scripts/build_refactor_inventory.py --chart ./chart --format json
```

| Exit | Meaning |
|---:|---|
| `0` | Complete for the declared static scope |
| `1` | Contract, schema, secret, or consistency failure |
| `2` | Incomplete coverage, missing optional evidence, or invalid assessment setup |

Skipping schema or overlay reconciliation is assessment-only and cannot produce a complete claim. For library charts, an absent operator overlay can be a documented coverage gap while the local contract remains complete; consumer-chart tests are still required for release confidence.

[1]: https://helm.sh/docs/topics/chart_best_practices/values/
[2]: https://json-schema.org/draft/2020-12/json-schema-core
[3]: https://python-jsonschema.readthedocs.io/en/latest/validate/
