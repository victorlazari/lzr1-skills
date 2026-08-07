#!/bin/bash
# verify-mongodb-version.sh
# Deterministic script to check the target MongoDB version and ensure compatibility.

set -euo pipefail

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Check the MongoDB version of a target instance."
    echo ""
    echo "Options:"
    echo "  -u, --uri URI      MongoDB connection URI (default: mongodb://localhost:27017)"
    echo "  -m, --min VERSION  Minimum required version (e.g., 8.0)"
    echo "  -h, --help         Show this help message"
}

URI="mongodb://localhost:27017"
MIN_VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--uri)
            URI="$2"
            shift 2
            ;;
        -m|--min)
            MIN_VERSION="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
    esac
done

if ! command -v mongosh &> /dev/null; then
    echo "Error: mongosh is not installed or not in PATH." >&2
    exit 1
fi

echo "Connecting to MongoDB at $URI..."
# Use --quiet to suppress startup warnings and only get the output of the eval
VERSION_JSON=$(mongosh "$URI" --quiet --eval 'JSON.stringify(db.version())' 2>/dev/null || echo "")

if [[ -z "$VERSION_JSON" ]]; then
    echo "Error: Failed to connect to MongoDB or retrieve version." >&2
    exit 1
fi

# Remove quotes from the JSON string
VERSION=$(echo "$VERSION_JSON" | tr -d '"')

echo "Detected MongoDB version: $VERSION"

if [[ -n "$MIN_VERSION" ]]; then
    # Simple version comparison using sort -V
    LOWEST=$(printf "%s\n%s" "$VERSION" "$MIN_VERSION" | sort -V | head -n1)
    if [[ "$LOWEST" != "$MIN_VERSION" && "$VERSION" != "$MIN_VERSION" ]]; then
        echo "Error: MongoDB version $VERSION is lower than the required minimum version $MIN_VERSION." >&2
        exit 1
    fi
    echo "Version check passed: $VERSION >= $MIN_VERSION"
fi

exit 0
