# Kubernetes Manifest Validation

## Target Exact Supported Versions

Kubernetes compatibility is a matrix, not a boolean. The project maintains the three most recent minor release branches; on 2026-08-07 these were 1.36, 1.35, and 1.34. Refresh the official release page before publishing a new claim because supported minors and patch levels change frequently.[1]

| Evidence | Required value |
|---|---|
| Kubernetes target | Exact minor or patch, not “current” |
| Helm target | Exact `--kube-version` used for capabilities |
| Offline schema | Exact Kubernetes version and source digest/commit |
| kubectl client | Exact client version and applicable version-skew result |
| API server | Exact server version and context when authorized |
| CRDs | Exact installed or reviewed schema versions |
| Pod Security profile | Profile plus Kubernetes version used for controls |

The kubectl client can generally be one minor older or newer than the API server, with narrower practical bounds in mixed-version high-availability control planes.[2] Do not infer server acceptance from a client-only parse.

## API Deprecation and Removal

For every target minor, inventory each `apiVersion` and kind, check the official deprecation guide, and review semantic migrations. Changing only `apiVersion` can be unsafe when selectors, defaults, validation, field meanings, or controllers changed.[3]

| Migration question | Required evidence |
|---|---|
| Is the API served in every target? | Target-specific discovery or authoritative migration documentation |
| Is the replacement structurally equivalent? | Field-level comparison and rendered diff |
| Did defaulting change? | Server dry-run or version-specific documentation |
| Did selector behavior change? | Scenario test using the intended workload relationships |
| Is conversion handled by a CRD webhook? | Reviewed CRD conversion strategy and target-cluster evidence |
| Does rollback need an older API? | Stored-version and downgrade plan before migration |

## Offline Schema Validation

Use kubeconform in strict mode with an explicit Kubernetes version and reviewed schema locations. Record the binary version, schema source, local snapshot digest or pinned commit, concurrency, summary counts, and every skipped or missing resource. Never use ignored missing schemas as a clean result.[4]

```bash
kubeconform \
  -strict \
  -summary \
  -output json \
  -kubernetes-version 1.36.0 \
  -schema-location /reviewed/schema-snapshot \
  rendered.yaml
```

| Result | Interpretation |
|---|---|
| Valid built-in resource | Passed the supplied converted schema only |
| Invalid resource | Failed for the recorded target/schema |
| Missing schema | Incomplete coverage; supply the schema or document the gap |
| CRD instance without exact CRD schema | Incomplete, never a clean skip |
| Duplicate key or unknown field in strict mode | Failure requiring source correction |
| Third-party catalog match | Supplemental evidence; record provenance and limitations |

Offline schemas do not reproduce API-server defaulting, admission webhooks, CEL policies, aggregated APIs, custom conversion, controller reconciliation, or cluster state.

## Custom Resources and CRDs

`apiextensions.k8s.io/v1` CRDs require structural OpenAPI v3 schemas. Validate the CRD object itself, derive or supply the exact instance schema, and test each served/storage version. Generic built-in schemas are insufficient for custom resources.[5]

| CRD control | Required check |
|---|---|
| Structural schema | All served versions use valid structural schemas |
| Required/defaulted fields | Defaults and required constraints do not conflict |
| Unknown-field behavior | Pruning/preservation is explicit and tested |
| Subresources | Status and scale schemas/paths are valid |
| Conversion | Strategy and webhook availability are tested where applicable |
| Version lifecycle | Served/storage flags, stored versions, and migration plan agree |
| Instance schemas | Kubeconform or equivalent receives the exact versioned schema |

## Cross-Object References

The bundled `rendered_manifest_lint.py` performs deterministic local checks for common namespace-scoped references, ConfigMap/Secret keys, workload ServiceAccounts, Services, Ingress backends, duplicates, and selected Pod Security controls. It never reads Secret values and distinguishes explicit external dependencies from missing local objects.

