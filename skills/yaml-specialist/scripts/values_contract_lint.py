#!/usr/bin/env python3
"""Audit a Helm values contract without modifying files or resolving network references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml_common as common

try:
    import jsonschema
    from jsonschema import validators
except ImportError:  # handled as an incomplete check at runtime
    jsonschema = None  # type: ignore[assignment]
    validators = None  # type: ignore[assignment]

REQUIRED_TAGS = ("type", "required", "accepted", "default", "example", "security")
TAG_RE = re.compile(r"^\s*#\s*@([A-Za-z][A-Za-z0-9_-]*)\s+(.+?)\s*$")
MODE_RE = re.compile(r"^\s*#\s*@mode\s+(active-overlay|commented-skeleton)\s*$")
COMMENTED_KEY_RE = re.compile(r"^(\s*)([A-Za-z0-9_.-]+):(?:\s*(.*))?$")
SIMPLE_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
AMBIGUOUS_SCALAR_RE = re.compile(
    r"^\s*[^#\n][^:\n]*:\s*(?:yes|no|on|off|y|n|[-+]?0[0-9]+)\s*(?:#.*)?$",
    re.IGNORECASE,
)
CREDENTIAL_URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://[^/@:\s]+:[^/@\s]+@")


@dataclass
class Parameter:
    path: str
    value: Any
    line: int
    comments: list[str]
    tags: dict[str, str]


class ContractError(common.InputError):
    """Raised when complete contract analysis is impossible."""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", required=True, type=Path, help="Helm chart directory")
    parser.add_argument("--values", type=Path, help="Canonical values file; must remain inside the chart")
    parser.add_argument("--values-template", type=Path, help="Operator template; must remain inside the chart")
    parser.add_argument("--schema", type=Path, help="JSON Schema file; must remain inside the chart")
    parser.add_argument("--schema-dialect", help="Explicit $schema URI only when the schema omits one")
    parser.add_argument("--skip-template", action="store_true", help="Skip values-template.yaml reconciliation")
    parser.add_argument("--skip-schema", action="store_true", help="Skip values.schema.json validation")
    parser.add_argument("--warnings-as-errors", action="store_true")
    parser.add_argument("--max-bytes", type=int, default=common.DEFAULT_MAX_BYTES)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def join_path(parent: str, key: Any) -> str:
    text = str(key)
    if SIMPLE_KEY_RE.fullmatch(text):
        return f"{parent}.{text}" if parent else text
    bracket = f"[{json.dumps(text, ensure_ascii=False)}]"
    return f"{parent}{bracket}" if parent else bracket


def comments_above(lines: list[str], line_index: int) -> list[str]:
    comments: list[str] = []
    cursor = line_index - 1
    while cursor >= 0:
        raw = lines[cursor]
        if raw.lstrip().startswith("#"):
            comments.append(raw)
            cursor -= 1
            continue
        if not raw.strip() and comments:
            break
        break
    comments.reverse()
    return comments


def extract_tags(comments: Iterable[str]) -> dict[str, str]:
    tags: dict[str, str] = {}
    for comment in comments:
        match = TAG_RE.match(comment)
        if match:
            tags[match.group(1).lower()] = match.group(2).strip()
    return tags


def flatten_parameters(node: Any, lines: list[str], parent: str = "") -> list[Parameter]:
    parameters: list[Parameter] = []
    if not isinstance(node, Mapping):
        return parameters
    for key, value in node.items():
        path = join_path(parent, key)
        try:
            line_index = int(node.lc.key(key)[0])  # type: ignore[attr-defined]
        except Exception:
            line_index = 0
        comments = comments_above(lines, line_index)
        parameters.append(Parameter(path, value, line_index + 1, comments, extract_tags(comments)))
        if isinstance(value, Mapping):
            parameters.extend(flatten_parameters(value, lines, path))
    return parameters


def load_yaml(path: Path, *, max_bytes: int = common.DEFAULT_MAX_BYTES) -> Any:
    _, _, mapping = common.load_mapping(path, max_bytes=max_bytes)
    return mapping


def accepted_types(text: str) -> set[str]:
    pieces = re.split(r"[|,/]+", text.lower().replace(" ", ""))
    allowed = {
        piece
        for piece in pieces
        if piece in {"string", "boolean", "integer", "number", "object", "array", "null"}
    }
    if "number" in allowed:
        allowed.add("integer")
    return allowed


def is_open_object(parameter: Parameter) -> bool:
    if common.yaml_kind(parameter.value) != "object":
        return False
    accepted = parameter.tags.get("accepted", "").lower()
    return any(token in accepted for token in ("additional keys", "open map", "arbitrary keys"))


def find_open_ancestor(path: str, registry: Mapping[str, Parameter]) -> str | None:
    candidates = sorted(registry, key=len, reverse=True)
    for candidate in candidates:
        if path.startswith(candidate + ".") or path.startswith(candidate + "["):
            parameter = registry[candidate]
            if is_open_object(parameter):
                return candidate
    return None


def _finding(
    findings: list[common.Finding],
    severity: str,
    code: str,
    path: Path,
    parameter: str,
    line: int | None,
    message: str,
    category: str = "contract",
) -> None:
    findings.append(common.Finding(severity, code, str(path), parameter, line, message, category))


def audit_canonical(path: Path, parameters: list[Parameter], lines: list[str]) -> list[common.Finding]:
    findings: list[common.Finding] = []
    for parameter in parameters:
        expected = re.compile(rf"^\s*#\s*--\s+{re.escape(parameter.path)}(?:\s|$)")
        if not any(expected.match(comment) for comment in parameter.comments):
            _finding(findings, "error", "missing-description", path, parameter.path, parameter.line,
                     f"add an adjacent '# -- {parameter.path} ...' purpose line")
        for tag in REQUIRED_TAGS:
            if tag not in parameter.tags:
                _finding(findings, "error", f"missing-{tag}", path, parameter.path, parameter.line,
                         f"add an adjacent # @{tag} metadata line")

        declared = accepted_types(parameter.tags.get("type", ""))
        actual = common.yaml_kind(parameter.value)
        if declared and actual not in declared:
            _finding(findings, "error", "type-mismatch", path, parameter.path, parameter.line,
                     f"declared type {parameter.tags.get('type')!r} does not accept parsed {actual}")
        elif "type" in parameter.tags and not declared:
            _finding(findings, "warning", "unrecognized-type-contract", path, parameter.path,
                     parameter.line, f"cannot verify @type value {parameter.tags['type']!r}")

        required = parameter.tags.get("required", "").lower()
        if required and required not in {"true", "false", "conditional"}:
            _finding(findings, "warning", "unrecognized-required-contract", path, parameter.path,
                     parameter.line, "@required should be true, false, or conditional")

        if common.is_secret_path(parameter.path) and common.is_concrete_secret(parameter.value):
            _finding(findings, "error", "concrete-secret-default", path, parameter.path, parameter.line,
                     "secret-like parameter has a concrete reusable default; value was not recorded")
        if isinstance(parameter.value, str) and CREDENTIAL_URL_RE.search(parameter.value):
            _finding(findings, "error", "credential-bearing-url", path, parameter.path, parameter.line,
                     "URL contains inline user information; split credentials into a Secret")
        if "configmap" in parameter.path.lower() and common.is_secret_path(parameter.path):
            _finding(findings, "error", "secret-in-configmap", path, parameter.path, parameter.line,
                     "secret-like parameter belongs in a Secret or external credential mechanism")
        if "[" in parameter.path:
            _finding(findings, "warning", "non-simple-values-key", path, parameter.path, parameter.line,
                     "key requires bracket/index access; confirm every Helm template consumer")

    for number, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        if re.search(r"(^|\s)[&*][A-Za-z0-9_-]+(?:\s|$)", line):
            _finding(findings, "warning", "yaml-anchor-or-alias", path, "", number,
                     "anchors and aliases require full consumer-toolchain compatibility evidence", "portability")
        if re.match(r"^\s*<<\s*:", line):
            _finding(findings, "error", "yaml-merge-key", path, "", number,
                     "merge keys are outside YAML 1.2 core and are not portable configuration contracts", "portability")
        if re.search(r"(^|\s)![^!\s][^\s]*", line):
            _finding(findings, "error", "custom-yaml-tag", path, "", number,
                     "custom tags are not accepted in portable Helm values", "safety")
        if "{{" in line or "}}" in line:
            _finding(findings, "warning", "template-expression-in-values", path, "", number,
                     "values files are data unless a reviewed template explicitly invokes tpl", "coverage")
        if AMBIGUOUS_SCALAR_RE.match(line):
            _finding(findings, "warning", "cross-parser-scalar-hazard", path, "", number,
                     "quote or type this scalar explicitly and test the actual consumer parser", "portability")
    return findings


def _infer_scalar(text: str) -> Any:
    if text == "":
        return {}
    parser = common.new_yaml()
    try:
        return parser.load(f"value: {text}\n")["value"]
    except Exception:
        return text.strip().strip("\"'")


def active_template_parameters(
    path: Path, *, max_bytes: int = common.DEFAULT_MAX_BYTES
) -> tuple[Any, list[Parameter], list[str], str | None]:
    _, text, data = common.load_mapping(path, max_bytes=max_bytes)
    lines = text.splitlines()
    mode: str | None = None
    for line in lines[:40]:
        match = MODE_RE.match(line)
        if match:
            mode = match.group(1)
            break
    return data, flatten_parameters(data, lines), lines, mode


def commented_template_paths(
    lines: list[str], registry: Mapping[str, Parameter]
) -> list[tuple[str, int, Any]]:
    """Statically infer simple commented mappings; complex examples remain a coverage gap."""
    found: list[tuple[str, int, Any]] = []
    stack: list[tuple[int, str, bool]] = []

    def pop_to(indent: int) -> None:
        while stack and indent <= stack[-1][0]:
            stack.pop()

    for index, raw in enumerate(lines):
        stripped = raw.lstrip()
        if not stripped:
            continue
        base_indent = len(raw) - len(stripped)
        commented = stripped.startswith("#")
        content = stripped[1:] if commented else raw
        if commented and content.startswith(" "):
            content = content[1:]
        if commented and content.startswith(("@", "--")):
            continue
        match = COMMENTED_KEY_RE.match(content)
        if not match:
            continue
        indent = (base_indent + len(match.group(1))) if commented else len(match.group(1))
        key = match.group(2)
        scalar = (match.group(3) or "").strip()
        pop_to(indent)
        if stack and stack[-1][2]:
            continue
        parent = stack[-1][1] if stack else ""
        path = join_path(parent, key)
        value = _infer_scalar(scalar)
        if commented:
            found.append((path, index + 1, value))
        canonical = registry.get(path)
        is_array = canonical is not None and common.yaml_kind(canonical.value) == "array"
        if scalar == "" or isinstance(value, Mapping):
            stack.append((indent, path, is_array))
    return found


def audit_template(
    path: Path,
    canonical_registry: Mapping[str, Parameter],
    *,
    max_bytes: int = common.DEFAULT_MAX_BYTES,
) -> tuple[list[common.Finding], list[str]]:
    findings: list[common.Finding] = []
    coverage: list[str] = []
    data, active, lines, mode = active_template_parameters(path, max_bytes=max_bytes)
    if mode is None:
        _finding(findings, "error", "missing-template-mode", path, "", 1,
                 "declare '# @mode active-overlay' or '# @mode commented-skeleton' in the header")
    if mode == "active-overlay" and not data:
        _finding(findings, "error", "empty-active-overlay", path, "", 1,
                 "an active overlay must contain at least one active value")
    if mode == "commented-skeleton" and data:
        _finding(findings, "warning", "active-values-in-skeleton", path, "", 1,
                 "confirm every active value is safe when the skeleton is applied unchanged")

    for parameter in active:
        canonical = canonical_registry.get(parameter.path)
        if canonical is None:
            if find_open_ancestor(parameter.path, canonical_registry) is None:
                _finding(findings, "error", "template-only-path", path, parameter.path,
                         parameter.line, "path is absent from canonical values and documented open maps")
            continue
        if common.yaml_kind(parameter.value) != common.yaml_kind(canonical.value):
            _finding(findings, "error", "template-type-mismatch", path, parameter.path, parameter.line,
                     f"template uses {common.yaml_kind(parameter.value)}; canonical uses {common.yaml_kind(canonical.value)}")
        if common.is_secret_path(parameter.path) and common.is_concrete_secret(parameter.value):
            _finding(findings, "error", "concrete-secret-template-value", path, parameter.path,
                     parameter.line, "operator template contains a concrete secret-like value")

    for path_text, line, value in commented_template_paths(lines, canonical_registry):
        canonical = canonical_registry.get(path_text)
        if canonical is None:
            if find_open_ancestor(path_text, canonical_registry) is None:
                _finding(findings, "error", "commented-template-only-path", path, path_text, line,
                         "commented example is absent from canonical values and documented open maps")
            continue
        expected = common.yaml_kind(canonical.value)
        actual = common.yaml_kind(value)
        if expected != actual and not (expected == "string" and actual == "null"):
            _finding(findings, "error", "commented-template-type-mismatch", path, path_text, line,
                     f"commented example uses {actual}; canonical uses {expected}")
        if common.is_secret_path(path_text) and common.is_concrete_secret(value):
            _finding(findings, "error", "concrete-secret-commented-example", path, path_text, line,
                     "commented example contains a concrete secret-like value")

    coverage.append("commented-template analysis recognizes simple mapping syntax only; list items, flow mappings, and dynamic activation require manual review")
    return findings, coverage


def _schema_refs(node: Any, path: str = "$") -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    if isinstance(node, Mapping):
        for key, value in node.items():
            child = f"{path}.{key}"
            if key == "$ref" and isinstance(value, str):
                refs.append((child, value))
            refs.extend(_schema_refs(value, child))
    elif isinstance(node, Sequence) and not isinstance(node, (str, bytes, bytearray)):
        for index, value in enumerate(node):
            refs.extend(_schema_refs(value, f"{path}[{index}]"))
    return refs


def validate_schema(
    values: Any,
    schema_path: Path,
    *,
    dialect_override: str | None,
    max_bytes: int,
) -> tuple[list[common.Finding], list[str], dict[str, Any]]:
    findings: list[common.Finding] = []
    coverage: list[str] = []
    metadata: dict[str, Any] = {"schema": str(schema_path), "validated": False}
    try:
        resolved, text = common.read_text(schema_path, max_bytes=max_bytes)
        schema = json.loads(text)
    except (common.InputError, json.JSONDecodeError) as exc:
        _finding(findings, "error", "schema-read-failure", schema_path, "", None, str(exc), "schema")
        return findings, coverage, metadata
    if not isinstance(schema, Mapping):
        _finding(findings, "error", "schema-root-not-object", resolved, "", None,
                 "JSON Schema root must be an object or boolean; this linter requires an object", "schema")
        return findings, coverage, metadata

    dialect = schema.get("$schema") or dialect_override
    if not isinstance(dialect, str) or not dialect:
        _finding(findings, "error", "schema-dialect-undeclared", resolved, "", None,
                 "declare $schema or pass --schema-dialect; implicit latest-draft selection is not reproducible", "schema")
        return findings, coverage, metadata
    if "$schema" not in schema:
        schema = dict(schema)
        schema["$schema"] = dialect
        coverage.append("schema dialect supplied by command-line override rather than committed $schema")
    metadata["dialect"] = dialect

    unsafe_refs = [(location, value) for location, value in _schema_refs(schema) if not value.startswith("#")]
    for location, value in unsafe_refs[:50]:
        _finding(findings, "error", "external-schema-reference", resolved, location, None,
                 f"only document-local $ref values are accepted by the bundled offline linter: {value!r}", "schema")
    if unsafe_refs:
        return findings, coverage, metadata

    if jsonschema is None or validators is None:
        coverage.append("jsonschema dependency is unavailable; schema validation did not run")
        _finding(findings, "error", "schema-validator-unavailable", resolved, "", None,
                 "install the exact dependency in scripts/requirements.txt in a reviewed environment", "tool")
        return findings, coverage, metadata

    try:
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
    except Exception as exc:
        _finding(findings, "error", "invalid-json-schema", resolved, "", None, str(exc), "schema")
        return findings, coverage, metadata

    compatibility = common.json_compatibility_errors(values)
    for message in compatibility[:100]:
        _finding(findings, "error", "non-json-compatible-value", resolved, "", None, message, "schema")
    if compatibility:
        return findings, coverage, metadata

    try:
        validator = validator_class(schema)
        errors = sorted(validator.iter_errors(values), key=lambda item: list(item.absolute_path))
    except Exception as exc:
        _finding(findings, "error", "schema-validation-failure", resolved, "", None, str(exc), "tool")
        return findings, coverage, metadata
    for error in errors[:200]:
        instance_path = "$"
        for component in error.absolute_path:
            instance_path += f"[{component}]" if isinstance(component, int) else f".{component}"
        _finding(findings, "error", "schema-instance-invalid", resolved, instance_path, None,
                 error.message, "schema")
    if len(errors) > 200:
        coverage.append(f"schema diagnostics truncated: {len(errors) - 200} additional errors")
    metadata["validated"] = True
    metadata["validator"] = getattr(jsonschema, "__version__", "unknown")
    metadata["format_assertions"] = False
    coverage.append("JSON Schema format keywords were not asserted")
    return findings, coverage, metadata


def chart_kind(chart_yaml: Any) -> str:
    if isinstance(chart_yaml, Mapping) and chart_yaml.get("type") == "library":
        return "library"
    return "application"


def summarize(
    findings: list[common.Finding],
    parameter_count: int,
    coverage: list[str],
    schema: dict[str, Any],
    warnings_as_errors: bool,
) -> dict[str, Any]:
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    status = "failed" if errors or (warnings_as_errors and warnings) else "complete"
    return {
        "status": status,
        "parameter_count": parameter_count,
        "errors": errors,
        "warnings": warnings,
        "coverage_gaps": sorted(set(coverage)),
        "tool_versions": {**common.version_info(), "jsonschema": getattr(jsonschema, "__version__", "unavailable")},
        "schema": schema,
        "findings": [asdict(item) for item in findings],
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    findings: list[common.Finding] = []
    coverage: list[str] = []
    schema_metadata: dict[str, Any] = {"validated": False}
    parameter_count = 0
    try:
        chart = args.chart.expanduser().resolve(strict=True)
        if not chart.is_dir():
            raise ContractError(f"chart is not a directory: {chart}")
        values_path = common.confine_existing_path(chart, args.values or chart / "values.yaml", kind="values")
        chart_path = common.confine_existing_path(chart, chart / "Chart.yaml", kind="Chart.yaml")
        _, values_text, canonical = common.load_mapping(values_path, max_bytes=args.max_bytes)
        parameters = flatten_parameters(canonical, values_text.splitlines())
        parameter_count = len(parameters)
        findings.extend(audit_canonical(values_path, parameters, values_text.splitlines()))
        registry = {parameter.path: parameter for parameter in parameters}
        chart_data = load_yaml(chart_path, max_bytes=args.max_bytes)

        if not args.skip_template:
            template_candidate = args.values_template or chart / "values-template.yaml"
            if template_candidate.exists():
                template_path = common.confine_existing_path(chart, template_candidate, kind="values template")
                template_findings, template_coverage = audit_template(
                    template_path, registry, max_bytes=args.max_bytes
                )
                findings.extend(template_findings)
                coverage.extend(template_coverage)
            elif chart_kind(chart_data) != "library":
                _finding(findings, "error", "missing-values-template", Path(template_candidate), "", None,
                         "installable application chart requires an explicit operator-template decision")
            else:
                coverage.append("values-template omitted for library chart")
        else:
            coverage.append("values-template reconciliation skipped by explicit option")

        if not args.skip_schema:
            schema_candidate = args.schema or chart / "values.schema.json"
            if schema_candidate.exists():
                schema_path = common.confine_existing_path(chart, schema_candidate, kind="schema")
                schema_findings, schema_coverage, schema_metadata = validate_schema(
                    canonical, schema_path, dialect_override=args.schema_dialect, max_bytes=args.max_bytes
                )
                findings.extend(schema_findings)
                coverage.extend(schema_coverage)
            else:
                _finding(findings, "error", "missing-values-schema", Path(schema_candidate), "", None,
                         "values.schema.json is required for a machine-enforced chart contract", "schema")
        else:
            coverage.append("JSON Schema validation skipped by explicit option")
    except (OSError, common.InputError, ContractError) as exc:
        findings.append(common.Finding("error", "analysis-failure", str(args.chart), "", None, str(exc), "tool"))

    result = summarize(findings, parameter_count, coverage, schema_metadata, args.warnings_as_errors)
    if args.format == "json":
        print(common.stable_json(result), end="")
    else:
        for item in findings:
            location = item.file + (f":{item.line}" if item.line else "")
            if item.path:
                location += f" [{item.path}]"
            print(f"{item.severity.upper():7} {item.code}: {location}: {item.message}")
        for gap in result["coverage_gaps"]:
            print(f"COVERAGE {gap}")
        print(f"Audited {parameter_count} parameters: {result['errors']} error(s), {result['warnings']} warning(s).")
    return 1 if result["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
