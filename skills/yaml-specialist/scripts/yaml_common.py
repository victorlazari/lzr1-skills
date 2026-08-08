#!/usr/bin/env python3
"""Shared bounded YAML utilities for yaml-specialist.

The module never installs dependencies, resolves remote references, constructs Python
objects from custom tags, or mutates target files. It uses ruamel.yaml's round-trip
loader solely to preserve comments and locations for diagnostics.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

try:
    import ruamel.yaml
    from ruamel.yaml import YAML
    from ruamel.yaml.comments import CommentedMap, CommentedSeq
except ImportError as exc:  # pragma: no cover - explicit dependency guard
    raise SystemExit(
        "missing dependency: install the exact versions in scripts/requirements.txt "
        "inside a reviewed virtual environment"
    ) from exc

DEFAULT_MAX_BYTES = 2 * 1024 * 1024
DEFAULT_MAX_DOCUMENTS = 100
DEFAULT_MAX_DEPTH = 80
DEFAULT_MAX_NODES = 200_000
DEFAULT_MAX_ALIASES = 1_000
CONTROL_CHARACTER = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ALIAS_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])[*&][A-Za-z0-9_-]+")
SECRET_PATH = re.compile(
    r"(?:^|[._-])(?:password|passwd|token|api[_-]?key|client[_-]?secret|"
    r"private[_-]?key|secret[_-]?key|credential|auth[_-]?jwt|cookie)(?:$|[._-])",
    re.IGNORECASE,
)
REFERENCE_PATH = re.compile(
    r"(?:^|\.)(?:existing_secret\.(?:name|key|ref)|secret_ref\.(?:name|key)|"
    r"secret_(?:name|key|ref)|image_pull_secrets?(?:\.[0-9]+)?\.name|"
    r"automount_service_account_token|token_expiration_seconds)$",
    re.IGNORECASE,
)
PLACEHOLDER = re.compile(
    r"^(?:\$\{[^}]+\}|\{\{.+\}\}|<[^>]+>|change[_ -]?me|replace[_ -]?me|"
    r"fill[_ -]?me|redacted|provided[_ -]through[_ -]secret[_ -]management)$",
    re.IGNORECASE,
)


class InputError(ValueError):
    """Raised when bounded, safe analysis cannot continue."""


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    file: str
    path: str
    line: int | None
    message: str
    category: str = "validation"


def finding_dict(item: Finding) -> dict[str, Any]:
    return asdict(item)


def version_info() -> dict[str, str]:
    return {
        "ruamel_yaml": getattr(ruamel.yaml, "__version__", "unknown"),
        "yaml_version": "1.2",
        "duplicate_key_policy": "reject",
    }


def ensure_regular_file(path: Path, *, max_bytes: int = DEFAULT_MAX_BYTES) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    metadata = resolved.lstat()
    if stat.S_ISLNK(metadata.st_mode):
        raise InputError(f"symbolic-link inputs are not accepted: {path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise InputError(f"input is not a regular file: {path}")
    if metadata.st_size > max_bytes:
        raise InputError(f"input exceeds {max_bytes} bytes: {path}")
    return resolved


def read_text(path: Path, *, max_bytes: int = DEFAULT_MAX_BYTES) -> tuple[Path, str]:
    resolved = ensure_regular_file(path, max_bytes=max_bytes)
    data = resolved.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff", b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        raise InputError(f"UTF-16/UTF-32 input is not accepted; convert to UTF-8: {path}")
    if b"\x00" in data:
        raise InputError(f"NUL bytes are not accepted: {path}")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError(f"input is not valid UTF-8: {path}: {exc}") from exc
    if CONTROL_CHARACTER.search(text):
        raise InputError(f"input contains disallowed control characters: {path}")
    if text.count("\t") and any(line.startswith("\t") for line in text.splitlines()):
        raise InputError(f"tab indentation is not accepted: {path}")
    return resolved, text


def new_yaml() -> YAML:
    parser = YAML(typ="rt", pure=True)
    parser.version = (1, 2)
    parser.allow_duplicate_keys = False
    parser.preserve_quotes = True
    return parser


def _walk(node: Any, *, depth: int, counters: dict[str, int], max_depth: int, max_nodes: int) -> None:
    counters["nodes"] += 1
    if counters["nodes"] > max_nodes:
        raise InputError(f"parsed YAML exceeds {max_nodes} nodes")
    if depth > max_depth:
        raise InputError(f"parsed YAML exceeds depth {max_depth}")
    if isinstance(node, Mapping):
        for key, value in node.items():
            _walk(key, depth=depth + 1, counters=counters, max_depth=max_depth, max_nodes=max_nodes)
            _walk(value, depth=depth + 1, counters=counters, max_depth=max_depth, max_nodes=max_nodes)
    elif isinstance(node, Sequence) and not isinstance(node, (str, bytes, bytearray)):
        for value in node:
            _walk(value, depth=depth + 1, counters=counters, max_depth=max_depth, max_nodes=max_nodes)


def load_documents(
    path: Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_documents: int = DEFAULT_MAX_DOCUMENTS,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_nodes: int = DEFAULT_MAX_NODES,
    max_aliases: int = DEFAULT_MAX_ALIASES,
) -> tuple[Path, str, list[Any]]:
    resolved, text = read_text(path, max_bytes=max_bytes)
    alias_tokens = len(ALIAS_TOKEN.findall(text))
    if alias_tokens > max_aliases:
        raise InputError(f"input contains more than {max_aliases} anchor/alias tokens")
    parser = new_yaml()
    try:
        documents = list(parser.load_all(text))
    except Exception as exc:  # ruamel exposes parser-specific exception classes
        raise InputError(f"cannot parse YAML 1.2 with duplicate keys rejected: {exc}") from exc
    if len(documents) > max_documents:
        raise InputError(f"input contains {len(documents)} documents; limit is {max_documents}")
    counters = {"nodes": 0}
    for document in documents:
        _walk(document, depth=0, counters=counters, max_depth=max_depth, max_nodes=max_nodes)
    return resolved, text, documents


def load_mapping(path: Path, **limits: Any) -> tuple[Path, str, Mapping[str, Any]]:
    resolved, text, documents = load_documents(path, **limits)
    if len(documents) != 1:
        raise InputError(f"expected exactly one YAML document, found {len(documents)}: {path}")
    document = documents[0]
    if document is None:
        document = CommentedMap()
    if not isinstance(document, Mapping):
        raise InputError(f"expected a mapping at the document root: {path}")
    return resolved, text, document


def json_compatibility_errors(node: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if node is None or isinstance(node, (str, bool, int, float)):
        if isinstance(node, float) and (node != node or node in {float("inf"), float("-inf")}):
            errors.append(f"{path}: non-finite number is outside the JSON data model")
        return errors
    if isinstance(node, Mapping):
        for key, value in node.items():
            if not isinstance(key, str):
                errors.append(f"{path}: mapping key {key!r} is not a string")
                child = f"{path}.<non-string-key>"
            else:
                child = f"{path}.{key}" if path != "$" else f"$.{key}"
            errors.extend(json_compatibility_errors(value, child))
        return errors
    if isinstance(node, Sequence) and not isinstance(node, (str, bytes, bytearray)):
        for index, value in enumerate(node):
            errors.extend(json_compatibility_errors(value, f"{path}[{index}]"))
        return errors
    errors.append(f"{path}: {type(node).__name__} is outside the JSON data model")
    return errors


def yaml_kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, Mapping):
        return "object"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "array"
    return "string"


def is_secret_path(path: str) -> bool:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", path)
    normalized = re.sub(r"\[(?:\"([^\"]+)\"|'([^']+)'|([0-9]+))\]", lambda match: "." + next(value for value in match.groups() if value is not None), normalized)
    normalized = normalized.replace("-", "_").lower().strip(".")
    if REFERENCE_PATH.search(normalized):
        return False
    return bool(SECRET_PATH.search(normalized))


def is_concrete_secret(value: Any) -> bool:
    if value in (None, ""):
        return False
    if isinstance(value, str) and PLACEHOLDER.fullmatch(value.strip()):
        return False
    return not isinstance(value, (Mapping, Sequence)) or isinstance(value, (str, bytes, bytearray))


def redact_value(path: str, value: Any) -> Any:
    if is_secret_path(path) and is_concrete_secret(value):
        return "<redacted-secret-value>"
    if isinstance(value, Mapping):
        return "{}" if not value else f"<object:{len(value)} keys>"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return "[]" if not value else f"<array:{len(value)} items>"
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def confine_existing_path(root: Path, candidate: Path, *, kind: str = "path") -> Path:
    safe_root = root.expanduser().resolve(strict=True)
    resolved = candidate.expanduser().resolve(strict=True)
    try:
        resolved.relative_to(safe_root)
    except ValueError as exc:
        raise InputError(f"{kind} escapes declared root {safe_root}: {candidate}") from exc
    return resolved


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def iter_mapping_paths(node: Any, parent: str = "") -> Iterator[tuple[str, Any]]:
    if not isinstance(node, Mapping):
        return
    for key, value in node.items():
        path = f"{parent}.{key}" if parent else str(key)
        yield path, value
        if isinstance(value, Mapping):
            yield from iter_mapping_paths(value, path)


def safe_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def executable_version(command: Iterable[str], *, timeout: int = 10) -> tuple[int, str]:
    """Run an explicit version command without a shell; used only by self-check/discovery."""
    import subprocess

    environment = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")}
    completed = subprocess.run(
        list(command),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=timeout,
        env=environment,
    )
    return completed.returncode, completed.stdout.strip().splitlines()[0] if completed.stdout.strip() else ""
