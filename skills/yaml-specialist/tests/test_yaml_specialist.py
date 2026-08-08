#!/usr/bin/env python3
"""Deterministic offline tests for yaml-specialist."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "scripts"
FIXTURES = PACKAGE / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import yaml_common as common  # noqa: E402


class Result:
    def __init__(self, completed: subprocess.CompletedProcess[str]) -> None:
        self.returncode = completed.returncode
        self.stdout = completed.stdout
        self.stderr = completed.stderr
        try:
            self.data = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise AssertionError(
                f"command did not emit JSON\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ) from exc


def run_script(name: str, *arguments: str, cwd: Path | None = None) -> Result:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONPATH"] = str(SCRIPTS)
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        cwd=str(cwd or PACKAGE),
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=30,
    )
    return Result(completed)


class YamlSpecialistTests(unittest.TestCase):
    maxDiff = 4000

    def test_application_contract_is_complete(self) -> None:
        result = run_script(
            "values_contract_lint.py",
            "--chart",
            str(FIXTURES / "application-chart"),
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.data["status"], "complete")
        self.assertEqual(result.data["errors"], 0)
        self.assertEqual(result.data["warnings"], 0)
        self.assertTrue(result.data["schema"]["validated"])

    def test_library_contract_is_complete_without_operator_overlay(self) -> None:
        result = run_script(
            "values_contract_lint.py",
            "--chart",
            str(FIXTURES / "library-chart"),
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.data["status"], "complete")
        self.assertIn("values-template omitted for library chart", result.data["coverage_gaps"])

    def test_static_values_scanner_covers_application_and_library_charts(self) -> None:
        for chart_name in ("application-chart", "library-chart"):
            with self.subTest(chart=chart_name):
                result = run_script(
                    "scan_template_values.py",
                    "--chart",
                    str(FIXTURES / chart_name),
                    "--format",
                    "json",
                )
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(result.data["status"], "complete")
                self.assertGreater(result.data["static_use_count"], 0)
                self.assertEqual(result.data["dynamic_review_count"], 0)

    def test_dynamic_template_expression_is_incomplete_not_clean(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yaml-specialist-dynamic-") as temporary:
            chart = Path(temporary) / "chart"
            shutil.copytree(FIXTURES / "application-chart", chart)
            dynamic = chart / "templates" / "dynamic.yaml"
            dynamic.write_text(
                '{{- $selected := "repository" -}}\nvalue: {{ index .Values.image $selected | quote }}\n',
                encoding="utf-8",
            )
            result = run_script(
                "scan_template_values.py",
                "--chart",
                str(chart),
                "--format",
                "json",
            )
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(result.data["status"], "incomplete")
        self.assertGreater(result.data["dynamic_review_count"], 0)

    def test_refactor_inventory_is_deterministic_and_omits_scalar_defaults(self) -> None:
        result = run_script(
            "build_refactor_inventory.py",
            "--chart",
            str(FIXTURES / "application-chart"),
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.data["status"], "complete")
        self.assertEqual(result.data["canonical_path_count"], result.data["documentation_complete_count"])
        self.assertNotIn("registry.example.invalid", result.stdout)
        self.assertTrue(all("disposition" in row for row in result.data["rows"]))

    def test_duplicate_keys_fail_closed(self) -> None:
        with self.assertRaises(common.InputError):
            common.load_mapping(FIXTURES / "duplicate-key.yaml")

    def test_secret_reference_metadata_is_not_confused_with_secret_material(self) -> None:
        self.assertTrue(common.is_secret_path("apiToken"))
        self.assertTrue(common.is_secret_path("database.password"))
        self.assertTrue(common.is_secret_path("clientSecret"))
        self.assertFalse(common.is_secret_path("existingSecret.name"))
        self.assertFalse(common.is_secret_path("existingSecret.key"))
        self.assertFalse(common.is_secret_path("secretRef.name"))
        self.assertFalse(common.is_secret_path("imagePullSecrets[0].name"))

    def test_contract_reports_secret_without_echoing_value(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yaml-specialist-secret-") as temporary:
            chart = Path(temporary) / "chart"
            shutil.copytree(FIXTURES / "application-chart", chart)
            secret_value = "sensi" + "tive-regression-value"
            with (chart / "values.yaml").open("a", encoding="utf-8") as stream:
                stream.write(
                    "\n# -- apiToken is an intentionally invalid concrete secret fixture.\n"
                    "# @type string\n# @required false\n# @accepted empty only\n"
                    "# @default empty\n# @example empty\n"
                    "# @security Use an external Secret reference instead.\n"
                    f"apiToken: {secret_value}\n"
                )
            result = run_script(
                "values_contract_lint.py",
                "--chart",
                str(chart),
                "--skip-schema",
                "--skip-template",
                "--format",
                "json",
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertEqual(result.data["status"], "failed")
        self.assertNotIn(secret_value, result.stdout)
        self.assertTrue(any(item["code"] == "concrete-secret-default" for item in result.data["findings"]))

    def test_repository_path_confinement_rejects_escape(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yaml-specialist-confine-") as temporary:
            root = Path(temporary) / "root"
            root.mkdir()
            outside = Path(temporary) / "outside.yaml"
            outside.write_text("safe: true\n", encoding="utf-8")
            link = root / "escape.yaml"
            link.symlink_to(outside)
            with self.assertRaises(common.InputError):
                common.confine_existing_path(root, link, kind="fixture")

    def test_chart_metadata_and_dependency_inventory_are_portable(self) -> None:
        metadata = run_script(
            "chart_metadata.py",
            "--chart",
            str(FIXTURES / "application-chart"),
            "--format",
            "json",
        )
        dependencies = run_script(
            "list_dependency_repositories.py",
            "--chart",
            str(FIXTURES / "application-chart"),
            "--format",
            "json",
        )
        self.assertEqual(metadata.returncode, 0, metadata.stdout)
        self.assertEqual(metadata.data["type"], "application")
        self.assertEqual(dependencies.returncode, 0, dependencies.stdout)
        self.assertEqual(dependencies.data["dependency_count"], 0)

    def test_dependency_credentials_are_redacted_and_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yaml-specialist-dependency-") as temporary:
            chart = Path(temporary) / "chart"
            chart.mkdir()
            credential = "review" + "-password"
            (chart / "Chart.yaml").write_text(
                "apiVersion: v2\nname: fixture\nversion: 0.1.0\ndependencies:\n"
                "  - name: child\n    version: 1.0.0\n"
                f"    repository: https://user:{credential}@charts.example.invalid\n",
                encoding="utf-8",
            )
            result = run_script(
                "list_dependency_repositories.py",
                "--chart",
                str(chart),
                "--format",
                "json",
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertNotIn(credential, result.stdout)
        self.assertEqual(result.data["errors"], 1)
        self.assertTrue(
            any(
                item["kind"] == "credential-bearing-url" and item["error"]
                for item in result.data["dependencies"]
            )
        )

    def test_rendered_reference_and_restricted_profile_checks(self) -> None:
        valid = run_script(
            "rendered_manifest_lint.py",
            "--input",
            str(FIXTURES / "rendered-valid.yaml"),
            "--pod-security-profile",
            "restricted",
            "--format",
            "json",
        )
        dangling = run_script(
            "rendered_manifest_lint.py",
            "--input",
            str(FIXTURES / "rendered-dangling.yaml"),
            "--pod-security-profile",
            "restricted",
            "--format",
            "json",
        )
        self.assertEqual(valid.returncode, 0, valid.stdout)
        self.assertEqual(valid.data["status"], "complete")
        self.assertFalse(valid.data["secret_values_emitted"])
        self.assertEqual(dangling.returncode, 1, dangling.stdout)
        self.assertEqual(dangling.data["status"], "failed")
        self.assertFalse(dangling.data["secret_values_emitted"])
        self.assertTrue(any(item["code"] == "dangling-reference" for item in dangling.data["findings"]))

    def test_size_limit_is_enforced_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="yaml-specialist-size-") as temporary:
            path = Path(temporary) / "large.yaml"
            path.write_text("key: " + ("x" * 100) + "\n", encoding="utf-8")
            with self.assertRaises(common.InputError):
                common.load_mapping(path, max_bytes=32)


if __name__ == "__main__":
    unittest.main(verbosity=2)
