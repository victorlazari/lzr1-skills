#!/usr/bin/env python3
"""Discover statically addressable Helm .Values paths and expose dynamic gaps."""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

import values_contract_lint as contract
import yaml_common as common

DOT_VALUES_RE = re.compile(r"\.Values((?:\.[A-Za-z_][A-Za-z0-9_-]*)+)")
INDEX_VALUES_RE = re.compile(
    r"\bindex\s+\.?Values((?:\.[A-Za-z_][A-Za-z0-9_-]*)*)"
    r"((?:\s+(?:\"(?:\\.|[^\"])*\"|`[^`]*`))+)")
INDEX_ARG_RE = re.compile(r'\"((?:\\.|[^\"])*)\"|`([^`]*)`')
DYNAMIC_RE = re.compile(
    r"(?:\b(?:index|dig|get|pluck|hasKey)\s+\.?Values\b|\btpl\b|"
    r"\.?Values\s*\[|\$[A-Za-z_][A-Za-z0-9_]*\s*:?=\s*\.?Values\b)"
)
TEMPLATE_COMMENT_RE = re.compile(r"\{\{-?\s*/\*.*?\*/\s*-?\}\}", re.DOTALL)
QUOTED_LITERAL_RE = re.compile(r'\"(?:\\.|[^\"])*\"|`[^`]*`')


