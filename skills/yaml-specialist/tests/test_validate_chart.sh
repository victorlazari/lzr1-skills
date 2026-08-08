#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="$PACKAGE_DIR/scripts/validate_chart.sh"
APP_CHART="$PACKAGE_DIR/tests/fixtures/application-chart"
LIB_CHART="$PACKAGE_DIR/tests/fixtures/library-chart"
RENDERED="$PACKAGE_DIR/tests/fixtures/rendered-valid.yaml"
TMP_ROOT="$(mktemp -d -t yaml-specialist-wrapper-tests.XXXXXXXX)"
trap 'rm -rf "$TMP_ROOT"' EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_rc() {
  local expected="$1"
  local actual="$2"
  local label="$3"
  [[ "$actual" -eq "$expected" ]] || fail "$label: expected exit $expected, got $actual"
}

run_capture() {
  local output="$1"
  shift
  set +e
  "$@" >"$output.stdout" 2>"$output.stderr"
  RUN_RC=$?
  set -e
}

make_fake_tools() {
  local directory="$1"
  local include_kubeconform="$2"
  local include_kubectl="$3"
  mkdir -p "$directory"

  cat >"$directory/helm" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
printf 'helm\t' >>"$FAKE_TOOL_LOG"
printf '%q ' "$@" >>"$FAKE_TOOL_LOG"
printf '\n' >>"$FAKE_TOOL_LOG"
case "${1:-}" in
  version)
    printf 'v4.2.3+fixture\n'
    ;;
  lint)
    exit "${FAKE_HELM_LINT_RC:-0}"
    ;;
  template)
    if [[ "${FAKE_HELM_TEMPLATE_RC:-0}" -ne 0 ]]; then
      printf 'fixture render failure\n' >&2
      exit "$FAKE_HELM_TEMPLATE_RC"
    fi
    cat "$FAKE_RENDER_FILE"
    ;;
  dependency)
    [[ "${2:-}" == "build" ]] || exit 9
    exit "${FAKE_HELM_DEPENDENCY_RC:-0}"
    ;;
  *)
    printf 'unexpected fake helm invocation: %s\n' "$*" >&2
    exit 9
    ;;
esac
EOF
  chmod 0755 "$directory/helm"

  if [[ "$include_kubeconform" == true ]]; then
    cat >"$directory/kubeconform" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
printf 'kubeconform\t' >>"$FAKE_TOOL_LOG"
printf '%q ' "$@" >>"$FAKE_TOOL_LOG"
printf '\n' >>"$FAKE_TOOL_LOG"
if [[ "${1:-}" == "-v" ]]; then
  printf 'v0.8.0-fixture\n'
  exit 0
fi
joined=" $* "
[[ "$joined" == *" -strict "* ]] || exit 8
[[ "$joined" != *" -ignore-missing-schemas "* ]] || exit 8
exit "${FAKE_KUBECONFORM_RC:-0}"
EOF
    chmod 0755 "$directory/kubeconform"
  fi

  if [[ "$include_kubectl" == true ]]; then
    cat >"$directory/kubectl" <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
printf 'kubectl\t' >>"$FAKE_TOOL_LOG"
printf '%q ' "$@" >>"$FAKE_TOOL_LOG"
printf '\n' >>"$FAKE_TOOL_LOG"
if [[ "${1:-}" == "version" ]]; then
  printf 'Client Version: v1.36.0-fixture\n'
  exit 0
fi
joined=" $* "
[[ "$joined" == *" --context fixture-context "* ]] || exit 8
[[ "$joined" == *" apply "* && "$joined" == *" --dry-run=server "* ]] || exit 8
exit "${FAKE_KUBECTL_RC:-0}"
EOF
    chmod 0755 "$directory/kubectl"
  fi
}

SYSTEM_PATH="$(dirname "$(command -v python3)"):/usr/local/bin:/usr/bin:/bin"
FAKE_BIN="$TMP_ROOT/fake-complete"
make_fake_tools "$FAKE_BIN" true true
export FAKE_TOOL_LOG="$TMP_ROOT/tools.log"
export FAKE_RENDER_FILE="$RENDERED"
: >"$FAKE_TOOL_LOG"
SCHEMAS="$TMP_ROOT/schemas"
mkdir -p "$SCHEMAS"

# Consent gates fail before any network or cluster-capable action.
run_capture "$TMP_ROOT/dependency-gate" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" --chart "$APP_CHART" --build-dependencies
assert_rc 2 "$RUN_RC" "dependency network gate"
grep -q -- '--build-dependencies requires --allow-network' "$TMP_ROOT/dependency-gate.stderr" || fail "dependency gate message missing"

run_capture "$TMP_ROOT/cluster-gate" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" --chart "$APP_CHART" --server-dry-run
assert_rc 2 "$RUN_RC" "cluster consent gate"
grep -q -- '--server-dry-run requires --allow-cluster and --context NAME' "$TMP_ROOT/cluster-gate.stderr" || fail "cluster gate message missing"

# A complete local run uses only fake executables and explicit local schema input.
COMPLETE_OUT="$TMP_ROOT/complete-evidence"
run_capture "$TMP_ROOT/complete" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" \
  --chart "$APP_CHART" \
  --namespace tests \
  --kube-version 1.36.0 \
  --schema-location "$SCHEMAS" \
  --pod-security-profile restricted \
  --output-dir "$COMPLETE_OUT"
