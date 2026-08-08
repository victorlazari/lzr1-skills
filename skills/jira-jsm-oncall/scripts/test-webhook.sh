#!/usr/bin/env bash
# Preview and, with explicit consent, send a bounded JSON webhook payload.

set -euo pipefail
umask 077

usage() {
    cat <<'EOF'
Usage:
  test-webhook.sh --url <https_url> --allow-host <exact_host> \
    --payload <json_file> [--allow-port <port>] [--dry-run]
  test-webhook.sh --url <https_url> --allow-host <exact_host> \
    --payload <json_file> [--allow-port <port>] --send

Options:
  --url <url>          HTTPS webhook URL; userinfo and fragments are rejected
  --allow-host <host>  Exact expected destination hostname (no wildcards)
  --allow-port <port>  Exact permitted port (default: 443)
  --payload <file>     JSON payload, at most 1 MiB, not a symbolic link
  --dry-run            Preview destination and payload digest; this is default
  --send               Explicitly authorize one outbound POST
  -h, --help           Show this help

Safety:
  The destination must resolve entirely to globally routable addresses. The
  validated addresses are pinned for curl, redirects and environment proxies
  are disabled, and response bodies are discarded.
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

URL=""
ALLOW_HOST=""
ALLOW_PORT=443
PAYLOAD_FILE=""
MODE="dry-run"

while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            require_value "$1" "$#"
            URL=$2
            shift 2
            ;;
        --allow-host)
            require_value "$1" "$#"
            ALLOW_HOST=$2
            shift 2
            ;;
        --allow-port)
            require_value "$1" "$#"
            ALLOW_PORT=$2
            shift 2
            ;;
        --payload)
            require_value "$1" "$#"
            PAYLOAD_FILE=$2
            shift 2
            ;;
        --dry-run)
            [[ $MODE != "send" ]] || fail "--dry-run and --send are mutually exclusive"
            MODE="dry-run"
            shift
            ;;
        --send)
            [[ $MODE == "dry-run" ]] || fail "--send may be specified only once"
            MODE="send"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            fail "unknown option: $1"
            ;;
    esac
done

[[ -n $URL ]] || fail "--url is required"
[[ -n $ALLOW_HOST ]] || fail "--allow-host is required"
[[ -n $PAYLOAD_FILE ]] || fail "--payload is required"
[[ $ALLOW_PORT =~ ^[0-9]+$ ]] || fail "--allow-port must be numeric"
if (( ALLOW_PORT < 1 || ALLOW_PORT > 65535 )); then
    fail "--allow-port must be between 1 and 65535"
fi

for dependency in python3 jq sha256sum; do
    command -v "$dependency" >/dev/null 2>&1 || fail "$dependency is required"
done

[[ -f $PAYLOAD_FILE ]] || fail "payload file not found: $PAYLOAD_FILE"
[[ ! -L $PAYLOAD_FILE ]] || fail "symbolic-link payloads are rejected"
PAYLOAD_SIZE=$(wc -c < "$PAYLOAD_FILE" | tr -d '[:space:]')
[[ $PAYLOAD_SIZE =~ ^[0-9]+$ ]] || fail "could not determine payload size"
if (( PAYLOAD_SIZE > 1048576 )); then
    fail "payload exceeds the 1 MiB limit"
fi
if ! jq -e . "$PAYLOAD_FILE" >/dev/null 2>&1; then
    fail "payload is not valid JSON"
fi
PAYLOAD_SHA256=$(sha256sum "$PAYLOAD_FILE" | awk '{print $1}')

TEMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/test-webhook.XXXXXX") || fail "could not create a temporary directory"
chmod 700 "$TEMP_DIR"
URL_RECORD="$TEMP_DIR/url.tsv"
RESOLUTION_RECORD="$TEMP_DIR/resolution.tsv"
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT HUP INT TERM

if ! python3 - "$URL" "$ALLOW_HOST" "$ALLOW_PORT" > "$URL_RECORD" <<'PY'
import re
import sys
from urllib.parse import urlsplit

url, allowed_host, allowed_port_text = sys.argv[1:]
try:
    parsed = urlsplit(url)
    port = parsed.port or 443
