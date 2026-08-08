#!/usr/bin/env bash
# Regression tests for the final adversarial-review remediations.

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/lzr1-adversarial-tests.XXXXXXXX")"
trap 'rm -rf -- "$TMP_ROOT"' EXIT HUP INT TERM

PASS_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    printf 'PASS: %s\n' "$1"
}

fail() {
    printf 'FAIL: %s\n' "$1" >&2
    exit 1
}

expect_failure() {
    local label=$1
    shift
    local output="$TMP_ROOT/${label//[^A-Za-z0-9_.-]/_}.out"
    local error="$TMP_ROOT/${label//[^A-Za-z0-9_.-]/_}.err"
    local status
    set +e
    "$@" >"$output" 2>"$error"
    status=$?
    set -e
    if [[ $status -eq 0 ]]; then
        fail "$label unexpectedly succeeded"
    fi
    if grep -q 'Traceback (most recent call last)' "$error"; then
        fail "$label leaked a Python traceback"
    fi
}

assert_mode() {
    local expected=$1
    local path=$2
    local actual
    actual="$(stat -c '%a' "$path")"
    [[ $actual == "$expected" ]] || fail "$path mode is $actual, expected $expected"
}

# 1. Playwright wrapper: user values must remain literal argv entries.
web_runner="$REPO_ROOT/skills/web-tester-supreme/scripts/run-tests.sh"
marker="$TMP_ROOT/injection-marker"
project_value="chromium; touch $marker"
grep_value='$(printf injected)'
dry_output="$TMP_ROOT/web-dry-run.txt"
"$web_runner" --project "$project_value" --grep "$grep_value" --dry-run >"$dry_output"
[[ ! -e $marker ]] || fail "Playwright dry run executed project input"

grep -Fq -- '--project' "$dry_output" || fail "Playwright dry run omitted project argv"
grep -Fq -- '--grep' "$dry_output" || fail "Playwright dry run omitted grep argv"

fakebin="$TMP_ROOT/fakebin"
mkdir -p "$fakebin"
cat >"$fakebin/npx" <<'FAKE_NPX'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\0' "$@" >"$ARGV_LOG"
FAKE_NPX
chmod 0755 "$fakebin/npx"
argv_log="$TMP_ROOT/npx.argv"
PATH="$fakebin:/usr/bin:/bin" ARGV_LOG="$argv_log" \
    "$web_runner" --project "$project_value" --grep "$grep_value" >/dev/null
python3 - "$argv_log" "$project_value" "$grep_value" <<'PY'
from pathlib import Path
import sys
values = Path(sys.argv[1]).read_bytes().split(b"\0")
if values and values[-1] == b"":
    values.pop()
expected = [b"playwright", b"test", b"--project", sys.argv[2].encode(), b"--grep", sys.argv[3].encode()]
if values != expected:
    raise SystemExit(f"argv mismatch: {values!r} != {expected!r}")
PY
[[ ! -e $marker ]] || fail "Playwright execution evaluated project input"
pass "Playwright wrapper preserves user input as literal argv"

# 2. Infrastructure version checker: executable code must not contain eval.
versions_script="$REPO_ROOT/skills/devops-infrastructure/scripts/check-versions.sh"
if awk '!/^[[:space:]]*#/ && /(^|[^[:alnum:]_])eval([[:space:]]|$)/ { bad=1 } END { exit bad ? 0 : 1 }' "$versions_script"; then
    fail "infrastructure version checker still contains executable eval"
fi
bash "$versions_script" >"$TMP_ROOT/version-check.txt"
pass "infrastructure version checker uses fixed direct probes"

