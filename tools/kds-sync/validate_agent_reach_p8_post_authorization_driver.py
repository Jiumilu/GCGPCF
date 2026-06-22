#!/usr/bin/env python3
"""Validate the P8 post-authorization driver without live search."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "tools/kds-sync/run_agent_reach_p8_post_authorization_driver.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_post_authorization_driver=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_driver():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_post_authorization_driver", DRIVER)
    if spec is None or spec.loader is None:
        fail("driver_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def default_local_auth_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request.get("batch_authorization_requests", [])]


def authorization_text(request: dict[str, Any], start: str, end: str) -> str:
    return "\n".join(
        [
            *[item["required_text"] for item in request.get("batch_authorization_requests", [])],
            "授权人：lujunxiang",
            f"有效期：{start} 至 {end}",
            "仅允许 web/rss/bilibili 公开内容读取，最多 5 个 query、每个 query 最多 10 条结果。",
            "禁止写凭据、提取 cookie、写 KDS canonical、写 GFIS source-of-record、改生产配置、改全局 MCP 配置、生产集成或声明 accepted/integrated/production_ready。",
        ]
    )


def run_cli(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(DRIVER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_cli_report(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"cli_report_missing:{path}")
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-20260622",
            "title: Agent-Reach P8 授权后执行 Driver 证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-post-authorization-driver-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权后执行 Driver 证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- dry_run_status: `{report['dry_run_status']}`",
            f"- cli_dry_run_status: `{report['cli_dry_run_status']}`",
            f"- negative_status: `{report['negative_status']}`",
            f"- cli_negative_exit_code: `{report['cli_negative_exit_code']}`",
            f"- default_local_authorization_files_created: `{report['default_local_authorization_files_created']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 新增 P8 post-authorization driver，串联授权文本摄取、授权文件创建、pipeline、输出质量门禁与返工队列入口。",
            "- 验证只使用临时授权文件和 pipeline dry-run，不执行真实搜索。",
            "",
            "## stop",
            "",
            "- 本轮停止在授权后执行 driver 就绪。",
            "- 未收到正式授权前，不写默认授权文件，不执行 web/rss/bilibili 请求。",
            "",
            "## verify",
            "",
            "- dry-run 路径进入 `authorized_execution_not_requested`。",
            "- CLI dry-run 路径进入 `authorized_execution_not_requested`。",
            "- `--execute-live` 未配套 `--write-evidence` 时被拒绝。",
            "- CLI 负向路径以非零退出码拒绝。",
            "- 默认 fixtures 授权文件未创建。",
            "",
            "## recover",
            "",
            "- 删除本轮 driver、validator 和 evidence/loop 文档即可回滚。",
            "",
            "## debug",
            "",
            "- 正式执行仍需要 P8 三批授权文本、ISO 时间窗、`--write-local-auth --execute-live --write-evidence`。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-001",
            "title: Agent-Reach P8 授权后执行 Driver Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权后执行 Driver Loop 001",
            "",
            "## run",
            "",
            "建立授权后执行 driver 的离线验证闭包。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；当前状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"dry-run `{report['dry_run_status']}`；CLI dry-run `{report['cli_dry_run_status']}`；负向用例 `{report['negative_status']}`；真实外搜 `{report['security_controls']['live_external_search_invoked']}`。",
            "",
            "## recover",
            "",
            "验证器未写默认授权文件；回滚为删除本轮新增 driver/validator/evidence。",
            "",
            "## debug",
            "",
            "继续执行仍需正式 P8 三批授权。",
            "",
        ]
    )


def main() -> None:
    driver = load_driver()
    request = load_json(REQUEST)
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_exists_before_test:{path.relative_to(ROOT)}")
    now = datetime.now(timezone.utc)
    start = now.isoformat()
    end = (now + timedelta(hours=2)).isoformat()
    with tempfile.TemporaryDirectory(prefix="agent-reach-p8-driver-") as tmpdir:
        tmp = Path(tmpdir)
        text_path = tmp / "authorization.txt"
        text_path.write_text(authorization_text(request, start, end), encoding="utf-8")
        dry_run = driver.build_report(
            authorization_text_path=text_path,
            write_local_auth=True,
            execute_live=False,
            write_evidence=False,
            authorization_output_dir=tmp / "auth",
            pipeline_report_path=tmp / "pipeline-report.json",
        )
        negative = driver.build_report(
            authorization_text_path=text_path,
            write_local_auth=True,
            execute_live=True,
            write_evidence=False,
            authorization_output_dir=tmp / "auth-negative",
        )
        cli_report_path = tmp / "cli-driver-report.json"
        cli_pipeline_report_path = tmp / "cli-pipeline-report.json"
        cli_dry = run_cli(
            [
                "--authorization-text-file",
                str(text_path),
                "--write-local-auth",
                "--authorization-output-dir",
                str(tmp / "cli-auth"),
                "--pipeline-report",
                str(cli_pipeline_report_path),
                "--report",
                str(cli_report_path),
            ]
        )
        cli_report = load_cli_report(cli_report_path)
        cli_negative = run_cli(
            [
                "--authorization-text-file",
                str(text_path),
                "--write-local-auth",
                "--execute-live",
                "--authorization-output-dir",
                str(tmp / "cli-auth-negative"),
                "--pipeline-report",
                str(tmp / "cli-negative-pipeline-report.json"),
                "--report",
                str(tmp / "cli-negative-report.json"),
            ]
        )
    if dry_run.get("status") != "authorized_execution_not_requested":
        fail(f"dry_run_status_mismatch:{dry_run.get('status')}")
    if dry_run.get("pipeline_report", {}).get("status") != "authorized_execution_not_requested":
        fail("pipeline_dry_run_status_mismatch")
    if dry_run.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("dry_run_invoked_live_search")
    if dry_run.get("rework_queue_module", {}).get("status") != "pass":
        fail("rework_queue_gate_not_pass")
    if negative.get("status") != "rejected_execute_requires_write_evidence":
        fail(f"negative_status_mismatch:{negative.get('status')}")
    if cli_dry.returncode != 0:
        fail(f"cli_dry_run_failed:{cli_dry.stderr or cli_dry.stdout}")
    if cli_report.get("status") != "authorized_execution_not_requested":
        fail(f"cli_dry_run_status_mismatch:{cli_report.get('status')}")
    if cli_report.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("cli_dry_run_invoked_live_search")
    if cli_negative.returncode == 0:
        fail("cli_negative_unexpected_success")
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_created:{path.relative_to(ROOT)}")
    report = {
        "id": "agent-reach-p8-post-authorization-driver-20260622",
        "round": "GPCF-AGENT-REACH-P8-POST-AUTHORIZATION-DRIVER-001",
        "date": "2026-06-22",
        "status": "p8_post_authorization_driver_ready",
        "current_admission": "limited_candidate_only",
        "dry_run_status": dry_run["status"],
        "cli_dry_run_status": cli_report["status"],
        "negative_status": negative["status"],
        "cli_negative_exit_code": cli_negative.returncode,
        "default_local_authorization_files_created": False,
        "pipeline_report_status": dry_run["pipeline_report"]["status"],
        "output_quality_gate_precheck": dry_run["output_quality_gate_precheck"],
        "rework_queue_gate": dry_run["rework_queue_module"],
        "security_controls": dry_run["security_controls"],
        "non_claims": dry_run["non_claims"],
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    print(
        "agent_reach_p8_post_authorization_driver=pass "
        "status=p8_post_authorization_driver_ready "
        "dry_run=authorized_execution_not_requested "
        "negative=pass default_local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
