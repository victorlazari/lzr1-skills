# Troubleshooting

Diagnose one layer at a time. Preserve the first failing command, exact exit, tool version, sanitized stderr, target version, and input digest before changing anything. Do not suppress a failure by skipping the layer or changing the compatibility target silently.

## Package and Python Dependencies

| Symptom | Likely cause | Safe response |
|---|---|---|
| `ModuleNotFoundError: ruamel` | Reviewed dependencies are absent from the current environment | Create an isolated environment, inspect `scripts/requirements.txt`, install exact pins, rerun tests; never auto-install from the skill |
| `ModuleNotFoundError: jsonschema` | Schema validator absent | Install exact reviewed pin in isolation or mark schema coverage incomplete |
| Dependency version differs | Environment drift | Record version, do not claim tested behavior, run package tests before use |
| Bytecode/cache appears in package | Tests ran without bytecode suppression | Remove `__pycache__`/`.pyc`, rerun with `PYTHONDONTWRITEBYTECODE=1` |
| Parser crashes or hangs | Resource limit, malformed input, parser defect | Stop, preserve a minimal sanitized reproducer, reduce bounds only after review |

## YAML Parse and Construction

| Symptom | Likely cause | Safe response |
|---|---|---|
| Duplicate-key error | Ambiguous mapping or policy shadowing | Resolve author intent; never choose first/last value automatically |
| Unsupported custom tag | Consumer-specific type | Identify exact consumer and safe constructor; keep rejected by default |
| YAML 1.1/1.2 warning | Ambiguous implicit scalar | Quote strings or use canonical booleans/nulls; test actual consumer |
| Non-string mapping key | YAML-only data model | Convert under explicit contract or exclude JSON/Helm/Kubernetes compatibility |
| Depth/node/alias/size limit | Adversarial or unusually complex input | Review source and raise only the narrow documented bound |
| Multiple documents where one expected | Wrong file shape | Split file or use the correct multi-document validator |

## Values Contract

| Symptom | Likely cause | Safe response |
|---|---|---|
| Missing comment metadata | Public value lacks local contract tags | Add adjacent full-path documentation and reconcile schema/template behavior |
| Comment type differs from value | Stale docs or unintended type change | Establish intended contract; update all surfaces and tests together |
| Schema path missing | Contract/schema drift | Add schema constraint or document a deliberate open-map ancestor |
| Overlay mode missing | Active versus commented intent unknown | Add the exact mode marker; do not infer from partial parsing |
| Concrete secret finding | Secret-like path contains material | Remove value, protect evidence, use reference/injection, rotate if exposure is possible |
| Declared but unconsumed | Indirect consumer or stale setting | Search parent charts, helpers, `tpl`, release automation, and compatibility policy before removal |
| Dynamic consumer | Computed template access | Add targeted render scenarios; retain incomplete static-coverage note |

## Helm Lint and Render

| Symptom | Likely cause | Safe response |
|---|---|---|
| Helm command unavailable | Tool not installed or PATH mismatch | Install only from reviewed source outside the skill; record exact version |
| `helm lint --strict` warning failure | Chart convention or target-capability problem | Fix or document repository-approved exception; do not remove strict mode silently |
| Dependency not found | Lock/package/repository mismatch | Inventory `Chart.lock`, `charts/`, and repository form; request network approval before build |
| Render output empty | Library chart, disabled feature, or broken chart | Confirm chart type and scenario expectations; application-chart emptiness fails |
| Render differs by Helm version | Major/minor semantic drift | Add explicit support matrix and version-specific expected outputs |
| `lookup` or cluster-dependent template | Local rendering cannot prove behavior | Refactor if possible or run separately authorized target-cluster tests |
| Plugin/post-renderer requested | Executable extension | Review code/provenance and obtain explicit execution authorization |

## Kubeconform and Schemas

