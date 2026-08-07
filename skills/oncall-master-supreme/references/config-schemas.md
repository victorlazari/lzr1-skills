# Configuration Schemas Guide

Verified against upstream: 2026-08-07

## Overview

This guide describes the JSON schemas used for configuring notifications, escalations, users, and integrations in the on-call system.

## Schema Definitions

### User Schema

Defines a user in the on-call system.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string", "format": "email" },
    "role": { "type": "string", "enum": ["admin", "user", "responder"] }
  },
  "required": ["id", "name", "email", "role"]
}
```

### Escalation Policy Schema

Defines an escalation policy.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "delay_minutes": { "type": "integer" },
          "targets": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": { "type": "string" },
                "type": { "type": "string", "enum": ["user", "schedule"] }
              },
              "required": ["id", "type"]
            }
          }
        },
        "required": ["delay_minutes", "targets"]
      }
    }
  },
  "required": ["id", "name", "rules"]
}
```

## Validation

Use the `scripts/validate-config.sh` script to validate configuration files against these schemas before applying them.
