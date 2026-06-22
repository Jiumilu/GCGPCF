#!/usr/bin/env python3
"""Build and validate the Agent-Reach P8 execution audit bundle."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
QUERY_PREFLIGHT = ROOT / "tools/kds-sync/validate_agent_reach_p8_query_quality_preflight.py"
OUTPUT_GATE = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
PIPELINE = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_pipeline.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-execution-audit-bundle-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-execution-audit-bundle-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-001.md"

SECURITY_FALSE_FIELDS = [
    "live_external_search_invoked",
    "agent_reach_binary_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_execution_audit_bundle=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"import_failed:{name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def local_authorization_files(request: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in request.get("batch_authorization_requests", []):
        path = ROOT / item["authorization_file_to_create_after_human_approval"]
        rows.append(
            {
                "batch_id": item["batch_id"],
                "path": display_path(path),
                "exists": path.exists(),
            }
        )
    return rows


def build_report() -> dict[str, Any]:
    query_preflight = load_module(QUERY_PREFLIGHT, "agent_reach_p8_query_quality_preflight")
    output_gate = load_module(OUTPUT_GATE, "agent_reach_p8_output_gate")
    pipeline = load_module(PIPELINE, "agent_reach_p8_pipeline")
    request = load_json(REQUEST)

    query_report = query_preflight.build_report()
    try:
        output_gate.validate_gate_evidence()
        output_status = "full_project_group_live_coverage_output_quality_gate_ready"
        output_reasons: list[str] = []
    except SystemExit as exc:
        output_status = "full_project_group_live_coverage_output_quality_gate_rework_required"
        output_reasons = [str(exc)]
    pipeline_report = pipeline.build_pipeline_report(
        execute=False,
        write_evidence=False,
        output_json=pipeline.DEFAULT_OUTPUT_JSON,
        output_md=pipeline.DEFAULT_OUTPUT_MD,
    )
    auth_files = local_authorization_files(request)
    missing_auth_batches = [
        row["batch_id"]
        for row in auth_files
        if row["exists"] is False
    ]
    required_texts = [
        item["required_text"]
        for item in request.get("batch_authorization_requests", [])
    ]
    ready_for_human_authorization = (
        query_report.get("status") == "p8_query_quality_preflight_pass"
        and output_status == "full_project_group_live_coverage_output_quality_gate_ready"
        and pipeline_report.get("status") == "blocked_pending_batch_authorization"
        and sorted(missing_auth_batches) == ["p8-batch-1", "p8-batch-2", "p8-batch-3"]
    )
    return {
        "id": "agent-reach-p8-execution-audit-bundle-20260622",
        "round": "GPCF-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-001",
        "date": "2026-06-22",
        "status": "p8_execution_audit_ready_for_human_authorization"
        if ready_for_human_authorization
        else "p8_execution_audit_rework_required",
        "current_admission": "limited_candidate_only",
        "ready_for_human_authorization": ready_for_human_authorization,
        "query_preflight": {
            "status": query_report.get("status"),
            "query_count": query_report.get("query_count"),
            "project_coverage": query_report.get("project_coverage"),
            "channel_coverage": query_report.get("channel_coverage"),
            "failing_query_count": query_report.get("failing_query_count"),
            "duplicate_normalized_query_count": query_report.get("duplicate_normalized_query_count"),
        },
        "output_quality_gate": {
            "status": output_status,
            "reasons": output_reasons,
        },
        "authorization_state": {
            "request_package": display_path(REQUEST),
            "request_status": request.get("authorization_status"),
            "generated_local_authorization_files": request.get("generated_local_authorization_files"),
            "execution_allowed_now": request.get("execution_allowed_now"),
            "local_authorization_files": auth_files,
            "missing_authorization_batches": missing_auth_batches,
            "required_authorization_texts": required_texts,
        },
        "pipeline_state": {
            "status": pipeline_report.get("status"),
            "missing_authorization_batches": pipeline_report.get("missing_authorization_batches", []),
            "next_required_authorizations": pipeline_report.get("next_required_authorizations", []),
            "quality_preflight": pipeline_report.get("quality_preflight", {}),
        },
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
    auth = report["authorization_state"]
    pipeline = report["pipeline_state"]
    required_texts = "\n".join(f"- `{text}`" for text in auth["required_authorization_texts"])
    missing = ", ".join(auth["missing_authorization_batches"])
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-20260622",
            "title: Agent-Reach P8 执行审计包 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-execution-audit-bundle-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-execution-audit-bundle-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 执行审计包 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- ready_for_human_authorization: `{report['ready_for_human_authorization']}`",
            f"- query_preflight_status: `{report['query_preflight']['status']}`",
            f"- output_quality_gate_status: `{report['output_quality_gate']['status']}`",
            "- pipeline_status: `authorization_boundary_pending_human_approval`",
            f"- missing_authorization_batches: `{missing}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 汇总 P8 查询质量预检、输出质量门禁、批量授权请求包和 pipeline 授权边界状态。",
            "- 本审计包用于执行前交接，不执行真实搜索，不创建 `.local.json` 授权文件。",
            "",
            "## stop",
            "",
            "- 停止类型为 `authorization_boundary`。",
            "- 三批本地授权文件仍缺失，pipeline 保持授权边界等待状态。",
            "",
            "## verify",
            "",
            "- query preflight 已证明 14/14 项目、web/rss/bilibili 渠道和 14 条查询计划通过离线质量预检。",
            "- output quality gate 已证明真实结果写入后必须满足覆盖率、去重、零错误、schema、分数、脱敏和非声明门禁。",
            "- pipeline 默认运行只做 preflight，不触发外部网络。",
            "",
            "## recover",
            "",
            "- 若授权文本或时间窗口不合规，不创建本地授权文件。",
            "- 若后续真实搜索失败，进入 P8 rework queue，不升级 accepted / integrated / production_ready。",
            "",
            "## debug",
            "",
            "下一步需要以下三条授权文本及具体 ISO 时间窗口：",
            "",
            required_texts,
            "",
            "## 非声明",
            "",
            "- 本证据不声明全量真实搜索已完成。",
            "- 本证据不声明 accepted / integrated / production_ready。",
            "- 本证据不写 KDS canonical Markdown。",
            "- 本证据不写 GFIS source-of-record。",
            "- 本证据不修改生产配置或全局 MCP 配置。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-001",
            "title: Agent-Reach P8 执行审计包 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-EXECUTION-AUDIT-BUNDLE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 执行审计包 Loop 001",
            "",
            "## run",
            "",
            "生成 P8 执行审计包，固化真实搜索执行前的质量、授权和安全状态。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；审计状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"pipeline 状态 `authorization_boundary_pending_human_approval`；缺失授权批次 `{', '.join(report['authorization_state']['missing_authorization_batches'])}`。",
            "",
            "## recover",
            "",
            "删除本轮审计包 evidence/loop 文档即可回滚；未创建授权文件，未执行外部搜索。",
            "",
            "## debug",
            "",
            "继续执行需要 P8 Batch 1、Batch 2、Batch 3 三条授权文本和具体 ISO 起止时间。",
            "",
        ]
    )


def validate_report(report: dict[str, Any]) -> None:
    if report.get("status") != "p8_execution_audit_ready_for_human_authorization":
        fail("status_not_ready_for_human_authorization")
    if report.get("ready_for_human_authorization") is not True:
        fail("ready_for_human_authorization_not_true")
    if report.get("query_preflight", {}).get("status") != "p8_query_quality_preflight_pass":
        fail("query_preflight_not_passed")
    if report.get("query_preflight", {}).get("failing_query_count") != 0:
        fail("query_preflight_has_failures")
    if report.get("output_quality_gate", {}).get("status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("output_quality_gate_not_ready")
    if report.get("pipeline_state", {}).get("status") != "blocked_pending_batch_authorization":
        fail("pipeline_not_blocked_on_authorization")
    if sorted(report.get("authorization_state", {}).get("missing_authorization_batches", [])) != [
        "p8-batch-1",
        "p8-batch-2",
        "p8-batch-3",
    ]:
        fail("missing_authorization_batches_mismatch")
    if len(report.get("authorization_state", {}).get("required_authorization_texts", [])) != 3:
        fail("required_authorization_text_count_mismatch")
    if any(row.get("exists") for row in report.get("authorization_state", {}).get("local_authorization_files", [])):
        fail("local_authorization_file_exists")
    controls = report.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")


def validate_written_artifacts(report: dict[str, Any]) -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("id") != report.get("id"):
        fail("written_evidence_id_mismatch")
    for marker in [
        "p8_execution_audit_ready_for_human_authorization",
        "authorization_boundary_pending_human_approval",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 1",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 2",
        "授权执行 Agent-Reach P8 Project Group Full Live Search Batch 3",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")


def main() -> None:
    report = build_report()
    validate_report(report)
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    LOOP_MD.write_text(render_loop(report), encoding="utf-8")
    validate_written_artifacts(report)
    print(
        "agent_reach_p8_execution_audit_bundle=pass "
        "status=p8_execution_audit_ready_for_human_authorization "
        "missing_authorization_batches=3 "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
