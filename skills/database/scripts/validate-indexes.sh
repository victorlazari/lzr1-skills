#!/bin/bash
# Script to verify that proposed indexes are supported by the target database version.

set -e

show_help() {
    echo "Usage: $0 --db <postgres|mongodb> --version <version> --index-type <type>"
    echo "Example: $0 --db postgres --version 16 --index-type btree"
}

if [ "$#" -eq 0 ]; then
    show_help
    exit 1
fi

DB=""
VERSION=""
INDEX_TYPE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --db) DB="$2"; shift ;;
        --version) VERSION="$2"; shift ;;
        --index-type) INDEX_TYPE="$2"; shift ;;
        --help) show_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$DB" ] || [ -z "$VERSION" ] || [ -z "$INDEX_TYPE" ]; then
    echo "Error: Missing required parameters."
    show_help
    exit 1
fi

echo "Validating index type '$INDEX_TYPE' for $DB version $VERSION..."

if [ "$DB" == "postgres" ]; then
    if [[ "$INDEX_TYPE" =~ ^(btree|hash|gist|gin|brin|sp-gist|pgvector)$ ]]; then
        echo "PASS: Index type '$INDEX_TYPE' is supported in PostgreSQL $VERSION."
        exit 0
    else
        echo "FAIL: Index type '$INDEX_TYPE' is not recognized for PostgreSQL."
        exit 1
    fi
elif [ "$DB" == "mongodb" ]; then
    if [[ "$INDEX_TYPE" =~ ^(single|compound|multikey|text|geospatial|hashed|ttl|vector)$ ]]; then
        echo "PASS: Index type '$INDEX_TYPE' is supported in MongoDB $VERSION."
        exit 0
    else
        echo "FAIL: Index type '$INDEX_TYPE' is not recognized for MongoDB."
        exit 1
    fi
else
    echo "Error: Unsupported database '$DB'."
    exit 1
fi
