#!/usr/bin/env python3
"""Validate Cognee P4 live writeback authorization signoff evidence."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SIGNOFF_MD = ROOT / "docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md"
DEFAULT_LIVE_JSON = ROOT / "docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json"
DEFAULT_SIGNOFF_JSON = ROOT / "fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json"

OWNER_FIELDS = [
    "owner_signer_name",
    "owner_signer_role",
    "owner_signer_token_source",
    "owner_signed_at",
    "owner_decision",
    "owner_decision_evidence",
]

WAES_FIELDS = [
    "waes_signer_name",
    "waes_signer_role",
    "waes_signed_at",
    "waes_decision",
    "waes_runtime_dependency_ok",
    "waes_rollback_plan_verified",
]

WINDOW_FIELDS = [
    "signoff_window_start_at",
    "signoff_window_expires_at",
]

REQUIRED_FALSE_FIELDS = [
    "production_write",
    "accepted",
    "integrated",
    "production_ready",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_SIGNOFF_MD), help="signoff evidence markdown path")
    parser.add_argument("--live-evidence", default=str(DEFAULT_LIVE_JSON), help="live evidence json path")
    parser.add_argument("--signoff-json", default=str(DEFAULT_SIGNOFF_JSON), help="machine-readable signoff payload")
    parser.add_argument(
        "--require-complete-signoff",
        action="store_true",
        help="fail unless all signoff fields are filled and the authorization window is valid",
    )
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def parse_table_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        if parts[0] in {"字段", "item"}:
            continue
        if set(parts[0]) == {"-"}:
            continue
        key = parts[0]
        value = parts[1]
        values[key] = value
    return values


def parse_iso8601(value: str) -> datetime | None:
    if not value or value == "REQUIRED_USER_INPUT":
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def as_bool(value: str) -> bool | None:
    if isinstance(value, bool):
        return value
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def flatten_signoff_payload(payload: dict) -> dict[str, str | bool]:
    rows: dict[str, str | bool] = {}
    rows.update(payload.get("owner_signoff", {}))
    rows.update(payload.get("waes_signoff", {}))
    rows.update(payload.get("signoff_window", {}))
    rows.update(payload.get("required_false_until_completed", {}))
    return rows


def main() -> int:
    args = parse_args()
    signoff_path = Path(args.input).resolve()
    live_path = Path(args.live_evidence).resolve()
    signoff_json_path = Path(args.signoff_json).resolve()
    signoff_text = read_text(signoff_path)
    live = load_json(live_path)
    signoff_payload = load_json(signoff_json_path)
    rows = parse_table_values(signoff_text)
    payload_rows = flatten_signoff_payload(signoff_payload)

    require("validate_cognee_p4_live_authorization_signoff.py" in signoff_text, "validator reference missing from signoff evidence")
    require("cognee-p4-live-authorization-signoff.pending.json" in signoff_text, "machine-readable signoff payload reference missing from signoff evidence")
    require(signoff_payload.get("package_id") == "COGNEE-P4-LIVE-AUTHORIZATION-SIGNOFF-PACKAGE-20260625", "invalid signoff package_id")
    require(
        signoff_payload.get("instance_status") in {"pending_human_signoff", "signoff_complete_ready_for_fixed_command_pack"},
        "instance_status must be pending_human_signoff or signoff_complete_ready_for_fixed_command_pack",
    )

    summary = live.get("summary", {})
    require(live.get("status") == "pass", "live evidence status must be pass")
    require(summary.get("record_count") == 5, "record_count must be 5")
    require(summary.get("requested_write_count") == 5, "requested_write_count must be 5")
    require(summary.get("execution_count") == 5, "execution_count must be 5")
    require(summary.get("live_execution_ready_rate") == 1.0, "live_execution_ready_rate must be 1.0")
    require(summary.get("pilot_gate_pass") is True, "pilot_gate_pass must be true")

    md_authorization_complete = as_bool(rows.get("authorization_complete", ""))
    payload_authorization_complete = as_bool(payload_rows.get("authorization_complete", False))
    require(
        (md_authorization_complete is False and payload_authorization_complete is False)
        or (md_authorization_complete is True and payload_authorization_complete is True)
        or args.require_complete_signoff,
        "authorization_complete must be synchronized between markdown and payload",
    )
    for field in REQUIRED_FALSE_FIELDS:
        require(as_bool(rows.get(field, "")) is False, f"{field} must remain false")
        require(as_bool(payload_rows.get(field, False)) is False, f"{field} must remain false in signoff payload")

    for field in OWNER_FIELDS + WAES_FIELDS + WINDOW_FIELDS + ["authorization_complete"]:
        md_value = rows.get(field, "")
        payload_value = payload_rows.get(field, "")
        if isinstance(payload_value, bool):
            require(as_bool(md_value) == payload_value or field in OWNER_FIELDS + WAES_FIELDS + WINDOW_FIELDS, f"markdown/payload mismatch: {field}")
        else:
            normalized_payload = str(payload_value)
            require(md_value == normalized_payload, f"markdown/payload mismatch: {field}")

    all_required = OWNER_FIELDS + WAES_FIELDS + WINDOW_FIELDS
    placeholders = [field for field in all_required if rows.get(field, "") == "REQUIRED_USER_INPUT"]

    if args.require_complete_signoff:
        require(not placeholders, f"required fields still unresolved: {','.join(placeholders)}")
        require(rows.get("owner_decision") == "approve_live_write", "owner_decision must be approve_live_write")
        require(rows.get("waes_decision") == "pass", "waes_decision must be pass")
        require(as_bool(rows.get("waes_runtime_dependency_ok", "")) is True, "waes_runtime_dependency_ok must be true")
        require(as_bool(rows.get("waes_rollback_plan_verified", "")) is True, "waes_rollback_plan_verified must be true")
        require(as_bool(rows.get("authorization_complete", "")) is True, "authorization_complete must be true after signoff")
        require(signoff_payload.get("instance_status") == "signoff_complete_ready_for_fixed_command_pack", "instance_status must indicate completed signoff")

        window_start = parse_iso8601(rows.get("signoff_window_start_at", ""))
        window_end = parse_iso8601(rows.get("signoff_window_expires_at", ""))
        owner_signed_at = parse_iso8601(rows.get("owner_signed_at", ""))
        waes_signed_at = parse_iso8601(rows.get("waes_signed_at", ""))

        require(window_start is not None, "signoff_window_start_at must be valid iso8601")
        require(window_end is not None, "signoff_window_expires_at must be valid iso8601")
        require(owner_signed_at is not None, "owner_signed_at must be valid iso8601")
        require(waes_signed_at is not None, "waes_signed_at must be valid iso8601")
        require(window_end > window_start, "signoff_window_expires_at must be after signoff_window_start_at")
        require(window_start <= owner_signed_at <= window_end, "owner_signed_at must be within signoff window")
        require(window_start <= waes_signed_at <= window_end, "waes_signed_at must be within signoff window")

        print(
            "cognee_p4_live_authorization_signoff=pass_complete "
            "authorization_complete=true owner_decision=approve_live_write waes_decision=pass "
            "runtime_dependency_ok=true rollback_plan_verified=true "
            "production_write=false accepted=false integrated=false production_ready=false"
        )
        return 0

    current_status = signoff_payload.get("instance_status")
    completion_flag = payload_authorization_complete
    if not placeholders and completion_flag is True and current_status == "signoff_complete_ready_for_fixed_command_pack":
        print(
            "cognee_p4_live_authorization_signoff=pass_complete "
            "missing_required_field_count=0 missing_required_fields=none "
            "authorization_complete=true production_write=false accepted=false integrated=false production_ready=false"
        )
        return 0

    print(
        "cognee_p4_live_authorization_signoff=pass_pending "
        f"missing_required_field_count={len(placeholders)} "
        f"missing_required_fields={','.join(placeholders) if placeholders else 'none'} "
        "authorization_complete=false production_write=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
