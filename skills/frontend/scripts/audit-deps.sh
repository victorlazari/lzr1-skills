#!/bin/bash

# audit-deps.sh
# Deterministic script to verify installed versions of React, Next.js, TypeScript, and Tailwind CSS.

set -e

echo "Auditing frontend dependencies..."

# Check if package.json exists
if [ ! -f "package.json" ]; then
  echo "Error: package.json not found in the current directory."
  exit 1
fi

# Function to check dependency version
check_dep() {
  local dep=$1
  local version=$(npm list "$dep" --depth=0 2>/dev/null | grep "$dep@" | awk -F@ '{print $2}')

  if [ -z "$version" ]; then
    echo "Warning: $dep is not installed."
  else
    echo "Found $dep version: $version"
  fi
}

check_dep "react"
check_dep "next"
check_dep "typescript"
check_dep "tailwindcss"

echo "Dependency audit complete."
exit 0
