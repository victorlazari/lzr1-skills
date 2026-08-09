#!/usr/bin/env python3
"""Offline, read-only Hermes Agent deployment preflight.

This analyzer deliberately does not import Hermes, execute subprocesses, access the
network, follow symlinks, or mutate the selected Hermes home. It implements a
conservative scalar-path scan rather than a complete YAML parser. Findings are
heuristics that require operator review; a clean report is not proof of security.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
MAX_FILE_BYTES = 1024 * 1024
KNOWN_FILES = ("config.yaml", ".env", "auth.json")
STATE_DIRECTORIES = (
    "memories",
    "skills",
    "cron",
    "sessions",
    "logs",
    "plugins",
)
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
SECRET_KEY_RE = re.compile(
    r"(?:^|[._-])(?:api[_-]?key|token|secret|password|passwd|credential|private[_-]?key|client[_-]?secret)(?:$|[._-])",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERNS = (
    re.compile(r"^sk-[A-Za-z0-9_-]{12,}$"),
    re.compile(r"^gh[pousr]_[A-Za-z0-9]{20,}$"),
    re.compile(r"^xox[baprs]-[A-Za-z0-9-]{12,}$"),
    re.compile(r"^[A-Za-z0-9+/]{32,}={0,2}$"),
)
ENV_SUB_RE = re.compile(r"^\$\{(?:env:)?[A-Za-z_][A-Za-z0-9_]*\}$")
PLACEHOLDER_RE = re.compile(
    r"(?:replace|placeholder|example|change[-_ ]?me|your[-_ ]|insert|dummy|not[-_ ]?set)",
    re.IGNORECASE,
)
TRUE_VALUES = {"1", "true", "yes", "on", "enabled"}
FALSE_VALUES = {"0", "false", "no", "off", "disabled", ""}
LOOPBACK_VALUES = {"127.0.0.1", "localhost", "::1", "[::1]"}
SANDBOX_BACKENDS = {
    "docker",
    "ssh",
    "modal",
    "daytona",
    "vercel_sandbox",
    "singularity",
}


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    title: str
    evidence: str
    detail: str
    remediation: str

    def as_dict(self) -> dict[str, str]:
        return {
            "id": self.finding_id,
            "severity": self.severity,
            "title": self.title,
            "evidence": self.evidence,
            "detail": self.detail,
            "remediation": self.remediation,
        }


@dataclass(frozen=True)
class Scalar:
    path: str
    value: str
    line: int
    kind: str


class Analyzer:
    def __init__(
        self,
        hermes_home: Path,
        deployment: str,
        input_trust: str,
        strict: bool,
    ) -> None:
        self.home = hermes_home
        self.deployment = deployment
        self.input_trust = input_trust
        self.strict = strict
        self.findings: list[Finding] = []
        self.config_scalars: dict[str, Scalar] = {}
        self.config_paths: set[str] = set()
        self.env_metadata: dict[str, dict[str, Any]] = {}
        self.auth_metadata: dict[str, Any] = {"present": False}
        self.state_metadata: dict[str, dict[str, Any]] = {}
        self.files_checked: list[str] = []

    def add(
        self,
        finding_id: str,
        severity: str,
        title: str,
        evidence: str,
        detail: str,
        remediation: str,
    ) -> None:
        self.findings.append(
            Finding(finding_id, severity, title, evidence, detail, remediation)
        )

    def analyze(self) -> dict[str, Any]:
        if not self._validate_root():
            return self._result()

        config_text = self._safe_read("config.yaml", required=True, sensitive=False)
        env_text = self._safe_read(".env", required=False, sensitive=True)
        auth_text = self._safe_read("auth.json", required=False, sensitive=True)
        self._inspect_state_directories()

        if config_text is not None:
            self._scan_config(config_text)
            self._analyze_config()
        if env_text is not None:
            self._scan_env(env_text)
        if auth_text is not None:
            self._scan_auth(auth_text)

        self._analyze_runtime_posture()
        self._analyze_api_server()
        self._analyze_env_controls()
        return self._result()

    def _validate_root(self) -> bool:
        evidence = str(self.home)
        try:
            root_stat = os.lstat(self.home)
        except FileNotFoundError:
            self.add(
                "HERMES-HOME-001",
                "error",
                "Hermes home does not exist",
                evidence,
                "The selected Hermes home could not be inspected.",
                "Confirm the intended profile/home or initialize it through a reviewed setup workflow.",
            )
            return False
        except OSError as exc:
            self.add(
                "HERMES-HOME-002",
                "error",
                "Hermes home is not inspectable",
                evidence,
                f"The selected path could not be inspected ({exc.__class__.__name__}).",
                "Correct ownership or path selection without broadening permissions unnecessarily.",
            )
            return False

        if stat.S_ISLNK(root_stat.st_mode):
            self.add(
                "HERMES-HOME-003",
                "error",
                "Symlinked Hermes home rejected",
                evidence,
                "The selected root is a symbolic link; the analyzer will not follow it.",
                "Select the canonical, non-symlinked Hermes home and verify its ownership.",
            )
            return False
        if not stat.S_ISDIR(root_stat.st_mode):
            self.add(
                "HERMES-HOME-004",
                "error",
                "Hermes home is not a directory",
                evidence,
                "The selected root is not a regular directory.",
                "Select the intended non-symlinked Hermes home directory.",
            )
            return False
        return True

    def _safe_read(self, name: str, required: bool, sensitive: bool) -> str | None:
        path = self.home / name
        evidence = name
        try:
            item_stat = os.lstat(path)
        except FileNotFoundError:
            if required:
                self.add(
                    "HERMES-FILE-001",
                    "error",
                    "Required configuration file is missing",
                    evidence,
                    "The expected configuration file was not found.",
                    "Confirm the selected profile/home and create configuration through a reviewed workflow.",
                )
            return None
        except OSError as exc:
            self.add(
                "HERMES-FILE-002",
                "error",
                "Known file is not inspectable",
                evidence,
                f"Metadata inspection failed ({exc.__class__.__name__}).",
                "Correct the path or ownership without weakening unrelated permissions.",
            )
            return None

        self.files_checked.append(name)
        if stat.S_ISLNK(item_stat.st_mode):
            self.add(
                "HERMES-FILE-003",
                "error",
                "Symlinked state file rejected",
                evidence,
                "A known Hermes file is a symbolic link; the analyzer will not follow it.",
                "Replace it with an owned regular file after reviewing the target and data flow.",
            )
            return None
        if not stat.S_ISREG(item_stat.st_mode):
            self.add(
                "HERMES-FILE-004",
                "error",
                "Unsafe state-file type",
                evidence,
                "A known Hermes file is not a regular file.",
                "Use an owned regular file and investigate the unexpected file type.",
            )
            return None
        if item_stat.st_size > MAX_FILE_BYTES:
            self.add(
                "HERMES-FILE-005",
                "error",
                "State file exceeds inspection limit",
                evidence,
                f"The file is larger than the {MAX_FILE_BYTES}-byte offline inspection cap.",
                "Inspect the unexpected growth separately and provide a bounded reviewed copy if needed.",
            )
            return None
        if sensitive and os.name == "posix" and stat.S_IMODE(item_stat.st_mode) & 0o077:
            self.add(
                "HERMES-PERM-001",
                "error",
                "Sensitive file permissions are too broad",
                evidence,
                "Group or other permission bits are set on a credential-bearing file.",
                "Set owner-only permissions after confirming the correct owner and required service access.",
            )

        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor: int | None = None
        try:
            descriptor = os.open(path, flags)
            opened_stat = os.fstat(descriptor)
            if not stat.S_ISREG(opened_stat.st_mode):
                raise OSError("opened object is not a regular file")
            if (opened_stat.st_dev, opened_stat.st_ino) != (
                item_stat.st_dev,
                item_stat.st_ino,
            ):
                raise OSError("file changed during inspection")
            data = os.read(descriptor, MAX_FILE_BYTES + 1)
        except OSError as exc:
            self.add(
                "HERMES-FILE-006",
                "error",
                "Safe file read failed",
                evidence,
                f"Bounded no-follow read failed ({exc.__class__.__name__}).",
                "Stop and inspect ownership, races, and file type before retrying.",
            )
            return None
        finally:
            if descriptor is not None:
                os.close(descriptor)

        if len(data) > MAX_FILE_BYTES:
            self.add(
                "HERMES-FILE-005",
                "error",
                "State file exceeds inspection limit",
                evidence,
                f"The file grew beyond the {MAX_FILE_BYTES}-byte inspection cap.",
                "Inspect the unexpected growth separately and provide a bounded reviewed copy if needed.",
            )
            return None
        try:
            text = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            self.add(
                "HERMES-FILE-007",
                "error",
                "State file is not valid UTF-8",
                evidence,
                "The file could not be decoded as UTF-8; no content was analyzed.",
                "Preserve the original, determine provenance, and repair through a reviewed migration.",
            )
            return None
        if any(ord(char) < 32 and char not in "\n\r\t" for char in text) or "\x7f" in text:
            self.add(
                "HERMES-FILE-008",
                "error",
                "State file contains control characters",
                evidence,
                "Unexpected control characters make safe text parsing unreliable.",
                "Preserve the original and investigate corruption or malicious content.",
            )
            return None
        return text

    def _inspect_state_directories(self) -> None:
        for name in STATE_DIRECTORIES:
            path = self.home / name
            metadata: dict[str, Any] = {"present": False, "nonempty": False}
            try:
                item_stat = os.lstat(path)
            except FileNotFoundError:
                self.state_metadata[name] = metadata
                continue
            except OSError as exc:
                self.add(
                    "HERMES-STATE-001",
                    "error",
                    "State directory is not inspectable",
                    name,
                    f"Metadata inspection failed ({exc.__class__.__name__}).",
                    "Inspect ownership and file type without following unknown links.",
                )
                self.state_metadata[name] = metadata
                continue

            metadata["present"] = True
            if stat.S_ISLNK(item_stat.st_mode):
                self.add(
                    "HERMES-STATE-002",
                    "error",
                    "Symlinked state directory rejected",
                    name,
                    "A selected state directory is a symbolic link.",
                    "Use an owned directory after reviewing the target and migration implications.",
                )
            elif not stat.S_ISDIR(item_stat.st_mode):
                self.add(
                    "HERMES-STATE-003",
                    "error",
                    "Unsafe state-directory type",
                    name,
                    "A selected state path is not a directory.",
                    "Investigate and restore the expected owned directory type.",
                )
            else:
                try:
                    with os.scandir(path) as entries:
                        metadata["nonempty"] = next(entries, None) is not None
                except OSError as exc:
                    self.add(
                        "HERMES-STATE-004",
                        "warning",
                        "State directory contents are not inspectable",
                        name,
                        f"Directory enumeration failed ({exc.__class__.__name__}).",
                        "Confirm ownership and review the directory separately.",
                    )
            self.state_metadata[name] = metadata

        review_map = {
            "skills": ("HERMES-EXT-001", "Installed skills require trust review"),
            "plugins": ("HERMES-EXT-002", "Installed plugins require trust review"),
            "cron": ("HERMES-AUTO-001", "Scheduled work requires an automation review"),
        }
        for name, (finding_id, title) in review_map.items():
            if self.state_metadata.get(name, {}).get("nonempty"):
                self.add(
                    finding_id,
                    "warning",
                    title,
                    name,
                    "The state directory is non-empty; package/code, authority, persistence, and rollback were not verified by this scan.",
                    "Inventory every item and apply the relevant trust or automation workflow.",
                )

    @staticmethod
    def _strip_yaml_comment(value: str) -> str:
        quote: str | None = None
        escaped = False
        output: list[str] = []
        for char in value:
            if escaped:
                output.append(char)
                escaped = False
                continue
            if char == "\\" and quote == '"':
                output.append(char)
                escaped = True
                continue
            if char in {"'", '"'}:
                if quote is None:
                    quote = char
                elif quote == char:
                    quote = None
                output.append(char)
                continue
            if char == "#" and quote is None:
                break
            output.append(char)
        return "".join(output).rstrip()

    @staticmethod
    def _unquote(value: str) -> str:
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            return value[1:-1]
        return value

    def _scan_config(self, text: str) -> None:
        stack: list[tuple[int, str]] = []
        seen: set[str] = set()
        key_re = re.compile(r"^[A-Za-z0-9_.-]+$")

        for line_number, raw_line in enumerate(text.splitlines(), start=1):
            if not raw_line.strip() or raw_line.lstrip().startswith("#"):
                continue
            if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip(" \t"))]:
                self.add(
                    "HERMES-YAML-001",
                    "error",
                    "Tab-indented YAML cannot be safely scanned",
                    f"config.yaml:{line_number}",
                    "The conservative scanner accepts space indentation only.",
                    "Validate and normalize indentation with a reviewed YAML workflow.",
                )
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            stripped = self._strip_yaml_comment(raw_line.strip())
            if not stripped:
                continue

            while stack and indent <= stack[-1][0]:
                stack.pop()

            if stripped.startswith("-"):
                parent = ".".join(item[1] for item in stack)
                if not parent:
                    self.add(
                        "HERMES-YAML-002",
                        "warning",
                        "Top-level YAML sequence requires manual review",
                        f"config.yaml:{line_number}",
                        "The scalar-path scanner cannot establish a mapping path for this sequence item.",
                        "Review the file with the target Hermes configuration schema.",
                    )
                    continue
                path = parent + "[]"
                value = self._unquote(stripped[1:].strip())
                self.config_paths.add(path)
                self.config_scalars[f"{path}#{line_number}"] = Scalar(
                    path, value, line_number, "sequence-item"
                )
                continue

            if ":" not in stripped:
                self.add(
                    "HERMES-YAML-003",
                    "warning",
                    "Complex YAML line requires manual review",
                    f"config.yaml:{line_number}",
                    "The line does not match a simple mapping scalar.",
                    "Validate it with the target Hermes schema and inspect the effective configuration.",
                )
                continue

            key, raw_value = stripped.split(":", 1)
            key = key.strip()
            if not key_re.fullmatch(key):
                self.add(
                    "HERMES-YAML-004",
                    "warning",
                    "Complex YAML key requires manual review",
                    f"config.yaml:{line_number}",
                    "The key is outside the conservative scalar-path grammar.",
                    "Validate it with the target Hermes schema and inspect the effective configuration.",
                )
                continue

            path = ".".join([*(item[1] for item in stack), key])
            self.config_paths.add(path)
            if path in seen:
                self.add(
                    "HERMES-YAML-005",
                    "error",
                    "Duplicate configuration path",
                    f"config.yaml:{line_number}:{path}",
                    "Duplicate YAML keys can produce parser-dependent or surprising effective values.",
                    "Remove the duplicate and validate the effective configuration.",
                )
            seen.add(path)

            value = self._unquote(raw_value.strip())
            if value == "":
                stack.append((indent, key))
                continue
            kind = "scalar"
            if value in {"|", ">", "|-", ">-", "|+", ">+"}:
                kind = "block-scalar"
                self.add(
                    "HERMES-YAML-006",
                    "warning",
                    "Block scalar requires manual review",
                    f"config.yaml:{line_number}:{path}",
                    "The conservative scanner does not interpret block scalar contents.",
                    "Review the complete value and effective runtime configuration.",
                )
            elif any(token in value for token in ("&", "*", "!!")):
                kind = "advanced-yaml"
                self.add(
                    "HERMES-YAML-007",
                    "warning",
                    "Advanced YAML feature requires manual review",
                    f"config.yaml:{line_number}:{path}",
                    "Anchor, alias, or tag syntax may affect interpretation.",
                    "Use plain verified values and validate with the target runtime.",
                )
            self.config_scalars[path] = Scalar(path, value, line_number, kind)

    def _scalar(self, path: str) -> str | None:
        scalar = self.config_scalars.get(path)
        return scalar.value.strip() if scalar else None

    @staticmethod
    def _normalized(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().strip("'\"").lower()

    @staticmethod
    def _is_nonempty_collection(value: str) -> bool:
        normalized = value.strip().lower()
        return normalized not in {"", "[]", "{}", "null", "none", "~"}

    def _analyze_config(self) -> None:
        for key, scalar in self.config_scalars.items():
            path = scalar.path
            value = scalar.value.strip()
            normalized = self._normalized(value) or ""
            evidence = f"config.yaml:{scalar.line}:{path}"

            if SECRET_KEY_RE.search(path):
                if value and normalized not in {"null", "none", "~", "''", '""'}:
                    if not ENV_SUB_RE.fullmatch(value) and not PLACEHOLDER_RE.search(value):
                        self.add(
                            "HERMES-SECRET-001",
                            "error",
                            "Literal secret-like configuration value",
                            evidence,
                            "A secret-bearing key appears to contain a literal value; the value is intentionally not reported.",
                            "Move the credential to the supported secret path, rotate it if exposed, and keep only an environment reference in YAML.",
                        )
            elif any(pattern.fullmatch(value) for pattern in SECRET_VALUE_PATTERNS):
                self.add(
                    "HERMES-SECRET-002",
                    "error",
                    "Secret-shaped literal in configuration",
                    evidence,
                    "A value matches a common credential shape; the value is intentionally not reported.",
                    "Remove and rotate the suspected credential, then use the supported secret path.",
                )

            review_prefixes = {
                "mcp_servers": ("HERMES-MCP-001", "MCP configuration requires review"),
                "plugins": ("HERMES-EXT-003", "Plugin configuration requires review"),
                "hooks": ("HERMES-AUTO-002", "Hook configuration requires review"),
                "cron": ("HERMES-AUTO-003", "Cron configuration requires review"),
                "gateway": ("HERMES-GATEWAY-001", "Gateway configuration requires review"),
            }
            for prefix, (finding_id, title) in review_prefixes.items():
                if path == prefix or path.startswith(prefix + "."):
                    if value == "" or self._is_nonempty_collection(value):
                        self.add(
                            finding_id,
                            "warning",
                            title,
                            evidence,
                            "The offline scan cannot prove identity, authorization, data flow, side effects, or isolation for this feature.",
                            "Apply the dedicated review workflow and validate allowed and denied paths.",
                        )
                    break

            if (
                path.startswith("memory.")
                and any(token in path.lower() for token in ("provider", "endpoint", "honcho"))
                and self._is_nonempty_collection(value)
            ):
                self.add(
                    "HERMES-MEMORY-001",
                    "warning",
                    "External memory configuration requires review",
                    evidence,
                    "A memory provider or endpoint may disclose and persist conversation data externally.",
                    "Verify provider, tenant identity, disclosed fields, retention, deletion, outage behavior, and consent.",
                )

            if path.startswith("terminal."):
                terminal_review = {
                    "terminal.env_passthrough": "Host environment forwarding requires review",
                    "terminal.docker_forward_env": "Container environment forwarding requires review",
                    "terminal.docker_env": "Literal container environment requires review",
                    "terminal.docker_volumes": "Container mounts require review",
                    "terminal.docker_extra_args": "Additional container arguments require review",
                    "terminal.ssh": "Remote execution configuration requires review",
                }
                for prefix, title in terminal_review.items():
                    if (path == prefix or path.startswith(prefix + ".") or path.startswith(prefix + "[]")) and self._is_nonempty_collection(value):
                        self.add(
                            "HERMES-EXEC-004",
                            "warning",
                            title,
                            evidence,
                            "The configured value can broaden filesystem, credential, process, or network authority; its content is not reported.",
                            "Allow only the minimum reviewed names, paths, destinations, and flags, then test denied access.",
                        )
                        break

            if path == "terminal.docker_network" and normalized in TRUE_VALUES:
                self.add(
                    "HERMES-NET-003",
                    "warning",
                    "Sandbox network access is enabled",
                    evidence,
                    "The terminal container can access the network; destination scope is not proven by this scan.",
                    "Disable egress or enforce and test an approved destination policy.",
                )
            if "docker_extra_args" in path and "--network=host" in normalized:
                self.add(
                    "HERMES-NET-004",
                    "error",
                    "Host networking requested for terminal container",
                    evidence,
                    "Host networking substantially broadens network reach and weakens separation.",
                    "Remove host networking and use an explicit restricted network design.",
                )

            if self._looks_like_listener_path(path) and value:
                host = normalized.strip("[]")
                if host not in {item.strip("[]") for item in LOOPBACK_VALUES}:
                    self.add(
                        "HERMES-NET-001",
                        "error",
                        "Non-loopback listener indicator",
                        evidence,
                        "A gateway/API/dashboard listener appears configured beyond loopback; the actual value is intentionally not reported.",
                        "Bind to loopback or document and test TLS, network policy, authentication, authorization, and rate limits.",
                    )

    @staticmethod
    def _looks_like_listener_path(path: str) -> bool:
        lowered = path.lower()
        surface = any(token in lowered for token in ("gateway", "api_server", "dashboard", "web"))
        leaf = lowered.rsplit(".", 1)[-1]
        return surface and leaf in {"host", "bind", "listen", "listen_host", "bind_host"}

    def _scan_env(self, text: str) -> None:
        for line_number, raw_line in enumerate(text.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].lstrip()
            if "=" not in line:
                self.add(
                    "HERMES-ENV-001",
                    "warning",
                    "Environment line cannot be classified",
                    f".env:{line_number}",
                    "The line is not a simple KEY=VALUE assignment; no value is reported.",
                    "Review and normalize the environment file without exposing credentials.",
                )
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                self.add(
                    "HERMES-ENV-002",
                    "warning",
                    "Environment key cannot be classified",
                    f".env:{line_number}",
                    "The key is outside the simple environment-name grammar; no value is reported.",
                    "Review and normalize the environment file.",
                )
                continue
            if key in self.env_metadata:
                self.add(
                    "HERMES-ENV-003",
                    "error",
                    "Duplicate environment key",
                    f".env:{line_number}:{key}",
                    "Duplicate environment assignments can make effective values order-dependent.",
                    "Keep one reviewed assignment per key.",
                )
            placeholder = bool(PLACEHOLDER_RE.search(value))
            length_class = "empty" if not value else "short" if len(value) < 16 else "long"
            normalized_value = value.lower()
            self.env_metadata[key] = {
                "present": bool(value),
                "placeholder": placeholder,
                "length_class": length_class,
                "line": line_number,
                "truth": normalized_value in TRUE_VALUES,
                "non_loopback_host": bool(value)
                and normalized_value.strip("[]")
                not in {item.strip("[]") for item in LOOPBACK_VALUES},
            }

    def _scan_auth(self, text: str) -> None:
        self.auth_metadata = {"present": True}
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            self.auth_metadata["valid_json"] = False
            self.add(
                "HERMES-AUTH-001",
                "error",
                "Authentication state is invalid JSON",
                "auth.json",
                "The credential state could not be parsed; no values were reported.",
                "Preserve the file, identify the owning provider flow, and recover through a documented authentication workflow.",
            )
            return
        self.auth_metadata["valid_json"] = True
        self.auth_metadata["top_level_type"] = type(parsed).__name__
        self.auth_metadata["top_level_count"] = len(parsed) if isinstance(parsed, (dict, list)) else 1
        if not isinstance(parsed, dict):
            self.add(
                "HERMES-AUTH-002",
                "warning",
                "Authentication state has an unexpected top-level type",
                "auth.json",
                "The file is valid JSON but not an object; no values were reported.",
                "Validate the target-version authentication schema before use.",
            )

    def _analyze_runtime_posture(self) -> None:
        backend = self._normalized(self._scalar("terminal.backend"))
        risky = self.deployment in {"shared", "production"} or self.input_trust == "untrusted"
        if backend is None:
            severity = "error" if risky else "warning"
            self.add(
                "HERMES-EXEC-001",
                severity,
                "Terminal backend is not explicitly established",
                "config.yaml:terminal.backend",
                "The scan cannot prove an isolated execution backend; target-version defaults must not be assumed for risky use.",
                "Discover the effective backend and configure a reviewed boundary or disable execution.",
            )
        elif backend == "local":
            severity = "error" if risky else "warning"
            self.add(
                "HERMES-EXEC-002",
                severity,
                "Local execution inherits host authority",
                "config.yaml:terminal.backend",
                "Terminal and code operations run with the host account's filesystem, process, credential, and network authority.",
                "Use a reviewed outer boundary and sandboxed backend, or limit work to controlled read-only tasks.",
            )
        elif backend in SANDBOX_BACKENDS:
            if self.input_trust == "untrusted" or self.deployment in {"shared", "production"}:
                self.add(
                    "HERMES-EXEC-003",
                    "warning",
                    "Terminal backend does not contain all Hermes code paths",
                    "config.yaml:terminal.backend",
                    "The selected backend may isolate terminal/file/code handlers, but host-side agent, gateway, browser, plugin, MCP, and credential paths require separate controls.",
                    "Map every execution path and use whole-process isolation for adversarial input.",
                )
        else:
            self.add(
                "HERMES-EXEC-005",
                "warning",
                "Unknown terminal backend requires review",
                "config.yaml:terminal.backend",
                "The backend value is not in this analyzer's verified snapshot; the value is intentionally not reported.",
                "Validate it against the installed version and document the actual boundary.",
            )

        approval_mode = self._normalized(self._scalar("approvals.mode"))
        if approval_mode == "off":
            severity = "error" if risky or self.strict else "warning"
            self.add(
                "HERMES-APPROVAL-001",
                severity,
                "Command approvals are disabled",
                "config.yaml:approvals.mode",
                "Approval checks are configured off. This does not create containment and materially increases execution risk.",
                "Restore manual or reviewed smart approvals and rely on OS isolation as the primary boundary.",
            )

    def _analyze_api_server(self) -> None:
        enabled_meta = self.env_metadata.get("API_SERVER_ENABLED")
        enabled = False
        if enabled_meta:
            # Re-read only the classified value through the original scalar map is intentionally
            # avoided. Presence alone is insufficient; scan the file value again without output.
            enabled = self._env_truth("API_SERVER_ENABLED")
        config_enabled = self._normalized(
            self._scalar("gateway.platforms.api_server.enabled")
        )
        enabled = enabled or config_enabled in TRUE_VALUES
        if not enabled:
            return

        key_meta = self.env_metadata.get("API_SERVER_KEY")
        config_key = self._scalar("gateway.platforms.api_server.api_key")
        key_indicator = bool(
            key_meta
            and key_meta["present"]
            and not key_meta["placeholder"]
            and key_meta["length_class"] == "long"
        ) or bool(config_key and ENV_SUB_RE.fullmatch(config_key.strip()))
        if not key_indicator:
            self.add(
                "HERMES-API-001",
                "error",
                "API server enabled without an adequate key indicator",
                "environment/config:API_SERVER_ENABLED",
                "The server appears enabled, but the scan cannot establish a non-placeholder credential of adequate length without revealing it.",
                "Provide a unique high-entropy secret through the supported secret path and test unauthenticated denial.",
            )
        self.add(
            "HERMES-API-002",
            "warning",
            "API server exposure requires perimeter review",
            "environment/config:API_SERVER_ENABLED",
            "The server can invoke the agent and tools; this scan cannot prove listener, TLS, network policy, authorization, limits, or tenant isolation.",
            "Keep loopback by default and validate every exposure and denied path before non-local use.",
        )

    def _env_truth(self, key: str) -> bool:
        return bool(self.env_metadata.get(key, {}).get("truth"))

    def _analyze_env_controls(self) -> None:
        if self._env_truth("HERMES_YOLO_MODE"):
            risky = self.deployment in {"shared", "production"} or self.input_trust == "untrusted"
            self.add(
                "HERMES-APPROVAL-002",
                "error" if risky or self.strict else "warning",
                "Unrestricted Yolo mode is enabled",
                ".env:HERMES_YOLO_MODE",
                "The environment requests unrestricted execution; the actual value is intentionally not reported.",
                "Disable it, restore approvals, and use a reviewed OS isolation boundary.",
            )
        if "HERMES_DASHBOARD_INSECURE" in self.env_metadata:
            self.add(
                "HERMES-DEPRECATED-001",
                "warning",
                "Deprecated dashboard-insecure variable is present",
                ".env:HERMES_DASHBOARD_INSECURE",
                "Current first-party documentation states this variable is ignored; retaining it can create a false security assumption.",
                "Remove it and configure the supported authenticated perimeter explicitly.",
            )

        for key in self.env_metadata:
            upper = key.upper()
            if any(token in upper for token in ("GATEWAY_HOST", "API_SERVER_HOST", "DASHBOARD_HOST", "BIND_HOST")):
                if self._env_host_is_non_loopback(key):
                    self.add(
                        "HERMES-NET-002",
                        "error",
                        "Non-loopback environment listener indicator",
                        f".env:{key}",
                        "A listener-related environment key appears non-loopback; the value is intentionally not reported.",
                        "Bind loopback or validate an authenticated TLS/network perimeter and denied access.",
                    )

    def _env_host_is_non_loopback(self, key: str) -> bool:
        return bool(self.env_metadata.get(key, {}).get("non_loopback_host"))

    def _result(self) -> dict[str, Any]:
        unique: dict[tuple[str, str, str], Finding] = {}
        for finding in self.findings:
            unique[(finding.finding_id, finding.evidence, finding.title)] = finding
        findings = sorted(
            unique.values(),
            key=lambda item: (
                SEVERITY_ORDER[item.severity],
                item.finding_id,
                item.evidence,
                item.title,
            ),
        )
        counts = {
            severity: sum(1 for item in findings if item.severity == severity)
            for severity in ("error", "warning", "info")
        }
        valid = counts["error"] == 0 and (not self.strict or counts["warning"] == 0)
        return {
            "schema_version": SCHEMA_VERSION,
            "target": str(self.home),
            "deployment": self.deployment,
            "input_trust": self.input_trust,
            "strict": self.strict,
            "valid": valid,
            "summary": counts,
            "findings": [item.as_dict() for item in findings],
            "coverage": {
                "files_checked": sorted(self.files_checked),
                "config_paths": sorted(self.config_paths),
                "environment": {
                    key: {
                        field: value
                        for field, value in sorted(metadata.items())
                        if field in {"present", "placeholder", "length_class"}
                    }
                    for key, metadata in sorted(self.env_metadata.items())
                },
                "auth": self.auth_metadata,
                "state_directories": {
                    key: self.state_metadata[key] for key in sorted(self.state_metadata)
                },
            },
            "limitations": [
                "Offline heuristic scan; no effective Hermes runtime state was queried.",
                "The YAML scanner recognizes conservative scalar paths and is not a full schema validator.",
                "Terminal-backend findings do not prove whole-process isolation.",
                "Credential presence and length indicators do not prove scope, validity, storage, or rotation.",
                "A valid result is not a security certification; perform the referenced manual and denied-path tests.",
            ],
        }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline, read-only Hermes Agent home preflight"
    )
    parser.add_argument(
        "--hermes-home",
        type=Path,
        default=None,
        help="Hermes home to inspect (default: HERMES_HOME or ~/.hermes)",
    )
    parser.add_argument(
        "--deployment",
        choices=("personal", "shared", "production"),
        default="personal",
    )
    parser.add_argument(
        "--input-trust",
        choices=("controlled", "mixed", "untrusted"),
        default="controlled",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as an invalid preflight result",
    )
    return parser


def _default_home() -> Path:
    configured = os.environ.get("HERMES_HOME")
    return Path(configured) if configured else Path.home() / ".hermes"


def _absolute_no_resolve(path: Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def _render_text(result: dict[str, Any]) -> str:
    lines = [
        "Hermes Agent Offline Preflight",
        f"Schema: {result['schema_version']}",
        f"Target: {result['target']}",
        f"Deployment: {result['deployment']}",
        f"Input trust: {result['input_trust']}",
        f"Strict: {str(result['strict']).lower()}",
        f"Valid: {str(result['valid']).lower()}",
        (
            "Findings: "
            f"{result['summary']['error']} error, "
            f"{result['summary']['warning']} warning, "
            f"{result['summary']['info']} info"
        ),
        "",
    ]
    if result["findings"]:
        for finding in result["findings"]:
            lines.extend(
                [
                    f"[{finding['severity'].upper()}] {finding['id']} — {finding['title']}",
                    f"  Evidence: {finding['evidence']}",
                    f"  Detail: {finding['detail']}",
                    f"  Remediation: {finding['remediation']}",
                ]
            )
    else:
        lines.append("No findings were emitted within the scanner's limited coverage.")
    lines.extend(["", "Limitations:"])
    lines.extend(f"- {item}" for item in result["limitations"])
    return "\n".join(lines) + "\n"


def main(argv: Iterable[str] | None = None) -> int:
    args = _build_parser().parse_args(list(argv) if argv is not None else None)
    home = _absolute_no_resolve(args.hermes_home or _default_home())
    result = Analyzer(home, args.deployment, args.input_trust, args.strict).analyze()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        sys.stdout.write(_render_text(result))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
