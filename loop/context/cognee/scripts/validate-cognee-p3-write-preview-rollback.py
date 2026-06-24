#!/usr/bin/env python3
"""Validate COGNEE P3 write-preview rollback evidence output."""

from __future__ import annotations

import argparse
import json

REQUIRED_TOP_LEVEL = {
    "schema_id",
    "pilot_id",
    "pilot_round_id",
    "status",
    "records",
    "summary",
}

REQUIRED_RECORD_FIELDS = {
    "task_id",
    "loop_round_id",
    "project_id",
    "agent_id",
    "model_id",
    "pilot_phase",
    "source_tag",
    "source_tenant",
    "retrieval_mode",
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
    "expected_blocked_reason",
    "reason_for_request",
    "token_before",
    "token_after",
    "saving_rate",
    "latency_ms_p95",
    "unauthorized_write_blocked",
    "measured_production_tokens",
    "accepted",
    "integrated",
    "production_ready",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="docs/harness/evidence/cognee-p3-write-preview-rollback-20260623.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    miss_top = sorted(REQUIRED_TOP_LEVEL - set(payload.keys()))
    if miss_top:
        raise SystemExit(f"missing top-level fields: {miss_top}")

    records = payload["records"]
    if not isinstance(records, list) or not records:
        raise SystemExit("records must be a non-empty list")

    for i, rec in enumerate(records, 1):
        miss_fields = sorted(REQUIRED_RECORD_FIELDS - set(rec.keys()))
        if miss_fields:
            raise SystemExit(f"record#{i} missing fields: {miss_fields}")

    print("cognee_p3_write_preview_rollback_output=pass")
    print(
        f"record_count={len(records)} "
        f"requested_write_count={payload.get('summary', {}).get('requested_write_count', 0)} "
        f"rollback_block_rate={payload.get('summary', {}).get('rollback_block_rate', 0.0)} "
        f"pilot_gate_pass={payload.get('summary', {}).get('pilot_gate_pass', False)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
