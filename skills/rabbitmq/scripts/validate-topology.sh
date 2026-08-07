#!/bin/bash

# validate-topology.sh
# Deterministic script to check definitions.json for legacy ha-mode policies,
# transient non-exclusive queues, and other 4.0-incompatible configurations.

set -euo pipefail

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed." >&2
    exit 1
fi

# Help text
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "Usage: $0 <path_to_definitions.json>"
    echo "Validates a RabbitMQ definitions.json file against 4.x constraints."
    exit 0
fi

# Input validation
if [[ $# -ne 1 ]]; then
    echo "Error: Missing input file." >&2
    echo "Usage: $0 <path_to_definitions.json>" >&2
    exit 1
fi

INPUT_FILE="$1"

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: File '$INPUT_FILE' not found." >&2
    exit 1
fi

# Initialize error counter
ERRORS=0

echo "Validating $INPUT_FILE against RabbitMQ 4.x constraints..."

# 1. Check for legacy ha-mode policies
echo "Checking for legacy ha-mode policies..."
HA_POLICIES=$(jq -r '.policies[] | select(.definition["ha-mode"] != null) | .name' "$INPUT_FILE" 2>/dev/null || echo "")
if [[ -n "$HA_POLICIES" ]]; then
    echo "ERROR: Found legacy ha-mode policies (Classic Mirrored Queues are removed in 4.x):" >&2
    echo "$HA_POLICIES" >&2
    ERRORS=$((ERRORS + 1))
fi

# 2. Check for transient non-exclusive queues
echo "Checking for transient non-exclusive queues..."
TRANSIENT_QUEUES=$(jq -r '.queues[] | select(.durable == false and .exclusive == false) | .name' "$INPUT_FILE" 2>/dev/null || echo "")
if [[ -n "$TRANSIENT_QUEUES" ]]; then
    echo "ERROR: Found transient non-exclusive queues (Not recommended/supported in modern HA):" >&2
    echo "$TRANSIENT_QUEUES" >&2
    ERRORS=$((ERRORS + 1))
fi

# 3. Check for Classic Queue version 1 (CQv1)
echo "Checking for Classic Queue version 1 (CQv1)..."
CQV1_QUEUES=$(jq -r '.queues[] | select(.arguments["x-queue-version"] == 1) | .name' "$INPUT_FILE" 2>/dev/null || echo "")
if [[ -n "$CQV1_QUEUES" ]]; then
    echo "ERROR: Found Classic Queue version 1 (CQv1 is deprecated/removed):" >&2
    echo "$CQV1_QUEUES" >&2
    ERRORS=$((ERRORS + 1))
fi

# Summary
if [[ $ERRORS -eq 0 ]]; then
    echo "Validation PASSED. No legacy configurations found."
    exit 0
else
    echo "Validation FAILED with $ERRORS error category/categories." >&2
    exit 1
fi
