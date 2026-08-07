---
name: trivy-scanner
description: "Plan, execute, validate, and operationalize Trivy security scans across repositories, filesystems, images, Kubernetes, VM images, and SBOMs. Use for vulnerability, misconfiguration, secret, license, compliance, SBOM/VEX, CI, air-gapped, client/server, or Trivy incident-response work."
---

# Trivy Scanner

Use this skill to operate Trivy as a **high-trust security dependency**. Begin with artifact verification, select the correct target and scanners, retain machine-readable evidence, and distinguish prioritization from governed suppression. Do not install, upgrade, execute, or replace a scanner artifact merely because a tag or badge looks legitimate.

## Scope

Use this skill for:

- repository, filesystem, root filesystem, container image, Kubernetes, VM image, and SBOM targets;
- vulnerability, misconfiguration, secret, and license scanners;
- SBOM generation and ingestion, VEX, attestations, compliance evidence, custom checks, and reporting;
- standalone, client/server, CI, offline, mirrored-database, module, or plugin operation;
- Trivy configuration, filtering, suppression review, troubleshooting, or scanner supply-chain investigation.

Route a complete manual application-security assessment to `security-review`. Route PR-review orchestration and CodeRabbit remediation to `coderabbit-reviewer`. Route publication-quality scan summaries and repository documentation to `legendary-readme`.

This skill does not declare a system secure, grant a compliance certification, make a legal license decision, or automatically remediate findings.

## Hard stop: establish scanner trust

Trivy's February–March 2026 supply-chain compromise demonstrated that a security scanner and its CI action can become credential-stealing code while still appearing to run normally. Before executing Trivy in a sensitive environment, establish and record all applicable facts:

1. acquisition channel and expected publisher;
2. exact binary version and checksum, container digest, or GitHub Action commit SHA;
3. verification of official checksum, signature, and provenance material available for that release;
4. runner isolation, token permissions, mounted credentials, and outbound-network exposure;
5. vulnerability, Java, checks, and VEX database sources and freshness;
6. whether a plugin, module, custom check, remote server, or mirror adds another trust boundary.

**Stop** if the executable or action cannot be tied to verified official release evidence. Never trust `latest`, a movable container tag, a release name alone, a mutable major/minor action ref, or a downloaded executable without verification. Do not pipe a remote installer into a shell. For the incident history, current verification procedure, and response steps, load [Supply-chain security](references/supply-chain-security.md).

## Intake and preconditions

Before choosing commands, capture the following.

| Decision | Required input |
|---|---|
| Objective | Discovery, release gate, audit evidence, SBOM, VEX validation, compliance evidence, or incident investigation |
| Target | Local path, repository URL, image reference/digest, Kubernetes context, VM image, or SBOM |
| Scanner scope | Vulnerability, misconfiguration, secret, license, or an explicitly justified combination |
| Trust boundary | Local binary, verified container, pinned action, client/server endpoint, plugin, or module |
| Data exposure | Source, manifests, package names, secrets, SBOM contents, and whether data may leave the environment |
| Network policy | Online, proxy-restricted, mirrored, or fully air-gapped |
| Gate policy | Severities, fix availability, status, exception policy, expiry, and exit behavior |
| Evidence | Required formats, retention, signing, upload destination, and confidentiality |

Obtain confirmation before scanning production clusters, private registries, remote repositories, persistent CI runners, or any target whose access may create load, transmit data, or expose credentials.

## Choose the target before the scanners

| Target | Trivy command family | Primary use | Important boundary |
|---|---|---|---|
| Container image | `trivy image` | OS/library packages, image config, secrets, licenses | Prefer an immutable digest; registry access can expose credentials and pull data. |
| Local project or artifact tree | `trivy fs` | Local source, lockfiles, IaC, secrets, licenses | Coverage follows files present locally. |
| Remote code repository | `trivy repo` | Clone-and-scan repository content | Requires network and may handle repository credentials. Prefer a controlled local clone for sensitive code. |
| Unpacked root filesystem | `trivy rootfs` | Host/container rootfs package analysis | Treat paths and mounted host data as sensitive. |
| Kubernetes | `trivy k8s` | Cluster resources and workload images | Read-only API access can still expose sensitive configuration; scope context and namespaces. |
| VM image | `trivy vm` | Supported VM/disk-image inspection | Large images and mounted data require storage and isolation planning. |
| Existing SBOM | `trivy sbom` | Analyze packages represented in an SBOM | Results cannot exceed SBOM completeness or Trivy's supported SBOM fields. |

