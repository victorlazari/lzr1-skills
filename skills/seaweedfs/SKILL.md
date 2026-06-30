---
name: seaweedfs
description: Comprehensive skill for managing, configuring, and troubleshooting SeaweedFS, a high-performance distributed object store and file system.
---

# SeaweedFS Skill

## When to Use

Use this skill when interacting with SeaweedFS deployments, including:
- Configuring Master, Volume, and Filer servers.
- Setting up Cloud Drive and tiered storage architectures.
- Implementing Erasure Coding for warm storage.
- Configuring advanced Filer setups (Active-Active sync, CDC, key-large-value store).
- Managing S3 API features (Object Lock, Versioning, Iceberg integration).
- Integrating with Hadoop and big data ecosystems (Spark, Trino).
- Setting up Seaweed Message Queue (SMQ) and PostgreSQL-compatible server (weed db).
- Troubleshooting cluster issues, performance tuning, and volume management.
- Implementing security best practices (TLS/mTLS, FIPS, IAM).

## Sub-Agent Spawning

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

## Workflow

1. **Assessment & Planning**: Identify the SeaweedFS components involved (Master, Volume, Filer, S3 API) and the specific goal (e.g., deployment, tuning, troubleshooting).
2. **Configuration**: Apply appropriate configurations using CLI commands (`weed master`, `weed volume`, `weed filer`) or configuration files (YAML/JSON).
3. **Validation**: Verify the configuration using health checks, `fs.verify`, and monitoring endpoints.
4. **Optimization**: Tune performance parameters (e.g., FUSE mount options, volume index memory, replication strategies).
5. **Troubleshooting**: Diagnose issues using logs, metrics, and specific commands (e.g., `volume.vacuum`, `volume.fix.replication`).
6. **Security Hardening**: Implement TLS/mTLS, configure firewalls, and audit access controls.

## Core Principles

- **O(1) Disk Access**: Leverage SeaweedFS's flat namespace and file ID (fid) system for near-constant time retrieval.
- **Separation of Concerns**: Understand the distinct roles of Master (metadata/topology), Volume (data storage), and Filer (hierarchical namespace/S3 API).
- **Scalability & Simplicity**: Utilize SeaweedFS's lightweight architecture for seamless horizontal scaling.
- **Fault Tolerance**: Implement appropriate replication strategies (e.g., `001`, `010`, `110`) and Erasure Coding for data durability.
- **Security First**: Always enforce TLS/mTLS, strong authentication, and least privilege access, especially in public or multi-tenant deployments.

## Key References

- **SeaweedFS GitHub Repository**: [https://github.com/chrislusf/seaweedfs](https://github.com/chrislusf/seaweedfs)
- **SeaweedFS Documentation**: [https://seaweedfs.com](https://seaweedfs.com)
- **Haystack Paper**: [https://research.facebook.com/publications/haystack-a-scalable-indexing-system-for-objects-at-facebook/](https://research.facebook.com/publications/haystack-a-scalable-indexing-system-for-objects-at-facebook/)
- **F4 Paper**: [https://research.google/pubs/pub38149/](https://research.google/pubs/pub38149/)
- **Raft Consensus Algorithm**: [https://raft.github.io/](https://raft.github.io/)

---

## Adversarial Verification Panel

For each significant cluster configuration issues, security vulnerabilities, volume errors, and migration outcomes produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong cluster configuration issues, security vulnerabilities, volume errors, and migration outcomes from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Cluster Configurator, Volume Diagnostics Agent, Security Auditor, Data Migration Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Auditor recommending TLS enforcement while Cluster Configurator sets a no-auth internal replication path)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified cluster health and action report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
