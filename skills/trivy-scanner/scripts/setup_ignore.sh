#!/usr/bin/env bash
# Generate one review-only .trivyignore.yaml proposal plus a separate governance ledger.
# The script never edits or merges an existing ignore file.

set -Eeuo pipefail
umask 077

TYPE=""
FINDING_ID=""
STATEMENT=""
OWNER=""
EVIDENCE=""
EXPIRES=""
APPROVER=""
OUTPUT_DIR=""
DRY_RUN=0
PATHS=()
PURLS=()

usage() {
  cat <<'EOF'
Usage:
  setup_ignore.sh --type TYPE --id ID --statement TEXT --owner OWNER \
    --evidence REF --expires YYYY-MM-DD --output-dir DIR [options]

Required:
  --type TYPE           vulnerabilities|misconfigurations|secrets|licenses
  --id ID               Exact Trivy finding identifier
  --statement TEXT      Bounded technical rationale placed in Trivy's supported field
  --owner NAME          Responsible team/role; stored only in governance JSON
  --evidence REF        Ticket or evidence reference; stored only in governance JSON
  --expires DATE        Future review/expiry date in YYYY-MM-DD
  --output-dir DIR      New directory for the two proposal files

Optional:
  --path PATH           Add a path scope; repeatable
  --purl PURL           Add a PURL scope; repeatable and vulnerabilities-only
  --approver NAME       Requested reviewer/approver; proposal remains unapproved
  --dry-run             Print both proposed files; write nothing
  --help                Show this help

Outputs:
  .trivyignore.yaml             Schema-limited Trivy input
  .trivyignore.governance.json  Owner, evidence, approval state, scope, and hashes

This generator deliberately does not merge, approve, or test the exception. The YAML
ignore feature was documented as experimental on 2026-08-07. Review both files, test
the YAML with the installed Trivy release and a representative target, then merge it
through the repository's normal review process.
EOF
}

die() { printf 'ERROR: %s\n' "$1" >&2; exit 2; }
require_value() { [[ $# -ge 2 && -n ${2:-} ]] || die "Option $1 requires a value"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) require_value "$@"; TYPE=$2; shift 2 ;;
    --id) require_value "$@"; FINDING_ID=$2; shift 2 ;;
    --statement) require_value "$@"; STATEMENT=$2; shift 2 ;;
    --owner) require_value "$@"; OWNER=$2; shift 2 ;;
    --evidence) require_value "$@"; EVIDENCE=$2; shift 2 ;;
    --expires) require_value "$@"; EXPIRES=$2; shift 2 ;;
    --output-dir) require_value "$@"; OUTPUT_DIR=$2; shift 2 ;;
    --path) require_value "$@"; PATHS+=("$2"); shift 2 ;;
    --purl) require_value "$@"; PURLS+=("$2"); shift 2 ;;
    --approver) require_value "$@"; APPROVER=$2; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) die "Unknown option: $1" ;;
  esac
done

for required in TYPE FINDING_ID STATEMENT OWNER EVIDENCE EXPIRES OUTPUT_DIR; do
  [[ -n ${!required} ]] || die "--${required,,} is required"
done
case "$TYPE" in
  vulnerabilities|misconfigurations|secrets|licenses) ;;
  *) die "--type must be vulnerabilities, misconfigurations, secrets, or licenses" ;;
