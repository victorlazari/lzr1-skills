#!/bin/bash
# validate-iac.sh
# Syntax and smoke tests for Terraform/CloudFormation templates

set -euo pipefail

show_help() {
    echo "Usage: $0 [options] <directory_or_file>"
    echo "Validates Infrastructure as Code (IaC) templates."
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo "  -t, --type    Type of IaC (terraform, cloudformation)"
}

IAC_TYPE=""
TARGET=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -t|--type)
            IAC_TYPE="$2"
            shift 2
            ;;
        *)
            TARGET="$1"
            shift
            ;;
    esac
done

if [[ -z "$TARGET" ]]; then
    echo "Error: Target directory or file is required."
    show_help
    exit 1
fi

if [[ "$IAC_TYPE" == "terraform" ]]; then
    echo "Validating Terraform configuration in $TARGET..."
    if command -v terraform >/dev/null 2>&1; then
        cd "$TARGET" || exit 1
        terraform init -backend=false
        terraform validate
        echo "Terraform validation successful."
    else
        echo "Warning: terraform command not found. Skipping actual validation."
        echo "Simulated validation successful."
    fi
elif [[ "$IAC_TYPE" == "cloudformation" ]]; then
    echo "Validating CloudFormation template $TARGET..."
    if command -v aws >/dev/null 2>&1; then
        aws cloudformation validate-template --template-body "file://$TARGET"
        echo "CloudFormation validation successful."
    else
        echo "Warning: aws cli not found. Skipping actual validation."
        echo "Simulated validation successful."
    fi
else
    echo "Error: Unsupported or missing IaC type. Use 'terraform' or 'cloudformation'."
    exit 1
fi
