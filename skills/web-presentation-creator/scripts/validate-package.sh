#!/bin/bash
# Validates the generated HTML/ZIP package for structure and required assets.

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-to-package-or-html>"
    exit 1
fi

TARGET="$1"

if [ ! -e "$TARGET" ]; then
    echo "Error: Target '$TARGET' does not exist."
    exit 1
fi

if [[ "$TARGET" == *.zip ]]; then
    echo "Validating ZIP package..."
    unzip -l "$TARGET" | grep -q "index.html" || { echo "Error: ZIP package must contain index.html"; exit 1; }
    echo "ZIP package validation passed."
elif [[ "$TARGET" == *.html ]]; then
    echo "Validating HTML file..."
    grep -q "<!DOCTYPE html>" "$TARGET" || { echo "Error: HTML file must start with <!DOCTYPE html>"; exit 1; }
    grep -q "<html" "$TARGET" || { echo "Error: HTML file must contain <html> tag"; exit 1; }
    grep -q "<head" "$TARGET" || { echo "Error: HTML file must contain <head> tag"; exit 1; }
    grep -q "<body" "$TARGET" || { echo "Error: HTML file must contain <body> tag"; exit 1; }
    echo "HTML file validation passed."
else
    echo "Error: Target must be a .zip or .html file."
    exit 1
fi
