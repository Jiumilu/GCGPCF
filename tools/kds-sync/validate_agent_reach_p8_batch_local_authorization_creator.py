#!/usr/bin/env python3
"""Validate the P8 batch local authorization creator without writing local auth."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CREATOR = ROOT / "tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_batch_local_authorization_creator=fail reason={message}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_creator():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_local_authorization_creator", CREATOR)
    if spec is None or spec.loader is None:
        fail("creator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def required_texts(request: dict[str, Any]) -> list[str]:
    return [item["required_text"] for item in request.get("batch_authorization_requests", [])]


def local_auth_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request.get("batch_authorization_requests", [])]


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-20260622",
            "title: Agent-Reach P8 批次本地授权创建器证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 批次本地授权创建器证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- dry_run_status: `{report['dry_run_status']}`",
            f"- isolated_write_status: `{report['isolated_write_status']}`",
            f"- negative_status: `{report['negative_status']}`",
            f"- local_authorization_files_created: `{report['local_authorization_files_created']}`",
            f"- isolated_authorization_files_created: `{report['isolated_authorization_files_created']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 新增 `tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py`，将精确 P8 批次授权文本转换为可机检 `.local.json`。",
            "- 默认 dry-run；只有显式 `--write-local-auth` 才允许写本地授权文件。",
            "",
            "## stop",
            "",
            "- 本轮停止在授权创建器就绪，不执行真实搜索。",
            "- 未收到三批 P8 执行授权时，不创建 `.local.json`。",
            "",
            "## verify",
            "",
            "- 正向 dry-run 覆盖三个 P8 batch。",
            "- 隔离写入模式在临时目录生成三份授权文件，并通过 runner 授权校验。",
            "- 负向用错误授权文本确认拒绝。",
            "- 验证期间未写默认 fixtures 本地授权文件。",
            "",
            "## recover",
            "",
            "- 如误写授权文件，删除 `fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json` 后重新运行本验证器。",
            "",
            "## debug",
            "",
            "- 下一步仍需人工逐批授权 P8 Batch 1、Batch 2、Batch 3，才可执行 pipeline。",
            "",
            "## 非声明",
            "",
            "- 本证据仅为候选证据。",
            "- 本证据不声明 accepted / integrated / production_ready 状态。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不持久化 raw provider payload。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001",
            "title: Agent-Reach P8 批次本地授权创建器 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 批次本地授权创建器 Loop 001",
            "",
            "## run",
            "",
            "建立 P8 batch 授权本地化入口，默认不写授权文件。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；当前状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"干运行 `{report['dry_run_status']}`；隔离写入 `{report['isolated_write_status']}`；负向用例 `{report['negative_status']}`；默认本地授权文件已创建 `{report['local_authorization_files_created']}`。",
            "",
            "## recover",
            "",
            "本轮没有真实外搜与生产写入，回滚为删除新增脚本和本轮 evidence/loop 文档。",
            "",
            "## debug",
            "",
            "等待 P8 三批执行授权；授权前 pipeline 仍应停在 `blocked_pending_batch_authorization`。",
            "",
        ]
    )


def main() -> None:
    creator = load_creator()
    request = load_json(REQUEST)
    paths = local_auth_paths(request)
    for path in paths:
        if path.exists():
            fail(f"local_authorization_file_exists_before_test:{path.relative_to(ROOT)}")
    now = datetime.now(timezone.utc)
    start = now.isoformat()
    end = (now + timedelta(hours=2)).isoformat()
    dry_run = creator.build_report(
        batch_ids=["p8-batch-1", "p8-batch-2", "p8-batch-3"],
        authorization_texts=required_texts(request),
        authorized_at=start,
        expires_at=end,
        write_local_auth=False,
    )
    if dry_run["status"] != "dry_run_valid":
        fail(f"dry_run_not_valid:{dry_run['status']}")
    with tempfile.TemporaryDirectory(prefix="agent-reach-p8-auth-") as tmpdir:
        isolated_write = creator.build_report(
            batch_ids=["p8-batch-1", "p8-batch-2", "p8-batch-3"],
            authorization_texts=required_texts(request),
            authorized_at=start,
            expires_at=end,
            write_local_auth=True,
            authorization_output_dir=Path(tmpdir),
        )
        if isolated_write["status"] != "local_authorization_files_written":
            fail(f"isolated_write_not_valid:{isolated_write['status']}")
        written_paths = [
            Path(item["authorization_file"])
            for item in isolated_write["batch_reports"].values()
            if item.get("authorization_file_written") is True
        ]
        if len(written_paths) != 3:
            fail("isolated_write_file_count_mismatch")
        for written_path in written_paths:
            if not written_path.exists():
                fail(f"isolated_write_file_missing:{written_path}")
    negative = creator.build_report(
        batch_ids=["p8-batch-1"],
        authorization_texts=["授权执行 Agent-Reach P8 Wrong Batch"],
        authorized_at=start,
        expires_at=end,
        write_local_auth=False,
    )
    if negative["status"] != "rejected":
        fail("negative_wrong_text_not_rejected")
    for path in paths:
        if path.exists():
            fail(f"local_authorization_file_created_by_validation:{path.relative_to(ROOT)}")
    evidence = {
        "id": "agent-reach-p8-batch-local-authorization-creator-20260622",
        "round": "GPCF-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001",
        "date": "2026-06-22",
        "status": "p8_batch_local_authorization_creator_ready",
        "current_admission": "limited_candidate_only",
        "dry_run_status": dry_run["status"],
        "isolated_write_status": isolated_write["status"],
        "negative_status": negative["status"],
        "local_authorization_files_created": False,
        "isolated_authorization_files_created": True,
        "input_artifacts": [
            "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json",
            "tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py",
        ],
        "output_artifacts": [
            "tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py",
            "tools/kds-sync/validate_agent_reach_p8_batch_local_authorization_creator.py",
            "docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.json",
            "docs/harness/evidence/agent-reach-p8-batch-local-authorization-creator-20260622.md",
            "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-LOCAL-AUTHORIZATION-CREATOR-001.md",
        ],
        "dry_run_batch_status": {
            batch_id: item["status"] for batch_id, item in dry_run["batch_reports"].items()
        },
        "isolated_write_batch_status": {
            batch_id: item["status"] for batch_id, item in isolated_write["batch_reports"].items()
        },
        "negative_reasons": negative["batch_reports"]["p8-batch-1"]["reasons"],
        "next_required_authorizations": required_texts(request),
        "security_controls": dry_run["security_controls"],
        "non_claims": dry_run["non_claims"],
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }
    write_json(EVIDENCE_JSON, evidence)
    EVIDENCE_MD.write_text(render_markdown(evidence), encoding="utf-8")
    LOOP_MD.write_text(render_loop(evidence), encoding="utf-8")
    print(
        "agent_reach_p8_batch_local_authorization_creator=pass "
        "status=p8_batch_local_authorization_creator_ready "
        "dry_run=pass isolated_write=pass negative=pass local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
