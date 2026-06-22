#!/usr/bin/env python3
"""Validate Agent-Reach P2 controlled adapter skeleton artifacts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_controlled_adapter_dry_run.py"
FIXTURE = ROOT / "fixtures/agent-reach/controlled-adapter-dry-run.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p2-controlled-adapter-skeleton-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p2-controlled-adapter-skeleton-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001.md"
ADAPTER_MD = ROOT / "third_party/agent-reach/CONTROLLED_ADAPTER.md"

REQUIRED_POLICY_BLOCKS = {
    "credential_required_channel",
    "production_write",
    "kds_canonical_write",
    "gfis_source_of_record_write",
    "global_mcp_config_write",
    "live_external_search_without_authorization",
}
REQUIRED_SCHEMA_FIELDS = {
    "candidate_id",
    "channel",
    "title",
    "source_url",
    "snippet",
    "evidence_tier",
    "admission_status",
}


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p2_controlled_adapter_skeleton=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_runner_report() -> dict:
    spec = importlib.util.spec_from_file_location("agent_reach_adapter_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_report()


def main() -> None:
    fixture = json.loads(read_text(FIXTURE))
    evidence = json.loads(read_text(EVIDENCE_JSON))
    evidence_md = read_text(EVIDENCE_MD)
    loop = read_text(LOOP_MD)
    adapter = read_text(ADAPTER_MD)
    report = load_runner_report()

    if evidence.get("status") != "controlled_adapter_skeleton_ready":
        fail("unexpected_status")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    if evidence.get("mode") != "dry_run_only":
        fail("mode_not_dry_run")
    if fixture.get("mode") != "dry_run_only":
        fail("fixture_mode_not_dry_run")
    if report.get("status") != "controlled_adapter_skeleton_ready":
        fail("runner_status_mismatch")
    if report.get("mode") != "dry_run_only":
        fail("runner_mode_mismatch")
    checks = report.get("checks", {})
    for field in ["fixture_loaded", "candidate_schema_valid", "candidate_only", "fixture_only"]:
        if checks.get(field) is not True:
            fail(f"{field}_not_true")
    if checks.get("allowed_command_count") != 3:
        fail("allowed_command_count_mismatch")
    if checks.get("blocked_command_count") != 6:
        fail("blocked_command_count_mismatch")
    if checks.get("candidate_count") != 2:
        fail("candidate_count_mismatch")
    if set(report.get("policy_block_reasons", [])) != REQUIRED_POLICY_BLOCKS:
        fail("policy_block_reasons_mismatch")
    if set(report.get("candidate_result_schema", [])) != REQUIRED_SCHEMA_FIELDS:
        fail("candidate_schema_fields_mismatch")
    controls = report.get("security_controls", {})
    for field in [
        "agent_reach_binary_invoked",
        "live_external_search_invoked",
        "doctor_health_probe_invoked",
        "credential_written",
        "browser_cookie_extraction_invoked",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if controls.get(field) is not False:
            fail(f"{field}_not_false")
    for marker in [
        "doc_id:",
        "status: controlled",
        "kds_space: 开发",
        "source_path: third_party/agent-reach/CONTROLLED_ADAPTER.md",
    ]:
        if marker not in adapter:
            fail(f"adapter_missing:{marker}")
    for phrase in [
        "不声明真实搜索已调用",
        "不声明搜索质量已验收",
        "不声明 accepted / integrated / production_ready",
    ]:
        if phrase not in evidence_md:
            fail(f"evidence_missing:{phrase}")
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop:
            fail(f"loop_missing_section:{section}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001":
        fail("next_round_mismatch")
    if report.get("next_round") != evidence.get("next_round"):
        fail("runner_next_round_mismatch")

    print(
        "agent_reach_p2_controlled_adapter_skeleton=pass "
        "status=controlled_adapter_skeleton_ready "
        "current_admission=limited_candidate_only "
        "mode=dry_run_only "
        "allowed_commands=3 blocked_commands=6 "
        "candidate_schema_fields=7 candidate_count=2 "
        "live_external_search_invoked=false "
        "agent_reach_binary_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
