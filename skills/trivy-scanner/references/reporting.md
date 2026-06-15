# Reporting Formats and Output Options

## Table of Contents

- [Supported Formats](#supported-formats)
- [Table Format (Default)](#table-format)
- [JSON Format](#json-format)
- [SARIF Format](#sarif-format)
- [Template Format](#template-format)
- [GitHub Dependency Snapshot](#github-dependency-snapshot)
- [Output Destinations](#output-destinations)
- [Combining Multiple Reports](#combining-multiple-reports)

## Supported Formats

| Format | Flag | Vuln | Misconfig | Secret | License | Use Case |
|--------|------|------|-----------|--------|---------|----------|
| Table | `--format table` | ✓ | ✓ | ✓ | ✓ | Human review |
| JSON | `--format json` | ✓ | ✓ | ✓ | ✓ | Programmatic analysis |
| SARIF | `--format sarif` | ✓ | ✓ | ✓ | ✗ | IDE/GitHub integration |
| Template | `--format template` | ✓ | ✓ | ✓ | ✓ | Custom reports |
| CycloneDX | `--format cyclonedx` | ✓ | ✗ | ✗ | ✓ | SBOM (security) |
| SPDX JSON | `--format spdx-json` | ✗ | ✗ | ✗ | ✓ | SBOM (compliance) |
| SPDX | `--format spdx` | ✗ | ✗ | ✗ | ✓ | SBOM (tag-value) |
| GitHub | `--format github` | ✓ | ✗ | ✗ | ✗ | Dependency graph |

## Table Format

Default human-readable output. Best for terminal review and quick assessments.

```bash
trivy repo --format table ./
trivy repo -f table ./  # short form
```

Features:
- Color-coded severity levels
- Summary statistics per target
- Truncated long values for readability
- Report summary table at the top

## JSON Format

Machine-readable structured output. Best for programmatic analysis, dashboards, and integrations.

```bash
trivy repo --format json --output results.json ./
```

### JSON Structure

```json
{
  "SchemaVersion": 2,
  "CreatedAt": "2024-01-01T00:00:00Z",
  "ArtifactName": "./",
  "ArtifactType": "repository",
  "Metadata": {
    "RepoURL": "https://github.com/user/repo",
    "Branch": "main",
    "Commit": "abc123..."
  },
  "Results": [
    {
      "Target": "package-lock.json",
      "Class": "lang-pkgs",
      "Type": "npm",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2023-1234",
          "PkgName": "lodash",
          "InstalledVersion": "4.17.20",
          "FixedVersion": "4.17.21",
          "Severity": "HIGH",
          "Title": "Prototype Pollution",
          "Description": "...",
          "References": ["https://..."],
          "CVSS": { ... }
        }
      ],
      "Misconfigurations": [ ... ],
      "Secrets": [ ... ]
    }
  ]
}
```

### Parsing JSON Results with Python

```python
import json

with open("results.json") as f:
    data = json.load(f)

# Count findings by severity
severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        sev = vuln.get("Severity", "UNKNOWN")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

# Extract all fixable vulnerabilities
fixable = []
for result in data.get("Results", []):
    for vuln in result.get("Vulnerabilities", []):
        if vuln.get("FixedVersion"):
            fixable.append({
                "id": vuln["VulnerabilityID"],
                "pkg": vuln["PkgName"],
                "installed": vuln["InstalledVersion"],
                "fixed": vuln["FixedVersion"],
                "severity": vuln["Severity"]
            })
```

### Parsing JSON Results with jq

```bash
# Count total vulnerabilities
jq '[.Results[].Vulnerabilities // [] | length] | add' results.json

# List all CRITICAL CVEs
jq -r '.Results[].Vulnerabilities[]? | select(.Severity == "CRITICAL") | .VulnerabilityID' results.json

# Get fixable vulnerabilities
jq -r '.Results[].Vulnerabilities[]? | select(.FixedVersion != "") | "\(.VulnerabilityID) \(.PkgName) \(.InstalledVersion) -> \(.FixedVersion)"' results.json

# Count by severity
jq -r '[.Results[].Vulnerabilities[]?.Severity] | group_by(.) | map({(.[0]): length}) | add' results.json
```

## SARIF Format

Static Analysis Results Interchange Format. Best for GitHub Code Scanning, VS Code, and other SARIF-compatible tools.

```bash
trivy repo --format sarif --output results.sarif ./
```

### GitHub Code Scanning Integration

Upload SARIF to GitHub Code Scanning in a GitHub Action:

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'repo'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy scan results to GitHub Security tab
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

## Template Format

Custom output using Go templates. Best for generating custom reports (HTML, CSV, Markdown, etc.).

```bash
# Use a built-in template
trivy repo --format template --template "@contrib/html.tpl" --output report.html ./

# Use a custom template file
trivy repo --format template --template "@/path/to/my-template.tpl" --output report.md ./
```

### Built-in Templates

Trivy ships with several contrib templates:
- `contrib/html.tpl` - HTML vulnerability report
- `contrib/gitlab.tpl` - GitLab dependency scanning format
- `contrib/junit.tpl` - JUnit XML format for CI systems
- `contrib/asff.tpl` - AWS Security Finding Format

### Custom Template Example (Markdown)

```go
{{- range . }}
## {{ .Target }}
{{ if .Vulnerabilities }}
| ID | Package | Severity | Installed | Fixed |
|----|---------|----------|-----------|-------|
{{- range .Vulnerabilities }}
| {{ .VulnerabilityID }} | {{ .PkgName }} | {{ .Severity }} | {{ .InstalledVersion }} | {{ .FixedVersion }} |
{{- end }}
{{ end }}
{{- end }}
```

## GitHub Dependency Snapshot

Generate a snapshot compatible with GitHub's Dependency Submission API:

```bash
trivy repo --format github --output snapshot.json ./
```

This integrates with GitHub's dependency graph and Dependabot alerts.

## Output Destinations

### File Output

```bash
# Write to a specific file
trivy repo --output /path/to/report.json --format json ./
```

### Standard Output (Default)

```bash
# Print to stdout (default)
trivy repo --format json ./
```

### Multiple Outputs (Requires Multiple Runs)

Trivy only supports one format/output per run. For multiple formats, run separate commands:

```bash
# Generate table for review + JSON for processing + SARIF for GitHub
trivy repo --format table --output report.txt ./
trivy repo --format json --output report.json ./
trivy repo --format sarif --output report.sarif ./
```

## Combining Multiple Reports

### Dependency Tree View

Show the dependency tree to understand transitive vulnerabilities:

```bash
trivy repo --dependency-tree ./
```

### List All Packages

Show all detected packages regardless of vulnerabilities:

```bash
trivy repo --list-all-pkgs --format json ./
```

This is useful for complete software inventory even when no vulnerabilities are found.
