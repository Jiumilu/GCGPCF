#!/usr/bin/env python3
"""Validate Agent-Reach P8 batch runtime runner readiness."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py"
AUTH_REQUEST = ROOT / "fixtures/agent-reach/project-group-full-live-search-batch-authorization.request.json"
OUTPUT_GATE = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-output-quality-gate-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-batch-runtime-runner-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-batch-runtime-runner-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-RUNTIME-RUNNER-001.md"

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
    raise SystemExit(f"agent_reach_p8_batch_runtime_runner=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_runner():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_batch_runner", RUNNER)
    if spec is None or spec.loader is None:
        fail("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    runner = load_runner()
    auth_request = load_json(AUTH_REQUEST)
    output_gate = load_json(OUTPUT_GATE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    if auth_request.get("authorization_status") != "pending_human_authorization":
        fail("authorization_request_status_mismatch")
    if output_gate.get("status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("output_gate_not_ready")
    for batch_id in ["p8-batch-1", "p8-batch-2", "p8-batch-3"]:
        report = runner.build_report(batch_id, runner.default_auth_path(batch_id), execute=False)
        if report.get("status") != "blocked_pending_execution_authorization":
            fail(f"default_without_authorization_not_blocked:{batch_id}")
        if "authorization_file_missing" not in report.get("authorization_reasons", []):
            fail(f"missing_authorization_reason_absent:{batch_id}")
        if report.get("security_controls", {}).get("live_external_search_invoked") is not False:
            fail(f"default_invoked_live_search:{batch_id}")

    if evidence.get("status") != "p8_batch_runtime_runner_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("runner_checks", {})
    for field in [
        "runner_created",
        "reuses_public_web_rss_bilibili_backends",
        "blocks_without_batch_authorization",
        "supports_three_batches",
        "supports_write_redacted_evidence_only",
        "output_quality_gate_ready_before_execution",
    ]:
        if checks.get(field) is not True:
            fail(f"runner_check_not_true:{field}")
    controls = evidence.get("security_controls", {})
    for field in SECURITY_FALSE_FIELDS:
        if controls.get(field) is not False:
            fail(f"security_control_not_false:{field}")
    for marker in [
        "p8_batch_runtime_runner_ready",
        "blocked_pending_execution_authorization",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")

    print(
        "agent_reach_p8_batch_runtime_runner=pass "
        "status=p8_batch_runtime_runner_ready "
        "default_without_authorization=blocked "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
