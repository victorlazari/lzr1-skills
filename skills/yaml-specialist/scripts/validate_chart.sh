#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART=""
RELEASE="yaml-specialist"
NAMESPACE="default"
KUBE_VERSION=""
OUTPUT_DIR=""
POD_SECURITY_PROFILE="baseline"
ALLOW_NETWORK=false
BUILD_DEPENDENCIES=false
ALLOW_CLUSTER=false
SERVER_DRY_RUN=false
KUBE_CONTEXT=""
SKIP_CONTRACT=false
SKIP_SCHEMA=false
SKIP_TEMPLATE=false
VALUES_FILES=()
SCHEMA_LOCATIONS=()
ALLOWED_EXTERNAL_REFS=()

usage() {
  cat <<'EOF'
Usage: validate_chart.sh --chart PATH [options]

Core options:
  --release NAME                  Helm release name (default: yaml-specialist)
  --namespace NAME               Render namespace (default: default)
  --kube-version VERSION         Explicit Kubernetes compatibility target
  --values LABEL=PATH            Additional values scenario; repeat as needed
  --output-dir PATH              New or empty private evidence directory
  --pod-security-profile VALUE   none, baseline, or restricted (default: baseline)
  --allow-external-ref VALUE     Kind/name or Kind/namespace/name; repeat explicitly

Dependency and schema options:
  --build-dependencies           Build dependencies in the copied chart only
  --allow-network                Permit explicitly requested dependency/schema network access
  --schema-location VALUE        Explicit kubeconform schema location; repeat as needed

Authorized API-server validation:
  --server-dry-run               Run kubectl apply --dry-run=server for rendered scenarios
  --allow-cluster                Required acknowledgement for --server-dry-run
  --context NAME                 Required exact kubectl context for --server-dry-run

Assessment-only exceptions (force an incomplete result):
  --skip-contract                Skip exhaustive values contract lint
  --skip-schema                  Skip values.schema.json validation
  --skip-template                Skip values-template reconciliation and scenario
  -h, --help                     Show help

Defaults are network-free and cluster-free. The script never installs or upgrades a
release. Server dry-run can invoke admission webhooks and is therefore gated by both
--server-dry-run and --allow-cluster. Rendered evidence may contain sensitive values;
its directory and files are created with owner-only permissions.
EOF
}

while (($#)); do
  case "$1" in
    --chart) CHART="${2:?--chart requires a path}"; shift 2 ;;
    --release) RELEASE="${2:?--release requires a name}"; shift 2 ;;
    --namespace) NAMESPACE="${2:?--namespace requires a name}"; shift 2 ;;
    --kube-version) KUBE_VERSION="${2:?--kube-version requires a version}"; shift 2 ;;
    --values) VALUES_FILES+=("${2:?--values requires LABEL=PATH}"); shift 2 ;;
    --output-dir) OUTPUT_DIR="${2:?--output-dir requires a path}"; shift 2 ;;
    --pod-security-profile) POD_SECURITY_PROFILE="${2:?--pod-security-profile requires a value}"; shift 2 ;;
    --allow-external-ref) ALLOWED_EXTERNAL_REFS+=("${2:?--allow-external-ref requires a value}"); shift 2 ;;
    --build-dependencies) BUILD_DEPENDENCIES=true; shift ;;
    --allow-network) ALLOW_NETWORK=true; shift ;;
    --schema-location) SCHEMA_LOCATIONS+=("${2:?--schema-location requires a value}"); shift 2 ;;
    --server-dry-run) SERVER_DRY_RUN=true; shift ;;
    --allow-cluster) ALLOW_CLUSTER=true; shift ;;
    --context) KUBE_CONTEXT="${2:?--context requires a value}"; shift 2 ;;
    --skip-contract) SKIP_CONTRACT=true; shift ;;
    --skip-schema) SKIP_SCHEMA=true; shift ;;
    --skip-template) SKIP_TEMPLATE=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$CHART" ]]; then
  echo "--chart is required" >&2
  exit 2
fi
case "$POD_SECURITY_PROFILE" in none|baseline|restricted) ;; *) echo "invalid --pod-security-profile" >&2; exit 2 ;; esac
if [[ "$BUILD_DEPENDENCIES" == true && "$ALLOW_NETWORK" != true ]]; then
  echo "--build-dependencies requires --allow-network because Helm may contact repositories" >&2
  exit 2