Consult [Targets, scanners, and operations](references/targets-scanners-operations.md) before using target-specific options. Interrogate the installed build with `trivy <command> --help`; do not assume flags remain unchanged.

## Scanner selection

Select only scanners that answer the stated question. Scanner availability and defaults differ by target.

| Scanner | Finds | Does not prove |
|---|---|---|
| `vuln` | Known vulnerabilities in detected OS and language packages | Exploitability, reachability, or absence of unknown vulnerabilities |
| `misconfig` | Built-in/custom policy findings in supported IaC and configuration formats | Runtime state, business authorization, or complete cloud posture |
| `secret` | Content matching built-in or custom secret rules | Whether a credential is active; avoid exposing matched values in logs |
| `license` | Detected package/source license evidence | Legal compatibility or organizational approval |

Record disabled scanners, skipped paths, unsupported ecosystems, parsing warnings, and target coverage as limitations. Treat a zero-finding result without coverage evidence as inconclusive.

## Operating workflow

### 1. Freeze the plan

Write a scan plan containing the target identity, immutable target digest or commit when available, selected scanners, configuration files, database policy, expected formats, exit policy, and suppression sources. For code, record the commit. For images, resolve and record the digest. For Kubernetes, record context, namespaces, and authorization scope.

### 2. Capture preflight evidence

Record commands and outputs needed to reproduce the run:

```bash
trivy --version
trivy <target-command> --help
```

Also record executable hash or image digest, action SHA, configuration precedence, database metadata shown by Trivy, environment mode, and redacted proxy/mirror settings. CLI flags override environment variables, which override the YAML configuration file. Never capture secret values.

### 3. Validate configuration without broadening trust

Review [the baseline configuration template](templates/trivy.yaml), [secret configuration](templates/trivy-secret.yaml), and any local overrides. Confirm that:

- `insecure` remains disabled;
- skipped directories/files are narrowly justified;
- offline mode is paired with pre-positioned databases and checks;
- custom checks, modules, plugins, templates, and mirrors are separately verified;
- no token or registry password is stored in config or command history;
- output directories are private and excluded from source control where appropriate.

### 4. Preview, then scan

For a local repository, preview the bundled runner first:

```bash
bash scripts/comprehensive_scan.sh --dry-run --target /absolute/path --output-dir /absolute/evidence/path
```

After reviewing the plan, run it without `--dry-run`. The script never installs Trivy, downloads an executable, changes the target, or suppresses failures. It writes a manifest, JSON, SARIF, SBOM, logs, hashes, and a policy-gate status to the explicit output directory.

For other targets, assemble the smallest command from the current `--help` output and [target reference](references/targets-scanners-operations.md). Quote paths and treat remote access, database updates, image pulls, and uploads as explicit network actions.

### 5. Validate evidence before interpreting findings

Confirm every expected file exists, is non-empty, parses in its declared format, and has a recorded SHA-256 digest. Check the Trivy exit code independently from transport or upload success. Preserve stderr because warnings about unsupported files, stale databases, and partial analysis are coverage evidence.

Use [Reporting and evidence](references/reporting.md) for table, JSON, SARIF, template, SBOM, and dependency-snapshot handling. Treat uploaded SARIF, artifacts, attestations, and dependency snapshots as external writes requiring appropriate authorization.

### 6. Triage without hiding uncertainty

Classify each actionable finding with target, component/path, identifier, installed/fixed version where applicable, severity and source, evidence, reachability or exposure context, proposed owner, and confidence. Do not equate severity with exploitability. Where business or code context is required, route to `security-review`.

### 7. Govern every suppression

Prioritization changes what is displayed; suppression removes findings from normal results. Review [Filtering and suppression](references/filtering.md) before creating an exception.

Every exception requires an owner, evidence/ticket, scope, rationale, expiry, approval state, and a validation test. Trivy's experimental YAML ignore schema accepts `id`, `paths`, `purls`, `expired_at`, and `statement`; keep ownership and evidence in a separate governance ledger rather than unsupported Trivy keys. Preview a proposal with:

```bash
bash scripts/setup_ignore.sh --dry-run --type vulnerabilities --id CVE-YYYY-NNNN \
  --statement "Bounded technical rationale" --owner "team" \
  --evidence "ticket-or-URL" --expires YYYY-MM-DD --output-dir /absolute/review/path
```

Do not merge the proposal until the installed Trivy build accepts it and a reviewer confirms it is narrowly scoped. Prefer VEX when a product-status assertion can be produced and maintained by an authoritative party.

