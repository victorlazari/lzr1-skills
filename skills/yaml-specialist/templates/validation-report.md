# YAML and Helm Validation Report

## Decision Summary

**Status:** `complete | failed | incomplete`
**Repository and revision:** `TODO`
**Chart or YAML scope:** `TODO`
**Reviewer:** `TODO`
**Evidence timestamp (UTC):** `TODO`
**Mutation authorization:** `none | approved change set reference`
**Network authorization:** `none | approved hosts and purpose`
**Cluster authorization:** `none | exact context and dry-run purpose`

> A **complete** result requires every declared target and scenario to pass. A tool error, skipped gate, missing schema, unsupported custom resource, unresolved dynamic expression, or untested compatibility target is not a clean result.

## Compatibility Contract

| Dimension | Declared target | Evidence | Result |
|---|---|---|---|
| YAML language and schema | YAML 1.2.2 / Core Schema or documented parser profile | `TODO` | `TODO` |
| Helm | `TODO exact version or supported range` | `TODO` | `TODO` |
| Kubernetes | `TODO explicit minor versions` | `TODO` | `TODO` |
| JSON Schema | Draft 2020-12 or chart-specific dialect | `TODO` | `TODO` |
| Custom resources | `TODO CRD versions and schema source` | `TODO` | `TODO` |
| Pod Security | `none | baseline | restricted` | `TODO` | `TODO` |

## Toolchain

| Tool | Exact version | Configuration or schema source | Trust note |
|---|---|---|---|
| Python | `TODO` | `TODO` | `TODO` |
| ruamel.yaml | `TODO` | YAML 1.2 safe round-trip profile | `TODO` |
| jsonschema | `TODO` | Draft selected by `$schema` | `TODO` |
| Helm | `TODO` | isolated state directories | `TODO` |
| kubeconform | `TODO` | explicit schema locations; no ignored missing schemas | `TODO` |
| kubectl | `TODO or not used` | exact context; server dry-run only | `TODO` |

## Scenario Matrix

| Scenario | Values inputs and precedence | Contract | Helm lint | Render | Reference lint | API schema | Server dry-run | Result |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Canonical defaults | `values.yaml` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |
| Operator template | `values.yaml`, `values-template.yaml` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |
| Compatibility fixture | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## Contract and Refactor Findings

| Stable finding ID | Severity | File and path | Evidence | Disposition | Verification |
|---|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `fix | accept with rationale | defer with owner` | `TODO` |

## Compatibility Disposition Register

| Current path or API | Target path or API | Disposition | Compatibility window | Migration evidence | Rollback trigger |
|---|---|---|---|---|---|
| `TODO` | `TODO` | `retain | rename | deprecate | remove | externalize` | `TODO` | `TODO` | `TODO` |

## Security and Secret-Handling Evidence

| Check | Evidence | Result |
|---|---|---|
| No concrete secret values in tracked YAML | `TODO` | `TODO` |
| Existing Secret references are documented and independently provisioned | `TODO` | `TODO` |
| Rendered evidence permissions are owner-only | `TODO` | `TODO` |
| Pod Security profile checked at declared version | `TODO` | `TODO` |
| Dependency transports, versions, lock file, and provenance reviewed | `TODO` | `TODO` |

## Coverage Gaps

| Gap | Why unresolved | Risk | Required next evidence | Owner |
|---|---|---|---|---|
| `TODO` | `TODO` | `TODO` | `TODO` | `TODO` |

## Approvals and Publication Boundary

No command in this report authorizes a Helm install or upgrade, `kubectl apply`, repository push, pull-request publication, configuration mutation, dependency download, or cluster access. Record any separately approved action here:

| Action | Exact scope | Approver | Timestamp | Result |
|---|---|---|---|---|
| `TODO or none` | `TODO` | `TODO` | `TODO` | `TODO` |

## Final Decision

**Decision:** `accept | reject | incomplete`
**Rationale:** `TODO`
**Rollback plan:** `TODO`
**Revalidation trigger:** `tool, schema, Helm, Kubernetes, CRD, or contract change`
