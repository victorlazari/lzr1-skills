#!/usr/bin/env python3
"""Audit a local Jira field-scheme export against documented count limits.

Verified against upstream: 2026-08-07.
This utility is intentionally offline. It does not accept credentials, contact a
Jira site, or claim that a local export proves live-instance compliance.
"""

from __future__ import annotations

import argparse
import json
import stat
import sys
from pathlib import Path
from typing import Any

FIELD_LIMIT = 700
WORK_TYPE_LIMIT = 150
DEFAULT_MAX_BYTES = 5 * 1024 * 1024
MAX_RECORDS_PER_COLLECTION = 100_000

MOCK_EVIDENCE = {
    "migration_status": "assumed-for-test-fixture",
    "spaces": [
        {"id": "10000", "key": "PROJ1", "name": "Project 1", "fieldCount": 450},
        {"id": "10001", "key": "PROJ2", "name": "Project 2", "fieldCount": 750},
    ],
    "schemes": [
        {"id": "1", "name": "Default Scheme", "workTypeCount": 50},
        {"id": "2", "name": "Complex Scheme", "workTypeCount": 160},
    ],
}


class AuditInputError(ValueError):
    """Expected local-evidence validation failure."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit an offline Jira field-scheme export against the documented 2026 count limits."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Local JSON export containing spaces and schemes arrays")
    source.add_argument("--mock", action="store_true", help="Run the built-in non-production fixture")
    parser.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args()
    if args.max_input_bytes <= 0:
        parser.error("--max-input-bytes must be positive")
    return args


def load_json_object(filename: str | Path, max_bytes: int) -> dict[str, Any]:
    path = Path(filename)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise AuditInputError(f"cannot access input file: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise AuditInputError("input file must not be a symbolic link")
    if not stat.S_ISREG(metadata.st_mode):
        raise AuditInputError("input must be a regular file")
    if metadata.st_size > max_bytes:
        raise AuditInputError(f"input exceeds the {max_bytes}-byte limit")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise AuditInputError(f"input is not readable UTF-8 text: {exc}") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AuditInputError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise AuditInputError("input JSON must be a top-level object")
    return value


def required_text(record: dict[str, Any], field: str, location: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AuditInputError(f"{location}.{field} must be a non-empty string")
    return value


def required_count(record: dict[str, Any], field: str, location: str) -> int:
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AuditInputError(f"{location}.{field} must be a non-negative integer")
    return value


def validate_collection(value: Any, *, name: str, count_field: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise AuditInputError(f"{name} must be an array")
    if len(value) > MAX_RECORDS_PER_COLLECTION:
        raise AuditInputError(f"{name} exceeds {MAX_RECORDS_PER_COLLECTION} records")
    records: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        location = f"{name}[{index}]"
        if not isinstance(item, dict):
            raise AuditInputError(f"{location} must be an object")
        required_text(item, "id", location)
        required_text(item, "name", location)
        if name == "spaces":
            required_text(item, "key", location)
        required_count(item, count_field, location)
        records.append(item)
    return records


def validate_evidence(value: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    allowed = {"migration_status", "spaces", "schemes"}
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise AuditInputError(f"unknown top-level fields: {', '.join(unknown)}")
    migration_status = value.get("migration_status")
    if not isinstance(migration_status, str) or not migration_status.strip():
        raise AuditInputError("migration_status must be a non-empty evidence string")
    spaces = validate_collection(value.get("spaces"), name="spaces", count_field="fieldCount")
    schemes = validate_collection(value.get("schemes"), name="schemes", count_field="workTypeCount")
    return spaces, schemes, migration_status


def audit_spaces(spaces: list[dict[str, Any]]) -> int:
    print(f"\n--- Auditing Spaces (Limit: {FIELD_LIMIT} fields/space) ---")
    violations = 0
    for space in spaces:
        count = space["fieldCount"]
        label = f"{space['name']} ({space['key']})"
        if count > FIELD_LIMIT:
            print(f"VIOLATION: Space {label!r} has {count} fields.")
            violations += 1
        else:
            print(f"OK: Space {label!r} has {count} fields.")
    return violations


def audit_schemes(schemes: list[dict[str, Any]]) -> int:
    print(f"\n--- Auditing Field Schemes (Limit: {WORK_TYPE_LIMIT} work types/scheme) ---")
    violations = 0
    for scheme in schemes:
        count = scheme["workTypeCount"]
        if count > WORK_TYPE_LIMIT:
            print(f"VIOLATION: Scheme {scheme['name']!r} has {count} work types.")
            violations += 1
        else:
            print(f"OK: Scheme {scheme['name']!r} has {count} work types.")
    return violations


def main() -> int:
    args = parse_args()
    try:
        raw_evidence = MOCK_EVIDENCE if args.mock else load_json_object(args.input, args.max_input_bytes)
        spaces, schemes, migration_status = validate_evidence(raw_evidence)
    except AuditInputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    source = "built-in test fixture" if args.mock else args.input
    print(f"Evidence source: {source}")
    print(f"Migration-status evidence: {migration_status}")
    print("Boundary: offline snapshot only; no live Jira request was performed.")

    total_violations = audit_spaces(spaces) + audit_schemes(schemes)
    print(f"\nAudit Complete. Total Violations Found: {total_violations}")
    return 1 if total_violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
