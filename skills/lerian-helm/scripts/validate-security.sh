#!/bin/bash
# Enforce Kubernetes Restricted Pod Security Standards on a values.yaml file

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-values.yaml>"
    exit 1
fi

VALUES_FILE="$1"

if [ ! -f "$VALUES_FILE" ]; then
    echo "Error: File '$VALUES_FILE' not found."
    exit 1
fi

echo "Validating $VALUES_FILE for Restricted Pod Security Standards..."

# Check for allowPrivilegeEscalation: false
if ! grep -q "allowPrivilegeEscalation: false" "$VALUES_FILE"; then
    echo "FAIL: allowPrivilegeEscalation: false is missing or not set correctly."
    exit 1
fi

# Check for seccompProfile: RuntimeDefault
if ! grep -q -A 1 "seccompProfile:" "$VALUES_FILE" | grep -q "type: RuntimeDefault"; then
    echo "FAIL: seccompProfile: type: RuntimeDefault is missing or not set correctly."
    exit 1
fi

echo "PASS: Security validation successful."
exit 0
