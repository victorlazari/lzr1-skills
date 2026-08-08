#!/usr/bin/env python3
"""Calculate MTTA, MTTR, and error-budget burn rates from local evidence."""

from __future__ import annotations

import argparse
import json
import stat
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_MAX_BYTES = 10 * 1024 * 1024
MAX_INCIDENTS = 250_000
TIMESTAMP_FIELDS = ("created_at", "acknowledged_at", "resolved_at")


class MetricsError(ValueError):
    """Expected input validation failure."""


def parse_timestamp(value: str, *, location: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise MetricsError(f"{location} is not a valid ISO-8601 timestamp") from exc
    return parsed


def load_incidents(filename: str | Path, *, max_bytes: int) -> list[dict[str, Any]]:
    path = Path(filename)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise MetricsError(f"cannot access incidents file: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise MetricsError("incidents file must not be a symbolic link")
    if not stat.S_ISREG(metadata.st_mode):
        raise MetricsError("incidents input must be a regular file")
    if metadata.st_size > max_bytes:
        raise MetricsError(f"incidents file exceeds the {max_bytes}-byte limit")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise MetricsError(f"incidents file is not readable UTF-8 text: {exc}") from exc
    try:
        value = json.loads(content)
    except json.JSONDecodeError as exc:
        raise MetricsError(
            f"invalid incidents JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, list):
        raise MetricsError("incidents JSON must be a top-level array")
    if len(value) > MAX_INCIDENTS:
        raise MetricsError(f"incidents array exceeds {MAX_INCIDENTS} records")

    incidents: list[dict[str, Any]] = []
    for index, record in enumerate(value):
        if not isinstance(record, dict):
            raise MetricsError(f"incidents[{index}] must be an object")
        for field in TIMESTAMP_FIELDS:
            if field not in record:
                continue
            raw_timestamp = record[field]
            if not isinstance(raw_timestamp, str) or not raw_timestamp.strip():
                raise MetricsError(f"incidents[{index}].{field} must be a non-empty string")
            parse_timestamp(raw_timestamp, location=f"incidents[{index}].{field}")
        incidents.append(record)
    return incidents


def elapsed_minutes(incident: dict[str, Any], end_field: str, *, index: int) -> float | None:
    if "created_at" not in incident or end_field not in incident:
        return None
    created = parse_timestamp(incident["created_at"], location=f"incidents[{index}].created_at")
    ended = parse_timestamp(incident[end_field], location=f"incidents[{index}].{end_field}")
    if (created.tzinfo is None) != (ended.tzinfo is None):
        raise MetricsError(
            f"incidents[{index}] mixes timezone-aware and timezone-naive timestamps"
        )
    delta = (ended - created).total_seconds() / 60
    if delta < 0:
        raise MetricsError(f"incidents[{index}].{end_field} precedes created_at")
    return delta


def calculate_mean_elapsed(incidents: list[dict[str, Any]], end_field: str) -> float:
    values = [
        value
        for index, incident in enumerate(incidents)
        if (value := elapsed_minutes(incident, end_field, index=index)) is not None
    ]
    return sum(values) / len(values) if values else 0.0


def calculate_mtta(incidents: list[dict[str, Any]]) -> float:
    """Calculate mean time to acknowledge in minutes."""
    return calculate_mean_elapsed(incidents, "acknowledged_at")


def calculate_mttr(incidents: list[dict[str, Any]]) -> float:
    """Calculate mean time to resolve in minutes."""
    return calculate_mean_elapsed(incidents, "resolved_at")


def calculate_burn_rate(slo_target: float, total_requests: int, failed_requests: int) -> float:
    """Calculate the error-rate to error-budget ratio."""
    if total_requests == 0:
        return 0.0
    error_rate = failed_requests / total_requests
    error_budget = 1.0 - (slo_target / 100.0)
    if error_budget == 0:
        return float("inf") if error_rate > 0 else 0.0
    return error_rate / error_budget


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate technical-support operations metrics")
    parser.add_argument("--incidents-file", help="Path to a bounded JSON incident array")
    parser.add_argument("--slo-target", type=float, help="SLO target percentage, from 0 through 100")
    parser.add_argument("--total-requests", type=int, help="Total requests in the time window")
    parser.add_argument("--failed-requests", type=int, help="Failed requests in the time window")
    parser.add_argument(
        "--time-window",
        type=float,
        default=720,
        help="Evidence time window in hours (default: 720); reported for context",
    )
    parser.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Label output as a preview; this script never mutates external systems",
    )
    args = parser.parse_args()
    if args.max_input_bytes <= 0:
        parser.error("--max-input-bytes must be positive")
    return args


def validate_slo_arguments(args: argparse.Namespace) -> bool:
    supplied = [
        args.slo_target is not None,
        args.total_requests is not None,
        args.failed_requests is not None,
    ]
    if any(supplied) and not all(supplied):
        raise MetricsError(
            "--slo-target, --total-requests, and --failed-requests must be provided together"
        )
    if not all(supplied):
        return False
    if not 0 <= args.slo_target <= 100:
        raise MetricsError("--slo-target must be between 0 and 100")
    if args.total_requests < 0 or args.failed_requests < 0:
        raise MetricsError("request counts must be non-negative")
    if args.failed_requests > args.total_requests:
        raise MetricsError("--failed-requests must not exceed --total-requests")
    if args.time_window <= 0:
        raise MetricsError("--time-window must be positive")
    return True


def main() -> int:
    args = parse_args()
    results: dict[str, float | str] = {}
    try:
        if args.incidents_file:
            incidents = load_incidents(args.incidents_file, max_bytes=args.max_input_bytes)
            results["MTTA_minutes"] = round(calculate_mtta(incidents), 2)
            results["MTTR_minutes"] = round(calculate_mttr(incidents), 2)

        if validate_slo_arguments(args):
            burn_rate = calculate_burn_rate(
                args.slo_target,
                args.total_requests,
                args.failed_requests,
            )
            results["Error_Budget_Burn_Rate"] = (
                "Infinity" if burn_rate == float("inf") else round(burn_rate, 2)
            )
            results["Time_Window_Hours"] = args.time_window

        if not results:
            raise MetricsError("provide --incidents-file or the complete SLO argument set")
    except MetricsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("[DRY RUN] Read-only calculated metrics:")
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
