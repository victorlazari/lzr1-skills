#!/usr/bin/env bash
set -euo pipefail

# Deterministic wrapper for Playwright tests with argument-safe command construction.

show_help() {
    cat <<'EOF'
Usage: run-tests.sh [OPTIONS]
Run Playwright tests safely.

Options:
  --project <name>   Run tests for a specific project (for example, chromium)
  --grep <pattern>   Run tests matching the pattern
  --dry-run          Preview the exact argv without executing it
  -h, --help         Show this help message
EOF
}

fail() {
    printf 'Error: %s\n' "$1" >&2
    exit 2
}

require_value() {
    local option_name=$1
    local remaining=$2
    if [[ $remaining -lt 2 ]]; then
        fail "$option_name requires a value"
    fi
}

print_command() {
    local arg
    printf '  '
    for arg in "$@"; do
        printf '%q ' "$arg"
    done
    printf '\n'
}

PROJECT=""
GREP_PATTERN=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            require_value "$1" "$#"
            PROJECT=$2
            shift 2
            ;;
        --grep)
            require_value "$1" "$#"
            GREP_PATTERN=$2
            shift 2
            ;;
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --)
            shift
            [[ $# -eq 0 ]] || fail "positional arguments are not supported"
            ;;
        *)
            fail "unknown option: $1"
            ;;
    esac
done

command_argv=(npx playwright test)

if [[ -n $PROJECT ]]; then
    command_argv+=(--project "$PROJECT")
fi

if [[ -n $GREP_PATTERN ]]; then
    command_argv+=(--grep "$GREP_PATTERN")
fi

if [[ $DRY_RUN -eq 1 ]]; then
    printf '%s\n' 'Dry run mode. Would execute:'
    print_command "${command_argv[@]}"
    exit 0
fi

printf '%s\n' 'Executing:'
print_command "${command_argv[@]}"
exec "${command_argv[@]}"
