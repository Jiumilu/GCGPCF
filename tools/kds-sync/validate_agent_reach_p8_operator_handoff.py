#!/usr/bin/env python3
"""Validate the Agent-Reach P8 operator handoff before live execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
READINESS = ROOT / "docs/harness/evidence/agent-reach-p8-live-execution-readiness-matrix-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-OPERATOR-HANDOFF-001.md"

FORBIDDEN_COMMAND_FRAGMENTS = [
    "git add",
    "git commit",
    "git push",
    "kds canonical",
    "production_ready",
    "accepted",
    "integrated",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_operator_handoff=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def local_authorization_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request["batch_authorization_requests"]]


def required_authorization_text(request: dict[str, Any]) -> str:
    batch_lines = "\n".join(item["required_text"] for item in request["batch_authorization_requests"])
    return "\n".join(
        [
            batch_lines,
            "授权人：lujunxiang",
            "有效期：<start-iso8601> 至 <end-iso8601>",
            "仅允许 web/rss/bilibili 公开内容读取，Batch 1/2 最多 5 个 query，Batch 3 最多 4 个 query，每个 query 最多 10 条结果。",
            "禁止写凭据、提取 cookie、写 KDS canonical、写 GFIS source-of-record、改生产配置、改全局 MCP 配置、生产集成或声明 accepted/integrated/production_ready。",
        ]
    )


def command_recipe() -> list[dict[str, str]]:
    return [
        {
            "step": "authorization_text_dry_run",
            "command": "python3 tools/kds-sync/ingest_agent_reach_p8_authorization_text.py --authorization-text-file <authorization-text-file>",
            "expected": "status=dry_run_valid",
        },
        {
            "step": "authorization_text_write_local_auth",
            "command": "python3 tools/kds-sync/ingest_agent_reach_p8_authorization_text.py --authorization-text-file <authorization-text-file> --write-local-auth",
            "expected": "writes fixtures/agent-reach/project-group-full-live-search-batch-*-authorization.local.json only after valid authorization",
        },
        {
            "step": "local_authorization_window_audit",
            "command": "python3 tools/kds-sync/validate_agent_reach_p8_local_authorization_window_audit.py",
            "expected": "blocks missing, future, expired, and wrong-batch local authorization files without network access",
        },
        {
            "step": "pre_execution_readiness",
            "command": "python3 tools/kds-sync/validate_agent_reach_p8_live_execution_readiness_matrix.py",
            "expected": "status=p8_live_execution_ready_pending_human_authorization before local auth, or no readiness regression after local auth",
        },
        {
            "step": "execute_live_with_evidence",
            "command": "python3 tools/kds-sync/run_agent_reach_p8_post_authorization_driver.py --authorization-text-file <authorization-text-file> --write-local-auth --execute-live --write-evidence --report docs/harness/evidence/agent-reach-p8-post-authorization-driver-live-20260623.json",
            "expected": "requires --write-evidence with --execute-live",
        },
        {
            "step": "output_quality_gate",
            "command": "python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py",
            "expected": "all project/query/channel coverage, no duplicate URLs, no query errors, required field coverage 1.0",
        },
        {
            "step": "document_governance",
            "command": "python3 tools/kds-sync/document_control.py && python3 tools/kds-sync/check_document_pollution.py && python3 tools/kds-sync/validate_kds_token.py && python3 tools/kds-sync/loop_document_gate.py",
            "expected": "controlled evidence, pollution pass, KDS token pass, loop document gate pass",
        },
    ]


def validate_recipe(recipe: list[dict[str, str]]) -> None:
    if len(recipe) != 7:
        fail("recipe_step_count_mismatch")
    for row in recipe:
        command = row["command"]
        lowered = command.lower()
        if not command.startswith("python3 tools/kds-sync/"):
            fail(f"command_not_local_validator_or_driver:{row['step']}")
        for fragment in FORBIDDEN_COMMAND_FRAGMENTS:
            if fragment in lowered:
                fail(f"forbidden_command_fragment:{row['step']}:{fragment}")
    execute = next(row for row in recipe if row["step"] == "execute_live_with_evidence")
    if "--execute-live" not in execute["command"] or "--write-evidence" not in execute["command"]:
        fail("execute_command_missing_evidence_guard")
    if "--write-local-auth" not in execute["command"]:
        fail("execute_command_missing_local_auth_write")


def build_report() -> dict[str, Any]:
    request = load_json(REQUEST)
    readiness = load_json(READINESS)
    local_auth = [
        {"path": str(path.relative_to(ROOT)), "exists": path.exists()}
        for path in local_authorization_paths(request)
    ]
    recipe = command_recipe()
    validate_recipe(recipe)
    if readiness.get("status") != "p8_live_execution_ready_pending_human_authorization":
        fail("readiness_status_mismatch")
    if readiness["readiness_summary"]["all_local_quality_gates_pass"] is not True:
        fail("readiness_local_gates_not_pass")
    if any(row["exists"] for row in local_auth):
        fail("local_authorization_file_exists")
    return {
        "id": "agent-reach-p8-operator-handoff-20260623",
        "round": "GPCF-AGENT-REACH-P8-OPERATOR-HANDOFF-001",
        "date": "2026-06-23",
        "status": "p8_operator_handoff_ready_pending_authorization",
        "current_admission": "limited_candidate_only",
        "source_readiness_matrix": str(READINESS.relative_to(ROOT)),
        "readiness_status": readiness["status"],
        "required_authorization_text": required_authorization_text(request),
        "local_authorization_files": local_auth,
        "command_recipe": recipe,
        "post_execution_required_gates": [
            "validate_agent_reach_project_group_full_live_coverage_output.py",
            "validate_agent_reach_p8_rework_queue.py",
            "document_control.py",
            "check_document_pollution.py",
            "validate_kds_token.py",
            "loop_document_gate.py",
        ],
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
    recipe = "\n".join(
        f"| {row['step']} | `{row['command']}` | {row['expected']} |" for row in report["command_recipe"]
    )
    local_auth = "\n".join(
        f"- `{row['path']}` exists=`{row['exists']}`" for row in report["local_authorization_files"]
    )
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-OPERATOR-HANDOFF-20260623",
            "title: Agent-Reach P8 Operator Handoff 2026-06-23",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.md",
            "source_path: docs/harness/evidence/agent-reach-p8-operator-handoff-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 Operator Handoff 2026-06-23",
            "",
            f"- status: `{report['status']}`",
            f"- readiness_status: `{report['readiness_status']}`",
            f"- current_admission: `{report['current_admission']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "本轮固化 P8 授权后执行交接清单，只生成本地 evidence，不执行真实搜索。",
            "",
            "## stop",
            "",
            "停止类型为 `authorization_boundary`。未收到正式 P8 三批授权前，不得执行真实 web/rss/bilibili 搜索。",
            "",
            "## verify",
            "",
            "### Required Authorization Text",
            "",
            "```text",
            report["required_authorization_text"],
            "```",
            "",
            "### Local Authorization Files",
            "",
            local_auth,
            "",
            "### Command Recipe",
            "",
            "| step | command | expected |",
            "|---|---|---|",
            recipe,
            "",
            "## recover",
            "",
            "删除本轮 evidence、loop 文档和 validator 即可回滚；本轮不创建 `.local.json` 授权文件。",
            "",
            "## debug",
            "",
            "- 下一步仍是 `GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`。",
            "- 执行后必须跑 output quality gate 与文档治理门禁。",
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
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-OPERATOR-HANDOFF-001",
            "title: Agent-Reach P8 Operator Handoff Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-OPERATOR-HANDOFF-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-OPERATOR-HANDOFF-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 Operator Handoff Loop 001",
            "",
            "## run",
            "",
            "建立 P8 授权后执行交接清单和命令配方。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"readiness `{report['readiness_status']}`；真实外搜 `{report['security_controls']['live_external_search_invoked']}`。",
            "",
            "## recover",
            "",
            "本轮未创建授权文件、未触网；删除本轮新增文件即可回滚。",
            "",
            "## debug",
            "",
            "继续执行仍需正式 P8 三批授权，并在执行后跑质量与文档治理门禁。",
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
        "p8_operator_handoff_ready_pending_authorization",
        "authorization_boundary",
        "--execute-live --write-evidence",
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
        "agent_reach_p8_operator_handoff=pass "
        "status=p8_operator_handoff_ready_pending_authorization "
        "readiness=p8_live_execution_ready_pending_human_authorization "
        "local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
