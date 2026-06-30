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

---

## Parallel Execution Protocol

> **All 4 agents launch simultaneously.** Do not wait for one to finish before starting the next. Each agent receives the full task context and its dedicated reference file only.

### Agent Roster

| Agent | Dimension | Scope | Reference |
|---|---|---|---|
| **Vulnerability Agent** | CVE Scanning | OS packages, language dependencies, and application libraries against NVD/CVE databases | `references/filtering.md` |
| **Misconfig Agent** | Misconfiguration Scanning | Dockerfile, Kubernetes manifests, Terraform, and cloud config security misconfigurations | `references/compliance-sbom.md` |
| **Secret Agent** | Secret Detection | Hardcoded credentials, tokens, and private keys embedded in source or container layers | `references/filtering.md` |
| **License Agent** | License Compliance | SBOM generation, license compatibility analysis, copyleft risk assessment | `references/compliance-sbom.md` |

### Spawning Rules

- **Trigger**: Every invocation of this skill — no exceptions
- **Concurrency**: All 4 agents launch in a single `parallel()` call
- **Context per agent**: Full task input + its dedicated reference file only (no cross-agent sharing during analysis)
- **Maximum concurrent agents**: 4

### Synthesis Agent

After all 4 agents report, run one **Synthesis Agent** with all reports that:

1. **Cross-references** findings across dimensions for interaction effects that no single agent could see
2. **Deduplicates** overlapping findings (same issue detected by multiple agents → one canonical entry)
3. **Prioritizes** the merged set by severity/impact
4. **Produces** a single unified output document

> Synthesis note for this skill: Merge all scan types into a single severity-ranked SBOM. Flag CVEs whose affected packages also have license compliance issues. Map misconfigurations to the CVEs they expose.

### Quality Gate

A finding from one agent that **contradicts** a finding from another agent must be flagged as `CONFLICT` and passed to the Synthesis Agent as a `MUST_RESOLVE` item — never silently dropped.
