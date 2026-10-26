from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from p1b_grading_engine import grade_document, load_document

SCRIPT = ROOT / "scripts" / "p1b_grading_engine.py"
FIXTURES = ROOT / "tests" / "fixtures" / "p1b"


@pytest.mark.parametrize(
    "name, initial_paid, initial_rule, final_paid, final_grade, final_eligible",
    [
        ("demand_e2.json", "paid", "FP-03", "paid", "E2", True),
        ("demand_e1.json", "paid", "FP-03", "pending", "E1", False),
        ("defect_e2.json", "free", "FP-01", "free", "E2", True),
        ("defect_e1.json", "free", "FP-01", "pending", "E1", False),
        ("demand_test.json", "free", "FP-04", "free", "E1", False),
        ("demand_trial.json", "included", "FP-05", "included", "E1", False),
    ],
)
def test_fixture_results(name, initial_paid, initial_rule, final_paid, final_grade, final_eligible):
    result = grade_document(load_document(FIXTURES / name))
    assert result["initial"]["free_paid"] == initial_paid
    assert result["initial"]["rule_id"] == initial_rule
    assert result["final"]["free_paid"] == final_paid
    assert result["final"]["evidence_grade"] == final_grade
    assert result["final"]["final_eligible"] is final_eligible


def test_missing_fields_pending_fp00i():
    result = grade_document({"case_id": "X", "type": "demand"})
    assert result["initial"]["free_paid"] == "pending"
    assert result["initial"]["rule_id"] == "FP-00I"
    assert result["initial"]["evidence_grade"] == "E0"
    assert result["final"]["rule_id"] == "FP-00F"


def test_formal_scope_in_r1_pending_for_fp07_decision():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "in",
        "requirement_level": "R1",
        "acceptance_criteria": ["ok"],
        "evidence_refs": {"contract_clause": "HT-A §3.1"},
    })
    assert result["initial"]["free_paid"] == "pending"
    assert result["initial"]["rule_id"] == "FP-00I"
    assert any("R1" in item for item in result["initial"]["unknown"])


def test_formal_scope_out_r1_pending_for_fp07_decision():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "none",
        "scope": "out",
        "requirement_level": "R1",
        "acceptance_criteria": ["ok"],
    })
    assert result["initial"]["free_paid"] == "pending"
    assert result["initial"]["rule_id"] == "FP-00I"
    assert any("R1" in item for item in result["initial"]["unknown"])


def test_formal_scope_in_r2_quota_true_included_fp02():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "in",
        "requirement_level": "R2",
        "acceptance_criteria": ["ok"],
        "quota_remaining": True,
        "evidence_refs": {"contract_clause": "HT-A §3.1"},
    })
    assert result["initial"]["free_paid"] == "included"
    assert result["initial"]["rule_id"] == "FP-02"
    assert result["final"]["final_eligible"] is True


def test_formal_scope_in_r2_quota_false_paid_fp03():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "in",
        "requirement_level": "R2",
        "acceptance_criteria": ["ok"],
        "quota_remaining": False,
        "evidence_refs": {"contract_clause": "HT-A §3.1"},
    })
    assert result["initial"]["free_paid"] == "paid"
    assert result["initial"]["rule_id"] == "FP-03"


def test_formal_scope_in_r2_quota_missing_pending():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "in",
        "requirement_level": "R2",
        "acceptance_criteria": ["ok"],
        "evidence_refs": {"contract_clause": "HT-A §3.1"},
    })
    assert result["initial"]["free_paid"] == "pending"
    assert any("quota_remaining" in item for item in result["initial"]["unknown"])


def test_defect_out_of_warranty_paid_fp03():
    result = grade_document({
        "case_id": "X",
        "type": "defect",
        "feedback_ref": "FB-1",
        "env": "formal",
        "severity": "S3",
        "warranty": False,
        "description": "demo",
        "reproduce": "demo",
        "impact": "demo",
        "evidence_refs": {"warranty_clause": "HT-A §8.1", "ticket": "TK-1"},
    })
    assert result["initial"]["free_paid"] == "paid"
    assert result["initial"]["rule_id"] == "FP-03"
    assert result["final"]["free_paid"] == "paid"
    assert result["final"]["final_eligible"] is True


def test_c1_schema_mapping_sample_id_level_source_ref_alias_warranty_string():
    result = grade_document({
        "sample_id": "SAMPLE-1",
        "type": "defect",
        "source_ref_alias": "FB-ALIAS-1",
        "env": "formal",
        "level": "S2",
        "warranty": "true",
        "description": "demo",
        "reproduce": "demo",
        "impact": "demo",
        "evidence_refs": {"warranty_clause": "HT-A §8.1", "ticket": "TK-1"},
    })
    assert result["case_id"] == "SAMPLE-1"
    assert result["level"] == "S2"
    assert result["initial"]["free_paid"] == "free"
    assert result["final"]["final_eligible"] is True


def test_warranty_int_is_rejected_not_treated_as_true():
    result = grade_document({
        "case_id": "X",
        "type": "defect",
        "feedback_ref": "FB-1",
        "env": "formal",
        "severity": "S2",
        "warranty": 1,
        "description": "demo",
        "reproduce": "demo",
        "impact": "demo",
    })
    assert result["initial"]["free_paid"] == "pending"
    assert any("warranty" in item for item in result["initial"]["unknown"])


def test_evidence_refs_string_does_not_crash():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "HT-A",
        "scope": "out",
        "requirement_level": "R3",
        "acceptance_criteria": ["ok"],
        "evidence_refs": "not-a-mapping",
    })
    assert result["initial"]["free_paid"] == "paid"
    assert result["final"]["free_paid"] == "pending"
    assert result["final"]["rule_id"] == "FP-00F"


def test_formal_in_r2_without_contract_pending():
    result = grade_document({
        "case_id": "X",
        "type": "demand",
        "customer_alias": "CUST-A",
        "layer": "enterprise",
        "stage": "formal",
        "contract_alias": "none",
        "scope": "in",
        "requirement_level": "R2",
        "acceptance_criteria": ["ok"],
    })
    assert result["initial"]["free_paid"] == "pending"
    assert result["initial"]["rule_id"] == "FP-00I"


def test_cli_outputs_json_and_exit_zero():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(FIXTURES / "demand_e2.json")],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["case_id"] == "ENG-DEM-E2"
    assert data["final"]["final_eligible"] is True


def test_cli_missing_file_exit_two():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(FIXTURES / "nope.json")],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 2
    assert "file not found" in result.stderr


def test_cli_output_missing_dir_exit_two(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--file",
            str(FIXTURES / "demand_e2.json"),
            "--output",
            str(tmp_path / "missing" / "out.json"),
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert result.returncode == 2
    assert "output directory not found" in result.stderr
