#!/usr/bin/env python3
"""Validate P9S source-direct local authorization file safety."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.request.json"
TEMPLATE = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.template.json"
LOCAL_AUTH = ROOT / "fixtures/agent-reach/p9-source-direct-hit-rate-authorization.local.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_source_direct_authorization_file_safety=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git_ls_files(path: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "--", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if proc.returncode != 0:
        fail("git_ls_files_failed")
    return [line for line in proc.stdout.splitlines() if line.strip()]


def git_status_short(path: Path) -> str:
    proc = subprocess.run(
        ["git", "status", "--short", "--", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if proc.returncode != 0:
        fail("git_status_failed")
    return proc.stdout.strip()


def git_check_ignore(path: Path) -> bool:
    proc = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", path.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if proc.returncode == 0:
        return True
    if proc.returncode == 1:
        return False
    fail("git_check_ignore_failed")


def is_placeholder(value: object) -> bool:
    return isinstance(value, str) and value.startswith("<required-") and value.endswith(">")


def build_report() -> dict[str, Any]:
    request = read_json(REQUEST)
    template = read_json(TEMPLATE)
    if request.get("status") != "p9_source_direct_authorization_request_ready":
        fail("authorization_request_not_ready")

    local_tracked_paths = git_ls_files(LOCAL_AUTH)
    template_tracked_paths = git_ls_files(TEMPLATE)
    local_present = LOCAL_AUTH.exists()
    local_tracked = bool(local_tracked_paths)
    local_ignored = git_check_ignore(LOCAL_AUTH)
    if local_tracked:
        fail("local_authorization_file_tracked_by_git")
    if not local_ignored:
        fail("local_authorization_file_not_git_ignored")

    template_placeholders = {
        "authorized_by": is_placeholder(template.get("authorized_by")),
        "authorized_at": is_placeholder(template.get("authorized_at")),
        "expires_at": is_placeholder(template.get("expires_at")),
    }
    template_executable = not all(template_placeholders.values())
    if template_executable:
        fail("authorization_template_is_executable")

    expected_local = request.get("authorization_file_to_create_after_human_approval")
    if expected_local != LOCAL_AUTH.relative_to(ROOT).as_posix():
        fail("authorization_request_local_path_mismatch")

    return {
        "id": "agent-reach-p9-source-direct-authorization-file-safety-20260626",
        "date": "2026-06-26",
        "status": "p9_source_direct_authorization_file_safety_ready",
        "current_admission": "limited_candidate_only",
        "mode": "authorization_file_safety_only",
        "authorization_request_status": request.get("status"),
        "local_authorization_file": LOCAL_AUTH.relative_to(ROOT).as_posix(),
        "local_authorization_file_present": local_present,
        "local_authorization_file_tracked": local_tracked,
        "local_authorization_file_git_ignored": local_ignored,
        "local_authorization_git_status": git_status_short(LOCAL_AUTH),
        "template_file": TEMPLATE.relative_to(ROOT).as_posix(),
        "template_file_present": TEMPLATE.exists(),
        "template_file_tracked": bool(template_tracked_paths),
        "template_git_status": git_status_short(TEMPLATE),
        "template_authorization_valid": False,
        "template_placeholder_fields": template_placeholders,
        "authorization_file_policy": {
            "local_authorization_must_not_be_tracked_by_git": True,
            "local_authorization_must_be_git_ignored": True,
            "template_must_remain_non_executable_until_human_filled": True,
            "live_execution_requires_separate_authorization_intake_pass": True,
        },
        "security_controls": {
            "live_external_fetch_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
        "completion_claim_allowed": False,
        "non_claims": [
            "authorization_file_safety_only",
            "not_live_fetch_invoked",
            "not_authorization_intake_passed",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P9-SOURCE-DIRECT-AUTH-FILE-SAFETY-20260626",
            "title: Agent-Reach P9S Source Direct Authorization File Safety 2026-06-26",
            "project: KDS",
            "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.md",
            "source_path: docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-26",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P9S Source Direct Authorization File Safety 2026-06-26",
            "",
            f"- status: `{report['status']}`",
            f"- local_authorization_file_present: `{report['local_authorization_file_present']}`",
            f"- local_authorization_file_tracked: `{report['local_authorization_file_tracked']}`",
            f"- local_authorization_file_git_ignored: `{report['local_authorization_file_git_ignored']}`",
            f"- template_authorization_valid: `{report['template_authorization_valid']}`",
            f"- live_external_fetch_invoked: `{report['security_controls']['live_external_fetch_invoked']}`",
            f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
            "",
            "## Boundary",
            "",
            "- This evidence validates authorization file safety only.",
            "- This evidence does not invoke live target-site fetch.",
            "- The local authorization file must not be tracked by git.",
            "- The local authorization file path must be protected by git ignore.",
            "- The template remains non-executable until a human replaces placeholder fields.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_source_direct_authorization_file_safety=pass "
        f"status={report['status']} local_auth_present={str(report['local_authorization_file_present']).lower()} "
        "live_external_fetch_invoked=false"
    )


if __name__ == "__main__":
    main()
