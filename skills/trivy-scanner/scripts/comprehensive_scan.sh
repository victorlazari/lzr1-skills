#!/usr/bin/env bash
# Run a trust-gated Trivy evidence scan against one local repository.
# This script never installs Trivy, changes the target, uploads results, or edits ignores.

set -Eeuo pipefail
umask 077

DRY_RUN=0
TARGET=""
OUTPUT_DIR=""
CONFIG_FILE=""
IGNORE_FILE=""
TRUST_RECORD=""
TRUST_REVIEWED=0
EXPECTED_TRIVY_SHA256=""
SCANNERS="vuln,misconfig,secret,license"
SARIF_SCANNERS="vuln,misconfig,secret"
SEVERITIES="UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
GATE_SEVERITIES="HIGH,CRITICAL"
OFFLINE=0
SKIP_UPDATES=0
TRIVY_BIN=""
TRIVY_SHA256=""
TRUST_SHA256=""
GATE_STATUS="not-run"
OVERALL_STATUS="incomplete"
FINAL_EXIT=2
FAILURES=()

usage() {
  cat <<'EOF'
Usage:
  comprehensive_scan.sh --target DIR --output-dir DIR [options]

Required for execution:
  --target DIR                    Existing local repository directory
  --output-dir DIR                New evidence directory outside the target
  --trust-record FILE             Non-empty artifact-verification record
  --expected-trivy-sha256 HEX     Expected SHA-256 of the resolved Trivy executable
  --trust-reviewed                Confirm the trust record was reviewed

Options:
  --config FILE                   Explicit Trivy YAML config; ambient trivy.yaml is avoided
  --ignorefile FILE               Explicit ignore file
  --scanners LIST                 JSON/gate scanners (default: vuln,misconfig,secret,license)
  --sarif-scanners LIST           SARIF scanners (default: vuln,misconfig,secret)
  --severity LIST                 Discovery severities (default: all five levels)
  --gate-severity LIST            Blocking severities (default: HIGH,CRITICAL)
  --offline                       Use offline-scan and skip DB/Java/check updates
  --skip-updates                  Skip DB/Java/check updates without offline-scan
  --dry-run                       Validate paths and print commands; execute nothing
  --help                          Show this help

Exit codes:
  0   Evidence complete; policy gate passed
  10  Evidence complete; policy gate found matching findings
  2   Trust, execution, validation, or evidence failure; result is incomplete

Security properties:
  - Does not install or upgrade Trivy.
  - Requires an expected executable hash and a separate trust record.
  - Refuses an existing output directory and output paths inside the target.
  - Runs from the new evidence directory to avoid an ambient trivy.yaml.
  - Does not upload SARIF/SBOMs, push attestations, or modify the target.
EOF
}

log() { printf '[%s] %s\n' "$1" "$2" >&2; }
die() { log ERROR "$1"; exit 2; }

require_value() {
  [[ $# -ge 2 && -n ${2:-} ]] || die "Option $1 requires a value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) require_value "$@"; TARGET=$2; shift 2 ;;
    --output-dir) require_value "$@"; OUTPUT_DIR=$2; shift 2 ;;
    --config) require_value "$@"; CONFIG_FILE=$2; shift 2 ;;
    --ignorefile) require_value "$@"; IGNORE_FILE=$2; shift 2 ;;
    --trust-record) require_value "$@"; TRUST_RECORD=$2; shift 2 ;;
    --expected-trivy-sha256) require_value "$@"; EXPECTED_TRIVY_SHA256=${2,,}; shift 2 ;;
    --trust-reviewed) TRUST_REVIEWED=1; shift ;;
    --scanners) require_value "$@"; SCANNERS=$2; shift 2 ;;
    --sarif-scanners) require_value "$@"; SARIF_SCANNERS=$2; shift 2 ;;
    --severity) require_value "$@"; SEVERITIES=$2; shift 2 ;;
    --gate-severity) require_value "$@"; GATE_SEVERITIES=$2; shift 2 ;;
    --offline) OFFLINE=1; SKIP_UPDATES=1; shift ;;
    --skip-updates) SKIP_UPDATES=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
