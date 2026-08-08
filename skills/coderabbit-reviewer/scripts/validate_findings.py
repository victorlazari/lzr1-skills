#!/usr/bin/env python3
"""Validate a CodeRabbit ``review --agent`` NDJSON event stream.

This validator checks transport structure and documented event invariants. It does
not determine whether a finding is correct, whether code is safe, or whether a
review covered the intended changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO

MAX_STREAM_BYTES = 50 * 1024 * 1024
MAX_LINE_BYTES = 2 * 1024 * 1024
KNOWN_TYPES = {"review_context", "status", "heartbeat", "finding", "complete", "error"}
TERMINAL_TYPES = {"complete", "error"}
SEVERITIES = {"critical", "major", "minor", "trivial", "info"}


class Audit:
    """Collect deterministic validation observations."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{location}: {message}")

    def warn(self, location: str, message: str) -> None:
        self.warnings.append(f"{location}: {message}")


class StreamResult:
    """Validation result and safe summary data."""

    def __init__(self) -> None:
        self.audit = Audit()
        self.bytes_read = 0
        self.sha256 = hashlib.sha256()
        self.nonempty_lines = 0
        self.event_counts = {name: 0 for name in sorted(KNOWN_TYPES)}
        self.unknown_event_counts: dict[str, int] = {}
        self.severity_counts = {name: 0 for name in sorted(SEVERITIES)}
        self.unknown_severity_counts: dict[str, int] = {}
        self.findings_observed = 0
        self.review_context_seen = False
        self.terminal_type: str | None = None
        self.terminal_status: str | None = None
        self.terminal_findings: int | None = None
        self.terminal_line: int | None = None

    @property
    def structurally_valid(self) -> bool:
        return not self.audit.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.structurally_valid,
            "outcome": outcome_for(self),
            "errors": self.audit.errors,
            "warnings": self.audit.warnings,
            "stream": {
                "bytes": self.bytes_read,
                "sha256": self.sha256.hexdigest(),
                "nonempty_lines": self.nonempty_lines,
                "event_counts": self.event_counts,
                "unknown_event_counts": self.unknown_event_counts,
            },
            "review": {
                "review_context_seen": self.review_context_seen,
                "findings_observed": self.findings_observed,
                "severity_counts": self.severity_counts,
                "unknown_severity_counts": self.unknown_severity_counts,
                "terminal_type": self.terminal_type,
                "terminal_status": self.terminal_status,
                "terminal_findings": self.terminal_findings,
                "terminal_line": self.terminal_line,
            },
        }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate CodeRabbit agent-mode NDJSON without executing CodeRabbit or project code."
    )
    parser.add_argument("stream", help="Path to stdout NDJSON from `coderabbit review --agent`, or - for stdin")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Reject undocumented event types and ordering anomalies instead of warning",
    )
    parser.add_argument(
        "--process-exit-code",
        type=int,
        help="Correlate the captured CodeRabbit process exit code with the terminal event",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=MAX_STREAM_BYTES,
        help=f"Maximum stream size in bytes (default: {MAX_STREAM_BYTES})",
    )
    parser.add_argument(
        "--max-line-bytes",
        type=int,
        default=MAX_LINE_BYTES,
        help=f"Maximum non-empty line size in bytes (default: {MAX_LINE_BYTES})",
    )
    parser.add_argument("--json-output", action="store_true", help="Emit a JSON validation summary")
    return parser.parse_args(argv)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def has_explanation(value: Any) -> bool:
    if nonempty_string(value):
        return True
    if isinstance(value, list):
        return any(has_explanation(item) for item in value)
    if isinstance(value, dict):
        return any(has_explanation(item) for item in value.values())
    return False


def check_repo_path(audit: Audit, location: str, value: Any) -> None:
    if not nonempty_string(value):
        audit.error(location, "must be a non-empty repository-relative path")
        return
    text = value.strip().replace("\\", "/")
    pure = PurePosixPath(text)
    if pure.is_absolute() or ".." in pure.parts:
        audit.error(location, "must not be absolute or traverse parent directories")
    if any(ord(character) < 32 or ord(character) == 127 for character in text):
        audit.error(location, "must not contain control characters")


