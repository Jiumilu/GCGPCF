#!/usr/bin/env python3
"""Audit P8 local authorization windows without running live search."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-local-authorization-window-audit-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-local-authorization-window-audit-20260623.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_local_authorization_window_audit=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_batch_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def default_local_auth_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request["batch_authorization_requests"]]


def request_for_batch(request: dict[str, Any], batch_id: str) -> dict[str, Any]:
    for item in request["batch_authorization_requests"]:
        if item["batch_id"] == batch_id:
            return item
    fail(f"batch_request_missing:{batch_id}")


def make_auth(request: dict[str, Any], batch_id: str, start: datetime, end: datetime, *, auth_batch_id: str | None = None) -> dict[str, Any]:
    fields = dict(request_for_batch(request, batch_id)["required_authorization_fields"])
    fields["authorized_at"] = start.isoformat()
    fields["expires_at"] = end.isoformat()
    if auth_batch_id is not None:
        fields["batch_id"] = auth_batch_id
    return fields


def write_auth(path: Path, auth: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(auth, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def scenario_report(runner, batch_id: str, auth_path: Path, execute: bool = False) -> dict[str, Any]:
    report = runner.build_report(batch_id, auth_path, execute=execute)
    return {
        "status": report.get("status"),
        "authorization_valid": report.get("authorization_valid"),
        "authorization_reasons": report.get("authorization_reasons", []),
        "live_external_search_invoked": report.get("security_controls", {}).get("live_external_search_invoked"),
    }


def build_report() -> dict[str, Any]:
    runner = load_runner()
    request = load_json(REQUEST)
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_exists:{path.relative_to(ROOT)}")
    now = datetime.now(timezone.utc)
    with tempfile.TemporaryDirectory(prefix="agent-reach-p8-auth-window-") as tmpdir:
        tmp = Path(tmpdir)
        missing = scenario_report(runner, "p8-batch-1", tmp / "missing.local.json")
        current_auth = write_auth(
            tmp / "current.local.json",
            make_auth(request, "p8-batch-1", now - timedelta(minutes=10), now + timedelta(hours=2)),
        )
        future_auth = write_auth(
            tmp / "future.local.json",
            make_auth(request, "p8-batch-1", now + timedelta(hours=2), now + timedelta(hours=4)),
        )
        expired_auth = write_auth(
            tmp / "expired.local.json",
            make_auth(request, "p8-batch-1", now - timedelta(hours=4), now - timedelta(hours=2)),
        )
        wrong_batch_auth = write_auth(
            tmp / "wrong-batch.local.json",
            make_auth(request, "p8-batch-1", now - timedelta(minutes=10), now + timedelta(hours=2), auth_batch_id="p8-batch-2"),
        )
        scenarios = {
            "missing_file": missing,
            "current_window": scenario_report(runner, "p8-batch-1", current_auth),
            "future_window": scenario_report(runner, "p8-batch-1", future_auth),
            "expired_window": scenario_report(runner, "p8-batch-1", expired_auth),
            "wrong_batch": scenario_report(runner, "p8-batch-1", wrong_batch_auth),
        }
    expectations = {
        "missing_file": "authorization_file_missing",
        "future_window": "authorization_not_yet_active",
        "expired_window": "authorization_expired",
        "wrong_batch": "batch_id_mismatch",
    }
    for name, reason in expectations.items():
        if reason not in scenarios[name]["authorization_reasons"]:
            fail(f"scenario_reason_missing:{name}:{reason}")
        if scenarios[name]["live_external_search_invoked"] is not False:
            fail(f"scenario_invoked_live_search:{name}")
    if scenarios["current_window"]["authorization_valid"] is not True:
        fail("current_window_not_valid")
    if scenarios["current_window"]["status"] != "authorized_execution_not_requested":
        fail("current_window_status_mismatch")
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_created:{path.relative_to(ROOT)}")
    return {
        "id": "agent-reach-p8-local-authorization-window-audit-20260623",
        "round": "GPCF-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-001",
        "date": "2026-06-23",
        "status": "p8_local_authorization_window_audit_pass",
        "current_admission": "limited_candidate_only",
        "scenario_results": scenarios,
        "default_local_authorization_files_created": False,
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
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }


def render_markdown(report: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| {name} | `{row['status']}` | `{row['authorization_valid']}` | `{', '.join(row['authorization_reasons'])}` |"
        for name, row in report["scenario_results"].items()
    )
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-20260623",
            "title: Agent-Reach P8 Local Authorization Window Audit 2026-06-23",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-local-authorization-window-audit-20260623.md",
            "source_path: docs/harness/evidence/agent-reach-p8-local-authorization-window-audit-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 Local Authorization Window Audit 2026-06-23",
            "",
            f"- status: `{report['status']}`",
            f"- current_admission: `{report['current_admission']}`",
            f"- default_local_authorization_files_created: `{report['default_local_authorization_files_created']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "本轮审计 P8 batch runner 对本地授权文件时间窗和批次范围的阻断行为，只使用临时授权文件，不执行真实搜索。",
            "",
            "## stop",
            "",
            "停止类型为 `authorization_boundary`。正式授权前默认 `.local.json` 不存在，真实搜索仍不得执行。",
            "",
            "## verify",
            "",
            "| scenario | status | authorization_valid | reasons |",
            "|---|---|---|---|",
            rows,
            "",
            "## recover",
            "",
            "删除本轮 evidence、loop 文档和 validator 即可回滚；本轮不写默认授权文件。",
            "",
            "## debug",
            "",
            "- 新增阻断：`authorization_not_yet_active`。",
            "- 继续执行仍需正式 P8 三批授权。",
            "",
            "## 非声明",
            "",
            "- 本证据不声明全量真实搜索已完成。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-001",
            "title: Agent-Reach P8 Local Authorization Window Audit Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LOCAL-AUTHORIZATION-WINDOW-AUDIT-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 Local Authorization Window Audit Loop 001",
            "",
            "## run",
            "",
            "审计 P8 本地授权时间窗和批次范围阻断。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"真实外搜 `{report['security_controls']['live_external_search_invoked']}`；默认授权文件创建 `{report['default_local_authorization_files_created']}`。",
            "",
            "## recover",
            "",
            "本轮仅使用临时授权文件；删除新增审计文件即可回滚。",
            "",
            "## debug",
            "",
            "继续执行仍需正式 P8 三批授权。",
            "",
        ]
    )


def validate_written(report: dict[str, Any]) -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("id") != report["id"]:
        fail("written_evidence_id_mismatch")
    for marker in [
        "p8_local_authorization_window_audit_pass",
        "authorization_not_yet_active",
        "authorization_expired",
        "batch_id_mismatch",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    validate_written(report)
    print(
        "agent_reach_p8_local_authorization_window_audit=pass "
        "status=p8_local_authorization_window_audit_pass "
        "future_window=blocked expired_window=blocked wrong_batch=blocked "
        "default_local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
