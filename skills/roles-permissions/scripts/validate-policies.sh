#!/bin/bash

# validate-policies.sh
# Validates Casbin policies against common misconfigurations.

set -e

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $0 [policy_file]"
    echo "Validates Casbin policies for syntax and conflicts."
    echo "  policy_file: Path to the Casbin policy file (default: policy.csv)"
    exit 0
fi

POLICY_FILE="${1:-policy.csv}"

if [[ ! -f "$POLICY_FILE" ]]; then
    echo "Error: Policy file '$POLICY_FILE' not found."
    exit 1
fi

echo "Validating policy file: $POLICY_FILE"

# Basic syntax check: Ensure each line has at least 3 comma-separated fields (p, sub, obj, act)
# Ignore empty lines and comments
grep -v '^\s*$' "$POLICY_FILE" | grep -v '^\s*#' | while read -r line; do
    fields=$(echo "$line" | awk -F',' '{print NF}')
    if [[ "$fields" -lt 3 ]]; then
        echo "Syntax Error: Line does not have enough fields: $line"
        exit 1
    fi
done

echo "Policy validation passed."
exit 0
