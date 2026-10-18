"""Closing a Feature requires a fresh, successful Evidence Gate run."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_close(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("gpcf_close_fresh_gate", ROOT / "scripts/gpcf_close_feature.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_close(tmp_path, monkeypatch):
    module = load_close(monkeypatch)
    active = tmp_path / "features/active"
    feature_dir = active / "F-999-demo"
    feature_dir.mkdir(parents=True)
    data = {
        "id": "F-999", "acceptance": ["Local test passes"],
        "scope": {"in": ["Local change"]},
        "verification": {"tests": ["python3 -m pytest"], "build": ["git diff --check"]},
        "evidence": {"tests": "pass", "build": "pass", "screenshots": "pass", "api": "pass", "summary": "pass"},
        "blockers": [],
    }
    monkeypatch.setattr(module, "ACTIVE", active)
    monkeypatch.setattr(module, "find_feature", lambda feature_id: feature_dir)
    monkeypatch.setattr(module, "feature_file", lambda path: path / "feature.yaml")
    monkeypatch.setattr(module, "read_feature", Mock(return_value=data))
    monkeypatch.setattr(module, "write_feature", Mock())
    monkeypatch.setattr(module, "move_feature_to_done", Mock())
    monkeypatch.setattr(sys, "argv", ["gpcf_close_feature.py", "F-999"])
    return module, data


def test_close_rejects_failed_fresh_evidence_before_status_change(tmp_path, monkeypatch):
    module, _ = prepare_close(tmp_path, monkeypatch)
    run = Mock(return_value=SimpleNamespace(returncode=1, stdout="tests failed", stderr=""))
    monkeypatch.setattr(module.subprocess, "run", run)

    with pytest.raises(SystemExit, match="fresh Evidence Gate failed: tests failed"):
        module.main()

    assert run.call_args.args[0] == [sys.executable, "scripts/gpcf_check_evidence.py", "F-999"]
    module.write_feature.assert_not_called()
    module.move_feature_to_done.assert_not_called()


def test_close_reads_fresh_evidence_result(tmp_path, monkeypatch):
    module, data = prepare_close(tmp_path, monkeypatch)
    failed = {**data, "evidence": {**data["evidence"], "tests": "fail"}}
    module.read_feature.side_effect = [data, failed]
    monkeypatch.setattr(module.subprocess, "run", Mock(return_value=SimpleNamespace(returncode=0, stdout="", stderr="")))

    with pytest.raises(SystemExit, match="evidence gate not complete"):
        module.main()

    assert module.read_feature.call_count == 2
    module.write_feature.assert_not_called()
    module.move_feature_to_done.assert_not_called()
