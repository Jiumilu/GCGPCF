#!/usr/bin/env python3
"""
COGNEE P2 preview 写入对照对齐脚本（受控对照，不进行真实写入）
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
    "retrieval_query_hash",
    "marker_gate",
    "waes_decision",
    "answer_equivalence",
    "write_requested",
    "write_allowed",
    "owner_authorization_present",
    "reason_for_request",
    "token_before",
    "token_after",
    "latency_ms_p95",
]

REQUIRED_TOP_LEVEL = ["pilot_id", "pilot_round_id", "gate_rules", "cases"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-p2-write-preview-template.json",
        help="input fixture file",
    )
    parser.add_argument(
        "--output-json",
        default="docs/harness/evidence/cognee-p2-write-preview-pilot-20260623.json",
        help="output evidence JSON",
    )
    return parser.parse_args()


def saving_rate(token_before: int, token_after: int) -> float:
    if token_before <= 0:
        return 0.0
    return max(0.0, 1.0 - token_after / token_before)


def is_preview_mode(payload_tier: str) -> bool:
    return payload_tier in {"preview", "non_business_only"}


def case_to_record(case: dict) -> dict:
    unauthorized_write_blocked = bool(case.get("write_requested", False)) and not bool(case.get("write_allowed", False))
    return {
        "task_id": case["task_id"],
        "loop_round_id": case["loop_round_id"],
        "project_id": case["project_id"],
        "agent_id": case["agent_id"],
        "model_id": case["model_id"],
        "pilot_phase": case["pilot_phase"],
        "source_tag": case["source_tag"],
        "source_tenant": case["source_tenant"],
        "retrieval_mode": "write_preview",
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
        "write_requested": bool(case.get("write_requested", False)),
        "write_allowed": bool(case.get("write_allowed", False)),
        "owner_authorization_present": bool(case.get("owner_authorization_present", False)),
        "reason_for_request": case["reason_for_request"],
        "token_before": case["token_before"],
        "token_after": case["token_after"],
        "saving_rate": saving_rate(case["token_before"], case["token_after"]),
        "latency_ms_p95": case["latency_ms_p95"],
        "unauthorized_write_blocked": unauthorized_write_blocked,
        "measured_production_tokens": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
    }


def summarize(records: list[dict], gate_rules: dict) -> tuple[bool, dict]:
    requested_records = [r for r in records if r["write_requested"]]
    marker_pass_rate = sum(1 for r in records if r["marker_gate"] == "pass") / max(1, len(records))
    block_rate = sum(
        1 for r in requested_records if r["unauthorized_write_blocked"]
    ) / max(1, len(requested_records))
    auth_rate = sum(
        1 for r in requested_records if r["owner_authorization_present"]
    ) / max(1, len(requested_records))
    waes_pass_rate = sum(
        1 for r in requested_records if r["waes_decision"] == "pass"
    ) / max(1, len(requested_records))
    preview_tier_rate = sum(
        1 for r in requested_records if is_preview_mode(r["payload_tier"])
    ) / max(1, len(requested_records))
    mean_saving = mean(r["saving_rate"] for r in records) if records else 0.0

    gate_pass = (
        block_rate >= gate_rules.get("preview_block_rate_min", 1.0)
        and auth_rate >= gate_rules.get("owner_authorization_presence_min", 1.0)
        and waes_pass_rate >= gate_rules.get("waes_pass_rate_min", 1.0)
        and preview_tier_rate >= gate_rules.get("payload_tier_preview_min", 1.0)
        and marker_pass_rate >= 0.95
    )

    summary = {
        "record_count": len(records),
        "requested_write_count": len(requested_records),
        "preview_block_rate": round(block_rate, 6),
        "owner_authorization_presence_rate": round(auth_rate, 6),
        "waes_pass_rate": round(waes_pass_rate, 6),
        "preview_tier_rate": round(preview_tier_rate, 6),
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
        "schema_id": "globalcloud.cognee_p2_write_preview_result.v1",
        "pilot_id": payload["pilot_id"],
        "pilot_round_id": payload["pilot_round_id"],
        "pilot_date": payload.get("pilot_date"),
        "pilot_name": payload.get("pilot_name"),
        "status": status,
        "status_reason": "pass" if status == "pass" else "pilot_threshold_not_reached",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "summary": summary,
        "validation": {
            "schema": "loop/context/cognee/harness/evidence-p2.schema.yaml",
            "validator": "loop/context/cognee/scripts/validate-cognee-p2-write-preview-output.py",
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