esac
[[ ${#PURLS[@]} -eq 0 || $TYPE == vulnerabilities ]] || die "--purl is supported only for vulnerability entries"
command -v python3 >/dev/null 2>&1 || die "python3 is required"

python3 - \
  "$TYPE" "$FINDING_ID" "$STATEMENT" "$OWNER" "$EVIDENCE" "$EXPIRES" \
  "$APPROVER" "$OUTPUT_DIR" "$DRY_RUN" "${#PATHS[@]}" "${#PURLS[@]}" \
  "${PATHS[@]}" "${PURLS[@]}" <<'PY'
import hashlib
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

(
    finding_type, finding_id, statement, owner, evidence, expires,
    approver, output_dir, dry_run_text, path_count_text, purl_count_text,
    *scopes,
) = sys.argv[1:]
dry_run = dry_run_text == "1"
path_count = int(path_count_text)
purl_count = int(purl_count_text)
paths = scopes[:path_count]
purls = scopes[path_count:path_count + purl_count]
if len(scopes) != path_count + purl_count:
    raise SystemExit("scope argument count mismatch")

def validate_text(label: str, value: str, maximum: int, minimum: int = 1) -> None:
    if not (minimum <= len(value) <= maximum):
        raise SystemExit(f"{label} must be {minimum}..{maximum} characters")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise SystemExit(f"{label} contains a control character")

validate_text("id", finding_id, 256)
validate_text("statement", statement, 512, 12)
validate_text("owner", owner, 256)
validate_text("evidence", evidence, 1024)
if approver:
    validate_text("approver", approver, 256)
for value in paths:
    validate_text("path", value, 1024)
for value in purls:
    validate_text("purl", value, 2048)
    if not value.startswith("pkg:"):
        raise SystemExit("every --purl value must start with 'pkg:'")

try:
    expiry = date.fromisoformat(expires)
except ValueError as exc:
    raise SystemExit("--expires must be a valid YYYY-MM-DD date") from exc
if expiry <= datetime.now(timezone.utc).date():
    raise SystemExit("--expires must be a future date")

# JSON string syntax is valid YAML double-quoted scalar syntax and safely escapes input.
def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)

lines = [
    "# Review-only Trivy ignore proposal.",
    "# YAML ignore behavior was experimental in upstream documentation verified 2026-08-07.",
    "# Invoke explicitly with --ignorefile and test with the installed release before merge.",
    f"{finding_type}:",
    f"  - id: {quoted(finding_id)}",
]
if paths:
    lines.append("    paths:")
    lines.extend(f"      - {quoted(value)}" for value in paths)
if purls:
    lines.append("    purls:")
    lines.extend(f"      - {quoted(value)}" for value in purls)
lines.extend([
    f"    expired_at: {expires}",
    f"    statement: {quoted(statement)}",
])
yaml_text = "\n".join(lines) + "\n"
yaml_sha = hashlib.sha256(yaml_text.encode("utf-8")).hexdigest()
created_at = datetime.now(timezone.utc).isoformat()
governance = {
    "schema_version": 1,
    "state": "proposed",
    "approved": False,
    "requested_approver": approver or None,
    "created_at": created_at,
    "review_by": expires,
    "owner": owner,
    "evidence": evidence,
    "rationale": statement,
    "trivy_entry": {
        "type": finding_type,
        "id": finding_id,
        "paths": paths,
        "purls": purls,
        "expired_at": expires,
        "statement": statement,
    },
    "trivy_yaml_sha256": yaml_sha,
    "validation_required": [
        "independent owner/evidence/expiry review",
        "parse test with the installed Trivy release",
        "positive test suppressing only the intended finding",
        "negative test retaining an unrelated finding",
        "CI reconciliation of approved governance and Trivy YAML entries",
    ],
    "source": {
        "url": "https://trivy.dev/docs/latest/configuration/filtering/",
        "verified_on": "2026-08-07",
        "feature_status_at_verification": "experimental",
    },
}
governance_text = json.dumps(governance, indent=2, ensure_ascii=False) + "\n"

if dry_run:
    print("--- .trivyignore.yaml ---")
    print(yaml_text, end="")
    print("--- .trivyignore.governance.json ---")
    print(governance_text, end="")
    raise SystemExit(0)

out = Path(output_dir).expanduser()
if out.exists():
    raise SystemExit(f"output directory already exists; choose a new path: {out}")
out.mkdir(mode=0o700, parents=True)
try:
    yaml_path = out / ".trivyignore.yaml"
    governance_path = out / ".trivyignore.governance.json"
    yaml_path.write_text(yaml_text, encoding="utf-8")
    governance_path.write_text(governance_text, encoding="utf-8")
    os.chmod(yaml_path, 0o600)
    os.chmod(governance_path, 0o600)
except Exception:
    # Leave a visible isolated proposal directory for diagnosis; never touch an existing file.
    raise

print(f"Created review-only proposal: {yaml_path}")
print(f"Created governance ledger: {governance_path}")
print("No existing ignore file was modified. Validate and merge through review.")
PY
