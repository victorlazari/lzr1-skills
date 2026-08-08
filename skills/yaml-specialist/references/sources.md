# Authoritative Sources and Freshness Policy

**Last verified:** 2026-08-07. This ledger is the evidence baseline for `yaml-specialist`; it is not an instruction to execute upstream scripts or install unreviewed binaries. Recheck every volatile source before publishing a new compatibility claim.

## Authority Model

The skill treats a language specification or project-owned documentation as primary authority for that project. A validator implementation proves only its own behavior at a recorded version. Community schema catalogs, generated OpenAPI conversions, blog posts, and package-index metadata can support discovery, but they do not override normative specifications or target-cluster behavior.

| Tier | Evidence | Permitted claim |
|---|---|---|
| 1 | Normative specification or official project policy | Language, dialect, compatibility, or support-policy semantics |
| 2 | First-party command and format documentation | Exact supported flags, file layouts, and tool behavior for a recorded release |
| 3 | Canonical implementation repository or signed/released package metadata | Implementation version, release date, and observed feature availability |
| 4 | Third-party schema catalog, conversion, article, or generated artifact | Supplemental evidence only, with provenance and limitations stated |

## YAML Language

YAML 1.2.2 is the current published YAML 1.2 specification revision. The YAML Test Suite is the language-independent conformance corpus, but its maintainers recommend using a dated release rather than a mutable development branch.[1][2]

| Source | Authority | Volatility | Refresh trigger |
|---|---|---|---|
| [YAML 1.2.2 specification][1] | Tier 1 | Low | New specification revision |
| [YAML project release index][3] | Tier 1 | Medium | Before claiming the current revision |
| [YAML specification repository][4] | Tier 1 | Medium | Specification errata or release |
| [YAML Test Suite][2] | Tier 3 | Medium | Parser upgrade or conformance claim |

## JSON Schema

Draft 2020-12 is the current published JSON Schema version. Core defines dialect and processing; Validation defines assertion vocabularies. The official test suite is the cross-implementation behavior corpus.[5][6][7][8]

| Source | Authority | Volatility | Refresh trigger |
|---|---|---|---|
| [JSON Schema specification index][5] | Tier 1 | Medium | New published draft |
| [Draft 2020-12 Core][6] | Tier 1 | Low | Erratum or replacement draft |
| [Draft 2020-12 Validation][7] | Tier 1 | Low | Erratum or replacement draft |
| [JSON Schema Test Suite][8] | Tier 3 | Medium | Validator or dialect change |

## Helm

The current first-party documentation serves Helm 4.2.3. Some topic pages identify themselves as not fully updated for Helm 4, so versioned command references control exact flag claims and every report records the actual binary version.[9]

| Source | Authority | Volatility | Refresh trigger |
|---|---|---|---|
| [Helm documentation home][9] | Tier 2 | High | Every release claim |
| [Chart format and structure][10] | Tier 2 | Medium | Helm major release or chart-format change |
| [Values best practices][11] | Tier 2 | Medium | Helm documentation revision |
| [`helm lint` reference][12] | Tier 2 | High | Helm binary upgrade |
| [`helm template` reference][13] | Tier 2 | High | Helm binary upgrade |
| [Dependency best practices][14] | Tier 2 | Medium | Repository-form change |
| [OCI registries][15] | Tier 2 | Medium | Registry or provenance behavior change |
| [`helm dependency build`][16] | Tier 2 | High | Helm binary upgrade |
| [`helm dependency update`][17] | Tier 2 | High | Helm binary upgrade |

## Kubernetes

Kubernetes maintains the three most recent minor release branches. On 2026-08-07 those branches were 1.36, 1.35, and 1.34; this matrix is volatile and must be refreshed from the release page before publication.[18]

| Source | Authority | Volatility | Refresh trigger |
|---|---|---|---|
| [Supported Kubernetes releases][18] | Tier 1 | Very high | Before every compatibility claim |
| [Version-skew policy][19] | Tier 1 | Medium | Client or cluster-version change |
| [Deprecated API migration guide][20] | Tier 1 | High | Target minor-version change |
| [Pod Security Standards][21] | Tier 1 | High | Target minor-version or profile change |
| [`kubectl apply` reference][22] | Tier 2 | High | kubectl upgrade |
| [API-server dry-run model][23] | Tier 1 | Medium | Server-validation workflow change |
| [CustomResourceDefinitions][24] | Tier 1 | High | CRD API or schema change |
| [Kubernetes Secrets][25] | Tier 1 | Medium | Secret-storage or policy change |

