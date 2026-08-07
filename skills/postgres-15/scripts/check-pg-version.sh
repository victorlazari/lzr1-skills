#!/bin/bash
# Verify PostgreSQL version and required extensions

set -euo pipefail

# Check if psql is available
if ! command -v psql >/dev/null 2>&1; then
    echo "ERROR: psql command not found. Please ensure PostgreSQL client is installed." >&2
    exit 1
fi

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Verify PostgreSQL version (must be 15+) and check for required extensions."
    echo ""
    echo "Options:"
    echo "  -h, --help      Show this help message and exit"
    echo "  -d, --dbname    Database name to connect to (default: postgres)"
    echo "  -U, --username  Database user name (default: postgres)"
    echo "  -h, --host      Database server host or socket directory"
    echo "  -p, --port      Database server port"
}

DBNAME="postgres"
DBUSER="postgres"
DBHOST=""
DBPORT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dbname)
            DBNAME="$2"
            shift 2
            ;;
        -U|--username)
            DBUSER="$2"
            shift 2
            ;;
        --host)
            DBHOST="$2"
            shift 2
            ;;
        -p|--port)
            DBPORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
    esac
done

# Build psql connection string
PSQL_CMD="psql -X -q -t -A"
if [ -n "$DBNAME" ]; then PSQL_CMD="$PSQL_CMD -d $DBNAME"; fi
if [ -n "$DBUSER" ]; then PSQL_CMD="$PSQL_CMD -U $DBUSER"; fi
if [ -n "$DBHOST" ]; then PSQL_CMD="$PSQL_CMD -h $DBHOST"; fi
if [ -n "$DBPORT" ]; then PSQL_CMD="$PSQL_CMD -p $DBPORT"; fi

echo "Checking PostgreSQL version..."
VERSION_OUTPUT=$($PSQL_CMD -c "SHOW server_version_num;")

if [ -z "$VERSION_OUTPUT" ]; then
    echo "ERROR: Failed to retrieve PostgreSQL version." >&2
    exit 1
fi

if [ "$VERSION_OUTPUT" -lt 150000 ]; then
    echo "ERROR: PostgreSQL version must be 15 or higher. Detected version: $($PSQL_CMD -c 'SHOW server_version;')" >&2
    exit 1
fi

echo "PostgreSQL version is 15+ (server_version_num: $VERSION_OUTPUT). PASS."

echo "Checking for required extensions..."
EXTENSIONS=("pg_stat_statements" "pgaudit")

for ext in "${EXTENSIONS[@]}"; do
    EXT_CHECK=$($PSQL_CMD -c "SELECT count(*) FROM pg_extension WHERE extname = '$ext';")
    if [ "$EXT_CHECK" -eq 0 ]; then
        echo "WARNING: Extension '$ext' is not installed in database '$DBNAME'." >&2
    else
        echo "Extension '$ext' is installed. PASS."
    fi
done

echo "Version and extension checks completed successfully."
exit 0
