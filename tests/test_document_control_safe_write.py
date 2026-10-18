"""Document-control writes must stay within an explicit, non-destructive scope."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_control():
    spec = importlib.util.spec_from_file_location("document_control_safe_write", ROOT / "tools/kds-sync/document_control.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_arg_write_is_refused_without_mutation():
    paths = [ROOT / "09-status/globalcloud-document-control-register.md", ROOT / ".kds/local-mirror-ledger.jsonl"]
    before = [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]
    result = subprocess.run([sys.executable, "tools/kds-sync/document_control.py"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "--apply-full" in result.stderr
    assert before == [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]


def test_scoped_register_replaces_only_its_row():
    control = load_control()
    previous = "# Register\n\n| doc_id | title | source_path | project |\n| --- | --- | --- | --- |\n| A | Old | docs/a.md | GPCF |\n| B | Keep | docs/b.md | GPCF |\n"
    generated = previous.replace("| A | Old |", "| A | Updated |")
    assert control.merge_scoped_register(previous, generated, {"docs/a.md"}) == previous.replace("| A | Old |", "| A | Updated |")


def test_scoped_register_refuses_new_document_without_full_reconciliation():
    control = load_control()
    with pytest.raises(ValueError, match="membership changed"):
        control.merge_scoped_register("| doc_id | source_path |\n", "| doc_id | source_path |\n| A | docs/new.md |\n", {"docs/new.md"})


def test_scoped_register_refuses_project_count_change():
    control = load_control()
    previous = "| A | Title | docs/a.md | GPCF | GPCF | status | controlled | 开发/12-GPCF/docs/a.md |\n"
    generated = previous.replace("| GPCF | GPCF |", "| KDS | GPCF |")
    with pytest.raises(ValueError, match="totals may change"):
        control.merge_scoped_register(previous, generated, {"docs/a.md"})


def test_scoped_mirror_keeps_unrelated_ledger_entry(tmp_path, monkeypatch):
    control = load_control()
    monkeypatch.setattr(control, "ROOT", tmp_path)
    source = tmp_path / "docs/current.md"
    source.parent.mkdir()
    source.write_text("current\n")
    ledger = tmp_path / ".kds/local-mirror-ledger.jsonl"
    ledger.parent.mkdir()
    old = {"source_path": "docs/historical.md", "kds_path": "开发/91-治理与验收/docs/historical.md", "status": "mirrored"}
    ledger.write_text(json.dumps(old) + "\n")
    control.mirror_scope_to_kds([{"source_path": "docs/current.md", "kds_path": "开发/91-治理与验收/docs/current.md", "doc_id": "CURRENT"}])
    entries = [json.loads(line) for line in ledger.read_text().splitlines()]
    assert {entry["source_path"] for entry in entries} == {"docs/historical.md", "docs/current.md"}


def test_full_mirror_does_not_delete_unrelated_file(tmp_path, monkeypatch):
    control = load_control()
    monkeypatch.setattr(control, "ROOT", tmp_path)
    source = tmp_path / "docs/current.md"
    source.parent.mkdir()
    source.write_text("current\n")
    unrelated = tmp_path / ".kds/development-space/开发/91-治理与验收/legacy.md"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("retain\n")
    ledger = tmp_path / ".kds/local-mirror-ledger.jsonl"
    ledger.write_text(json.dumps({"source_path": "docs/historical.md", "status": "mirrored"}) + "\n")
    control.mirror_to_kds([{"source_path": "docs/current.md", "kds_path": "开发/91-治理与验收/docs/current.md", "doc_id": "CURRENT"}])
    assert unrelated.read_text() == "retain\n"
    assert {json.loads(line)["source_path"] for line in ledger.read_text().splitlines()} == {"docs/historical.md", "docs/current.md"}
