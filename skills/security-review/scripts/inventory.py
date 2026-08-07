#!/usr/bin/env python3
"""Create a read-only metadata inventory for a security review.

The helper never opens regular files, follows symlinks, executes target code, or
uses the network. It classifies directory entries from paths and lstat metadata
only. Its output is a scope seed, not a security finding.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

VERSION = 1
DEFAULT_MAX_ENTRIES = 200_000
VCS_DIRS = {".git", ".hg", ".svn"}
VENDORED_SEGMENTS = {
    "node_modules",
    "vendor",
    "vendors",
    "third_party",
    "third-party",
    "Pods",
    ".venv",
    "venv",
}
GENERATED_SEGMENTS = {
    "dist",
    "build",
    "coverage",
    "generated",
    "gen",
    ".next",
    ".nuxt",
    "target",
}
SOURCE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".cxx", ".dart", ".ex", ".exs", ".fs",
    ".fsx", ".go", ".groovy", ".h", ".hpp", ".java", ".js", ".jsx",
    ".kt", ".kts", ".lua", ".m", ".mm", ".php", ".pl", ".pm", ".py",
    ".r", ".rb", ".rs", ".scala", ".sh", ".sol", ".swift", ".ts", ".tsx",
    ".vue", ".zig",
}
CONFIG_EXTENSIONS = {".conf", ".config", ".env", ".ini", ".json", ".properties", ".toml", ".xml", ".yaml", ".yml"}
DOC_EXTENSIONS = {".adoc", ".md", ".mdx", ".rst", ".txt"}
ARCHIVE_EXTENSIONS = {".7z", ".bz2", ".gz", ".jar", ".rar", ".tar", ".tgz", ".war", ".xz", ".zip"}
BINARY_EXTENSIONS = {".a", ".apk", ".bin", ".class", ".dll", ".dylib", ".elf", ".exe", ".o", ".obj", ".pdf", ".so", ".wasm"}
MEDIA_EXTENSIONS = {".avif", ".gif", ".ico", ".jpeg", ".jpg", ".mov", ".mp3", ".mp4", ".png", ".svg", ".webm", ".webp", ".wav"}
LOCKFILES = {
    "bun.lock", "bun.lockb", "composer.lock", "deno.lock", "flake.lock",
    "gemfile.lock", "go.sum", "gradle.lockfile", "mix.lock", "package-lock.json",
    "packages.lock.json", "pnpm-lock.yaml", "poetry.lock", "pubspec.lock",
    "requirements.lock", "uv.lock", "yarn.lock",
}
MANIFESTS = {
    "build.gradle", "build.gradle.kts", "cargo.toml", "composer.json", "deno.json",
    "deno.jsonc", "flake.nix", "gemfile", "go.mod", "mix.exs", "package.json",
    "pom.xml", "pubspec.yaml", "pyproject.toml", "requirements.txt", "setup.cfg",
    "setup.py",
}
BUILD_FILES = {
    "dockerfile", "jenkinsfile", "makefile", "rakefile", "taskfile.yml",
    "taskfile.yaml", "justfile",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory paths and lstat metadata without reading file contents, "
            "following symlinks, executing target code, or using the network."
        )
    )
    parser.add_argument("root", nargs="?", default=".", help="Directory to inventory (default: current directory)")
    parser.add_argument("--output", "-o", default="-", help="Output JSON path, or - for stdout")
    parser.add_argument(
        "--max-entries",
        type=int,
        default=DEFAULT_MAX_ENTRIES,
        help=f"Stop after this many entries (default: {DEFAULT_MAX_ENTRIES})",
    )
    parser.add_argument(
        "--include-vcs-internals",
        action="store_true",
        help="Traverse VCS metadata directories; disabled by default and recorded as pruned",
    )
    parser.add_argument(
        "--allow-filesystem-root",
        action="store_true",
        help="Permit inventorying the filesystem root; rejected by default",
    )
    return parser.parse_args(argv)


def relative_posix(path: Path, root: Path) -> str:
    return PurePosixPath(path.relative_to(root).as_posix()).as_posix()


def classify(relative: str, is_directory: bool) -> tuple[str, bool, bool]:
    pure = PurePosixPath(relative)
    parts = set(pure.parts)
    lowered_parts = {part.lower() for part in pure.parts}
    name = pure.name.lower()
    suffix = pure.suffix.lower()
    vendored = bool(parts & VENDORED_SEGMENTS or lowered_parts & {item.lower() for item in VENDORED_SEGMENTS})
    generated = bool(lowered_parts & {item.lower() for item in GENERATED_SEGMENTS})

    if is_directory:
        category = "directory"
    elif name in LOCKFILES:
        category = "dependency-lockfile"
    elif name in MANIFESTS:
        category = "dependency-manifest"
    elif ".github" in lowered_parts and "workflows" in lowered_parts:
        category = "ci-workflow"
    elif name in BUILD_FILES or name.startswith("dockerfile"):
        category = "build-or-container-definition"
    elif any(part in lowered_parts for part in {"migrations", "migration", "schema", "seeds"}):
        category = "database-schema-or-migration"
    elif any(part in lowered_parts for part in {"terraform", "cloudformation", "kubernetes", "k8s", "helm", "pulumi", "ansible"}):
        category = "infrastructure-as-code"
    elif any(part in lowered_parts for part in {"android", "ios", "mobile", "appclip", "watchos"}):
        category = "mobile-or-client"
    elif any(part in lowered_parts for part in {"prompts", "models", "retrieval", "rag", "agents", "mcp", "evals", "evaluations"}):
        category = "ai-or-agentic"
    elif any(part in lowered_parts for part in {"test", "tests", "spec", "specs", "__tests__", "fixtures", "fuzz"}):
        category = "test-or-fixture"
    elif suffix in SOURCE_EXTENSIONS:
        category = "source"
    elif suffix in CONFIG_EXTENSIONS or name.startswith(".env"):
        category = "configuration"
    elif suffix in DOC_EXTENSIONS:
        category = "documentation"
    elif suffix in ARCHIVE_EXTENSIONS:
        category = "archive-opaque"
    elif suffix in BINARY_EXTENSIONS:
        category = "binary-opaque"
    elif suffix in MEDIA_EXTENSIONS:
        category = "media-opaque"
    else:
        category = "unclassified"
    return category, generated, vendored


def entry_record(path: Path, root: Path) -> dict[str, Any]:
    info = path.lstat()
    mode = info.st_mode
    is_link = stat.S_ISLNK(mode)
    is_directory = stat.S_ISDIR(mode)
    kind = (
        "symlink" if is_link else
        "directory" if is_directory else
        "regular-file" if stat.S_ISREG(mode) else
        "special"
    )
    relative = relative_posix(path, root)
    category, generated, vendored = classify(relative, is_directory)
    return {
        "path": relative,
        "kind": kind,
        "category": category,
        "size_bytes": info.st_size if stat.S_ISREG(mode) else None,
        "executable": bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)),
        "generated_hint": generated,
        "vendored_hint": vendored,
        "coverage_state": "mechanically_inventoried",
        "content_read": False,
        "symlink_followed": False,
    }


def scan(root: Path, max_entries: int, include_vcs: bool) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    pruned: list[dict[str, str]] = []
    stack = [root]
    truncated = False

    while stack:
        directory = stack.pop()
        try:
            children = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            rel = "." if directory == root else relative_posix(directory, root)
            errors.append({"path": rel, "error": f"{type(exc).__name__}: {exc.strerror or str(exc)}"})
            continue

        child_directories: list[Path] = []
        for child in children:
            if len(entries) >= max_entries:
                truncated = True
                stack.clear()
                break
            path = Path(child.path)
            try:
                record = entry_record(path, root)
            except OSError as exc:
                relative = PurePosixPath(path.relative_to(root).as_posix()).as_posix()
                errors.append({"path": relative, "error": f"{type(exc).__name__}: {exc.strerror or str(exc)}"})
                continue
            entries.append(record)
            if record["kind"] == "directory":
                if not include_vcs and child.name in VCS_DIRS:
                    pruned.append({"path": record["path"], "reason": "VCS internals excluded by default"})
                else:
                    child_directories.append(path)
        stack.extend(reversed(child_directories))

    counts: dict[str, int] = {}
    for entry in entries:
        category = str(entry["category"])
        counts[category] = counts.get(category, 0) + 1
    return {
        "schema_version": VERSION,
        "root": str(root),
        "contract": {
            "read_file_contents": False,
            "follow_symlinks": False,
            "execute_target_code": False,
            "network_access": False,
            "security_conclusions": False,
        },
        "summary": {
            "entries": len(entries),
            "categories": dict(sorted(counts.items())),
            "errors": len(errors),
            "pruned": len(pruned),
            "truncated": truncated,
        },
        "entries": entries,
        "pruned": pruned,
        "errors": errors,
    }


def write_json(payload: dict[str, Any], destination: str) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if destination == "-":
        sys.stdout.write(text)
        return
    output = Path(destination).expanduser()
    if output.exists() and output.is_dir():
        raise ValueError("output path is a directory")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(text)
    os.replace(temporary, output)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.max_entries < 1:
        print("error: --max-entries must be positive", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser()
    try:
        root = root.resolve(strict=True)
    except OSError as exc:
        print(f"error: cannot resolve root: {exc}", file=sys.stderr)
        return 2
    if not root.is_dir() or root.is_symlink():
        print("error: root must be a real directory, not a file or symlink", file=sys.stderr)
        return 2
    if root == Path(root.anchor) and not args.allow_filesystem_root:
        print("error: refusing to inventory the filesystem root without --allow-filesystem-root", file=sys.stderr)
        return 2

    payload = scan(root, args.max_entries, args.include_vcs_internals)
    try:
        write_json(payload, args.output)
    except (OSError, ValueError) as exc:
        print(f"error: cannot write inventory: {exc}", file=sys.stderr)
        return 2
    return 3 if payload["summary"]["truncated"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
