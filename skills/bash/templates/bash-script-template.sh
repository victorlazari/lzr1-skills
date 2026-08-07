#!/usr/bin/env bash
# Template for robust Bash scripts

# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error when substituting.
# The return value of a pipeline is the status of the last command to exit with a non-zero status.
set -euo pipefail

# Set Internal Field Separator to newline and tab to prevent unintended word splitting
IFS=$'\n\t'

# Function to display usage information
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Description of the script."
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
    # Add other options here
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
    esac
done

# Main script logic starts here
echo "Script execution started."

# Example function with local variables
example_function() {
    local arg1="$1"
    echo "Processing: $arg1"
}

# example_function "test"

echo "Script execution completed successfully."
exit 0
