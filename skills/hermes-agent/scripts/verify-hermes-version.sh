#!/bin/bash

# verify-hermes-version.sh
# Validates the installed Hermes Agent version against v0.20.0 and checks for required dependencies.

set -euo pipefail

EXPECTED_VERSION="0.20.0"

# Check if hermes command is available
if ! command -v hermes &> /dev/null; then
    echo "Error: hermes command not found. Please install Hermes Agent using the official one-line installer." >&2
    exit 1
fi

# Get installed version
INSTALLED_VERSION=$(hermes --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

if [ -z "$INSTALLED_VERSION" ]; then
    echo "Error: Could not determine Hermes Agent version." >&2
    exit 1
fi

if [ "$INSTALLED_VERSION" != "$EXPECTED_VERSION" ]; then
    echo "Error: Installed Hermes Agent version ($INSTALLED_VERSION) does not match expected version ($EXPECTED_VERSION)." >&2
    echo "Please update Hermes Agent to v$EXPECTED_VERSION." >&2
    exit 1
fi

echo "Hermes Agent version $INSTALLED_VERSION verified successfully."
exit 0