done

[[ -n $TARGET ]] || die "--target is required"
[[ -n $OUTPUT_DIR ]] || die "--output-dir is required"
[[ -d $TARGET ]] || die "Target is not an existing directory: $TARGET"
[[ -r $TARGET ]] || die "Target is not readable: $TARGET"

for cmd in realpath sha256sum python3; do
  command -v "$cmd" >/dev/null 2>&1 || die "Required command not found: $cmd"
done

TARGET=$(realpath "$TARGET")
OUTPUT_DIR=$(realpath -m "$OUTPUT_DIR")
[[ $TARGET != / ]] || die "Refusing to scan the filesystem root"
[[ ! -e $OUTPUT_DIR ]] || die "Output path already exists; choose a new directory: $OUTPUT_DIR"
case "$OUTPUT_DIR/" in
  "$TARGET"/*) die "Output directory must be outside the target" ;;
esac

if [[ -n $CONFIG_FILE ]]; then
  [[ -f $CONFIG_FILE && -r $CONFIG_FILE ]] || die "Config file is not readable: $CONFIG_FILE"
  CONFIG_FILE=$(realpath "$CONFIG_FILE")
fi
if [[ -n $IGNORE_FILE ]]; then
  [[ -f $IGNORE_FILE && -r $IGNORE_FILE ]] || die "Ignore file is not readable: $IGNORE_FILE"
  IGNORE_FILE=$(realpath "$IGNORE_FILE")
fi

[[ $SCANNERS =~ ^[a-z]+(,[a-z]+)*$ ]] || die "Invalid --scanners list"
[[ $SARIF_SCANNERS =~ ^[a-z]+(,[a-z]+)*$ ]] || die "Invalid --sarif-scanners list"
[[ $SEVERITIES =~ ^[A-Z]+(,[A-Z]+)*$ ]] || die "Invalid --severity list"
[[ $GATE_SEVERITIES =~ ^[A-Z]+(,[A-Z]+)*$ ]] || die "Invalid --gate-severity list"

if [[ $DRY_RUN -eq 0 ]]; then
  [[ -n $TRUST_RECORD ]] || die "--trust-record is required for execution"
  [[ -s $TRUST_RECORD && -r $TRUST_RECORD ]] || die "Trust record must be a non-empty readable file"
  TRUST_RECORD=$(realpath "$TRUST_RECORD")
  [[ $TRUST_REVIEWED -eq 1 ]] || die "--trust-reviewed is required for execution"
  [[ $EXPECTED_TRIVY_SHA256 =~ ^[0-9a-f]{64}$ ]] || die "--expected-trivy-sha256 must be 64 hexadecimal characters"

  TRIVY_BIN=$(type -P trivy || true)
  [[ -n $TRIVY_BIN ]] || die "Trivy executable not found; automatic installation is disabled"
  TRIVY_BIN=$(realpath "$TRIVY_BIN")
  TRIVY_SHA256=$(sha256sum "$TRIVY_BIN" | awk '{print $1}')
  [[ $TRIVY_SHA256 == "$EXPECTED_TRIVY_SHA256" ]] || die "Trivy executable hash does not match the reviewed expected hash"
  TRUST_SHA256=$(sha256sum "$TRUST_RECORD" | awk '{print $1}')
else
  TRIVY_BIN=${TRIVY_BIN:-trivy}
fi

GLOBAL_ARGS=()
[[ -n $CONFIG_FILE ]] && GLOBAL_ARGS+=(--config "$CONFIG_FILE")
IGNORE_ARGS=()
[[ -n $IGNORE_FILE ]] && IGNORE_ARGS+=(--ignorefile "$IGNORE_FILE")
FIRST_RUN_DATA_ARGS=()
CONSISTENT_DATA_ARGS=(--skip-db-update --skip-java-db-update --skip-check-update)
if [[ $SKIP_UPDATES -eq 1 ]]; then
  FIRST_RUN_DATA_ARGS+=(--skip-db-update --skip-java-db-update --skip-check-update)
fi
if [[ $OFFLINE -eq 1 ]]; then
  FIRST_RUN_DATA_ARGS+=(--offline-scan)
  CONSISTENT_DATA_ARGS+=(--offline-scan)
fi

CANONICAL_JSON="$OUTPUT_DIR/trivy.json"
SARIF_JSON="$OUTPUT_DIR/trivy.sarif"
CYCLONEDX_JSON="$OUTPUT_DIR/sbom.cdx.json"
SPDX_JSON="$OUTPUT_DIR/sbom.spdx.json"
GATE_JSON="$OUTPUT_DIR/gate.json"

CANONICAL_CMD=("$TRIVY_BIN" "${GLOBAL_ARGS[@]}" repo --scanners "$SCANNERS" --severity "$SEVERITIES" --exit-code 0 "${IGNORE_ARGS[@]}" "${FIRST_RUN_DATA_ARGS[@]}" --format json --output "$CANONICAL_JSON" "$TARGET")
SARIF_CMD=("$TRIVY_BIN" "${GLOBAL_ARGS[@]}" repo --scanners "$SARIF_SCANNERS" --severity "$SEVERITIES" --exit-code 0 "${IGNORE_ARGS[@]}" "${CONSISTENT_DATA_ARGS[@]}" --format sarif --output "$SARIF_JSON" "$TARGET")
CYCLONEDX_CMD=("$TRIVY_BIN" "${GLOBAL_ARGS[@]}" repo "${CONSISTENT_DATA_ARGS[@]}" --format cyclonedx --output "$CYCLONEDX_JSON" "$TARGET")
SPDX_CMD=("$TRIVY_BIN" "${GLOBAL_ARGS[@]}" repo "${CONSISTENT_DATA_ARGS[@]}" --format spdx-json --output "$SPDX_JSON" "$TARGET")
GATE_CMD=("$TRIVY_BIN" "${GLOBAL_ARGS[@]}" repo --scanners "$SCANNERS" --severity "$GATE_SEVERITIES" --exit-code 10 "${IGNORE_ARGS[@]}" "${CONSISTENT_DATA_ARGS[@]}" --format json --output "$GATE_JSON" "$TARGET")

print_cmd() {
  printf '  '
  printf '%q ' "$@"
  printf '\n'
}

if [[ $DRY_RUN -eq 1 ]]; then
  cat <<EOF
DRY RUN: no directories will be created and no scanner will execute.
Target: $TARGET
Output: $OUTPUT_DIR
Execution additionally requires a reviewed trust record and expected Trivy executable SHA-256.
Planned commands:
EOF
  print_cmd "${CANONICAL_CMD[@]}"
  print_cmd "${SARIF_CMD[@]}"
  print_cmd "${CYCLONEDX_CMD[@]}"
  print_cmd "${SPDX_CMD[@]}"
  print_cmd "${GATE_CMD[@]}"
  exit 0
fi

mkdir -p "$OUTPUT_DIR"
chmod 700 "$OUTPUT_DIR"

# Run from the empty evidence directory so an unrelated ./trivy.yaml is not loaded.
cd "$OUTPUT_DIR"

"$TRIVY_BIN" --version >trivy-version.txt 2>trivy-version.stderr.log || {
  FAILURES+=("Unable to execute the hash-verified Trivy binary for version capture")
}
printf '%s\n' "$TRIVY_BIN" >trivy-executable-path.txt
printf '%s  %s\n' "$TRIVY_SHA256" "$TRIVY_BIN" >trivy-executable.sha256
printf '%s  %s\n' "$TRUST_SHA256" "$TRUST_RECORD" >trust-record.sha256
printf '%s\n' "$TARGET" >target-path.txt
env | sed -n 's/^\(TRIVY_[A-Za-z0-9_]*\)=.*/\1/p' | LC_ALL=C sort >trivy-environment-variable-names.txt