### 8. Add a CI gate only after local validation

Start from [the immutable GitHub Actions template](templates/github-actions-trivy.yaml). Re-resolve every annotated release tag to its expected full commit SHA before adoption; a pin is immutable but can still point to an obsolete or historically compromised release. Keep least-privilege permissions, ephemeral runners, timeouts, concurrency, minimal secrets, and artifact retention. Never expose privileged secrets to untrusted pull-request code.

### 9. Report coverage, not just counts

Produce the output contract below. State skipped or failed analysis prominently. A clean report with a stale database, unsupported target, incomplete SBOM, ignored exit code, or broad suppression is not a passing result.

## Bounded parallel review

Parallelize only when at least five independent targets or evidence dimensions can use the same schema. Provide each worker with target identity, trust evidence, scanner set, configuration hash, and output schema. Set a finite concurrency limit, prohibit workers from changing suppressions, and synthesize once by stable finding identity. Stop when every target has a validated result, the iteration cap is reached, or progress stalls. Never create an unbounded scan–fix loop.

## Failure handling

| Failure | Response |
|---|---|
| Artifact trust cannot be established | Stop; reacquire from the official channel and verify independently. Do not make an exception to run the scanner. |
| Database/check update fails | Preserve the error and freshness metadata; use a verified mirror or approved offline bundle, or report the scan as incomplete. |
| Target authentication fails | Confirm scope and credential source without printing secrets; do not broaden permissions reflexively. |
| Partial/unsupported analysis | Record the unsupported component and supplement with another appropriate tool or manual review. |
| Scanner crashes or times out | Preserve logs, reduce the target deterministically, and retry only after changing one documented variable. |
| CI upload fails after scan | Preserve local evidence and distinguish scan status from publishing status. |
| Findings do not decrease in a remediation loop | Stop at the iteration cap or when the same set repeats; report the blocking root cause. |

## Output contract

Return a concise report containing:

1. **Scope and identity:** target type, path/ref, commit or digest, date, and operator environment.
2. **Trust evidence:** Trivy version, executable hash/image digest/action SHA, acquisition channel, verification result, database/check/VEX provenance, and runner isolation.
3. **Configuration:** selected scanners, configuration hash, filters, skip rules, suppression/VEX sources, network mode, and exit policy.
4. **Coverage:** detected ecosystems, scanned objects, unsupported/skipped items, warnings, and limitations.
5. **Findings:** stable identifier, component/path, severity source, status, fix evidence, confidence, and owner/next action.
6. **Exceptions:** owner, rationale, scope, evidence, approval, expiry, and validation result.
7. **Evidence index:** files, formats, SHA-256 digests, retention location, and upload/attestation status.
8. **Outcome:** pass, fail, or incomplete—never infer pass from an empty result alone.

## Resources

| Resource | Load or run when |
|---|---|
| [Supply-chain security](references/supply-chain-security.md) | Verifying artifacts/actions, reviewing the 2026 incident, or responding to historical execution |
| [Targets, scanners, and operations](references/targets-scanners-operations.md) | Selecting targets/scanners, offline/client-server modes, databases, modules, plugins, or custom checks |
| [Filtering and suppression](references/filtering.md) | Prioritizing results, using ignore files/Rego/VEX, or reviewing exceptions |
| [Compliance and SBOM](references/compliance-sbom.md) | Generating/consuming SBOMs, attestations, VEX, or compliance evidence |
| [Reporting and evidence](references/reporting.md) | Selecting formats, validating output, SARIF, artifacts, templates, or dependency snapshots |
| [Authoritative source map](references/sources.md) | Checking volatile behavior against current official documentation |
| [Comprehensive scan runner](scripts/comprehensive_scan.sh) | Producing a reproducible local-repository evidence bundle |
| [Suppression proposal runner](scripts/setup_ignore.sh) | Generating review-only ignore and governance proposals |
| [Pinned GitHub Actions workflow](templates/github-actions-trivy.yaml) | Adding a least-privilege CI scan after re-verifying pins |
| [Secret rules template](templates/trivy-secret.yaml) | Defining organization-specific secret rules and allow rules |
| [Baseline Trivy config](templates/trivy.yaml) | Starting a minimal supported configuration and documenting precedence |
| [YAML ignore template](templates/trivyignore.yaml) | Creating a schema-valid, time-bounded exception proposal |

**Source baseline:** official Trivy documentation and upstream repositories, verified 2026-08-07. Recheck volatile versions, flags, action SHAs, database locations, compliance IDs, schemas, and release-security guidance at execution time.
