#!/usr/bin/env python3
"""Validate Headroom production-token intake gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-PRODUCTION-TOKEN-INTAKE-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_production_token_intake_gate.py"
LEDGER_TEMPLATE = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
LEDGER_TEMPLATE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_template.py"
LEDGER_EVALUATOR = ROOT / "tools/kds-sync/evaluate_headroom_production_token_ledger.py"
LEDGER_NEGATIVE_FIXTURES = ROOT / "fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json"
LEDGER_NEGATIVE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py"
AUTHORIZATION_PACKAGE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
AUTHORIZATION_PACKAGE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_package.py"
AUTHORIZATION_ACTION_QUEUE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
AUTHORIZATION_ACTION_QUEUE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_action_queue.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    ledger_template = load_json(LEDGER_TEMPLATE)
    ledger_template_validator = read(LEDGER_TEMPLATE_VALIDATOR)
    ledger_evaluator = read(LEDGER_EVALUATOR)
    ledger_negative_fixtures = load_json(LEDGER_NEGATIVE_FIXTURES)
    ledger_negative_validator = read(LEDGER_NEGATIVE_VALIDATOR)
    authorization_package = load_json(AUTHORIZATION_PACKAGE)
    authorization_package_validator = read(AUTHORIZATION_PACKAGE_VALIDATOR)
    authorization_action_queue = load_json(AUTHORIZATION_ACTION_QUEUE)
    authorization_action_queue_validator = read(AUTHORIZATION_ACTION_QUEUE_VALIDATOR)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("authorized_window_required" in runner, "runner must define authorization prerequisite")
    require("provider_billing_export_or_sanitized_runtime_usage_ledger" in runner, "runner must define token source")

    require(evidence.get("evidence_id") == "HEADROOM-PRODUCTION-TOKEN-INTAKE-GATE-20260621", "invalid evidence id")
    require(evidence.get("status") == "production_token_intake_gate_defined_blocking", "invalid status")
    require(evidence.get("ledger_template") == LEDGER_TEMPLATE.relative_to(ROOT).as_posix(), "ledger template path mismatch")
    require(evidence.get("ledger_template_validator") == LEDGER_TEMPLATE_VALIDATOR.relative_to(ROOT).as_posix(), "ledger template validator path mismatch")
    require(evidence.get("ledger_evaluator") == LEDGER_EVALUATOR.relative_to(ROOT).as_posix(), "ledger evaluator path mismatch")
    require(evidence.get("ledger_negative_fixtures") == LEDGER_NEGATIVE_FIXTURES.relative_to(ROOT).as_posix(), "ledger negative fixtures path mismatch")
    require(evidence.get("ledger_negative_validator") == LEDGER_NEGATIVE_VALIDATOR.relative_to(ROOT).as_posix(), "ledger negative validator path mismatch")
    require(evidence.get("authorization_package") == AUTHORIZATION_PACKAGE.relative_to(ROOT).as_posix(), "authorization package path mismatch")
    require(evidence.get("authorization_package_validator") == AUTHORIZATION_PACKAGE_VALIDATOR.relative_to(ROOT).as_posix(), "authorization package validator path mismatch")
    require(evidence.get("authorization_action_queue") == AUTHORIZATION_ACTION_QUEUE.relative_to(ROOT).as_posix(), "authorization action queue path mismatch")
    require(evidence.get("authorization_action_queue_validator") == AUTHORIZATION_ACTION_QUEUE_VALIDATOR.relative_to(ROOT).as_posix(), "authorization action queue validator path mismatch")
    require(ledger_template.get("measured_production_tokens") is False, "ledger template must not claim production tokens")
    require("admission_gate" in ledger_template_validator, "ledger template validator must evaluate admission gate")
    require("evaluate_ledger" in ledger_evaluator, "ledger evaluator must expose evaluate_ledger")
    require(len(ledger_negative_fixtures.get("cases", [])) >= 5, "negative fixture set too small")
    require("negative case was accepted" in ledger_negative_validator, "negative validator must fail accepted negative cases")
    require(authorization_package.get("authorization", {}).get("status") == "pending", "authorization package must remain pending")
    require("authorization_package_gate" in authorization_package_validator, "authorization package validator must check gate")
    require(authorization_action_queue.get("gate", {}).get("authorization_action_queue_gate") is False, "authorization action queue must remain blocked")
    require("authorization_action_queue_gate" in authorization_action_queue_validator, "authorization action queue validator must check gate")
    prerequisites = evidence.get("prerequisites", {})
    require(prerequisites.get("telemetry_required") == "off", "telemetry must remain off")
    require(prerequisites.get("raw_prompt_storage") == "forbidden", "raw prompt storage must be forbidden")
    require(prerequisites.get("kds_write_allowed") is False, "KDS write must remain false")
    require(prerequisites.get("external_api_write_allowed") is False, "external API write must remain false")
    for field in [
        "measurement_id",
        "authorized_window_id",
        "input_tokens_before",
        "input_tokens_after",
        "answer_equivalence",
        "sensitive_redaction_gate",
    ]:
        require(field in evidence.get("required_measurement_fields", []), f"missing required measurement field: {field}")

    gate = evidence.get("gate", {})
    require(gate.get("production_source_present") is False, "production source must not be claimed")
    require(gate.get("sanitized_usage_ledger_present") is False, "sanitized usage ledger must not be claimed")
    require(gate.get("authorized_window_present") is False, "authorized window must not be claimed")
    require(gate.get("telemetry_off_enforced") is True, "telemetry off must be enforced")
    require(gate.get("no_sensitive_raw_text_stored") is True, "raw text must not be stored")
    require(gate.get("independent_replay_gate") is True, "independent replay prerequisite must pass")
    require(gate.get("authorization_action_queue_gate") is False, "authorization action queue must remain blocked")
    require(gate.get("production_token_intake_gate") is False, "production token intake must remain blocked")
    require(gate.get("production_admission_gate") is False, "production admission must remain false")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-PRODUCTION-TOKEN-INTAKE-GATE-20260621",
        "production_token_intake_gate | false",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "headroom-production-token-ledger-template.json",
        "headroom-production-token-ledger-negative-fixtures.json",
        "headroom-production-token-authorization-package-20260621.json",
        "headroom-production-token-authorization-action-queue-20260621.json",
        "不得申请 L3.5/L4 admission、accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_production_token_intake_gate.py" in loop_round, "loop round missing runner")
    require("validate_headroom_production_token_intake_gate.py" in loop_round, "loop round missing validator")
    print(
        "headroom_production_token_intake_gate=pass "
        "production_token_intake_gate=false "
        "measured_production_tokens=false "
        "production_admission_gate=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
