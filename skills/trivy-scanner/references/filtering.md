# Filtering and Ignoring Findings

## Table of Contents

- [Severity Filtering](#severity-filtering)
- [Status Filtering](#status-filtering)
- [Ignore Files (.trivyignore)](#ignore-files)
- [YAML Ignore Format (.trivyignore.yaml)](#yaml-ignore-format)
- [Rego-Based Filtering](#rego-based-filtering)
- [VEX-Based Suppression](#vex-based-suppression)
- [Skipping Files and Directories](#skipping-files-and-directories)
- [Exit Codes for CI/CD](#exit-codes-for-cicd)

## Severity Filtering

Filter results by severity level using `--severity`:

```bash
# Only show HIGH and CRITICAL findings
trivy repo --severity HIGH,CRITICAL ./

# Show all severities (default behavior)
trivy repo --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL ./
```

Supported severity levels (from lowest to highest):
- `UNKNOWN` - Severity not yet assigned
- `LOW` - Minor issues with minimal impact
- `MEDIUM` - Moderate issues that should be addressed
- `HIGH` - Serious issues requiring prompt attention
- `CRITICAL` - Severe issues requiring immediate action

## Status Filtering

Filter vulnerabilities by their fix status using `--ignore-status`:

```bash
# Ignore vulnerabilities that have no fix available
trivy repo --ignore-status affected,will_not_fix ./

# Only show vulnerabilities with available fixes
trivy repo --ignore-status affected,will_not_fix,end_of_life ./
```

Supported statuses:
- `affected` - Package is affected, no fix available yet
- `fixed` - A fix is available
- `will_not_fix` - Vendor has decided not to fix
- `end_of_life` - Package is end-of-life

## Ignore Files

### Plain Format (.trivyignore)

Create a `.trivyignore` file in the repository root to suppress specific findings:

```
# Vulnerability IDs
CVE-2023-1234
CVE-2023-5678

# Misconfiguration IDs
AVD-DS-0002

# Secret rule IDs
generic-api-key

# With expiration date (finding reappears after this date)
CVE-2024-9999  # exp:2025-06-30
```

### Usage

```bash
# Use default .trivyignore in current directory
trivy repo ./

# Specify a custom ignore file
trivy repo --ignorefile /path/to/my-ignore-file ./
```

## YAML Ignore Format

The `.trivyignore.yaml` format provides richer metadata:

```yaml
vulnerabilities:
  - id: CVE-2023-1234
    paths:
      - "go.sum"
    reason: "Not exploitable in our usage context"
    expires: 2025-06-30

  - id: CVE-2023-5678
    reason: "Mitigated by network policy"

misconfigurations:
  - id: AVD-DS-0002
    paths:
      - "Dockerfile.dev"
    reason: "Development-only Dockerfile, not used in production"

secrets:
  - id: generic-api-key
    paths:
      - "tests/fixtures/**"
    reason: "Test fixtures with dummy keys"
```

### Key fields

| Field | Description | Required |
|-------|-------------|----------|
| `id` | Finding ID (CVE, AVD, rule ID) | Yes |
| `paths` | Glob patterns to limit suppression scope | No |
| `reason` | Justification for ignoring | No (recommended) |
| `expires` | Date after which finding reappears (YYYY-MM-DD) | No |

## Rego-Based Filtering

For complex filtering logic, use Rego policies with `--ignore-policy`:

```bash
trivy repo --ignore-policy policy.rego ./
```

Example `policy.rego`:

```rego
package trivy

import data.lib.trivy

# Ignore unfixed vulnerabilities
default ignore = false

ignore {
    input.PkgName == "linux-libc-dev"
}

ignore {
    # Ignore low severity in test directories
    input.Severity == "LOW"
    contains(input.PkgPath, "test")
}

ignore {
    # Ignore specific CWE
    input.CweIDs[_] == "CWE-400"
}
```

## VEX-Based Suppression

Vulnerability Exploitability eXchange (VEX) provides a standardized way to communicate vulnerability status:

```bash
# Use a local VEX file
trivy repo --vex ./vex.json ./

# Use VEX repository
trivy repo --vex repo ./
```

Example VEX document (OpenVEX format):

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://example.com/vex/12345",
  "author": "security-team@example.com",
  "timestamp": "2024-01-01T00:00:00Z",
  "statements": [
    {
      "vulnerability": {"name": "CVE-2023-1234"},
      "products": [{"@id": "pkg:golang/example.com/myapp"}],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path"
    }
  ]
}
```

## Skipping Files and Directories

Exclude specific paths from scanning:

```bash
# Skip directories
trivy repo --skip-dirs vendor,node_modules,test ./

# Skip specific files
trivy repo --skip-files "config/dummy-secret.yaml,tests/fixtures/key.pem" ./

# Combine both
trivy repo --skip-dirs vendor --skip-files "*.test.js" ./
```

Common directories to skip:
- `vendor/` - Vendored dependencies (already scanned via lock files)
- `node_modules/` - NPM packages (already scanned via package-lock.json)
- `test/`, `tests/`, `spec/` - Test directories with dummy credentials
- `.git/` - Git internals (skipped by default)

## Exit Codes for CI/CD

Control pipeline behavior with `--exit-code`:

```bash
# Exit with code 1 if any vulnerability is found (default: exit 0)
trivy repo --exit-code 1 ./

# Exit with code 1 only for HIGH/CRITICAL
trivy repo --exit-code 1 --severity HIGH,CRITICAL ./

# Separate exit codes for different scan types
trivy repo --scanners vuln --exit-code 1 --severity CRITICAL ./
trivy repo --scanners misconfig --exit-code 2 --severity HIGH,CRITICAL ./
```

### CI/CD Gate Strategy

```bash
# Soft gate: warn on MEDIUM, fail on HIGH/CRITICAL
trivy repo --severity HIGH,CRITICAL --exit-code 1 ./
RESULT=$?
if [ $RESULT -ne 0 ]; then
    echo "BLOCKING: Critical/High findings detected"
    exit 1
fi

# Informational: show all findings but never fail
trivy repo --exit-code 0 ./
```
