#!/bin/bash
# Validates Block Kit JSON payloads against a basic schema check.
# Usage: ./validate-block-kit.sh <file.json>

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file.json>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

# Perform a basic JSON syntax check
if ! jq . "$FILE" > /dev/null 2>&1; then
    echo "Error: Invalid JSON syntax in '$FILE'."
    exit 1
fi

# Check for required top-level structure (e.g., blocks array)
if ! jq -e '.blocks | type == "array"' "$FILE" > /dev/null 2>&1; then
    echo "Warning: JSON does not contain a top-level 'blocks' array. This might not be a valid Block Kit payload."
    # We don't exit 1 here because it might be a partial block or a different payload type
fi

echo "Validation passed for '$FILE'."
exit 0