@dataclass(frozen=True)
class Use:
    path: str
    file: str
    line: int
    expression: str
    kind: str


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    file: str
    line: int
    message: str
    category: str = "coverage"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", required=True, type=Path)
    parser.add_argument("--values", type=Path, help="Canonical values file inside the chart")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--max-bytes-per-file", type=int, default=common.DEFAULT_MAX_BYTES)
    parser.add_argument("--max-files", type=int, default=10_000)
    parser.add_argument("--max-uses", type=int, default=200_000)
    return parser.parse_args(argv)


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def clean_template_text(text: str) -> str:
    def preserve_lines(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    return TEMPLATE_COMMENT_RE.sub(preserve_lines, text)


def decode_index_arguments(raw: str) -> list[str]:
    values: list[str] = []
    for match in INDEX_ARG_RE.finditer(raw):
        if match.group(1) is not None:
            try:
                values.append(json.loads('"' + match.group(1) + '"'))
            except json.JSONDecodeError:
                values.append(match.group(1))
        else:
            values.append(match.group(2))
    return values


def build_path(parts: list[str]) -> str:
    path = ""
    for part in parts:
        path = contract.join_path(path, part)
    return path


def redact_expression(expression: str) -> str:
    collapsed = " ".join(expression.split())[:400]
    return QUOTED_LITERAL_RE.sub('"<literal>"', collapsed)


def scan_file(path: Path, *, max_bytes: int) -> tuple[list[Use], list[Use]]:
    resolved, raw = common.read_text(path, max_bytes=max_bytes)
    text = clean_template_text(raw)
    static: list[Use] = []
    dynamic: list[Use] = []
    occupied: list[tuple[int, int]] = []

    for match in INDEX_VALUES_RE.finditer(text):
        base = [part for part in match.group(1).split(".") if part]
        indexed = decode_index_arguments(match.group(2))
        static.append(
            Use(
                build_path(base + indexed),
                str(resolved),
                line_for_offset(text, match.start()),
                "index .Values <literal-key>...",
                "index",
            )
        )
        occupied.append(match.span())

    def occupied_offset(offset: int) -> bool:
        return any(left <= offset < right for left, right in occupied)

    for match in DOT_VALUES_RE.finditer(text):
        if occupied_offset(match.start()):
            continue
        parts = [part for part in match.group(1).split(".") if part]
        static.append(
            Use(
                build_path(parts),
                str(resolved),
                line_for_offset(text, match.start()),
                match.group(0),
                "dot",
            )
        )

    for match in DYNAMIC_RE.finditer(text):
        end = text.find("}}", match.start())
        expression = text[match.start() : end + 2] if end >= 0 else text[match.start() : match.start() + 400]
        if INDEX_VALUES_RE.search(expression):
            continue
        dynamic.append(
            Use(
                "",
                str(resolved),
                line_for_offset(text, match.start()),
                redact_expression(expression),
                "dynamic-review",
            )
        )
    return static, dynamic


def template_files(chart: Path, *, max_files: int) -> list[Path]:
    templates = chart / "templates"
    if not templates.exists():
        return []
    if templates.is_symlink() or not templates.is_dir():
        raise common.InputError("templates must be a real directory, not a symbolic link")
    files: list[Path] = []
    for path in sorted(templates.rglob("*")):
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise common.InputError(f"symbolic links are not scanned: {path}")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml", ".tpl", ".txt"}:
            common.confine_existing_path(chart, path, kind="template")
            files.append(path)
            if len(files) > max_files:
                raise common.InputError(f"template file count exceeds {max_files}")
    return files


def path_is_declared(path: str, registry: Mapping[str, str], open_paths: set[str]) -> bool:
    if path in registry:
        return True
    return any(path.startswith(candidate + ".") or path.startswith(candidate + "[") for candidate in open_paths)


def dedupe_uses(uses: list[Use]) -> list[Use]:
    seen: set[tuple[str, str, int, str]] = set()
    result: list[Use] = []
    for use in sorted(uses, key=lambda item: (item.file, item.line, item.kind, item.path)):
        identity = (use.path, use.file, use.line, use.kind)
        if identity not in seen:
            seen.add(identity)
            result.append(use)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings: list[Finding] = []
    static: list[Use] = []
    dynamic: list[Use] = []
    registry: dict[str, str] = {}
    chart_text = str(args.chart)
    values_text = str(args.values or "values.yaml")
    scanned_files = 0
    fatal = False

    try:
        chart = args.chart.expanduser().resolve(strict=True)
        if not chart.is_dir():
            raise common.InputError(f"chart is not a directory: {chart}")
        chart_text = str(chart)
        values_path = common.confine_existing_path(chart, args.values or chart / "values.yaml", kind="values")
        values_text = str(values_path)
        _, raw_values, canonical = common.load_mapping(values_path, max_bytes=args.max_bytes_per_file)
        parameters = contract.flatten_parameters(canonical, raw_values.splitlines())
        registry = {parameter.path: common.yaml_kind(parameter.value) for parameter in parameters}
        open_paths = {parameter.path for parameter in parameters if contract.is_open_object(parameter)}
        chart_path = common.confine_existing_path(chart, chart / "Chart.yaml", kind="Chart.yaml")
        chart_data = contract.load_yaml(chart_path, max_bytes=args.max_bytes_per_file)
        is_library = isinstance(chart_data, Mapping) and chart_data.get("type") == "library"

        files = template_files(chart, max_files=args.max_files)
        scanned_files = len(files)
        for path in files:
            file_static, file_dynamic = scan_file(path, max_bytes=args.max_bytes_per_file)
            static.extend(file_static)
            dynamic.extend(file_dynamic)
            if len(static) + len(dynamic) > args.max_uses:
                raise common.InputError(f"discovered use count exceeds {args.max_uses}")
        static = dedupe_uses(static)
        dynamic = dedupe_uses(dynamic)

        for use in static:
            if not path_is_declared(use.path, registry, open_paths):
                findings.append(
                    Finding(
                        "warning" if is_library else "error",
                        "undeclared-library-input" if is_library else "undeclared-values-path",
                        use.path,
                        use.file,
                        use.line,
                        (
                            "library helper consumes a caller-provided path; document and test the consumer contract"
                            if is_library
                            else "template consumes a path absent from canonical values and documented open maps"
                        ),
                        "contract",
                    )
                )
        for use in dynamic:
            findings.append(
                Finding(
                    "warning",
                    "dynamic-values-review",
                    "",
                    use.file,
                    use.line,
                    f"static scanner cannot resolve expression: {use.expression}",
                    "coverage",
                )
            )
    except (OSError, common.InputError) as exc:
        fatal = True
        findings.append(Finding("error", "analysis-failure", "", chart_text, 0, str(exc), "tool"))

    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    incomplete_reasons: list[str] = []
    if dynamic:
        incomplete_reasons.append("dynamic .Values expressions require manual or rendered-scenario review")
    if any(item.code == "undeclared-library-input" for item in findings):
        incomplete_reasons.append("library-chart caller inputs require consumer-chart evidence")
    incomplete_reasons.append("scanner is lexical, not a Go template evaluator; include/define dataflow and unreachable branches are not proven")
    status = "failed" if errors or (args.warnings_as_errors and warnings) else ("incomplete" if dynamic or any(item.code == "undeclared-library-input" for item in findings) else "complete")
    result = {
        "status": status,
        "chart": chart_text,
        "values": values_text,
        "scanned_template_files": scanned_files,
        "declared_path_count": len(registry),
        "static_use_count": len(static),
        "dynamic_review_count": len(dynamic),
        "errors": errors,
        "warnings": warnings,
        "coverage_gaps": sorted(set(incomplete_reasons)),
        "uses": [asdict(item) for item in static],
        "dynamic_uses": [asdict(item) for item in dynamic],
        "findings": [asdict(item) for item in findings],
    }

    if args.format == "json":
        print(common.stable_json(result), end="")
    else:
        for item in findings:
            suffix = f" [{item.path}]" if item.path else ""
            line = f":{item.line}" if item.line else ""
            print(f"{item.severity.upper():7} {item.code}: {item.file}{line}{suffix}: {item.message}")
        for gap in result["coverage_gaps"]:
            print(f"COVERAGE {gap}")
        print(f"Found {len(static)} static use(s), {len(dynamic)} dynamic review item(s), and {errors} error(s).")

    if fatal or status == "failed":
        return 1
    if status == "incomplete":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
