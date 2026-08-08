# Trivy Targets, Scanners, and Operations

**Verified against upstream:** 2026-08-07

## Contents

1. [Target selection](#target-selection)
2. [Scanner semantics](#scanner-semantics)
3. [Configuration and precedence](#configuration-and-precedence)
4. [Databases, cache, and checks](#databases-cache-and-checks)
5. [Online, mirrored, and air-gapped operation](#online-mirrored-and-air-gapped-operation)
6. [Standalone and client/server modes](#standalone-and-clientserver-modes)
7. [Custom checks, modules, plugins, and templates](#custom-checks-modules-plugins-and-templates)
8. [Kubernetes and remote targets](#kubernetes-and-remote-targets)
9. [Coverage validation](#coverage-validation)
10. [Troubleshooting sequence](#troubleshooting-sequence)
11. [Sources](#sources)

## Target selection

Choose the target command from the object actually being assessed. Do not substitute a convenient target and imply equivalent coverage.

| Target | Command family | Typical evidence | Key limitations and controls |
|---|---|---|---|
| Container image | `trivy image` | OS and language packages, image configuration, secrets/licenses where supported | Resolve a digest; document registry source, platform, image source order, and whether image config scanning is enabled. |
| Filesystem | `trivy fs` | Local project files, lockfiles, IaC, secrets, licenses | Scans only available files; generated artifacts or runtime packages may be absent. |
| Repository | `trivy repo` | A remote or local repository checkout | Remote operation creates network/authentication boundaries. Record branch, tag, or commit and prefer an immutable commit. |
| Root filesystem | `trivy rootfs` | OS/application packages from an unpacked root filesystem | Ensure the path is an intended rootfs and protect mounted host data. |
| Kubernetes | `trivy k8s` | Cluster resources, workload images, configuration findings | Scope context, namespaces, included/excluded kinds, node collection, API permissions, and cluster load. |
| VM image | `trivy vm` | Supported VM/disk image content | Validate supported formats, storage requirements, and isolation before opening untrusted images. |
| SBOM | `trivy sbom` | Vulnerabilities represented by CycloneDX/SPDX content | Cannot recover components omitted from the SBOM; preserve generator and completeness metadata. |

Use `trivy <command> --help` and the current official target guide before execution. Defaults and flags are volatile.

## Scanner semantics

### Vulnerability scanner

The vulnerability scanner matches detected OS and language packages against Trivy's vulnerability intelligence. Results depend on correct package, distribution, version, and end-of-life detection. A finding is not proof of exploitability; an absent finding is not proof of safety.

Record:

- detected operating system/distribution and package ecosystems;
- package relationship and development-dependency choices;
- severity source, status filtering, ignored statuses, and unfixed-finding policy;
- database source, schema/metadata, update status, and offline/mirror mode;
- end-of-life warnings, detection-priority setting, and unsupported packages;
- VEX sources and whether they changed result status.

### Misconfiguration scanner

The misconfiguration scanner evaluates supported IaC/configuration formats using built-in or custom checks. Coverage varies across Terraform, Terraform plans, Kubernetes, Helm, Dockerfiles, CloudFormation, Azure ARM, and other supported formats.

Record rendered inputs, variable/values files, downloaded-module policy, included namespaces, custom checks/data, checks-bundle identity, deprecated-check policy, and parse failures. A static configuration finding does not establish deployed runtime state.

### Secret scanner

The secret scanner identifies content matching built-in or custom rules. Secret findings can themselves be sensitive. Redact values from reports, logs, examples, and issue trackers. Confirm whether a finding represents an active credential through an approved incident process; do not test a credential against a service without authorization.

Custom rules require stable identifiers, bounded regexes/keywords, severity, path-aware allow rules, tests with synthetic values, and review for catastrophic regex behavior or broad false positives.

### License scanner

The license scanner reports detected license evidence. Coverage differs between package metadata and full source scanning, and path filtering has ecosystem limitations. Treat detected categories as technical evidence only. Organizational allow/deny policy and legal compatibility decisions require an approved policy owner or legal review.

### Scanner defaults

Defaults vary by target and release. For example, the official configuration reference verified on the date above shows `vuln` and `secret` in the generic scan defaults, but this is not a promise for every target or future version. Always specify the required scanners explicitly in automation and preserve the final command/configuration.

## Configuration and precedence

Trivy accepts CLI flags, `TRIVY_` environment variables, and YAML configuration. Precedence is:

1. CLI flags;
2. environment variables;
3. YAML configuration.

The default file name is `trivy.yaml`; `--config` selects another file. A CLI option generally maps to an uppercase `TRIVY_` variable with underscores replacing hyphens, but verify the current reference before use.

Before execution:

1. record every config file and SHA-256 hash;
2. list only the **names** of relevant environment variables, never secret values;
3. capture the explicit CLI arguments;
4. identify conflicting settings and document the winning value;
5. reject `insecure: true`, broad skip lists, unknown plugins, or credential-bearing config;
6. use `trivy <command> --help` to verify volatile flags.

The bundled [configuration template](../templates/trivy.yaml) intentionally includes a small supported subset. For a release-specific complete example, use the current official configuration-file reference rather than copying an old generated default.

## Databases, cache, and checks

Trivy may obtain vulnerability, Java, checks, and VEX data from upstream registries or configured mirrors. Cache behavior differs between standalone and client/server operation.

Capture:

- each repository or mirror and immutable artifact identity where available;
- update time and metadata reported by Trivy;
- cache backend/location, retention, and sharing boundary;
- whether database/check updates were skipped;
- the reason for offline mode and how data was transferred;
- checks-bundle, VEX repository, module, and plugin versions/content hashes.

Do not treat a completed command as current if updates failed or were intentionally skipped. A scan with stale or absent data must be marked **incomplete** unless the stated objective explicitly accepts the pinned data set.

Avoid sharing a mutable filesystem cache across mutually untrusted jobs. Protect Redis or other remote cache backends with authentication, TLS, network controls, and tenancy boundaries. Never put cache credentials in a repository.

## Online, mirrored, and air-gapped operation

### Online

Document outbound endpoints and approve registry, VEX, checks, telemetry, and target connections. Use TLS verification and least-privilege credentials. Treat automatic data updates as network actions even though they do not modify the target.

### Mirrored

Verify the mirror's ownership, synchronization, retention, signature behavior, and artifact identity. Record how the mirror maps to official upstream artifacts. A mirror improves availability and egress control but becomes another trusted publisher.

### Air-gapped

Prepare all required databases, checks bundles, policies, modules/plugins, and scanner artifacts outside the enclave using verified sources. Transfer them with signed/hash manifests through the approved media process. Inside the enclave:

1. verify transfer hashes and signatures;
2. use supported skip-update/offline settings;
3. point repositories/mirrors to approved local sources;
4. prevent unexpected egress;
5. record data age and refresh procedure;
6. test the complete workflow with a synthetic target before relying on results.

Offline mode can reduce lookup capability and never makes stale data current. Follow the exact current official air-gap/database guidance for the installed release.

## Standalone and client/server modes

In standalone mode, the client performs local analysis and uses local/cache data. In client/server mode, the server primarily provides vulnerability analysis/data services; not every scanner or target behavior moves to the server. Confirm current mode limitations.

For client/server use:

- authenticate the endpoint and verify TLS identity;
- do not disable certificate verification;
- scope tokens and custom headers, and prevent them from logs;
- document which data leaves the client and which analysis remains local;
- restrict listener interfaces and network access;
- bound timeouts and request concurrency;
- align client/server versions according to current compatibility guidance;
- monitor server database freshness and availability;
- treat server compromise as an integrity and confidentiality risk.

## Custom checks, modules, plugins, and templates

### Custom Rego checks

Review custom checks as code. Validate package namespaces, selectors, schemas, external data, test fixtures, failure behavior, and compatibility with the installed Trivy version. Run policy tests before production use. Pin repositories/commits and record content hashes.

### Modules

Trivy modules are an extension surface and may be experimental or release-sensitive. Inspect source, publisher, declared capabilities, install/update behavior, and content identity. Never auto-install a module from an unreviewed location during a scan.

### Plugins

Plugins are executable code. Search results or a plugin registry entry do not establish trust. Review the plugin repository and release, verify immutable artifacts, constrain environment/secrets/network access, and test in isolation. Pin the version/digest and do not use an unattended floating upgrade.

### Output templates

Templates process finding data and can expose sensitive fields. Pin and review templates, render only to protected paths, and test escaping for the destination format. Do not download a template at scan time without verification.

## Kubernetes and remote targets

For Kubernetes, begin with a read-only identity and explicit context. Capture:

- cluster/context identity and server endpoint;
- namespaces and resource kinds included/excluded;
- whether node collection is enabled and the additional privilege it requires;
- workload image references and resolved digests;
- timeout, concurrency, and expected API load;
- handling of secrets/configuration in reports;
- which results came from manifest checks versus image scans.

For private repositories and registries, use short-lived read-only credentials. Avoid embedding credentials in URLs. Redact target URLs if they contain sensitive organization names or paths.

## Coverage validation

A valid evidence bundle answers:

| Question | Evidence |
|---|---|
| Was the intended target scanned? | Canonical path/ref plus commit, digest, context, or SBOM hash |
| Which scanner build ran? | Version output and executable hash/image digest/action SHA |
| Which scanners ran? | Explicit scanner list and final command/config |
| Which data sources informed results? | Database/check/VEX metadata and update status |
| What was skipped? | Skip lists, unsupported files, parsing warnings, scanner omissions |
| Did the output parse? | JSON/SARIF/SBOM validation result and file hashes |
| Did policy pass? | Exit code, gate configuration, and finding summary |
| What left the environment? | Registry/server/upload endpoints and artifact destinations |

An empty result without these answers is inconclusive.

## Troubleshooting sequence

1. Reproduce with the same immutable target and scanner identity.
2. Capture `trivy --version`, the target-command help, exact exit code, and stderr.
3. Confirm configuration precedence and remove only one override at a time.
4. Verify target accessibility and credentials without printing secret values.
5. Verify database/check freshness and mirror reachability.
6. Reduce to one scanner and the smallest representative target.
7. Distinguish parser/coverage warnings from finding-policy failures.
8. Consult the matching current command reference and upstream issue tracker.
9. Retry only after changing one documented variable; otherwise stop and report.

## Sources

- [Targets overview](https://trivy.dev/docs/latest/guide/)
- [Scanner overview](https://trivy.dev/docs/latest/scanner/vulnerability/)
- [Coverage overview](https://trivy.dev/docs/latest/coverage/)
- [Configuration overview](https://trivy.dev/docs/latest/configuration/)
- [Configuration-file reference](https://trivy.dev/docs/latest/references/configuration/config-file/)
- [CLI command reference](https://trivy.dev/docs/latest/references/configuration/cli/trivy/)
- [Standalone and client/server modes](https://trivy.dev/docs/latest/references/modes/client-server/)
- [Databases](https://trivy.dev/docs/latest/configuration/db/)
- [Cache](https://trivy.dev/docs/latest/configuration/cache/)
- [Connectivity and network considerations](https://trivy.dev/docs/latest/guide/advanced/air-gap/)
- [Self-hosting databases](https://trivy.dev/docs/latest/advanced/self-hosting/)
- [Modules](https://trivy.dev/docs/latest/advanced/modules/)
- [Plugins](https://trivy.dev/docs/latest/plugin/)
- [Custom checks](https://trivy.dev/docs/latest/scanner/misconfiguration/custom/)
- [Troubleshooting](https://trivy.dev/docs/latest/references/troubleshooting/)

Verify redirects and current page locations when consulting these sources; the official documentation reorganizes sections across releases.
