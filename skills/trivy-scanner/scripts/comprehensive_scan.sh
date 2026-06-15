#!/usr/bin/env bash
# comprehensive_scan.sh - Run a full Trivy security analysis on a local repository
# Usage: bash comprehensive_scan.sh <repo_path> [output_dir]
#
# This script performs a comprehensive security scan including:
#   - Vulnerability scanning (all severities)
#   - Misconfiguration scanning (IaC checks)
#   - Secret detection
#   - License compliance checking
#   - SBOM generation (CycloneDX JSON)
#
# Outputs:
#   - Table report to stdout
#   - JSON report for programmatic analysis
#   - SARIF report for IDE/GitHub integration
#   - CycloneDX SBOM

set -euo pipefail

# --- Configuration ---
REPO_PATH="${1:-.}"
OUTPUT_DIR="${2:-./trivy-reports}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Functions ---
print_header() {
    echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"
}

print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_trivy() {
    if ! command -v trivy &> /dev/null; then
        print_error "Trivy is not installed. Installing..."
        # Attempt installation via common methods
        if command -v brew &> /dev/null; then
            brew install trivy
        elif command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y wget apt-transport-https gnupg lsb-release
            wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
            echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
            sudo apt-get update && sudo apt-get install -y trivy
        else
            print_error "Cannot auto-install Trivy. Please install manually: https://trivy.dev/docs/latest/getting-started/"
            exit 1
        fi
    fi
    print_step "Trivy version: $(trivy --version 2>/dev/null | head -1)"
}

update_db() {
    print_step "Updating Trivy vulnerability database..."
    trivy image --download-db-only 2>/dev/null || true
}

# --- Main Execution ---
print_header "TRIVY COMPREHENSIVE SECURITY ANALYSIS"
echo -e "  Target:     ${REPO_PATH}"
echo -e "  Output Dir: ${OUTPUT_DIR}"
echo -e "  Timestamp:  ${TIMESTAMP}"
echo ""

# Validate target
if [ ! -d "$REPO_PATH" ] && [[ ! "$REPO_PATH" =~ ^https?:// ]]; then
    print_error "Target path does not exist: $REPO_PATH"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check Trivy installation
check_trivy

# Update vulnerability database
update_db

# --- Phase 1: Full Vulnerability + Secret + Misconfig Scan (Table) ---
print_header "Phase 1: Full Security Scan (Table Output)"
trivy repo \
    --scanners vuln,misconfig,secret \
    --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
    "$REPO_PATH" 2>&1 | tee "$OUTPUT_DIR/scan_table_${TIMESTAMP}.txt"
print_step "Table report saved: $OUTPUT_DIR/scan_table_${TIMESTAMP}.txt"

# --- Phase 2: JSON Report ---
print_header "Phase 2: JSON Report Generation"
trivy repo \
    --scanners vuln,misconfig,secret \
    --format json \
    --output "$OUTPUT_DIR/scan_results_${TIMESTAMP}.json" \
    "$REPO_PATH"
print_step "JSON report saved: $OUTPUT_DIR/scan_results_${TIMESTAMP}.json"

# --- Phase 3: SARIF Report ---
print_header "Phase 3: SARIF Report Generation"
trivy repo \
    --scanners vuln,misconfig,secret \
    --format sarif \
    --output "$OUTPUT_DIR/scan_results_${TIMESTAMP}.sarif" \
    "$REPO_PATH"
print_step "SARIF report saved: $OUTPUT_DIR/scan_results_${TIMESTAMP}.sarif"

# --- Phase 4: License Scan ---
print_header "Phase 4: License Compliance Scan"
trivy repo \
    --scanners license \
    --format json \
    --output "$OUTPUT_DIR/license_results_${TIMESTAMP}.json" \
    "$REPO_PATH" 2>&1 || print_warn "License scan completed with findings"
print_step "License report saved: $OUTPUT_DIR/license_results_${TIMESTAMP}.json"

# --- Phase 5: SBOM Generation (CycloneDX) ---
print_header "Phase 5: SBOM Generation (CycloneDX)"
trivy repo \
    --format cyclonedx \
    --output "$OUTPUT_DIR/sbom_cyclonedx_${TIMESTAMP}.json" \
    "$REPO_PATH"
print_step "CycloneDX SBOM saved: $OUTPUT_DIR/sbom_cyclonedx_${TIMESTAMP}.json"

# --- Phase 6: SBOM Generation (SPDX) ---
print_header "Phase 6: SBOM Generation (SPDX)"
trivy repo \
    --format spdx-json \
    --output "$OUTPUT_DIR/sbom_spdx_${TIMESTAMP}.json" \
    "$REPO_PATH"
print_step "SPDX SBOM saved: $OUTPUT_DIR/sbom_spdx_${TIMESTAMP}.json"

# --- Phase 7: Critical/High Only (for CI gating) ---
print_header "Phase 7: Critical & High Findings Summary"
trivy repo \
    --scanners vuln,misconfig,secret \
    --severity HIGH,CRITICAL \
    --exit-code 0 \
    "$REPO_PATH" 2>&1 | tee "$OUTPUT_DIR/critical_high_${TIMESTAMP}.txt"
print_step "Critical/High summary saved: $OUTPUT_DIR/critical_high_${TIMESTAMP}.txt"

# --- Summary ---
print_header "SCAN COMPLETE"
echo -e "  All reports saved to: ${GREEN}${OUTPUT_DIR}/${NC}"
echo ""
echo "  Files generated:"
ls -la "$OUTPUT_DIR"/*"${TIMESTAMP}"* 2>/dev/null | awk '{print "    " $NF " (" $5 " bytes)"}'
echo ""

# Count findings from JSON report
if [ -f "$OUTPUT_DIR/scan_results_${TIMESTAMP}.json" ]; then
    if command -v python3 &> /dev/null; then
        python3 -c "
import json, sys
with open('$OUTPUT_DIR/scan_results_${TIMESTAMP}.json') as f:
    data = json.load(f)
total_vulns = 0
total_misconfig = 0
total_secrets = 0
for result in data.get('Results', []):
    for vuln in result.get('Vulnerabilities', []):
        total_vulns += 1
    for mc in result.get('Misconfigurations', []):
        total_misconfig += 1
    for sec in result.get('Secrets', []):
        total_secrets += 1
print(f'  Findings Summary:')
print(f'    Vulnerabilities:   {total_vulns}')
print(f'    Misconfigurations: {total_misconfig}')
print(f'    Secrets:           {total_secrets}')
print(f'    Total:             {total_vulns + total_misconfig + total_secrets}')
" 2>/dev/null || true
    fi
fi

echo ""
print_step "Comprehensive scan finished at $(date)"
