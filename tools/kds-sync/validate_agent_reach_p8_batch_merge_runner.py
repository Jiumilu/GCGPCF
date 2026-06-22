#!/usr/bin/env python3
"""Validate Agent-Reach P8 batch merge runner readiness."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MERGER = ROOT / "tools/kds-sync/merge_agent_reach_project_group_full_live_search_batches.py"
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
OUTPUT_VALIDATOR = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/agent-reach-p8-batch-merge-runner-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/agent-reach-p8-batch-merge-runner-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001.md"


def fail(message: str) -> None:
    raise SystemExit(f"agent_reach_p8_batch_merge_runner=fail reason={message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"import_failed:{name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def self_test_batches(validator) -> list[dict[str, Any]]:
    plan = load_json(PLAN)
    full_report, _ = validator.build_self_test_report(plan)
    by_batch: dict[str, list[dict[str, Any]]] = {}
    for candidate in full_report["candidates"]:
        query_id = candidate["query_id"]
        batch_id = "p8-batch-1" if query_id <= "p8-q05" else "p8-batch-2" if query_id <= "p8-q10" else "p8-batch-3"
        by_batch.setdefault(batch_id, []).append(candidate)
    reports = []
    for batch_id in ["p8-batch-1", "p8-batch-2", "p8-batch-3"]:
        reports.append(
            {
                "id": "agent-reach-p8-project-group-full-live-search-batch-runtime",
                "batch_id": batch_id,
                "status": "p8_live_search_batch_completed",
                "current_admission": "limited_candidate_only",
                "execution_requested": True,
                "security_controls": {
                    "live_external_search_invoked": True,
                    "credential_written": False,
                    "browser_cookie_extraction_invoked": False,
                    "kds_canonical_write_allowed": False,
                    "gfis_source_of_record_write_allowed": False,
                    "production_config_write_allowed": False,
                    "global_mcp_config_write_allowed": False,
                    "production_integration_allowed": False,
                },
                "candidates": by_batch[batch_id],
                "query_errors": [],
            }
        )
    return reports


def main() -> None:
    merger = load_module(MERGER, "agent_reach_p8_merger")
    validator = load_module(OUTPUT_VALIDATOR, "agent_reach_p8_output_validator")
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read_text(EVIDENCE_MD)
    loop_md = read_text(LOOP_MD)

    blocked = merger.merge_reports(merger.default_batch_paths())
    if blocked.get("status") != "blocked_pending_batch_evidence":
        fail("default_without_batch_evidence_not_blocked")
    if blocked.get("security_controls", {}).get("live_external_search_invoked") is not False:
        fail("default_blocked_invoked_live_search")

    with tempfile.TemporaryDirectory() as tmpdir:
        paths = []
        for idx, report in enumerate(self_test_batches(validator), 1):
            path = Path(tmpdir) / f"batch-{idx}.json"
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            paths.append(path)
        merged = merger.merge_reports(paths)
        markdown = merger.render_markdown(merged)
        validator.validate_report(merged, markdown, load_json(PLAN))

    if evidence.get("status") != "p8_batch_merge_runner_ready":
        fail("evidence_status_mismatch")
    checks = evidence.get("merge_checks", {})
    for field in [
        "merge_runner_created",
        "blocks_when_batch_evidence_missing",
        "merges_three_batch_outputs",
        "merged_output_passes_full_quality_validator",
        "does_not_execute_live_search",
    ]:
        if checks.get(field) is not True:
            fail(f"merge_check_not_true:{field}")
    for marker in [
        "p8_batch_merge_runner_ready",
        "blocked_pending_batch_evidence",
        "不执行真实搜索",
        "不声明 accepted / integrated / production_ready",
    ]:
        if marker not in evidence_md:
            fail(f"evidence_md_missing:{marker}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_md:
            fail(f"loop_missing_section:{section}")
    print(
        "agent_reach_p8_batch_merge_runner=pass "
        "status=p8_batch_merge_runner_ready "
        "default_without_batch_evidence=blocked "
        "self_test=pass live_external_search_invoked=false "
        "next=GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001"
    )


if __name__ == "__main__":
    main()