def validate_finding(result: StreamResult, event: dict[str, Any], line_number: int) -> None:
    audit = result.audit
    location = f"line {line_number} finding"
    severity = event.get("severity")
    if not nonempty_string(severity):
        audit.error(f"{location}.severity", "must be a non-empty string")
    elif severity not in SEVERITIES:
        result.unknown_severity_counts[severity] = result.unknown_severity_counts.get(severity, 0) + 1
        audit.warn(f"{location}.severity", f"undocumented value {severity!r}; preserved but not normalized")
    else:
        result.severity_counts[severity] += 1

    check_repo_path(audit, f"{location}.fileName", event.get("fileName"))

    for key in ("codegenInstructions", "comment"):
        if key in event and not isinstance(event[key], str):
            audit.error(f"{location}.{key}", "must be a string when present")

    if not any(has_explanation(event.get(key)) for key in ("codegenInstructions", "comment", "suggestions")):
        audit.warn(location, "has no non-empty instructions, comment, or suggestions; triage as needs-evidence")


def validate_terminal(result: StreamResult, event: dict[str, Any], line_number: int) -> None:
    audit = result.audit
    event_type = event["type"]
    location = f"line {line_number} {event_type}"
    if result.terminal_type is not None:
        audit.error(location, f"duplicate terminal event after {result.terminal_type!r} on line {result.terminal_line}")
        return

    result.terminal_type = event_type
    result.terminal_line = line_number
    status_value = event.get("status")
    if status_value is not None:
        if nonempty_string(status_value):
            result.terminal_status = status_value
        else:
            audit.error(f"{location}.status", "must be a non-empty string when present")

    if event_type == "complete":
        findings = event.get("findings")
        if findings is None:
            audit.warn(location, "does not declare a findings count")
        elif isinstance(findings, bool) or not isinstance(findings, int) or findings < 0:
            audit.error(f"{location}.findings", "must be a non-negative integer when present")
        else:
            result.terminal_findings = findings
            if findings != result.findings_observed:
                audit.error(
                    f"{location}.findings",
                    f"declares {findings}, but {result.findings_observed} finding event(s) were observed",
                )
        if result.terminal_status == "review_skipped" and result.findings_observed != 0:
            audit.error(location, "review_skipped must not contain finding events")

    if event_type == "error":
        candidates = event.get("candidates")
        if candidates is not None and not isinstance(candidates, list):
            audit.error(f"{location}.candidates", "must be an array when present")
        note = event.get("candidatesNote")
        if note is not None and not isinstance(note, str):
            audit.error(f"{location}.candidatesNote", "must be a string when present")


def validate_event(result: StreamResult, event: Any, line_number: int, *, strict: bool) -> None:
    audit = result.audit
    location = f"line {line_number}"
    if not isinstance(event, dict):
        audit.error(location, "each NDJSON value must be an object")
        return

    event_type = event.get("type")
    if not nonempty_string(event_type):
        audit.error(location, "event field 'type' must be a non-empty string")
        return

    if result.terminal_type is not None:
        audit.error(location, f"event {event_type!r} appears after terminal event on line {result.terminal_line}")

    if event_type not in KNOWN_TYPES:
        result.unknown_event_counts[event_type] = result.unknown_event_counts.get(event_type, 0) + 1
        message = f"undocumented event type {event_type!r}; preserved without interpretation"
        if strict:
            audit.error(location, message)
        else:
            audit.warn(location, message)
        return

    result.event_counts[event_type] += 1

    if result.nonempty_lines == 1 and event_type != "review_context":
        message = f"first event is {event_type!r}, not documented review context"
        if strict:
            audit.error(location, message)
        else:
            audit.warn(location, message)

    if event_type == "review_context":
        if result.review_context_seen:
            message = "multiple review_context events observed"
            if strict:
                audit.error(location, message)
            else:
                audit.warn(location, message)
        result.review_context_seen = True
    elif event_type == "finding":
        result.findings_observed += 1
        validate_finding(result, event, line_number)
    elif event_type in TERMINAL_TYPES:
        validate_terminal(result, event, line_number)
    elif event_type == "status" and "status" in event and not nonempty_string(event.get("status")):
        audit.error(f"{location} status.status", "must be a non-empty string when present")


