#!/bin/bash
# Deterministic script to verify Node.js, Playwright CLI, and browser installations.

set -e

echo "Verifying Playwright Environment..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed."
    exit 1
fi
NODE_VERSION=$(node -v)
echo "Node.js version: $NODE_VERSION"

# Check Playwright CLI
if ! command -v npx &> /dev/null; then
    echo "ERROR: npx is not installed (usually comes with Node.js)."
    exit 1
fi

if ! npx playwright --version &> /dev/null; then
    echo "ERROR: Playwright CLI is not installed or not accessible via npx."
    echo "Run 'npm init playwright@latest' to install."
    exit 1
fi
PLAYWRIGHT_VERSION=$(npx playwright --version)
echo "Playwright version: $PLAYWRIGHT_VERSION"

# Check Browsers (Dry run to see if they are installed)
echo "Checking browser installations..."
if ! npx playwright install --dry-run &> /dev/null; then
    echo "WARNING: Browsers might not be fully installed. Run 'npx playwright install' to ensure all required browsers are present."
else
    echo "Browsers appear to be installed."
fi

echo "Environment verification complete."
exit 0
