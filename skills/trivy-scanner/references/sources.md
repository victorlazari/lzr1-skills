# Trivy Authoritative Source Map

**Verified against upstream:** 2026-08-07

Use this map to verify volatile behavior before changing commands, templates, pins, policies, or incident conclusions. Prefer the current official page over copied examples. When a page moves, start from the [Trivy documentation root](https://trivy.dev/docs/latest/) or the [upstream repository](https://github.com/aquasecurity/trivy).

| Area | Primary source | What it governs | Recheck when |
|---|---|---|---|
| Releases | [Trivy releases](https://github.com/aquasecurity/trivy/releases) | Current release, assets, checksums, signatures, provenance | Installing/upgrading or approving an artifact |
| Installation | [Installation](https://trivy.dev/docs/latest/getting-started/installation/) | Supported acquisition channels | Selecting a distribution method |
| Signature verification | [Signature verification](https://trivy.dev/docs/latest/getting-started/signature-verification/) | Official artifact-verification procedure | Before executing a new binary/image |
| Targets overview | [Targets](https://trivy.dev/docs/latest/target/) | Target taxonomy | Planning any scan |
| Container images | [Container image](https://trivy.dev/docs/latest/target/container_image/) | Image sources, platform, digest/input behavior | Scanning images or registries |
| Filesystem | [Filesystem](https://trivy.dev/docs/latest/target/filesystem/) | Local filesystem coverage | Scanning local projects/artifacts |
| Root filesystem | [Rootfs](https://trivy.dev/docs/latest/target/rootfs/) | Unpacked rootfs semantics | Scanning hosts or unpacked images |
| Repository | [Code repository](https://trivy.dev/docs/latest/target/repository/) | Remote/local repository behavior | Scanning a repository URL/ref |
| VM | [VM image](https://trivy.dev/docs/latest/target/vm/) | VM-image support and limits | Scanning disk/VM images |
| Kubernetes | [Kubernetes](https://trivy.dev/docs/latest/target/kubernetes/) | Cluster/resource/image behavior | Accessing a cluster |
| SBOM target | [SBOM](https://trivy.dev/docs/latest/target/sbom/) | SBOM ingestion and limitations | Scanning an existing SBOM |
| Scanners overview | [Scanners](https://trivy.dev/docs/latest/scanner/) | Scanner taxonomy and defaults | Choosing scanners |
| Vulnerabilities | [Vulnerability scanner](https://trivy.dev/docs/latest/scanner/vulnerability/) | Package detection, status, severity, VEX interactions | Interpreting vulnerability results |
| Misconfiguration | [Misconfiguration scanner](https://trivy.dev/docs/latest/scanner/misconfiguration/) | IaC/configuration coverage and policy | Scanning IaC or custom checks |
| Custom checks | [Custom checks](https://trivy.dev/docs/latest/scanner/misconfiguration/custom/) | Rego/data/schema/test workflow | Adding policy code |
| Secrets | [Secret scanner](https://trivy.dev/docs/latest/scanner/secret/) | Rules, allow rules, performance, output sensitivity | Customizing secret detection |
| Licenses | [License scanner](https://trivy.dev/docs/latest/scanner/license/) | License detection modes and categories | Producing license evidence |
| Coverage | [Coverage](https://trivy.dev/docs/latest/coverage/) | Supported OS, languages, IaC, and other ecosystems | Stating scan completeness |
| Configuration | [Configuration overview](https://trivy.dev/docs/latest/configuration/) | Precedence and configuration areas | Combining flags/env/YAML |
| Config schema | [Configuration-file reference](https://trivy.dev/docs/latest/references/configuration/config-file/) | Current YAML hierarchy and defaults | Editing `trivy.yaml` |
| CLI reference | [CLI commands](https://trivy.dev/docs/latest/references/configuration/cli/) | Current flags and command-specific behavior | Before freezing automation |
| Filtering | [Filtering](https://trivy.dev/docs/latest/configuration/filtering/) | Severity/status, ignore files, Rego, VEX | Adding filters/suppressions |
| File selection | [Selecting files](https://trivy.dev/docs/latest/configuration/skipping/) | Skip/include behavior | Changing scan scope |
| Reporting | [Reporting](https://trivy.dev/docs/latest/configuration/reporting/) | Formats, templates, result conversion | Choosing/validating evidence |
| Cache | [Cache](https://trivy.dev/docs/latest/configuration/cache/) | Cache backends and semantics | Sharing or cleaning cache |
| Databases | [Databases](https://trivy.dev/docs/latest/configuration/db/) | DB repositories, freshness, update settings | Online/offline/mirrored scans |
| SBOM generation | [Supply-chain SBOM](https://trivy.dev/docs/latest/supply-chain/sbom/) | CycloneDX/SPDX generation | Producing SBOM evidence |
| Attestations | [Attestation](https://trivy.dev/docs/latest/supply-chain/attestation/) | SBOM/scan-record attestation workflows | Signing/publishing attestations |
| VEX | [VEX](https://trivy.dev/docs/latest/supply-chain/vex/) | Repository, local, SBOM-reference, and attestation VEX | Modifying vulnerability status |
| Built-in compliance | [Built-in compliance](https://trivy.dev/docs/latest/compliance/) | Available reports and status | Running compliance evidence |
| Custom compliance | [Custom compliance](https://trivy.dev/docs/latest/compliance/custom/) | Custom report definitions | Creating an organizational profile |
| Modules | [Modules](https://trivy.dev/docs/latest/advanced/modules/) | Module lifecycle and status | Enabling extension modules |
| Plugins | [Plugin user guide](https://trivy.dev/docs/latest/plugin/user-guide/) | Plugin search/install/run/update behavior | Executing a plugin |
| Connectivity | [Network considerations](https://trivy.dev/docs/latest/advanced/connectivity/) | Required endpoints and network behavior | Designing egress/proxy rules |
| Database mirrors | [Self-hosting databases](https://trivy.dev/docs/latest/advanced/self-hosting/) | Mirroring/self-hosting patterns | Operating an internal mirror |
| Telemetry | [Usage telemetry](https://trivy.dev/docs/latest/advanced/telemetry/) | Telemetry behavior and controls | Applying privacy/network policy |
| Modes | [Standalone and client/server](https://trivy.dev/docs/latest/references/modes/) | Mode boundaries and server behavior | Deploying a Trivy server |
| Troubleshooting | [Troubleshooting](https://trivy.dev/docs/latest/references/troubleshooting/) | Maintainer troubleshooting guidance | Diagnosing repeatable failures |
| Action releases | [trivy-action releases](https://github.com/aquasecurity/trivy-action/releases) | Action release-to-commit mapping | Updating CI pins |
| 2026 incident | [Initial incident record](https://github.com/aquasecurity/trivy/discussions/10425) | Affected channels/windows and response | Assessing historical exposure |
| 2026 conclusion | [Incident conclusion](https://github.com/aquasecurity/trivy/discussions/10462) | Maintainer remediation and conclusions | Updating durable controls |
| Secure Actions use | [GitHub security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions) | Full-SHA pinning and workflow trust | Reviewing CI configuration |

## Source handling rules

1. Open and read the source; do not rely on a search snippet.
2. Record the consulted URL, access date, installed Trivy version, and target command.
3. Treat `latest`, `dev`, and floating tags as navigational conveniences, not immutable evidence.
4. For releases/actions/images, record the immutable checksum, commit SHA, or digest.
5. For experimental features—including YAML ignore behavior where currently marked—verify the installed release and test syntax before production use.
6. When official documentation and installed behavior differ, stop, preserve both observations, and consult release notes or upstream issues rather than inventing a reconciliation.
7. Independent security research may supplement incident analysis but must not override official command/schema documentation.
