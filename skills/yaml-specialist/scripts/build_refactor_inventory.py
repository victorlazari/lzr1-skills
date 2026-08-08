#!/usr/bin/env python3
"""Build a secret-safe, reviewable before-state inventory for Helm values refactoring."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import scan_template_values as scanner
import values_contract_lint as contract
import yaml_common as common


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", required=True, type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--include-nonsecret-scalars", action="store_true",
                        help="Include non-secret scalar defaults; secrets remain redacted")
    parser.add_argument("--max-bytes", type=int, default=common.DEFAULT_MAX_BYTES)
    return parser.parse_args(argv)


def display_default(path: str, value: Any, include_scalars: bool) -> Any:
    if common.is_secret_path(path):
        return "<redacted-secret-value>" if common.is_concrete_secret(value) else "<empty-or-placeholder>"
    if isinstance(value, dict):
        return "{}" if not value else f"<object:{len(value)} keys>"
    if isinstance(value, list):
        return "[]" if not value else f"<array:{len(value)} items>"
    if include_scalars:
        return value
    return f"<{common.yaml_kind(value)} default omitted>"


def related(path: str, candidates: set[str]) -> bool:
    return any(
        candidate == path
        or candidate.startswith(path + ".")
        or candidate.startswith(path + "[")
        or path.startswith(candidate + ".")
        or path.startswith(candidate + "[")
        for candidate in candidates
    )


def escape_markdown(value: Any) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|").replace("\n", "<br>")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        chart = args.chart.expanduser().resolve(strict=True)
        if not chart.is_dir():
            raise common.InputError(f"chart is not a directory: {chart}")
        values_path = common.confine_existing_path(chart, chart / "values.yaml", kind="values")
        _, values_text, values_data = common.load_mapping(values_path, max_bytes=args.max_bytes)
        parameters = contract.flatten_parameters(values_data, values_text.splitlines())
        registry = {parameter.path: parameter for parameter in parameters}

        template_path = chart / "values-template.yaml"
        active_template: list[contract.Parameter] = []
        commented_template: list[tuple[str, int, Any]] = []
        template_mode: str | None = None
        coverage: list[str] = []
        if template_path.exists():
            safe_template = common.confine_existing_path(chart, template_path, kind="values template")
            _, active_template, lines, template_mode = contract.active_template_parameters(
                safe_template, max_bytes=args.max_bytes
            )
            commented_template = contract.commented_template_paths(lines, registry)
            if template_mode == "commented-skeleton" or commented_template:
                coverage.append("commented-template inventory covers simple mapping syntax only")
        else:
            coverage.append("values-template.yaml is absent")

        active_paths = {item.path for item in active_template}
        commented_paths = {path for path, _, _ in commented_template}
        static_uses: list[scanner.Use] = []
        dynamic_uses: list[scanner.Use] = []
        for template in scanner.template_files(chart, max_files=10_000):
            static, dynamic = scanner.scan_file(template, max_bytes=args.max_bytes)
            static_uses.extend(static)
            dynamic_uses.extend(dynamic)
        static_uses = scanner.dedupe_uses(static_uses)
        dynamic_uses = scanner.dedupe_uses(dynamic_uses)
        consumed = {item.path for item in static_uses if item.path}
        if dynamic_uses:
            coverage.append("dynamic values expressions require rendered or manual consumer analysis")

        rows: list[dict[str, Any]] = []
        complete_docs = 0
        for parameter in parameters:
            missing_tags = [tag for tag in contract.REQUIRED_TAGS if tag not in parameter.tags]
            description_ok = any(
                line.lstrip().startswith(f"# -- {parameter.path}") for line in parameter.comments
            )
            documentation_complete = description_ok and not missing_tags
            complete_docs += int(documentation_complete)
            operator_presence = ""
            if related(parameter.path, active_paths):
                operator_presence = "active"
            if related(parameter.path, commented_paths):
                operator_presence = f"{operator_presence}+commented" if operator_presence else "commented"
            used = related(parameter.path, consumed)
            suggested = "retain-or-modernize"
            if not used and not operator_presence:
                suggested = "prove-reserved-or-remove"
            if common.is_secret_path(parameter.path) and common.is_concrete_secret(parameter.value):
                suggested = "externalize-before-refactor"
            rows.append(
                {
                    "current_path": parameter.path,
                    "current_type": common.yaml_kind(parameter.value),
                    "safe_default": display_default(
                        parameter.path, parameter.value, args.include_nonsecret_scalars
                    ),
                    "documentation_complete": documentation_complete,
                    "missing_metadata": missing_tags,
                    "template_consumed": used,
                    "operator_presence": operator_presence,
                    "suggested_review": suggested,
                    "disposition": "TODO: retain|rename|deprecate|remove|externalize",
                    "target_path": "TODO",
                    "target_type": "TODO",
                    "compatibility": "TODO: additive|alias-window|breaking",
                    "migration_evidence": "TODO",
                }
            )

        canonical_paths = set(registry)
        for path in sorted(active_paths | commented_paths):
            if path in canonical_paths or contract.find_open_ancestor(path, registry):
                continue
            rows.append(
                {
                    "current_path": path,
                    "current_type": "template-only",
                    "safe_default": "<omitted>",
                    "documentation_complete": False,
                    "missing_metadata": list(contract.REQUIRED_TAGS),
                    "template_consumed": related(path, consumed),
                    "operator_presence": "template-only",
                    "suggested_review": "promote-or-remove-with-proof",
                    "disposition": "TODO: retain|rename|deprecate|remove",
                    "target_path": "TODO",
                    "target_type": "TODO",
                    "compatibility": "TODO: additive|alias-window|breaking",
                    "migration_evidence": "TODO",
                }
            )

        chart_yaml = contract.load_yaml(chart / "Chart.yaml", max_bytes=args.max_bytes)
        result = {
            "status": "incomplete" if coverage else "complete",
            "chart": str(chart),
            "chart_name": chart_yaml.get("name", chart.name) if isinstance(chart_yaml, dict) else chart.name,
            "template_mode": template_mode,
            "canonical_path_count": len(parameters),
            "documentation_complete_count": complete_docs,
            "template_only_path_count": sum(row["current_type"] == "template-only" for row in rows),
            "static_values_use_count": len(static_uses),
            "dynamic_values_review_count": len(dynamic_uses),
            "coverage_gaps": sorted(set(coverage)),
            "dynamic_values_review": [asdict(item) for item in dynamic_uses],
            "rows": rows,
        }

        if args.format == "json":
            output = common.stable_json(result)
        else:
            output_lines = [
                f"# Values Refactor Inventory — {result['chart_name']}",
                "",
                f"**Chart path:** `{chart}`  ",
                f"**Operator-template mode:** `{template_mode or 'missing-or-undeclared'}`  ",
                f"**Canonical paths:** {len(parameters)}  ",
                f"**Fully documented paths:** {complete_docs}  ",
                f"**Template-only paths:** {result['template_only_path_count']}  ",
                f"**Dynamic expressions requiring review:** {len(dynamic_uses)}",
                "",
                "## Coverage Gaps",
                "",
            ]
            output_lines.extend([f"- {gap}" for gap in result["coverage_gaps"]] or ["- None detected by the bounded static inventory."])
            output_lines.extend(
                [
                    "",
                    "## Path Disposition Register",
                    "",
                    "| Current path | Current type | Safe default | Docs complete | Consumed | Operator presence | Suggested review | Disposition | Target path | Target type | Compatibility | Migration evidence |",
                    "|---|---|---|---:|---:|---|---|---|---|---|---|---|",
                ]
            )
            keys = (
                "current_path", "current_type", "safe_default", "documentation_complete",
                "template_consumed", "operator_presence", "suggested_review", "disposition",
                "target_path", "target_type", "compatibility", "migration_evidence",
            )
            for row in rows:
                output_lines.append("| " + " | ".join(escape_markdown(row[key]) for key in keys) + " |")
            if dynamic_uses:
                output_lines.extend(["", "## Dynamic Expressions", "", "| File | Line | Redacted expression |", "|---|---:|---|"])
                for item in dynamic_uses:
                    output_lines.append(
                        f"| {escape_markdown(item.file)} | {item.line} | `{escape_markdown(item.expression)}` |"
                    )
            output = "\n".join(output_lines) + "\n"

        if args.output:
            target = args.output.expanduser().resolve()
            if target.exists() and not args.overwrite:
                raise common.InputError(f"output exists; pass --overwrite to replace it: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
        return 2 if result["status"] == "incomplete" else 0
    except (OSError, common.InputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
