#!/usr/bin/env python3
"""Validate Agent-Reach P7 execution harness authorization guard."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"
AUTH_TEMPLATE = ROOT / "fixtures/agent-reach/limited-live-search-dry-run-authorization.template.json"
P6_EVIDENCE = ROOT / "docs/harness/evidence/agent-reach-p6-limited-live-search-dry-run-preparation-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-execution-harness-guard-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-execution-harness-guard-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-EXECUTION-HARNESS-GUARD-001.md"

SECURITY_FALSE_FIELDS = [
    "agent_reach_binary_invoked",
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
    raise SystemExit(f"agent_reach_p7_execution_harness_guard=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def load_runner_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_runner_report(module) -> dict:
    missing_auth = ROOT / "fixtures/agent-reach/__missing_p7_authorization__.json"
    return module.build_report(missing_auth, execute=False)


def validate_evidence_writer(module, runner_report: dict) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        json_path = tmp / "agent-reach-p7-runtime.json"
        md_path = tmp / "agent-reach-p7-runtime.md"
        module.write_evidence(runner_report, json_path, md_path)
        written_json = load_json(json_path)
        written_md = read_text(md_path)
    if written_json.get("status") != "blocked_pending_execution_authorization":
        fail("writer_json_status_mismatch")
    if written_json.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("writer_json_live_external_not_false")
    for marker in [
        "candidate-only",
        "Raw provider payloads are not persisted",
        "accepted, integrated, or production_ready",
    ]:
        if marker not in written_md:
            fail(f"writer_md_missing:{marker}")


def main() -> None:
    auth_template = load_json(AUTH_TEMPLATE)
    p6 = load_json(P6_EVIDENCE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    runner_module = load_runner_module()
    runner_report = load_runner_report(runner_module)
    validate_evidence_writer(runner_module, runner_report)

    if p6.get("status") != "limited_live_search_dry_run_preparation_ready":
        fail("p6_not_ready")
    if auth_template.get("authorization_status") != "pending_human_authorization":
        fail("auth_template_status_mismatch")
    if auth_template.get("allow_external_network") is not True:
        fail("auth_template_external_network_not_true")
    if auth_template.get("allow_write_evidence_only") is not True:
        fail("auth_template_evidence_only_not_true")
    if "allow_agent_reach_binary_invocation" not in auth_template:
        fail("auth_template_binary_field_missing")
    if runner_report.get("status") != "blocked_pending_execution_authorization":
        fail("runner_missing_auth_not_blocked")
    if "authorization_file_missing" not in runner_report.get("authorization_reasons", []):
        fail("runner_missing_auth_reason_missing")
    controls = runner_report.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"runner_security_control_not_false:{field}")
    if runner_report.get("candidates") != []:
        fail("runner_candidates_not_empty_without_auth")
    if len(runner_report.get("execution_plan", [])) != 5:
        fail("runner_execution_plan_count_mismatch")

    if evidence.get("status") != "limited_live_search_execution_harness_guard_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("guard_checks", {})
    for field in [
        "authorization_template_created",
        "runner_created",
        "default_without_authorization_blocks",
        "requires_execute_flag_for_network",
        "quality_report_available",
        "evidence_writer_available",
        "output_contract_paths_supported",
    ]:
        if checks.get(field) is not True:
            fail(f"guard_check_not_true:{field}")
    evidence_controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if evidence_controls.get(field) is not False:
            fail(f"evidence_security_control_not_false:{field}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001":
        fail("next_round_mismatch")

    for marker in [
        "limited_live_search_execution_harness_guard_ready",
        "blocked_pending_execution_authorization",
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p7_execution_harness_guard=pass "
        "status=limited_live_search_execution_harness_guard_ready "
        "default_without_authorization=blocked "
        "live_external_search_invoked=false "
        "agent_reach_binary_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
