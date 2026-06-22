#!/usr/bin/env python3
"""Validate Agent-Reach P8 full live-search pipeline readiness."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_pipeline.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-full-live-search-pipeline-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-full-live-search-pipeline-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_full_live_search_pipeline=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_pipeline():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_pipeline", PIPELINE)
    if spec is None or spec.loader is None:
        fail("pipeline_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    pipeline = load_pipeline()
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)
    report = pipeline.build_pipeline_report(execute=False, write_evidence=False, output_json=pipeline.DEFAULT_OUTPUT_JSON, output_md=pipeline.DEFAULT_OUTPUT_MD)
    if report.get("status") != "blocked_pending_batch_authorization":
        fail("default_without_batch_authorization_not_blocked")
    preflight = report.get("quality_preflight", {})
    if preflight.get("query_quality_status") != "p8_query_quality_preflight_pass":
        fail("query_quality_preflight_not_passed")
    if preflight.get("query_quality_failing_count") != 0:
        fail("query_quality_failing_count_not_zero")
    if preflight.get("output_quality_gate_status") != "full_project_group_live_coverage_output_quality_gate_ready":
        fail("output_quality_gate_preflight_not_ready")
    if preflight.get("output_quality_gate_reasons") != []:
        fail("output_quality_gate_reasons_not_empty")
    if report.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("default_invoked_live_search")
    if sorted(report.get("missing_authorization_batches", [])) != ["p8-batch-1", "p8-batch-2", "p8-batch-3"]:
        fail("missing_authorization_batches_mismatch")

    if evidence.get("status") != "p8_full_live_search_pipeline_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("pipeline_checks", {})
    for field in [
        "pipeline_created",
        "blocks_without_three_batch_authorizations",
        "runs_three_batches_when_execute_enabled",
        "merges_batch_outputs",
        "requires_query_quality_preflight",
        "requires_output_quality_gate_preflight",
        "runs_full_output_quality_gate",
        "does_not_execute_live_search_in_preflight",
    ]:
        if checks.get(field) is not True:
            fail(f"pipeline_check_not_true:{field}")
    for marker in [
        "p8_full_live_search_pipeline_ready",
        "blocked_pending_batch_authorization",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")
    print(
        "agent_reach_p8_full_live_search_pipeline=pass "
        "status=p8_full_live_search_pipeline_ready "
        "default_without_authorization=blocked "
        "live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
