#!/bin/bash
# Valkey Migration Helper Script
# Assists with migrating from Redis OSS to Valkey.

set -euo pipefail

DRY_RUN=0
SOURCE_HOST="127.0.0.1"
SOURCE_PORT="6379"
TARGET_HOST="127.0.0.1"
TARGET_PORT="6380"

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --dry-run          Perform a dry-run pre-flight check"
    echo "  --source-host IP   Source Redis host (default: 127.0.0.1)"
    echo "  --source-port PORT Source Redis port (default: 6379)"
    echo "  --target-host IP   Target Valkey host (default: 127.0.0.1)"
    echo "  --target-port PORT Target Valkey port (default: 6380)"
    echo "  --help             Show this help message"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=1 ;;
        --source-host) SOURCE_HOST="$2"; shift ;;
        --source-port) SOURCE_PORT="$2"; shift ;;
        --target-host) TARGET_HOST="$2"; shift ;;
        --target-port) TARGET_PORT="$2"; shift ;;
        --help) usage; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; usage; exit 1 ;;
    esac
    shift
done

echo "Starting Valkey Migration Helper..."

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY RUN] Performing pre-flight checks..."

    # Check if redis-cli or valkey-cli is available
    if command -v valkey-cli >/dev/null 2>&1; then
        CLI="valkey-cli"
    elif command -v redis-cli >/dev/null 2>&1; then
        CLI="redis-cli"
    else
        echo "Error: Neither valkey-cli nor redis-cli found in PATH."
        exit 1
    fi

    echo "[DRY RUN] Using CLI: $CLI"
    echo "[DRY RUN] Checking source connectivity ($SOURCE_HOST:$SOURCE_PORT)..."
    if ! $CLI -h "$SOURCE_HOST" -p "$SOURCE_PORT" PING >/dev/null 2>&1; then
        echo "Warning: Could not connect to source Redis."
    else
        echo "Source connected successfully."
    fi

    echo "[DRY RUN] Checking target connectivity ($TARGET_HOST:$TARGET_PORT)..."
    if ! $CLI -h "$TARGET_HOST" -p "$TARGET_PORT" PING >/dev/null 2>&1; then
        echo "Warning: Could not connect to target Valkey."
    else
        echo "Target connected successfully."
    fi

    echo "[DRY RUN] Pre-flight checks complete."
    exit 0
fi

echo "Error: This script currently only supports --dry-run mode for safety."
echo "Please perform the actual migration manually following the steps in references/complete-reference.md"
exit 1
