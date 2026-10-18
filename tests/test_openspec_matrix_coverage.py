from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/kds-sync/validate_project_group_openspec_coverage.py"
MATRIX = ROOT / "09-status/globalcloud-project-group-openspec-applicability-matrix.md"


@pytest.mark.parametrize(
    ("added_row", "expected_failure"),
    [
        (
            "| Project | project | required | `openspec/changes/project-<change>/` | `gpcf_new_feature --project project` | Governance | required | required |",
            "duplicate project row: Project",
        ),
        (
            "| Ghost | ghost | required | `openspec/changes/ghost-<change>/` | `gpcf_new_feature --project ghost` | Governance | required | required |",
            "matrix has unexpected projects: ['Ghost']",
        ),
    ],
)
def test_matrix_rejects_duplicate_and_unregistered_rows(tmp_path, monkeypatch, capsys, added_row, expected_failure):
    spec = importlib.util.spec_from_file_location("openspec_coverage", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    matrix = tmp_path / "matrix.md"
    matrix.write_text(MATRIX.read_text(encoding="utf-8").replace("## 状态边界", added_row + "\n\n## 状态边界"), encoding="utf-8")
    monkeypatch.setattr(module, "MATRIX", matrix)

    assert module.main() == 1
    result = json.loads(capsys.readouterr().out)
    assert expected_failure in result["failures"]
