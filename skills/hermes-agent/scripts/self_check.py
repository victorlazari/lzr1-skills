#!/usr/bin/env python3
"""Validate the Hermes Agent skill package without network access.

The self-check validates this package only. It does not import Hermes, inspect a
user installation, execute fixture commands, access the network, or certify a
target deployment as secure.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit, urlunsplit

sys.dont_write_bytecode = True

EXPECTED_FILES = {
    "SKILL.md",
    "references/architecture-runtime.md",
    "references/automation-multi-agent.md",
    "references/configuration-providers.md",
    "references/development-extensions.md",
    "references/gateways-integrations.md",
    "references/memory-context-skills.md",
    "references/operating-model.md",
    "references/security-production.md",
    "references/sources.md",
    "references/tools-execution-isolation.md",
    "references/troubleshooting-recovery.md",
    "scripts/hermes_preflight.py",
    "scripts/self_check.py",
    "templates/assessment-report.md",
    "templates/change-plan.md",
    "templates/config-hardening-fragment.yaml",
    "templates/env.example",
    "templates/production-readiness.md",
    "tests/fixtures/invalid-home/.env",
    "tests/fixtures/invalid-home/auth.json",
    "tests/fixtures/invalid-home/config.yaml",
    "tests/fixtures/safe-home/.env",
    "tests/fixtures/safe-home/config.yaml",
    "tests/fixtures/unsafe-home/.env",
    "tests/fixtures/unsafe-home/config.yaml",
    "tests/test_hermes_preflight.py",
}
EXPECTED_DIRECTORIES = {
    "references",
    "scripts",
    "templates",
    "tests",
    "tests/fixtures",
    "tests/fixtures/invalid-home",
    "tests/fixtures/safe-home",
    "tests/fixtures/unsafe-home",
}
INSTALLER_MARKER = ".lzr1-managed"
INSTALLER_MARKER_TEXT = (
    "schema=1\n"
    "source=victorlazari/lzr1-skills\n"
    "skill=hermes-agent\n"
)
ALLOWED_FRONTMATTER = {"name", "description", "license"}
VERIFIED_DATE = "2026-08-08"
UPSTREAM_COMMIT = "3e6a081d60e8d04a03d37008464f44555bc88832"
UPSTREAM_VERSION = "0.20.0"
UPSTREAM_RELEASE = "v2026.8.3"
OFFICIAL_SOURCE_COUNT = 98
SOURCE_DEFINITION_COUNT = 109
MIN_GUIDANCE_SOURCE_URLS = 50
MAX_PACKAGE_FILE_BYTES = 2 * 1024 * 1024
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CITATION = re.compile(r"(?<!\!)\[([0-9]+)\](?!\()")
SOURCE_DEFINITION = re.compile(r"^\[([0-9]+)\]: (https://\S+)(?:\s+\"[^\"]*\")?$", re.MULTILINE)
OFFICIAL_ROW = re.compile(
    r"^\| ([0-9]+) \| \[[^\]]+\]\[([0-9]+)\] \| `[^`]+` \| (?:yes|no) \| [0-9]+\.[0-9]+ \|$",
    re.MULTILINE,
)
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
REAL_TOKEN_SHAPE = re.compile(
    r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?(?!REPLACE_|EXAMPLE_|NOT_A_REAL_)[A-Za-z0-9_./+=-]{20,}"
)
PREFLIGHT_ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "argparse",
    "dataclasses",
    "json",
    "os",
    "pathlib",
    "re",
    "stat",
    "sys",
    "typing",
}
PREFLIGHT_FORBIDDEN_CALLS = {
    "__import__",
    "compile",
    "eval",
    "exec",
    "open",
    "os.popen",
    "os.system",
}
PREFLIGHT_FORBIDDEN_PREFIXES = (
    "ftplib.",
    "http.",
    "requests.",
    "smtplib.",
    "socket.",
    "subprocess.",
    "urllib.",
)
PREFLIGHT_MUTATING_METHODS = {
    "chmod",
    "chown",
    "hardlink_to",
    "mkdir",
    "rename",
    "replace",
    "rmdir",
    "symlink_to",
    "touch",
    "unlink",
    "write_bytes",
    "write_text",
}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.metrics: dict[str, int | str] = {}

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate this Hermes Agent skill package without network access."
    )
    parser.add_argument("--json-output", action="store_true", help="Emit JSON results")
    parser.add_argument(
        "--require-installer-marker",
        action="store_true",
        help="Require the exact managed-install ownership marker",
    )
    return parser.parse_args(argv)


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def inventory(root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        try:
            mode = path.lstat().st_mode
        except OSError:
            continue
        if stat.S_ISDIR(mode):
            directories.add(relative)
        elif stat.S_ISREG(mode) or stat.S_ISLNK(mode):
            files.add(relative)
    return files, directories


def check_installer_marker(audit: Audit, root: Path, *, required: bool) -> None:
    marker = root / INSTALLER_MARKER
    if not marker.exists() and not marker.is_symlink():
        if required:
            audit.error(f"{INSTALLER_MARKER}: required managed-install marker is missing")
        return
    try:
        mode = marker.lstat().st_mode
    except OSError as exc:
        audit.error(f"{INSTALLER_MARKER}: cannot inspect installer marker: {exc}")
        return
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        audit.error(f"{INSTALLER_MARKER}: marker must be a regular, non-symlink file")
        return
    try:
        content = marker.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        audit.error(f"{INSTALLER_MARKER}: cannot read installer marker: {exc}")
        return
    if content != INSTALLER_MARKER_TEXT:
        audit.error(f"{INSTALLER_MARKER}: invalid installer marker content")


def check_inventory(audit: Audit, root: Path) -> None:
    files, directories = inventory(root)
    missing_files = sorted(EXPECTED_FILES - files)
    unexpected_files = sorted(files - EXPECTED_FILES - {INSTALLER_MARKER})
    missing_directories = sorted(EXPECTED_DIRECTORIES - directories)
    unexpected_directories = sorted(directories - EXPECTED_DIRECTORIES)
    for relative in missing_files:
        audit.error(f"missing required file: {relative}")
    for relative in unexpected_files:
        audit.error(f"unexpected package file: {relative}")
    for relative in missing_directories:
        audit.error(f"missing required directory: {relative}")
    for relative in unexpected_directories:
        audit.error(f"unexpected package directory: {relative}")
    audit.metrics["expected_files"] = len(EXPECTED_FILES)


def parse_frontmatter(audit: Audit, text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        audit.error("SKILL.md: missing opening YAML frontmatter marker")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        audit.error("SKILL.md: missing closing YAML frontmatter marker")
        return {}
    result: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            audit.error(f"SKILL.md:{number}: unsupported frontmatter syntax")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if not key or not value:
            audit.error(f"SKILL.md:{number}: frontmatter keys and values must be non-empty")
            continue
        if key in result:
            audit.error(f"SKILL.md:{number}: duplicate frontmatter key {key!r}")
        result[key] = value
    if set(result) != ALLOWED_FRONTMATTER:
        audit.error(
            f"SKILL.md: frontmatter keys must be exactly {sorted(ALLOWED_FRONTMATTER)}"
        )
    if result.get("name") != "hermes-agent":
        audit.error("SKILL.md: frontmatter name must equal hermes-agent")
    if not result.get("description", "").strip():
        audit.error("SKILL.md: frontmatter description must be non-empty")
    if result.get("license") != "MIT":
        audit.error("SKILL.md: frontmatter license must equal MIT")
    return result


def check_entrypoint(audit: Audit, root: Path) -> None:
    path = root / "SKILL.md"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        audit.error(f"SKILL.md: cannot read: {exc}")
        return
    parse_frontmatter(audit, text)
    line_count = len(text.splitlines())
    audit.metrics["skill_lines"] = line_count
    if not 180 <= line_count <= 500:
        audit.error(f"SKILL.md: expected 180-500 lines, found {line_count}")
    required_markers = (
        f"**Verified:** {VERIFIED_DATE}",
        UPSTREAM_COMMIT,
        f"package version `{UPSTREAM_VERSION}`",
        f"release `{UPSTREAM_RELEASE}`",
        "## Non-negotiable safety contract",
        "## Follow the mandatory workflow",
        "## Resource map",
        "scripts/hermes_preflight.py",
        "references/sources.md",
        "templates/production-readiness.md",
    )
    for marker in required_markers:
        if marker not in text:
            audit.error(f"SKILL.md: missing required marker {marker!r}")
    if "curl | bash" in text or "curl|bash" in text:
        audit.error("SKILL.md: must not recommend an unreviewed pipe-to-shell workflow")


def valid_markdown_title(value: str) -> bool:
    value = value.strip()
    return bool(
        len(value) >= 2
        and (
            (value[0] == value[-1] and value[0] in {'"', "'"})
            or (value[0] == "(" and value[-1] == ")")
        )
        and "\n" not in value
        and "\r" not in value
    )


def target_from_markdown(raw: str) -> str | None:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing < 0:
            return None
        target = value[1:closing]
        suffix = value[closing + 1 :].strip()
        if suffix and not valid_markdown_title(suffix):
            return None
    else:
        parts = value.split(None, 1)
        target = parts[0] if parts else ""
        if len(parts) == 2 and not valid_markdown_title(parts[1]):
            return None
    return unquote(target)


def check_markdown_links(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            audit.error(f"{path.relative_to(root)}: cannot read Markdown: {exc}")
            continue
        for raw in MARKDOWN_LINK.findall(text):
            target = target_from_markdown(raw)
            if target is None:
                audit.error(
                    f"{path.relative_to(root)}: malformed Markdown link destination {raw!r}"
                )
                continue
            if not target or target.startswith("#"):
                continue
            if any(
                ord(character) < 32 or ord(character) == 127 for character in target
            ):
                audit.error(f"{path.relative_to(root)}: unsafe link target {target!r}")
                continue
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                if parsed.scheme != "https":
                    audit.error(
                        f"{path.relative_to(root)}: external links must use HTTPS: {target}"
                    )
                continue
            file_part = target.split("#", 1)[0].split("?", 1)[0]
            if not file_part:
                continue
            normalized = file_part.replace("\\", "/")
            pure = PurePosixPath(normalized)
            if pure.is_absolute() or any(
                ord(character) < 32 or ord(character) == 127 for character in normalized
            ):
                audit.error(f"{path.relative_to(root)}: unsafe relative link {target}")
                continue
            resolved = (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                audit.error(f"{path.relative_to(root)}: link escapes package root: {target}")
                continue
            if not resolved.exists():
                audit.error(
                    f"{path.relative_to(root)}: missing relative-link target {target}"
                )


def check_file_safety(audit: Audit, root: Path) -> None:
    forbidden_suffixes = {".exe", ".dll", ".so", ".dylib", ".jar", ".zip", ".tar", ".tgz", ".gz"}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        try:
            item_stat = path.lstat()
        except OSError as exc:
            audit.error(f"{relative}: cannot inspect: {exc}")
            continue
        if stat.S_ISLNK(item_stat.st_mode):
            audit.error(f"{relative}: symlinks are not allowed in this package")
            continue
        if not stat.S_ISREG(item_stat.st_mode):
            continue
        if item_stat.st_size > MAX_PACKAGE_FILE_BYTES:
            audit.error(f"{relative}: file exceeds package size limit")
        if path.suffix.lower() in forbidden_suffixes:
            audit.error(f"{relative}: executable or archive artifact is not allowed")
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            audit.error(f"{relative}: must be readable UTF-8 text: {exc}")
            continue
        if any(
            ord(character) < 32 and character not in "\n\r\t" for character in text
        ) or "\x7f" in text:
            audit.error(f"{relative}: contains disallowed control characters")
        if PRIVATE_KEY.search(text):
            audit.error(f"{relative}: contains a private-key block")

    executable = {
        "scripts/hermes_preflight.py",
        "scripts/self_check.py",
        "tests/test_hermes_preflight.py",
    }
    for relative in executable:
        path = root / relative
        if path.exists() and os.name == "posix" and not (path.stat().st_mode & stat.S_IXUSR):
            audit.error(f"{relative}: expected owner-executable mode")


def resolved_ast_name(node: ast.AST, aliases: dict[str, str]) -> str:
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        prefix = resolved_ast_name(node.value, aliases)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def check_preflight_ast(audit: Audit, relative: str, source: str) -> bool:
    try:
        tree = ast.parse(source, filename=relative)
    except SyntaxError as exc:
        audit.error(f"{relative}: Python AST parse failure: {exc}")
        return False

    aliases: dict[str, str] = {}
    violations: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for imported in node.names:
                root_name = imported.name.split(".", 1)[0]
                if root_name not in PREFLIGHT_ALLOWED_IMPORT_ROOTS:
                    violations.add(f"forbidden import {imported.name!r}")
                aliases[imported.asname or root_name] = imported.name
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            root_name = module_name.split(".", 1)[0]
            if root_name not in PREFLIGHT_ALLOWED_IMPORT_ROOTS:
                violations.add(f"forbidden import from {module_name!r}")
            for imported in node.names:
                local_name = imported.asname or imported.name
                aliases[local_name] = f"{module_name}.{imported.name}".strip(".")

    open_flags: dict[str, set[str] | None] = {}

    def flag_symbols(node: ast.AST) -> set[str] | None:
        name = resolved_ast_name(node, aliases)
        if name in {"os.O_RDONLY", "os.O_NOFOLLOW", "os.O_CLOEXEC"}:
            return {name}
        if isinstance(node, ast.Name):
            return open_flags.get(node.id)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = flag_symbols(node.left)
            right = flag_symbols(node.right)
            if left is not None and right is not None:
                return left | right
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                open_flags[target.id] = flag_symbols(node.value)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            if isinstance(node.op, ast.BitOr):
                current = open_flags.get(node.target.id)
                addition = flag_symbols(node.value)
                open_flags[node.target.id] = (
                    current | addition
                    if current is not None and addition is not None
                    else None
                )

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call_name = resolved_ast_name(node.func, aliases)
        tail = call_name.rsplit(".", 1)[-1]
        if call_name in PREFLIGHT_FORBIDDEN_CALLS or any(
            call_name.startswith(prefix) for prefix in PREFLIGHT_FORBIDDEN_PREFIXES
        ):
            violations.add(f"forbidden call {call_name!r}")
        if tail in PREFLIGHT_MUTATING_METHODS:
            violations.add(f"mutating filesystem call {call_name!r}")
        if call_name == "os.open":
            if len(node.args) < 2:
                violations.add("os.open must provide explicit read-only flags")
            else:
                symbols = flag_symbols(node.args[1])
                if symbols is None or "os.O_RDONLY" not in symbols:
                    violations.add("os.open flags are not provably read-only")
        for keyword in node.keywords:
            if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant):
                if keyword.value.value is True:
                    violations.add("shell=True is forbidden")

    for violation in sorted(violations):
        audit.error(f"{relative}: offline analyzer AST violation: {violation}")
    return not violations


def check_python(audit: Audit, root: Path) -> bool:
    preflight_ast_safe = False
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root).as_posix()
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except (OSError, UnicodeError, SyntaxError) as exc:
            audit.error(f"{relative}: Python syntax/read failure: {exc}")
            continue
        if relative == "scripts/hermes_preflight.py":
            preflight_ast_safe = check_preflight_ast(audit, relative, source)
    return preflight_ast_safe


def check_sources_and_citations(audit: Audit, root: Path) -> None:
    source_path = root / "references" / "sources.md"
    try:
        source_text = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        audit.error(f"references/sources.md: cannot read: {exc}")
        return

    required_markers = (
        f"**Verified:** {VERIFIED_DATE}",
        f"**Upstream snapshot:** `{UPSTREAM_COMMIT}`",
        f"**Coverage:** {OFFICIAL_SOURCE_COUNT} unique pages",
        "## Authority model",
        "## Refresh procedure",
        "## Official documentation ledger",
        "## Additional first-party controls",
        "## References",
    )
    for marker in required_markers:
        if marker not in source_text:
            audit.error(f"references/sources.md: missing required marker {marker!r}")

    definitions = SOURCE_DEFINITION.findall(source_text)
    definition_numbers = [int(number) for number, _ in definitions]
    expected_definitions = list(range(1, SOURCE_DEFINITION_COUNT + 1))
    if definition_numbers != expected_definitions:
        audit.error(
            "references/sources.md: source definitions must be contiguous 1-109 exactly once"
        )
    urls = [url.rstrip(".,;:") for _, url in definitions]
    if len(urls) != SOURCE_DEFINITION_COUNT:
        audit.error(
            f"references/sources.md: expected {SOURCE_DEFINITION_COUNT} definitions, found {len(urls)}"
        )
    if len(set(urls)) != len(urls):
        audit.error("references/sources.md: source URLs must be unique")
    allowed_hosts = {"hermes-agent.nousresearch.com", "github.com"}
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
            audit.error(f"references/sources.md: non-first-party or non-HTTPS source {url}")

    official_rows = OFFICIAL_ROW.findall(source_text)
    row_numbers = [int(left) for left, _ in official_rows]
    row_refs = [int(right) for _, right in official_rows]
    expected_rows = list(range(1, OFFICIAL_SOURCE_COUNT + 1))
    if row_numbers != expected_rows or row_refs != expected_rows:
        audit.error("references/sources.md: official ledger rows must map 1-98 exactly")
    audit.metrics["official_sources"] = len(official_rows)
    audit.metrics["source_definitions"] = len(definitions)

    fallback_expectations = {
        106: "website/docs/integrations/index.md",
        107: "website/docs/reference/tools-reference.md",
        108: "website/docs/user-guide/docker.md",
        109: "website/docs/user-guide/features/honcho.md",
    }
    definition_map = {int(number): url for number, url in definitions}
    for number, suffix in fallback_expectations.items():
        url = definition_map.get(number, "")
        if UPSTREAM_COMMIT not in url or not url.endswith(suffix):
            audit.error(
                f"references/sources.md: fallback [{number}] must be pinned to the research commit and expected path"
            )

    def canonical_source_url(url: str) -> str:
        parsed = urlsplit(url.rstrip(".,;:"))
        path = parsed.path.rstrip("/") or "/"
        return urlunsplit(
            (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, "")
        )

    ledger_urls = {canonical_source_url(url) for url in urls}
    official_urls = {
        canonical_source_url(definition_map[number])
        for number in range(1, OFFICIAL_SOURCE_COUNT + 1)
        if number in definition_map
    }
    guidance_urls: set[str] = set()
    guidance_paths = [
        root / "SKILL.md",
        *sorted((root / "references").glob("*.md")),
    ]
    for path in guidance_paths:
        if path.name == "sources.md":
            continue
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            audit.error(f"{relative}: cannot read citations: {exc}")
            continue
        local_definitions = SOURCE_DEFINITION.findall(text)
        local_map = {
            int(number): canonical_source_url(url)
            for number, url in local_definitions
        }
        local_numbers = [int(number) for number, _ in local_definitions]
        expected_local = list(range(1, len(local_definitions) + 1))
        if not local_definitions:
            audit.error(f"{relative}: must define local numeric source references")
            continue
        if local_numbers != expected_local or len(local_map) != len(local_definitions):
            audit.error(
                f"{relative}: local source definitions must be contiguous and unique"
            )
        citation_text = SOURCE_DEFINITION.sub("", text)
        local_used = {int(number) for number in CITATION.findall(citation_text)}
        for number in sorted(local_used - set(local_map)):
            audit.error(f"{relative}: undefined local citation [{number}]")
        for number in sorted(set(local_map) - local_used):
            audit.error(f"{relative}: unused local source definition [{number}]")
        for number in sorted(local_used & set(local_map)):
            url = local_map[number]
            parsed = urlsplit(url)
            if parsed.scheme != "https" or parsed.hostname not in allowed_hosts:
                audit.error(f"{relative}: citation [{number}] is not first-party HTTPS")
            if url not in ledger_urls:
                audit.error(f"{relative}: citation [{number}] is absent from sources.md")
            guidance_urls.add(url)

    official_guidance_urls = guidance_urls & official_urls
    if len(official_guidance_urls) < MIN_GUIDANCE_SOURCE_URLS:
        audit.error(
            "Hermes guidance must substantively cite at least "
            f"{MIN_GUIDANCE_SOURCE_URLS} distinct official documentation pages; "
            f"found {len(official_guidance_urls)}"
        )
    audit.metrics["distinct_citations_used"] = len(guidance_urls)
    audit.metrics["guidance_source_urls"] = len(guidance_urls)
    audit.metrics["official_guidance_source_urls"] = len(official_guidance_urls)


def check_templates(audit: Audit, root: Path) -> None:
    required_markers = {
        "templates/assessment-report.md": (
            "## Immutable baseline",
            "## Authorization and trust model",
            "## Validation evidence",
            "## Residual risk, unknowns, and exceptions",
            "## Rollback and recovery status",
        ),
        "templates/change-plan.md": (
            "## Scope and exclusions",
            "## Credential and data handling",
            "## Backup and rollback",
            "## Consent record",
            "## Validation plan",
        ),
        "templates/production-readiness.md": (
            "## 3. Full-process and execution isolation",
            "## 4. Identity and authorization",
            "## 8. Extensions and supply chain",
            "## 9. Automation and external effects",
            "## 12. Recovery and incident response",
        ),
    }
    for relative, markers in required_markers.items():
        text = (root / relative).read_text(encoding="utf-8")
        if "{{" not in text or "}}" not in text:
            audit.error(f"{relative}: must contain explicit fill-in placeholders")
        for marker in markers:
            if marker not in text:
                audit.error(f"{relative}: missing required marker {marker!r}")

    yaml_text = (root / "templates/config-hardening-fragment.yaml").read_text(
        encoding="utf-8"
    )
    for marker in (
        "mode: manual",
        "denial_breaker_threshold: 3",
        "enabled: true",
        "pre_update_backup: full",
        "backend: docker",
        "home_mode: profile",
        "env_passthrough: []",
        "docker_network: false",
        "docker_run_as_host_user: false",
        "container_persistent: false",
    ):
        if marker not in yaml_text:
            audit.error(
                f"templates/config-hardening-fragment.yaml: missing safe marker {marker!r}"
            )
    if re.search(r"^\s*mode:\s*off\s*$", yaml_text, re.MULTILINE):
        audit.error("templates/config-hardening-fragment.yaml: approvals must not be off")

    env_text = (root / "templates/env.example").read_text(encoding="utf-8")
    active_env = "\n".join(
        line for line in env_text.splitlines() if line.strip() and not line.lstrip().startswith("#")
    )
    for marker in (
        "HERMES_YOLO_MODE=false",
        "API_SERVER_ENABLED=false",
        "API_SERVER_KEY=REPLACE_WITH_UNIQUE_HIGH_ENTROPY_SECRET",
    ):
        if marker not in active_env:
            audit.error(f"templates/env.example: missing safe active marker {marker!r}")
    if re.search(r"(?m)^HERMES_DASHBOARD_INSECURE=", active_env):
        audit.error("templates/env.example: deprecated insecure variable must not be active")
    if REAL_TOKEN_SHAPE.search(active_env):
        audit.error("templates/env.example: contains a secret-shaped active value")


def load_preflight(audit: Audit, root: Path):
    path = root / "scripts" / "hermes_preflight.py"
    spec = importlib.util.spec_from_file_location("hermes_agent_preflight_self_check", path)
    if spec is None or spec.loader is None:
        audit.error("scripts/hermes_preflight.py: cannot create import specification")
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # Package code is trusted input to its own self-check.
        audit.error(
            f"scripts/hermes_preflight.py: import failed: {type(exc).__name__}: {exc}"
        )
        return None
    return module


def check_preflight_contract(audit: Audit, root: Path) -> None:
    module = load_preflight(audit, root)
    if module is None:
        return
    with tempfile.TemporaryDirectory(prefix="hermes-package-self-check-") as temporary:
        temporary_root = Path(temporary)
        safe = temporary_root / "safe-home"
        unsafe = temporary_root / "unsafe-home"
        shutil.copytree(root / "tests" / "fixtures" / "safe-home", safe)
        shutil.copytree(root / "tests" / "fixtures" / "unsafe-home", unsafe)
        if os.name == "posix":
            (safe / ".env").chmod(0o600)
            (unsafe / ".env").chmod(0o600)
        safe_result = module.Analyzer(safe, "production", "untrusted", False).analyze()
        unsafe_result = module.Analyzer(
            unsafe, "production", "untrusted", False
        ).analyze()

    if not safe_result.get("valid"):
        audit.error("scripts/hermes_preflight.py: safe fixture must pass non-strict mode")
    if unsafe_result.get("valid"):
        audit.error("scripts/hermes_preflight.py: unsafe fixture must fail")
    unsafe_ids = {finding.get("id") for finding in unsafe_result.get("findings", [])}
    expected_ids = {
        "HERMES-API-001",
        "HERMES-APPROVAL-001",
        "HERMES-APPROVAL-002",
        "HERMES-EXEC-002",
        "HERMES-MCP-001",
        "HERMES-NET-001",
        "HERMES-NET-002",
        "HERMES-SECRET-001",
    }
    missing_ids = sorted(expected_ids - unsafe_ids)
    if missing_ids:
        audit.error(
            f"scripts/hermes_preflight.py: unsafe fixture missing findings {missing_ids}"
        )
    rendered = json.dumps(unsafe_result, sort_keys=True)
    if "redaction-sentinel-7f3a9c2e6b4d8f1a" in rendered:
        audit.error("scripts/hermes_preflight.py: report leaked the synthetic secret")
    if "AWS_SECRET_ACCESS_KEY" in rendered:
        audit.error("scripts/hermes_preflight.py: report leaked a forwarded variable name")
    audit.metrics["preflight_safe_errors"] = int(safe_result["summary"]["error"])
    audit.metrics["preflight_unsafe_errors"] = int(unsafe_result["summary"]["error"])


def check_fixture_hygiene(audit: Audit, root: Path) -> None:
    unsafe_config = (
        root / "tests" / "fixtures" / "unsafe-home" / "config.yaml"
    ).read_text(encoding="utf-8")
    expected_secret = "redaction-sentinel-7f3a9c2e6b4d8f1a"
    if unsafe_config.count(expected_secret) != 1:
        audit.error("unsafe fixture must contain exactly one known synthetic secret")
    for path in sorted((root / "tests" / "fixtures").rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if PRIVATE_KEY.search(text):
            audit.error(f"{path.relative_to(root)}: fixture contains a private key")
        for match in REAL_TOKEN_SHAPE.finditer(text):
            if expected_secret not in match.group(0):
                audit.error(
                    f"{path.relative_to(root)}: unexpected secret-shaped fixture value"
                )


def run(root: Path, *, require_installer_marker: bool = False) -> Audit:
    audit = Audit()
    check_inventory(audit, root)
    check_installer_marker(audit, root, required=require_installer_marker)
    if audit.errors:
        return audit
    check_entrypoint(audit, root)
    check_file_safety(audit, root)
    check_markdown_links(audit, root)
    preflight_ast_safe = check_python(audit, root)
    check_sources_and_citations(audit, root)
    check_templates(audit, root)
    check_fixture_hygiene(audit, root)
    if preflight_ast_safe:
        check_preflight_contract(audit, root)
    else:
        audit.error(
            "scripts/hermes_preflight.py: runtime contract skipped after AST safety failure"
        )
    return audit


def emit(audit: Audit, *, json_output: bool) -> None:
    payload = {
        "valid": not audit.errors,
        "errors": audit.errors,
        "warnings": audit.warnings,
        "metrics": audit.metrics,
    }
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    state = "PASS" if not audit.errors else "FAIL"
    print(f"{state}: {len(audit.errors)} error(s), {len(audit.warnings)} warning(s)")
    for error in audit.errors:
        print(f"ERROR: {error}")
    for warning in audit.warnings:
        print(f"WARNING: {warning}")
    for key, value in sorted(audit.metrics.items()):
        print(f"METRIC: {key}={value}")
    print("This validates package integrity and fixtures, not a Hermes deployment.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    audit = run(
        package_root(), require_installer_marker=args.require_installer_marker
    )
    emit(audit, json_output=args.json_output)
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
