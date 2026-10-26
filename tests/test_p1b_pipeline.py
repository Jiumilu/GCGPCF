from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from p1b_pipeline import run_pipeline

SCRIPT = ROOT / "scripts" / "p1b_pipeline.py"


def complete_demand() -> dict:
    return {
        "sample_id": "SAMPLE-1",
        "type": "demand",
        "source_system": "feedback-center",
        "source_ref_alias": "FB-1",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "out",
        "level": "R3",
        "priority": "P1",
        "evidence_grade": "E2",
        "redaction_level": "R1",
        "authorization": {"approved_by": "老卢"},
        "owner": "Lead",
        "acceptance_criteria": ["demo acceptance"],
        "evidence_refs": {"contract_clause": "HT-A §3.2", "change_request": "CR-1"},
    }


def test_complete_demand_passes_and_final_eligible():
    result = run_pipeline(complete_demand())
    assert result["intake"]["status"] == "pass"
    assert result["grading"]["initial"]["free_paid"] == "paid"
    assert result["grading"]["final"]["final_eligible"] is True


def test_missing_grading_fields_fail_intake():
    doc = complete_demand()
    doc.pop("acceptance_criteria")
    result = run_pipeline(doc)
    assert result["intake"]["status"] == "fail"
    assert any("acceptance_criteria" in item for item in result["intake"]["missing"])
    assert result["grading"]["initial"]["rule_id"] == "FP-00I"


def test_warranty_string_maps_and_complete_defect_passes():
    result = run_pipeline({
        "sample_id": "SAMPLE-2",
        "type": "defect",
        "source_system": "feedback-center",
        "source_ref_alias": "FB-2",
        "customer_alias": "CUST-B",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-B",
        "level": "S2",
        "priority": "P1",
        "evidence_grade": "E2",
        "redaction_level": "R1",
        "authorization": {"approved_by": "老卢"},
        "owner": "Lead",
        "env": "formal",
        "impact": "core report down",
        "description": "demo",
        "reproduce": "demo",
        "warranty": "true",
        "evidence_refs": {"warranty_clause": "HT-B §8.1", "ticket": "TK-1"},
    })
    assert result["intake"]["status"] == "pass"
    assert result["grading"]["initial"]["free_paid"] == "free"
    assert result["grading"]["final"]["final_eligible"] is True


def test_cli_exit_codes(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(json.dumps(complete_demand(), ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(good)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["intake"]["status"] == "pass"

    bad = tmp_path / "bad.json"
    doc = complete_demand()
    doc.pop("acceptance_criteria")
    bad.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(bad)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 1
    assert "acceptance_criteria" in result.stdout


def test_cli_missing_file_exit_two():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", "/tmp/does-not-exist-p1b.json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 2


def test_pipeline_rejects_c1_enum_violations():
    for field, value in (("redaction_level", "R9"), ("evidence_grade", "E9"), ("priority", "P9")):
        doc = complete_demand()
        doc[field] = value
        result = run_pipeline(doc)
        assert result["intake"]["status"] == "fail", field


def test_pipeline_rejects_c1_sensitive_value():
    doc = complete_demand()
    doc["owner"] = "alice@example.com"
    result = run_pipeline(doc)
    assert result["intake"]["status"] == "fail"
    assert any("sensitive" in item for item in result["intake"]["missing"])


def test_pipeline_invalid_type_is_intake_fail_not_exception():
    doc = complete_demand()
    doc["type"] = "incident"
    result = run_pipeline(doc)
    assert result["intake"]["status"] == "fail"
    assert result["grading"] is None


def test_pipeline_missing_formal_scope_fails():
    doc = complete_demand()
    doc.pop("scope")
    result = run_pipeline(doc)
    assert result["intake"]["status"] == "fail"
    assert any("scope" in item for item in result["intake"]["missing"])


def test_pipeline_r2_quota_missing_fails():
    doc = complete_demand()
    doc["scope"] = "in"
    doc["level"] = "R2"
    doc.pop("quota_remaining", None)
    result = run_pipeline(doc)
    assert result["intake"]["status"] == "fail"
    assert any("quota_remaining" in item for item in result["intake"]["missing"])
