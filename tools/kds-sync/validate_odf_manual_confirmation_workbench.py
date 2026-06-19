#!/usr/bin/env python3
"""Validate ODF manual confirmation workbench governance.

This gate checks that the next ODF admission step is queued, bounded, and
blocked until explicit human confirmation. It is read-only and does not
authorize rollout, KDS writes, or business status upgrades by itself.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKBENCH = ROOT / "docs/harness/evidence/odf-phase6-manual-confirmation-workbench-20260618.json"
MAX_SMALL_BATCH_SAMPLES = 5
MAX_OPEN_QUEUE_ITEMS = 3
REQUIRED_TOP_LEVEL_FIELDS = {
    "workbench_id",
    "status",
    "phase",
    "date",
    "max_small_batch_samples",
    "release_allowed",
    "queue_items",
    "guardrails",
}
ALLOWED_WORKBENCH_STATUSES = {
    "phase6_manual_workbench_ready",
    "phase6_manual_workbench_confirmed",
}
REQUIRED_QUEUE_FIELDS = {
    "queue_id",
    "request_id",
    "source_phase",
    "queue_status",
    "owner",
    "requested_by",
    "requested_action",
    "sample_scope",
    "source_paths",
    "odf_paths",
    "kds_sync_paths",
    "rollback_hints",
    "human_confirmation",
    "review_gates",
    "boundary",
}
ALLOWED_QUEUE_STATUSES = {
    "pending_human_confirmation",
    "confirmed_ready_for_future_batch",
    "closed_reference",
}
REQUIRED_REVIEW_GATES = {
    "odf_schema_gate",
    "odf_change_request_gate",
    "odf_manual_confirmation_workbench",
    "document_pollution",
    "kds_token",
    "kds_conflict_guard",
    "kds_directed_sync",
}
REQUIRED_BOUNDARY_FALSE = {
    "full_rollout",
    "accepted",
    "integrated",
    "business_completion_claim",
    "production_write",
    "external_api_write",
}
FORBIDDEN_MARKERS = {
    "full_rollout",
    "accepted",
    "integrated",
    "production_write",
    "external_api_write",
}


def fail(reason: str) -> None:
    raise SystemExit(f"odf_manual_confirmation_workbench=fail reason={reason}")


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing_workbench:{path.relative_to(ROOT).as_posix()}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid_workbench_json:{exc}")


def require_list(value: object, field: str, queue_id: str) -> list:
    if not isinstance(value, list) or not value:
        fail(f"{queue_id}:{field}_must_be_non_empty_list")
    return value


def require_dict(value: object, field: str, queue_id: str) -> dict:
    if not isinstance(value, dict):
        fail(f"{queue_id}:{field}_must_be_object")
    return value


def validate_no_forbidden_markers(value: object, path: str) -> None:
    if isinstance(value, str):
        lowered = value.lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in lowered:
                fail(f"forbidden_marker:{path}:{marker}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            validate_no_forbidden_markers(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            validate_no_forbidden_markers(item, f"{path}.{key}")


def main() -> int:
    workbench = load_json(WORKBENCH)
    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - workbench.keys())
    if missing:
        fail(f"missing_top_level_fields:{','.join(missing)}")
    if workbench.get("status") not in ALLOWED_WORKBENCH_STATUSES:
        fail(f"invalid_status:{workbench.get('status')}")
    if workbench.get("phase") != "ODF Phase 6":
        fail(f"invalid_phase:{workbench.get('phase')}")
    if workbench.get("max_small_batch_samples") != MAX_SMALL_BATCH_SAMPLES:
        fail("max_small_batch_samples_mismatch")
    release_allowed_top = workbench.get("release_allowed")
    if not isinstance(release_allowed_top, bool):
        fail("release_allowed_must_be_bool")

    guardrails = require_dict(workbench.get("guardrails"), "guardrails", "workbench")
    for key in REQUIRED_BOUNDARY_FALSE:
        if guardrails.get(key) is not False:
            fail(f"guardrail_must_be_false:{key}")

    queue_items = workbench.get("queue_items", [])
    if not isinstance(queue_items, list) or not queue_items:
        fail("queue_items_empty")
    if len(queue_items) > MAX_OPEN_QUEUE_ITEMS:
        fail("too_many_open_queue_items")

    seen_queue_ids: set[str] = set()
    pending = 0
    confirmed = 0
    closed = 0
    blocked_release = 0
    total_samples = 0

    for item in queue_items:
        validate_no_forbidden_markers(item, "queue_item")
        queue_id = item.get("queue_id", "<missing>")
        missing = sorted(REQUIRED_QUEUE_FIELDS - item.keys())
        if missing:
            fail(f"{queue_id}:missing_fields:{','.join(missing)}")
        if queue_id in seen_queue_ids:
            fail(f"duplicate_queue_id:{queue_id}")
        seen_queue_ids.add(queue_id)

        queue_status = item.get("queue_status")
        if queue_status not in ALLOWED_QUEUE_STATUSES:
            fail(f"{queue_id}:invalid_queue_status:{queue_status}")
        if queue_status == "pending_human_confirmation":
            pending += 1
        elif queue_status == "confirmed_ready_for_future_batch":
            confirmed += 1
        else:
            closed += 1

        if item.get("requested_action") != "prepare_next_odf_small_batch":
            fail(f"{queue_id}:invalid_requested_action")

        sample_scope = require_dict(item.get("sample_scope"), "sample_scope", queue_id)
        sample_count = sample_scope.get("sample_count")
        if not isinstance(sample_count, int) or sample_count < 1:
            fail(f"{queue_id}:invalid_sample_count")
        if sample_count > MAX_SMALL_BATCH_SAMPLES:
            fail(f"{queue_id}:sample_count_exceeds_limit")
        total_samples += sample_count

        source_paths = require_list(item.get("source_paths"), "source_paths", queue_id)
        odf_paths = require_list(item.get("odf_paths"), "odf_paths", queue_id)
        kds_sync_paths = require_list(item.get("kds_sync_paths"), "kds_sync_paths", queue_id)
        rollback_hints = require_list(item.get("rollback_hints"), "rollback_hints", queue_id)
        if len(source_paths) != sample_count:
            fail(f"{queue_id}:source_path_count_mismatch")
        if len(odf_paths) != sample_count:
            fail(f"{queue_id}:odf_path_count_mismatch")
        if len(rollback_hints) != sample_count:
            fail(f"{queue_id}:rollback_hint_count_mismatch")
        for field, paths in {
            "source_paths": source_paths,
            "odf_paths": odf_paths,
            "kds_sync_paths": kds_sync_paths,
        }.items():
            for path in paths:
                if not isinstance(path, str) or not path:
                    fail(f"{queue_id}:{field}:empty_path")
                if "TOKEN" in path or "token" in path:
                    fail(f"{queue_id}:{field}:path_must_not_reference_token")

        human_confirmation = require_dict(item.get("human_confirmation"), "human_confirmation", queue_id)
        release_allowed = item.get("release_allowed")
        if queue_status == "pending_human_confirmation":
            if human_confirmation.get("confirmed") is not False:
                fail(f"{queue_id}:pending_item_must_not_be_confirmed")
            if release_allowed is not False:
                fail(f"{queue_id}:pending_item_release_must_be_false")
            blocked_release += 1
        if queue_status == "confirmed_ready_for_future_batch":
            if human_confirmation.get("confirmed") is not True:
                fail(f"{queue_id}:confirmed_item_missing_confirmation")
            if not human_confirmation.get("confirmed_by"):
                fail(f"{queue_id}:confirmed_item_missing_confirmed_by")
            if not human_confirmation.get("confirmed_at"):
                fail(f"{queue_id}:confirmed_item_missing_confirmed_at")
            if not human_confirmation.get("confirmation_text"):
                fail(f"{queue_id}:confirmed_item_missing_confirmation_text")
            approved_source_paths = human_confirmation.get("approved_source_paths")
            approved_odf_paths = human_confirmation.get("approved_odf_paths")
            if approved_source_paths != source_paths:
                fail(f"{queue_id}:approved_source_paths_mismatch")
            if approved_odf_paths != odf_paths:
                fail(f"{queue_id}:approved_odf_paths_mismatch")
        if not human_confirmation.get("required_fields"):
            fail(f"{queue_id}:human_confirmation_required_fields_empty")

        review_gates = require_dict(item.get("review_gates"), "review_gates", queue_id)
        for key in REQUIRED_REVIEW_GATES:
            if key not in review_gates:
                fail(f"{queue_id}:missing_review_gate:{key}")

        boundary = require_dict(item.get("boundary"), "boundary", queue_id)
        for key in REQUIRED_BOUNDARY_FALSE:
            if boundary.get(key) is not False:
                fail(f"{queue_id}:boundary_must_be_false:{key}")

    if release_allowed_top is False:
        if pending < 1:
            fail("at_least_one_pending_human_confirmation_item_required")
        if blocked_release < 1:
            fail("no_blocked_release_items")
    else:
        if pending != 0:
            fail("release_allowed_requires_no_pending_items")
        if confirmed < 1:
            fail("release_allowed_requires_confirmed_item")

    print(
        "odf_manual_confirmation_workbench=pass "
        f"queue_items={len(queue_items)} "
        f"pending={pending} "
        f"confirmed_ready={confirmed} "
        f"closed_reference={closed} "
        f"total_samples={total_samples} "
        f"max_small_batch_samples={MAX_SMALL_BATCH_SAMPLES} "
        f"release_allowed={int(release_allowed_top)} "
        "human_confirmation_required=pass "
        "forbidden_rollout=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