| Symptom | Likely cause | Safe response |
|---|---|---|
| kubeconform unavailable | Binary absent | Mark schema stage incomplete; never substitute an unrecorded online service |
| Missing schema | Wrong target, CRD, or incomplete snapshot | Supply exact schema and provenance; do not use ignored missing schemas as success |
| Unknown field in strict mode | API mismatch or typo | Compare exact target-version schema and deprecation guide |
| Valid resource rejected | Schema conversion/catalog mismatch | Confirm target and source; compare with authorized API-server dry-run |
| Invalid resource accepted by server | Schema snapshot/tool divergence or server extension | Preserve both results; target server controls acceptance, but investigate policy/portability |
| Remote schema blocked | Network-free default | Snapshot and review locally, record digest; use network only with explicit approval |
| CRD instance incomplete | Exact CRD schema absent | Obtain the served version’s structural schema and validate separately |

## Rendered Reference and Security Checks

| Symptom | Likely cause | Safe response |
|---|---|---|
| Dangling ConfigMap/Secret/ServiceAccount | Object omitted, wrong namespace, or external dependency | Add object, correct reference, or exact allowlist plus deployment evidence |
| ConfigMap/Secret key missing | Key mismatch | Correct source/reference; never print Secret values |
| Ingress backend missing | Service or port mismatch | Reconcile effective namespace and named/numbered ports |
| Duplicate object identity | Multiple templates/scenarios emit same kind/name/namespace | Fix generation or explicitly separate scenarios |
| Pod Security finding | Workload violates selected profile subset | Update security context or document target policy and approved exception |
| Static linter passes, admission rejects | Cluster-specific policy/defaulting | Treat server result as separate authoritative target evidence |

## Validation Orchestrator

| Symptom | Likely cause | Safe response |
|---|---|---|
| Exit `2` | Missing schema/tool/target, library consumer gap, skipped stage, or invalid invocation | Read `results/steps.tsv` and logs; complete missing evidence rather than reclassifying |
| Exit `1` | One or more stages failed | Fix first failed layer; retain all incomplete counts |
| Output directory rejected | Existing content or symlink | Choose a new empty non-symlink private directory |
| Chart rejected for symlink | Input could escape copied scope | Replace with reviewed regular files; do not follow links silently |
| Dependency build gate fails | Network acknowledgement absent | Preview repository/diff effects and obtain explicit `--allow-network` approval |
| Server-dry-run gate fails | Cluster acknowledgement/context absent | Confirm exact target and use both `--allow-cluster` and `--context` only after approval |
| Plain HTTP schema location rejected | Insecure transport | Use a reviewed local snapshot or HTTPS with explicit network authorization |

The report’s final status follows `failed` over `incomplete` over `complete`. Check per-stage records rather than relying only on the final line.

## API-Server Dry-Run

| Symptom | Likely cause | Safe response |
|---|---|---|
| Context mismatch | Wrong kubeconfig or operator assumption | Stop; never choose another context automatically |
| Authentication prompt/failure | Missing or expired credentials | Ask the user to handle authentication through approved means; do not solicit secrets in logs |
| Version-skew issue | Client outside supported range | Use a compatible reviewed kubectl version |
| Webhook timeout | Admission dependency unavailable | Preserve target evidence and retry only under user-approved operational policy |
| Rejected unknown field | Server strict validation/defaulting mismatch | Correct manifest for target API; do not change validation to ignore |
| Dry-run would expose secrets | Manifest contains sensitive material | Stop and obtain explicit handling approval or sanitize the test input |

## Conflicting Results

| Conflict | Resolution |
|---|---|
| yamllint clean, parser fails | Parser/declared YAML profile controls syntax and construction |
| Parser clean, schema fails | Schema controls declared application data model |
| Schema clean, Helm fails | Helm chart/template semantics remain unsatisfied |
| Helm clean, kubeconform fails | Rendered object does not match supplied Kubernetes/CRD schema |
| Kubeconform clean, server fails | Target server/admission evidence controls target acceptance |
| Server dry-run clean, runtime fails | Controller/external/runtime behavior lies beyond validation scope |

## Escalation Record

When unresolved, provide a minimal sanitized reproducer, tool and dependency versions, exact target matrix, command with secrets removed, exit status, first failing diagnostic, relevant schema digest, what was tried, and why the remaining outcome is failed or incomplete. Do not attach raw rendered manifests until they are reviewed for sensitive values.
