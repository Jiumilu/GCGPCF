"""Feature closure keeps document locations aligned with the moved workspace."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_move_feature_updates_document_paths_without_changing_body(tmp_path, monkeypatch):
    path = ROOT / "scripts/gpcf_feature_lib.py"
    spec = importlib.util.spec_from_file_location("gpcf_feature_move", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    active = tmp_path / "features/active/F-999-demo"
    done = tmp_path / "features/done"
    (active / "evidence").mkdir(parents=True)
    done.mkdir(parents=True)
    old = "features/active/F-999-demo/"
    body = "# Journal\n\nHistorical reference: features/active/F-999-demo/\n"
    (active / "journal.md").write_text(
        f"---\nsource_path: {old}journal.md\n"
        f"kds_path: 开发/91-治理与验收/{old}journal.md\n"
        "last_reviewed: 2026-10-01\n---\n\n" + body,
        encoding="utf-8",
    )
    (active / "evidence/summary.md").write_text(
        f"---\nsource_path: {old}evidence/summary.md\n"
        f"kds_path: 开发/91-治理与验收/{old}evidence/summary.md\n---\n\n# Evidence\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "DONE", done)
    target = module.move_feature_to_done(active)
    assert target == done / active.name
    journal = (target / "journal.md").read_text(encoding="utf-8")
    summary = (target / "evidence/summary.md").read_text(encoding="utf-8")
    assert "source_path: features/done/F-999-demo/journal.md" in journal
    assert "kds_path: 开发/91-治理与验收/features/done/F-999-demo/journal.md" in journal
    assert "last_reviewed: 2026-10-01" in journal
    assert journal.endswith(body)
    assert "source_path: features/done/F-999-demo/evidence/summary.md" in summary
    assert "kds_path: 开发/91-治理与验收/features/done/F-999-demo/evidence/summary.md" in summary
