#!/usr/bin/env python3
"""Run deterministic, local checks against the security-review skill package.

The self-check never scans a user repository, accesses the network, installs
software, or executes the synthetic vulnerable fixture.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

# The self-check must not mutate the package while importing its local validator.
sys.dont_write_bytecode = True

EXPECTED_FILES = {
    "SKILL.md",
    "references/ai-llm-agentic.md",
    "references/application-api.md",
    "references/auth-identity.md",
    "references/business-logic-distributed.md",
    "references/cloud-container-iac.md",
    "references/logging-privacy.md",
    "references/mobile-client.md",
    "references/remediation-validation.md",
    "references/scoring-prioritization.md",
    "references/secrets-cryptography.md",
    "references/sources.md",
    "references/supply-chain-build.md",
    "references/threat-modeling-evidence.md",
    "scripts/inventory.py",
    "scripts/self_check.py",
    "scripts/validate_report.py",
    "templates/finding.schema.json",
    "templates/security-report.md",
    "tests/expected-findings.json",
    "tests/fixtures/README.md",
    "tests/fixtures/vulnerable_sample.py",
}
ALLOWED_FRONTMATTER = {"name", "description", "license"}
VERIFIED_DATE = "2026-08-07"
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTTPS_URL = re.compile(r"https://[^\s)>\]}]+")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
TOKEN_SHAPE = re.compile(r"(?i)(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][A-Za-z0-9_./+=-]{20,}['\"]")


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate this security-review skill package without network access.")
    parser.add_argument("--json-output", action="store_true", help="Emit JSON results")
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
        if stat.S_ISLNK(mode):
            found.add(relative)
        elif path.is_file():
            found.add(relative)
    return found


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
            audit.error(f"SKILL.md:{number}: frontmatter key and value must be non-empty")
            continue
        if key in result:
            audit.error(f"SKILL.md:{number}: duplicate frontmatter key {key!r}")
        result[key] = value
    if set(result) != ALLOWED_FRONTMATTER:
        audit.error(f"SKILL.md: frontmatter keys must be exactly {sorted(ALLOWED_FRONTMATTER)}")
    if result.get("name") != "security-review":
        audit.error("SKILL.md: frontmatter name must equal security-review")
    if not result.get("description", "").strip():
        audit.error("SKILL.md: frontmatter description must be non-empty")
    if result.get("license") != "MIT":
        audit.error("SKILL.md: frontmatter license must equal MIT")
    return result


def target_from_markdown(raw: str) -> str:
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
            target = target_from_markdown(raw)
            if not target or target.startswith("#"):
                continue
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("//"):
                if parsed.scheme == "http":
                    audit.warn(f"{path.relative_to(root)}: non-HTTPS external link {target}")
                continue
            file_part = target.split("#", 1)[0].split("?", 1)[0]
            if not file_part:
                continue
            normalized = file_part.replace("\\", "/")
            pure = PurePosixPath(normalized)
            if pure.is_absolute() or any(ord(ch) < 32 or ord(ch) == 127 for ch in normalized):
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


def check_python(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*.py")):
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
        except (OSError, UnicodeError, SyntaxError) as exc:
            audit.error(f"{path.relative_to(root)}: Python syntax/read failure: {exc}")


def check_json(audit: Audit, root: Path) -> dict[str, object]:
    loaded: dict[str, object] = {}
    for path in sorted(root.rglob("*.json")):
        relative = path.relative_to(root).as_posix()
        try:
            loaded[relative] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            audit.error(f"{relative}: invalid JSON: {exc}")
    schema = loaded.get("templates/finding.schema.json")
    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        audit.error("templates/finding.schema.json: must declare JSON Schema draft 2020-12")
    return loaded


def load_validator(audit: Audit, root: Path):
    validator_path = root / "scripts" / "validate_report.py"
    spec = importlib.util.spec_from_file_location("security_review_validate_report", validator_path)
    if spec is None or spec.loader is None:
        audit.error("scripts/validate_report.py: cannot create import specification")
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # The package file is trusted input to its own self-check.
        audit.error(f"scripts/validate_report.py: import failed: {type(exc).__name__}: {exc}")
        return None
    return module


def check_expected_report(audit: Audit, root: Path, loaded: dict[str, object]) -> None:
    expected = loaded.get("tests/expected-findings.json")
    if expected is None:
        return
    module = load_validator(audit, root)
    if module is None:
        return
    try:
        result = module.validate_report(expected, final=True)
    except Exception as exc:
        audit.error(f"tests/expected-findings.json: validator raised {type(exc).__name__}: {exc}")
        return
    for error in getattr(result, "errors", ["validator returned no errors field"]):
        audit.error(f"tests/expected-findings.json: {error}")
    for warning in getattr(result, "warnings", []):
        audit.warn(f"tests/expected-findings.json: {warning}")


def check_sources(audit: Audit, root: Path) -> None:
    path = root / "references" / "sources.md"
    text = path.read_text(encoding="utf-8")
    if f"Verified against upstream: {VERIFIED_DATE}" not in text:
        audit.error(f"references/sources.md: missing exact verification date {VERIFIED_DATE}")
    urls = {url.rstrip(".,;:") for url in HTTPS_URL.findall(text)}
    hosts = {urlsplit(url).hostname for url in urls if urlsplit(url).hostname}
    if len(urls) < 25:
        audit.error(f"references/sources.md: expected at least 25 unique HTTPS sources, found {len(urls)}")
    if len(hosts) < 15:
        audit.error(f"references/sources.md: expected at least 15 unique authoritative hosts, found {len(hosts)}")


def check_fixture_hygiene(audit: Audit, root: Path) -> None:
    fixture = root / "tests" / "fixtures" / "vulnerable_sample.py"
    text = fixture.read_text(encoding="utf-8")
    if PRIVATE_KEY.search(text):
        audit.error("tests/fixtures/vulnerable_sample.py: must not contain a private-key block")
    for match in TOKEN_SHAPE.finditer(text):
        value = match.group(0)
        if "DEMO_" not in value and "EXAMPLE_" not in value and "NOT_A_REAL_" not in value:
            audit.error("tests/fixtures/vulnerable_sample.py: secret-shaped fixture value lacks an explicit non-secret marker")
    if "DO NOT EXECUTE" not in text:
        audit.error("tests/fixtures/vulnerable_sample.py: must state DO NOT EXECUTE")


def check_file_safety(audit: Audit, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        try:
            mode = path.lstat().st_mode
        except OSError as exc:
            audit.error(f"{path.relative_to(root)}: cannot lstat: {exc}")
            continue
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            audit.error(f"{relative}: symlinks are not allowed in this package")
        if path.is_file() and path.suffix.lower() in {".exe", ".dll", ".so", ".dylib", ".jar", ".zip", ".tar", ".tgz", ".gz"}:
            audit.error(f"{relative}: executable or archive artifact is not allowed")


def run(root: Path) -> Audit:
    audit = Audit()
    found = all_files(root)
    missing = sorted(EXPECTED_FILES - found)
    unexpected = sorted(found - EXPECTED_FILES)
    for item in missing:
        audit.error(f"missing required file: {item}")
    for item in unexpected:
        audit.error(f"unexpected package file: {item}")
    if missing:
        return audit

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
    parse_frontmatter(audit, skill_text)
    line_count = len(skill_text.splitlines())
    if not 240 <= line_count <= 520:
        audit.error(f"SKILL.md: expected 240-520 lines for the advanced entrypoint, found {line_count}")
    if f"Verified against upstream: {VERIFIED_DATE}" not in skill_text:
        audit.error(f"SKILL.md: missing exact verification date {VERIFIED_DATE}")

    check_file_safety(audit, root)
    check_markdown_links(audit, root)
    loaded = check_json(audit, root)
    check_python(audit, root)
    check_sources(audit, root)
    check_fixture_hygiene(audit, root)
    check_expected_report(audit, root, loaded)
    return audit


def emit(audit: Audit, *, json_output: bool) -> None:
    payload = {"valid": not audit.errors, "errors": audit.errors, "warnings": audit.warnings}
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    state = "PASS" if not audit.errors else "FAIL"
    print(f"{state}: {len(audit.errors)} error(s), {len(audit.warnings)} warning(s)")
    for error in audit.errors:
        print(f"ERROR: {error}")
    for warning in audit.warnings:
        print(f"WARNING: {warning}")
    print("This validates package integrity and report structure, not target security.")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    audit = run(package_root())
    emit(audit, json_output=args.json_output)
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
