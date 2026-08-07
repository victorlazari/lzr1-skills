#!/bin/bash

# Script to validate n8n workflow JSON structure
# Usage: ./validate-workflow.sh <path-to-workflow.json>

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <path-to-workflow.json>"
  exit 1
fi

WORKFLOW_FILE="$1"

if [ ! -f "$WORKFLOW_FILE" ]; then
  echo "Error: File not found: $WORKFLOW_FILE"
  exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
  echo "Error: jq is required but not installed."
  exit 1
fi

# Validate JSON syntax
if ! jq empty "$WORKFLOW_FILE" > /dev/null 2>&1; then
  echo "Error: Invalid JSON syntax in $WORKFLOW_FILE"
  exit 1
fi

# Basic n8n workflow structure validation
if ! jq -e '.nodes and .connections' "$WORKFLOW_FILE" > /dev/null 2>&1; then
  echo "Error: Invalid n8n workflow structure. Missing 'nodes' or 'connections' arrays."
  exit 1
fi

echo "Validation passed: $WORKFLOW_FILE appears to be a valid n8n workflow JSON."
exit 0