def validate_binary_stream(
    handle: BinaryIO,
    *,
    strict: bool = False,
    max_bytes: int = MAX_STREAM_BYTES,
    max_line_bytes: int = MAX_LINE_BYTES,
    process_exit_code: int | None = None,
) -> StreamResult:
    result = StreamResult()
    if max_bytes < 1 or max_line_bytes < 1:
        result.audit.error("arguments", "size limits must be positive integers")
        return result

    for line_number, raw_line in enumerate(handle, start=1):
        result.bytes_read += len(raw_line)
        result.sha256.update(raw_line)
        if result.bytes_read > max_bytes:
            result.audit.error("stream", f"exceeds maximum size of {max_bytes} bytes")
            break
        if len(raw_line) > max_line_bytes:
            result.audit.error(f"line {line_number}", f"exceeds maximum size of {max_line_bytes} bytes")
            continue
        if b"\x00" in raw_line:
            result.audit.error(f"line {line_number}", "contains a NUL byte")
            continue
        if not raw_line.strip():
            continue
        result.nonempty_lines += 1
        try:
            decoded = raw_line.decode("utf-8")
        except UnicodeDecodeError as exc:
            result.audit.error(f"line {line_number}", f"is not valid UTF-8: {exc}")
            continue
        try:
            event = json.loads(decoded)
        except json.JSONDecodeError as exc:
            result.audit.error(f"line {line_number}", f"invalid JSON at column {exc.colno}: {exc.msg}")
            continue
        validate_event(result, event, line_number, strict=strict)

    if result.nonempty_lines == 0:
        result.audit.error("stream", "contains no events")
    if not result.review_context_seen:
        message = "contains no review_context event"
        if strict:
            result.audit.error("stream", message)
        else:
            result.audit.warn("stream", message)
    if result.terminal_type is None:
        result.audit.error("stream", "contains no terminal complete or error event")

    if process_exit_code is not None:
        if process_exit_code < 0 or process_exit_code > 255:
            result.audit.error("process_exit_code", "must be between 0 and 255")
        elif result.terminal_type == "complete" and process_exit_code != 0:
            result.audit.error(
                "process_exit_code",
                f"is {process_exit_code}, but the stream terminates with complete",
            )
        elif result.terminal_type == "error" and process_exit_code == 0:
            result.audit.warn("process_exit_code", "is 0 even though the stream terminates with error")

    return result


def open_stream(path_text: str, max_bytes: int) -> tuple[BinaryIO, bool]:
    if path_text == "-":
        return sys.stdin.buffer, False
    path = Path(path_text)
    file_stat = path.lstat()
    if stat.S_ISLNK(file_stat.st_mode):
        raise ValueError("stream path must not be a symbolic link")
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError("stream path must be a regular file")
    if file_stat.st_size > max_bytes:
        raise ValueError(f"stream size {file_stat.st_size} exceeds maximum {max_bytes}")
    return path.open("rb"), True


def validate_path(
    path_text: str,
    *,
    strict: bool = False,
    max_bytes: int = MAX_STREAM_BYTES,
    max_line_bytes: int = MAX_LINE_BYTES,
    process_exit_code: int | None = None,
) -> StreamResult:
    try:
        handle, should_close = open_stream(path_text, max_bytes)
    except (OSError, ValueError) as exc:
        result = StreamResult()
        result.audit.error("stream", f"cannot open safely: {exc}")
        return result
    try:
        return validate_binary_stream(
            handle,
            strict=strict,
            max_bytes=max_bytes,
            max_line_bytes=max_line_bytes,
            process_exit_code=process_exit_code,
        )
    finally:
        if should_close:
            handle.close()


def outcome_for(result: StreamResult) -> str:
    if result.audit.errors:
        return "invalid"
    if result.terminal_type == "error":
        return "review_error"
    if result.terminal_status == "review_skipped":
        return "review_skipped"
    if result.terminal_type == "complete":
        return "complete"
    return "invalid"


def emit(result: StreamResult, *, json_output: bool) -> None:
    payload = result.as_dict()
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    state = "PASS" if result.structurally_valid else "FAIL"
    print(
        f"{state}: outcome={payload['outcome']}; "
        f"{len(result.audit.errors)} error(s), {len(result.audit.warnings)} warning(s)"
    )
    print(
        f"Stream: {result.bytes_read} byte(s), sha256:{result.sha256.hexdigest()}, "
        f"{result.nonempty_lines} event line(s)"
    )
    print(
        f"Review: terminal={result.terminal_type or 'missing'}, "
        f"status={result.terminal_status or 'unspecified'}, findings={result.findings_observed}"
    )
    for error in result.audit.errors:
        print(f"ERROR: {error}")
    for warning in result.audit.warnings:
        print(f"WARNING: {warning}")
    print("This validates event transport and consistency, not finding correctness or review coverage.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = validate_path(
        args.stream,
        strict=args.strict,
        max_bytes=args.max_bytes,
        max_line_bytes=args.max_line_bytes,
        process_exit_code=args.process_exit_code,
    )
    emit(result, json_output=args.json_output)
    if result.audit.errors:
        return 1
    if result.terminal_type == "error":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
