#!/usr/bin/env python3
"""Validate Agent-Reach P3 offline quality replay harness artifacts."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_quality_replay_harness.py"
FIXTURE = ROOT / "fixtures/agent-reach/quality-replay-harness.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001.md"
HARNESS_MD = ROOT / "third_party/agent-reach/QUALITY_REPLAY_HARNESS.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p3_quality_replay_harness=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_runner_report() -> dict:
    spec = importlib.util.spec_from_file_location("agent_reach_quality_runner", RUNNER)
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
    harness = read_text(HARNESS_MD)
    report = load_runner_report()

    if evidence.get("status") != "quality_replay_harness_ready":
        fail("unexpected_status")
    if evidence.get("current_admission") != "limited_candidate_only":
        fail("current_admission_not_limited")
    if evidence.get("mode") != "offline_replay_only":
        fail("evidence_mode_mismatch")
    if fixture.get("mode") != "offline_replay_only":
        fail("fixture_mode_mismatch")
    if report.get("status") != "quality_replay_harness_ready":
        fail("runner_status_mismatch")
    if report.get("mode") != "offline_replay_only":
        fail("runner_mode_mismatch")
    metrics = evidence.get("metrics", {})
    for field in ["query_count", "candidate_count", "average_score", "precision_at_1", "required_field_coverage", "forbidden_claim_count"]:
        if metrics.get(field) != report.get(field):
            fail(f"metric_mismatch:{field}")
    if report.get("query_count") != 3:
        fail("query_count_mismatch")
    if report.get("candidate_count") != 5:
        fail("candidate_count_mismatch")
    if report.get("average_score") < 0.78:
        fail("average_score_below_threshold")
    if report.get("precision_at_1") < 0.66:
        fail("precision_at_1_below_threshold")
    if report.get("required_field_coverage") != 1.0:
        fail("field_coverage_mismatch")
    if report.get("forbidden_claim_count") != 0:
        fail("forbidden_claims_present")
    if report.get("threshold_pass") is not True:
        fail("threshold_not_pass")
    if len(report.get("query_reports", [])) != 3:
        fail("query_reports_count_mismatch")
    if not all(item.get("precision_at_1_hit") is True for item in report.get("query_reports", [])):
        fail("top_hit_mismatch")
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
        "source_path: third_party/agent-reach/QUALITY_REPLAY_HARNESS.md",
    ]:
        if marker not in harness:
            fail(f"harness_missing:{marker}")
    for phrase in [
        "不声明真实搜索已调用",
        "不声明真实搜索质量已验收",
        "不声明 accepted / integrated / production_ready",
    ]:
        if phrase not in evidence_md:
            fail(f"evidence_missing:{phrase}")
    for section in ["输入", "动作", "输出", "检查", "反馈", "下一轮"]:
        if f"## {section}" not in loop:
            fail(f"loop_missing_section:{section}")
    if evidence.get("next_round") != "GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001":
        fail("next_round_mismatch")
    if report.get("next_round") != evidence.get("next_round"):
        fail("runner_next_round_mismatch")

    print(
        "agent_reach_p3_quality_replay_harness=pass "
        "status=quality_replay_harness_ready "
        "current_admission=limited_candidate_only "
        "mode=offline_replay_only "
        f"query_count={report['query_count']} candidate_count={report['candidate_count']} "
        f"average_score={report['average_score']} precision_at_1={report['precision_at_1']} "
        "live_external_search_invoked=false "
        "agent_reach_binary_invoked=false "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
