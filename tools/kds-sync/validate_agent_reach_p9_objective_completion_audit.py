#!/usr/bin/env python3
"""Audit Agent-Reach P9 objective completion against current evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
P9_PRECHECK = ROOT / "fixtures/agent-reach/p9-priority-target-hit-rate-precheck-20260626.json"
P9S_PRECHECK_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-precheck-20260626.json"
P9S_LIVE_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-hit-rate-live-run-20260626.json"
P9S_LIVE_REWORK_CLASSIFICATION = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-rework-classification-20260627.json"
P9R_RERUN_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p9-priority-target-hit-rate-rerun-20260626.json"
P9R_REWORK_CLASSIFICATION = ROOT / "docs/harness/evidence/agent-reach-p9-rerun-rework-classification-20260626.json"
P9S_CLOSURE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-readiness-closure-20260626.json"
DRIFT_MONITOR = ROOT / "docs/harness/evidence/agent-reach-full-coverage-markdown-drift-monitor-20260626.json"
P9S_DRIFT_MONITOR = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-markdown-drift-monitor-20260626.json"
P9S_REVIEW_BRIDGE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-review-queue-bridge-readiness-20260626.json"
P9S_COMMAND_PACK = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-execution-command-pack-20260626.json"
P9S_CLOSURE_RUNNER = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-20260626.json"
P9S_CLOSURE_RUNNER_READINESS = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-runner-readiness-20260626.json"
P9S_CLOSURE_AUTHORIZATION_GATE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-closure-authorization-gate-20260626.json"
P9S_AUTH_INTAKE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-live-authorization-intake-20260626.json"
P9S_OFFLINE_SIMULATION = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-offline-hit-rate-simulation-20260626.json"
P9S_AUTH_NEGATIVE_FIXTURES = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-negative-fixtures-20260626.json"
P9S_AUTH_TEMPLATE = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-template-20260626.json"
P9S_AUTH_FILE_SAFETY = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-file-safety-20260626.json"
P9S_AUTH_HANDOFF_PACK = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-authorization-handoff-pack-20260626.json"
P9S_PRE_LIVE_PREFLIGHT = ROOT / "docs/harness/evidence/agent-reach-p9-source-direct-pre-live-preflight-20260626.json"
P9_POST_LIVE_PATH_SIMULATION = ROOT / "docs/harness/evidence/agent-reach-p9-objective-post-live-path-simulation-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p9-objective-completion-audit-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p9-objective-completion-audit-20260626.md"

REQUIRED_TOPICS = {"green_supply_chain", "phosphogypsum", "industrial_solid_waste", "zero_waste_city"}
REQUIRED_OBJECTIVE_FIELDS = {
    "supplier_esg",
    "solid_waste_disposal_receipt",
    "resource_utilization_product",
    "product_carbon_footprint",
    "zero_waste_city_indicator",
    "green_financing_purpose",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p9_objective_completion_audit=fail reason={message}")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def requirement(status: str, evidence: str, summary: str) -> dict[str, Any]:
    return {"status": status, "evidence": evidence, "summary": summary}


def validate_no_boundary_violation(*evidences: dict[str, Any]) -> None:
    for evidence in evidences:
        controls = evidence.get("security_controls", {})
        if controls.get("credential_written") is True:
            fail("credential_written_detected")
        if controls.get("browser_cookie_extraction_invoked") is True:
            fail("cookie_extraction_detected")
        if controls.get("kds_canonical_write_allowed") is True:
            fail("kds_canonical_write_allowed_detected")
        if controls.get("gfis_source_of_record_write_allowed") is True:
            fail("gfis_source_of_record_write_allowed_detected")
        if evidence.get("completion_claim_allowed") is True:
            fail("completion_claim_allowed_detected")


def build_report() -> dict[str, Any]:
    p9_precheck = read_json(P9_PRECHECK)
    p9s_precheck = read_json(P9S_PRECHECK_EVIDENCE)
    p9s_live = read_json(P9S_LIVE_EVIDENCE)
    p9s_live_rework = read_json(P9S_LIVE_REWORK_CLASSIFICATION)
    p9r_rerun = read_json(P9R_RERUN_EVIDENCE)
    p9r_rework = read_json(P9R_REWORK_CLASSIFICATION)
    p9s_closure = read_json(P9S_CLOSURE)
    drift = read_json(DRIFT_MONITOR)
    p9s_drift = read_json(P9S_DRIFT_MONITOR)
    review = read_json(P9S_REVIEW_BRIDGE)
    command_pack = read_json(P9S_COMMAND_PACK)
    closure_runner = read_json(P9S_CLOSURE_RUNNER)
    closure_runner_readiness = read_json(P9S_CLOSURE_RUNNER_READINESS)
    closure_authorization_gate = read_json(P9S_CLOSURE_AUTHORIZATION_GATE)
    auth_intake = read_json(P9S_AUTH_INTAKE)
    offline_simulation = read_json(P9S_OFFLINE_SIMULATION)
    auth_negative = read_json(P9S_AUTH_NEGATIVE_FIXTURES)
    auth_template = read_json(P9S_AUTH_TEMPLATE)
    auth_file_safety = read_json(P9S_AUTH_FILE_SAFETY)
    auth_handoff = read_json(P9S_AUTH_HANDOFF_PACK)
    pre_live_preflight = read_json(P9S_PRE_LIVE_PREFLIGHT)
    post_live_path_simulation = read_json(P9_POST_LIVE_PATH_SIMULATION)
    validate_no_boundary_violation(
        p9s_live,
        p9s_live_rework,
        p9r_rerun,
        p9r_rework,
        p9s_closure,
        command_pack,
        closure_runner,
        closure_runner_readiness,
        closure_authorization_gate,
        auth_intake,
        offline_simulation,
        auth_negative,
        auth_template,
        auth_file_safety,
        auth_handoff,
        pre_live_preflight,
        post_live_path_simulation,
    )

    topic_count = len(p9_precheck.get("topics", []))
    query_count = sum(len(topic.get("query_expansion", [])) for topic in p9_precheck.get("topics", []))
    topic_ids = {topic.get("topic_id") for topic in p9_precheck.get("topics", [])}
    boost_policy = p9_precheck.get("domain_boost_policy", {})
    mapped_fields = {field for fields in p9_precheck.get("business_field_mapping", {}).values() for field in fields}

    live_hit_rate = p9s_live.get("hit_rate_report", {})
    live_completed = (
        p9s_live.get("status") == "p9_source_direct_hit_rate_completed"
        and live_hit_rate.get("threshold_pass") is True
        and live_hit_rate.get("topic_coverage") == 1.0
        and p9s_live.get("security_controls", {}).get("live_external_fetch_invoked") is True
    )
    pre_live_source_direct_ready = (
        p9s_closure.get("status") == "p9_source_direct_live_execution_readiness_closure_ready"
        and command_pack.get("status") == "p9_source_direct_live_execution_command_pack_ready"
        and closure_runner.get("status") == "blocked_pending_p9_source_direct_authorization"
        and closure_runner.get("live_external_fetch_invoked") is False
        and closure_runner_readiness.get("status") == "p9_source_direct_live_closure_runner_readiness_pass"
        and closure_runner_readiness.get("live_external_fetch_invoked") is False
        and closure_authorization_gate.get("status") == "p9_source_direct_live_closure_authorization_gate_pass"
        and closure_authorization_gate.get("live_external_fetch_invoked") is False
        and offline_simulation.get("status") == "p9_source_direct_offline_hit_rate_simulation_pass"
        and offline_simulation.get("threshold_pass") is True
        and offline_simulation.get("live_external_fetch_invoked") is False
        and pre_live_preflight.get("status") == "p9_source_direct_pre_live_preflight_pass"
        and post_live_path_simulation.get("status") == "p9_objective_post_live_path_simulation_pass"
    )
    post_live_source_direct_completed = (
        live_completed
        and command_pack.get("status") == "p9_source_direct_live_execution_command_pack_ready"
        and closure_runner.get("status") == "p9_source_direct_live_closure_completed"
        and closure_runner.get("live_external_fetch_invoked") is True
    )
    live_rework_classified = (
        p9s_live_rework.get("status") == "p9_source_direct_live_rework_classification_pass"
        and p9s_live_rework.get("classification") == "p9s_live_hit_rate_rework_required"
        and p9s_live_rework.get("live_external_fetch_invoked") is True
    )
    authorization_boundary_complete = (
        live_completed
        or auth_intake.get("status") == "p9_source_direct_live_authorization_intake_ready"
        or p9s_live.get("authorization_valid") is True
    )
    source_direct_ready = pre_live_source_direct_ready or post_live_source_direct_completed or live_rework_classified
    requirements = {
        "priority_target_hit_rate_assessment": requirement(
            "missing_live_authorized_execution" if not live_completed else "complete",
            P9S_LIVE_EVIDENCE.relative_to(ROOT).as_posix(),
            "真实站点命中率/主题覆盖率尚未完成；P9R 搜索引擎路径已授权复跑但仍为 rework，P9S source-direct live evidence 仍为授权前 blocked 占位。"
            if not live_completed and not live_rework_classified
            else "真实站点命中率/主题覆盖率尚未通过；P9S source-direct 已授权执行但需要 rework。"
            if live_rework_classified
            else "真实站点命中率/主题覆盖率已通过。",
        ),
        "topic_query_expansion": requirement(
            "complete" if topic_ids == REQUIRED_TOPICS and topic_count == 4 and query_count >= 12 else "incomplete",
            P9_PRECHECK.relative_to(ROOT).as_posix(),
            f"已配置 {topic_count} 个主题、{query_count} 条 query expansion。",
        ),
        "domain_boost_source_scoring": requirement(
            "complete"
            if boost_policy.get("mode") == "candidate_scoring_only"
            and {"P0", "P1"} <= set(boost_policy.get("priority_domains", {}))
            and boost_policy.get("must_preserve_candidate_only") is True
            else "incomplete",
            P9_PRECHECK.relative_to(ROOT).as_posix(),
            "已配置 P0/P1 domain boost，且保持 candidate-only。",
        ),
        "markdown_drift_monitor": requirement(
            "complete"
            if drift.get("status") == "full_coverage_markdown_drift_monitor_pass"
            and p9s_drift.get("status") == "p9_source_direct_markdown_drift_monitor_pass"
            else "incomplete",
            DRIFT_MONITOR.relative_to(ROOT).as_posix(),
            "full coverage 与 P9S source-direct Markdown candidate-only / non-claim marker 漂移监控已通过。",
        ),
        "gfis_was_business_mapping": requirement(
            "complete"
            if REQUIRED_OBJECTIVE_FIELDS <= mapped_fields
            and review.get("coverage", {}).get("route_project_coverage") == ["GFIS", "KDS", "WAES", "WAS"]
            else "incomplete",
            P9S_REVIEW_BRIDGE.relative_to(ROOT).as_posix(),
            "P9S source-direct target 已映射到 GFIS/WAS/WAES/KDS review lanes，且仅 preview-only。",
        ),
        "source_direct_readiness": requirement(
            "complete"
            if source_direct_ready
            else "incomplete",
            P9S_CLOSURE.relative_to(ROOT).as_posix(),
            "P9R rerun rework 已分类；P9S source-direct 支持授权前 readiness 和授权后 closure completed 两种受控完成路径。",
        ),
        "authorization_boundary": requirement(
            "complete"
            if authorization_boundary_complete
            else (
            "pending_human_authorization"
            if auth_intake.get("status") == "blocked_pending_p9_source_direct_authorization"
            and auth_negative.get("status") == "p9_source_direct_authorization_negative_fixtures_pass"
            and auth_template.get("status") == "p9_source_direct_authorization_template_ready"
            and auth_file_safety.get("status") == "p9_source_direct_authorization_file_safety_ready"
            and auth_handoff.get("status") == "p9_source_direct_authorization_handoff_pack_ready"
            else "ready_for_live_execution"
            ),
            P9S_AUTH_INTAKE.relative_to(ROOT).as_posix(),
            "P9S live 授权与执行已完成。"
            if live_completed
            else "P9S live 授权已通过并已执行，当前进入命中率 rework。"
            if authorization_boundary_complete
            else (
                "当前缺少 P9S live 授权文件；授权模板、负样例、local 授权文件安全边界与授权交接包已准备，未触发 live fetch。"
                if auth_intake.get("status") == "blocked_pending_p9_source_direct_authorization"
                else "授权 intake 已通过，可进入 live execution。"
            ),
        ),
    }
    completed = [key for key, item in requirements.items() if item["status"] == "complete"]
    incomplete = [key for key, item in requirements.items() if item["status"] not in {"complete", "ready_for_live_execution"}]
    status = (
        "p9_objective_completed"
        if live_completed and not incomplete
        else "p9_objective_not_completed_hit_rate_rework"
        if live_rework_classified
        else "p9_objective_not_completed_authorization_boundary"
    )
    return {
        "id": "agent-reach-p9-objective-completion-audit-20260626",
        "date": "2026-06-26",
        "status": status,
        "current_admission": "limited_candidate_only",
        "completion_claim_allowed": live_completed and not incomplete,
        "live_external_fetch_invoked": p9s_live.get("security_controls", {}).get("live_external_fetch_invoked") is True,
        "requirements": requirements,
        "search_provider_path_summary": {
            "rerun_status": p9r_rerun.get("status"),
            "rerun_authorization_valid": p9r_rerun.get("authorization_valid"),
            "rerun_live_external_search_invoked": p9r_rerun.get("security_controls", {}).get("live_external_search_invoked"),
            "rerun_candidate_count": p9r_rerun.get("hit_rate_report", {}).get("candidate_count"),
            "rerun_query_error_count": p9r_rerun.get("hit_rate_report", {}).get("query_error_count"),
            "rerun_rework_classification": p9r_rework.get("classification"),
            "recommended_next_path": p9r_rework.get("recommended_next_path"),
        },
        "source_direct_execution_mode": (
            "post_live_closure_completed"
            if post_live_source_direct_completed
            else ("p9s_live_rework_required" if live_rework_classified else ("pre_live_ready" if pre_live_source_direct_ready else "not_ready"))
        ),
        "completed_requirement_count": len(completed),
        "incomplete_requirements": incomplete,
        "blocking_condition": (
            None
            if live_completed
            else "p9s_live_hit_rate_rework_required"
            if live_rework_classified
            else "p9s_live_authorization_missing"
        ),
        "next_required_authorization_text": None if authorization_boundary_complete else "授权执行 Agent-Reach P9S Source Direct Hit-Rate Live Run",
        "non_claims": [
            "audit_only",
            "not_live_fetch_invoked" if not live_completed else "live_fetch_invoked_by_prior_evidence",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "---",
        "doc_id: GPCF-DOC-AGENT-REACH-P9-OBJECTIVE-COMPLETION-AUDIT-20260626",
        "title: Agent-Reach P9 Objective Completion Audit 2026-06-26",
        "project: KDS",
        "related_projects: [GFIS, WAS, WAES, KDS, GPCF]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: KDS",
        "kds_space: 开发",
        "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p9-objective-completion-audit-20260626.md",
        "source_path: docs/harness/evidence/agent-reach-p9-objective-completion-audit-20260626.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-26",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Agent-Reach P9 Objective Completion Audit 2026-06-26",
        "",
        f"- status: `{report['status']}`",
        f"- completion_claim_allowed: `{report['completion_claim_allowed']}`",
        f"- completed_requirement_count: `{report['completed_requirement_count']}`",
        f"- blocking_condition: `{report['blocking_condition']}`",
        f"- search_provider_path: `{report['search_provider_path_summary']['rerun_rework_classification']}`",
        f"- recommended_next_path: `{report['search_provider_path_summary']['recommended_next_path']}`",
        "",
        "## Requirements",
        "",
    ]
    for key, item in report["requirements"].items():
        lines.append(f"- `{key}`: `{item['status']}` - {item['summary']}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This evidence is an objective completion audit only.",
            "- This evidence does not invoke live target-site fetch.",
            "- This evidence does not write KDS canonical Markdown.",
            "- This evidence does not write GFIS source-of-record.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    report = build_report()
    write_json(EVIDENCE_JSON, report)
    EVIDENCE_MD.write_text(render_markdown(report), encoding="utf-8")
    print(
        "agent_reach_p9_objective_completion_audit=pass "
        f"status={report['status']} completed={report['completed_requirement_count']} "
        f"blocking_condition={report['blocking_condition']}"
    )


if __name__ == "__main__":
    main()
