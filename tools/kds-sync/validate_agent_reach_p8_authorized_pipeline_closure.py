#!/usr/bin/env python3
"""Validate that P8 pipeline recognizes all three batch authorizations without executing search."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CREATOR = ROOT / "tools/kds-sync/create_agent_reach_p8_batch_authorization_local.py"
PIPELINE = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_pipeline.py"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-authorized-pipeline-closure-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-authorized-pipeline-closure-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-001.md"

BATCH_IDS = ["p8-batch-1", "p8-batch-2", "p8-batch-3"]
SECURITY_FALSE_FIELDS = [
    "live_external_search_invoked",
    "credential_written",
    "browser_cookie_extraction_invoked",
    "kds_canonical_write_allowed",
    "gfis_source_of_record_write_allowed",
    "production_config_write_allowed",
    "global_mcp_config_write_allowed",
    "production_integration_allowed",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_authorized_pipeline_closure=fail reason={message}")


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


def required_texts(request: dict[str, Any]) -> list[str]:
    return [item["required_text"] for item in request.get("batch_authorization_requests", [])]


def default_local_auth_paths(request: dict[str, Any]) -> list[Path]:
    return [ROOT / item["authorization_file_to_create_after_human_approval"] for item in request.get("batch_authorization_requests", [])]


def build_report() -> dict[str, Any]:
    creator = load_module(CREATOR, "agent_reach_p8_local_authorization_creator")
    pipeline = load_module(PIPELINE, "agent_reach_p8_pipeline")
    request = load_json(REQUEST)
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_exists:{path.relative_to(ROOT)}")
    now = datetime.now(timezone.utc)
    with tempfile.TemporaryDirectory(prefix="agent-reach-p8-pipeline-auth-") as tmpdir:
        auth_dir = Path(tmpdir)
        auth_report = creator.build_report(
            batch_ids=BATCH_IDS,
            authorization_texts=required_texts(request),
            authorized_at=now.isoformat(),
            expires_at=(now + timedelta(hours=2)).isoformat(),
            write_local_auth=True,
            authorization_output_dir=auth_dir,
        )
        if auth_report.get("status") != "local_authorization_files_written":
            fail(f"isolated_authorization_write_failed:{auth_report.get('status')}")
        pipeline_report = pipeline.build_pipeline_report(
            execute=False,
            write_evidence=False,
            output_json=pipeline.DEFAULT_OUTPUT_JSON,
            output_md=pipeline.DEFAULT_OUTPUT_MD,
            authorization_dir=auth_dir,
        )
    for path in default_local_auth_paths(request):
        if path.exists():
            fail(f"default_local_authorization_file_created:{path.relative_to(ROOT)}")
    return {
        "id": "agent-reach-p8-authorized-pipeline-closure-20260622",
        "round": "GPCF-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-001",
        "date": "2026-06-22",
        "status": "p8_authorized_pipeline_closure_ready",
        "current_admission": "limited_candidate_only",
        "isolated_authorization_status": auth_report.get("status"),
        "pipeline_status_with_isolated_authorizations": pipeline_report.get("status"),
        "preflight_status": pipeline_report.get("preflight_status", {}),
        "quality_preflight": pipeline_report.get("quality_preflight", {}),
        "missing_authorization_batches": pipeline_report.get("missing_authorization_batches", []),
        "default_local_authorization_files_created": False,
        "execution_requested": pipeline_report.get("execution_requested"),
        "write_evidence_requested": pipeline_report.get("write_evidence_requested"),
        "batch_authorization_text_count": len(required_texts(request)),
        "security_controls": pipeline_report.get("security_controls", {}),
        "non_claims": [
            "not_live_search_invoked",
            "not_full_project_group_live_coverage_completed",
            "not_default_local_authorization_written",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
        "next_round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001",
    }


def render_markdown(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-20260622",
            "title: Agent-Reach P8 授权后 Pipeline 闭包证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-authorized-pipeline-closure-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-authorized-pipeline-closure-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权后 Pipeline 闭包证据 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- isolated_authorization_status: `{report['isolated_authorization_status']}`",
            f"- pipeline_status_with_isolated_authorizations: `authorized_execution_not_requested`",
            f"- default_local_authorization_files_created: `{report['default_local_authorization_files_created']}`",
            f"- execution_requested: `{report['execution_requested']}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 在临时目录生成三批有效授权文件，验证 pipeline 可识别三批授权齐备。",
            "- 不传入 `--execute`，因此只验证授权闭包，不执行 web/rss/bilibili 请求。",
            "",
            "## stop",
            "",
            "- 停止类型为 `authorization_boundary`。",
            "- 默认 fixtures 授权文件未创建，真实搜索仍等待正式 P8 授权。",
            "",
            "## verify",
            "",
            "- 三批 preflight 状态均为 `authorized_execution_not_requested`。",
            "- 查询质量预检与输出质量门禁仍为 ready/pass。",
            "- `live_external_search_invoked` 保持 `False`。",
            "",
            "## recover",
            "",
            "- 临时授权目录随验证器退出自动删除。",
            "- 若后续正式授权窗口变化，重新运行本验证器即可复核 pipeline 识别逻辑。",
            "",
            "## debug",
            "",
            "- 下一步仍是正式创建三批 `.local.json` 授权文件并执行 pipeline。",
            "- 本证据不声明 full live search completed、accepted、integrated 或 production_ready。",
            "",
        ]
    )


def render_loop(report: dict[str, Any]) -> str:
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-001",
            "title: Agent-Reach P8 授权后 Pipeline 闭包 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-AUTHORIZED-PIPELINE-CLOSURE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 授权后 Pipeline 闭包 Loop 001",
            "",
            "## run",
            "",
            "用临时三批授权文件验证 pipeline 的授权后待执行状态。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；当前状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"pipeline 授权闭包状态 `{report['pipeline_status_with_isolated_authorizations']}`；真实外搜 `{report['security_controls']['live_external_search_invoked']}`。",
            "",
            "## recover",
            "",
            "验证器不写默认授权文件；回滚为删除本轮 evidence/loop 文档和验证脚本。",
            "",
            "## debug",
            "",
            "继续执行仍需正式 P8 Batch 1、Batch 2、Batch 3 授权。",
            "",
        ]
    )


def validate_report(report: dict[str, Any]) -> None:
    if report.get("status") != "p8_authorized_pipeline_closure_ready":
        fail("status_mismatch")
    if report.get("isolated_authorization_status") != "local_authorization_files_written":
        fail("isolated_authorization_not_written")
    if report.get("pipeline_status_with_isolated_authorizations") != "authorized_execution_not_requested":
        fail("pipeline_did_not_reach_authorized_not_requested")
    if report.get("missing_authorization_batches") != []:
        fail("missing_authorization_batches_not_empty")
    if report.get("default_local_authorization_files_created") is not False:
        fail("default_local_authorization_files_created")
    if report.get("execution_requested") is not False:
        fail("execution_requested_not_false")
    controls = report.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    preflight = report.get("preflight_status", {})
    for batch_id in BATCH_IDS:
        if preflight.get(batch_id) != "authorized_execution_not_requested":
            fail(f"batch_preflight_not_authorized_not_requested:{batch_id}")
    quality = report.get("quality_preflight", {})
    if quality.get("query_quality_status") != "p8_query_quality_preflight_pass":
        fail("query_quality_preflight_not_pass")
    if quality.get("output_quality_gate_status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("output_quality_gate_not_ready")


def validate_written(report: dict[str, Any]) -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("id") != report.get("id"):
        fail("written_evidence_id_mismatch")
    for marker in [
        "p8_authorized_pipeline_closure_ready",
        "authorized_execution_not_requested",
        "live_external_search_invoked",
        "不执行 web/rss/bilibili 请求",
        "不声明 full live search completed",
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
    validate_written(report)
    print(
        "agent_reach_p8_authorized_pipeline_closure=pass "
        "status=p8_authorized_pipeline_closure_ready "
        "pipeline_status=authorized_execution_not_requested "
        "default_local_authorization_files_created=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