| Reference | Local validation rule |
|---|---|
| `serviceAccountName` | A matching ServiceAccount exists in the effective namespace or is explicitly external |
| ConfigMap/Secret volume or env reference | Object and required key exist locally, or external reference is allowlisted |
| Ingress backend Service | Service and named/numbered port are consistent |
| Namespace | Namespaced identity includes explicit/default namespace |
| Cluster-scoped object | Identity omits namespace and duplicates remain global |
| External operator-managed object | Allowlist exact `Kind/name` or `Kind/namespace/name`; do not wildcard silently |

An allowlisted external reference means “intentionally outside this bundle,” not “proved to exist.” Verify it separately in the deployment environment.

## Pod Security

Pod Security Standards define cumulative Privileged, Baseline, and Restricted profiles. Controls evolve by Kubernetes version; the package’s static linter implements a documented subset and cannot replace admission policy.[6]

| Restricted-oriented check | Expected posture |
|---|---|
| Privileged containers | `privileged` absent or false |
| Privilege escalation | `allowPrivilegeEscalation: false` |
| User identity | Pod or container explicitly runs as non-root |
| Capabilities | Drop `ALL`; add only version-permitted capabilities |
| Seccomp | Pod or container uses `RuntimeDefault` or `Localhost` as allowed |
| Host namespaces | Host PID, IPC, and network disabled |
| Host paths and volume types | Only profile-permitted types |
| Probe/lifecycle host usage | Apply versioned host restrictions for current targets |

Always record the profile and target version. If the target uses Kyverno, Gatekeeper, ValidatingAdmissionPolicy, custom webhooks, or cloud-provider controls, add those as separate policy layers.

## Secret and Sensitive Evidence

Kubernetes Secrets are base64-encoded, not encrypted by that encoding. Avoid placing real credentials in examples, Git, command arguments, rendered logs, or validation reports.[7]

| Artifact | Handling rule |
|---|---|
| `Secret.data` or `stringData` | Validate key names and structure; never decode or echo values |
| Helm values containing secret material | Fail contract review; use an external reference or approved injection path |
| Rendered manifest | Treat as sensitive even when source values appear benign |
| Tool stderr/stdout | Store privately; sanitize before publication |
| External Secret references | Record provider/object metadata without credentials |
| Evidence directory | Owner-only permissions and explicit retention policy |

## Server-Side Dry-Run

`kubectl apply --dry-run=server` sends objects through API-server processing without persistence and can exercise defaulting and eligible admission components.[8][9] It contacts a real cluster, may expose manifest content to webhooks, and therefore requires explicit authorization and an exact context.

```bash
scripts/validate_chart.sh \
  --chart ./chart \
  --kube-version 1.36.0 \
  --schema-location /reviewed/schemas \
  --server-dry-run \
  --allow-cluster \
  --context exact-context-name \
  --output-dir ./private-evidence
```

| Precondition | Stop condition |
|---|---|
| User approved target cluster contact | Context differs from the approved name |
| Rendered evidence reviewed for secrets | Sensitive content lacks approved handling |
| Client/server skew supported | Version discovery fails or falls outside policy |
| No mutating command requested | Command is not exact server dry-run |
| Admission side effects understood | Webhook behavior is unknown or unsafe |

A successful server dry-run still does not prove controller reconciliation, scheduling, external service readiness, rollout health, or production correctness. State this boundary in the final report.

[1]: https://kubernetes.io/releases/
[2]: https://kubernetes.io/releases/version-skew-policy/
[3]: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
[4]: https://github.com/yannh/kubeconform
[5]: https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/
[6]: https://kubernetes.io/docs/concepts/security/pod-security-standards/
[7]: https://kubernetes.io/docs/concepts/configuration/secret/
[8]: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/
[9]: https://kubernetes.io/blog/2019/01/14/apiserver-dry-run-and-kubectl-diff/
