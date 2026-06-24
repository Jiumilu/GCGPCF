#!/usr/bin/env python3
"""COGNEE P4 真实写入前置预检脚本。"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

REQUIRED_CASE_FIELDS = [
    "task_id",
    "loop_round_id",
    "project_id",
    "agent_id",
    "model_id",
    "pilot_phase",
    "source_tag",
    "source_tenant",
    "scenario_id",
    "operation",
    "caller",
    "tenant_id",
    "owner",
    "payload_tier",
    "harness_evidence_ref",
    "owner_authorization_present",
    "waes_decision",
    "marker_gate",
    "answer_equivalence",
    "write_requested",
    "write_allowed",
    "authorization_token_source",
    "reason_for_request",
    "precheck_passed",
    "expected_blocked_reason",
    "runtime_dependency_ok",
    "rollback_plan_verified",
    "retrieval_query_hash",
    "token_before",
    "token_after",
    "latency_ms_p95",
]

REQUIRED_TOP_LEVEL = ["pilot_id", "pilot_round_id", "gate_rules", "cases"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-p4-real-writeback-precheck-template.json",
        help="input fixture file",
    )
    parser.add_argument(
        "--output-json",
        default="docs/harness/evidence/cognee-p4-real-writeback-precheck-20260623.json",
        help="output evidence JSON",
    )
    return parser.parse_args()


def saving_rate(token_before: int, token_after: int) -> float:
    if token_before <= 0:
        return 0.0
    return max(0.0, 1.0 - token_after / token_before)


def case_to_record(case: dict) -> dict:
    write_requested = bool(case.get("write_requested", False))
    return {
        "task_id": case["task_id"],
        "loop_round_id": case["loop_round_id"],
        "project_id": case["project_id"],
        "agent_id": case["agent_id"],
        "model_id": case["model_id"],
        "pilot_phase": case["pilot_phase"],
        "source_tag": case["source_tag"],
        "source_tenant": case["source_tenant"],
        "retrieval_mode": "write_precheck",
        "scenario_id": case["scenario_id"],
        "operation": case["operation"],
        "caller": case["caller"],
        "tenant_id": case["tenant_id"],
        "owner": case["owner"],
        "payload_tier": case["payload_tier"],
        "harness_evidence_ref": case["harness_evidence_ref"],
        "retrieval_query_hash": case["retrieval_query_hash"],
        "marker_gate": case["marker_gate"],
        "waes_decision": case["waes_decision"],
        "answer_equivalence": case["answer_equivalence"],
        "write_requested": write_requested,
        "write_allowed": bool(case.get("write_allowed", False)),
        "owner_authorization_present": bool(case.get("owner_authorization_present", False)),
        "reason_for_request": case["reason_for_request"],
        "authorization_token_source": case["authorization_token_source"],
        "precheck_passed": bool(case.get("precheck_passed", False)),
        "expected_blocked_reason": case["expected_blocked_reason"],
        "runtime_dependency_ok": bool(case.get("runtime_dependency_ok", False)),
        "rollback_plan_verified": bool(case.get("rollback_plan_verified", False)),
        "token_before": case["token_before"],
        "token_after": case["token_after"],
        "saving_rate": saving_rate(case["token_before"], case["token_after"]),
        "latency_ms_p95": case["latency_ms_p95"],
        "unauthorized_write_blocked": bool(write_requested) and not bool(case.get("write_allowed", False)),
        "measured_production_tokens": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
    }


def summarize(records: list[dict], gate_rules: dict) -> tuple[bool, dict]:
    requested_records = [r for r in records if r["write_requested"]]
    marker_pass_rate = sum(1 for r in records if r["marker_gate"] == "pass") / max(1, len(records))

    precheck_pass_rate = sum(1 for r in requested_records if r["precheck_passed"]) / max(1, len(requested_records))
    owner_auth_rate = sum(1 for r in requested_records if r["owner_authorization_present"]) / max(1, len(requested_records))
    waes_pass_rate = sum(1 for r in requested_records if r["waes_decision"] == "pass") / max(1, len(requested_records))
    runtime_dependency_ok_rate = sum(1 for r in requested_records if r["runtime_dependency_ok"]) / max(1, len(requested_records))
    rollback_readiness_rate = sum(1 for r in requested_records if r["rollback_plan_verified"]) / max(1, len(requested_records))
    token_source_coverage = sum(
        1 for r in requested_records if r["authorization_token_source"] != "none"
    ) / max(1, len(requested_records))
    blocked_records = [r for r in requested_records if not r["write_allowed"]]
    if blocked_records:
        expected_blocked_reason_rate = sum(
            1 for r in blocked_records if r["expected_blocked_reason"] != "none"
        ) / len(blocked_records)
    else:
        expected_blocked_reason_rate = 1.0
    mean_saving = mean(r["saving_rate"] for r in records) if records else 0.0

    gate_pass = (
        precheck_pass_rate >= gate_rules.get("precheck_pass_rate_min", 1.0)
        and owner_auth_rate >= gate_rules.get("owner_authorization_presence_min", 1.0)
        and waes_pass_rate >= gate_rules.get("waes_pass_rate_min", 1.0)
        and runtime_dependency_ok_rate >= gate_rules.get("runtime_dependency_ok_rate_min", 1.0)
        and rollback_readiness_rate >= gate_rules.get("rollback_readiness_rate_min", 1.0)
        and token_source_coverage >= gate_rules.get("authorization_token_source_coverage_min", 1.0)
        and expected_blocked_reason_rate >= gate_rules.get("expected_blocked_reason_rate_min", 1.0)
        and marker_pass_rate >= gate_rules.get("marker_pass_rate_min", 0.95)
    )

    summary = {
        "record_count": len(records),
        "requested_write_count": len(requested_records),
        "precheck_pass_rate": round(precheck_pass_rate, 6),
        "owner_authorization_presence_rate": round(owner_auth_rate, 6),
        "waes_pass_rate": round(waes_pass_rate, 6),
        "runtime_dependency_ok_rate": round(runtime_dependency_ok_rate, 6),
        "rollback_readiness_rate": round(rollback_readiness_rate, 6),
        "authorization_token_source_coverage": round(token_source_coverage, 6),
        "expected_blocked_reason_rate": round(expected_blocked_reason_rate, 6),
        "marker_coverage": round(marker_pass_rate, 6),
        "mean_saving_rate": round(mean_saving, 6),
        "gate_rules": gate_rules,
        "pilot_gate_pass": gate_pass,
    }
    return gate_pass, summary


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output_json)

    with input_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    missing_top = [k for k in REQUIRED_TOP_LEVEL if k not in payload]
    if missing_top:
        raise ValueError(f"Missing top-level fields: {missing_top}")

    records = []
    for idx, case in enumerate(payload["cases"], 1):
        missing = [k for k in REQUIRED_CASE_FIELDS if k not in case]
        if missing:
            raise ValueError(f"Case {idx} missing fields: {missing}")
        records.append(case_to_record(case))

    gate_pass, summary = summarize(records, payload.get("gate_rules", {}))
    status = "pass" if gate_pass else "hold"

    evidence = {
        "schema_id": "globalcloud.cognee_p4_real_writeback_precheck_result.v1",
        "pilot_id": payload["pilot_id"],
        "pilot_round_id": payload["pilot_round_id"],
        "pilot_date": payload.get("pilot_date"),
        "pilot_name": payload.get("pilot_name"),
        "status": status,
        "status_reason": "pass" if status == "pass" else "precheck_gate_not_reached",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "summary": summary,
        "validation": {
            "schema": "loop/context/cognee/harness/evidence-p4.schema.yaml",
            "validator": "loop/context/cognee/scripts/validate-cognee-p4-real-writeback-precheck.py",
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
