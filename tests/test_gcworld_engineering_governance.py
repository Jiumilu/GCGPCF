from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "openspec/changes/gcworld-evidence-twin-foundation/artifacts"
SCHEMA = ARTIFACTS / "gcworld-engineering-governance.schema.json"
FIXTURES = ARTIFACTS / "gcworld-engineering-governance-fixtures.json"
MANIFEST = ARTIFACTS / "gcworld-engineering-governance-contract-manifest.yaml"
VALIDATOR = ROOT / "tools/kds-sync/validate_gcworld_engineering_governance.py"


class GCWorldEngineeringGovernanceTest(unittest.TestCase):
    def test_schema_is_valid_draft_2020_12_and_uses_chinese_title(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertIn("工程与治理", schema["title"])

    def test_manifest_pins_every_contract_artifact(self) -> None:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        for item in manifest["artifacts"]:
            path = ROOT / item["path"]
            self.assertTrue(path.is_file(), path)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_fixture_matrix_covers_engineering_and_governance_boundaries(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("gcworld_engineering_governance=pass", result.stdout)
        self.assertIn("positive=7", result.stdout)
        self.assertIn("negative=21", result.stdout)
        self.assertIn("data_layers=7", result.stdout)
        self.assertIn("storage_roles=7", result.stdout)
        self.assertIn("domain_interfaces=8", result.stdout)
        self.assertIn("observability_metrics=11", result.stdout)
        self.assertIn("delivery_phases=8", result.stdout)
        self.assertIn("determinism_runs=3", result.stdout)
        self.assertIn("real_events=0", result.stdout)
        self.assertIn("external_writes=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
