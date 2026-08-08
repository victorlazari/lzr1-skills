# Safe YAML and Helm Refactoring

## Refactor Only After Discovery

A YAML refactor can preserve syntax while changing types, precedence, defaults, comments, anchors, template behavior, or API semantics. Begin with read-only inventory, define compatibility targets, and classify every canonical value or object before editing. Do not auto-format, rename, delete, or migrate fields based only on apparent cleanliness.

| Discovery artifact | Purpose |
|---|---|
| Git status and diff | Establish pre-existing user work and rollback boundary |
| Consumer inventory | Identify parsers, Helm charts, CI jobs, Kubernetes targets, and applications |
| `build_refactor_inventory.py` result | Reconcile values paths, documentation, schema, overlays, and static consumers |
| Dynamic-expression list | Mark paths that static analysis cannot prove |
| Compatibility matrix | Name supported Helm/Kubernetes/parser versions and scenarios |
| Sensitive-path inventory | Prevent secrets from entering diffs, logs, or examples |

## Canonical Dispositions

Every value path receives an explicit disposition before mutation. Unknown does not mean removable.

| Disposition | Meaning | Required evidence |
|---|---|---|
| Preserve | Stable public contract remains unchanged | Existing consumer or compatibility commitment |
| Add | New value/object with no collision | Schema, docs, default, consumer, and tests |
| Rename with compatibility bridge | Old and new names coexist temporarily | Precedence rule, deprecation notice, tests, removal version |
| Migrate | Representation changes with conversion | Before/after semantics, migration procedure, rollback |
| Deprecate | Supported but discouraged | Replacement, timeline, warning behavior |
| Remove | Contract intentionally deleted | Consumer search, release policy, migration and rollback |
| Internalize | Public setting becomes implementation detail | Proof that no external consumer depends on it |
| Investigate | Evidence is incomplete or contradictory | No mutation until resolved |

The bundled inventory defaults paths to `investigate`; it does not infer safe removal.

## Plan Atomic Change Sets

Split large work into independently reviewable changes. A useful sequence is contract normalization, schema alignment, template migration, manifest/API migration, formatting, and documentation. Avoid mixing semantic migrations with mass formatting because reviewers cannot reliably isolate behavior changes.

| Change-set property | Requirement |
|---|---|
| Scope | Named files and paths only |
| Invariant | Behavior that must remain stable |
| Intentional change | Exact semantic difference |
| Compatibility | Supported old/new clients and rollback window |
| Validation | Scenarios and target versions that prove the change |
| Stop condition | Failure or unexpected diff that pauses the loop |

## Editing Rules

Use a round-trip parser for comment- or style-sensitive files, but preview every diff because no emitter is perfectly semantics-neutral across consumers. Prefer targeted textual edits when the transformation is small and unambiguous. Never deserialize and rewrite an entire repository merely to change one key.

| Risk | Control |
|---|---|
| Comment loss or movement | Round-trip parser plus human diff review |
| Quote/type drift | Compare parsed types before and after under every relevant parser |
| Key-order churn | Preserve order unless the user requested canonicalization |
| Anchor/alias expansion | Refuse or test exact consumer semantics |
| Duplicate-key normalization | Stop and resolve intent; do not choose a winner automatically |
| Line-ending/encoding change | Preserve or declare normalization separately |
| Secret exposure | Redact values; never include them in generated examples or reports |
| Symlink/path escape | Resolve within repository root and reject symlink inputs by default |

## Helm Values Migration

A Helm values change touches at least four planes: default values, documentation, schema, and templates. Operator overlays and downstream consumers add more. Reconcile them in one inventory and test ordered precedence.

| Migration type | Safe pattern |
|---|---|
| Rename | Read new key first, support old key for a declared period, fail on conflicting simultaneous values if ambiguity matters |
| Type change | Introduce a new key or explicit conversion; schema both transition states only when runtime code supports both |
| Nesting change | Preserve old path with translation or publish a major-version migration |
| Default change | Treat as behavioral change; test omitted versus explicit old value |
| List/map change | Document replacement/merge semantics and test complete overrides |
| Secret value removal | Replace with Secret/provider reference; never migrate the concrete value through logs |

`build_refactor_inventory.py` and `values_contract_lint.py` provide evidence, not automated migration authority. Dynamic templates, `tpl`, `lookup`, custom functions, subcharts, and external files require dedicated tests.

## Kubernetes API Migration

Consult the official deprecation guide for every target version and inspect semantic changes, not only the replacement `apiVersion`.[1]

| Migration checkpoint | Required action |
|---|---|
| Served API | Verify against each target minor |
| Field transformation | Compare schema, defaults, and validation |
| Selectors and references | Prove cross-object relationships remain valid |
| CRD storage version | Plan stored-object migration and rollback |
| Admission/policy | Run authorized target-server dry-run where required |
| Controller behavior | Add integration/runtime verification outside this local skill |

## Bounded Remediation Loop

Use at most three automated edit-and-validate passes for one approved scope. After each pass, compare finding identities, counts, rendered object sets, and Git diff. Stop sooner when no measurable progress occurs, scope expands, a new high-severity issue appears, secrets surface, dependency/network/cluster access becomes necessary, or user work changes concurrently.

| Pass | Required record |
|---|---|
| 0 | Baseline inventory, tests, diff, and known gaps |
| 1 | Minimal approved correction and full relevant validation |
| 2 | Only remaining confirmed root causes; no opportunistic cleanup |
| 3 | Final bounded attempt, then escalate unresolved findings |

Never auto-commit, push, publish, install, upgrade, apply, or delete as part of a refactor loop. Those are separate operations with explicit authorization.

## Validation Order

Run cheap deterministic checks before expensive or authorized checks. Failures do not erase later coverage needs.

| Order | Stage |
|---:|---|
| 1 | Path, size, encoding, duplicate-key, and YAML-profile checks |
| 2 | Values comments, types, schema, and static consumer reconciliation |
| 3 | Repository style and application-specific schema checks |
| 4 | Helm strict lint and declared scenario rendering |
| 5 | Cross-object, security, and exact-version Kubernetes schema checks |
| 6 | Explicitly authorized server dry-run |
| 7 | Separate runtime/deployment tests when required |

## Completion and Rollback

A refactor is complete only when the declared matrix is complete, intentional compatibility changes are documented, unexpected diffs are absent, evidence is private and reviewable, and rollback has been tested or is mechanically clear. Preserve the pre-change commit/diff, migration notes, tool versions, and result report.

| Stop or rollback trigger | Response |
|---|---|
| Unexpected rendered object or type change | Revert the atomic change and diagnose |
| Consumer fails under a supported version | Restore compatibility or revise scope with approval |
| Secret appears in diff/evidence | Stop, protect evidence, rotate if exposure is possible, and remediate handling |
| Target schema or API unavailable | Mark incomplete; do not claim success |
| Concurrent user edits overlap | Stop and re-baseline rather than overwrite |
| Dependency/cluster operation becomes necessary | Request separate authorization with exact command and target |

[1]: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
