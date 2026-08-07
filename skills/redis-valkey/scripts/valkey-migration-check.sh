#!/bin/bash
# Deterministic script to verify Redis version compatibility and module availability before migration.

set -euo pipefail

HOST="${1:-127.0.0.1}"
PORT="${2:-6379}"
PASSWORD="${3:-}"

AUTH_ARGS=""
if [ -n "$PASSWORD" ]; then
    AUTH_ARGS="-a $PASSWORD"
fi

echo "Running Valkey migration pre-check on $HOST:$PORT..."

# Check connection
if ! redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS PING > /dev/null 2>&1; then
    echo "ERROR: Could not connect to Redis at $HOST:$PORT"
    exit 1
fi

# Get Redis version
VERSION_STRING=$(redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO SERVER | grep "^redis_version:" | cut -d':' -f2 | tr -d '\r')

if [ -z "$VERSION_STRING" ]; then
    # Might already be Valkey
    VALKEY_VERSION=$(redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO SERVER | grep "^valkey_version:" | cut -d':' -f2 | tr -d '\r')
    if [ -n "$VALKEY_VERSION" ]; then
        echo "Target is already running Valkey version $VALKEY_VERSION."
        exit 0
    else
        echo "ERROR: Could not determine Redis version."
        exit 1
    fi
fi

echo "Detected Redis version: $VERSION_STRING"

# Parse major and minor version
MAJOR=$(echo "$VERSION_STRING" | cut -d'.' -f1)
MINOR=$(echo "$VERSION_STRING" | cut -d'.' -f2)

# Check compatibility (Valkey is compatible with Redis <= 7.2)
if [ "$MAJOR" -gt 7 ] || ( [ "$MAJOR" -eq 7 ] && [ "$MINOR" -gt 2 ] ); then
    echo "ERROR: Redis version $VERSION_STRING is NOT compatible with Valkey."
    echo "Valkey is a fork of Redis 7.2.4 and cannot read RDB files from Redis 7.4 or later."
    exit 1
else
    echo "SUCCESS: Redis version $VERSION_STRING is compatible with Valkey migration."
fi

# Check for loaded modules
echo "Checking for loaded modules..."
MODULES=$(redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS MODULE LIST)
if [ -z "$MODULES" ] || echo "$MODULES" | grep -q "empty array"; then
    echo "No modules loaded."
else
    echo "WARNING: The following modules are loaded. Ensure they are compatible with Valkey:"
    echo "$MODULES"
fi

echo "Migration pre-check completed."
exit 0
