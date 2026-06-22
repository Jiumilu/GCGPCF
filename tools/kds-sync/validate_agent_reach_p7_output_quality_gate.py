#!/usr/bin/env python3
"""Validate Agent-Reach P7 output-quality gate artifacts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_VALIDATOR = ROOT / "tools/kds-sync/validate_agent_reach_p7_limited_live_search_output.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p7-output-quality-gate-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p7_output_quality_gate=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def main() -> None:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    proc = subprocess.run(
        ["python3", str(OUTPUT_VALIDATOR), "--self-test"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
        timeout=20,
    )
    if proc.returncode != 0:
        fail("output_validator_self_test_failed")
    if "agent_reach_p7_limited_live_search_output=pass" not in proc.stdout:
        fail("output_validator_self_test_marker_missing")
    for case in ["missing-query", "query-error", "raw-payload", "duplicate-url", "missing-channel"]:
        negative_proc = subprocess.run(
            ["python3", str(OUTPUT_VALIDATOR), "--negative-test", case],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=20,
        )
        if negative_proc.returncode != 0:
            fail(f"output_validator_negative_test_failed:{case}")
        if f"agent_reach_p7_limited_live_search_output_negative=pass case={case}" not in negative_proc.stdout:
            fail(f"output_validator_negative_test_marker_missing:{case}")

    if evidence.get("status") != "limited_live_search_output_quality_gate_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("validator_checks", {})
    for field in [
        "requires_completed_status",
        "requires_valid_authorization",
        "requires_execution_requested",
        "requires_live_external_search_invoked",
        "requires_candidate_schema",
        "requires_full_query_candidate_coverage",
        "requires_full_channel_candidate_coverage",
        "requires_zero_query_errors",
        "requires_zero_duplicate_urls",
        "enforces_query_and_result_scope",
        "enforces_allowed_channels",
        "enforces_quality_thresholds",
        "enforces_non_claims",
        "blocks_raw_provider_payload_persistence",
        "blocks_credential_leak",
        "self_test_passed_without_network",
        "negative_missing_query_test_passed",
        "negative_query_error_test_passed",
        "negative_raw_payload_test_passed",
        "negative_duplicate_url_test_passed",
        "negative_missing_channel_test_passed",
    ]:
        if checks.get(field) is not True:
            fail(f"validator_check_not_true:{field}")
    controls = evidence.get("security_controls", {})
    for field in [
        "live_external_search_invoked",
        "agent_reach_binary_invoked",
        "credential_written",
        "browser_cookie_extraction_invoked",
        "kds_canonical_write_allowed",
        "gfis_source_of_record_write_allowed",
        "production_config_write_allowed",
        "global_mcp_config_write_allowed",
        "production_integration_allowed",
    ]:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    for marker in [
        "limited_live_search_output_quality_gate_ready",
        "validate_agent_reach_p7_limited_live_search_output.py --self-test",
        "query_candidate_coverage",
        "channel_candidate_coverage",
        "query_error_count",
        "duplicate_url_count",
        "不声明真实搜索已调用",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p7_output_quality_gate=pass "
        "status=limited_live_search_output_quality_gate_ready "
        "self_test=pass "
        f"next={evidence['next_round']}"
    )


if __name__ == "__main__":
    main()
