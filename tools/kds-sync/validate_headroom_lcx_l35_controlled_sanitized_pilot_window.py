#!/usr/bin/env python3
"""Validate the Headroom LCX L3.5 controlled sanitized pilot window."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_l35_controlled_sanitized_pilot_window.py"

PROJECTS = {
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
}


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("用户回复：批准" in runner, "runner must record current-session approval signal")
    require("allow production" not in runner.lower(), "runner must not allow production")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622", "invalid evidence id")
    require(evidence.get("status") == "l3_5_controlled_sanitized_pilot_window_pass_check_only", "invalid status")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("scenario_count") == 3, "scenario count mismatch")
    require(evidence.get("entry_count") == 45, "entry count mismatch")
    require(evidence.get("pilot_smoke_record_count") == 45, "pilot smoke record count mismatch")
    require(evidence.get("failures") == [], "failures must be empty")

    authorization = evidence.get("authorization", {})
    require(authorization.get("authorized_window_id") == "HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001", "invalid window id")
    require(authorization.get("authorized_by") == "user_current_codex_session", "invalid authorized_by")
    require(str(authorization.get("authorized_at", "")).startswith("2026-06-22T"), "invalid authorized_at")
    require(authorization.get("authorization_complete_for_l3_5") is True, "L3.5 authorization must be complete")
    require(authorization.get("authorization_complete_for_l4_l5_or_production") is False, "production authorization must be false")
    require(authorization.get("sanitized_production_token_ledger") == "fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json", "wrong ledger")
    require(authorization.get("rollback_plan_id") == "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001", "wrong rollback plan")
    require(authorization.get("waes_harness_admission_decision") == "admitted_for_l3_5_sanitized_pilot_only", "wrong WAES/Harness decision")

    records = evidence.get("pilot_smoke_records", [])
    require(isinstance(records, list) and len(records) == 45, "pilot records mismatch")
    require({record.get("project_id") for record in records} == PROJECTS, "pilot project coverage mismatch")
    for record in records:
        for key in [
            "task_id",
            "loop_round_id",
            "project_id",
            "agent_id",
            "model_id",
            "mode",
            "content_type",
            "tokens_before",
            "tokens_after",
            "tokens_saved",
            "saving_rate",
            "ccr_enabled",
            "ccr_retrieve_count",
            "policy_profile",
            "waes_decision",
            "answer_equivalence",
            "marker_gate",
            "sensitive_redaction_gate",
            "measured_production_tokens",
            "accepted",
            "integrated",
            "production_ready",
        ]:
            require(key in record, f"pilot record missing key: {key}")
        require(record["tokens_saved"] == "not_calculated", "tokens_saved must not be calculated")
        require(record["saving_rate"] == "not_calculated", "saving_rate must not be calculated")
        require(record["answer_equivalence"] == "not_measured", "answer equivalence must not be measured")
        for key in ["measured_production_tokens", "accepted", "integrated", "production_ready"]:
            require(record[key] is False, f"record field must be false: {key}")

    gates = evidence.get("gates", {})
    for key in [
        "l3_5_pilot_window_generated",
        "authorization_complete_for_l3_5",
        "readiness_gate",
        "negative_gate_pass",
        "replay_stability_gate",
        "project_coverage_gate",
        "pilot_smoke_gate",
        "telemetry_off",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "authorization_complete_for_l4_l5_or_production",
        "raw_prompt_storage",
        "raw_completion_storage",
        "unredacted_sensitive_material_processed",
        "headroom_learn_apply_executed",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "database_migration",
        "permission_change",
        "l4_candidate",
        "l5_candidate",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622",
        "authorized_window_id: `HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001`",
        "authorization_complete_for_l3_5 | true",
        "authorization_complete_for_l4_l5_or_production | false",
        "pilot_smoke_gate | true",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in ["run:", "stop:", "verify:", "recover:", "debug:"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")
    require("validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_l35_controlled_sanitized_pilot_window=pass_check_only "
        "authorized_window_id=HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001 "
        "project_count=15 pilot_smoke_record_count=45 l4_candidate=false "
        "measured_production_tokens=false production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
