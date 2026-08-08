#!/usr/bin/env bash
# Validate JQL with Jira Cloud's syntax-only parse endpoint.
# Verified against Atlassian REST API v3 documentation: 2026-08-07.

set -euo pipefail
umask 077

usage() {
    cat <<'EOF'
Usage:
  validate-jql.sh --jql <query> --domain <tenant.atlassian.net> --anonymous [--dry-run]
  validate-jql.sh --jql <query> --domain <tenant.atlassian.net> \
    --user <email> [--token-env <ENV_NAME>] [--dry-run]

Options:
  --jql <query>       JQL query to parse and validate
  --domain <host>     Jira Cloud host only, for example acme.atlassian.net
  --user <email>      Atlassian account email for contextual validation
  --token-env <name>  Environment variable containing the API token
                      (default: JIRA_API_TOKEN)
  --anonymous         Validate without authentication; permissions and visible
                      fields may differ from an authenticated user's context
  --dry-run           Validate arguments and print the endpoint without sending
  -h, --help          Show this help

Security:
  API tokens are never accepted as command-line values. The destination is
  restricted to a single-label *.atlassian.net Jira Cloud tenant host.
EOF
}

fail() {
    printf 'Error: %s\n' "$1" >&2
    exit 2
}

require_value() {
    local option_name=$1
    local remaining=$2
    [[ $remaining -ge 2 ]] || fail "$option_name requires a value"
}

JQL=""
DOMAIN=""
USER_EMAIL=""
TOKEN_ENV="JIRA_API_TOKEN"
ANONYMOUS=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --jql)
            require_value "$1" "$#"
            JQL=$2
            shift 2
            ;;
        --domain)
            require_value "$1" "$#"
            DOMAIN=$2
            shift 2
            ;;
        --user)
            require_value "$1" "$#"
            USER_EMAIL=$2
            shift 2
            ;;
        --token-env)
            require_value "$1" "$#"
            TOKEN_ENV=$2
            shift 2
            ;;
        --anonymous)
            ANONYMOUS=1
            shift
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --token)
            fail "--token is intentionally unsupported because command-line secrets leak; use --token-env"
            ;;
        *)
            fail "unknown option: $1"
            ;;
    esac
done

[[ -n $JQL ]] || fail "--jql is required"
[[ -n $DOMAIN ]] || fail "--domain is required"

DOMAIN=$(printf '%s' "$DOMAIN" | tr '[:upper:]' '[:lower:]')
if [[ ! $DOMAIN =~ ^[a-z0-9][a-z0-9-]{0,62}\.atlassian\.net$ ]]; then
    fail "--domain must be a host such as acme.atlassian.net; schemes, paths, ports, userinfo, and non-Atlassian hosts are rejected"
fi

if [[ $ANONYMOUS -eq 1 && -n $USER_EMAIL ]]; then
    fail "--anonymous and --user are mutually exclusive"
