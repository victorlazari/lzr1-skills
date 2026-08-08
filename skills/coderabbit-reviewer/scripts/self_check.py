#!/usr/bin/env python3
"""Validate coderabbit-reviewer locally without network access or target execution.

The self-check never authenticates, starts a CodeRabbit review, installs software,
changes Git state, executes project code, or reads file contents from the target
repository. Optional repository discovery runs only read-only Git metadata commands.
"""

from __future__ import annotations

import argparse
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
    "references/agent-events.md",
    "references/agent-integration.md",
    "references/ci-pr-relationship.md",
    "references/cli-commands.md",
    "references/configuration.md",
    "references/findings-triage.md",
    "references/headless-auth.md",
    "references/remediation-loop.md",
    "references/sources.md",
    "references/troubleshooting.md",
    "scripts/install-coderabbit.sh",
    "scripts/run-review.sh",
    "scripts/self_check.py",
    "scripts/validate_findings.py",
    "templates/coderabbit.example.yaml",
    "templates/review-report.md",
    "tests/fixtures/complete.ndjson",
    "tests/fixtures/error.ndjson",
    "tests/fixtures/malformed.ndjson",
    "tests/fixtures/post-terminal.ndjson",
    "tests/fixtures/skipped.ndjson",
    "tests/fixtures/unknown-event.ndjson",
    "tests/test_validate_findings.py",
    "tests/test_wrappers.sh",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTTPS_URL = re.compile(r"https://[^\s)>\]}\"']+")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_./+=-]{20,}['\"]"
)
FORBIDDEN_SHELL = {
    "eval ": "dynamic eval is forbidden",
    "set -x": "shell tracing can disclose credentials",
    "source <(curl": "remote process substitution is forbidden",
    "source <(wget": "remote process substitution is forbidden",
}
ARCHIVE_SUFFIXES = {".exe", ".dll", ".so", ".dylib", ".jar", ".zip", ".tar", ".tgz", ".gz"}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


class Discovery:
    def __init__(self) -> None:
        self.repository: dict[str, Any] | None = None
        self.cli: dict[str, Any] = {}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate coderabbit-reviewer and optionally inventory Git metadata without network access."
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
    if values.get("name") != "coderabbit-reviewer":
        audit.error("SKILL.md: frontmatter name must equal coderabbit-reviewer")
    if values.get("license") != "MIT":
        audit.error("SKILL.md: frontmatter license must equal MIT")
    if not values.get("description", "").strip():
        audit.error("SKILL.md: description must be non-empty")


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
        if path.is_file():
            if path.suffix.lower() in ARCHIVE_SUFFIXES:
                audit.error(f"{relative}: binary or archive artifacts are not allowed")
            if file_stat.st_size > 2 * 1024 * 1024:
                audit.error(f"{relative}: package file exceeds 2 MiB")
            if relative.startswith(("scripts/", "tests/")) and path.suffix in {".py", ".sh"}:
                if not file_stat.st_mode & stat.S_IXUSR:
                    audit.error(f"{relative}: package-owned script must be owner-executable")


def check_text_hygiene(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".sh", ".yaml", ".yml", ".ndjson"}:
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
            for needle, message in FORBIDDEN_SHELL.items():
                if needle in text:
                    audit.error(f"{relative}: {message}")


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
            )
            if completed.returncode != 0:
                detail = completed.stderr.strip() or f"exit {completed.returncode}"
                audit.error(f"{path.relative_to(root)}: bash syntax failure: {detail}")


def check_template(audit: Audit, root: Path) -> None:
    path = root / "templates" / "coderabbit.example.yaml"
    text = path.read_text(encoding="utf-8")
    required = {
        "$schema=https://www.coderabbit.ai/integrations/schema.v2.json": "current schema declaration",
        "early_access: false": "early-access disabled",
        "inheritance: false": "inheritance disabled by default",
        "request_changes_workflow: false": "automatic request-change workflow disabled",
        "path_filters: []": "no silent path exclusions",
        "path_instructions: []": "no unreviewed prompt instructions",
    }
    for needle, description in required.items():
        if needle not in text:
            audit.error(f"templates/coderabbit.example.yaml: missing {description}")
    if re.search(r"(?m)^\s*early_access:\s*true\s*$", text):
        audit.error("templates/coderabbit.example.yaml: early_access must not be enabled")