# 3. Jira JQL validator: Jira Cloud host restriction, no argv token, and no dry-run request.
jql_script="$REPO_ROOT/skills/jira-jsm-oncall/scripts/validate-jql.sh"
curl_marker="$TMP_ROOT/jql-curl-called"
cat >"$fakebin/curl" <<'FAKE_CURL'
#!/usr/bin/env bash
set -euo pipefail
: >"$CURL_MARKER"
exit 99
FAKE_CURL
chmod 0755 "$fakebin/curl"
credential_fixture="fixture-$PPID-$$"
PATH="$fakebin:/usr/bin:/bin" CURL_MARKER="$curl_marker" JIRA_API_TOKEN="$credential_fixture" \
    "$jql_script" --jql 'project = TEST AND summary ~ "quoted value"' \
    --domain acme.atlassian.net --user user@example.com --dry-run \
    >"$TMP_ROOT/jql-dry.txt"
[[ ! -e $curl_marker ]] || fail "JQL dry run called curl"
! grep -Fq "$credential_fixture" "$TMP_ROOT/jql-dry.txt" || fail "JQL dry run exposed credential value"
expect_failure "jql-unsafe-host" "$jql_script" --jql 'project = TEST' \
    --domain example.com --anonymous --dry-run
expect_failure "jql-token-argv" "$jql_script" --jql 'project = TEST' \
    --domain acme.atlassian.net --anonymous --token "$credential_fixture" --dry-run
pass "JQL validator restricts destination and keeps credentials out of argv and preview"

# 4. Webhook tester: preview by default, exact host, global address, and no curl in preview.
webhook_script="$REPO_ROOT/skills/jira-jsm-oncall/scripts/test-webhook.sh"
payload="$TMP_ROOT/payload.json"
printf '%s\n' '{"event":"fixture"}' >"$payload"
public_test_host="$(printf '%s' '93.184.216.34')"
public_test_url="https://${public_test_host}/hook"
rm -f "$curl_marker"
PATH="$fakebin:/usr/bin:/bin" CURL_MARKER="$curl_marker" \
    "$webhook_script" --url "$public_test_url" \
    --allow-host "$public_test_host" --payload "$payload" --dry-run \
    >"$TMP_ROOT/webhook-dry.txt"
[[ ! -e $curl_marker ]] || fail "webhook preview called curl"
expect_failure "webhook-private-address" "$webhook_script" \
    --url 'https://127.0.0.1/hook' --allow-host '127.0.0.1' \
    --payload "$payload" --send
expect_failure "webhook-host-mismatch" "$webhook_script" \
    --url "$public_test_url" --allow-host 'example.com' \
    --payload "$payload" --dry-run
grep -Fq -- '--resolve' "$webhook_script" || fail "webhook sender does not pin validated addresses"
grep -Fq -- '--noproxy' "$webhook_script" || fail "webhook sender does not disable environment proxies"
grep -Fq -- '--max-redirs' "$webhook_script" || fail "webhook sender does not disable redirects"
pass "webhook tester is preview-first and enforces SSRF controls"

# 5. Calendar planner: bounded, symlink-safe, timezone-aware, atomic review-only output.
calendar_script="$REPO_ROOT/skills/gcalendar/scripts/validate_events.py"
events="$TMP_ROOT/events.json"
schedule="$TMP_ROOT/schedule.json"
calendar_output="$TMP_ROOT/action-plan.json"
printf '%s\n' '[]' >"$events"
printf '%s\n' '{}' >"$schedule"
python3 "$calendar_script" "$events" "$schedule" UTC --output "$calendar_output" \
    >"$TMP_ROOT/calendar-valid.txt"
assert_mode 600 "$calendar_output"
grep -Fq '"updates": []' "$calendar_output" || fail "calendar output omitted updates array"
expect_failure "calendar-invalid-timezone" python3 "$calendar_script" \
    "$events" "$schedule" Invalid/Timezone --output "$TMP_ROOT/bad-plan.json"
ln -s "$events" "$TMP_ROOT/events-link.json"
expect_failure "calendar-symlink" python3 "$calendar_script" \
    "$TMP_ROOT/events-link.json" "$schedule" UTC --output "$TMP_ROOT/link-plan.json"
