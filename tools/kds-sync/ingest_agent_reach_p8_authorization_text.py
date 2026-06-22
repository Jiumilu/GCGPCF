#!/usr/bin/env python3
"""Parse human P8 authorization text and delegate safe local authorization creation."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CREATOR = ROOT / "tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
REQUIRED_APPROVER = "lujunxiang"
REQUIRED_CHANNELS = {"web", "rss", "bilibili"}
FORBIDDEN_MARKERS = {
    "写凭据",
    "提取 cookie",
    "写 KDS canonical",
    "写 GFIS source-of-record",
    "改生产配置",
    "改全局 MCP 配置",
    "生产集成",
    "accepted",
    "integrated",
    "production_ready",
}

APPROVER_RE = re.compile(r"授权人[:：]\s*(?P<approver>[A-Za-z0-9_\-]+)")
WINDOW_RE = re.compile(r"有效期[:：]\s*(?P<start>\S+)\s*至\s*(?P<end>\S+)")


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


def load_creator():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_local_authorization_creator", CREATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("creator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def required_texts(request: dict[str, Any]) -> list[str]:
    return [item["required_text"] for item in request.get("batch_authorization_requests", [])]


def parse_authorization_text(text: str, request: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    approver_match = APPROVER_RE.search(text)
    window_match = WINDOW_RE.search(text)
    approver = approver_match.group("approver") if approver_match else None
    authorized_at = window_match.group("start") if window_match else None
    expires_at = window_match.group("end") if window_match else None
    if approver != REQUIRED_APPROVER:
        reasons.append("authorized_by_missing_or_mismatch")
    if not authorized_at or not expires_at:
        reasons.append("authorization_window_missing")
    expected_texts = required_texts(request)
    present_texts = [expected for expected in expected_texts if expected in text]
    missing_texts = [expected for expected in expected_texts if expected not in text]
    if missing_texts:
        reasons.append("required_batch_authorization_text_missing")
    lowered = text.lower()
    channel_mentions = {channel for channel in REQUIRED_CHANNELS if channel in lowered}
    if channel_mentions != REQUIRED_CHANNELS:
        reasons.append("allowed_channels_missing")
    for marker in FORBIDDEN_MARKERS:
        if marker.lower() not in lowered:
            reasons.append(f"forbidden_boundary_missing:{marker}")
    return {
        "authorized_by": approver,
        "authorized_at": authorized_at,
        "expires_at": expires_at,
        "authorization_texts": present_texts,
        "missing_authorization_texts": missing_texts,
        "reasons": sorted(set(reasons)),
    }


def build_report(
    *,
    authorization_text_path: Path,
    write_local_auth: bool,
    authorization_output_dir: Path | None = None,
) -> dict[str, Any]:
    request = load_json(REQUEST)
    text = authorization_text_path.read_text(encoding="utf-8")
    parsed = parse_authorization_text(text, request)
    creator_report: dict[str, Any] | None = None
    status = "rejected"
    if not parsed["reasons"]:
        creator = load_creator()
        creator_report = creator.build_report(
            batch_ids=["p8-batch-1", "p8-batch-2", "p8-batch-3"],
            authorization_texts=parsed["authorization_texts"],
            authorized_at=parsed["authorized_at"],
            expires_at=parsed["expires_at"],
            write_local_auth=write_local_auth,
            authorization_output_dir=authorization_output_dir,
        )
        status = creator_report["status"]
    return {
        "id": "agent-reach-p8-authorization-text-intake",
        "current_admission": "limited_candidate_only",
        "authorization_text_path": display_path(authorization_text_path),
        "write_local_auth_requested": write_local_auth,
        "authorization_output_dir": display_path(authorization_output_dir)
        if authorization_output_dir is not None
        else "default_fixture_path",
        "status": status,
        "parsed_authorization": parsed,
        "creator_report": creator_report,
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
    parser.add_argument("--authorization-text-file", type=Path, required=True)
    parser.add_argument("--write-local-auth", action="store_true")
    parser.add_argument("--authorization-output-dir", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = build_report(
        authorization_text_path=args.authorization_text_file,
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
