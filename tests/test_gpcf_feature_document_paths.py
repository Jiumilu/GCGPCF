"""Feature documents keep their controlled paths after a workspace move."""

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_moved_feature_rejects_stale_kds_path(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "feature_workspace_paths", ROOT / "tools/kds-sync/validate_gpcf_2_feature_workspace.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    feature = tmp_path / "features/done/F-999-demo"
    feature.mkdir(parents=True)
    document = feature / "journal.md"
    relative = "features/done/F-999-demo/journal.md"
    old_kds = "开发/91-治理与验收/features/active/F-999-demo/journal.md"
    document.write_text(f"---\nsource_path: {relative}\nkds_path: {old_kds}\n---\n\n# Journal\n", encoding="utf-8")

    with pytest.raises(SystemExit, match="feature document kds_path is stale"):
        module.validate_feature_document_paths(feature)

    document.write_text(document.read_text(encoding="utf-8").replace(old_kds, "开发/91-治理与验收/" + relative), encoding="utf-8")
    module.validate_feature_document_paths(feature)