fi
if [[ $ANONYMOUS -eq 0 ]]; then
    [[ -n $USER_EMAIL ]] || fail "provide --user or select --anonymous explicitly"
    if [[ ! $USER_EMAIL =~ ^[^[:space:]:@]+@[^[:space:]:@]+$ ]]; then
        fail "--user must be a single email address without whitespace or a colon"
    fi
    if [[ ! $TOKEN_ENV =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
        fail "--token-env must be a valid environment-variable name"
    fi
fi

API_URL="https://${DOMAIN}/rest/api/3/jql/parse?validation=strict"

if [[ $DRY_RUN -eq 1 ]]; then
    printf 'Dry run: would POST one JQL query to %s\n' "$API_URL"
    if [[ $ANONYMOUS -eq 1 ]]; then
        printf '%s\n' 'Authentication: anonymous (validation context may be incomplete)'
    else
        printf 'Authentication: protected Basic header derived from --user and environment variable %s\n' "$TOKEN_ENV"
    fi
    exit 0
fi

for dependency in curl jq; do
    command -v "$dependency" >/dev/null 2>&1 || fail "$dependency is required"
done
if [[ $ANONYMOUS -eq 0 ]]; then
    command -v base64 >/dev/null 2>&1 || fail "base64 is required for authenticated mode"
fi

REQUEST_BODY=$(jq -cn --arg jql "$JQL" '{queries: [$jql]}') || fail "could not encode JQL as JSON"

TEMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/validate-jql.XXXXXX") || fail "could not create a temporary directory"
chmod 700 "$TEMP_DIR"
RESPONSE_FILE="$TEMP_DIR/response.json"
AUTH_CONFIG="$TEMP_DIR/curl-auth.conf"
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT HUP INT TERM

curl_argv=(
    curl
    --silent
    --show-error
    --connect-timeout 10
    --max-time 30
    --proto '=https'
    --tlsv1.2
    --request POST
    --header 'Accept: application/json'
    --header 'Content-Type: application/json'
    --data-binary "$REQUEST_BODY"
    --output "$RESPONSE_FILE"
    --write-out '%{http_code}'
)

if [[ $ANONYMOUS -eq 0 ]]; then
    TOKEN=${!TOKEN_ENV-}
    [[ -n $TOKEN ]] || fail "environment variable $TOKEN_ENV is empty or unset"
    case $TOKEN in
        *$'\n'*|*$'\r'*) fail "the API token must not contain newlines" ;;
    esac
    AUTH_VALUE=$(printf '%s' "${USER_EMAIL}:${TOKEN}" | base64 | tr -d '\r\n')
    printf 'header = "Authorization: Basic %s"\n' "$AUTH_VALUE" > "$AUTH_CONFIG"
    chmod 600 "$AUTH_CONFIG"
    curl_argv+=(--config "$AUTH_CONFIG")
    unset TOKEN AUTH_VALUE
fi

curl_argv+=("$API_URL")

if ! HTTP_STATUS=$("${curl_argv[@]}"); then
    fail "request failed before Jira returned an HTTP status"
fi

if ! jq -e . "$RESPONSE_FILE" >/dev/null 2>&1; then
    printf 'Error: Jira returned HTTP %s with a non-JSON body\n' "$HTTP_STATUS" >&2
    exit 1
fi

case $HTTP_STATUS in
    200)
        if ! jq -e '.queries | type == "array" and length == 1' "$RESPONSE_FILE" >/dev/null; then
            printf '%s\n' 'Error: Jira returned an unexpected parse-response shape.' >&2
            exit 1
        fi
        ERROR_COUNT=$(jq '[.queries[0].errors[]?] | length' "$RESPONSE_FILE")
        if [[ $ERROR_COUNT -gt 0 ]]; then
            printf '%s\n' 'JQL is invalid:' >&2
            jq -r '.queries[0].errors[] | "- \(.)"' "$RESPONSE_FILE" >&2
            exit 1
        fi
        WARNING_COUNT=$(jq '[.queries[0].warnings[]?] | length' "$RESPONSE_FILE")
        if [[ $WARNING_COUNT -gt 0 ]]; then
            printf '%s\n' 'JQL parsed with contextual warnings:' >&2
            jq -r '.queries[0].warnings[] | "- \(.)"' "$RESPONSE_FILE" >&2
        fi
        printf '%s\n' 'JQL parsed successfully in the selected Jira context.'
        ;;
    400)
        printf '%s\n' 'Error: Jira rejected the parse request.' >&2
        jq -r '.errorMessages[]?, (.errors // {} | to_entries[]? | "\(.key): \(.value)")' "$RESPONSE_FILE" >&2
        exit 1
        ;;
    401|403)
        printf 'Error: Jira returned HTTP %s; authentication, authorization, or API-token scope is insufficient.\n' "$HTTP_STATUS" >&2
        exit 1
        ;;
    429)
        printf '%s\n' 'Error: Jira rate-limited the request (HTTP 429); retry according to Retry-After without tight loops.' >&2
        exit 1
        ;;
    *)
        printf 'Error: unexpected Jira HTTP status %s.\n' "$HTTP_STATUS" >&2
        exit 1
        ;;
esac
