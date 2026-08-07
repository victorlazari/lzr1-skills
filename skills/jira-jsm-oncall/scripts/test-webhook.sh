#!/bin/bash
# Test webhook payloads and endpoints

set -euo pipefail

usage() {
    echo "Usage: $0 --url <webhook_url> --payload <json_file> [--dry-run]"
    echo "Tests a webhook endpoint with a given JSON payload."
    exit 1
}

URL=""
PAYLOAD_FILE=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            URL="$2"
            shift 2
            ;;
        --payload)
            PAYLOAD_FILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=1
            shift 1
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

if [[ -z "$URL" || -z "$PAYLOAD_FILE" ]]; then
    echo "Error: Missing required arguments."
    usage
fi

if [[ ! -f "$PAYLOAD_FILE" ]]; then
    echo "Error: Payload file '$PAYLOAD_FILE' not found."
    exit 1
fi

# Validate JSON payload
if ! jq . "$PAYLOAD_FILE" >/dev/null 2>&1; then
    echo "Error: Invalid JSON in payload file."
    exit 1
fi

if [[ $DRY_RUN -eq 1 ]]; then
    echo "Dry run mode enabled. Would send the following payload to $URL:"
    cat "$PAYLOAD_FILE"
    echo ""
    echo "Dry run successful."
    exit 0
fi

echo "Sending payload to $URL..."

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d @"${PAYLOAD_FILE}" \
    "${URL}")

if [[ "$HTTP_STATUS" =~ ^2 ]]; then
    echo "Webhook test successful. HTTP Status: $HTTP_STATUS"
    exit 0
else
    echo "Error: Webhook test failed. HTTP Status: $HTTP_STATUS"
    exit 1
fi
