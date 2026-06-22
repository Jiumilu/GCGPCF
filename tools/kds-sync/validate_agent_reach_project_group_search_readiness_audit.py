#!/usr/bin/env python3
"""Validate Agent-Reach project-group search readiness without claiming completion."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FULL_GOAL = ROOT / "docs/harness/evidence/agent-reach-full-implementation-goal-20260622.json"
P3 = ROOT / "docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.json"
P6 = ROOT / "docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.json"
P7_AUTH = ROOT / "docs/harness/evidence/agent-reach-p7-authorization-precheck-20260622.json"
P7_DEP = ROOT / "docs/harness/evidence/agent-reach-p7-runtime-dependency-precheck-20260622.json"
P7_WEB = ROOT / "docs/harness/evidence/agent-reach-p7-web-backend-runtime-repair-20260622.json"
P7_QUALITY = ROOT / "docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.json"
P7_RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
P7_RUNTIME_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-limited-live-search-dry-run-20260622.json"
LOCAL_AUTH = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.local.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-project-group-search-readiness-audit-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-search-readiness-audit-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001.md"

EXPECTED_PROJECT_SCOPE = {
    "GPCF",
    "KDS",
    "WAES",
    "Brain",
    "GFIS",
    "GPC",
    "PVAOS",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
}
EXPECTED_P7_PILOT_PROJECTS = {"GPCF", "GFIS", "KDS", "WAES", "GPC"}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_project_group_search_readiness_audit=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_runner_report() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", P7_RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_report(LOCAL_AUTH, execute=False)


def main() -> None:
    full_goal = load_json(FULL_GOAL)
    p3 = load_json(P3)
    p6 = load_json(P6)
    p7_auth = load_json(P7_AUTH)
    p7_dep = load_json(P7_DEP)
    p7_web = load_json(P7_WEB)
    p7_quality = load_json(P7_QUALITY)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    default_runner = load_runner_report()

    if full_goal.get("status") != "full_implementation_prompt_ready":
        fail("full_goal_not_ready")
    if set(full_goal.get("project_scope", [])) != EXPECTED_PROJECT_SCOPE:
        fail("full_goal_project_scope_mismatch")
    if p3.get("status") != "quality_replay_harness_ready":
        fail("p3_replay_not_ready")
    if p3.get("metrics", {}).get("threshold_pass") is not True:
        fail("p3_threshold_not_pass")
    if p6.get("status") != "limited_live_search_dry_run_preparation_ready":
        fail("p6_not_ready")
    if p7_auth.get("status") != "p7_authorization_precheck_ready":
        fail("p7_auth_precheck_not_ready")
    if p7_dep.get("status") != "runtime_dependencies_ready":
        fail("p7_dependencies_not_ready")
    if p7_web.get("status") != "web_backend_runtime_dependency_repaired":
        fail("p7_web_backend_not_repaired")
    if p7_quality.get("status") != "limited_live_search_output_quality_gate_ready":
        fail("p7_quality_gate_not_ready")
    if P7_RUNTIME_JSON.exists():
        fail("p7_runtime_evidence_exists_before_authorized_run")
    if default_runner.get("status") != "blocked_pending_execution_authorization":
        fail("default_runner_not_blocked")
    if "authorization_file_missing" not in default_runner.get("authorization_reasons", []):
        fail("default_runner_missing_authorization_reason_absent")
    if default_runner.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("default_runner_live_search_invoked")
    if len(default_runner.get("execution_plan", [])) != 5:
        fail("p7_execution_plan_count_mismatch")
    pilot_projects = {item.get("project") for item in default_runner.get("execution_plan", [])}
    if pilot_projects != EXPECTED_P7_PILOT_PROJECTS:
        fail("p7_pilot_project_scope_mismatch")

    if evidence.get("status") != "search_readiness_verified_pending_p7_authorization":
        fail("evidence_status_mismatch")
    if evidence.get("completion_claim_allowed") is not False:
        fail("completion_claim_allowed_not_false")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    checks = evidence.get("readiness_checks", {})
    for field in [
        "full_project_scope_declared_14_projects",
        "offline_replay_quality_passed",
        "p7_query_plan_prepared",
        "p7_authorization_precheck_ready",
        "p7_runtime_dependencies_ready",
        "p7_web_backend_ready",
        "p7_output_quality_gate_ready",
        "default_runner_blocks_without_authorization",
        "no_p7_runtime_evidence_written",
        "no_live_external_search_invoked",
    ]:
        if checks.get(field) is not True:
            fail(f"readiness_check_not_true:{field}")
    gaps = set(evidence.get("remaining_completion_gaps", []))
    for gap in [
        "p7_execution_authorization_missing",
        "p7_live_runtime_evidence_missing",
        "project_group_14_project_live_coverage_missing",
        "human_review_and_production_admission_missing",
    ]:
        if gap not in gaps:
            fail(f"remaining_gap_missing:{gap}")
    for marker in [
        "search_readiness_verified_pending_p7_authorization",
        "p7_execution_authorization_missing",
        "不声明项目群全量真实搜索已完成",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_project_group_search_readiness_audit=pass "
        "status=search_readiness_verified_pending_p7_authorization "
        "project_scope=14 p7_pilot_projects=5 "
        "offline_replay_quality=pass p7_quality_gate=pass "
        "live_external_search_invoked=false "
        "completion_claim_allowed=false "
        "next=GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001"
    )


if __name__ == "__main__":
    main()
