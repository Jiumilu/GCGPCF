#!/usr/bin/env python3
"""COGNEE P4 真实写入演练/预演脚本。

本脚本默认仅输出 dry-run（预演）结果，不执行真实系统写入。
仅当显式传入 --allow-live-write 时才允许执行写入动作的模拟计数。
"""
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
    "answer_equivalence",
    "write_requested",
    "write_allowed",
    "authorization_token_source",
    "reason_for_request",
    "precheck_passed",
    "expected_blocked_reason",
    "runtime_dependency_ok",
    "rollback_plan_verified",
    "token_before",
    "token_after",
    "latency_ms_p95",
]

REQUIRED_TOP_LEVEL = ["pilot_id", "pilot_round_id", "gate_rules", "cases"]



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json",
        help="input fixture file",
    )
    parser.add_argument(
        "--output-json",
        default="docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json",
        help="output evidence JSON",
    )
    parser.add_argument(
        "--allow-live-write",
        action="store_true",
        help="explicit allow switch for live write execution",
    )
    parser.add_argument(
        "--dry-run-output-only",
        action="store_true",
        default=False,
        help="keep this and --allow-live-write mutually exclusive when true",
    )
    return parser.parse_args()


def saving_rate(token_before: int, token_after: int) -> float:
    if token_before <= 0:
        return 0.0
    return max(0.0, 1.0 - token_after / token_before)


def is_live_ready(case: dict) -> bool:
    return (
        bool(case.get("write_requested", False))
        and bool(case.get("precheck_passed", False))
        and bool(case.get("write_allowed", False))
        and bool(case.get("owner_authorization_present", False))
        and bool(case.get("runtime_dependency_ok", False))
        and bool(case.get("rollback_plan_verified", False))
        and str(case.get("waes_decision", "")).lower() == "pass"
        and str(case.get("expected_blocked_reason", "")).strip().lower() == "none"
    )


def case_to_record(case: dict, allow_live_write: bool, dry_run_output_only: bool) -> dict:
    live_ready = is_live_ready(case)
    if dry_run_output_only:
        write_executed = False
        production_write = False
        actual_execution_status = "dry_run"
    else:
        write_executed = bool(allow_live_write and live_ready)
        production_write = bool(write_executed)
        actual_execution_status = (
            "executed" if write_executed else "blocked_by_policy_or_precheck"
        )

    return {
        "task_id": case["task_id"],
        "loop_round_id": case["loop_round_id"],
        "project_id": case["project_id"],
        "agent_id": case["agent_id"],
        "model_id": case["model_id"],
        "pilot_phase": case["pilot_phase"],
        "source_tag": case["source_tag"],
        "source_tenant": case["source_tenant"],
        "retrieval_mode": "writeback_live_execution",
        "scenario_id": case["scenario_id"],
        "operation": case["operation"],
        "caller": case["caller"],
        "tenant_id": case["tenant_id"],
        "owner": case["owner"],
        "payload_tier": case["payload_tier"],
        "harness_evidence_ref": case["harness_evidence_ref"],
        "authorization_token_source": case["authorization_token_source"],
        "reason_for_request": case["reason_for_request"],
        "precheck_passed": bool(case.get("precheck_passed", False)),
        "expected_blocked_reason": case["expected_blocked_reason"],
        "runtime_dependency_ok": bool(case.get("runtime_dependency_ok", False)),
        "rollback_plan_verified": bool(case.get("rollback_plan_verified", False)),
        "owner_authorization_present": bool(case.get("owner_authorization_present", False)),
        "waes_decision": case["waes_decision"],
        "answer_equivalence": case["answer_equivalence"],
        "write_requested": bool(case.get("write_requested", False)),
        "write_allowed": bool(case.get("write_allowed", False)),
        "live_execution_ready": live_ready,
        "write_executed": write_executed,
        "production_write": production_write,
        "execution_status": actual_execution_status,
        "token_before": case["token_before"],
        "token_after": case["token_after"],
        "saving_rate": saving_rate(case["token_before"], case["token_after"]),
        "latency_ms_p95": case["latency_ms_p95"],
        "retrieved": datetime.now(timezone.utc).isoformat(),
    }


def summarize(records: list[dict]) -> tuple[bool, dict]:
    requested_records = [r for r in records if r["write_requested"]]
    requested_count = len(requested_records)
    live_ready_count = sum(1 for r in requested_records if r["live_execution_ready"])
    executed_count = sum(1 for r in records if r["write_executed"])
    production_write_count = sum(1 for r in records if r["production_write"])
    unknown_block_reason_count = sum(
        1
        for r in requested_records
        if r["write_requested"] and str(r["expected_blocked_reason"]).strip().lower() != "none"
    )

    live_ready_rate = live_ready_count / max(1, requested_count)
    block_due_blocked_reason_rate = (
        unknown_block_reason_count / max(1, requested_count) if requested_count else 0.0
    )

    summary = {
        "record_count": len(records),
        "requested_write_count": requested_count,
        "live_execution_ready_rate": round(live_ready_rate, 6),
        "live_execution_ready_count": live_ready_count,
        "execution_count": executed_count,
        "production_write_count": production_write_count,
        "blocked_due_expected_reason_rate": round(block_due_blocked_reason_rate, 6),
        "mean_saving_rate": round(mean(r["saving_rate"] for r in records), 6) if records else 0.0,
        "gate_rules": {
            "live_execution_ready_rate_min": 1.0,
            "blocked_due_expected_reason_rate_max": 0.0,
            "production_write_allowed": True,
        },
        "pilot_gate_pass": live_ready_rate >= 1.0 and block_due_blocked_reason_rate <= 0.0,
    }

    return summary["pilot_gate_pass"], summary


def main() -> int:
    args = parse_args()

    if args.allow_live_write and args.dry_run_output_only:
        raise ValueError("--allow-live-write and --dry-run-output-only cannot both be true")

    input_path = Path(args.input)
    output_path = Path(args.output_json)

    with input_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    missing_top = [k for k in REQUIRED_TOP_LEVEL if k not in payload]
    if missing_top:
        raise ValueError(f"Missing top-level fields: {missing_top}")

    records: list[dict] = []
    for idx, case in enumerate(payload["cases"], 1):
        missing = [k for k in REQUIRED_CASE_FIELDS if k not in case]
        if missing:
            raise ValueError(f"Case {idx} missing fields: {missing}")
        records.append(
            case_to_record(
                case,
                allow_live_write=args.allow_live_write,
                dry_run_output_only=args.dry_run_output_only or (not args.allow_live_write),
            )
        )

    pilot_gate_pass, summary = summarize(records)

    if args.allow_live_write:
        status = "pass" if pilot_gate_pass else "hold"
        status_reason = "pass" if status == "pass" else "live_execution_gate_not_reached"
    else:
        status = "pass" if pilot_gate_pass else "hold"
        status_reason = "dry_run_ready"

    evidence = {
        "schema_id": "globalcloud.cognee_p4_real_writeback_live_result.v1",
        "pilot_id": payload["pilot_id"],
        "pilot_round_id": payload["pilot_round_id"],
        "pilot_date": payload.get("pilot_date"),
        "pilot_name": payload.get("pilot_name"),
        "status": status,
        "status_reason": status_reason,
        "allow_live_write": bool(args.allow_live_write),
        "dry_run_output_only": bool(args.dry_run_output_only) or (not args.allow_live_write),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "summary": summary,
        "validation": {
            "schema": "loop/context/cognee/harness/evidence-p4-live.schema.yaml",
            "validator": "loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py",
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
