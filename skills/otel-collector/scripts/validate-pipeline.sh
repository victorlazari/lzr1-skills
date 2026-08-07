#!/bin/bash
# Validates that memory_limiter is the first processor and GOMEMLIMIT is set.

set -euo pipefail

CONFIG_FILE="${1:-}"

if [[ -z "$CONFIG_FILE" ]]; then
  echo "Usage: $0 <config.yaml>"
  exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Configuration file '$CONFIG_FILE' not found."
  exit 1
fi

# Check if GOMEMLIMIT is set in the environment
if [[ -z "${GOMEMLIMIT:-}" ]]; then
  echo "Warning: GOMEMLIMIT environment variable is not set. It is highly recommended to set it to ~80% of the container's hard memory limit."
fi

# Check if memory_limiter is the first processor in pipelines
# This is a basic check and might not catch all complex YAML structures,
# but it serves as a good smoke test.
if grep -q "pipelines:" "$CONFIG_FILE"; then
  # Extract the processors list for each pipeline and check the first item
  # A more robust check would require a YAML parser like yq
  if command -v yq >/dev/null 2>&1; then
    PIPELINES=$(yq e '.service.pipelines | keys | .[]' "$CONFIG_FILE")
    for pipeline in $PIPELINES; do
      FIRST_PROCESSOR=$(yq e ".service.pipelines.$pipeline.processors[0]" "$CONFIG_FILE")
      if [[ "$FIRST_PROCESSOR" != "memory_limiter" && "$FIRST_PROCESSOR" != "null" ]]; then
        echo "Error: memory_limiter is not the first processor in pipeline '$pipeline'."
        exit 1
      fi
    done
  else
    echo "Warning: 'yq' is not installed. Performing a basic grep check for memory_limiter."
    if ! grep -q "memory_limiter" "$CONFIG_FILE"; then
      echo "Warning: memory_limiter processor not found in the configuration."
    fi
  fi
else
  echo "Warning: No pipelines defined in the configuration."
fi

echo "Validation passed."
exit 0
