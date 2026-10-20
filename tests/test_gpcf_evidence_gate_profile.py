"""F-003: the Evidence Gate must require scope evidence or explicit waivers."""

import copy
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("ui_api_scope", "with_waivers", "expected", "expected_rc"),
    [
        (False, False, "fail", 1),
        (False, True, "waived", 0),
        (True, False, "fail", 1),
    ],
)
def test_scope_evidence_requires_proof_or_reason(tmp_path, monkeypatch, ui_api_scope, with_waivers, expected, expected_rc):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_check_evidence as gate

    active = tmp_path / "active"
    feature_dir = active / "F-003-sample"
    feature_dir.mkdir(parents=True)
    data = {
        "id": "F-003", "name": "evidence-gate-profile", "project": "gpcf",
        "goal": "Check local evidence", "scope": {"in": ["UI and API" if ui_api_scope else "local scripts"]},
        "acceptance": ["Evidence Gate reports actual results"], "blockers": [],
        "loop": {"current_step": "evaluate", "iteration": 1},
        "verification": {
            "tests": ["python3 -c 'print(1)'"],
            "build": ["python3 -c 'print(1)'"],
            "waivers": {"screenshots": "No UI", "api": "No external API"} if with_waivers else {},
        },
    }
    written = []
    commands = []
    monkeypatch.setattr(gate, "ACTIVE", active)
    monkeypatch.setattr(gate, "find_feature", lambda _: feature_dir)
    monkeypatch.setattr(gate, "feature_file", lambda _: feature_dir / "feature.yaml")
    monkeypatch.setattr(gate, "read_feature", lambda _: copy.deepcopy(data))
    monkeypatch.setattr(gate, "write_feature", lambda _, value: written.append(copy.deepcopy(value)))
    monkeypatch.setattr(gate, "run_command", lambda command: (commands.append(command) or ("pass", "command passed")))
    monkeypatch.setattr(gate, "update_queue_entry", lambda *args, **kwargs: None)
    monkeypatch.setattr(gate, "append_runtime_log", lambda *args, **kwargs: None)
    monkeypatch.setattr(gate, "append_journal", lambda *args, **kwargs: None)
    monkeypatch.setattr(sys, "argv", ["gpcf_check_evidence.py", "F-003"])

    assert gate.main() == expected_rc
    result = written[0]["evidence"]
    assert (result["screenshots"], result["api"]) == (expected, expected)
    assert result["summary"] == ("pass" if expected_rc == 0 else "fail")
    assert "not_required" not in result.values()
    assert sum(command[:2] == ["python3", "-c"] for command in commands) == 2
    summary = (feature_dir / "evidence/summary.md").read_text(encoding="utf-8")
    assert summary.startswith("---\ndoc_id: GPCF-DOC-F003-EVIDENCE-SUMMARY\n")
    assert "source_path: features/active/F-003-sample/evidence/summary.md" in summary
    assert "status: draft\n" in summary
    assert "last_reviewed: unreviewed\n" in summary


def test_ui_evidence_ignores_build_file_but_accepts_named_ui_note(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    import gpcf_check_evidence as gate

    feature_dir = tmp_path / "F-003-sample"
    evidence_dir = feature_dir / "evidence"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "build.txt").write_text("build passed\n")
    assert gate.detect_ui_evidence(feature_dir, evidence_dir)[0] == "fail"
    (evidence_dir / "ui-browser.txt").write_text("browser trace\n")
    assert gate.detect_ui_evidence(feature_dir, evidence_dir)[0] == "pass"
