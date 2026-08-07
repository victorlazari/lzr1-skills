#!/bin/bash
# verify-owasp.sh
# Verifies the current OWASP Top 10 by fetching the canonical page and extracting the year/version.

set -euo pipefail

URL="https://owasp.org/www-project-top-ten/"

echo "Verifying OWASP Top 10 from $URL..."

# Fetch the page and look for the current version year (e.g., "OWASP Top 10 - 2021")
if curl -sL "$URL" | grep -i "OWASP Top 10 - 20" | head -n 1; then
    echo "Verification successful. Date: $(date -u +'%Y-%m-%d')"
    exit 0
else
    echo "Error: Could not verify current OWASP Top 10 version." >&2
    exit 1
fi