fi
if [[ "$SERVER_DRY_RUN" == true ]]; then
  if [[ "$ALLOW_CLUSTER" != true || -z "$KUBE_CONTEXT" ]]; then
    echo "--server-dry-run requires --allow-cluster and --context NAME" >&2
    exit 2
  fi
fi
if [[ "$ALLOW_CLUSTER" == true && "$SERVER_DRY_RUN" != true ]]; then
  echo "--allow-cluster is meaningless without --server-dry-run" >&2
  exit 2
fi

for command in python3 helm; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command is unavailable: $command" >&2
    exit 2
  fi
done
if [[ "$SERVER_DRY_RUN" == true ]] && ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl is required for --server-dry-run" >&2
  exit 2
fi

CHART="$(cd "$CHART" && pwd -P)"
if [[ ! -f "$CHART/Chart.yaml" || -L "$CHART/Chart.yaml" ]]; then
  echo "Chart.yaml must be a regular non-symlink file under $CHART" >&2
  exit 2
fi
if find "$CHART" -type l -print -quit | grep -q .; then
  echo "Chart input contains symbolic links; validation copy is refused" >&2
  exit 2
fi

if [[ -n "$OUTPUT_DIR" ]]; then
  if [[ -L "$OUTPUT_DIR" ]]; then
    echo "output directory must not be a symbolic link" >&2
    exit 2
  fi
  mkdir -p "$OUTPUT_DIR"
  OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd -P)"
  if find "$OUTPUT_DIR" -mindepth 1 -print -quit | grep -q .; then
    echo "output directory must be empty: $OUTPUT_DIR" >&2
    exit 2
  fi
  WORK_DIR="$OUTPUT_DIR"
else
  WORK_DIR="$(mktemp -d -t yaml-specialist-evidence.XXXXXXXX)"
