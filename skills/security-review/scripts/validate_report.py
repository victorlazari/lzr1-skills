#!/usr/bin/env python3
"""Validate a security-review JSON report.

This validator checks structure and internal consistency. It does not determine
whether a reported vulnerability is real, whether a CVSS score is correct, or
whether a system is secure or compliant.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

MAX_REPORT_BYTES = 10 * 1024 * 1024
ID_RE = re.compile(r"^SR-[A-Z0-9][A-Z0-9._-]{2,63}$")
REVIEW_ID_RE = re.compile(r"^REV-[A-Z0-9][A-Z0-9._-]{2,63}$")
CONFLICT_ID_RE = re.compile(r"^CONFLICT-[A-Z0-9][A-Z0-9._-]{2,63}$")
UNKNOWN_ID_RE = re.compile(r"^UNKNOWN-[A-Z0-9][A-Z0-9._-]{2,63}$")
CWE_RE = re.compile(r"^CWE-[1-9][0-9]*$")
CAPEC_RE = re.compile(r"^CAPEC-[1-9][0-9]*$")
ATTACK_RE = re.compile(r"^T[0-9]{4}(?:\.[0-9]{3})?$")
DIGEST_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
CVSS_RE = re.compile(r"^CVSS:4\.0(?:/[A-Z]{1,3}:[A-Z0-9]+)+$")
REQUIRED_CVSS_BASE_METRICS = {"AV", "AC", "AT", "PR", "UI", "VC", "VI", "VA", "SC", "SI", "SA"}
STATUS_VALUES = {"candidate", "confirmed", "disputed", "mitigated", "accepted-risk", "false-positive"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
EVIDENCE_TYPES = {
    "code-excerpt", "configuration", "test-result", "artifact-digest",
    "runtime-observation", "advisory", "reasoning-only",
}
REASONING_MODELS = {
    "source-to-sink", "authorization-decision", "state-invariant", "trust-chain",
    "supply-chain", "configuration-exposure", "other",
}
IMPACT_DIMENSIONS = {
    "confidentiality", "integrity", "availability", "privacy", "financial",
    "safety", "supply-chain", "compliance-evidence",
}
VALIDATION_RESULTS = {"not-performed", "passed", "failed", "inconclusive"}
AUTH_ACTIONS = {"read", "local-static-analysis", "local-test", "write", "publish"}
ENVIRONMENTS = {"local", "ci", "development", "staging", "production", "offline", "unknown"}
ROOT_KEYS = {"schema_version", "review", "findings", "conflicts", "unknowns"}
FINDING_REQUIRED = {
    "id", "title", "status", "asset", "locations", "evidence", "reasoning",
    "preconditions", "impact", "taxonomy", "confidence", "remediation",
    "validation", "residual_risk", "conflicts",
}
FINDING_ALLOWED = FINDING_REQUIRED | {"cvss_v4", "live_context", "accepted_risk"}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structure and internal consistency of a security-review JSON report."
    )
    parser.add_argument("report", help="Path to the JSON report")
    parser.add_argument(
        "--final",
        action="store_true",
        help="Apply final-delivery gates: no candidate findings; disputed findings require linked open conflicts",
    )
    parser.add_argument(
        "--as-of",
        metavar="YYYY-MM-DD",
        help="Deterministic reference date for accepted-risk expiry checks; no wall clock is read",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Emit validator results as JSON instead of human-readable text",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=MAX_REPORT_BYTES,
        help=f"Maximum report size in bytes (default: {MAX_REPORT_BYTES})",
    )
    return parser.parse_args(argv)


def non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_string_list(value: Any, *, nonempty: bool = False) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and all(non_empty(item) for item in value)


def check_exact_keys(audit: Audit, path: str, value: Any, required: set[str], allowed: set[str]) -> bool:
    if not isinstance(value, dict):
        audit.error(path, "must be an object")
        return False
    keys = set(value)
    for key in sorted(required - keys):
        audit.error(path, f"missing required field {key!r}")
    for key in sorted(keys - allowed):
        audit.error(path, f"unexpected field {key!r}")
    return not bool(required - keys)


def parse_timestamp(audit: Audit, path: str, value: Any) -> datetime | None:
    if not non_empty(value):
        audit.error(path, "must be a non-empty RFC 3339 timestamp")
        return None
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        audit.error(path, "must be a valid RFC 3339 timestamp")
        return None
    if parsed.tzinfo is None:
        audit.error(path, "timestamp must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def parse_date(audit: Audit, path: str, value: Any) -> date | None:
    if not non_empty(value):
        audit.error(path, "must be an ISO 8601 date")
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        audit.error(path, "must be an ISO 8601 date")
        return None


def check_https(audit: Audit, path: str, value: Any) -> None:
    if not non_empty(value) or not value.startswith("https://") or any(ch.isspace() for ch in value):
        audit.error(path, "must be an HTTPS URL without whitespace")


def check_repo_path(audit: Audit, path: str, value: Any) -> None:
    if not non_empty(value):
        audit.error(path, "must be a non-empty repository-relative path or artifact label")
        return
    text = value.strip().replace("\\", "/")
    pure = PurePosixPath(text)
    if pure.is_absolute() or ".." in pure.parts or any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        audit.error(path, "must not be absolute, traverse parents, or contain control characters")


def validate_review(audit: Audit, value: Any) -> None:
    path = "review"
    required = {"id", "target_revision", "generated_at", "authorization", "scope", "coverage", "source_freshness"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    if not isinstance(value.get("id"), str) or not REVIEW_ID_RE.fullmatch(value["id"]):
        audit.error("review.id", "must match REV-[A-Z0-9][A-Z0-9._-]{2,63}")
    if not non_empty(value.get("target_revision")):
        audit.error("review.target_revision", "must be non-empty")
    parse_timestamp(audit, "review.generated_at", value.get("generated_at"))

    authorization = value.get("authorization")
    auth_required = {"owner_or_authorizer", "allowed_actions", "environment"}
    auth_allowed = auth_required | {"constraints"}
    if check_exact_keys(audit, "review.authorization", authorization, auth_required, auth_allowed):
        if not non_empty(authorization.get("owner_or_authorizer")):
            audit.error("review.authorization.owner_or_authorizer", "must be non-empty")
        actions = authorization.get("allowed_actions")
        if not isinstance(actions, list) or not actions:
            audit.error("review.authorization.allowed_actions", "must be a non-empty array")
        else:
            if len(actions) != len(set(str(item) for item in actions)):
                audit.error("review.authorization.allowed_actions", "must not contain duplicates")
            for index, action in enumerate(actions):
                if action not in AUTH_ACTIONS:
                    audit.error(f"review.authorization.allowed_actions[{index}]", f"must be one of {sorted(AUTH_ACTIONS)}")
        if authorization.get("environment") not in ENVIRONMENTS:
            audit.error("review.authorization.environment", f"must be one of {sorted(ENVIRONMENTS)}")
        if "constraints" in authorization and not is_string_list(authorization["constraints"]):
            audit.error("review.authorization.constraints", "must be an array of non-empty strings")

    scope = value.get("scope")
    if check_exact_keys(audit, "review.scope", scope, {"included", "excluded"}, {"included", "excluded"}):
        if not is_string_list(scope.get("included"), nonempty=True):
            audit.error("review.scope.included", "must be a non-empty array of non-empty strings")
        excluded = scope.get("excluded")
        if not isinstance(excluded, list):
            audit.error("review.scope.excluded", "must be an array")
        else:
            for index, item in enumerate(excluded):
                item_path = f"review.scope.excluded[{index}]"
                if check_exact_keys(audit, item_path, item, {"path_or_area", "reason"}, {"path_or_area", "reason", "approved_by"}):
                    check_repo_path(audit, f"{item_path}.path_or_area", item.get("path_or_area"))
                    if not non_empty(item.get("reason")):
                        audit.error(f"{item_path}.reason", "must be non-empty")
                    if item.get("approved_by") is not None and not non_empty(item.get("approved_by")):
                        audit.error(f"{item_path}.approved_by", "must be null or non-empty")

    coverage_keys = {
        "reviewed", "mechanically_inventoried", "generated", "vendored",
        "binary_or_opaque", "inaccessible", "excluded", "not_applicable",
    }
    coverage = value.get("coverage")
    if check_exact_keys(audit, "review.coverage", coverage, coverage_keys, coverage_keys):
        for key in sorted(coverage_keys):
            count = coverage.get(key)
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                audit.error(f"review.coverage.{key}", "must be a non-negative integer")
        if all(isinstance(coverage.get(key), int) and not isinstance(coverage.get(key), bool) for key in coverage_keys):
            if sum(coverage[key] for key in coverage_keys) == 0:
                audit.warn("review.coverage", "all coverage counts are zero")

    freshness = value.get("source_freshness")
    if not isinstance(freshness, list):
        audit.error("review.source_freshness", "must be an array")
    else:
        for index, item in enumerate(freshness):
            item_path = f"review.source_freshness[{index}]"
            required_keys = {"source", "retrieved_at", "url"}
            if check_exact_keys(audit, item_path, item, required_keys, required_keys):
                if not non_empty(item.get("source")):
                    audit.error(f"{item_path}.source", "must be non-empty")
                parse_timestamp(audit, f"{item_path}.retrieved_at", item.get("retrieved_at"))
                check_https(audit, f"{item_path}.url", item.get("url"))


def validate_locations(audit: Audit, finding_path: str, value: Any) -> None:
    path = f"{finding_path}.locations"
    if not isinstance(value, list) or not value:
        audit.error(path, "must be a non-empty array")
        return
    required = {"path"}
    allowed = {"path", "line_start", "line_end", "symbol", "artifact_digest", "unavailable_reason"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_exact_keys(audit, item_path, item, required, allowed):
            continue
        check_repo_path(audit, f"{item_path}.path", item.get("path"))
        start = item.get("line_start")
        end = item.get("line_end")
        for key, number in (("line_start", start), ("line_end", end)):
            if number is not None and (isinstance(number, bool) or not isinstance(number, int) or number < 1):
                audit.error(f"{item_path}.{key}", "must be null or a positive integer")
        if isinstance(start, int) and isinstance(end, int) and not isinstance(start, bool) and not isinstance(end, bool) and end < start:
            audit.error(item_path, "line_end must not be before line_start")
        if item.get("artifact_digest") is not None and (not isinstance(item.get("artifact_digest"), str) or not DIGEST_RE.fullmatch(item["artifact_digest"])):
            audit.error(f"{item_path}.artifact_digest", "must be null or sha256:<64 lowercase hex>")
        if item.get("unavailable_reason") is not None and not non_empty(item.get("unavailable_reason")):
            audit.error(f"{item_path}.unavailable_reason", "must be null or non-empty")
        if start is None and item.get("artifact_digest") is None and not non_empty(item.get("unavailable_reason")):
            audit.warn(item_path, "has no line, artifact digest, or unavailability reason")


def validate_evidence(audit: Audit, finding_path: str, value: Any) -> None:
    path = f"{finding_path}.evidence"
    if not isinstance(value, list) or not value:
        audit.error(path, "must be a non-empty array")
        return
    required = {"type", "summary", "redacted", "reference"}
    allowed = required | {"digest"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_exact_keys(audit, item_path, item, required, allowed):
            continue
        if item.get("type") not in EVIDENCE_TYPES:
            audit.error(f"{item_path}.type", f"must be one of {sorted(EVIDENCE_TYPES)}")
        if not non_empty(item.get("summary")):
            audit.error(f"{item_path}.summary", "must be non-empty")
        if not isinstance(item.get("redacted"), bool):
            audit.error(f"{item_path}.redacted", "must be boolean")
        if not non_empty(item.get("reference")):
            audit.error(f"{item_path}.reference", "must be non-empty")
        digest = item.get("digest")
        if digest is not None and (not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest)):
            audit.error(f"{item_path}.digest", "must be null or sha256:<64 lowercase hex>")
        summary = str(item.get("summary") or "")
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", summary):
            audit.error(f"{item_path}.summary", "appears to contain a private key; redact evidence")


def validate_reasoning(audit: Audit, path: str, value: Any) -> None:
    required = {"model", "narrative", "steps"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    if value.get("model") not in REASONING_MODELS:
        audit.error(f"{path}.model", f"must be one of {sorted(REASONING_MODELS)}")
    if not non_empty(value.get("narrative")):
        audit.error(f"{path}.narrative", "must be non-empty")
    if not is_string_list(value.get("steps"), nonempty=True):
        audit.error(f"{path}.steps", "must be a non-empty array of non-empty strings")


def validate_taxonomy(audit: Audit, path: str, value: Any) -> None:
    if not check_exact_keys(audit, path, value, {"cwe"}, {"cwe", "capec", "attack"}):
        return
    for key, pattern, required in (("cwe", CWE_RE, True), ("capec", CAPEC_RE, False), ("attack", ATTACK_RE, False)):
        items = value.get(key, [] if not required else None)
        if not isinstance(items, list) or (required and not items):
            audit.error(f"{path}.{key}", "must be a non-empty array" if required else "must be an array")
            continue
        if len(items) != len(set(str(item) for item in items)):
            audit.error(f"{path}.{key}", "must not contain duplicates")
        for index, item in enumerate(items):
            if not isinstance(item, str) or not pattern.fullmatch(item):
                audit.error(f"{path}.{key}[{index}]", "has an invalid identifier")


def validate_confidence(audit: Audit, path: str, value: Any) -> None:
    required = {"level", "rationale", "uncertainties"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    if value.get("level") not in CONFIDENCE_VALUES:
        audit.error(f"{path}.level", f"must be one of {sorted(CONFIDENCE_VALUES)}")
    if not non_empty(value.get("rationale")):
        audit.error(f"{path}.rationale", "must be non-empty")
    if not is_string_list(value.get("uncertainties")):
        audit.error(f"{path}.uncertainties", "must be an array of non-empty strings")


def validate_cvss(audit: Audit, path: str, value: Any) -> None:
    if value is None:
        return
    required = {"vector", "metric_rationale"}
    allowed = required | {"base_score"}
    if not check_exact_keys(audit, path, value, required, allowed):
        return
    vector = value.get("vector")
    if not isinstance(vector, str) or not CVSS_RE.fullmatch(vector):
        audit.error(f"{path}.vector", "must be a syntactically shaped CVSS:4.0 vector")
        metrics: set[str] = set()
    else:
        metrics = {segment.split(":", 1)[0] for segment in vector.split("/")[1:]}
        missing = sorted(REQUIRED_CVSS_BASE_METRICS - metrics)
        if missing:
            audit.error(f"{path}.vector", f"missing CVSS v4 base metrics: {', '.join(missing)}")
    score = value.get("base_score")
    if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 10):
        audit.error(f"{path}.base_score", "must be null or a number from 0 to 10")
    rationale = value.get("metric_rationale")
    if not isinstance(rationale, dict) or not rationale:
        audit.error(f"{path}.metric_rationale", "must be a non-empty object")
    else:
        for metric in sorted(metrics):
            if not non_empty(rationale.get(metric)):
                audit.error(f"{path}.metric_rationale.{metric}", "must explain the selected metric")


def validate_live_context(audit: Audit, path: str, value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        audit.error(path, "must be an array")
        return
    required = {"source", "identifier", "status", "retrieved_at", "url"}
    allowed_sources = {"CISA-KEV", "EPSS", "CVE", "NVD", "vendor-advisory", "other"}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not check_exact_keys(audit, item_path, item, required, required):
            continue
        if item.get("source") not in allowed_sources:
            audit.error(f"{item_path}.source", f"must be one of {sorted(allowed_sources)}")
        for key in ("identifier", "status"):
            if not non_empty(item.get(key)):
                audit.error(f"{item_path}.{key}", "must be non-empty")
        parse_timestamp(audit, f"{item_path}.retrieved_at", item.get("retrieved_at"))
        check_https(audit, f"{item_path}.url", item.get("url"))


def validate_remediation(audit: Audit, path: str, value: Any) -> None:
    required = {"recommendation", "alternatives", "compatibility", "rollout", "rollback"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    for key in ("recommendation", "compatibility", "rollout", "rollback"):
        if not non_empty(value.get(key)):
            audit.error(f"{path}.{key}", "must be non-empty")
    if not is_string_list(value.get("alternatives")):
        audit.error(f"{path}.alternatives", "must be an array of non-empty strings")


def validate_validation(audit: Audit, path: str, value: Any) -> None:
    required = {"method", "expected", "performed", "result", "evidence"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    for key in ("method", "expected"):
        if not non_empty(value.get(key)):
            audit.error(f"{path}.{key}", "must be non-empty")
    performed = value.get("performed")
    result = value.get("result")
    if not isinstance(performed, bool):
        audit.error(f"{path}.performed", "must be boolean")
    if result not in VALIDATION_RESULTS:
        audit.error(f"{path}.result", f"must be one of {sorted(VALIDATION_RESULTS)}")
    if performed is False and result != "not-performed":
        audit.error(path, "performed=false requires result=not-performed")
    if performed is True and result == "not-performed":
        audit.error(path, "performed=true cannot use result=not-performed")
    if not is_string_list(value.get("evidence")):
        audit.error(f"{path}.evidence", "must be an array of non-empty strings")


def validate_accepted_risk(audit: Audit, path: str, value: Any, *, as_of: date | None) -> None:
    required = {"owner", "rationale", "compensating_controls", "review_by", "expires_at"}
    if not check_exact_keys(audit, path, value, required, required):
        return
    for key in ("owner", "rationale"):
        if not non_empty(value.get(key)):
            audit.error(f"{path}.{key}", "must be non-empty")
    if not is_string_list(value.get("compensating_controls"), nonempty=True):
        audit.error(f"{path}.compensating_controls", "must be a non-empty array of non-empty strings")
    review_by = parse_date(audit, f"{path}.review_by", value.get("review_by"))
    expires = parse_date(audit, f"{path}.expires_at", value.get("expires_at"))
    if review_by and expires and expires < review_by:
        audit.error(path, "expires_at must not precede review_by")
    if as_of and expires and expires < as_of:
        audit.error(f"{path}.expires_at", f"accepted-risk record is expired as of {as_of.isoformat()}")


def validate_finding(audit: Audit, value: Any, index: int, *, final: bool, as_of: date | None) -> str | None:
    path = f"findings[{index}]"
    if not check_exact_keys(audit, path, value, FINDING_REQUIRED, FINDING_ALLOWED):
        return None
    finding_id = value.get("id")
    if not isinstance(finding_id, str) or not ID_RE.fullmatch(finding_id):
        audit.error(f"{path}.id", "must match SR-[A-Z0-9][A-Z0-9._-]{2,63}")
        finding_id = None
    for key in ("title", "asset"):
        if not non_empty(value.get(key)):
            audit.error(f"{path}.{key}", "must be non-empty")
    status = value.get("status")
    if status not in STATUS_VALUES:
        audit.error(f"{path}.status", f"must be one of {sorted(STATUS_VALUES)}")
    if final and status == "candidate":
        audit.error(f"{path}.status", "candidate status is not allowed with --final")

    validate_locations(audit, path, value.get("locations"))
    validate_evidence(audit, path, value.get("evidence"))
    validate_reasoning(audit, f"{path}.reasoning", value.get("reasoning"))
    if not is_string_list(value.get("preconditions"), nonempty=True):
        audit.error(f"{path}.preconditions", "must be a non-empty array of non-empty strings")

    impact = value.get("impact")
    if check_exact_keys(audit, f"{path}.impact", impact, {"dimensions", "narrative"}, {"dimensions", "narrative"}):
        dimensions = impact.get("dimensions")
        if not isinstance(dimensions, list) or not dimensions:
            audit.error(f"{path}.impact.dimensions", "must be a non-empty array")
        else:
            if len(dimensions) != len(set(str(item) for item in dimensions)):
                audit.error(f"{path}.impact.dimensions", "must not contain duplicates")
            for dim_index, dimension in enumerate(dimensions):
                if dimension not in IMPACT_DIMENSIONS:
                    audit.error(f"{path}.impact.dimensions[{dim_index}]", f"must be one of {sorted(IMPACT_DIMENSIONS)}")
        if not non_empty(impact.get("narrative")):
            audit.error(f"{path}.impact.narrative", "must be non-empty")

    validate_taxonomy(audit, f"{path}.taxonomy", value.get("taxonomy"))
    validate_confidence(audit, f"{path}.confidence", value.get("confidence"))
    validate_cvss(audit, f"{path}.cvss_v4", value.get("cvss_v4"))
    validate_live_context(audit, f"{path}.live_context", value.get("live_context"))
    validate_remediation(audit, f"{path}.remediation", value.get("remediation"))
    validate_validation(audit, f"{path}.validation", value.get("validation"))

    residual = value.get("residual_risk")
    if check_exact_keys(audit, f"{path}.residual_risk", residual, {"summary"}, {"summary", "owner", "review_by"}):
        if not non_empty(residual.get("summary")):
            audit.error(f"{path}.residual_risk.summary", "must be non-empty")
        if residual.get("owner") is not None and not non_empty(residual.get("owner")):
            audit.error(f"{path}.residual_risk.owner", "must be null or non-empty")
        if residual.get("review_by") is not None:
            parse_date(audit, f"{path}.residual_risk.review_by", residual.get("review_by"))

    conflicts = value.get("conflicts")
    if not isinstance(conflicts, list):
        audit.error(f"{path}.conflicts", "must be an array")
    else:
        if len(conflicts) != len(set(str(item) for item in conflicts)):
            audit.error(f"{path}.conflicts", "must not contain duplicates")
        for conflict_index, conflict_id in enumerate(conflicts):
            if not isinstance(conflict_id, str) or not CONFLICT_ID_RE.fullmatch(conflict_id):
                audit.error(f"{path}.conflicts[{conflict_index}]", "has an invalid conflict ID")

    if status == "accepted-risk":
        if "accepted_risk" not in value:
            audit.error(path, "accepted-risk status requires accepted_risk details")
        else:
            validate_accepted_risk(audit, f"{path}.accepted_risk", value.get("accepted_risk"), as_of=as_of)
    elif "accepted_risk" in value:
        audit.error(f"{path}.accepted_risk", "is allowed only when status is accepted-risk")
    if status == "mitigated":
        validation = value.get("validation")
        if not isinstance(validation, dict) or validation.get("performed") is not True or validation.get("result") != "passed":
            audit.error(f"{path}.validation", "mitigated status requires performed=true and result=passed")
    if status == "false-positive":
        confidence = value.get("confidence")
        validation = value.get("validation")
        if not isinstance(confidence, dict) or not non_empty(confidence.get("rationale")):
            audit.error(f"{path}.confidence.rationale", "false-positive status requires rejection rationale")
        if not isinstance(validation, dict) or not non_empty(validation.get("method")):
            audit.error(f"{path}.validation", "false-positive status requires validation method")
    return finding_id


def validate_conflicts(audit: Audit, value: Any, finding_ids: set[str]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    if not isinstance(value, list):
        audit.error("conflicts", "must be an array")
        return statuses
    for index, item in enumerate(value):
        path = f"conflicts[{index}]"
        required = {"id", "finding_ids", "status", "positions"}
        allowed = required | {"resolution"}
        if not check_exact_keys(audit, path, item, required, allowed):
            continue
        conflict_id = item.get("id")
        if not isinstance(conflict_id, str) or not CONFLICT_ID_RE.fullmatch(conflict_id):
            audit.error(f"{path}.id", "has an invalid conflict ID")
            continue
        if conflict_id in statuses:
            audit.error(f"{path}.id", "duplicates another conflict ID")
        status = item.get("status")
        if status not in {"open", "resolved"}:
            audit.error(f"{path}.status", "must be open or resolved")
        else:
            statuses[conflict_id] = status
        related = item.get("finding_ids")
        if not isinstance(related, list) or not related:
            audit.error(f"{path}.finding_ids", "must be a non-empty array")
        else:
            if len(related) != len(set(str(found) for found in related)):
                audit.error(f"{path}.finding_ids", "must not contain duplicates")
            for finding_index, finding_id in enumerate(related):
                if finding_id not in finding_ids:
                    audit.error(f"{path}.finding_ids[{finding_index}]", "does not reference a known finding")
        positions = item.get("positions")
        if not is_string_list(positions) or len(positions) < 2:
            audit.error(f"{path}.positions", "must contain at least two non-empty positions")
        resolution = item.get("resolution")
        if status == "resolved" and not non_empty(resolution):
            audit.error(f"{path}.resolution", "resolved conflict requires a resolution")
        if status == "open" and resolution is not None and not non_empty(resolution):
            audit.error(f"{path}.resolution", "must be null, absent, or non-empty")
    return statuses


def validate_unknowns(audit: Audit, value: Any) -> None:
    if not isinstance(value, list):
        audit.error("unknowns", "must be an array")
        return
    seen: set[str] = set()
    required = {"id", "description", "potential_impact", "owner"}
    for index, item in enumerate(value):
        path = f"unknowns[{index}]"
        if not check_exact_keys(audit, path, item, required, required):
            continue
        unknown_id = item.get("id")
        if not isinstance(unknown_id, str) or not UNKNOWN_ID_RE.fullmatch(unknown_id):
            audit.error(f"{path}.id", "has an invalid unknown ID")
        elif unknown_id in seen:
            audit.error(f"{path}.id", "duplicates another unknown ID")
        else:
            seen.add(unknown_id)
        for key in ("description", "potential_impact"):
            if not non_empty(item.get(key)):
                audit.error(f"{path}.{key}", "must be non-empty")
        if item.get("owner") is not None and not non_empty(item.get("owner")):
            audit.error(f"{path}.owner", "must be null or non-empty")


def validate_report(report: Any, *, final: bool, as_of: date | None = None) -> Audit:
    audit = Audit()
    if not isinstance(report, dict):
        audit.error("$", "report must be an object")
        return audit
    check_exact_keys(audit, "$", report, ROOT_KEYS, ROOT_KEYS)
    if report.get("schema_version") != "1.0":
        audit.error("schema_version", "must equal 1.0")
    validate_review(audit, report.get("review"))

    findings = report.get("findings")
    finding_ids: set[str] = set()
    finding_conflicts: dict[str, list[str]] = {}
    if not isinstance(findings, list):
        audit.error("findings", "must be an array")
    else:
        for index, finding in enumerate(findings):
            finding_id = validate_finding(audit, finding, index, final=final, as_of=as_of)
            if finding_id:
                if finding_id in finding_ids:
                    audit.error(f"findings[{index}].id", "duplicates another finding ID")
                finding_ids.add(finding_id)
                if isinstance(finding, dict) and isinstance(finding.get("conflicts"), list):
                    finding_conflicts[finding_id] = [item for item in finding["conflicts"] if isinstance(item, str)]

    conflict_statuses = validate_conflicts(audit, report.get("conflicts"), finding_ids)
    for finding_id, conflict_ids in finding_conflicts.items():
        for conflict_id in conflict_ids:
            if conflict_id not in conflict_statuses:
                audit.error(f"finding {finding_id}", f"references missing conflict {conflict_id}")
    if isinstance(report.get("conflicts"), list):
        for index, conflict in enumerate(report["conflicts"]):
            if not isinstance(conflict, dict) or not isinstance(conflict.get("id"), str):
                continue
            conflict_id = conflict["id"]
            for finding_id in conflict.get("finding_ids", []) if isinstance(conflict.get("finding_ids"), list) else []:
                if finding_id in finding_conflicts and conflict_id not in finding_conflicts[finding_id]:
                    audit.error(f"conflicts[{index}]", f"finding {finding_id} does not link back to {conflict_id}")
            if conflict.get("status") == "open":
                for finding_id in conflict.get("finding_ids", []) if isinstance(conflict.get("finding_ids"), list) else []:
                    if isinstance(findings, list):
                        status = next((item.get("status") for item in findings if isinstance(item, dict) and item.get("id") == finding_id), None)
                        if status != "disputed":
                            audit.error(f"conflicts[{index}]", f"open conflict requires finding {finding_id} to have disputed status")

    validate_unknowns(audit, report.get("unknowns"))
    return audit


def load_report(path_text: str, max_bytes: int) -> Any:
    path = Path(path_text).expanduser()
    resolved = path.resolve(strict=True)
    if not resolved.is_file() or resolved.is_symlink():
        raise ValueError("report must be a real regular file, not a directory or symlink")
    size = resolved.stat().st_size
    if size > max_bytes:
        raise ValueError(f"report is {size} bytes; maximum is {max_bytes}")
    with resolved.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def emit(audit: Audit, *, json_output: bool) -> None:
    payload = {
        "valid": not audit.errors,
        "errors": audit.errors,
        "warnings": audit.warnings,
    }
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if audit.errors:
        print(f"INVALID: {len(audit.errors)} error(s), {len(audit.warnings)} warning(s)")
        for error in audit.errors:
            print(f"ERROR: {error}")
    else:
        print(f"VALID: 0 errors, {len(audit.warnings)} warning(s)")
    for warning in audit.warnings:
        print(f"WARNING: {warning}")
    print("Structural validity does not prove that findings are correct or that the target is secure.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.max_bytes < 1:
        print("error: --max-bytes must be positive", file=sys.stderr)
        return 2
    as_of = None
    if args.as_of is not None:
        try:
            as_of = date.fromisoformat(args.as_of)
        except ValueError:
            print("error: --as-of must be an ISO 8601 date in YYYY-MM-DD form", file=sys.stderr)
            return 2
    try:
        report = load_report(args.report, args.max_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        if args.json_output:
            print(json.dumps({"valid": False, "errors": [f"cannot load report: {exc}"], "warnings": []}, indent=2))
        else:
            print(f"error: cannot load report: {exc}", file=sys.stderr)
        return 2
    audit = validate_report(report, final=args.final, as_of=as_of)
    emit(audit, json_output=args.json_output)
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
