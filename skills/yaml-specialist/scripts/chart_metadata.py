#!/usr/bin/env python3
"""Read portable Helm Chart.yaml metadata without evaluating templates or plugins."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

import yaml_common as common

SEMVER_LIKE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", required=True, type=Path, help="Chart directory or Chart.yaml")
    parser.add_argument(
        "--field",
        choices=("name", "apiVersion", "type", "version", "appVersion", "kubeVersion", "dependency-count"),
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument("--max-bytes", type=int, default=common.DEFAULT_MAX_BYTES)
    return parser.parse_args(argv)


def sanitize_repository(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    if value.startswith(("@", "alias:", "file://", "oci://")):
        return value
    parsed = urlsplit(value)
    if parsed.username is not None or parsed.password is not None:
        host = parsed.hostname or ""
        if parsed.port:
            host += f":{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path, parsed.query, parsed.fragment))
    return value


def normalize(data: Mapping[str, Any], path: Path) -> tuple[dict[str, Any], list[str]]:
    findings: list[str] = []
    chart_type = str(data.get("type") or "application")
    if chart_type not in {"application", "library"}:
        findings.append(f"unsupported chart type: {chart_type!r}")
    api_version = str(data.get("apiVersion") or "")
    if api_version != "v2":
        findings.append("Helm 3/4 charts should declare apiVersion: v2")
    version = str(data.get("version") or "")
    if version and not SEMVER_LIKE.fullmatch(version):
        findings.append("chart version is not a simple SemVer string; verify with Helm")
    dependencies: list[dict[str, str]] = []
    raw_dependencies = data.get("dependencies") or []
    if not isinstance(raw_dependencies, list):
        findings.append("dependencies must be a sequence")
        raw_dependencies = []
    for index, dependency in enumerate(raw_dependencies):
        if not isinstance(dependency, Mapping):
            findings.append(f"dependency {index} is not a mapping")
            continue
        dependencies.append(
            {
                "name": str(dependency.get("name") or ""),
                "version": str(dependency.get("version") or ""),
                "repository": sanitize_repository(dependency.get("repository")),
                "alias": str(dependency.get("alias") or ""),
                "condition": str(dependency.get("condition") or ""),
            }
        )
    result = {
        "source": str(path),
        "name": str(data.get("name") or ""),
        "apiVersion": api_version,
        "type": chart_type,
        "version": version,
        "appVersion": str(data.get("appVersion") or ""),
        "kubeVersion": str(data.get("kubeVersion") or ""),
        "dependency-count": len(dependencies),
        "dependencies": dependencies,
        "findings": findings,
    }
    return result, findings


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        candidate = args.chart.expanduser()
        if candidate.is_dir():
            candidate = candidate / "Chart.yaml"
        resolved, _, data = common.load_mapping(candidate, max_bytes=args.max_bytes)
        result, findings = normalize(data, resolved)
    except (OSError, common.InputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.field:
        value = result[args.field]
        print(value)
    elif args.format == "json":
        print(common.stable_json(result), end="")
    else:
        for key in ("name", "apiVersion", "type", "version", "appVersion", "kubeVersion", "dependency-count"):
            print(f"{key}\t{result[key]}")
        for finding in findings:
            print(f"WARNING\t{finding}", file=sys.stderr)
    return 2 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
