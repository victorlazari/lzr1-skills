---
name: database
description: A comprehensive skill for database specialists covering architecture, indexing, query optimization, replication, and security for PostgreSQL and MongoDB. Triggers when advanced database operations, architecture design, performance tuning, or security audits are required.
---

# Database Specialist Skill

## Scope and Triggers
Use this skill when you need to perform advanced database operations, architecture design, performance tuning, or security audits. It is particularly suited for tasks involving PostgreSQL (16/17) and MongoDB (7.0/8.0), including:
- Designing and evaluating database architectures for relational and NoSQL systems.
- Implementing and optimizing indexing strategies to improve query performance.
- Configuring and managing replication, high availability, and disaster recovery.
- Conducting comprehensive database security audits and implementing hardening strategies.
- Managing database configurations, connection pooling, and resource allocation.

Explicit non-goals: This skill does not cover general application development or frontend integration.

## Preconditions
Before acting, detect the target database, environment, versions, permissions, inputs, constraints, and user intent.
- Verify the target database version (PostgreSQL 16/17 or MongoDB 7.0/8.0).
- Ensure appropriate permissions are granted for the intended operations.
- Identify the specific task requirements (e.g., performance tuning, security audit).

## Source Freshness
Volatile facts, such as supported versions and features, must be checked against the official documentation at runtime or verified against a specific date.
- PostgreSQL Official Documentation: https://www.postgresql.org/docs/
- MongoDB Official Documentation: https://www.mongodb.com/docs/
- MongoDB Atlas Database: https://www.mongodb.com/products/platform/atlas-database
- AWS MongoDB vs PostgreSQL Comparison: https://aws.amazon.com/compare/the-difference-between-mongodb-and-postgresql/

## Workflow
1. **Requirement Analysis**: Understand the specific database task, whether it involves architecture design, performance tuning, security auditing, or configuration management.
2. **Architecture Evaluation**: Assess the current database architecture and identify areas for improvement or scaling.
3. **Performance Tuning**: Analyze query execution plans, evaluate indexing strategies, and optimize configurations.
4. **Security Assessment**: Conduct a thorough security audit covering authentication, authorization, encryption, network security, and vulnerability management.
5. **Implementation and Testing**: Apply the necessary changes and rigorously test the outcomes.
6. **Documentation and Review**: Document all changes, configurations, and audit findings.

Stop conditions: The task is completed, or a critical error occurs that requires user intervention.

## Safety
- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- Do not execute untrusted artifacts.

## Validation
- Verify that all proposed indexes are supported by the target database version.
- Ensure that replication configurations are tested in a staging environment before production deployment.
- Validate security configurations against the latest CIS benchmarks.
- Perform dry runs of data migrations to identify potential bottlenecks.

## Failure Handling
- If an operation fails, diagnose the error using logs and error messages.
- Choose alternative approaches or roll back changes if necessary.
- Do not repeat a failed action unchanged.

## Output Contract
The result must include:
- A structured summary of the operations performed.
- Evidence of validation and testing.
- Severity/confidence levels for any findings.
- Actionable next steps.

## Resources
- [PostgreSQL Reference](references/postgresql-reference.md): Focused reference for PostgreSQL architecture, indexing, query optimization, replication, and security.
- [MongoDB Reference](references/mongodb-reference.md): Focused reference for MongoDB architecture, indexing, query optimization, replication, and security.
- [Source Map](references/source-map.md): Focused source map replacing the speculative reading list.
- [Validate Indexes Script](scripts/validate-indexes.sh): Script to verify that proposed indexes are supported by the target database version.
- [Test Replication Script](scripts/test-replication.sh): Script to test replication configurations in a staging environment.
- [Validate Security Script](scripts/validate-security.sh): Script to validate security configurations against the latest CIS benchmarks.
- [Dry Run Migration Script](scripts/dry-run-migration.sh): Script to perform dry runs of data migrations.

## Orchestration
This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.
