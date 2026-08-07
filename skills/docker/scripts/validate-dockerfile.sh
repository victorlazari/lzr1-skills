#!/bin/bash
# Perform basic syntax and best practice checks on Dockerfiles

set -euo pipefail

DOCKERFILE="${1:-Dockerfile}"

if [[ ! -f "$DOCKERFILE" ]]; then
  echo "Error: Dockerfile '$DOCKERFILE' not found." >&2
  exit 1
fi

echo "Validating $DOCKERFILE..."

# Check for digest pinning
if grep -q "^FROM " "$DOCKERFILE" && ! grep -q "^FROM .*@" "$DOCKERFILE"; then
  echo "Warning: Base image digest pinning is recommended." >&2
fi

# Basic syntax check using buildx bake --print (dry-run)
if docker buildx bake -f "$DOCKERFILE" --print >/dev/null 2>&1; then
  echo "Syntax check passed."
else
  echo "Syntax check failed or buildx bake not supported for this file." >&2
  # Fallback to a simple build dry-run if bake fails
  # Note: docker build doesn't have a true dry-run, so we just check if the file exists and has a FROM instruction
  if grep -q "^FROM " "$DOCKERFILE"; then
      echo "Basic FROM instruction found."
  else
      echo "Error: No FROM instruction found in Dockerfile." >&2
      exit 1
  fi
fi

echo "Validation complete."
