# Oncall-Master-Supreme CLI Command Reference

Verified against upstream: 2026-08-07

## Overview

The `oncall-master-supreme` CLI provides a command-line interface for managing incidents, schedules, and configurations.

## Global Options

-   `--config <path>`: Path to the configuration file.
-   `--dry-run`: Simulate the command without making any changes.
-   `--format <json|text>`: Output format.

## Commands

### Incident Management

-   `oncall-master-supreme incident list [--status <open|resolved>]`: List incidents.
-   `oncall-master-supreme incident get <id>`: Get details for a specific incident.
-   `oncall-master-supreme incident resolve <id>`: Resolve an incident (requires confirmation).

### Schedule Management

-   `oncall-master-supreme schedule list`: List all schedules.
-   `oncall-master-supreme schedule override <id> --user <user_id> --start <time> --end <time>`: Create a schedule override (requires confirmation).

### Configuration Management

-   `oncall-master-supreme config validate <path>`: Validate a configuration file against the schema.
-   `oncall-master-supreme config apply <path>`: Apply a configuration file (supports `--dry-run`).

## Examples

```bash
# List open incidents
oncall-master-supreme incident list --status open

# Validate a configuration file
oncall-master-supreme config validate ./config.json

# Apply a configuration file with a dry run
oncall-master-supreme config apply ./config.json --dry-run
```
