#!/bin/bash
# Security Audit Script for Go Projects
# This script runs deterministic security checks including govulncheck and race detection.

set -e

function show_help {
    echo "Usage: $0 [options] [target_dir]"
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo "  --dry-run     Show what would be executed without running the checks"
    echo ""
    echo "Arguments:"
    echo "  target_dir    The directory containing the Go project (default: current directory)"
}

DRY_RUN=0
TARGET_DIR="."

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) show_help; exit 0 ;;
        --dry-run) DRY_RUN=1; shift ;;
        *) TARGET_DIR="$1"; shift ;;
    esac
done

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist."
    exit 1
fi

cd "$TARGET_DIR"

if [[ ! -f "go.mod" ]]; then
    echo "Error: No go.mod found in '$TARGET_DIR'. This script must be run in a Go module."
    exit 1
fi

echo "Starting security audit for Go project in '$TARGET_DIR'..."

if [[ $DRY_RUN -eq 1 ]]; then
    echo "[Dry Run] Would execute: go test -race ./..."
    echo "[Dry Run] Would execute: govulncheck ./..."
    exit 0
fi

echo "Running race detector..."
if ! go test -race ./...; then
    echo "Warning: Race conditions detected or tests failed."
fi

echo "Running govulncheck..."
if ! command -v govulncheck &> /dev/null; then
    echo "govulncheck not found. Installing..."
    go install golang.org/x/vuln/cmd/govulncheck@latest
fi

if ! govulncheck ./...; then
    echo "Warning: Vulnerabilities detected by govulncheck."
fi

echo "Security audit completed."