except ValueError as exc:
    raise SystemExit(f"invalid URL: {exc}")

host = (parsed.hostname or "").rstrip(".").lower()
allowed = allowed_host.rstrip(".").lower()
if parsed.scheme.lower() != "https":
    raise SystemExit("only https URLs are allowed")
if parsed.username is not None or parsed.password is not None:
    raise SystemExit("URL userinfo is rejected")
if parsed.fragment:
    raise SystemExit("URL fragments are rejected")
if not host or not re.fullmatch(r"(?=.{1,253}\Z)[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host):
    raise SystemExit("destination must be an ASCII DNS hostname")
if ".." in host or any(len(label) > 63 or not label for label in host.split(".")):
    raise SystemExit("destination hostname is malformed")
if host != allowed:
    raise SystemExit("URL hostname does not exactly match --allow-host")
if port != int(allowed_port_text):
    raise SystemExit("URL port does not exactly match --allow-port")
if parsed.query and any(ord(ch) < 32 or ord(ch) == 127 for ch in parsed.query):
    raise SystemExit("URL query contains control characters")
if any(ord(ch) < 32 or ord(ch) == 127 for ch in parsed.path):
    raise SystemExit("URL path contains control characters")
print(f"{host}\t{port}")
PY
then
    fail "URL failed the destination policy"
fi

IFS=$'\t' read -r DEST_HOST DEST_PORT < "$URL_RECORD"
[[ -n $DEST_HOST && -n $DEST_PORT ]] || fail "URL validation returned no destination"

printf 'Destination: https://%s:%s\n' "$DEST_HOST" "$DEST_PORT"
printf 'Payload: %s bytes, SHA-256 %s\n' "$PAYLOAD_SIZE" "$PAYLOAD_SHA256"
printf '%s\n' 'Redirects: disabled; environment proxies: disabled'

if [[ $MODE == "dry-run" ]]; then
    printf '%s\n' 'Dry run only. No DNS lookup or network request was performed. Use --send to authorize one POST.'
    exit 0
fi

command -v curl >/dev/null 2>&1 || fail "curl is required for --send"

if ! python3 - "$DEST_HOST" "$DEST_PORT" > "$RESOLUTION_RECORD" <<'PY'
import ipaddress
import socket
import sys

host, port_text = sys.argv[1:]
try:
    answers = socket.getaddrinfo(host, int(port_text), type=socket.SOCK_STREAM)
except OSError as exc:
    raise SystemExit(f"DNS resolution failed: {exc}")

addresses = sorted({answer[4][0].split("%", 1)[0] for answer in answers})
if not addresses:
    raise SystemExit("DNS returned no addresses")
for text in addresses:
    address = ipaddress.ip_address(text)
    if not address.is_global:
        raise SystemExit(f"destination resolves to a non-global address: {address}")
    print(address.compressed)
PY
then
    fail "destination DNS failed the public-address policy"
fi

curl_argv=(
    curl
    --silent
    --show-error
    --connect-timeout 10
    --max-time 30
    --max-redirs 0
    --proto '=https'
    --tlsv1.2
    --noproxy '*'
    --request POST
    --header 'Content-Type: application/json'
    --data-binary "@${PAYLOAD_FILE}"
    --output /dev/null
    --write-out '%{http_code}'
)

while IFS= read -r address; do
    [[ -n $address ]] || continue
    if [[ $address == *:* ]]; then
        address="[$address]"
    fi
    curl_argv+=(--resolve "${DEST_HOST}:${DEST_PORT}:${address}")
done < "$RESOLUTION_RECORD"

curl_argv+=("$URL")

printf '%s\n' 'Sending one explicitly authorized webhook request...'
if ! HTTP_STATUS=$("${curl_argv[@]}"); then
    fail "request failed before the destination returned an HTTP status"
fi

if [[ $HTTP_STATUS =~ ^2[0-9][0-9]$ ]]; then
    printf 'Webhook request succeeded with HTTP %s.\n' "$HTTP_STATUS"
    exit 0
fi
printf 'Error: webhook request returned HTTP %s.\n' "$HTTP_STATUS" >&2
exit 1
