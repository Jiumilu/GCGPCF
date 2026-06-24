#!/usr/bin/env python3
"""
COGNEE P1 对照跑：将 headroom 与 cognee 的召回结果转为 harness evidence JSON。
- 只做对照与摘要，不做真实写入。
- 未提供真实 LLM 调用；输入用例文件需包含 headroom 与 cognee 的候选统计。
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
    "retrieval_query_hash",
    "headroom_returned_count",
    "headroom_relevant_count",
    "cognee_returned_count",
    "cognee_relevant_count",
    "token_before",
    "token_after",
    "latency_ms_p95",
    "marker_gate",
    "waes_decision",
    "answer_equivalence",
    "write_requested",
    "write_allowed",
]

REQUIRED_TOP_LEVEL = ["pilot_id", "pilot_round_id", "gate_rules", "cases"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="fixtures/cognee/cognee-p1-recall-comparison-template.json",
        help="input benchmark file",
    )
    parser.add_argument(
        "--output-json",
        default="docs/harness/evidence/cognee-p1-recall-comparison-pilot-20260623.json",
        help="output evidence JSON",
    )
    return parser.parse_args()


def precision(returned_count: int, relevant_count: int) -> float:
    if returned_count <= 0:
        return 0.0
    return min(1.0, relevant_count / returned_count)


def saving_rate(token_before: int, token_after: int) -> float:
    if token_before <= 0:
        return 0.0
    return max(0.0, 1.0 - token_after / token_before)


def retrieval_match(case: dict) -> bool:
    headroom = set(case.get("headroom_top_candidates", []))
    cognee = set(case.get("cognee_top_candidates", []))
    if not headroom and not cognee:
        return False
    overlap = headroom & cognee
    return len(overlap) > 0


def case_to_record(case: dict) -> dict:
    rec = {
        "task_id": case["task_id"],
        "loop_round_id": case["loop_round_id"],
        "project_id": case["project_id"],
        "agent_id": case["agent_id"],
        "model_id": case["model_id"],
        "pilot_phase": case["pilot_phase"],
        "source_tag": case["source_tag"],
        "source_tenant": case["source_tenant"],
        "retrieval_mode": "compare_recall",
        "scenario_id": case["scenario_id"],
        "retrieval_query_hash": case["retrieval_query_hash"],
        "retrieved_count": case["cognee_returned_count"],
        "retrieved_relevant_count": case["cognee_relevant_count"],
        "retrieved_precision": precision(case["cognee_returned_count"], case["cognee_relevant_count"]),
        "marker_gate": case["marker_gate"],
        "waes_decision": case["waes_decision"],
        "answer_equivalence": case["answer_equivalence"],
        "token_before": case["token_before"],
        "token_after": case["token_after"],
        "saving_rate": saving_rate(case["token_before"], case["token_after"]),
        "latency_ms_p95": case["latency_ms_p95"],
        "retrieval_match": retrieval_match(case),
        "headroom_returned_count": case["headroom_returned_count"],
        "headroom_relevant_count": case["headroom_relevant_count"],
        "headroom_precision": precision(case["headroom_returned_count"], case["headroom_relevant_count"]),
        "write_requested": bool(case.get("write_requested", False)),
        "write_allowed": bool(case.get("write_allowed", False)),
        "unauthorized_write_blocked": bool(case.get("write_requested", False)) and not bool(case.get("write_allowed", False)),
        "measured_production_tokens": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
    }
    return rec


def summarize(records: list[dict], gate_rules: dict) -> tuple[bool, dict]:
    recall_precisions = [r["retrieved_precision"] for r in records]
    marker_pass = sum(1 for r in records if r["marker_gate"] == "pass") / max(1, len(records))
    unauthorized_rate = sum(1 for r in records if r["unauthorized_write_blocked"]) / max(1, sum(1 for r in records if r["write_requested"])) if any(r["write_requested"] for r in records) else 1.0

    gate_pass = (
        mean(recall_precisions) >= gate_rules.get("recall_precision_min", 0.85)
        and marker_pass >= gate_rules.get("marker_coverage_min", 0.95)
        and unauthorized_rate >= gate_rules.get("write_block_rate_min", 1.0)
    )

    summary = {
        "record_count": len(records),
        "mean_retrieval_precision": round(mean(recall_precisions), 6) if recall_precisions else 0.0,
        "marker_coverage": round(marker_pass, 6),
        "unauthorized_write_block_rate": round(unauthorized_rate, 6),
        "mean_saving_rate": round(mean([r["saving_rate"] for r in records]) if records else 0.0, 6),
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

    cases = payload.get("cases", [])
    records = []
    for idx, case in enumerate(cases, 1):
        missing = [k for k in REQUIRED_CASE_FIELDS if k not in case]
        if missing:
            raise ValueError(f"Case {idx} missing fields: {missing}")

        records.append(case_to_record(case))

    gate_pass, summary = summarize(records, payload.get("gate_rules", {}))
    status = "pass" if gate_pass else "hold"

    evidence = {
        "schema_id": "globalcloud.cognee_p1_pilot_result.v1",
        "pilot_id": payload["pilot_id"],
        "pilot_round_id": payload["pilot_round_id"],
        "pilot_date": payload.get("pilot_date"),
        "pilot_name": payload.get("pilot_name"),
        "status": status,
        "status_reason": "pass" if status == "pass" else "pilot_threshold_not_reached",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "summary": {
            **summary,
            "gate_rules": payload["gate_rules"],
            "pilot_gate_pass": gate_pass,
        },
        "non_claim_defaults": {
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "validation": {
            "schema": "loop/context/cognee/harness/evidence.schema.yaml",
            "validator": "loop/context/cognee/scripts/validate-cognee-p1-recall-output.py",
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(evidence, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
