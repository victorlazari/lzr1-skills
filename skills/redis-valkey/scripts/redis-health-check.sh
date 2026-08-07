#!/bin/bash
# Deterministic script to perform basic health checks, memory stats, and latency measurements.

set -euo pipefail

HOST="${1:-127.0.0.1}"
PORT="${2:-6379}"
PASSWORD="${3:-}"

AUTH_ARGS=""
if [ -n "$PASSWORD" ]; then
    AUTH_ARGS="-a $PASSWORD"
fi

echo "Running health check on $HOST:$PORT..."

# Check connection
if ! redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS PING > /dev/null 2>&1; then
    echo "ERROR: Could not connect to Redis/Valkey at $HOST:$PORT"
    exit 1
fi
echo "Connection: OK"

# Get basic info
echo "--- Server Info ---"
redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO SERVER | grep -E "^redis_version|^valkey_version|^os|^uptime_in_days"

echo "--- Memory Stats ---"
redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO MEMORY | grep -E "^used_memory_human|^used_memory_rss_human|^used_memory_peak_human|^maxmemory_human|^maxmemory_policy"

echo "--- Clients ---"
redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO CLIENTS | grep -E "^connected_clients|^blocked_clients"

echo "--- Keyspace ---"
redis-cli -h "$HOST" -p "$PORT" $AUTH_ARGS INFO KEYSPACE

echo "Health check completed successfully."
exit 0