## Validation Implementations

These sources describe tools used by the package. A clean result from one tool is not a universal correctness proof; every report names versions, configurations, target schemas, and skipped coverage.[26][27][28][29]

| Source | Recorded version | Authority | Refresh trigger |
|---|---:|---|---|
| [yamllint documentation][26] | 1.38.0 | Tier 2 | Tool upgrade |
| [kubeconform repository][27] and [v0.8.0 release][28] | 0.8.0 | Tier 2/3 | Tool or schema-source change |
| [ruamel.yaml package metadata][29] and [API guide][30] | 0.19.1 | Tier 2/3 | Dependency upgrade |
| [PyYAML package metadata][31] and [loader warning][32] | 6.0.3 | Tier 2/3 | Dependency upgrade or parser comparison |
| [Python jsonschema metadata][33], [release][34], and [validator guide][35] | 4.26.0 | Tier 2/3 | Dependency or dialect change |

## Refresh Procedure

A refresh records the UTC date, the resolved upstream version, the exact page or release URL, and semantic changes affecting commands, schema dialects, supported Kubernetes minors, Pod Security controls, dependency behavior, or parser safety. Do not silently rewrite a compatibility matrix from search snippets. Read the primary pages, update tests and fixtures, run the full package self-check, and retain the prior evidence in version control.

| Change observed | Required package action |
|---|---|
| New YAML or JSON Schema revision | Reassess parser profile, examples, schema validation, and conformance language |
| New Helm major/minor | Recheck every flag, chart behavior, isolation variable, and fixture render |
| New Kubernetes minor | Refresh supported-version matrix, removed APIs, Pod Security rules, and schemas |
| New kubeconform release or schema source | Recheck strict/missing-schema semantics and source provenance |
| Parser or jsonschema upgrade | Re-run duplicate-key, depth, custom-tag, reference, format, and dialect tests |
| Security advisory | Reassess dependency pin, loader mode, input limits, and evidence exposure immediately |

[1]: https://yaml.org/spec/1.2.2/
[2]: https://github.com/yaml/yaml-test-suite
[3]: https://yaml.org/
[4]: https://github.com/yaml/yaml-spec
[5]: https://json-schema.org/specification
[6]: https://json-schema.org/draft/2020-12/json-schema-core
[7]: https://json-schema.org/draft/2020-12/json-schema-validation
[8]: https://github.com/json-schema-org/JSON-Schema-Test-Suite
[9]: https://helm.sh/docs/
[10]: https://helm.sh/docs/topics/charts/
[11]: https://helm.sh/docs/topics/chart_best_practices/values/
[12]: https://helm.sh/docs/helm/helm_lint/
[13]: https://helm.sh/docs/helm/helm_template/
[14]: https://helm.sh/docs/topics/chart_best_practices/dependencies/
[15]: https://helm.sh/docs/topics/registries/
[16]: https://helm.sh/docs/helm/helm_dependency_build/
[17]: https://helm.sh/docs/helm/helm_dependency_update/
[18]: https://kubernetes.io/releases/
[19]: https://kubernetes.io/releases/version-skew-policy/
[20]: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
[21]: https://kubernetes.io/docs/concepts/security/pod-security-standards/
[22]: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/
[23]: https://kubernetes.io/blog/2019/01/14/apiserver-dry-run-and-kubectl-diff/
[24]: https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/
[25]: https://kubernetes.io/docs/concepts/configuration/secret/
[26]: https://yamllint.readthedocs.io/en/stable/
[27]: https://github.com/yannh/kubeconform
[28]: https://github.com/yannh/kubeconform/releases/tag/v0.8.0
[29]: https://pypi.org/project/ruamel.yaml/
[30]: https://yaml.dev/doc/ruamel.yaml/api/
[31]: https://pypi.org/project/PyYAML/
[32]: https://pyyaml.org/wiki/PyYAMLDocumentation
[33]: https://pypi.org/project/jsonschema/
[34]: https://github.com/python-jsonschema/jsonschema/releases/tag/v4.26.0
[35]: https://python-jsonschema.readthedocs.io/en/latest/validate/
