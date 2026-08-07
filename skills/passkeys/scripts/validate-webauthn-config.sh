#!/bin/bash
# Validate WebAuthn configuration

set -euo pipefail

usage() {
    echo "Usage: $0 <config_file.json>"
    echo "Validates a WebAuthn configuration file for required fields."
    exit 1
}

if [ "$#" -ne 1 ]; then
    usage
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: File '$CONFIG_FILE' not found."
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

# Validate JSON syntax
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
    echo "Error: Invalid JSON syntax in '$CONFIG_FILE'."
    exit 1
fi

# Check for required fields
RP_ID=$(jq -r '.rp_id // empty' "$CONFIG_FILE")
ORIGINS=$(jq -r '.origins // empty' "$CONFIG_FILE")

if [ -z "$RP_ID" ]; then
    echo "Error: Missing 'rp_id' in configuration."
    exit 1
fi

if [ -z "$ORIGINS" ]; then
    echo "Error: Missing 'origins' in configuration."
    exit 1
fi

echo "Configuration is valid."
echo "RP ID: $RP_ID"
echo "Origins: $(jq -c '.origins' "$CONFIG_FILE")"

exit 0
