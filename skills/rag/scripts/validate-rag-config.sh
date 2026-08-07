#!/bin/bash
# Deterministic script to validate RAG configuration schemas (JSON)

set -euo pipefail

# Help text
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "Usage: $0 <config.json>"
    echo "Validates a RAG configuration JSON file for required fields."
    echo "Required fields: vector_db.type, embedding.model, chunking.strategy"
    exit 0
fi

CONFIG_FILE="${1:-}"

if [[ -z "$CONFIG_FILE" ]]; then
    echo "Error: Configuration file not provided."
    echo "Usage: $0 <config.json>"
    exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: File '$CONFIG_FILE' not found."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: 'jq' is required but not installed."
    exit 1
fi

# Validate JSON syntax
if ! jq empty "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "Error: '$CONFIG_FILE' is not a valid JSON file."
    exit 1
fi

# Check required fields
MISSING_FIELDS=0

check_field() {
    local field_path="$1"
    local field_name="$2"
    local value
    value=$(jq -r "$field_path // empty" "$CONFIG_FILE")
    if [[ -z "$value" ]]; then
        echo "Validation Error: Missing required field '$field_name'."
        MISSING_FIELDS=$((MISSING_FIELDS + 1))
    fi
}

check_field ".vector_db.type" "vector_db.type"
check_field ".embedding.model" "embedding.model"
check_field ".chunking.strategy" "chunking.strategy"

if [[ $MISSING_FIELDS -gt 0 ]]; then
    echo "Validation failed: $MISSING_FIELDS required field(s) missing."
    exit 1
fi

echo "Validation passed: '$CONFIG_FILE' contains all required fields."
exit 0
