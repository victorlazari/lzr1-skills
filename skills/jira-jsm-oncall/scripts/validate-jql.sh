#!/bin/bash
# Validate JQL syntax against Jira API

set -euo pipefail

usage() {
    echo "Usage: $0 --jql <jql_query> --domain <jira_domain> --user <email> --token <api_token>"
    echo "Validates a JQL query using the Jira Cloud REST API."
    exit 1
}

JQL=""
DOMAIN=""
USER=""
TOKEN=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --jql)
            JQL="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --user)
            USER="$2"
            shift 2
            ;;
        --token)
            TOKEN="$2"
            shift 2
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

if [[ -z "$JQL" || -z "$DOMAIN" || -z "$USER" || -z "$TOKEN" ]]; then
    echo "Error: Missing required arguments."
    usage
fi

# Use the search API with maxResults=0 to validate syntax without fetching issues
API_URL="https://${DOMAIN}/rest/api/3/search"

# We use curl to send the request
# The --fail flag ensures curl returns a non-zero exit code on HTTP errors (like 400 Bad Request for invalid JQL)
# We capture the HTTP status code to provide better error messages
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -u "${USER}:${TOKEN}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d "{\"jql\": \"${JQL}\", \"maxResults\": 0}" \
    "${API_URL}")

if [[ "$HTTP_STATUS" == "200" ]]; then
    echo "JQL is valid."
    exit 0
elif [[ "$HTTP_STATUS" == "400" ]]; then
    echo "Error: Invalid JQL syntax."
    # Fetch the actual error message
    curl -s -u "${USER}:${TOKEN}" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "{\"jql\": \"${JQL}\", \"maxResults\": 0}" \
        "${API_URL}" | grep -o '"errorMessages":\[[^]]*\]' || true
    exit 1
elif [[ "$HTTP_STATUS" == "401" || "$HTTP_STATUS" == "403" ]]; then
    echo "Error: Authentication failed. Check your user email and API token."
    exit 1
else
    echo "Error: Unexpected HTTP status code ${HTTP_STATUS}."
    exit 1
fi
