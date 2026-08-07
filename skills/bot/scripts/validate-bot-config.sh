#!/bin/bash
# Deterministic validation of bot configuration files

set -euo pipefail

usage() {
    echo "Usage: $0 <config_file>"
    echo "Validates bot configuration files (e.g., openclaw.json, bot-config.yml)."
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

CONFIG_FILE="$1"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: File '$CONFIG_FILE' not found."
    exit 1
fi

EXT="${CONFIG_FILE##*.}"

echo "Validating $CONFIG_FILE..."

if [ "$EXT" = "json" ]; then
    if command -v jq >/dev/null 2>&1; then
        if jq . "$CONFIG_FILE" >/dev/null 2>&1; then
            echo "PASS: JSON syntax is valid."
        else
            echo "FAIL: Invalid JSON syntax."
            exit 1
        fi
    else
        if python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$CONFIG_FILE" >/dev/null 2>&1; then
            echo "PASS: JSON syntax is valid."
        else
            echo "FAIL: Invalid JSON syntax."
            exit 1
        fi
    fi
elif [ "$EXT" = "yml" ] || [ "$EXT" = "yaml" ]; then
    if command -v yq >/dev/null 2>&1; then
        if yq . "$CONFIG_FILE" >/dev/null 2>&1; then
            echo "PASS: YAML syntax is valid."
        else
            echo "FAIL: Invalid YAML syntax."
            exit 1
        fi
    else
        if python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" "$CONFIG_FILE" >/dev/null 2>&1; then
            echo "PASS: YAML syntax is valid."
        else
            echo "FAIL: Invalid YAML syntax."
            exit 1
        fi
    fi
else
    echo "Warning: Unsupported file extension '$EXT'. Only .json, .yml, and .yaml are fully supported."
    echo "Performing basic read check..."
    if cat "$CONFIG_FILE" >/dev/null 2>&1; then
        echo "PASS: File is readable."
    else
        echo "FAIL: File is not readable."
        exit 1
    fi
fi

echo "Validation complete."
exit 0