fi
chmod 0700 "$WORK_DIR"
mkdir -p "$WORK_DIR/logs" "$WORK_DIR/results" "$WORK_DIR/rendered" "$WORK_DIR/scenarios" "$WORK_DIR/helm-state/config" "$WORK_DIR/helm-state/cache" "$WORK_DIR/helm-state/data"
chmod 0700 "$WORK_DIR"/*

VALIDATION_CHART="$WORK_DIR/chart"
mkdir -p "$VALIDATION_CHART"
cp -a "$CHART/." "$VALIDATION_CHART/"
find "$VALIDATION_CHART" -type f -exec chmod 0600 {} +
find "$VALIDATION_CHART" -type d -exec chmod 0700 {} +

export HELM_CONFIG_HOME="$WORK_DIR/helm-state/config"
export HELM_CACHE_HOME="$WORK_DIR/helm-state/cache"
export HELM_DATA_HOME="$WORK_DIR/helm-state/data"
export HELM_PLUGINS="$WORK_DIR/helm-state/plugins-disabled"
export KUBECONFIG="$WORK_DIR/nonexistent-kubeconfig"

FAILURES=0
INCOMPLETE=0
STEPS_FILE="$WORK_DIR/results/steps.tsv"
printf 'step\texit\tstatus\n' >"$STEPS_FILE"

record_step() {
  local label="$1"
  local rc="$2"
  local status="complete"
  if [[ "$rc" -eq 1 || "$rc" -gt 2 ]]; then
    status="failed"
    FAILURES=$((FAILURES + 1))
  elif [[ "$rc" -eq 2 ]]; then
    status="incomplete"
    INCOMPLETE=$((INCOMPLETE + 1))
  fi
  printf '%s\t%s\t%s\n' "$label" "$rc" "$status" >>"$STEPS_FILE"
}

run_step() {
  local label="$1"
  shift
  local stdout_file="$WORK_DIR/results/${label}.out"
  local stderr_file="$WORK_DIR/logs/${label}.err"
  local rc=0
  printf '==> %s\n' "$label"
  set +e
  "$@" >"$stdout_file" 2>"$stderr_file"
  rc=$?
  set -e
  chmod 0600 "$stdout_file" "$stderr_file"
  record_step "$label" "$rc"
}

mark_incomplete() {
  local label="$1"
  local message="$2"
  printf '%s\n' "$message" >"$WORK_DIR/logs/${label}.err"
  chmod 0600 "$WORK_DIR/logs/${label}.err"
  record_step "$label" 2
}

{
  printf 'python\t'; python3 --version 2>&1
  printf 'helm\t'; helm version --short 2>&1
  if command -v kubeconform >/dev/null 2>&1; then printf 'kubeconform\t'; kubeconform -v 2>&1; fi
  if command -v kubectl >/dev/null 2>&1; then printf 'kubectl\t'; kubectl version --client=true 2>&1 | head -n 1; fi
} >"$WORK_DIR/results/tool-versions.txt"
chmod 0600 "$WORK_DIR/results/tool-versions.txt"

CONTRACT_ARGS=(--chart "$VALIDATION_CHART" --format json)
if [[ "$SKIP_TEMPLATE" == true ]]; then CONTRACT_ARGS+=(--skip-template); fi
if [[ "$SKIP_SCHEMA" == true ]]; then CONTRACT_ARGS+=(--skip-schema); fi
if [[ "$SKIP_CONTRACT" == true ]]; then
  mark_incomplete contract "Contract validation skipped by explicit assessment-only option."
else
  run_step contract python3 "$SCRIPT_DIR/values_contract_lint.py" "${CONTRACT_ARGS[@]}"
fi
run_step template-values python3 "$SCRIPT_DIR/scan_template_values.py" --chart "$VALIDATION_CHART" --format json
run_step dependencies python3 "$SCRIPT_DIR/list_dependency_repositories.py" --chart "$VALIDATION_CHART" --format json

if [[ "$BUILD_DEPENDENCIES" == true ]]; then
  run_step dependency-build helm dependency build "$VALIDATION_CHART"
elif [[ -f "$VALIDATION_CHART/Chart.lock" ]]; then
  if [[ ! -d "$VALIDATION_CHART/charts" ]] || ! find "$VALIDATION_CHART/charts" -maxdepth 1 -type f -print -quit | grep -q .; then
    mark_incomplete dependency-build "Chart.lock exists but packaged dependencies are absent; rerun with --build-dependencies --allow-network after review."
  else
    printf '%s\n' "Using already packaged dependencies from the isolated chart copy." >"$WORK_DIR/results/dependency-build.out"
    record_step dependency-build 0
  fi
else
  printf '%s\n' "No Chart.lock present; Helm lint will determine whether dependency metadata is satisfiable." >"$WORK_DIR/results/dependency-build.out"
  record_step dependency-build 0
fi

HELM_KUBE_ARGS=()
if [[ -n "$KUBE_VERSION" ]]; then HELM_KUBE_ARGS+=(--kube-version "$KUBE_VERSION"); fi
run_step helm-lint-default helm lint "$VALIDATION_CHART" --strict "${HELM_KUBE_ARGS[@]}"

CHART_TYPE="application"
set +e
CHART_TYPE="$(python3 "$SCRIPT_DIR/chart_metadata.py" --chart "$VALIDATION_CHART" --field type 2>"$WORK_DIR/logs/chart-type.err")"
CHART_TYPE_RC=$?
set -e
record_step chart-type "$CHART_TYPE_RC"

SCENARIO_LABELS=(default)
SCENARIO_PATHS=("")
if [[ "$SKIP_TEMPLATE" != true && -f "$VALIDATION_CHART/values-template.yaml" ]]; then
  SCENARIO_LABELS+=(values-template)
  SCENARIO_PATHS+=("$VALIDATION_CHART/values-template.yaml")
elif [[ "$SKIP_TEMPLATE" == true ]]; then
  mark_incomplete template-scenario "values-template scenario skipped by explicit assessment-only option."
fi

for entry in "${VALUES_FILES[@]}"; do
  if [[ "$entry" != *=* ]]; then
    echo "invalid --values $entry; use LABEL=PATH" >&2
    exit 2
  fi
  label="${entry%%=*}"
  source_file="${entry#*=}"
  if [[ ! "$label" =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$ ]]; then
    echo "invalid scenario label: $label" >&2
    exit 2
  fi
  if [[ ! -f "$source_file" || -L "$source_file" ]]; then
    echo "scenario values must be a regular non-symlink file: $source_file" >&2
    exit 2
  fi
  target_file="$WORK_DIR/scenarios/$label.yaml"
  cp "$source_file" "$target_file"
  chmod 0600 "$target_file"
  SCENARIO_LABELS+=("$label")
  SCENARIO_PATHS+=("$target_file")
done

if [[ "$CHART_TYPE" == "library" ]]; then
  mark_incomplete render-library "Library charts are not installable; validate exported helpers through reviewed consumer charts."
else
  index=0
  while [[ "$index" -lt "${#SCENARIO_LABELS[@]}" ]]; do
    label="${SCENARIO_LABELS[$index]}"
    values_path="${SCENARIO_PATHS[$index]}"
    manifest="$WORK_DIR/rendered/$label.yaml"
    helm_args=(template "$RELEASE" "$VALIDATION_CHART" --namespace "$NAMESPACE" --include-crds "${HELM_KUBE_ARGS[@]}")
    if [[ -n "$values_path" ]]; then helm_args+=(-f "$values_path"); fi
    run_step "helm-lint-$label" helm lint "$VALIDATION_CHART" --strict "${HELM_KUBE_ARGS[@]}" ${values_path:+-f "$values_path"}

    printf '==> render-%s\n' "$label"
    set +e
    helm "${helm_args[@]}" >"$manifest" 2>"$WORK_DIR/logs/render-$label.err"
    render_rc=$?
    set -e
    chmod 0600 "$manifest" "$WORK_DIR/logs/render-$label.err"
    record_step "render-$label" "$render_rc"

    if [[ "$render_rc" -eq 0 ]]; then
      manifest_args=(--input "$manifest" --default-namespace "$NAMESPACE" --pod-security-profile "$POD_SECURITY_PROFILE" --format json)
      for allowed_ref in "${ALLOWED_EXTERNAL_REFS[@]}"; do manifest_args+=(--allow-external-ref "$allowed_ref"); done
      run_step "manifest-$label" python3 "$SCRIPT_DIR/rendered_manifest_lint.py" "${manifest_args[@]}"

      if command -v kubeconform >/dev/null 2>&1 && [[ -n "$KUBE_VERSION" && "${#SCHEMA_LOCATIONS[@]}" -gt 0 ]]; then
        kube_args=(-strict -summary -output json -kubernetes-version "$KUBE_VERSION")
        for location in "${SCHEMA_LOCATIONS[@]}"; do
          if [[ "$location" == http://* ]]; then
            echo "plaintext kubeconform schema locations are forbidden: $location" >&2
            exit 2
          fi
          if [[ "$location" == https://* || "$location" == default ]] && [[ "$ALLOW_NETWORK" != true ]]; then
            echo "network schema location requires --allow-network: $location" >&2
            exit 2
          fi
          kube_args+=(-schema-location "$location")
        done
        run_step "kubeconform-$label" kubeconform "${kube_args[@]}" "$manifest"
      else
        mark_incomplete "kubeconform-$label" "kubeconform requires the binary, --kube-version, and at least one explicit --schema-location; missing schemas are never ignored."
      fi

      if [[ "$SERVER_DRY_RUN" == true ]]; then
        run_step "server-dry-run-$label" kubectl --context "$KUBE_CONTEXT" apply --dry-run=server -f "$manifest"
      fi
    else
      mark_incomplete "post-render-$label" "Post-render checks could not run because Helm rendering failed."
    fi
    index=$((index + 1))
  done
fi

FINAL_STATUS="complete"
FINAL_EXIT=0
if [[ "$FAILURES" -gt 0 ]]; then
  FINAL_STATUS="failed"
  FINAL_EXIT=1
elif [[ "$INCOMPLETE" -gt 0 ]]; then
  FINAL_STATUS="incomplete"
  FINAL_EXIT=2
fi

cat >"$WORK_DIR/REPORT.md" <<EOF
# yaml-specialist validation evidence

**Status:** $FINAL_STATUS
**Chart copy:** $VALIDATION_CHART
**Kubernetes target:** ${KUBE_VERSION:-not declared}
**Network allowed:** $ALLOW_NETWORK
**Cluster contacted:** $SERVER_DRY_RUN
**Failures:** $FAILURES
**Incomplete stages:** $INCOMPLETE

Rendered manifests may contain sensitive configuration and remain owner-readable only.
Review results/steps.tsv, per-stage outputs, and stderr logs before making any claim.
This local workflow does not equal admission success unless an explicitly authorized
server dry-run stage completed for every scenario.
EOF
chmod 0600 "$WORK_DIR/REPORT.md" "$STEPS_FILE"
printf 'Validation status: %s\nEvidence directory: %s\n' "$FINAL_STATUS" "$WORK_DIR"
exit "$FINAL_EXIT"
