#!/usr/bin/env python3
"""Validate Agent-Reach P8 authorization text intake without default auth writes."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
INTAKE = ROOT / "tools/kds-sync/ingest_agent_reach_p8_authorization_text.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_authorization_text_intake=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_intake():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_authorization_text_intake", INTAKE)
    if spec is None or spec.loader is None:
        fail("intake_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def required_texts(request: dict[str, Any]) -> list[str]:
    return [item["required_text"] for item in request.get("batch_authorization_requests", [])]


def default_local_auth_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request.get("batch_authorization_requests", [])]


def authorization_text(request: dict[str, Any], start: str, end: str, include_all_batches: bool = True) -> str:
    texts = required_texts(request)
    if not include_all_batches:
        texts = texts[:2]
    return "\n".join(
        [
            *texts,
            "授权人：lujunxiang",
            f"有效期：{start} 至 {end}",
            "仅允许 web/rss/bilibili 公开内容读取，最多 5 个 query、每个 query 最多 10 条结果。",
            "禁止写凭据、提取 cookie、写 KDS canonical、写 GFIS source-of-record、改生产配置、改全局 MCP 配置、生产集成或声明 accepted/integrated/production_ready。",
        ]
    )


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-20260622",
            "title: Agent-Reach P8 授权文本摄取证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-authorization-text-intake-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权文本摄取证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- dry_run_status: `{report['dry_run_status']}`",
            f"- isolated_write_status: `{report['isolated_write_status']}`",
            f"- negative_status: `{report['negative_status']}`",
            f"- default_local_authorization_files_created: `{report['default_local_authorization_files_created']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 新增授权文本摄取脚本，支持从一段文本抽取授权人、有效期和三条 P8 batch 授权文本。",
            "- 默认 dry-run；只有显式 `--write-local-auth` 才会委托创建 `.local.json`。",
            "",
            "## stop",
            "",
            "- 本轮不执行真实搜索，不写默认授权文件。",
            "- 缺少任一批次授权文本、授权人、有效期、渠道或禁止边界时拒绝。",
            "",
            "## verify",
            "",
            "- 完整文本 dry-run 通过。",
            "- 完整文本在临时目录隔离写入通过。",
            "- 缺少 Batch 3 的负向文本被拒绝。",
            "- 默认 fixtures 授权文件未创建。",
            "",
            "## recover",
            "",
            "- 摄取脚本不写生产配置，不写 KDS canonical，不写 GFIS source-of-record。",
            "- 如误写默认授权文件，删除 `fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json` 后重新运行验证器。",
            "",
            "## debug",
            "",
            "下一步仍需正式 P8 三批授权文本与具体 ISO 起止时间窗口。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-001",
            "title: Agent-Reach P8 授权文本摄取 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权文本摄取 Loop 001",
            "",
            "## run",
            "",
            "建立 P8 授权文本摄取和离线校验闭包。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；当前状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"dry-run `{report['dry_run_status']}`；隔离写入 `{report['isolated_write_status']}`；负向用例 `{report['negative_status']}`。",
            "",
            "## recover",
            "",
            "验证器未创建默认授权文件；删除本轮 evidence/loop 文档和脚本即可回滚。",
            "",
            "## debug",
            "",
            "继续执行仍需正式 P8 Batch 1、Batch 2、Batch 3 授权。",
            "",
        ]
    )


def main() -> None:
    intake = load_intake()
    request = load_json(REQUEST)
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_exists_before_test:{path.relative_to(ROOT)}")
    now = datetime.now(timezone.utc)
    start = now.isoformat()
    end = (now + timedelta(hours=2)).isoformat()
    with tempfile.TemporaryDirectory(prefix="agent-reach-p8-text-intake-") as tmpdir:
        tmp = Path(tmpdir)
        good_text = tmp / "good-authorization.txt"
        bad_text = tmp / "bad-authorization.txt"
        good_text.write_text(authorization_text(request, start, end), encoding="utf-8")
        bad_text.write_text(authorization_text(request, start, end, include_all_batches=False), encoding="utf-8")
        dry_run = intake.build_report(
            authorization_text_path=good_text,
            write_local_auth=False,
        )
        isolated_write = intake.build_report(
            authorization_text_path=good_text,
            write_local_auth=True,
            authorization_output_dir=tmp / "auth-out",
        )
        negative = intake.build_report(
            authorization_text_path=bad_text,
            write_local_auth=False,
        )
    if dry_run["status"] != "dry_run_valid":
        fail(f"dry_run_not_valid:{dry_run['status']}")
    if isolated_write["status"] != "local_authorization_files_written":
        fail(f"isolated_write_not_valid:{isolated_write['status']}")
    if negative["status"] != "rejected":
        fail("negative_missing_batch_not_rejected")
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_created:{path.relative_to(ROOT)}")
    report = {
        "id": "agent-reach-p8-authorization-text-intake-20260622",
        "round": "GPCF-AGENT-REACH-P8-AUTHORIZATION-TEXT-INTAKE-001",
        "date": "2026-06-22",
        "status": "p8_authorization_text_intake_ready",
        "current_admission": "limited_candidate_only",
        "dry_run_status": dry_run["status"],
        "isolated_write_status": isolated_write["status"],
        "negative_status": negative["status"],
        "negative_reasons": negative["parsed_authorization"]["reasons"],
        "default_local_authorization_files_created": False,
        "required_authorization_texts": required_texts(request),
        "security_controls": dry_run["security_controls"],
        "non_claims": dry_run["non_claims"],
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    print(
        "agent_reach_p8_authorization_text_intake=pass "
        "status=p8_authorization_text_intake_ready "
        "dry_run=pass isolated_write=pass negative=pass "
        "default_local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
