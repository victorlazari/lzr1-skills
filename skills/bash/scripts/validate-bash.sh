#!/usr/bin/env bash
set -euo pipefail

# validate-bash.sh
# Deterministic script to run syntax checks on Bash scripts.

show_help() {
    echo "Usage: $0 <script_file>"
    echo "Validates the syntax of a Bash script using 'bash -n'."
    echo "Returns 0 on success, non-zero on failure."
}

if [[ $# -eq 0 || "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

SCRIPT_FILE="$1"

if [[ ! -f "$SCRIPT_FILE" ]]; then
    echo "Error: File '$SCRIPT_FILE' not found." >&2
    exit 1
fi

echo "Running syntax check on '$SCRIPT_FILE'..."
if bash -n "$SCRIPT_FILE"; then
    echo "Syntax check passed: '$SCRIPT_FILE'"
    exit 0
else
    echo "Syntax check failed: '$SCRIPT_FILE'" >&2
    exit 1
fi
