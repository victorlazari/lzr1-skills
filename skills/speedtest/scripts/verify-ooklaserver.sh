#!/bin/bash
# verify-ooklaserver.sh
# Deterministic script to verify OoklaServer configuration, firewall rules, and security headers.

set -euo pipefail

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Verify OoklaServer configuration, firewall rules, and security headers."
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message"
    echo "  --dry-run     Perform a dry run without making any changes (default behavior as this is a read-only script)"
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    show_help
    exit 0
fi

echo "Starting OoklaServer verification..."

# 1. Check OpenSSL version
echo "Checking OpenSSL version..."
if command -v openssl >/dev/null 2>&1; then
    OPENSSL_VERSION=$(openssl version | awk '{print $2}')
    # Simple version check (requires 3.5.5+)
    # Note: In a real scenario, a more robust version comparison would be used.
    # For this script, we just report the version.
    echo "Found OpenSSL version: $OPENSSL_VERSION"
    # Basic check for 3.5.5 or higher
    if [[ $(echo -e "3.5.5\n$OPENSSL_VERSION" | sort -V | head -n1) != "3.5.5" ]]; then
        echo "WARNING: OpenSSL version $OPENSSL_VERSION may be lower than the required 3.5.5+."
    else
        echo "OpenSSL version is acceptable."
    fi
else
    echo "ERROR: OpenSSL is not installed."
    exit 1
fi

# 2. Check Firewall Rules (UDP 8080/5060)
echo "Checking firewall rules for UDP 8080 and 5060..."
# This is a read-only check. We simulate checking iptables/ufw.
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "active"; then
    if ufw status | grep -q "8080/udp" && ufw status | grep -q "5060/udp"; then
        echo "Firewall rules for UDP 8080 and 5060 are present in UFW."
    else
        echo "WARNING: Firewall rules for UDP 8080 and/or 5060 might be missing in UFW."
    fi
elif command -v iptables >/dev/null 2>&1; then
    # Requires root to run iptables -L, so we just print a message
    echo "iptables is installed. Please ensure UDP 8080 and 5060 are allowed."
else
    echo "No standard firewall (ufw/iptables) detected. Please verify manually."
fi

# 3. Check Security Headers (if server is running locally)
echo "Checking security headers on localhost:8080..."
if command -v curl >/dev/null 2>&1; then
    # We use a short timeout and ignore connection refused errors if the server isn't running
    HEADERS=$(curl -s -I -m 2 http://localhost:8080 || true)
    if [[ -n "$HEADERS" ]]; then
        if echo "$HEADERS" | grep -qi "Strict-Transport-Security"; then
            echo "HSTS header found."
        else
            echo "WARNING: HSTS header missing."
        fi
        if echo "$HEADERS" | grep -qi "X-Frame-Options"; then
            echo "X-Frame-Options header found."
        else
            echo "WARNING: X-Frame-Options header missing."
        fi
    else
        echo "OoklaServer does not appear to be running on localhost:8080 or is unreachable."
    fi
else
    echo "curl is not installed, skipping header check."
fi

echo "Verification complete."
exit 0
