#!/usr/bin/env bash
# setup_ignore.sh - Create or update .trivyignore / .trivyignore.yaml files
# Usage: bash setup_ignore.sh <format> <target_dir> [finding_ids...]
#
# Arguments:
#   format     - "plain" for .trivyignore or "yaml" for .trivyignore.yaml
#   target_dir - Directory where the ignore file will be created
#   finding_ids - Space-separated list of CVE IDs or finding IDs to ignore
#
# Examples:
#   bash setup_ignore.sh plain ./myrepo CVE-2023-1234 CVE-2023-5678
#   bash setup_ignore.sh yaml ./myrepo CVE-2023-1234 AVD-DS-0002

set -euo pipefail

FORMAT="${1:-plain}"
TARGET_DIR="${2:-.}"
shift 2 || true
FINDING_IDS=("$@")

TIMESTAMP=$(date +%Y-%m-%d)

if [ "$FORMAT" = "yaml" ]; then
    IGNORE_FILE="$TARGET_DIR/.trivyignore.yaml"
    echo "# Trivy Ignore File (YAML format)"  > "$IGNORE_FILE"
    echo "# Generated: $TIMESTAMP"           >> "$IGNORE_FILE"
    echo "# Documentation: https://trivy.dev/docs/latest/configuration/filtering/" >> "$IGNORE_FILE"
    echo ""                                   >> "$IGNORE_FILE"
    echo "vulnerabilities:"                   >> "$IGNORE_FILE"

    for id in "${FINDING_IDS[@]}"; do
        if [[ "$id" =~ ^CVE- ]] || [[ "$id" =~ ^GHSA- ]]; then
            echo "  - id: $id"               >> "$IGNORE_FILE"
            echo "    # reason: \"TODO: Add justification\"" >> "$IGNORE_FILE"
            echo "    # expires: $(date -d '+90 days' +%Y-%m-%d 2>/dev/null || date -v+90d +%Y-%m-%d 2>/dev/null || echo '2025-12-31')" >> "$IGNORE_FILE"
        fi
    done

    echo ""                                   >> "$IGNORE_FILE"
    echo "misconfigurations:"                 >> "$IGNORE_FILE"

    for id in "${FINDING_IDS[@]}"; do
        if [[ "$id" =~ ^AVD- ]]; then
            echo "  - id: $id"               >> "$IGNORE_FILE"
            echo "    # reason: \"TODO: Add justification\"" >> "$IGNORE_FILE"
        fi
    done

    echo ""                                   >> "$IGNORE_FILE"
    echo "secrets:"                           >> "$IGNORE_FILE"
    echo "  # - id: <secret-rule-id>"        >> "$IGNORE_FILE"
    echo "  #   path: \"path/to/file\""      >> "$IGNORE_FILE"

else
    IGNORE_FILE="$TARGET_DIR/.trivyignore"
    echo "# Trivy Ignore File"               > "$IGNORE_FILE"
    echo "# Generated: $TIMESTAMP"           >> "$IGNORE_FILE"
    echo "# Documentation: https://trivy.dev/docs/latest/configuration/filtering/" >> "$IGNORE_FILE"
    echo "# Format: One finding ID per line" >> "$IGNORE_FILE"
    echo "# Supported: CVE IDs, GHSA IDs, AVD IDs" >> "$IGNORE_FILE"
    echo ""                                   >> "$IGNORE_FILE"

    for id in "${FINDING_IDS[@]}"; do
        echo "# TODO: Add justification for ignoring $id" >> "$IGNORE_FILE"
        echo "$id"                            >> "$IGNORE_FILE"
    done
fi

echo "Created ignore file: $IGNORE_FILE"
echo "Contents:"
cat "$IGNORE_FILE"
