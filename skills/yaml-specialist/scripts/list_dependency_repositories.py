#!/usr/bin/env python3
"""Classify Helm dependency repository forms without adding repositories or using network access."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urlsplit, urlunsplit

import yaml_common as common


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", required=True, type=Path, help="Chart directory or Chart.yaml")
    parser.add_argument("--format", choices=("json", "tsv"), default="json")
    parser.add_argument("--max-bytes", type=int, default=common.DEFAULT_MAX_BYTES)
    return parser.parse_args(argv)


def redact_url(value: str) -> tuple[str, bool]:
    parsed = urlsplit(value)
    has_credentials = parsed.username is not None or parsed.password is not None
    if not has_credentials:
        return value, False
    host = parsed.hostname or ""
    if parsed.port:
        host += f":{parsed.port}"
    return urlunsplit((parsed.scheme, host, parsed.path, parsed.query, parsed.fragment)), True


def classify(repository: str, chart_dir: Path) -> tuple[str, str, str, bool]:
    """Return kind, normalized value, disposition, and hard-error flag."""
    if not repository:
        return "vendored-or-unresolved", "", "verify dependency exists in charts/ or is supplied by the build", False
    if repository.startswith("@"):
        return "helm-repository-alias", repository, "resolve from an explicit, reviewed Helm repository configuration", False
    if repository.startswith("alias:"):
        return "helm-repository-alias", repository, "resolve from an explicit, reviewed Helm repository configuration", False
    if repository.startswith("file://"):
        raw_path = unquote(repository[len("file://") :])
        candidate = (chart_dir / raw_path).resolve()
        try:
            candidate.relative_to(chart_dir.parent.resolve())
            disposition = "review local dependency path and package contents"
            hard_error = False
        except ValueError:
            disposition = "local dependency path escapes the chart parent; require explicit approval"
            hard_error = True
        return "local-file", repository, disposition, hard_error
    parsed = urlsplit(repository)
    normalized, credentials = redact_url(repository)
    if credentials:
        return "credential-bearing-url", normalized, "remove inline credentials and use approved credential storage", True
    if parsed.scheme == "https":
        return "https-index", normalized, "verify host trust, TLS, version pin, and Chart.lock before download", False
    if parsed.scheme == "http":
        return "plaintext-index", normalized, "replace plaintext transport with HTTPS or a reviewed internal mirror", True
    if parsed.scheme == "oci":
        return "oci-registry", normalized, "authenticate separately; verify registry trust, version, and provenance", False
    return "unsupported", normalized, f"unsupported repository scheme {parsed.scheme!r}", True


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        candidate = args.chart.expanduser()
        if candidate.is_dir():
            candidate = candidate / "Chart.yaml"
        resolved, _, data = common.load_mapping(candidate, max_bytes=args.max_bytes)
        dependencies = data.get("dependencies") or []
        if not isinstance(dependencies, list):
            raise common.InputError("Chart.yaml dependencies must be a sequence")
        rows: list[dict[str, Any]] = []
        errors = 0
        unresolved = 0
        for index, dependency in enumerate(dependencies):
            if not isinstance(dependency, Mapping):
                rows.append(
                    {
                        "index": index,
                        "name": "",
                        "version": "",
                        "kind": "invalid",
                        "repository": "",
                        "disposition": "dependency entry must be a mapping",
                        "error": True,
                    }
                )
                errors += 1
                continue
            repository = str(dependency.get("repository") or "")
            kind, normalized, disposition, hard_error = classify(repository, resolved.parent)
            unresolved += int(kind in {"helm-repository-alias", "vendored-or-unresolved", "local-file"})
            errors += int(hard_error)
            rows.append(
                {
                    "index": index,
                    "name": str(dependency.get("name") or ""),
                    "version": str(dependency.get("version") or ""),
                    "kind": kind,
                    "repository": normalized,
                    "disposition": disposition,
                    "error": hard_error,
                }
            )
        status = "failed" if errors else ("incomplete" if unresolved else "complete")
        result = {
            "status": status,
            "chart": str(resolved),
            "dependency_count": len(rows),
            "errors": errors,
            "unresolved_or_local_count": unresolved,
            "network_performed": False,
            "dependencies": rows,
        }
    except (OSError, common.InputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(common.stable_json(result), end="")
    else:
        print("index\tname\tversion\tkind\trepository\terror\tdisposition")
        for row in rows:
            fields = [
                row["index"], row["name"], row["version"], row["kind"], row["repository"],
                str(row["error"]).lower(), row["disposition"],
            ]
            print("\t".join(str(value).replace("\t", " ").replace("\n", " ") for value in fields))
    return 1 if status == "failed" else (2 if status == "incomplete" else 0)


if __name__ == "__main__":
    sys.exit(main())
