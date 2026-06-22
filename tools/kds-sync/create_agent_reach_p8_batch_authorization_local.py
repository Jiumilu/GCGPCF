#!/usr/bin/env python3
"""Create local P8 batch authorization files only after exact human approval."""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST_PATH = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
BATCH_RUNNER_PATH = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py"
BATCH_IDS = {"p8-batch-1", "p8-batch-2", "p8-batch-3"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_iso8601(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone_required")
    return parsed


def load_batch_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_batch_runner", BATCH_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("batch_runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request_by_batch(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["batch_id"]: item for item in request.get("batch_authorization_requests", [])}


def build_authorization(batch_request: dict[str, Any], authorized_at: str, expires_at: str) -> dict[str, Any]:
    fields = dict(batch_request["required_authorization_fields"])
    fields["authorized_at"] = authorized_at
    fields["expires_at"] = expires_at
    return fields


def validate_time_window(authorized_at: str, expires_at: str) -> list[str]:
    reasons: list[str] = []
    try:
        start = parse_iso8601(authorized_at)
    except ValueError as exc:
        return [f"authorized_at_invalid:{exc}"]
    try:
        end = parse_iso8601(expires_at)
    except ValueError as exc:
        return [f"expires_at_invalid:{exc}"]
    if end <= start:
        reasons.append("expires_at_not_after_authorized_at")
    if datetime.now(timezone.utc) > end.astimezone(timezone.utc):
        reasons.append("authorization_expired")
    return reasons


def build_report(
    *,
    batch_ids: list[str],
    authorization_texts: list[str],
    authorized_at: str,
    expires_at: str,
    write_local_auth: bool,
    authorization_output_dir: Path | None = None,
) -> dict[str, Any]:
    request = load_json(REQUEST_PATH)
    batch_runner = load_batch_runner()
    request_map = request_by_batch(request)
    time_reasons = validate_time_window(authorized_at, expires_at)
    reports: dict[str, Any] = {}
    expected_texts = {
        batch_id: request_map[batch_id]["required_text"]
        for batch_id in batch_ids
        if batch_id in request_map
    }
    supplied_texts = set(authorization_texts)
    for batch_id in batch_ids:
        batch_request = request_map.get(batch_id)
        if batch_request is None:
            reports[batch_id] = {
                "status": "rejected",
                "reasons": ["batch_not_in_request_package"],
                "authorization_file_written": False,
            }
            continue
        required_text = batch_request["required_text"]
        reasons = list(time_reasons)
        if required_text not in supplied_texts:
            reasons.append("required_authorization_text_missing")
        auth = build_authorization(batch_request, authorized_at, expires_at)
        default_auth_path = ROOT / batch_request["authorization_file_to_create_after_human_approval"]
        auth_path = (
            authorization_output_dir / default_auth_path.name
            if authorization_output_dir is not None
            else default_auth_path
        )
        runner_ok = False
        runner_reasons: list[str] = []
        if not reasons:
            temp_path = auth_path.with_suffix(".validation.tmp.json")
            write_json(temp_path, auth)
            try:
                plan = batch_runner.load_json(batch_runner.PLAN_PATH)
                batch = batch_runner.batch_by_id(plan, batch_id)
                runner_ok, runner_reasons, _ = batch_runner.validate_authorization(temp_path, plan, batch)
            finally:
                temp_path.unlink(missing_ok=True)
            if not runner_ok:
                reasons.extend(runner_reasons)
        if reasons:
            reports[batch_id] = {
                "status": "rejected",
                "reasons": sorted(set(reasons)),
                "authorization_file": display_path(auth_path),
                "authorization_file_written": False,
            }
            continue
        if write_local_auth:
            write_json(auth_path, auth)
        reports[batch_id] = {
            "status": "local_authorization_written" if write_local_auth else "dry_run_valid",
            "reasons": [],
            "authorization_file": display_path(auth_path),
            "authorization_file_written": write_local_auth,
            "runner_authorization_precheck_passed": runner_ok,
        }
    written_count = sum(1 for report in reports.values() if report.get("authorization_file_written"))
    rejected_count = sum(1 for report in reports.values() if report.get("status") == "rejected")
    valid_count = sum(1 for report in reports.values() if report.get("status") in {"dry_run_valid", "local_authorization_written"})
    return {
        "id": "agent-reach-p8-batch-local-authorization-creator",
        "current_admission": "limited_candidate_only",
        "request_package": display_path(REQUEST_PATH),
        "batch_ids": batch_ids,
        "write_local_auth_requested": write_local_auth,
        "authorization_output_dir": display_path(authorization_output_dir)
        if authorization_output_dir is not None
        else "default_fixture_path",
        "status": "local_authorization_files_written"
        if write_local_auth and written_count == len(batch_ids) and rejected_count == 0
        else "dry_run_valid"
        if not write_local_auth and valid_count == len(batch_ids) and rejected_count == 0
        else "rejected",
        "batch_reports": reports,
        "expected_authorization_texts": expected_texts,
        "security_controls": {
            "live_external_search_invoked": False,
            "agent_reach_binary_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "non_claims": [
            "not_live_search_invoked",
            "not_full_project_group_live_coverage_completed",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-id", action="append", choices=sorted(BATCH_IDS), required=True)
    parser.add_argument("--authorization-text", action="append", default=[])
    parser.add_argument("--authorized-at", required=True)
    parser.add_argument("--expires-at", required=True)
    parser.add_argument("--write-local-auth", action="store_true")
    parser.add_argument("--authorization-output-dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = build_report(
        batch_ids=args.batch_id,
        authorization_texts=args.authorization_text,
        authorized_at=args.authorized_at,
        expires_at=args.expires_at,
        write_local_auth=args.write_local_auth,
        authorization_output_dir=args.authorization_output_dir,
    )
    if args.report:
        write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if report["status"] == "rejected":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
