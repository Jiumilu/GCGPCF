"""Replay F-005's declared local Runtime role-chain acceptance."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runtime/logs/F-005.jsonl"


def test_f005_runtime_log_has_all_declared_roles():
    events = [json.loads(line) for line in LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert events
    assert all(event["feature_id"] == "F-005" for event in events)
    assert {"Dispatcher", "Planner", "Builder", "Evaluator", "Repair", "Recorder"} <= {
        event["role"] for event in events
    }


def test_passing_evidence_does_not_mark_active_sample_closable(tmp_path, monkeypatch, capsys):
    import sys
    import yaml
    import pytest

    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_check_evidence as gate

    active = tmp_path / "active"
    feature_dir = active / "F-005-sample"
    feature_dir.mkdir(parents=True)
    data = yaml.safe_load((ROOT / "features/active/F-005-factory-exception-intake-dry-run/feature.yaml").read_text(encoding="utf-8"))
    data["blockers"] = []
    data["loop"]["current_step"] = "commit"
    monkeypatch.setattr(gate, "ACTIVE", active)
    monkeypatch.setattr(gate, "find_feature", lambda _: feature_dir)
    monkeypatch.setattr(gate, "feature_file", lambda _: feature_dir / "feature.yaml")
    monkeypatch.setattr(gate, "read_feature", lambda _: data)
    monkeypatch.setattr(gate, "run_command", lambda _: ("pass", "ok"))
    monkeypatch.setattr(gate, "run_declared_commands", lambda *_: [("feature command", "pass", "ok")])
    monkeypatch.setattr(gate, "write_feature", lambda *_: None)
    monkeypatch.setattr(gate, "update_queue_entry", lambda *_, **__: pytest.fail("active sample queue position changed"))
    monkeypatch.setattr(gate, "append_runtime_log", lambda *_, **__: None)
    journal_answers = []
    monkeypatch.setattr(gate, "append_journal", lambda *_, **kwargs: journal_answers.extend(kwargs["answers"]))
    monkeypatch.setattr(sys, "argv", ["gpcf_check_evidence.py", "F-005"])

    assert gate.main() == 0
    assert "close_candidate=false" in capsys.readouterr().out
    assert data["status"] == "active"
    assert data["loop"]["current_step"] == "commit"
    assert "保持 active" in journal_answers[-1]
