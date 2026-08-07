#!/bin/bash
# /usr/local/bin/docker-cron-wrapper.sh
# 
# Wrapper script for running cron jobs in Docker containers from the host machine.
# This ensures 100% correct execution by verifying the container is actually running
# before attempting to execute the command, preventing silent failures and log spam.

# Usage: /usr/local/bin/docker-cron-wrapper.sh <container_name> <command> [args...]
# Example: /usr/local/bin/docker-cron-wrapper.sh openclaw_app python /app/sync.py

set -e

if [ "$#" -lt 2 ]; then
    echo "Error: Missing arguments."
    echo "Usage: $0 <container_name> <command> [args...]"
    exit 1
fi

CONTAINER=$1
shift
COMMAND="$@"

# Check if the container exists and is running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    # Container is running, execute the command safely
    # Note: Do NOT use -it (interactive/tty) flags in cron!
    docker exec "$CONTAINER" $COMMAND
else
    # Container not running - log the error to stderr
    echo "[$(date -u)] Error: Container '$CONTAINER' is not running. Cannot execute: $COMMAND" >&2
    exit 1
fi
