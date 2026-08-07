#!/bin/bash
set -euo pipefail

# Deterministic script to execute Playwright tests with safe defaults and error handling.

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run Playwright tests safely."
    echo ""
    echo "Options:"
    echo "  --project <name>   Run tests for a specific project (e.g., chromium, firefox)"
    echo "  --grep <pattern>   Run tests matching the pattern"
    echo "  --dry-run          Preview the command without executing"
    echo "  --help             Show this help message"
}

PROJECT=""
GREP=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT="$2"
            shift 2
            ;;
        --grep)
            GREP="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

CMD="npx playwright test"

if [[ -n "$PROJECT" ]]; then
    CMD="$CMD --project=\"$PROJECT\""
fi

if [[ -n "$GREP" ]]; then
    CMD="$CMD --grep=\"$GREP\""
fi

if [[ $DRY_RUN -eq 1 ]]; then
    echo "Dry run mode. Would execute:"
    echo "$CMD"
    exit 0
fi

echo "Executing: $CMD"
eval "$CMD"
