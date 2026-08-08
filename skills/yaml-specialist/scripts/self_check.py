#!/usr/bin/env python3
"""Validate yaml-specialist without network, cluster, chart, or repository mutation.

The default check reads only this package, compiles source without importing target
code, validates bundled examples, and runs isolated package tests. Optional --repo
discovery executes read-only Git metadata commands and never parses target YAML.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True

VERIFIED_DATE = "2026-08-07"
ALLOWED_FRONTMATTER = {"name", "description", "license"}
EXPECTED_FILES = {
    "SKILL.md",
    "references/helm-chart-workflow.md",
    "references/kubernetes-validation.md",
    "references/refactoring-workflow.md",
    "references/security-and-trust.md",
    "references/sources.md",
    "references/troubleshooting.md",
    "references/validation-layers.md",
    "references/values-contract.md",
    "references/yaml-language.md",
    "scripts/build_refactor_inventory.py",
    "scripts/chart_metadata.py",
    "scripts/list_dependency_repositories.py",
    "scripts/rendered_manifest_lint.py",
    "scripts/requirements.txt",
    "scripts/scan_template_values.py",
    "scripts/self_check.py",
    "scripts/validate_chart.sh",
    "scripts/values_contract_lint.py",
    "scripts/yaml_common.py",
    "templates/validation-matrix.example.yaml",
    "templates/validation-report.md",
    "templates/values-contract.example.yaml",
    "templates/values-template.example.yaml",
    "templates/values.schema.example.json",
    "tests/fixtures/application-chart/Chart.yaml",
    "tests/fixtures/application-chart/templates/configmap.yaml",
    "tests/fixtures/application-chart/templates/deployment.yaml",
    "tests/fixtures/application-chart/templates/service.yaml",
    "tests/fixtures/application-chart/templates/serviceaccount.yaml",
    "tests/fixtures/application-chart/values-template.yaml",
    "tests/fixtures/application-chart/values.schema.json",
    "tests/fixtures/application-chart/values.yaml",
    "tests/fixtures/duplicate-key.yaml",
    "tests/fixtures/library-chart/Chart.yaml",
    "tests/fixtures/library-chart/templates/_helpers.tpl",
    "tests/fixtures/library-chart/values.schema.json",
    "tests/fixtures/library-chart/values.yaml",
    "tests/fixtures/rendered-dangling.yaml",
    "tests/fixtures/rendered-valid.yaml",
    "tests/test_validate_chart.sh",
    "tests/test_yaml_specialist.py",
}
EXPECTED_REQUIREMENTS = {"jsonschema": "4.26.0", "ruamel.yaml": "0.19.1"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTTPS_URL = re.compile(r"https://[^\s)>\]}\"']+")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|client[_-]?secret|private[_-]?key|token|password)\s*[:=]\s*"
    r"['\"][A-Za-z0-9_./+=-]{20,}['\"]"
)
FORBIDDEN_SHELL = {
    "eval ": "dynamic eval is forbidden",
    "set -x": "shell tracing can disclose sensitive values",
    "source <(curl": "remote process substitution is forbidden",
    "source <(wget": "remote process substitution is forbidden",
    "curl | sh": "piped remote execution is forbidden",
    "curl | bash": "piped remote execution is forbidden",
}
ARCHIVE_SUFFIXES = {".exe", ".dll", ".so", ".dylib", ".jar", ".zip", ".tar", ".tgz", ".gz"}
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh", ".tpl", ".txt", ".yaml", ".yml"}
ALLOWED_SOURCE_HOSTS = {
    "github.com",
    "helm.sh",
    "json-schema.org",
    "kubernetes.io",
    "pyyaml.org",
    "pypi.org",
    "python-jsonschema.readthedocs.io",
    "yaml.dev",
    "yaml.org",
    "yamllint.readthedocs.io",
}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def pass_check(self, message: str) -> None:
        self.checks.append(message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate yaml-specialist offline and optionally inventory read-only Git metadata."
    )
    parser.add_argument("--repo", help="Optional target worktree for read-only Git metadata discovery")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args(argv)


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def all_files(root: Path) -> set[str]:
    found: set[str] = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        try:
            mode = path.lstat().st_mode
        except OSError:
            continue
        if stat.S_ISLNK(mode) or path.is_file():
            found.add(relative)
    return found


def parse_frontmatter(audit: Audit, text: str) -> None:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        audit.error("SKILL.md: missing opening YAML frontmatter marker")
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        audit.error("SKILL.md: missing closing YAML frontmatter marker")
        return
    values: dict[str, str] = {}
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
            audit.error(f"SKILL.md:{number}: frontmatter key and value must be non-empty")
            continue
        if key in values:
            audit.error(f"SKILL.md:{number}: duplicate frontmatter key {key!r}")
        values[key] = value
    if set(values) != ALLOWED_FRONTMATTER:
        audit.error(f"SKILL.md: frontmatter keys must be exactly {sorted(ALLOWED_FRONTMATTER)}")
    if values.get("name") != "yaml-specialist":
        audit.error("SKILL.md: frontmatter name must equal yaml-specialist")
    if values.get("license") != "MIT":
        audit.error("SKILL.md: frontmatter license must equal MIT")
    description = values.get("description", "")
    if len(description) < 100 or "Use for" not in description:
        audit.error("SKILL.md: description must explain capability and activation with 'Use for'")


def markdown_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return unquote(target)


def check_markdown_links(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(text):
            target = markdown_target(raw)
            if not target or target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                if parsed.scheme != "https":
                    audit.error(f"{path.relative_to(root)}: external links must use HTTPS: {target}")
                continue
            file_part = target.split("#", 1)[0].split("?", 1)[0]
            if not file_part:
                continue
            normalized = file_part.replace("\\", "/")
            pure = PurePosixPath(normalized)
            if pure.is_absolute() or any(ord(character) < 32 or ord(character) == 127 for character in normalized):
                audit.error(f"{path.relative_to(root)}: unsafe relative link {target}")
                continue
            resolved = (path.parent / file_part).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                audit.error(f"{path.relative_to(root)}: link escapes package root: {target}")
                continue
            if not resolved.exists():
                audit.error(f"{path.relative_to(root)}: missing relative-link target {target}")
    audit.pass_check("Markdown links are package-confined and HTTPS-only externally")


def check_file_safety(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        try:
            file_stat = path.lstat()
        except OSError as exc:
            audit.error(f"{relative}: cannot inspect: {exc}")
            continue
        if stat.S_ISLNK(file_stat.st_mode):
            audit.error(f"{relative}: symlinks are not allowed")
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in ARCHIVE_SUFFIXES:
            audit.error(f"{relative}: binary or archive artifacts are not allowed")
        if file_stat.st_size > 2 * 1024 * 1024:
            audit.error(f"{relative}: package file exceeds 2 MiB")
        if relative.startswith(("scripts/", "tests/")) and path.suffix in {".py", ".sh"}:
            if not file_stat.st_mode & stat.S_IXUSR:
                audit.error(f"{relative}: package-owned script/test must be owner-executable")
    audit.pass_check("File types, sizes, symlinks, and executable modes inspected")


def check_text_hygiene(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            audit.error(f"{relative}: UTF-8 read failed: {exc}")
            continue
        if "\r" in text:
            audit.error(f"{relative}: CR characters are not allowed")
        if "\t" in text and path.suffix in {".yaml", ".yml"}:
            audit.error(f"{relative}: YAML must not contain tabs")
        if PRIVATE_KEY.search(text):
            audit.error(f"{relative}: contains a private-key marker")
        if SECRET_ASSIGNMENT.search(text):
            audit.error(f"{relative}: contains a credential-shaped literal")
        if path.suffix == ".sh":
            lowered = text.lower()
            for needle, message in FORBIDDEN_SHELL.items():
                if needle in lowered:
                    audit.error(f"{relative}: {message}")
    audit.pass_check("UTF-8, line endings, YAML tabs, secrets, and shell hazards inspected")


def run_syntax_checks(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*.py")):
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except (OSError, UnicodeError, SyntaxError) as exc:
            audit.error(f"{path.relative_to(root)}: Python syntax/read failure: {exc}")

    bash = shutil.which("bash")
    if bash is None:
        audit.error("bash is required to syntax-check bundled shell scripts")
    else:
        for path in sorted(root.rglob("*.sh")):
            completed = subprocess.run(
                [bash, "-n", str(path)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                timeout=30,
            )
            if completed.returncode != 0:
                detail = completed.stderr.strip() or f"exit {completed.returncode}"
                audit.error(f"{path.relative_to(root)}: bash syntax failure: {detail}")

    shellcheck = shutil.which("shellcheck")
    if shellcheck is None:
        audit.warn("shellcheck is unavailable; Bash syntax was checked but static shell analysis is incomplete")
    else:
        scripts = [str(path) for path in sorted(root.rglob("*.sh"))]
        completed = subprocess.run(
            [shellcheck, "-x", "--severity=warning", *scripts],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=60,
        )
        if completed.returncode != 0:
            detail = (completed.stdout + "\n" + completed.stderr).strip()
            audit.error(f"shellcheck failed: {detail}")
    audit.pass_check("Python and Bash syntax inspected")


def check_requirements(audit: Audit, root: Path) -> None:
    path = root / "scripts" / "requirements.txt"
    actual: dict[str, str] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line or line.count("==") != 1:
            audit.error(f"scripts/requirements.txt:{number}: dependency must use exact == pin")
            continue
        name, version = (part.strip() for part in line.split("==", 1))
        if not name or not version or name in actual:
            audit.error(f"scripts/requirements.txt:{number}: invalid or duplicate dependency")
            continue
        actual[name] = version
    if actual != EXPECTED_REQUIREMENTS:
        audit.error(f"scripts/requirements.txt: expected {EXPECTED_REQUIREMENTS}, found {actual}")
    for name, expected in EXPECTED_REQUIREMENTS.items():
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            audit.error(f"dependency unavailable: {name}=={expected}; install reviewed pins in an isolated environment")
            continue
        if installed != expected:
            audit.error(f"dependency drift: {name} expected {expected}, found {installed}")
    audit.pass_check("Dependency pins and installed test versions inspected")


def has_remote_ref(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str) and urlsplit(child).scheme:
                return True
            if has_remote_ref(child):
                return True
    elif isinstance(value, list):
        return any(has_remote_ref(child) for child in value)
    return False


def check_templates(audit: Audit, root: Path) -> None:
    try:
        from jsonschema import Draft202012Validator
        from ruamel.yaml import YAML
    except ImportError as exc:
        audit.error(f"template validation dependency unavailable: {exc}")
        return

    yaml = YAML(typ="safe", pure=True)
    yaml.version = (1, 2)
    yaml.allow_duplicate_keys = False
    for path in sorted((root / "templates").glob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                documents = list(yaml.load_all(handle))
        except Exception as exc:  # parser diagnostics are part of this deterministic check
            audit.error(f"{path.relative_to(root)}: YAML 1.2 parse failure: {exc}")
            continue
        if len(documents) != 1 or not isinstance(documents[0], dict):
            audit.error(f"{path.relative_to(root)}: expected one mapping document")

    contract_text = (root / "templates" / "values-contract.example.yaml").read_text(encoding="utf-8")
    for marker in ("# -- ", "@type", "@required", "@accepted", "@default", "@example", "@security"):
        if marker not in contract_text:
            audit.error(f"templates/values-contract.example.yaml: missing marker {marker!r}")

    overlay_text = (root / "templates" / "values-template.example.yaml").read_text(encoding="utf-8")
    if "# @mode active-overlay" not in overlay_text:
        audit.error("templates/values-template.example.yaml: missing '# @mode active-overlay' declaration")

    schema_path = root / "templates" / "values.schema.example.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        audit.error(f"templates/values.schema.example.json: invalid JSON: {exc}")
        return
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        audit.error("templates/values.schema.example.json: must declare Draft 2020-12")
    if has_remote_ref(schema):
        audit.error("templates/values.schema.example.json: remote $ref is forbidden")
    try:
        Draft202012Validator.check_schema(schema)
        values = yaml.load(contract_text)
        errors = sorted(Draft202012Validator(schema).iter_errors(values), key=lambda item: list(item.path))
        if errors:
            audit.error(f"template values do not satisfy bundled schema: {errors[0].message}")
    except Exception as exc:
        audit.error(f"template schema validation failed: {exc}")
    audit.pass_check("YAML examples, values metadata, and Draft 2020-12 schema inspected")


def check_entrypoint_and_sources(audit: Audit, root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    parse_frontmatter(audit, skill)
    line_count = len(skill.splitlines())
    if not 180 <= line_count <= 450:
        audit.error(f"SKILL.md: expected 180-450 lines, found {line_count}")
    required_phrases = (
        f"**Verified against upstream: {VERIFIED_DATE}.**",
        "Maximum three approved edit-and-validate passes",
        "The wrapper never installs or upgrades a release",
        "The skill never installs them automatically",
        "Mark it **incomplete**",
    )
    for phrase in required_phrases:
        if phrase not in skill:
            audit.error(f"SKILL.md: missing safety/freshness contract phrase {phrase!r}")

    sources = (root / "references" / "sources.md").read_text(encoding="utf-8")
    if f"**Last verified:** {VERIFIED_DATE}" not in sources:
        audit.error(f"references/sources.md: missing verification date {VERIFIED_DATE}")
    urls = {url.rstrip(".,;:") for url in HTTPS_URL.findall(sources)}
    if len(urls) < 30:
        audit.error(f"references/sources.md: expected at least 30 unique HTTPS URLs, found {len(urls)}")
    for url in sorted(urls):
        host = urlsplit(url).hostname
        if host not in ALLOWED_SOURCE_HOSTS:
            audit.warn(f"references/sources.md: review non-primary source host {host!r}: {url}")
    audit.pass_check("Entrypoint metadata, freshness, safety contract, and source ledger inspected")


def run_package_tests(audit: Audit, root: Path) -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["LC_ALL"] = "C"
    commands = [
        ("tests/test_yaml_specialist.py", [sys.executable, str(root / "tests" / "test_yaml_specialist.py")]),
        ("tests/test_validate_chart.sh", ["bash", str(root / "tests" / "test_validate_chart.sh")]),
    ]
    for label, command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=str(root),
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                timeout=180,
            )
        except subprocess.TimeoutExpired:
            audit.error(f"{label}: timed out after 180 seconds")
            continue
        if completed.returncode != 0:
            detail = (completed.stdout + "\n" + completed.stderr).strip()
            audit.error(f"{label}: failed: {detail}")
        else:
            audit.pass_check(f"{label}: passed")


def git_output(arguments: list[str]) -> str:
    completed = subprocess.run(
        arguments,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=15,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit {completed.returncode}"
        raise ValueError(detail)
    return completed.stdout.strip()


def discover_repository(audit: Audit, repo_input: str) -> dict[str, Any] | None:
    git = shutil.which("git")
    if git is None:
        audit.error("repository discovery: git is not installed")
        return None
    try:
        root_text = git_output([git, "-C", repo_input, "rev-parse", "--show-toplevel"])
        root = Path(root_text).resolve(strict=True)
        head = git_output([git, "-C", str(root), "rev-parse", "--verify", "HEAD"])
        try:
            branch = git_output([git, "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"])
        except ValueError:
            branch = "(detached)"
        status = git_output([git, "-C", str(root), "status", "--porcelain=v1", "--untracked-files=normal"])
        tracked = git_output([git, "-C", str(root), "ls-files", "-z"])
    except (OSError, ValueError) as exc:
        audit.error(f"repository discovery: {exc}")
        return None
    entries = [entry for entry in status.splitlines() if entry]
    return {
        "root": str(root),
        "head": head,
        "branch": branch,
        "dirty": bool(entries),
        "status_entries": len(entries),
        "tracked_files": 0 if not tracked else tracked.count("\0"),
        "content_read": False,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = package_root()
    audit = Audit()

    actual = all_files(root)
    missing = sorted(EXPECTED_FILES - actual)
    extra = sorted(actual - EXPECTED_FILES)
    for relative in missing:
        audit.error(f"missing expected package file: {relative}")
    for relative in extra:
        audit.error(f"unexpected package file: {relative}")
    if not missing and not extra:
        audit.pass_check(f"Exact package inventory verified ({len(EXPECTED_FILES)} files)")

    check_file_safety(audit, root)
    check_text_hygiene(audit, root)
    run_syntax_checks(audit, root)
    check_markdown_links(audit, root)
    check_entrypoint_and_sources(audit, root)
    check_requirements(audit, root)
    check_templates(audit, root)
    run_package_tests(audit, root)

    repository = discover_repository(audit, args.repo) if args.repo else None
    result = {
        "status": "failed" if audit.errors else ("warning" if audit.warnings else "passed"),
        "package": "yaml-specialist",
        "verified_date": VERIFIED_DATE,
        "files": len(actual),
        "checks": audit.checks,
        "errors": audit.errors,
        "warnings": audit.warnings,
        "repository": repository,
        "network_used": False,
        "cluster_used": False,
        "target_content_read": False,
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"yaml-specialist self-check: {result['status']}")
        print(f"files: {len(actual)}; checks: {len(audit.checks)}; errors: {len(audit.errors)}; warnings: {len(audit.warnings)}")
        for message in audit.errors:
            print(f"ERROR: {message}")
        for message in audit.warnings:
            print(f"WARNING: {message}")
        if repository is not None:
            print(
                "repository: "
                f"branch={repository['branch']} head={repository['head']} "
                f"dirty={repository['dirty']} status_entries={repository['status_entries']} "
                f"tracked_files={repository['tracked_files']} content_read=false"
            )

    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
