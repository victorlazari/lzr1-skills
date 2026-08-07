#!/bin/bash
# Deterministic script to perform read-only discovery and validation of cluster state.

set -euo pipefail

# Help text
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  echo "Usage: $0 [OPTIONS]"
  echo "Perform read-only discovery and validation of EKS cluster state."
  echo ""
  echo "Options:"
  echo "  -h, --help    Show this help message and exit"
  echo "  --dry-run     Run in dry-run mode (simulates checks without executing kubectl)"
  exit 0
fi

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  echo "[INFO] Running in dry-run mode."
fi

echo "========================================"
echo "EKS Cluster Health Verification"
echo "========================================"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[DRY-RUN] Would check kubectl context..."
  echo "[DRY-RUN] Would check node readiness..."
  echo "[DRY-RUN] Would check pod health..."
  echo "[DRY-RUN] Would check CoreDNS status..."
  echo "[DRY-RUN] Would check VPC CNI status..."
  echo "========================================"
  echo "Dry-run completed successfully."
  exit 0
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
  echo "[ERROR] kubectl is not installed or not in PATH."
  exit 1
fi

# 1. Check Current Context
echo "[INFO] Current Context:"
kubectl config current-context || { echo "[ERROR] Failed to get current context."; exit 1; }
echo ""

# 2. Check Node Readiness
echo "[INFO] Node Status:"
NOT_READY_NODES=$(kubectl get nodes --field-selector=status.phase!=Running -o jsonpath='{.items[*].metadata.name}')
if [[ -n "$NOT_READY_NODES" ]]; then
  echo "[WARNING] The following nodes are NotReady:"
  echo "$NOT_READY_NODES"
else
  echo "[OK] All nodes are Ready."
fi
echo ""

# 3. Check Pod Health (CrashLoopBackOff, Error, Pending)
echo "[INFO] Pod Health (All Namespaces):"
UNHEALTHY_PODS=$(kubectl get pods -A --field-selector=status.phase!=Running | grep -v 'Completed' || true)
if [[ -n "$UNHEALTHY_PODS" && "$UNHEALTHY_PODS" != *"No resources found"* ]]; then
  echo "[WARNING] Found unhealthy pods:"
  echo "$UNHEALTHY_PODS"
else
  echo "[OK] No unhealthy pods found."
fi
echo ""

# 4. Check CoreDNS Status
echo "[INFO] CoreDNS Status:"
COREDNS_READY=$(kubectl get deployment coredns -n kube-system -o jsonpath='{.status.readyReplicas}' || echo "0")
COREDNS_DESIRED=$(kubectl get deployment coredns -n kube-system -o jsonpath='{.spec.replicas}' || echo "0")
if [[ "$COREDNS_READY" != "$COREDNS_DESIRED" ]]; then
  echo "[WARNING] CoreDNS is degraded ($COREDNS_READY/$COREDNS_DESIRED ready)."
else
  echo "[OK] CoreDNS is healthy ($COREDNS_READY/$COREDNS_DESIRED ready)."
fi
echo ""

# 5. Check VPC CNI (aws-node) Status
echo "[INFO] VPC CNI (aws-node) Status:"
AWS_NODE_READY=$(kubectl get daemonset aws-node -n kube-system -o jsonpath='{.status.numberReady}' || echo "0")
AWS_NODE_DESIRED=$(kubectl get daemonset aws-node -n kube-system -o jsonpath='{.status.desiredNumberScheduled}' || echo "0")
if [[ "$AWS_NODE_READY" != "$AWS_NODE_DESIRED" ]]; then
  echo "[WARNING] VPC CNI is degraded ($AWS_NODE_READY/$AWS_NODE_DESIRED ready)."
else
  echo "[OK] VPC CNI is healthy ($AWS_NODE_READY/$AWS_NODE_DESIRED ready)."
fi
echo ""

echo "========================================"
echo "Cluster health verification completed."
echo "========================================"
exit 0
