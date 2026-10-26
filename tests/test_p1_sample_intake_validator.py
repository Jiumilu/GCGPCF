"""P1-C C1：sample-intake 校验器 CLI 行为测试。

覆盖 3 个合成 fixture 的退出码与违规关键字，以及 --help / 不存在路径；
并用 pytest tmp_path 临时 YAML 覆盖敏感粗筛、豁免审计、枚举、类型错误、
level/type 规则与 UnicodeDecodeError。所有数据均为合成数据，不涉及真实样本。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "p1_sample_intake_validator.py"
FIXTURES = ROOT / "tests" / "fixtures"


def run_validator(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def _valid_document() -> Dict[str, Any]:
    text = (FIXTURES / "p1_sample_intake_valid.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(text)


def _write_document(tmp_path: Path, document: Dict[str, Any]) -> Path:
    path = tmp_path / "sample_intake.yaml"
    path.write_text(
        yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return path


def test_valid_fixture_exits_zero() -> None:
    result = run_validator("--file", str(FIXTURES / "p1_sample_intake_valid.yaml"))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[PASS]" in result.stdout
    assert "0 violation(s)" in result.stdout


def test_missing_field_fixture_is_rejected_with_missing_keywords() -> None:
    result = run_validator(
        "--file", str(FIXTURES / "p1_sample_intake_missing_field.yaml")
    )
    assert result.returncode != 0
    assert "[FAIL]" in result.stdout
    assert "missing redaction_level" in result.stdout
    assert "missing owner" in result.stdout


def test_unauthorized_fixture_is_rejected_without_echoing_approver() -> None:
    result = run_validator(
        "--file", str(FIXTURES / "p1_sample_intake_unauthorized.yaml")
    )
    assert result.returncode != 0
    assert "[FAIL]" in result.stdout
    assert "authorization.approved_by must be 老卢" in result.stdout
    assert "none" not in result.stdout


def test_help_lists_file_and_allow_sensitive_options() -> None:
    result = run_validator("--help")
    assert result.returncode == 0
    assert "--file" in result.stdout
    assert "--allow-sensitive" in result.stdout
    assert "FIELD=REASON" in result.stdout


def test_nonexistent_path_exits_with_error() -> None:
    result = run_validator("--file", str(FIXTURES / "does_not_exist.yaml"))
    assert result.returncode != 0
    assert "path does not exist" in result.stderr


@pytest.mark.parametrize(
    ("field", "value", "expected_path"),
    [
        ("notes", "contact me at jane.doe@example.com", "notes"),
        ("contact_phone", "13800138000", "contact_phone"),
        ("session_note", "sk-test-abcdefghijklmnop1234567890", "session_note"),
        ("api_key", "plainvalue123", "api_key"),
    ],
)
def test_sensitive_values_are_rejected(
    tmp_path: Path, field: str, value: str, expected_path: str
) -> None:
    document = _valid_document()
    document[field] = value
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: %s" % expected_path in result.stdout


@pytest.mark.parametrize(
    "phone",
    [
        "+8613800138000",
        "8613800138000",
        "138-0013-8000",
        "138 0013 8000",
    ],
)
def test_phone_variants_are_rejected(tmp_path: Path, phone: str) -> None:
    document = _valid_document()
    document["notes"] = phone
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: notes" in result.stdout


def test_id_card_number_is_rejected(tmp_path: Path) -> None:
    document = _valid_document()
    document["notes"] = "11010519491231002X"
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: notes" in result.stdout


@pytest.mark.parametrize(
    "key",
    [
        "customer_name",
        "contact_name",
        "real_name",
        "id_card",
        "id_number",
        "address",
        "phone",
        "mobile",
        "email",
        "bank_account",
        "contract_no",
        "amount",
        "price",
        "姓名",
        "手机号",
        "电话",
        "身份证",
        "地址",
        "金额",
        "价格",
        "合同号",
    ],
)
def test_sensitive_key_names_are_rejected(tmp_path: Path, key: str) -> None:
    document = _valid_document()
    document[key] = "placeholder-value"
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: %s" % key in result.stdout


def test_jwt_value_is_rejected(tmp_path: Path) -> None:
    document = _valid_document()
    document["notes"] = (
        "eyJhbGciOiJIUzI1NiJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIn0."
        "dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
    )
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: notes" in result.stdout


def test_base64_blob_is_rejected(tmp_path: Path) -> None:
    document = _valid_document()
    document["notes"] = (
        "QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVphYmNkZWZnaGlqa2xtbm9wcXJzdHV2"
        "d3h5ejEyMzQ1Ng=="
    )
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "sensitive field detected: notes" in result.stdout


def test_allow_sensitive_exempts_matching_fields(tmp_path: Path) -> None:
    document = _valid_document()
    document["contact_email"] = "jane.doe@example.com"
    document["contact_phone"] = "13800138000"
    path = _write_document(tmp_path, document)

    blocked = run_validator("--file", str(path))
    assert blocked.returncode != 0
    assert "sensitive field detected: contact_email" in blocked.stdout
    assert "sensitive field detected: contact_phone" in blocked.stdout

    allowed = run_validator(
        "--file",
        str(path),
        "--allow-sensitive",
        "contact_email",
        "--allow-sensitive",
        "contact_phone",
    )
    assert allowed.returncode == 0, allowed.stdout + allowed.stderr
    assert "sensitive field detected" not in allowed.stdout
    assert (
        "[WARN] sensitive exemption: contact_email (reason: not provided)"
        in allowed.stdout
    )


def test_allow_sensitive_without_reason_warns(tmp_path: Path) -> None:
    document = _valid_document()
    document["notes"] = "jane.doe@example.com"
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path), "--allow-sensitive", "notes")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[WARN] sensitive exemption: notes (reason: not provided)" in result.stdout
    assert "sensitive field detected" not in result.stdout


def test_allow_sensitive_with_reason_is_audited(tmp_path: Path) -> None:
    document = _valid_document()
    document["notes"] = "jane.doe@example.com"
    path = _write_document(tmp_path, document)
    result = run_validator(
        "--file", str(path), "--allow-sensitive", "notes=synthetic demo value"
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "[WARN] sensitive exemption: notes (reason: synthetic demo value)"
        in result.stdout
    )
    assert "sensitive field detected" not in result.stdout


@pytest.mark.parametrize(
    ("field", "value", "fragment"),
    [
        (
            "redaction_level",
            "R4",
            "redaction_level must be one of R1, R2, R3",
        ),
        (
            "evidence_grade",
            "E4",
            "evidence_grade must be one of E0, E1, E2, E3",
        ),
        ("priority", "P4", "priority must be one of P0, P1, P2, P3"),
        (
            "layer",
            "global",
            "layer must be one of personal, team, enterprise, city",
        ),
        ("stage", "pilot", "stage must be one of test, trial, formal"),
        ("scope", "external", "scope must be one of in, out, unknown"),
        ("warranty", "yes", "warranty must be one of true, false, unknown"),
    ],
)
def test_enum_values_are_validated(
    tmp_path: Path, field: str, value: str, fragment: str
) -> None:
    document = _valid_document()
    document[field] = value
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert fragment in result.stdout


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("owner", []),
        ("sample_id", {}),
        ("redaction_level", False),
    ],
)
def test_non_string_required_field_is_rejected(
    tmp_path: Path, field: str, value: Any
) -> None:
    document = _valid_document()
    document[field] = value
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert "%s must be a string" % field in result.stdout


def test_authorization_must_be_mapping(tmp_path: Path) -> None:
    document = _valid_document()
    document["authorization"] = ["老卢"]
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0
    assert "authorization must be a mapping" in result.stdout


@pytest.mark.parametrize(
    ("type_value", "level_value", "fragment"),
    [
        ("demand", "S2", "level must match R[1-4] for type=demand"),
        ("defect", "R2", "level must match S[1-4] for type=defect"),
        ("incident", "R3", "type must be one of demand, defect"),
    ],
)
def test_type_and_level_rules(
    tmp_path: Path, type_value: str, level_value: str, fragment: str
) -> None:
    document = _valid_document()
    document["type"] = type_value
    document["level"] = level_value
    path = _write_document(tmp_path, document)
    result = run_validator("--file", str(path))
    assert result.returncode != 0, result.stdout + result.stderr
    assert fragment in result.stdout


def test_undecodable_file_exits_with_code_2(tmp_path: Path) -> None:
    path = tmp_path / "bad_utf8.yaml"
    path.write_bytes(b"sample_id: \xff\xfe\x80\n")
    result = run_validator("--file", str(path))
    assert result.returncode == 2, result.stdout + result.stderr
    assert "invalid UTF-8" in result.stderr
