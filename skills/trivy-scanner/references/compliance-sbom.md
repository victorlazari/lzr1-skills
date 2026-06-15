# Compliance Reports and SBOM Generation

## Table of Contents

- [SBOM Generation](#sbom-generation)
- [CycloneDX Format](#cyclonedx-format)
- [SPDX Format](#spdx-format)
- [Scanning an Existing SBOM](#scanning-an-existing-sbom)
- [Compliance Reports](#compliance-reports)
- [Docker Compliance](#docker-compliance)
- [Kubernetes Compliance](#kubernetes-compliance)
- [Custom Compliance Specs](#custom-compliance-specs)

## SBOM Generation

Trivy can generate Software Bill of Materials (SBOM) in two industry-standard formats: CycloneDX and SPDX.

### When to Generate SBOMs

- Supply chain security requirements
- Regulatory compliance (Executive Order 14028, EU CRA)
- Software composition analysis
- Dependency tracking and inventory management
- Vulnerability management workflows

## CycloneDX Format

CycloneDX is ideal for security workflows and vulnerability management.

```bash
# Generate CycloneDX SBOM for a repository
trivy repo --format cyclonedx --output sbom.cdx.json ./

# Generate CycloneDX with vulnerabilities included (Bill of Vulnerabilities)
trivy repo --format cyclonedx --scanners vuln --output sbom-with-vulns.cdx.json ./

# Generate for a filesystem path
trivy fs --format cyclonedx --output sbom.cdx.json /path/to/project
```

### CycloneDX Output Structure

The output includes:
- `bomFormat`: "CycloneDX"
- `specVersion`: "1.3" or later
- `metadata`: Tool info, timestamp, main component
- `components`: All detected packages with PURLs, licenses, and properties
- `dependencies`: Dependency relationships between components
- `vulnerabilities`: (Only when `--scanners vuln` is specified)

## SPDX Format

SPDX is preferred for license compliance and is the ISO/IEC 5962:2021 standard.

```bash
# Generate SPDX JSON
trivy repo --format spdx-json --output sbom.spdx.json ./

# Generate SPDX tag-value format
trivy repo --format spdx --output sbom.spdx ./
```

### Supported SPDX Output Formats

| Format Flag | Description | File Extension |
|-------------|-------------|----------------|
| `spdx-json` | SPDX in JSON format | `.spdx.json` |
| `spdx` | SPDX tag-value format | `.spdx` |

## Scanning an Existing SBOM

Trivy can scan previously generated SBOMs for vulnerabilities:

```bash
# Scan a CycloneDX SBOM
trivy sbom ./sbom.cdx.json

# Scan an SPDX SBOM
trivy sbom ./sbom.spdx.json

# Scan with severity filter
trivy sbom --severity HIGH,CRITICAL ./sbom.cdx.json
```

This is useful for:
- Re-scanning SBOMs against updated vulnerability databases
- Scanning third-party SBOMs provided by vendors
- Continuous monitoring without re-analyzing source code

## Compliance Reports

Trivy can generate reports against industry compliance frameworks using the `--compliance` flag.

### Usage

```bash
trivy image --compliance <compliance_id> <image>
trivy k8s --compliance <compliance_id> cluster
```

### Report Options

| Flag | Effect |
|------|--------|
| `--report summary` | Shows pass/fail count per control |
| `--report all` | Shows full details with failure reasons |
| `--format table` | Human-readable table output |
| `--format json` | Machine-readable JSON output |

## Docker Compliance

### Available Docker Compliance IDs

| ID | Description |
|----|-------------|
| `docker-cis-1.6.0` | CIS Docker Benchmark v1.6.0 |

```bash
# Run Docker CIS benchmark against an image
trivy image --compliance docker-cis-1.6.0 --report summary myimage:latest
trivy image --compliance docker-cis-1.6.0 --report all --format json myimage:latest
```

## Kubernetes Compliance

### Available Kubernetes Compliance IDs

| ID | Description |
|----|-------------|
| `k8s-cis-1.23` | CIS Kubernetes Benchmark v1.23 |
| `k8s-nsa` | NSA/CISA Kubernetes Hardening Guide |
| `k8s-pss-baseline` | Pod Security Standards - Baseline |
| `k8s-pss-restricted` | Pod Security Standards - Restricted |
| `eks-cis-1.4` | CIS Amazon EKS Benchmark v1.4 |
| `aks-cis-1.4` | CIS Azure Kubernetes Service Benchmark v1.4 |
| `gke-cis-1.4` | CIS Google Kubernetes Engine Benchmark v1.4 |
| `rke2-cis-1.24` | CIS RKE2 Benchmark v1.24 |

```bash
# Run Kubernetes NSA compliance
trivy k8s --compliance k8s-nsa --report summary cluster

# Run CIS benchmark with full details
trivy k8s --compliance k8s-cis-1.23 --report all --format json cluster
```

## Custom Compliance Specs

Create custom compliance reports by defining a YAML specification:

```yaml
---
spec:
  id: my-org-policy
  title: My Organization Security Policy
  description: Internal security requirements
  platform: docker
  type: cis
  version: "1.0"
  controls:
    - id: 1.1
      name: Ensure non-root user is specified
      description: Containers should not run as root
      checks:
        - id: AVD-DS-0002
      severity: HIGH

    - id: 1.2
      name: Ensure HEALTHCHECK is defined
      description: Docker images should include a HEALTHCHECK
      checks:
        - id: AVD-DS-0026
      severity: MEDIUM
```

```bash
# Use custom compliance spec
trivy image --compliance @./my-compliance.yaml --report summary myimage:latest
```

### Compliance ID Naming Convention

Format: `{platform}-{type}-{version}`

- **Platform**: k8s, eks, aks, gke, rke2, ocp, docker, aws
- **Type**: cis, nsa, pss
- **Version**: Benchmark version number
