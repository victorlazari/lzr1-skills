---
name: database
description: A comprehensive skill for database specialists covering architecture, indexing, query optimization, replication, and security for PostgreSQL and MongoDB.
---

# Database Specialist Skill

## When to Use

Use this skill when you need to perform advanced database operations, architecture design, performance tuning, or security audits. It is particularly suited for tasks involving PostgreSQL and MongoDB, including:
- Designing and evaluating database architectures for relational and NoSQL systems.
- Implementing and optimizing indexing strategies to improve query performance.
- Analyzing and tuning complex queries using execution plans and caching strategies.
- Configuring and managing replication, high availability, and disaster recovery.
- Conducting comprehensive database security audits and implementing hardening strategies.
- Managing database configurations, connection pooling, and resource allocation.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple databases to audit | Security Auditor | Parallel security review of each database instance |
| Multiple queries to optimize | Query Optimizer | Parallel analysis and tuning of slow queries |
| Multiple nodes to configure | Config Validator | Parallel validation of database configurations across nodes |
| Bulk data migrations | Migration Agent | Parallel execution of data migration tasks |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis**: Understand the specific database task, whether it involves architecture design, performance tuning, security auditing, or configuration management.
2. **Architecture Evaluation**: Assess the current database architecture (e.g., PostgreSQL process model, MongoDB replica sets) and identify areas for improvement or scaling.
3. **Performance Tuning**: Analyze query execution plans, evaluate indexing strategies, and optimize configurations (e.g., connection pooling, memory allocation) to enhance performance.
4. **Security Assessment**: Conduct a thorough security audit covering authentication, authorization, encryption, network security, and vulnerability management.
5. **Implementation and Testing**: Apply the necessary changes, such as creating indexes, updating configurations, or enforcing security policies, and rigorously test the outcomes.
6. **Documentation and Review**: Document all changes, configurations, and audit findings, ensuring compliance with organizational standards and best practices.

## Core Principles

- **Data Integrity and Consistency**: Prioritize ACID compliance in relational databases and understand the trade-offs in NoSQL systems (e.g., CAP theorem, eventual consistency).
- **Performance by Design**: Incorporate performance considerations early in the design phase, focusing on appropriate indexing, query optimization, and efficient resource utilization.
- **Security First**: Implement a defense-in-depth approach, ensuring robust authentication, granular access controls, and comprehensive encryption for data at rest and in transit.
- **Scalability and High Availability**: Design systems that can scale horizontally or vertically and ensure high availability through robust replication and failover mechanisms.
- **Continuous Monitoring**: Establish proactive monitoring and alerting for database health, performance metrics, and security events to detect and resolve issues promptly.

## Key References

- [Complete Reference Guide](references/complete-reference.md): An exhaustive compilation of advanced topics, CLI commands, configuration schemas, and security checklists for PostgreSQL and MongoDB.
- [Reading List](references/reading-list.md): A curated collection of recent books and articles (2023-2026) covering advanced database concepts, performance tuning, and security.

---

## Adversarial Verification Panel

For each significant performance bottleneck and security vulnerability produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong performance bottlenecks and security vulnerabilities from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Security Auditor, Query Optimizer, Config Validator, Migration Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Config Validator recommending aggressive connection pool sizing while Query Optimizer recommends limiting concurrent connections to reduce lock contention)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified database assessment report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