def check_entrypoint_and_sources(audit: Audit, root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    parse_frontmatter(audit, skill)
    line_count = len(skill.splitlines())
    if not 140 <= line_count <= 400:
        audit.error(f"SKILL.md: expected 140-400 lines, found {line_count}")
    if f"**Verified against upstream: {VERIFIED_DATE}**" not in skill:
        audit.error(f"SKILL.md: missing verification date {VERIFIED_DATE}")
    for phrase in (
        "never invokes `cr skills` automatically",
        "default ceiling is three review passes",
        "No commit, push, pull-request action",
    ):
        if phrase not in skill:
            audit.error(f"SKILL.md: missing safety contract phrase {phrase!r}")

    sources = (root / "references" / "sources.md").read_text(encoding="utf-8")
    if f"**Research cutoff:** {VERIFIED_DATE}" not in sources:
        audit.error(f"references/sources.md: missing research cutoff {VERIFIED_DATE}")
    urls = {url.rstrip(".,;:") for url in HTTPS_URL.findall(sources)}
    if len(urls) < 12:
        audit.error(f"references/sources.md: expected at least 12 unique HTTPS URLs, found {len(urls)}")
    allowed_hosts = {"docs.coderabbit.ai", "www.coderabbit.ai", "cli.coderabbit.ai", "agentskills.io", "github.com"}
    for url in sorted(urls):
        host = urlsplit(url).hostname
        if host not in allowed_hosts:
            audit.warn(f"references/sources.md: review non-primary source host {host!r}: {url}")


def run_unit_tests(audit: Audit, root: Path) -> None:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = [
        ("tests/test_validate_findings.py", [sys.executable, str(root / "tests" / "test_validate_findings.py")]),
        ("tests/test_wrappers.sh", ["bash", str(root / "tests" / "test_wrappers.sh")]),
    ]
    for label, command in commands:
        completed = subprocess.run(
            command,
            cwd=str(root),
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=60,
        )
        if completed.returncode != 0:
            detail = (completed.stdout + "\n" + completed.stderr).strip()
            audit.error(f"{label}: failed: {detail}")


def git_output(arguments: list[str]) -> str:
    completed = subprocess.run(
        arguments,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=15,
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
        branch = git_output([git, "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"])
    except ValueError as exc:
        # Detached HEAD makes symbolic-ref fail; recover it without changing state.
        try:
            root_text = git_output([git, "-C", repo_input, "rev-parse", "--show-toplevel"])
            root = Path(root_text).resolve(strict=True)
            head = git_output([git, "-C", str(root), "rev-parse", "--verify", "HEAD"])
            branch = "(detached)"
        except (OSError, ValueError) as nested:
            audit.error(f"repository discovery: {exc}; {nested}")
            return None
    except OSError as exc:
        audit.error(f"repository discovery: {exc}")
        return None

    try:
        status_text = git_output([git, "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"])
        common_dir = git_output([git, "-C", str(root), "rev-parse", "--git-common-dir"])
        remote_names_text = git_output([git, "-C", str(root), "remote"])
    except (OSError, ValueError) as exc:
        audit.error(f"repository discovery: metadata command failed: {exc}")
        return None

    staged = 0
    unstaged = 0
    untracked = 0
    conflicted = 0
    for line in status_text.splitlines():
        if line.startswith("??"):
            untracked += 1
            continue
        if len(line) < 2:
            continue
        index_state, worktree_state = line[0], line[1]
        if index_state not in {" ", "?", "!"}:
            staged += 1
        if worktree_state not in {" ", "?", "!"}:
            unstaged += 1
        if index_state == "U" or worktree_state == "U" or (index_state, worktree_state) in {
            ("A", "A"), ("D", "D"), ("A", "U"), ("U", "D"), ("D", "U"), ("U", "A")
        }:
            conflicted += 1

    return {
        "root": str(root),
        "head": head,
        "branch": branch,
        "staged_entries": staged,
        "unstaged_entries": unstaged,
        "untracked_entries": untracked,
        "conflicted_entries": conflicted,
        "has_gitmodules": (root / ".gitmodules").is_file(),
        "git_common_dir": common_dir,
        "remote_names": remote_names_text.splitlines() if remote_names_text else [],
        "note": "Counts are metadata only; file contents and remote URLs were not read.",
    }


def discover_cli() -> dict[str, Any]:
    path_text = shutil.which("coderabbit") or shutil.which("cr")
    if path_text is None:
        return {"found": False, "note": "No command was executed."}
    path = Path(path_text)
    try:
        resolved = str(path.resolve(strict=True))
    except OSError:
        resolved = str(path)
    return {
        "found": True,
        "entrypoint": path_text,
        "resolved_path": resolved,
        "note": "The executable was located but not invoked; version, auth, and connectivity remain unverified.",
    }


def run(root: Path, repo_input: str | None) -> tuple[Audit, Discovery]:
    audit = Audit()
    discovery = Discovery()
    found = all_files(root)
    for item in sorted(EXPECTED_FILES - found):
        audit.error(f"missing required file: {item}")
    for item in sorted(found - EXPECTED_FILES):
        audit.error(f"unexpected package file: {item}")
    if EXPECTED_FILES - found:
        return audit, discovery

    check_file_safety(audit, root)
    check_text_hygiene(audit, root)
    check_entrypoint_and_sources(audit, root)
    check_markdown_links(audit, root)
    run_syntax_checks(audit, root)
    check_template(audit, root)
    run_unit_tests(audit, root)
    discovery.cli = discover_cli()
    if repo_input is not None:
        discovery.repository = discover_repository(audit, repo_input)
    return audit, discovery


def emit(audit: Audit, discovery: Discovery, *, json_output: bool) -> None:
    payload = {
        "valid": not audit.errors,
        "errors": audit.errors,
        "warnings": audit.warnings,
        "package": "coderabbit-reviewer",
        "verified_against_upstream": VERIFIED_DATE,
        "discovery": {"cli": discovery.cli, "repository": discovery.repository},
        "limitations": [
            "No network, authentication, installation, configuration-schema request, or CodeRabbit review was performed.",
            "Package validity does not establish target-code correctness, security, or review coverage.",
        ],
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
    print(f"CodeRabbit CLI found: {discovery.cli.get('found', False)} (not executed)")
    if discovery.repository is not None:
        repository = discovery.repository
        print(
            "Repository: "
            f"{repository['root']} @ {repository['head']} "
            f"({repository['staged_entries']} staged, {repository['unstaged_entries']} unstaged, "
            f"{repository['untracked_entries']} untracked, {repository['conflicted_entries']} conflicted)"
        )
    print("No network request, target-code execution, installation, authentication, or review was performed.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    audit, discovery = run(package_root(), args.repo)
    emit(audit, discovery, json_output=args.json)
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
