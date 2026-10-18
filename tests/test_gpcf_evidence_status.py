"""The workspace validator rejects legacy evidence placeholders."""

import importlib.util
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_feature_workspace_rejects_not_required(tmp_path, monkeypatch):
    path = ROOT / "tools/kds-sync/validate_gpcf_2_feature_workspace.py"
    spec = importlib.util.spec_from_file_location("feature_workspace_status", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)

    feature = tmp_path / "features/active/F-999-invalid-evidence"
    (feature / "evidence").mkdir(parents=True)
    (feature / "artifacts").mkdir()
    data = yaml.safe_load((ROOT / "features/done/F-002-project-group-feature-queue/feature.yaml").read_text())
    data["evidence"]["tests"] = "not_required"
    (feature / "feature.yaml").write_text(yaml.safe_dump(data, allow_unicode=True))
    (feature / "journal.md").write_text("这轮做什么 改了什么 怎么验证 发现什么问题 是否可以提交")

    with pytest.raises(SystemExit, match="unsupported evidence status tests=not_required"):
        module.validate_feature_dir(feature)
