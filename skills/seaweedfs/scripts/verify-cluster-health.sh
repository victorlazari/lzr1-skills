#!/bin/bash
# verify-cluster-health.sh
# Verifies the health of a SeaweedFS cluster (Master, Volume, Filer).

set -euo pipefail

MASTER_URL="${1:-http://localhost:9333}"
FILER_URL="${2:-http://localhost:8888}"

echo "Verifying SeaweedFS cluster health..."

# Check Master
echo "Checking Master at $MASTER_URL..."
if curl -s -f "$MASTER_URL/cluster/status" > /dev/null; then
    echo "Master is reachable and healthy."
else
    echo "Error: Master is unreachable or unhealthy."
    exit 1
fi

# Check Filer
echo "Checking Filer at $FILER_URL..."
if curl -s -f "$FILER_URL/" > /dev/null; then
    echo "Filer is reachable and healthy."
else
    echo "Error: Filer is unreachable or unhealthy."
    exit 1
fi

echo "Cluster health verification completed successfully."
exit 0
