#!/usr/bin/env python3
"""Deterministic tests for the offline Hermes Agent preflight analyzer."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PACKAGE_ROOT / "scripts" / "hermes_preflight.py"
FIXTURES = PACKAGE_ROOT / "tests" / "fixtures"

SPEC = importlib.util.spec_from_file_location("hermes_preflight", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load hermes_preflight.py")
PREFLIGHT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREFLIGHT
SPEC.loader.exec_module(PREFLIGHT)


class HermesPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="hermes-preflight-test-")
        self.addCleanup(self.temporary.cleanup)
        self.temp_root = Path(self.temporary.name)

    def copy_fixture(self, name: str) -> Path:
        destination = self.temp_root / name
        shutil.copytree(FIXTURES / name, destination)
        for sensitive_name in (".env", "auth.json"):
            sensitive = destination / sensitive_name
            if sensitive.exists() and os.name == "posix":
                sensitive.chmod(0o600)
        return destination

    def analyze(
        self,
        home: Path,
        deployment: str = "production",
        input_trust: str = "untrusted",
        strict: bool = False,
    ) -> dict[str, object]:
        return PREFLIGHT.Analyzer(home, deployment, input_trust, strict).analyze()

    @staticmethod
    def finding_ids(result: dict[str, object]) -> list[str]:
        findings = result["findings"]
        assert isinstance(findings, list)
        return [str(item["id"]) for item in findings]

    def run_cli(self, home: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT_PATH),
                "--hermes-home",
                str(home),
                "--deployment",
                "production",
                "--input-trust",
                "untrusted",
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
            timeout=10,
        )

    def test_safe_fixture_is_valid_non_strict(self) -> None:
        result = self.analyze(self.copy_fixture("safe-home"))
        self.assertTrue(result["valid"])
        self.assertEqual(result["summary"]["error"], 0)
        self.assertIn("HERMES-EXEC-003", self.finding_ids(result))

    def test_strict_mode_fails_on_unresolved_warning(self) -> None:
        result = self.analyze(self.copy_fixture("safe-home"), strict=True)
        self.assertFalse(result["valid"])
        self.assertGreater(result["summary"]["warning"], 0)

    def test_unsafe_fixture_emits_required_findings(self) -> None:
        result = self.analyze(self.copy_fixture("unsafe-home"))
        self.assertFalse(result["valid"])
        expected = {
            "HERMES-API-001",
            "HERMES-APPROVAL-001",
            "HERMES-APPROVAL-002",
            "HERMES-DEPRECATED-001",
            "HERMES-EXEC-002",
            "HERMES-EXEC-004",
            "HERMES-MCP-001",
            "HERMES-NET-001",
            "HERMES-NET-002",
            "HERMES-NET-003",
            "HERMES-NET-004",
            "HERMES-SECRET-001",
        }
        self.assertTrue(expected.issubset(set(self.finding_ids(result))))

    def test_secret_values_are_not_emitted(self) -> None:
        home = self.copy_fixture("unsafe-home")
        secret = "redaction-sentinel-7f3a9c2e6b4d8f1a"
        result = self.analyze(home)
        rendered = json.dumps(result, sort_keys=True)
        self.assertNotIn(secret, rendered)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", rendered)

    def test_environment_metadata_is_classified_without_values(self) -> None:
        result = self.analyze(self.copy_fixture("unsafe-home"))
        environment = result["coverage"]["environment"]
        self.assertEqual(
            set(environment["API_SERVER_KEY"]),
            {"length_class", "placeholder", "present"},
        )
        self.assertNotIn("short", json.dumps(environment["API_SERVER_KEY"]).split(":", 1)[0])

    def test_duplicate_and_invalid_state_fail_closed(self) -> None:
        result = self.analyze(self.copy_fixture("invalid-home"))
        self.assertFalse(result["valid"])
        ids = set(self.finding_ids(result))
        self.assertIn("HERMES-YAML-005", ids)
        self.assertIn("HERMES-ENV-003", ids)
        self.assertIn("HERMES-AUTH-001", ids)

    def test_missing_home_is_invalid(self) -> None:
        result = self.analyze(self.temp_root / "does-not-exist")
        self.assertFalse(result["valid"])
        self.assertEqual(self.finding_ids(result), ["HERMES-HOME-001"])

    def test_missing_config_is_invalid(self) -> None:
        home = self.temp_root / "empty-home"
        home.mkdir()
        result = self.analyze(home, deployment="personal", input_trust="controlled")
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-FILE-001", self.finding_ids(result))

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links unavailable")
    def test_symlinked_root_is_rejected(self) -> None:
        target = self.copy_fixture("safe-home")
        link = self.temp_root / "linked-home"
        link.symlink_to(target, target_is_directory=True)
        result = self.analyze(link)
        self.assertFalse(result["valid"])
        self.assertEqual(self.finding_ids(result), ["HERMES-HOME-003"])

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links unavailable")
    def test_symlinked_known_file_is_not_followed(self) -> None:
        home = self.copy_fixture("safe-home")
        secret = "secret-that-must-never-appear"
        target = self.temp_root / "outside.env"
        target.write_text(f"API_SERVER_KEY={secret}\n", encoding="utf-8")
        env_file = home / ".env"
        env_file.unlink()
        env_file.symlink_to(target)
        result = self.analyze(home)
        rendered = json.dumps(result, sort_keys=True)
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-FILE-003", self.finding_ids(result))
        self.assertNotIn(secret, rendered)

    def test_oversized_known_file_is_rejected(self) -> None:
        home = self.copy_fixture("safe-home")
        env_file = home / ".env"
        env_file.write_bytes(b"A" * (PREFLIGHT.MAX_FILE_BYTES + 1))
        result = self.analyze(home)
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-FILE-005", self.finding_ids(result))

    def test_invalid_utf8_is_rejected(self) -> None:
        home = self.copy_fixture("safe-home")
        env_file = home / ".env"
        env_file.write_bytes(b"API_SERVER_KEY=\xff\xfe\n")
        result = self.analyze(home)
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-FILE-007", self.finding_ids(result))

    def test_control_character_is_rejected(self) -> None:
        home = self.copy_fixture("safe-home")
        env_file = home / ".env"
        env_file.write_bytes(b"API_SERVER_KEY=abc\x00def\n")
        result = self.analyze(home)
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-FILE-008", self.finding_ids(result))

    @unittest.skipUnless(os.name == "posix", "POSIX mode bits required")
    def test_broad_sensitive_file_permissions_fail(self) -> None:
        home = self.copy_fixture("safe-home")
        (home / ".env").chmod(0o644)
        result = self.analyze(home)
        self.assertFalse(result["valid"])
        self.assertIn("HERMES-PERM-001", self.finding_ids(result))

    def test_json_output_is_deterministic(self) -> None:
        home = self.copy_fixture("unsafe-home")
        first = self.run_cli(home, "--format", "json")
        second = self.run_cli(home, "--format", "json")
        self.assertEqual(first.returncode, 1)
        self.assertEqual(second.returncode, 1)
        self.assertEqual(first.stdout, second.stdout)
        parsed = json.loads(first.stdout)
        self.assertEqual(parsed["schema_version"], "1.0")

    def test_cli_exit_codes_match_validity(self) -> None:
        safe = self.run_cli(self.copy_fixture("safe-home"), "--format", "text")
        unsafe = self.run_cli(self.copy_fixture("unsafe-home"), "--format", "text")
        self.assertEqual(safe.returncode, 0, safe.stdout + safe.stderr)
        self.assertEqual(unsafe.returncode, 1, unsafe.stdout + unsafe.stderr)
        self.assertIn("Valid: true", safe.stdout)
        self.assertIn("Valid: false", unsafe.stdout)

    def test_cli_rejects_unknown_enumerations(self) -> None:
        home = self.copy_fixture("safe-home")
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT_PATH),
                "--hermes-home",
                str(home),
                "--deployment",
                "internet-scale",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)

    def test_output_contains_explicit_limitations(self) -> None:
        result = self.analyze(self.copy_fixture("safe-home"))
        limitations = result["limitations"]
        self.assertGreaterEqual(len(limitations), 5)
        self.assertTrue(any("not a security certification" in item for item in limitations))


class HermesPackageSelfCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="hermes-self-check-test-")
        self.addCleanup(self.temporary.cleanup)
        self.package = Path(self.temporary.name) / "hermes-agent"
        shutil.copytree(PACKAGE_ROOT, self.package)

    def run_self_check(self, *extra: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(self.package / "scripts" / "self_check.py"),
                "--json-output",
                *extra,
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
            timeout=20,
        )

    def test_source_package_passes(self) -> None:
        result = self.run_self_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["metrics"]["official_sources"], 98)
        self.assertGreaterEqual(
            payload["metrics"]["official_guidance_source_urls"], 50
        )

    def test_required_installer_marker_rejects_missing_marker(self) -> None:
        result = self.run_self_check("--require-installer-marker")
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"])
        self.assertIn(
            ".lzr1-managed: required managed-install marker is missing",
            payload["errors"],
        )

    def test_exact_installer_marker_is_accepted(self) -> None:
        (self.package / ".lzr1-managed").write_text(
            "schema=1\nsource=victorlazari/lzr1-skills\nskill=hermes-agent\n",
            encoding="utf-8",
        )
        result = self.run_self_check("--require-installer-marker")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])

    def test_tampered_installer_marker_is_rejected(self) -> None:
        (self.package / ".lzr1-managed").write_text(
            "schema=1\nsource=untrusted/example\nskill=hermes-agent\n",
            encoding="utf-8",
        )
        result = self.run_self_check()
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"])
        self.assertTrue(any("invalid installer marker content" in item for item in payload["errors"]))

    def test_unexpected_package_file_is_rejected(self) -> None:
        (self.package / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
        result = self.run_self_check()
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["valid"])
        self.assertIn("unexpected package file: unexpected.txt", payload["errors"])

    def test_ast_rejects_alias_bypasses_before_runtime_execution(self) -> None:
        preflight = self.package / "scripts" / "hermes_preflight.py"
        original = preflight.read_text(encoding="utf-8")
        sentinel = self.package / "ast-mutation-must-not-run"
        mutations = {
            "network_alias": "\nimport socket as net\nnet.create_connection(('example.invalid', 443))\n",
            "system_alias": "\nfrom os import system as invoke\ninvoke('true')\n",
            "writable_open": (
                "\nimport os as safe_os\n"
                f"safe_os.open({str(sentinel)!r}, safe_os.O_WRONLY | safe_os.O_CREAT)\n"
            ),
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                preflight.write_text(original + mutation, encoding="utf-8")
                result = self.run_self_check()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                payload = json.loads(result.stdout)
                self.assertTrue(
                    any("AST violation" in item for item in payload["errors"]),
                    payload,
                )
                self.assertTrue(
                    any("runtime contract skipped" in item for item in payload["errors"]),
                    payload,
                )
                self.assertFalse(sentinel.exists())
        preflight.write_text(original, encoding="utf-8")

    def test_citation_target_mutation_is_rejected(self) -> None:
        skill = self.package / "SKILL.md"
        original = skill.read_text(encoding="utf-8")
        trusted = "https://hermes-agent.nousresearch.com/docs/getting-started/installation"
        self.assertIn(trusted, original)
        skill.write_text(
            original.replace(trusted, "https://example.invalid/hermes", 1),
            encoding="utf-8",
        )
        result = self.run_self_check()
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any("not first-party HTTPS" in item for item in payload["errors"]),
            payload,
        )
        self.assertTrue(
            any("absent from sources.md" in item for item in payload["errors"]),
            payload,
        )

    def test_citation_definition_deletion_is_rejected(self) -> None:
        skill = self.package / "SKILL.md"
        original = skill.read_text(encoding="utf-8")
        definition = (
            "[12]: https://hermes-agent.nousresearch.com/docs/guides/"
            "delegation-patterns \"Delegation and parallel work\"\n"
        )
        self.assertIn(definition, original)
        skill.write_text(original.replace(definition, "", 1), encoding="utf-8")
        result = self.run_self_check()
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertTrue(
            any("undefined local citation [12]" in item for item in payload["errors"]),
            payload,
        )

    def test_markdown_angle_path_with_fragment_and_title_is_accepted(self) -> None:
        skill = self.package / "SKILL.md"
        original = skill.read_text(encoding="utf-8")
        skill.write_text(
            original
            + "\n[Link parser regression](<references/security-production.md#threat-model> \"Security\")\n",
            encoding="utf-8",
        )
        result = self.run_self_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_markdown_traversal_and_malformed_title_are_rejected(self) -> None:
        skill = self.package / "SKILL.md"
        original = skill.read_text(encoding="utf-8")
        mutations = {
            "encoded_traversal": "\n[bad](%2E%2E/outside.md)\n",
            "malformed_title": (
                "\n[bad](references/security-production.md unquoted-title)\n"
            ),
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                skill.write_text(original + mutation, encoding="utf-8")
                result = self.run_self_check()
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)["valid"])
        skill.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main(verbosity=2)