GIT_COMMIT=""
GIT_DIRTY="unknown"
if command -v git >/dev/null 2>&1 && git -C "$TARGET" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  GIT_COMMIT=$(git -C "$TARGET" rev-parse HEAD 2>/dev/null || true)
  if [[ -n $(git -C "$TARGET" status --porcelain --untracked-files=normal 2>/dev/null || true) ]]; then
    GIT_DIRTY="true"
  else
    GIT_DIRTY="false"
  fi
fi

{
  printf 'Generated: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'Target: %s\n' "$TARGET"
  printf 'Target commit: %s\n' "${GIT_COMMIT:-not-detected}"
  printf 'Target dirty: %s\n' "$GIT_DIRTY"
  printf 'Config SHA-256: %s\n' "$([[ -n $CONFIG_FILE ]] && sha256sum "$CONFIG_FILE" | awk '{print $1}' || printf 'none')"
  printf 'Ignore SHA-256: %s\n' "$([[ -n $IGNORE_FILE ]] && sha256sum "$IGNORE_FILE" | awk '{print $1}' || printf 'none')"
  printf 'Commands:\n'
  print_cmd "${CANONICAL_CMD[@]}"
  print_cmd "${SARIF_CMD[@]}"
  print_cmd "${CYCLONEDX_CMD[@]}"
  print_cmd "${SPDX_CMD[@]}"
  print_cmd "${GATE_CMD[@]}"
} >scan-plan.txt

