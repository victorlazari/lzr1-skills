#!/bin/bash
# check-version.sh
# Script to query the Wiki.js API and verify the instance is running the latest stable version.

set -euo pipefail

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Query the Wiki.js API to verify the instance version."
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -u, --url URL    Wiki.js instance URL (e.g., https://wiki.example.com)"
    echo "  -t, --token TKN  Wiki.js API token"
}

WIKI_URL=""
API_TOKEN=""
EXPECTED_VERSION="2.5.314"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--url)
            WIKI_URL="$2"
            shift 2
            ;;
        -t|--token)
            API_TOKEN="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [[ -z "$WIKI_URL" || -z "$API_TOKEN" ]]; then
    echo "Error: Both URL and API token are required."
    show_help
    exit 1
fi

# Remove trailing slash from URL if present
WIKI_URL="${WIKI_URL%/}"
GRAPHQL_ENDPOINT="${WIKI_URL}/graphql"

echo "Querying Wiki.js version at: $GRAPHQL_ENDPOINT"

QUERY='{"query": "query { site { info { version } } }"}'

RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $API_TOKEN" \
    -d "$QUERY" \
    "$GRAPHQL_ENDPOINT")

if [[ -z "$RESPONSE" ]]; then
    echo "Error: Empty response from server."
    exit 1
fi

# Basic JSON parsing using grep/sed (assuming jq might not be available, though it usually is)
# Alternatively, we can use python for robust parsing
VERSION=$(python3 -c "
import sys, json
try:
    data = json.loads(sys.argv[1])
    print(data['data']['site']['info']['version'])
except Exception as e:
    print('Error parsing response:', e, file=sys.stderr)
    sys.exit(1)
" "$RESPONSE")

if [[ $? -ne 0 ]]; then
    echo "Failed to extract version from response: $RESPONSE"
    exit 1
fi

echo "Detected version: $VERSION"

if [[ "$VERSION" == "$EXPECTED_VERSION" ]]; then
    echo "Success: Instance is running the expected stable version ($EXPECTED_VERSION)."
    exit 0
else
    echo "Warning: Instance is running version $VERSION, expected $EXPECTED_VERSION."
    exit 2
fi