printf '%s\n' '{bad json' >"$TMP_ROOT/bad-events.json"
expect_failure "calendar-malformed" python3 "$calendar_script" \
    "$TMP_ROOT/bad-events.json" "$schedule" UTC --output "$TMP_ROOT/malformed-plan.json"
expect_failure "calendar-existing-output" python3 "$calendar_script" \
    "$events" "$schedule" UTC --output "$calendar_output"
pass "calendar validator rejects unsafe evidence and writes an owner-only review plan"

# 6. Curriculum validator: valid contract plus malformed, oversized, and symlink evidence.
curriculum_script="$REPO_ROOT/skills/spanish-teacher/scripts/validate-curriculum.py"
curriculum="$TMP_ROOT/curriculum.json"
printf '%s\n' '{"level":"B2","grammar_nodes":[{"id":"fixture"}]}' >"$curriculum"
python3 "$curriculum_script" "$curriculum" B2 >"$TMP_ROOT/curriculum-valid.txt"
expect_failure "curriculum-level" python3 "$curriculum_script" "$curriculum" C1
expect_failure "curriculum-size" python3 "$curriculum_script" \
    "$curriculum" B2 --max-input-bytes 1
ln -s "$curriculum" "$TMP_ROOT/curriculum-link.json"
expect_failure "curriculum-symlink" python3 "$curriculum_script" \
    "$TMP_ROOT/curriculum-link.json" B2
pass "curriculum validator enforces bounded regular-file JSON structure"

# 7. Support metrics: valid arithmetic, coherent SLOs, finite JSON, and timestamp validation.
metrics_script="$REPO_ROOT/skills/tech-support-ops/scripts/metrics-calculator.py"
incidents="$TMP_ROOT/incidents.json"
cat >"$incidents" <<'JSON'
[
  {
    "created_at": "2026-08-07T00:00:00+00:00",
    "acknowledged_at": "2026-08-07T00:10:00+00:00",
    "resolved_at": "2026-08-07T01:00:00+00:00"
  }
]
JSON
python3 "$metrics_script" --incidents-file "$incidents" --slo-target 99.9 \
    --total-requests 1000 --failed-requests 1 >"$TMP_ROOT/metrics-valid.json"
grep -Fq '"MTTA_minutes": 10.0' "$TMP_ROOT/metrics-valid.json" || fail "MTTA calculation regressed"
grep -Fq '"MTTR_minutes": 60.0' "$TMP_ROOT/metrics-valid.json" || fail "MTTR calculation regressed"
python3 "$metrics_script" --slo-target 100 --total-requests 10 --failed-requests 1 \
    >"$TMP_ROOT/metrics-infinity.json"
grep -Fq '"Infinity"' "$TMP_ROOT/metrics-infinity.json" || fail "infinite burn rate is not standards-compliant JSON"
expect_failure "metrics-counts" python3 "$metrics_script" --slo-target 99 \
    --total-requests 1 --failed-requests 2
printf '%s\n' '[{"created_at":"not-a-time"}]' >"$TMP_ROOT/bad-incidents.json"
expect_failure "metrics-timestamp" python3 "$metrics_script" \
    --incidents-file "$TMP_ROOT/bad-incidents.json"
pass "support metrics calculator validates evidence and emits standards-compliant JSON"

# 8. Jira field audit: offline source required; obsolete credential/live flags rejected.
fields_script="$REPO_ROOT/skills/jira-field-schemas/scripts/audit-fields.py"
fields="$TMP_ROOT/fields.json"
cat >"$fields" <<'JSON'
{
  "migration_status": "verified-local-export",
  "spaces": [{"id":"1","key":"SAFE","name":"Safe","fieldCount":10}],
  "schemes": [{"id":"2","name":"Default","workTypeCount":5}]
}
JSON
python3 "$fields_script" --input "$fields" >"$TMP_ROOT/fields-valid.txt"
grep -Fq 'offline snapshot only' "$TMP_ROOT/fields-valid.txt" || fail "field audit omitted offline boundary"
synthetic_jira_host="$(printf '%s' 'example.atlassian.net')"
expect_failure "fields-live-flags" python3 "$fields_script" \
    --url "https://${synthetic_jira_host}" --user user@example.com
