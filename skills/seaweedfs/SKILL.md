---
name: seaweedfs
description: Manage, configure, and troubleshoot SeaweedFS deployments, including Kubernetes operator and CSI driver setups.
---

# SeaweedFS Skill

## Scope and Triggers

Use this skill when interacting with SeaweedFS deployments, including:
- Configuring Master, Volume, and Filer servers.
- Deploying SeaweedFS on Kubernetes using the official operator and CSI driver.
- Setting up Cloud Drive and tiered storage architectures.
- Implementing Erasure Coding for warm storage.
- Configuring advanced Filer setups (Active-Active sync, CDC, key-large-value store).
- Managing S3 API features (Object Lock, Versioning, Iceberg integration).
- Integrating with Hadoop and big data ecosystems (Spark, Trino).
- Setting up Seaweed Message Queue (SMQ) and PostgreSQL-compatible server (weed db).
- Troubleshooting cluster issues, performance tuning, and volume management.
- Implementing security best practices (TLS/mTLS, FIPS, IAM).

## Preconditions

- Identify the deployment environment (bare metal, Kubernetes, etc.).
- Verify access to the target cluster or servers.
- Ensure required tools (e.g., `kubectl`, `weed` CLI) are installed and accessible.

## Source Freshness

- Verify commands and configurations against the latest official documentation at [seaweedfs/seaweedfs](https://github.com/seaweedfs/seaweedfs) and [seaweedfs.com](https://seaweedfs.com).
- Consult `references/official-docs.md` for verified links.

## Workflow

1. **Assessment & Planning**: Identify the SeaweedFS components involved (Master, Volume, Filer, S3 API) and the specific goal (e.g., deployment, tuning, troubleshooting).
2. **Configuration**: Apply appropriate configurations using CLI commands (`weed master`, `weed volume`, `weed filer`), configuration files (YAML/JSON), or Kubernetes Operator.
3. **Validation**: Verify the configuration using health checks, `fs.verify`, monitoring endpoints, and `scripts/verify-cluster-health.sh`.
4. **Optimization**: Tune performance parameters based on the deployment type.
5. **Troubleshooting**: Diagnose issues using logs, metrics, and specific commands (e.g., `volume.vacuum`, `volume.fix.replication`).
6. **Security Hardening**: Implement TLS/mTLS, configure firewalls, and audit access controls.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- Do not execute untrusted artifacts.

## Validation

- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.
- Run `scripts/verify-cluster-health.sh` to validate cluster health.

## Failure Handling

- Diagnose errors using logs and metrics.
- Choose alternatives or roll back if a configuration fails.
- Do not repeat a failed action unchanged.

## Output Contract

- Provide a structured report of actions taken, evidence of success, and actionable next steps.
- Include severity/confidence levels for findings.

## Resources

- `references/complete-reference.md`: Detailed reference on SeaweedFS architecture, components, and configurations.
- `references/official-docs.md`: Verified links to official documentation and resources.
- `scripts/verify-cluster-health.sh`: Script to verify the health of the SeaweedFS cluster.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple clusters to configure | Cluster Configurator | Parallel configuration of Master, Volume, and Filer servers across clusters |
| Bulk volume troubleshooting | Volume Diagnostics Agent | Parallel investigation of volume issues (e.g., "No Free Volumes Left") |
| Multiple environments to audit | Security Auditor | Parallel security review (TLS, mTLS, FIPS, IAM) of each environment |
| Large-scale data migration | Data Migration Agent | Parallel data transfer and tiered storage setup |

### Spawning Rules
- Spawn when 3+ independent items (clusters, volumes, environments) need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

### Cross-System Consistency Validator

After all parallel agents complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

### Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified cluster health and action report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
