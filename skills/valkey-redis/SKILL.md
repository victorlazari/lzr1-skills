---
name: valkey-redis
description: Specialist skill for architecting, deploying, troubleshooting, and securing highly optimized Redis environments integrated with ValKey.
---

# ValKey-Redis Specialist Skill

## When to Use

Use this skill when you need to architect, deploy, troubleshoot, or secure Redis environments that are integrated with ValKey. ValKey is a key management system that provides granular key-level access control, encryption at rest, and real-time auditing for Redis. This skill is essential for handling demanding production environments, resolving intricate issues, and designing scalable, secure data architectures that meet enterprise-grade security and compliance requirements.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Redis nodes to troubleshoot | Node Troubleshooter | Parallel investigation of latency, throughput, or connectivity issues across nodes |
| Multiple ValKey policies to validate | Policy Validator | Parallel validation of RBAC policies and key access rules |
| Multiple keys to encrypt/decrypt | Crypto Agent | Parallel batch encryption or decryption operations |
| Multiple tenants to isolate | Tenant Configurator | Parallel configuration of multi-tenant isolation settings |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Validate Connectivity and Authentication**: Ensure Redis clients can authenticate and communicate with Redis and ValKey services using TLS certificates and access tokens.
2. **Analyze Logs and Metrics**: Inspect Redis logs and ValKey audit logs for permission denials, encryption errors, and latency spikes.
3. **Inspect Key Policies and Permissions**: Dump and review current ValKey key policies to identify conflicting or overly restrictive rules.
4. **Verify Data Integrity**: Dump key data from Redis and test decryption with ValKey tools to ensure data consistency.
5. **Test Failover and Replication**: Simulate node failures to verify ValKey policy consistency across the Redis cluster.
6. **Scale and Optimize**: Implement appropriate architecture patterns (e.g., Sharded Redis Cluster, Proxy-based Access Layer) and optimize ValKey policy propagation and encryption overhead.
7. **Secure the Environment**: Harden Redis configurations, enforce strict ValKey RBAC policies, and automate encryption key rotation.

## Core Principles

- **Security First**: Always enforce encryption at rest, RBAC, audit logging, and TLS encryption to protect sensitive data.
- **High Availability**: Ensure ValKey policies are consistently propagated across all Redis nodes to maintain availability during failovers.
- **Performance Optimization**: Minimize encryption overhead by using hardware acceleration and batch operations, and employ connection pooling to reduce handshake latency.
- **Granular Access Control**: Define strict, least-privilege policies for key access based on user roles.
- **Proactive Monitoring**: Continuously monitor CPU, memory, network IO, and latency metrics to detect and resolve bottlenecks early.

## Key References

- Redis Official Documentation: https://redis.io/docs/
- ValKey Security Framework: https://valkey.io/docs/
- Redis Cluster and Sentinel Architecture: https://redis.io/docs/manual/scaling/
- Advanced Redis Security Practices: https://redis.io/docs/manual/security/
- Lua Scripting in Redis: https://redis.io/docs/manual/programmability/eval-intro/