run_logged() {
  local label=$1
  shift
  local rc
  log INFO "Running $label"
  if "$@" >"${label}.stdout.log" 2>"${label}.stderr.log"; then
    rc=0
  else
    rc=$?
  fi
  printf '%s\n' "$rc" >"${label}.exit-code"
  return "$rc"
}

validate_json() {
  local path=$1
  python3 - "$path" <<'PY'
import json
import sys
from pathlib import Path
p = Path(sys.argv[1])
if not p.is_file() or p.stat().st_size == 0:
    raise SystemExit(f"missing or empty JSON artifact: {p}")
with p.open("r", encoding="utf-8") as handle:
    json.load(handle)
PY
}

finalize() {
  local outcome=$1
  local gate=$2
  printf '%s\n' "${FAILURES[@]:-}" | sed '/^$/d' >failures.txt
  python3 - "$OUTPUT_DIR" "$TARGET" "$GIT_COMMIT" "$GIT_DIRTY" "$TRIVY_BIN" "$TRIVY_SHA256" "$TRUST_RECORD" "$TRUST_SHA256" "$CONFIG_FILE" "$IGNORE_FILE" "$SCANNERS" "$SARIF_SCANNERS" "$SEVERITIES" "$GATE_SEVERITIES" "$outcome" "$gate" <<'PY'
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
(
    out, target, commit, dirty, trivy_bin, trivy_sha, trust_path, trust_sha,
    config_path, ignore_path, scanners, sarif_scanners, severities,
    gate_severities, outcome, gate,
) = sys.argv[1:]
out_path = Path(out)
failures_path = out_path / "failures.txt"
failures = failures_path.read_text(encoding="utf-8").splitlines() if failures_path.exists() else []

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

artifacts = []
for path in sorted(out_path.iterdir(), key=lambda p: p.name):
    if path.is_file() and path.name not in {"manifest.json", "SHA256SUMS"}:
        artifacts.append({
            "path": path.name,
            "bytes": path.stat().st_size,
            "sha256": file_hash(path),
        })
manifest = {
    "schema_version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "outcome": outcome,
    "gate_status": gate,
    "failures": failures,
    "target": {"path": target, "git_commit": commit or None, "git_dirty": dirty},
    "scanner": {"path": trivy_bin, "sha256": trivy_sha},
    "trust_record": {"path": trust_path, "sha256": trust_sha},
    "configuration": {
        "config_path": config_path or None,
        "ignore_path": ignore_path or None,
        "scanners": scanners.split(","),
        "sarif_scanners": sarif_scanners.split(","),
        "severities": severities.split(","),
        "gate_severities": gate_severities.split(","),
    },
    "artifacts": artifacts,
}
(out_path / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
PY
  (
    cd "$OUTPUT_DIR"
    find . -maxdepth 1 -type f ! -name SHA256SUMS -print0 \
      | LC_ALL=C sort -z \
      | xargs -0 sha256sum >SHA256SUMS
  )
}

if ! run_logged canonical "${CANONICAL_CMD[@]}"; then
  FAILURES+=("Canonical scan execution failed; see canonical.stderr.log")
  OVERALL_STATUS="incomplete"
  GATE_STATUS="not-run"
  finalize "$OVERALL_STATUS" "$GATE_STATUS"
  exit 2
fi
if ! validate_json "$CANONICAL_JSON"; then
  FAILURES+=("Canonical Trivy JSON is missing, empty, or invalid")
fi

if ! python3 - "$CANONICAL_JSON" "$OUTPUT_DIR/summary.json" <<'PY'
import json
import sys
from collections import Counter
from pathlib import Path
source, destination = map(Path, sys.argv[1:])
data = json.loads(source.read_text(encoding="utf-8"))
counts = Counter()
for result in data.get("Results") or []:
    if not isinstance(result, dict):
        continue
    for field in ("Vulnerabilities", "Misconfigurations", "Secrets", "Licenses"):
        for finding in result.get(field) or []:
            if isinstance(finding, dict):
                counts[f"{field}:{finding.get('Severity', 'UNKNOWN')}"] += 1
summary = {
    "schema_version": data.get("SchemaVersion"),
    "artifact_name": data.get("ArtifactName"),
    "artifact_type": data.get("ArtifactType"),
    "result_groups": len(data.get("Results") or []),
    "counts": dict(sorted(counts.items())),
    "total_findings": sum(counts.values()),
}
destination.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
PY
then
  FAILURES+=("Canonical JSON summary generation failed")
fi

if ! run_logged sarif "${SARIF_CMD[@]}"; then
  FAILURES+=("SARIF generation failed; see sarif.stderr.log")
elif ! validate_json "$SARIF_JSON"; then
  FAILURES+=("SARIF artifact is missing, empty, or invalid JSON")
fi

if ! run_logged cyclonedx "${CYCLONEDX_CMD[@]}"; then
  FAILURES+=("CycloneDX generation failed; see cyclonedx.stderr.log")
elif ! validate_json "$CYCLONEDX_JSON"; then
  FAILURES+=("CycloneDX artifact is missing, empty, or invalid JSON")
fi

if ! run_logged spdx "${SPDX_CMD[@]}"; then
  FAILURES+=("SPDX generation failed; see spdx.stderr.log")
elif ! validate_json "$SPDX_JSON"; then
  FAILURES+=("SPDX artifact is missing, empty, or invalid JSON")
fi

if run_logged gate "${GATE_CMD[@]}"; then
  GATE_STATUS="pass"
else
  gate_rc=$?
  if [[ $gate_rc -eq 10 ]]; then
    GATE_STATUS="fail"
  else
    GATE_STATUS="incomplete"
    FAILURES+=("Gate execution failed with exit code $gate_rc; see gate.stderr.log")
  fi
fi
if [[ -f $GATE_JSON ]] && ! validate_json "$GATE_JSON"; then
  FAILURES+=("Gate JSON is missing, empty, or invalid")
  GATE_STATUS="incomplete"
fi

if [[ ${#FAILURES[@]} -gt 0 || $GATE_STATUS == incomplete ]]; then
  OVERALL_STATUS="incomplete"
  FINAL_EXIT=2
elif [[ $GATE_STATUS == fail ]]; then
  OVERALL_STATUS="fail"
  FINAL_EXIT=10
else
  OVERALL_STATUS="pass"
  FINAL_EXIT=0
fi

finalize "$OVERALL_STATUS" "$GATE_STATUS"
log INFO "Outcome: $OVERALL_STATUS; gate: $GATE_STATUS; evidence: $OUTPUT_DIR"
exit "$FINAL_EXIT"