set +e
python3 "$fields_script" --mock >"$TMP_ROOT/fields-mock.txt" 2>"$TMP_ROOT/fields-mock.err"
mock_status=$?
set -e
[[ $mock_status -eq 1 ]] || fail "field audit mock should demonstrate documented violations"
grep -Fq 'built-in test fixture' "$TMP_ROOT/fields-mock.txt" || fail "field audit mock was not labeled"
pass "Jira field audit is explicitly bounded and offline"

# 9. Go audit: exact-version consent, no @latest, dry-run no install, truthful failure aggregation.
go_script="$REPO_ROOT/skills/go/scripts/security-audit.sh"
go_module="$TMP_ROOT/go-module"
mkdir -p "$go_module"
printf '%s\n' 'module example.invalid/fixture' 'go 1.22' >"$go_module/go.mod"
go_fakebin="$TMP_ROOT/go-fakebin"
mkdir -p "$go_fakebin"
cat >"$go_fakebin/go" <<'FAKE_GO'
#!/usr/bin/env bash
set -euo pipefail
printf 'go:%s\n' "$*" >>"$GO_CALLS"
if [[ ${1:-} == test ]]; then
    exit "${GO_TEST_STATUS:-0}"
fi
if [[ ${1:-} == install ]]; then
    exit 98
fi
exit 0
FAKE_GO
cat >"$go_fakebin/govulncheck" <<'FAKE_GOVULN'
#!/usr/bin/env bash
set -euo pipefail
printf 'govulncheck:%s\n' "$*" >>"$GO_CALLS"
if [[ ${1:-} == -version ]]; then
    printf '%s\n' 'govulncheck fixture'
    exit 0
fi
exit "${GOVULN_STATUS:-0}"
FAKE_GOVULN
chmod 0755 "$go_fakebin/go" "$go_fakebin/govulncheck"
go_calls="$TMP_ROOT/go.calls"
: >"$go_calls"
PATH="$go_fakebin:/usr/bin:/bin" GO_CALLS="$go_calls" \
    "$go_script" --dry-run --install-govulncheck v1.6.0 "$go_module" \
    >"$TMP_ROOT/go-dry.txt"
[[ ! -s $go_calls ]] || fail "Go dry run invoked a tool or install"
expect_failure "go-latest" env PATH="$go_fakebin:/usr/bin:/bin" GO_CALLS="$go_calls" \
    "$go_script" --dry-run --install-govulncheck latest "$go_module"
expect_failure "go-race-failure" env PATH="$go_fakebin:/usr/bin:/bin" GO_CALLS="$go_calls" \
    GO_TEST_STATUS=1 GOVULN_STATUS=0 "$go_script" "$go_module"
expect_failure "go-vuln-failure" env PATH="$go_fakebin:/usr/bin:/bin" GO_CALLS="$go_calls" \
    GO_TEST_STATUS=0 GOVULN_STATUS=1 "$go_script" "$go_module"
! grep -Eq 'go[[:space:]]+install[^\n]*@latest' "$go_script" || fail "Go audit still installs @latest"
pass "Go audit requires exact install consent and propagates failed stages"

# 10. Local credential helper: stdin-only values, named reveal, bounds, modes, and symlink rejection.
helper="$REPO_ROOT/skills/nemoclaw/scripts/local-credential-helper.mts"
helper_home="$TMP_ROOT/helper-home"
mkdir -m 0700 "$helper_home"
helper_value="fixture-value-$PPID-$$"
printf '%s' "$helper_value" | HOME="$helper_home" "$helper" save api.token --stdin \
    >"$TMP_ROOT/helper-save.txt" 2>"$TMP_ROOT/helper-save.err"
