# Compose Patterns

## Overview
This reference covers advanced Compose patterns, multi-environment setups, and Compose Specification features.

## Multi-Environment Setups
Use multiple Compose files to manage different environments (e.g., development, testing, production).
- Base configuration: `docker-compose.yml`
- Environment-specific overrides: `docker-compose.override.yml` (default for dev), `docker-compose.prod.yml`

Command example:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Compose Specification Features
- **Profiles:** Group services into profiles to selectively start them.
- **Depends On:** Define startup and shutdown dependencies between services.
- **Healthchecks:** Define health checks to ensure services are ready before dependents start.

## Validation
Always validate Compose files before deployment:
```bash
docker compose config
```

## Authoritative Source
- Compose Specification: https://compose-spec.io/
Verified against upstream: 2026-08-07.
