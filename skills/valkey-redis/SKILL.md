---
name: valkey-redis
description: Specialist skill for managing Valkey (the open-source Redis fork), configuring valkey.conf, and executing safe migrations from Redis OSS to Valkey.
---

# Valkey Database Administration and Migration Skill

## Scope and Triggers

Use this skill when you need to architect, deploy, configure, troubleshoot, or secure Valkey databases, or when you need to migrate an existing Redis OSS deployment to Valkey. Valkey is an open-source, high-performance key-value data store that originated as a fork of Redis OSS 7.2.4.

**Non-goals:** Do not use this skill for managing legacy Redis deployments prior to 7.2.4 or Redis Enterprise. For those, route to the `redis-admin` skill. Do not treat Valkey as a "key management system" (KMS) for Redis; Valkey is the database itself.

## Preconditions

Before executing any operations, detect the target environment:
1. Identify existing Redis/Valkey instances, versions, and configurations.
2. Verify the installed version via the `INFO` command (look for `valkey_version`).
3. Ensure you have the necessary permissions to read configuration files (e.g., `valkey.conf`) and execute CLI commands (`valkey-cli`).
4. For migrations, confirm the source Redis version is compatible (Redis OSS 7.2 or earlier).

## Source Freshness

Valkey is actively developed. Always verify volatile facts against the official documentation.
- **Primary Source:** Valkey Documentation (https://valkey.io/docs/)
- **Migration Guide:** https://valkey.io/topics/migration/
- **Verified Date:** 2026-08-07

## Workflow

1. **Discover Environment:** Identify existing Redis/Valkey instances, versions, and configurations using `valkey-cli INFO` or `redis-cli INFO`.
2. **Pre-flight Check (Migration):** Run `scripts/migration-helper.sh` in dry-run mode to assess migration readiness.
3. **Plan Migration:** Determine the appropriate migration strategy (physical vs. replication) based on downtime tolerance and environment constraints.
4. **Execute Migration:** Perform the migration. **Explicit user confirmation is required** before initiating any data migration or failover.
5. **Validate:** Verify data integrity, client connectivity, and cluster health post-migration. Ensure `valkey-cli ping` succeeds.
6. **Stop Condition:** Migration is complete, `valkey-cli` reports healthy status, and clients are successfully connected to the new Valkey instance.

## Safety

- **Read-only Discovery:** Always perform read-only discovery (e.g., `INFO`, `CONFIG GET`) before attempting any mutations.
- **Confirmation Required:** You MUST require explicit user confirmation before executing destructive, external, privileged, or production-impacting actions, including data migration, failover, or service restarts.
- **Dry Runs:** Use dry-run modes for scripts where available.

## Validation

- **Syntax Checks:** Validate `valkey.conf` syntax before restarting services.
- **Postconditions:** Ensure `valkey-cli ping` returns `PONG` and `INFO` reports the expected `valkey_version` after deployment or migration.

## Failure Handling

- If a migration step fails, do not repeat the same action unchanged.
- Consult the logs (defined in `valkey.conf`) to diagnose errors.
- If replication fails, verify network connectivity and firewall rules between the source and target nodes.
- Rollback: If a migration cannot be completed, revert clients to the source Redis instance and ensure data consistency.

## Output Contract

The result must include:
- A summary of the actions performed (e.g., configuration updated, migration completed).
- Evidence of success (e.g., output of `valkey-cli ping` or `INFO`).
- Any warnings or non-critical issues encountered.
- Actionable next steps for the user (e.g., update client connection strings).

## Resources

- [Complete Reference](references/complete-reference.md): Detailed architecture, configuration, and CLI reference for Valkey.
- [Migration Helper Script](scripts/migration-helper.sh): Deterministic script to assist with migrating from Redis OSS to Valkey.

## Orchestration

Parallel work is generally not recommended for single-instance migrations to avoid race conditions. For cluster migrations, ensure operations on different shards are independent and synthesize the results to confirm overall cluster health.
