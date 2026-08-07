#!/bin/bash
# Validate Compose files against the latest Compose Specification

set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.yml}"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Error: Compose file '$COMPOSE_FILE' not found." >&2
  exit 1
fi

echo "Validating $COMPOSE_FILE..."
if docker compose -f "$COMPOSE_FILE" config >/dev/null; then
  echo "Validation successful."
else
  echo "Validation failed." >&2
  exit 1
fi
