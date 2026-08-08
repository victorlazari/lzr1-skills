#!/usr/bin/env bash
# Check installed versions of common infrastructure tools without string execution.

set -euo pipefail

if [[ ${1:-} == "--help" ]]; then
    cat <<'EOF'
Usage: check-versions.sh
Checks whether common infrastructure tools are installed and reports their
self-declared versions. This script does not download, update, or modify tools.
EOF
    exit 0
fi

if [[ $# -gt 0 ]]; then
    printf 'Error: unknown argument: %s\n' "$1" >&2
    exit 2
fi

first_line() {
    local text=$1
    printf '%s\n' "${text%%$'\n'*}"
}

probe_version() {
    local tool=$1
    local output

    case $tool in
        terraform)
            output=$(terraform version 2>&1) || return 1
            first_line "$output"
            ;;
        kubectl)
            if output=$(kubectl version --client -o yaml 2>&1); then
                printf '%s\n' "$output" | awk -F': ' '/^[[:space:]]*gitVersion:/{print $2; found=1; exit} END{if (!found) exit 1}'
            else
                output=$(kubectl version --client 2>&1) || return 1
                first_line "$output"
            fi
            ;;
        helm)
            helm version --short 2>&1
            ;;
        aws)
            aws --version 2>&1
            ;;
        gcloud)
            output=$(gcloud version 2>&1) || return 1
            first_line "$output"
            ;;
        az)
            az version --query '"azure-cli"' --output tsv 2>&1
            ;;
        *)
            printf 'unsupported probe: %s\n' "$tool" >&2
            return 2
            ;;
    esac
}

check_tool() {
    local tool=$1
    local version

    if ! command -v "$tool" >/dev/null 2>&1; then
        printf '[WARN] %s is not installed.\n' "$tool"
        return 0
    fi

    if version=$(probe_version "$tool"); then
        printf '[PASS] %s is installed: %s\n' "$tool" "$version"
    else
        printf '[WARN] %s is installed, but its version probe failed.\n' "$tool"
    fi
}

printf '%s\n' 'Checking infrastructure tools...'
for tool in terraform kubectl helm aws gcloud az; do
    check_tool "$tool"
done
printf '%s\n' 'Version check complete.'