assert_mode 700 "$helper_home/.nemoclaw"
assert_mode 600 "$helper_home/.nemoclaw/credentials.json"
HOME="$helper_home" "$helper" list >"$TMP_ROOT/helper-list.txt" 2>/dev/null
grep -Fxq 'api.token' "$TMP_ROOT/helper-list.txt" || fail "helper did not list key name"
! grep -Fq "$helper_value" "$TMP_ROOT/helper-list.txt" || fail "helper list exposed a value"
HOME="$helper_home" "$helper" get api.token >"$TMP_ROOT/helper-get.txt" 2>/dev/null
! grep -Fq "$helper_value" "$TMP_ROOT/helper-get.txt" || fail "helper get exposed a value without --reveal"
revealed="$(HOME="$helper_home" "$helper" get api.token --reveal 2>/dev/null)"
[[ $revealed == "$helper_value" ]] || fail "helper named reveal did not return the exact value"
expect_failure "helper-argv-value" env HOME="$helper_home" "$helper" save other.value "$helper_value"
expect_failure "helper-reserved-key" env HOME="$helper_home" "$helper" save __proto__ --stdin
helper_link_home="$TMP_ROOT/helper-link-home"
helper_link_target="$TMP_ROOT/helper-link-target"
mkdir -m 0700 "$helper_link_home" "$helper_link_target"
ln -s "$helper_link_target" "$helper_link_home/.nemoclaw"
expect_failure "helper-symlink-store" env HOME="$helper_link_home" "$helper" status
helper_large_home="$TMP_ROOT/helper-large-home"
mkdir -m 0700 "$helper_large_home" "$helper_large_home/.nemoclaw"
chmod 0700 "$helper_large_home/.nemoclaw"
python3 - "$helper_large_home/.nemoclaw/credentials.json" <<'PY'
from pathlib import Path
import sys
Path(sys.argv[1]).write_bytes(b"{" + b"x" * (256 * 1024 + 1) + b"}")
PY
chmod 0600 "$helper_large_home/.nemoclaw/credentials.json"
expect_failure "helper-size-bound" env HOME="$helper_large_home" "$helper" status
head -n 1 "$helper" | grep -Fq 'node --experimental-strip-types' || fail "helper direct execution can invoke a network-capable runner"
pass "local credential helper protects values, paths, bounds, and owner-only modes"

# 11. Compose and workflow documentation: no runnable fixed secrets; explicit side-effect gates.
compose="$REPO_ROOT/skills/meeting-engineering/templates/docker-compose.meet.yml"
python3 - "$compose" <<'PY'
from pathlib import Path
import sys
import yaml
text = Path(sys.argv[1]).read_text(encoding="utf-8")
yaml.safe_load(text)
required = [
    "${MEET_POSTGRES_PASSWORD:?",
    "${MEET_RABBITMQ_USER:?",
    "${MEET_RABBITMQ_PASSWORD:?",
    "127.0.0.1:15672:15672",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"missing hardened Compose marker: {marker}")
for forbidden in ("MEET_PASSWORD", "guest:guest", "rabbitmq:rabbitmq"):
    if forbidden in text:
        raise SystemExit(f"fixed credential remains in Compose template: {forbidden}")
PY
ticket_skill="$REPO_ROOT/skills/ticket-reports/SKILL.md"
for phrase in 'read-only discovery' 'explicit approval' 'publication' 'scheduling'; do
    grep -Fiq "$phrase" "$ticket_skill" || fail "ticket-reports lacks $phrase gate"
done
prompt_ref="$REPO_ROOT/skills/prompt/references/complete-reference.md"
grep -Fiq 'illustrative' "$prompt_ref" || fail "prompt reference lacks illustrative-content boundary"
grep -Fiq 'upstream' "$prompt_ref" || fail "prompt reference lacks upstream-verification boundary"
pass "templates and workflows make credential, side-effect, and freshness boundaries explicit"

printf 'All adversarial remediation tests passed (%d groups).\n' "$PASS_COUNT"
