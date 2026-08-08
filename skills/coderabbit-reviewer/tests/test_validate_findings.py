#!/usr/bin/env python3
"""Deterministic tests for the CodeRabbit NDJSON validator."""

from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_PATH = ROOT / "scripts" / "validate_findings.py"
FIXTURES = ROOT / "tests" / "fixtures"

spec = importlib.util.spec_from_file_location("coderabbit_validate_findings", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load validate_findings.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidateFindingsTests(unittest.TestCase):
    def validate_fixture(self, name: str, **kwargs):
        return validator.validate_path(str(FIXTURES / name), **kwargs)

    def validate_text(self, text: str, **kwargs):
        return validator.validate_binary_stream(io.BytesIO(text.encode("utf-8")), **kwargs)

    def test_complete_stream(self) -> None:
        result = self.validate_fixture("complete.ndjson", process_exit_code=0)
        self.assertFalse(result.audit.errors)
        self.assertEqual(validator.outcome_for(result), "complete")
        self.assertEqual(result.findings_observed, 2)
        self.assertEqual(result.terminal_findings, 2)
        self.assertEqual(result.severity_counts["major"], 1)
        self.assertEqual(result.severity_counts["minor"], 1)

    def test_skipped_stream_is_not_clean_completion(self) -> None:
        result = self.validate_fixture("skipped.ndjson", process_exit_code=0)
        self.assertFalse(result.audit.errors)
        self.assertEqual(validator.outcome_for(result), "review_skipped")
        self.assertEqual(result.findings_observed, 0)

    def test_error_stream_is_structurally_valid_but_review_failed(self) -> None:
        result = self.validate_fixture("error.ndjson", process_exit_code=1)
        self.assertFalse(result.audit.errors)
        self.assertEqual(validator.outcome_for(result), "review_error")
        self.assertEqual(result.terminal_type, "error")

    def test_unknown_event_warns_in_compatible_mode(self) -> None:
        result = self.validate_fixture("unknown-event.ndjson")
        self.assertFalse(result.audit.errors)
        self.assertTrue(result.audit.warnings)
        self.assertEqual(result.unknown_event_counts.get("future_progress"), 1)

    def test_unknown_event_fails_in_strict_mode(self) -> None:
        result = self.validate_fixture("unknown-event.ndjson", strict=True)
        self.assertTrue(result.audit.errors)
        self.assertEqual(validator.outcome_for(result), "invalid")

    def test_malformed_json_fails(self) -> None:
        result = self.validate_fixture("malformed.ndjson")
        self.assertTrue(any("invalid JSON" in item for item in result.audit.errors))

    def test_event_after_terminal_fails(self) -> None:
        result = self.validate_fixture("post-terminal.ndjson")
        self.assertTrue(any("after terminal" in item for item in result.audit.errors))

    def test_terminal_count_mismatch_fails(self) -> None:
        result = self.validate_text(
            '{"type":"review_context"}\n'
            '{"type":"finding","severity":"major","fileName":"src/a.py","comment":"Issue"}\n'
            '{"type":"complete","status":"completed","findings":0}\n'
        )
        self.assertTrue(any("finding event(s) were observed" in item for item in result.audit.errors))

    def test_escaping_finding_path_fails(self) -> None:
        result = self.validate_text(
            '{"type":"review_context"}\n'
            '{"type":"finding","severity":"minor","fileName":"../secret","comment":"Issue"}\n'
            '{"type":"complete","status":"completed","findings":1}\n'
        )
        self.assertTrue(any("traverse parent" in item for item in result.audit.errors))

    def test_complete_with_nonzero_process_exit_fails(self) -> None:
        result = self.validate_fixture("complete.ndjson", process_exit_code=7)
        self.assertTrue(any("stream terminates with complete" in item for item in result.audit.errors))

    def test_missing_terminal_fails(self) -> None:
        result = self.validate_text('{"type":"review_context"}\n{"type":"heartbeat"}\n')
        self.assertTrue(any("no terminal" in item for item in result.audit.errors))

    def test_size_limit_fails_closed(self) -> None:
        result = self.validate_text(
            '{"type":"review_context"}\n{"type":"complete","findings":0}\n',
            max_bytes=10,
        )
        self.assertTrue(any("maximum size" in item for item in result.audit.errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
