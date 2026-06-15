---
name: trivy-scanner
description: "Comprehensive security analysis for local and remote GitHub repositories using Trivy. Use for scanning repositories for vulnerabilities, misconfigurations, secrets, and licenses; generating SBOMs; applying compliance checks; filtering results; and generating security reports in various formats."
---

# Trivy Security Scanner

This skill provides a comprehensive workflow for performing security analysis on code repositories using Trivy.

## Overview

Trivy is a versatile security scanner that can analyze code repositories (both local and remote) for four main categories of security issues:
1. **Vulnerabilities** in OS packages and language-specific dependencies
2. **Misconfigurations** in Infrastructure as Code (IaC) files
3. **Exposed Secrets** like passwords, API keys, and tokens
4. **License Issues** based on organizational policies

## Core Workflow

Follow these steps when tasked with scanning a repository:

1. **Determine the target**: Identify if scanning a local path or a remote GitHub URL.
2. **Determine the scope**: Identify which scanners are needed (vuln, misconfig, secret, license).
3. **Configure the scan**: Set up severity filters, ignore rules, and output formats.
4. **Execute the scan**: Run the appropriate Trivy command.
5. **Process the results**: Generate reports or SBOMs as required.

### 1. Basic Repository Scanning

For a comprehensive scan of a repository including all security checks:

```bash
trivy repo --scanners vuln,misconfig,secret,license <target_path_or_url>
```

*Note: By default, `trivy repo` only enables `vuln` and `secret` scanners. You must explicitly add `misconfig` and `license` if needed.*

### 2. Advanced Scanning Options

Refer to the bundled reference files for specific use cases:

- **Filtering & Ignoring**: See [references/filtering.md](references/filtering.md) for handling false positives, using `.trivyignore`, and severity filtering.
- **Compliance & SBOMs**: See [references/compliance-sbom.md](references/compliance-sbom.md) for generating SBOMs (CycloneDX/SPDX) and running compliance reports (e.g., CIS benchmarks).
- **Reporting Formats**: See [references/reporting.md](references/reporting.md) for outputting results as JSON, SARIF, or using templates.

### 3. Using Helper Scripts

This skill includes helper scripts to automate complex workflows:

- **Comprehensive Scan**: Use `scripts/comprehensive_scan.sh` to run all scanners and generate multiple report formats simultaneously.
- **Setup Ignore File**: Use `scripts/setup_ignore.sh` to quickly create a `.trivyignore` or `.trivyignore.yaml` file based on a list of CVEs or finding IDs.

## Best Practices

1. **Always use `--scanners` explicitly** when a user asks for a "full" or "comprehensive" scan to ensure misconfigurations and licenses are included.
2. **Use `--format json`** when you need to programmatically analyze the results or extract specific data points.
3. **Check for `.trivyignore`** in the repository before scanning, as it might contain intentionally suppressed findings.
4. **For remote repositories**, you can specify branches, tags, or commits:
   `trivy repo --branch main https://github.com/user/repo`
5. **Full License Scanning**: If deep license analysis is required (scanning source code headers, not just package managers), add the `--license-full` flag. Note this takes significantly longer.
