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
