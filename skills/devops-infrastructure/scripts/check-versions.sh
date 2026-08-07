#!/bin/bash
# Check installed versions of common infrastructure tools against required minimums

set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
    echo "Usage: $0"
    echo "Checks installed versions of common infrastructure tools."
    exit 0
fi

check_tool() {
    local tool=$1
    local cmd=$2
    if command -v "$tool" >/dev/null 2>&1; then
        echo "[PASS] $tool is installed: $(eval "$cmd")"
    else
        echo "[WARN] $tool is not installed."
    fi
}

echo "Checking infrastructure tools..."
check_tool "terraform" "terraform version | head -n1"
check_tool "kubectl" "kubectl version --client --short 2>/dev/null || kubectl version --client -o yaml | grep gitVersion | awk '{print \$2}'"
check_tool "helm" "helm version --short"
check_tool "aws" "aws --version"
check_tool "gcloud" "gcloud version | head -n1"
check_tool "az" "az version | grep '\"azure-cli\"' | awk -F':' '{print \$2}' | tr -d ' \",'"

echo "Version check complete."
