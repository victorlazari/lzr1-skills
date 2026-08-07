# Trivy Supply-Chain Security

**Verified against upstream:** 2026-08-07

## Contents

1. [Why the scanner is a privileged dependency](#why-the-scanner-is-a-privileged-dependency)
2. [The 2026 incident](#the-2026-incident)
3. [Mandatory trust gate](#mandatory-trust-gate)
4. [Verification by distribution channel](#verification-by-distribution-channel)
5. [GitHub Actions controls](#github-actions-controls)
6. [Runtime containment](#runtime-containment)
7. [Historical-execution response](#historical-execution-response)
8. [Evidence record](#evidence-record)
9. [Sources](#sources)

## Why the scanner is a privileged dependency

A scanner commonly receives source code, lockfiles, container layers, registry credentials, cloud configuration, CI tokens, environment variables, and access to private infrastructure. It may run before build isolation is established and may be permitted to upload SARIF or artifacts. Treat the scanner binary, container, action, plugin, module, custom policy, database, and report template as executable or policy-bearing supply-chain components.

A successful-looking scan is not proof that the scanner was trustworthy. Release names, badges, mutable tags, and normal output establish neither publisher identity nor artifact integrity.

## The 2026 incident

Aqua's public incident record describes a February–March 2026 compromise affecting parts of Trivy's release and automation supply chain. Malicious artifacts were distributed through multiple affected channels during defined windows, including Trivy binaries/container artifacts and releases associated with `trivy-action` and `setup-trivy`. Aqua identified malicious Trivy versions 0.69.4, 0.69.5, and 0.69.6 in affected channels and documented later remediation.[1][2][3]

Independent technical analysis reported that poisoned action tags executed credential-stealing behavior before invoking legitimate scanner behavior. The targeted material included runner memory, environment variables, cloud and registry credentials, SSH keys, Kubernetes secrets, database credentials, CI configuration, infrastructure-as-code secrets, and other sensitive files.[4]

Do not convert this history into a timeless blocklist. Exposure windows, indicators, affected digests, and response guidance are volatile incident facts. Re-read Aqua's current incident record before making an incident determination.

## Mandatory trust gate

Before first execution in an environment, create a trust record with:

| Field | Required evidence |
|---|---|
| Component | Binary, container, GitHub Action, package, plugin, module, custom check, template, or database |
| Source | Canonical official release/repository/registry URL and acquisition timestamp |
| Immutable identity | SHA-256 checksum, container digest, full Git commit SHA, or content hash |
| Publisher verification | Result of official checksum/signature verification and signer identity |
| Provenance | Attestation/provenance result when the release publishes it |
| Version relationship | Human-readable release mapped to the immutable identity |
| Environment | Runner type, persistence, mounts, token permissions, secrets, and egress policy |
| Databases/checks | Source registry/mirror, downloaded artifact identity, and freshness metadata |
| Decision | Approved, rejected, or incomplete, with reviewer and date |

**Fail closed** when the expected identity cannot be verified. Do not solve a verification failure by using a floating tag or disabling signature/TLS checks.

## Verification by distribution channel

### Release binary

1. Open the canonical upstream release page over authenticated TLS.
2. Select the expected release deliberately; do not resolve `latest` in automation.
3. Download the binary archive, published checksums, signature, and provenance material separately.
4. Verify the checksum before extraction or execution.
5. Verify the published signature/provenance using the upstream-documented method and expected identity.
6. Record the final executable SHA-256 hash and `trivy --version` output.
7. Execute only from a controlled location with least privilege.

Never use a remote-install pipeline that downloads and immediately executes code. Package-manager installation still requires validation of repository identity, package version, and local provenance appropriate to that ecosystem.

### Container image

1. Resolve the selected release tag to an immutable digest through the trusted registry.
2. Verify the image signature/provenance according to Trivy's current signature-verification guidance.
3. Pin the digest in automation and record the platform architecture.
4. Review mounts, user, capabilities, network access, and exposed credentials.
5. Re-resolve the human-readable tag during planned dependency updates; never silently follow it at runtime.

### GitHub Action

1. Select a reviewed release from the canonical action repository.
2. Resolve the release tag to a full 40-character commit SHA through the GitHub API or a verified local clone.
3. Inspect the action metadata and entrypoint at that commit.
4. Pin `uses:` to the full commit SHA and annotate the expected release tag as a comment.
5. Re-verify the mapping whenever dependency automation proposes an update.
6. Treat a changed tag target, unexpected entrypoint, or unexplained distribution change as an incident signal.

The bundled workflow contains SHAs resolved on 2026-08-07. They are examples of the required form, not permanent claims of suitability. Re-resolve them before adoption.

### Database, checks bundle, VEX repository, plugin, or module

These components affect results or execute code/policy. Use only approved sources, pin immutable versions/digests where supported, verify signatures and content hashes, and retain acquisition evidence. Review plugins and modules as executable code. Review custom Rego and templates as policy/code that can alter decisions or expose report data.

## GitHub Actions controls

A hardened scan job should:

- pin **every** third-party action to a full commit SHA;
- use explicit least-privilege `permissions` and grant `security-events: write` only to the upload job that needs it;
- avoid privileged secrets and write tokens on untrusted pull-request code;
- run on ephemeral, isolated runners where possible;
- set job timeouts and concurrency cancellation;
- resolve the target by commit and container images by digest;
- prevent workflow-command injection by quoting data and avoiding unsafe interpolation in `run:` scripts;
- retain the scan log, JSON/SARIF, SBOM, configuration, version/database metadata, and artifact hashes;
- separate the scan result from upload status so a publishing failure does not hide a scan failure;
- use dependency-update tooling that understands immutable SHA pins and produces reviewable changes.

Do not grant `contents: write`, package publishing, cloud federation, or deployment permissions to a scan job unless a separately reviewed workflow requires them.

## Runtime containment

Even a verified scanner should run with bounded authority:

- prefer read-only target mounts;
- use a dedicated output directory and avoid mounting home directories, SSH agents, Docker sockets, or broad cloud credentials;
- pass only credentials required for the target, with read-only scope and short lifetime;
- restrict egress to approved registries, mirrors, or server endpoints;
- do not scan untrusted repositories on persistent privileged runners;
- keep report artifacts confidential because secret findings and source paths may be sensitive;
- disable telemetry only through the supported setting when policy requires it; do not weaken TLS;
- inspect plugins, custom checks, templates, and modules before enabling them.

## Historical-execution response

If an artifact that may fall within an affected incident window executed:

1. preserve workflow logs, runner images, artifact digests, action SHAs, network logs, and acquisition records;
2. identify the exact artifact identity and execution time rather than relying on a tag name;
3. isolate persistent or self-hosted runners that may retain material;
4. consult the latest official incident record for affected identities and indicators;
5. scope every credential, token, key, secret, mounted file, and metadata service reachable by the process;
6. follow the organization's incident-response process for revocation and rotation—do not rotate blindly before preserving necessary evidence;
7. inspect downstream use of potentially exposed credentials and invalidate sessions where applicable;
8. document the decision, evidence, and residual uncertainty.

Route the investigation to `security-review` or the organization's incident-response team. Do not publish indicators, secrets, or victim details in a public issue.

## Evidence record

Use this compact record in scan evidence:

```yaml
scanner_trust:
  acquired_from: "canonical URL or package repository"
  version: "runtime output"
  immutable_identity: "sha256, digest, or full commit SHA"
  checksum_verified: true
  signature_verified: true
  provenance_verified: true
  verification_method: "official procedure and tool version"
  verified_at: "RFC3339 timestamp"
  reviewer: "team or role"
  runner:
    ephemeral: true
    token_permissions: "documented minimal set"
    secret_exposure: "none or enumerated scope"
    egress_policy: "approved endpoints"
  data_sources:
    vulnerability_db: "registry/mirror and metadata"
    java_db: "registry/mirror and metadata"
    checks_bundle: "registry and identity"
    vex: "source and identity"
```

Do not store credential values in this record.

## Sources

The first three sources are the upstream incident record and maintainer response. The fourth is independent technical analysis used to understand observed attacker behavior.

1. [Aqua Security / Trivy: Security incident 2026-03-19](https://github.com/aquasecurity/trivy/discussions/10425)
2. [Aqua Security / Trivy: incident conclusion](https://github.com/aquasecurity/trivy/discussions/10462)
3. [Aqua Security: Trivy supply-chain attack update](https://www.aquasec.com/blog/trivy-supply-chain-attack-what-you-need-to-know/)
4. [CrowdStrike: From Scanner to Stealer](https://www.crowdstrike.com/en-us/blog/from-scanner-to-stealer-inside-the-trivy-action-supply-chain-compromise/)
5. [Trivy signature verification](https://trivy.dev/docs/latest/getting-started/signature-verification/)
6. [GitHub: secure use reference for pinning actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions)

Recheck all incident facts and release-verification procedures at execution time.
