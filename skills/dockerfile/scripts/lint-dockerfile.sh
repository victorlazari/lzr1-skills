#!/bin/bash

# Deterministic script to run Hadolint and basic Trivy scans on a Dockerfile.

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-Dockerfile>"
    exit 1
fi

DOCKERFILE_PATH="$1"

if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo "Error: Dockerfile not found at $DOCKERFILE_PATH"
    exit 1
fi

echo "Running Hadolint..."
if command -v hadolint &> /dev/null; then
    hadolint "$DOCKERFILE_PATH"
else
    echo "Warning: hadolint not found. Skipping Hadolint scan."
fi

echo "Running Trivy config scan..."
if command -v trivy &> /dev/null; then
    trivy config "$DOCKERFILE_PATH"
else
    echo "Warning: trivy not found. Skipping Trivy scan."
fi

echo "Linting and scanning complete."
