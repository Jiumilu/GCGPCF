from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA = ARTIFACTS / "gcworld-world-model.schema.json"
VALIDATOR = ROOT / "tools/kds-sync/validate_gcworld_world_model.py"


class GCWorldWorldModelTest(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_fixture_matrix_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("gcworld_world_model=pass", result.stdout)
        self.assertIn("positive=3", result.stdout)
        self.assertIn("negative=4", result.stdout)


if __name__ == "__main__":
    unittest.main()
