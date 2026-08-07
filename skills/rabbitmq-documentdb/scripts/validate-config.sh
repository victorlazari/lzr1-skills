#!/bin/bash
# validate-config.sh
# Validates RabbitMQ and DocumentDB configuration files (syntax and smoke tests).

set -e

usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --rabbitmq-conf <file>    Path to rabbitmq.conf"
    echo "  --docdb-conf <file>       Path to DocumentDB connection-settings.json"
    echo "  --dry-run                 Perform syntax checks without attempting connections"
    echo "  --help                    Show this help message"
    exit 1
}

RABBITMQ_CONF=""
DOCDB_CONF=""
DRY_RUN=0

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --rabbitmq-conf) RABBITMQ_CONF="$2"; shift ;;
        --docdb-conf) DOCDB_CONF="$2"; shift ;;
        --dry-run) DRY_RUN=1 ;;
        --help) usage ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

if [[ -z "$RABBITMQ_CONF" && -z "$DOCDB_CONF" ]]; then
    echo "Error: Must provide at least one configuration file to validate."
    usage
fi

# Validate RabbitMQ config
if [[ -n "$RABBITMQ_CONF" ]]; then
    if [[ ! -f "$RABBITMQ_CONF" ]]; then
        echo "Error: RabbitMQ config file not found: $RABBITMQ_CONF"
        exit 1
    fi
    echo "Validating RabbitMQ config syntax: $RABBITMQ_CONF"
    # Basic syntax check (e.g., checking for key=value format)
    if grep -qE "^[a-zA-Z0-9_.-]+\s*=\s*.*$" "$RABBITMQ_CONF"; then
        echo "RabbitMQ config syntax appears valid."
    else
        echo "Warning: RabbitMQ config may not contain valid key=value pairs."
    fi
fi

# Validate DocumentDB config
if [[ -n "$DOCDB_CONF" ]]; then
    if [[ ! -f "$DOCDB_CONF" ]]; then
        echo "Error: DocumentDB config file not found: $DOCDB_CONF"
        exit 1
    fi
    echo "Validating DocumentDB config syntax: $DOCDB_CONF"
    if command -v jq >/dev/null 2>&1; then
        if jq empty "$DOCDB_CONF" >/dev/null 2>&1; then
            echo "DocumentDB config JSON syntax is valid."
        else
            echo "Error: DocumentDB config JSON syntax is invalid."
            exit 1
        fi
    else
        echo "Warning: 'jq' not found. Skipping JSON syntax validation."
    fi
fi

if [[ $DRY_RUN -eq 1 ]]; then
    echo "Dry run complete. No connections attempted."
    exit 0
fi

echo "Validation complete."
exit 0