assert_rc 0 "$RUN_RC" "complete isolated run"
grep -q '^\*\*Status:\*\* complete' "$COMPLETE_OUT/REPORT.md" || fail "complete report status missing"
grep -q $'^kubeconform-default\t0\tcomplete$' "$COMPLETE_OUT/results/steps.tsv" || fail "default kubeconform stage missing"
grep -q $'^kubeconform-values-template\t0\tcomplete$' "$COMPLETE_OUT/results/steps.tsv" || fail "overlay kubeconform stage missing"
if grep -q '^kubectl.* apply .*--dry-run=server' "$FAKE_TOOL_LOG"; then fail "default local run attempted server dry-run"; fi
if grep -q $'^helm\tdependency build' "$FAKE_TOOL_LOG"; then fail "default local run built dependencies"; fi
[[ "$(stat -c '%a' "$COMPLETE_OUT")" == "700" ]] || fail "evidence directory is not mode 0700"
[[ "$(stat -c '%a' "$COMPLETE_OUT/REPORT.md")" == "600" ]] || fail "report is not mode 0600"
[[ "$(stat -c '%a' "$COMPLETE_OUT/rendered/default.yaml")" == "600" ]] || fail "rendered evidence is not mode 0600"

# Explicitly authorized server dry-run reaches only the fake kubectl with the exact context.
: >"$FAKE_TOOL_LOG"
CLUSTER_OUT="$TMP_ROOT/cluster-evidence"
run_capture "$TMP_ROOT/cluster" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" \
  --chart "$APP_CHART" \
  --namespace tests \
  --kube-version 1.36.0 \
  --schema-location "$SCHEMAS" \
  --server-dry-run \
  --allow-cluster \
  --context fixture-context \
  --output-dir "$CLUSTER_OUT"
assert_rc 0 "$RUN_RC" "authorized fake server dry-run"
grep -q '^kubectl' "$FAKE_TOOL_LOG" || fail "authorized fake kubectl was not invoked"
grep -q -- '--context fixture-context apply --dry-run=server' "$FAKE_TOOL_LOG" || fail "kubectl context or server-dry-run argument missing"

# Absence of kubeconform is incomplete rather than clean.
HELM_ONLY="$TMP_ROOT/fake-helm-only"
make_fake_tools "$HELM_ONLY" false false
INCOMPLETE_OUT="$TMP_ROOT/incomplete-evidence"
run_capture "$TMP_ROOT/incomplete" env PATH="$HELM_ONLY:$SYSTEM_PATH" "$VALIDATOR" \
  --chart "$APP_CHART" --namespace tests --output-dir "$INCOMPLETE_OUT"
assert_rc 2 "$RUN_RC" "missing schema validator"
grep -q '^\*\*Status:\*\* incomplete' "$INCOMPLETE_OUT/REPORT.md" || fail "incomplete report status missing"

# A Helm render error remains failed even though downstream checks become incomplete.
FAIL_OUT="$TMP_ROOT/failure-evidence"
run_capture "$TMP_ROOT/failure" env PATH="$FAKE_BIN:$SYSTEM_PATH" FAKE_HELM_TEMPLATE_RC=7 "$VALIDATOR" \
  --chart "$APP_CHART" \
  --namespace tests \
  --kube-version 1.36.0 \
  --schema-location "$SCHEMAS" \
  --output-dir "$FAIL_OUT"
assert_rc 1 "$RUN_RC" "render failure propagation"
grep -q '^\*\*Status:\*\* failed' "$FAIL_OUT/REPORT.md" || fail "failed report status missing"
grep -q $'^render-default\t7\tfailed$' "$FAIL_OUT/results/steps.tsv" || fail "render failure was not recorded"

# Library charts are explicitly incomplete without a reviewed consumer chart.
LIB_OUT="$TMP_ROOT/library-evidence"
run_capture "$TMP_ROOT/library" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" \
  --chart "$LIB_CHART" \
  --kube-version 1.36.0 \
  --schema-location "$SCHEMAS" \
  --output-dir "$LIB_OUT"
assert_rc 2 "$RUN_RC" "library consumer coverage"
grep -q $'^render-library\t2\tincomplete$' "$LIB_OUT/results/steps.tsv" || fail "library coverage gap was not recorded"

# Existing evidence and symlink-bearing inputs are refused.
NONEMPTY="$TMP_ROOT/nonempty"
mkdir -p "$NONEMPTY"
printf 'owned\n' >"$NONEMPTY/existing.txt"
run_capture "$TMP_ROOT/nonempty-run" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" --chart "$APP_CHART" --output-dir "$NONEMPTY"
assert_rc 2 "$RUN_RC" "nonempty evidence refusal"

SYMLINK_CHART="$TMP_ROOT/symlink-chart"
cp -a "$APP_CHART" "$SYMLINK_CHART"
ln -s /etc/passwd "$SYMLINK_CHART/templates/escape"
run_capture "$TMP_ROOT/symlink-run" env PATH="$FAKE_BIN:$SYSTEM_PATH" "$VALIDATOR" --chart "$SYMLINK_CHART"
assert_rc 2 "$RUN_RC" "chart symlink refusal"
grep -q 'contains symbolic links' "$TMP_ROOT/symlink-run.stderr" || fail "symlink refusal message missing"

printf 'yaml-specialist wrapper tests: PASS\n'
