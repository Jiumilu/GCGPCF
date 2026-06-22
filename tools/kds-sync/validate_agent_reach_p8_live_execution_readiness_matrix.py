#!/usr/bin/env python3
"""Build the final P8 live execution readiness matrix before human authorization."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-live-execution-readiness-matrix-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-live-execution-readiness-matrix-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-001.md"
REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"

GATES = {
    "authorization_text_intake": ROOT / "tools/kds-sync/validate_agent_reach_p8_authorization_text_intake.py",
    "local_authorization_window_audit": ROOT / "tools/kds-sync/validate_agent_reach_p8_local_authorization_window_audit.py",
    "authorized_pipeline_closure": ROOT / "tools/kds-sync/validate_agent_reach_p8_authorized_pipeline_closure.py",
    "execution_audit_bundle": ROOT / "tools/kds-sync/validate_agent_reach_p8_execution_audit_bundle.py",
    "post_authorization_driver": ROOT / "tools/kds-sync/validate_agent_reach_p8_post_authorization_driver.py",
    "query_quality_preflight": ROOT / "tools/kds-sync/validate_agent_reach_p8_query_quality_preflight.py",
    "output_quality_gate": ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py",
    "rework_queue": ROOT / "tools/kds-sync/validate_agent_reach_p8_rework_queue.py",
    "batch_runtime_runner": ROOT / "tools/kds-sync/validate_agent_reach_p8_batch_runtime_runner.py",
    "batch_merge_runner": ROOT / "tools/kds-sync/validate_agent_reach_p8_batch_merge_runner.py",
    "full_pipeline": ROOT / "tools/kds-sync/validate_agent_reach_p8_full_live_search_pipeline.py",
}
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
    raise SystemExit(f"agent_reach_p8_live_execution_readiness_matrix=fail reason={message}")


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


def run_gate(path: Path, name: str) -> dict[str, Any]:
    module = load_module(path, f"agent_reach_p8_{name}")
    try:
        module.main()
        return {"status": "pass", "reason": ""}
    except SystemExit as exc:
        code = exc.code
        if code in (0, None):
            return {"status": "pass", "reason": ""}
        return {"status": "fail", "reason": str(exc)}


def local_authorization_files(request: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in request.get("batch_authorization_requests", []):
        path = ROOT / item["authorization_file_to_create_after_human_approval"]
        rows.append({"batch_id": item["batch_id"], "path": str(path.relative_to(ROOT)), "exists": path.exists()})
    return rows


def build_report() -> dict[str, Any]:
    request = load_json(REQUEST)
    gate_results = {name: run_gate(path, name) for name, path in GATES.items()}
    auth_files = local_authorization_files(request)
    missing_auth = [row["batch_id"] for row in auth_files if row["exists"] is False]
    all_gates_pass = all(result["status"] == "pass" for result in gate_results.values())
    ready_pending_auth = all_gates_pass and sorted(missing_auth) == ["p8-batch-1", "p8-batch-2", "p8-batch-3"]
    return {
        "id": "agent-reach-p8-live-execution-readiness-matrix-20260622",
        "round": "GPCF-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-001",
        "date": "2026-06-22",
        "status": "p8_live_execution_ready_pending_human_authorization"
        if ready_pending_auth
        else "p8_live_execution_readiness_rework_required",
        "current_admission": "limited_candidate_only",
        "gate_results": gate_results,
        "authorization_state": {
            "request_status": request.get("authorization_status"),
            "execution_allowed_now": request.get("execution_allowed_now"),
            "generated_local_authorization_files": request.get("generated_local_authorization_files"),
            "local_authorization_files": auth_files,
            "missing_authorization_batches": missing_auth,
            "required_authorization_texts": [
                item["required_text"] for item in request.get("batch_authorization_requests", [])
            ],
        },
        "readiness_summary": {
            "all_local_quality_gates_pass": all_gates_pass,
            "human_authorization_required": True,
            "can_execute_live_now": False,
            "ready_after_valid_authorization_text": ready_pending_auth,
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
    gate_lines = "\n".join(f"- {name}: `{result['status']}`" for name, result in report["gate_results"].items())
    auth_lines = "\n".join(f"- `{text}`" for text in report["authorization_state"]["required_authorization_texts"])
    missing = ", ".join(report["authorization_state"]["missing_authorization_batches"])
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-20260622",
            "title: Agent-Reach P8 真实搜索执行准备矩阵 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-live-execution-readiness-matrix-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-p8-live-execution-readiness-matrix-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 真实搜索执行准备矩阵 2026-06-22",
            "",
            f"- status: `{report['status']}`",
            f"- all_local_quality_gates_pass: `{report['readiness_summary']['all_local_quality_gates_pass']}`",
            f"- human_authorization_required: `{report['readiness_summary']['human_authorization_required']}`",
            f"- can_execute_live_now: `{report['readiness_summary']['can_execute_live_now']}`",
            f"- missing_authorization_batches: `{missing}`",
            f"- live_external_search_invoked: `{report['security_controls']['live_external_search_invoked']}`",
            "",
            "## run",
            "",
            "- 聚合 P8 授权摄取、授权后 driver、查询质量、输出质量、返工队列、batch runner、merge runner 和 pipeline gate。",
            "- 本矩阵用于真实搜索前最终机检，不执行真实搜索，不创建默认授权文件。",
            "",
            "## stop",
            "",
            "- 停止类型为 `authorization_boundary`。",
            "- 所有本地质量 gate 已准备，真实执行仍需人工授权。",
            "",
            "## verify",
            "",
            gate_lines,
            "",
            "## recover",
            "",
            "- 若任一 gate 失败，先修复对应 validator/evidence，再重新生成本矩阵。",
            "- 若正式授权文本不合规，摄取脚本会拒绝创建本地授权文件。",
            "",
            "## debug",
            "",
            "下一步需要正式授权：",
            "",
            auth_lines,
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
            "doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-001",
            "title: Agent-Reach P8 真实搜索执行准备矩阵 Loop 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS]",
            "domain: governance",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-LIVE-EXECUTION-READINESS-MATRIX-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach P8 真实搜索执行准备矩阵 Loop 001",
            "",
            "## run",
            "",
            "生成 P8 真实搜索前最终 readiness matrix。",
            "",
            "## stop",
            "",
            f"停止类型为 `authorization_boundary`；矩阵状态 `{report['status']}`。",
            "",
            "## verify",
            "",
            f"本地质量 gate `{report['readiness_summary']['all_local_quality_gates_pass']}`；真实外搜 `{report['security_controls']['live_external_search_invoked']}`。",
            "",
            "## recover",
            "",
            "删除本轮矩阵 evidence/loop 文档和验证器即可回滚。",
            "",
            "## debug",
            "",
            "继续执行需要正式 P8 三批授权。",
            "",
        ]
    )


def validate_report(report: dict[str, Any]) -> None:
    if report.get("status") != "p8_live_execution_ready_pending_human_authorization":
        fail("status_mismatch")
    if report["readiness_summary"]["all_local_quality_gates_pass"] is not True:
        fail("local_quality_gates_not_all_pass")
    if report["readiness_summary"]["can_execute_live_now"] is not False:
        fail("can_execute_live_now_should_be_false")
    if sorted(report["authorization_state"]["missing_authorization_batches"]) != ["p8-batch-1", "p8-batch-2", "p8-batch-3"]:
        fail("missing_authorization_batches_mismatch")
    for field in SECURITY_FALSE_FIELDS:
        if report["security_controls"].get(field) is not False:
            fail(f"security_control_not_false:{field}")


def validate_written(report: dict[str, Any]) -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    if evidence.get("id") != report.get("id"):
        fail("written_evidence_id_mismatch")
    for marker in [
        "p8_live_execution_ready_pending_human_authorization",
        "all_local_quality_gates_pass",
        "authorization_boundary",
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
    validate_written(report)
    print(
        "agent_reach_p8_live_execution_readiness_matrix=pass "
        "status=p8_live_execution_ready_pending_human_authorization "
        "all_local_quality_gates_pass=true "
        "can_execute_live_now=false "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
