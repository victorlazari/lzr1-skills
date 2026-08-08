#!/usr/bin/env python3
"""Build a read-only Google Calendar correction plan from bounded JSON evidence.

The script never mutates a calendar. It validates local exports and writes an
action-plan artifact for separate human review and explicitly authorized use.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_MAX_BYTES = 10 * 1024 * 1024
MAX_EVENTS = 100_000
MAX_SCHEDULE_ENTRIES = 100_000


class ValidationError(ValueError):
    """Expected input or output validation failure."""


def normalize_team(name: str) -> str:
    """Normalize team names for matching, handling common aliases."""
    team_aliases = {
        "ir iran": "iran",
        "korea republic": "south korea",
        "côte d'ivoire": "ivory coast",
        "cote d'ivoire": "ivory coast",
        "cabo verde": "cape verde",
        "usa": "united states",
        "türkiye": "turkiye",
    }
    normalized = name.lower().strip()
    return team_aliases.get(normalized, normalized)


def normalize_match_name(summary: str) -> str:
    """Extract team names from a calendar event summary."""
    value = summary.replace("World Cup 2026: ", "")
    if "—" in value:
        value = value.split("—", 1)[0].strip()
    if "Opening Match" in value:
        if "(" in value and ")" in value:
            inner = value[value.index("(") + 1 : value.index(")")]
            if " vs " in inner:
                value = inner
        else:
            value = "Mexico vs South Africa"
    return value.strip()


def match_teams(calendar_match: str, official_match: str) -> bool:
    """Return whether two descriptions contain the same two teams."""
    calendar_parts = [normalize_team(team) for team in calendar_match.lower().split(" vs ")]
    official_parts = [normalize_team(team) for team in official_match.lower().split(" vs ")]
    return len(calendar_parts) == 2 and len(official_parts) == 2 and set(calendar_parts) == set(official_parts)


def load_json_file(filename: str | Path, *, label: str, max_bytes: int) -> Any:
    """Load bounded UTF-8 JSON from a regular, non-symlink file."""
    path = Path(filename)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise ValidationError(f"{label} cannot be accessed: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise ValidationError(f"{label} must not be a symbolic link: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise ValidationError(f"{label} must be a regular file: {path}")
    if metadata.st_size > max_bytes:
        raise ValidationError(f"{label} exceeds the {max_bytes}-byte limit: {metadata.st_size} bytes")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"{label} is not readable UTF-8 text: {exc}") from exc
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def validate_schedule(value: Any) -> dict[str, str]:
    """Validate the official match-to-ISO-time mapping."""
    if not isinstance(value, dict):
        raise ValidationError("official schedule JSON must be an object")
    if len(value) > MAX_SCHEDULE_ENTRIES:
        raise ValidationError(f"official schedule exceeds {MAX_SCHEDULE_ENTRIES} entries")
    schedule: dict[str, str] = {}
    for match_name, start_time in value.items():
        if not isinstance(match_name, str) or not match_name.strip():
            raise ValidationError("every official schedule key must be a non-empty string")
        if not isinstance(start_time, str) or not start_time.strip():
            raise ValidationError(f"official time for {match_name!r} must be a non-empty ISO-8601 string")
        try:
            datetime.fromisoformat(start_time)
        except ValueError as exc:
            raise ValidationError(f"official time for {match_name!r} is not ISO-8601: {start_time!r}") from exc
        schedule[match_name] = start_time
    return schedule


def validate_events(value: Any) -> list[dict[str, Any]]:
    """Validate the event-export shape needed by the planner."""
    if not isinstance(value, list):
        raise ValidationError("events JSON must be an array")
    if len(value) > MAX_EVENTS:
        raise ValidationError(f"events JSON exceeds {MAX_EVENTS} records")

    events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw_event in enumerate(value):
        location = f"events[{index}]"
        if not isinstance(raw_event, dict):
            raise ValidationError(f"{location} must be an object")
        event_id = raw_event.get("id")
        summary = raw_event.get("summary")
        description = raw_event.get("description", "")
        start = raw_event.get("start", {})
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValidationError(f"{location}.id must be a non-empty string")
        if event_id in seen_ids:
            raise ValidationError(f"duplicate event id: {event_id!r}")
        seen_ids.add(event_id)
        if not isinstance(summary, str):
            raise ValidationError(f"{location}.summary must be a string")
        if not isinstance(description, str):
            raise ValidationError(f"{location}.description must be a string when present")
        if not isinstance(start, dict):
            raise ValidationError(f"{location}.start must be an object when present")
        for field in ("dateTime", "date"):
            if field in start and not isinstance(start[field], str):
                raise ValidationError(f"{location}.start.{field} must be a string")
        events.append(raw_event)
    return events


def validate_calendar(
    events_file: str | Path,
    official_schedule_dict: dict[str, str],
    target_timezone: str,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> dict[str, list[dict[str, Any]]]:
    """Validate event evidence and return proposed updates and deletions only."""
    try:
        ZoneInfo(target_timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValidationError(f"unknown IANA timezone: {target_timezone!r}") from exc

    events = validate_events(load_json_file(events_file, label="events file", max_bytes=max_bytes))
    official_schedule = validate_schedule(official_schedule_dict)
    event_matches: list[tuple[int, str | None, str]] = []

    for index, event in enumerate(events):
        summary = event["summary"]
        if "Group Stage" in summary or "match schedule" in summary:
            event_matches.append((index, None, "generic"))
            continue

        match_name = normalize_match_name(summary)
        found_key = next(
            (official_match for official_match in official_schedule if match_teams(match_name, official_match)),
            None,
        )
        if found_key is None:
            event_matches.append((index, None, "not_found"))
            continue

        start = event.get("start", {})
        start_time = start.get("dateTime", start.get("date", ""))
        status = "correct" if start_time.startswith(official_schedule[found_key]) else "incorrect"
        event_matches.append((index, found_key, status))

    match_to_events: defaultdict[str, list[int]] = defaultdict(list)
    for event_index, match_key, _status in event_matches:
        if match_key:
            match_to_events[match_key].append(event_index)

    duplicates_to_delete: list[int] = []
    events_to_keep: dict[str, int] = {}
    status_by_event = {event_index: status for event_index, _key, status in event_matches}
    for match_key, event_indices in match_to_events.items():
        if len(event_indices) == 1:
            events_to_keep[match_key] = event_indices[0]
            continue
        correct = [event_index for event_index in event_indices if status_by_event[event_index] == "correct"]
        keep = correct[0] if correct else max(event_indices, key=lambda item: len(events[item].get("description", "")))
        events_to_keep[match_key] = keep
        duplicates_to_delete.extend(item for item in event_indices if item != keep)

    generic_to_delete = [event_index for event_index, _key, status in event_matches if status == "generic"]
    all_to_delete = set(duplicates_to_delete + generic_to_delete)
    deletes = [
        {"eventId": events[index]["id"], "summary": events[index]["summary"]}
        for index in sorted(all_to_delete)
    ]

    updates: list[dict[str, Any]] = []
    for event_index, match_key, status in event_matches:
        if (
            status != "incorrect"
            or match_key is None
            or event_index in all_to_delete
            or event_index != events_to_keep.get(match_key)
        ):
            continue
        correct_start = official_schedule[match_key]
        start_datetime = datetime.fromisoformat(correct_start)
        updates.append(
            {
                "eventId": events[event_index]["id"],
                "summary": events[event_index]["summary"],
                "start": {"dateTime": correct_start, "timeZone": target_timezone},
                "end": {
                    "dateTime": (start_datetime + timedelta(hours=2)).isoformat(),
                    "timeZone": target_timezone,
                },
            }
        )
    return {"updates": updates, "deletes": deletes}


def write_json_atomic(filename: str | Path, value: Any, *, force: bool) -> None:
    """Write owner-readable JSON atomically and refuse silent overwrite."""
    destination = Path(filename)
    if destination.exists() or destination.is_symlink():
        if not force:
            raise ValidationError(f"output already exists; use --force to replace it: {destination}")
        metadata = destination.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValidationError("output replacement is allowed only for a regular, non-symlink file")
    parent = destination.parent.resolve()
    if not parent.is_dir():
        raise ValidationError(f"output parent is not a directory: {parent}")

    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate local Google Calendar event evidence and write a review-only action plan."
    )
    parser.add_argument("events_file", help="Path to an exported events JSON array")
    parser.add_argument("schedule_file", help="Path to an official match-to-ISO-time JSON object")
    parser.add_argument("target_timezone", help="IANA timezone, for example America/Sao_Paulo")
    parser.add_argument("--output", default="action_plan.json", help="New action-plan JSON path")
    parser.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--force", action="store_true", help="Replace an existing regular output file")
    args = parser.parse_args()
    if args.max_input_bytes <= 0:
        parser.error("--max-input-bytes must be positive")
    return args


def main() -> int:
    args = parse_args()
    try:
        official_schedule = validate_schedule(
            load_json_file(args.schedule_file, label="schedule file", max_bytes=args.max_input_bytes)
        )
        plan = validate_calendar(
            args.events_file,
            official_schedule,
            args.target_timezone,
            max_bytes=args.max_input_bytes,
        )
        write_json_atomic(args.output, plan, force=args.force)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Error: output operation failed: {exc}", file=sys.stderr)
        return 2
    print(f"Read-only action plan written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
