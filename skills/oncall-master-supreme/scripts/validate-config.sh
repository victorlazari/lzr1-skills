#!/bin/bash

# validate-config.sh
# Deterministic script to validate JSON configuration schemas

set -euo pipefail

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed." >&2
    exit 1
fi

# Help text
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "Usage: $0 <config.json>"
    echo "Validates the syntax of a JSON configuration file."
    exit 0
fi

# Check arguments
if [[ $# -ne 1 ]]; then
    echo "Error: Missing configuration file argument." >&2
    echo "Usage: $0 <config.json>" >&2
    exit 1
fi

CONFIG_FILE="$1"

# Check if file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: File '$CONFIG_FILE' not found." >&2
    exit 1
fi

# Validate JSON syntax
if jq -e . "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "Validation successful: '$CONFIG_FILE' is valid JSON."
    exit 0
else
    echo "Validation failed: '$CONFIG_FILE' contains invalid JSON." >&2
    exit 1
fi
