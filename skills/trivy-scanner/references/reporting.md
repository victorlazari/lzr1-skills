# Trivy Reporting and Evidence Integrity

**Verified against upstream:** 2026-08-07
**Primary source:** [Trivy reporting documentation](https://trivy.dev/docs/latest/configuration/reporting/)

## Contents

1. [Evidence hierarchy](#evidence-hierarchy)
2. [Output formats](#output-formats)
3. [Canonical JSON workflow](#canonical-json-workflow)
4. [SARIF](#sarif)
5. [Templates and derived reports](#templates-and-derived-reports)
6. [SBOM and dependency snapshots](#sbom-and-dependency-snapshots)
7. [Multiple formats](#multiple-formats)
8. [Sensitive-data controls](#sensitive-data-controls)
9. [Validation and manifest](#validation-and-manifest)
10. [Finding identity and deduplication](#finding-identity-and-deduplication)
11. [Publication boundaries](#publication-boundaries)

## Evidence hierarchy

Use machine-readable output as the canonical record and derive human presentation from it when the installed release supports a lossless-enough conversion.

1. **Canonical scan evidence:** JSON plus stderr/log, invocation, configuration, target identity, scanner trust, and database metadata.
2. **Exchange/integration evidence:** SARIF, CycloneDX, SPDX, GitHub dependency snapshot, or another documented format.
3. **Human presentation:** table, Markdown, HTML, summary, chart, or issue text.

A table, badge, finding count, or upload success is not sufficient audit evidence. Never discard warnings because the result file parsed.

## Output formats

Format support, scanner-field coverage, and flags change across releases. Confirm with the installed target command and current official reporting page.

| Format family | Primary use | Important limitation |
|---|---|---|
| Table | Interactive human review | May truncate fields and is difficult to validate deterministically |
| JSON | Canonical analysis and automation | Schema and optional fields are release-sensitive |
| SARIF | Code-scanning/IDE exchange | May not preserve every Trivy-specific field; upload semantics are platform-specific |
| Go template | Controlled derived formats such as HTML/JUnit/ASFF | A template is code-like content that can expose or misrender findings |
| CycloneDX/SPDX | SBOM inventory exchange | SBOM semantics differ from a full Trivy findings report |
| GitHub dependency snapshot | Dependency Submission API integration | Publishing changes remote dependency-graph state and requires a scoped token |
| Plugin output | Specialized integrations | Adds executable plugin and destination trust boundaries |

Do not freeze a compatibility matrix without testing the exact installed release.

## Canonical JSON workflow

Representative command—verify current flags first:

```bash
trivy repo --format json --output /absolute/evidence/trivy.json /absolute/project
```

Immediately capture:

- process exit code;
- stdout/stderr separately;
- `trivy --version` output;
- executable hash, image digest, or action SHA;
- target commit/digest/hash;
- configuration files and hashes;
- database/check/VEX metadata and update outcome;
- JSON byte size, parse result, and SHA-256 hash.

Use defensive parsing because result arrays and fields can be absent. Example:

```python
import json
from collections import Counter
from pathlib import Path

path = Path("trivy.json")
data = json.loads(path.read_text(encoding="utf-8"))
if not isinstance(data, dict):
    raise ValueError("Trivy JSON root must be an object")

counts = Counter()
for result in data.get("Results") or []:
    if not isinstance(result, dict):
        continue
    for field in ("Vulnerabilities", "Misconfigurations", "Secrets", "Licenses"):
        for finding in result.get(field) or []:
            if isinstance(finding, dict):
                counts[(field, str(finding.get("Severity", "UNKNOWN")))] += 1

print(dict(sorted(counts.items())))
```

Do not assume a fixed `SchemaVersion`, severity set, or field presence. Validate business logic with fixtures from the exact release used in CI.

## SARIF

Generate SARIF only for a target/scanner combination supported by the installed release:

```bash
trivy repo --format sarif --output /absolute/evidence/trivy.sarif /absolute/project
```

Before upload:

1. parse it as JSON;
2. validate expected SARIF root/version and non-empty `runs` where findings are expected;
3. inspect artifact URIs for absolute paths, tokens, repository names, or sensitive infrastructure details;
4. record the SHA-256 hash;
5. compare finding counts to canonical JSON and explain expected loss/transformation;
6. authorize the repository, category, ref/commit, and visibility.

Uploading SARIF changes remote code-scanning state. Use a full-SHA-pinned upload action, least-privilege `security-events: write`, a trusted event context, and no privileged secrets for untrusted pull-request code. Consult the bundled [GitHub Actions template](../templates/github-actions-trivy.yaml).

Separate these statuses:

- scanner execution;
- policy gate;
- SARIF generation/validation;
- SARIF upload.

A successful upload cannot turn a failed scan into a pass, and a failed upload cannot erase valid local scan evidence.

## Templates and derived reports

Go templates can produce HTML, JUnit, ASFF, Markdown, or organization-specific output. Treat every template as reviewed code/content:

- pin and hash the template;
- do not download it during the scan without verification;
- inspect escaping for HTML/Markdown/XML/CSV contexts;
- prevent formula injection in spreadsheet-oriented output;
- keep secret values and sensitive paths out of public reports;
- test empty, malformed, high-volume, and unusual-character findings;
- preserve canonical JSON separately.

Representative syntax—verify against the current release:

```bash
trivy repo --format template --template '@/reviewed/report.tpl' \
  --output /absolute/evidence/report.html /absolute/project
```

A rendered document is a presentation artifact, not the canonical record.

## SBOM and dependency snapshots

CycloneDX and SPDX outputs are inventory artifacts. See [Compliance and SBOM](compliance-sbom.md) for validation and subject binding.

A GitHub dependency snapshot is intended for GitHub's Dependency Submission API. Generation and submission are distinct operations. Validate the snapshot locally, bind it to the correct repository/commit, and obtain authorization before submission. Use a narrowly scoped token and a trusted workflow event.

Dependency-tree and all-package options can improve triage/inventory but may increase output sensitivity and volume. Confirm current flag compatibility and record whether they were enabled.

## Multiple formats

Trivy commonly writes one selected format per invocation. Multiple independent scans can drift if databases, target content, or configuration change between runs.

Preferred order:

1. freeze target and configuration;
2. create canonical JSON;
3. use the installed `trivy convert` capability when it supports the required destination and preserves needed fields;
4. otherwise repeat the scan only with the same immutable target, scanner build, data sources, and configuration;
5. compare counts and record why formats differ.

Never overwrite an earlier artifact. Use distinct deterministic paths and hash every file.

## Sensitive-data controls

Reports can reveal:

- secret rule matches or surrounding content;
- internal paths, repositories, registries, clusters, namespaces, and account names;
- complete package inventory and vulnerable versions;
- image history, layers, labels, and configuration;
- source snippets, policies, and exception rationale.

Controls:

- create output directories with restrictive permissions;
- exclude evidence directories from source control;
- avoid console output on shared CI logs;
- redact secret **values**, tokens, signed URLs, credentials, and sensitive path segments in derived reports;
- retain stable identifiers and enough non-secret context for remediation;
- encrypt and apply retention/access policies to stored artifacts;
- review visibility before uploading to GitHub, object storage, ticketing, chat, or an AI service;
- never paste a raw secret-finding report into a public issue.

## Validation and manifest

Every evidence bundle should include a manifest similar to:

```json
{
  "schema_version": 1,
  "target": {
    "type": "repo",
    "identity": "commit SHA or digest"
  },
  "scanner": {
    "version": "runtime output",
    "identity": "executable SHA-256, image digest, or action SHA"
  },
  "configuration_sha256": "...",
  "data_sources": {
    "vulnerability_db": "metadata",
    "java_db": "metadata",
    "checks_bundle": "identity",
    "vex": []
  },
  "command_redacted": ["trivy", "repo", "--format", "json", "..."],
  "exit_code": 0,
  "coverage_warnings": [],
  "artifacts": [
    {
      "path": "trivy.json",
      "media_type": "application/json",
      "bytes": 0,
      "sha256": "...",
      "parse_status": "pass"
    }
  ]
}
```

Validate:

- expected files exist and are non-empty;
- JSON/SARIF/SBOM/XML parses in the intended parser;
- hashes match after transfer;
- canonical and derived counts reconcile;
- scanner/target/config/data identities are complete;
- warnings and stderr are retained;
- policy status is based on the intended result, not the last command in a shell pipeline.

## Finding identity and deduplication

Do not deduplicate solely by vulnerability ID or rule ID. A practical stable key includes:

- target immutable identity;
- result class/type and target path;
- scanner finding identifier;
- package name, installed version, PURL, or IaC/secret location as applicable;
- image layer/digest when relevant;
- configuration/suppression/VEX context.

Keep severity source and current severity as attributes, not identity. When merging parallel scans, preserve provenance from every source and flag conflicting records rather than silently choosing one.

## Publication boundaries

The following are external writes and require an authorized destination and identity:

- SARIF upload;
- dependency snapshot submission;
- OCI artifact/SBOM/attestation push;
- transparency-log entry;
- ticket, comment, pull request, release, or chat message;
- cloud security-finding import;
- artifact upload outside the controlled runner.

Preview the exact files and metadata first. Confirm repository/account/project, visibility, retention, token scope, and whether the action can overwrite or close existing remote findings.
