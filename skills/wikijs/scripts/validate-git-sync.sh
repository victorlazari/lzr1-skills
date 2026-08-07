#!/bin/bash
# validate-git-sync.sh
# Deterministic script to verify Git storage configuration and connectivity.

set -euo pipefail

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Verify Git connectivity for Wiki.js storage sync."
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message"
    echo "  -r, --repo URL   Git repository URL to test (e.g., git@github.com:user/repo.git)"
}

REPO_URL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -r|--repo)
            REPO_URL="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [[ -z "$REPO_URL" ]]; then
    echo "Error: Repository URL is required."
    show_help
    exit 1
fi

echo "Validating Git connectivity to: $REPO_URL"

# Extract host from SSH URL (e.g., git@github.com:user/repo.git -> github.com)
if [[ "$REPO_URL" == git@* ]]; then
    HOST=$(echo "$REPO_URL" | cut -d'@' -f2 | cut -d':' -f1)
    echo "Testing SSH connectivity to $HOST..."

    # Use ssh -T to test connection. It usually returns 1 for successful auth but no shell access (like GitHub).
    # We use a timeout to prevent hanging.
    if timeout 10 ssh -T -o StrictHostKeyChecking=no "git@$HOST" 2>&1 | grep -q -E "successfully authenticated|Welcome to"; then
        echo "SSH connectivity test passed."
    else
        echo "Warning: SSH connectivity test failed or returned unexpected output. Please verify your SSH keys."
        # We don't exit 1 here because some Git servers might not respond to ssh -T in the expected way.
    fi
else
    echo "Note: URL does not appear to be an SSH URL. Skipping SSH connectivity test."
fi

# Attempt to run git ls-remote to verify access to the repository
echo "Testing repository access with git ls-remote..."
if git ls-remote "$REPO_URL" > /dev/null 2>&1; then
    echo "Success: Successfully accessed the repository."
    exit 0
else
    echo "Error: Failed to access the repository. Please check the URL and your credentials."
    exit 1
fi
