#!/usr/bin/env python3
"""Validate the minimum portable structure of a Spanish curriculum JSON file."""

from __future__ import annotations

import argparse
import json
import stat
import sys
from pathlib import Path
from typing import Any

DEFAULT_MAX_BYTES = 5 * 1024 * 1024


class CurriculumError(ValueError):
    """Expected curriculum input failure."""


def load_json_object(file_path: str | Path, max_bytes: int) -> dict[str, Any]:
    path = Path(file_path)
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise CurriculumError(f"cannot access input file: {exc}") from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise CurriculumError("input file must not be a symbolic link")
    if not stat.S_ISREG(metadata.st_mode):
        raise CurriculumError("input must be a regular file")
    if metadata.st_size > max_bytes:
        raise CurriculumError(f"input exceeds the {max_bytes}-byte limit")
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CurriculumError(f"input is not readable UTF-8 text: {exc}") from exc
    try:
        value = json.loads(content)
    except json.JSONDecodeError as exc:
        raise CurriculumError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise CurriculumError("curriculum JSON must be a top-level object")
    return value


def validate_curriculum(file_path: str | Path, level: str, *, max_bytes: int) -> None:
    if not isinstance(level, str) or not level.strip():
        raise CurriculumError("target level must be a non-empty string")

    data = load_json_object(file_path, max_bytes)
    declared_level = data.get("level")
    if not isinstance(declared_level, str):
        raise CurriculumError("curriculum level must be a string")
    if declared_level != level:
        raise CurriculumError(
            f"curriculum level {declared_level!r} does not match requested level {level!r}"
        )

    grammar_nodes = data.get("grammar_nodes")
    if not isinstance(grammar_nodes, (list, dict)) or not grammar_nodes:
        raise CurriculumError("grammar_nodes must be a non-empty array or object")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a generated curriculum plan.")
    parser.add_argument("file_path", help="Path to a curriculum JSON object")
    parser.add_argument("level", help="Expected CEFR or ACTFL level")
    parser.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_BYTES)
    args = parser.parse_args()
    if args.max_input_bytes <= 0:
        parser.error("--max-input-bytes must be positive")
    return args


def main() -> int:
    args = parse_args()
    try:
        validate_curriculum(args.file_path, args.level, max_bytes=args.max_input_bytes)
    except CurriculumError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Validation passed for level {args.level}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
