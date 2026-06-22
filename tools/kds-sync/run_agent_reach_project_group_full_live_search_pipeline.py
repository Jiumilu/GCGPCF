#!/usr/bin/env python3
"""Run the full Agent-Reach P8 project-group search pipeline behind batch gates."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BATCH_RUNNER = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_batch.py"
MERGER = ROOT / "tools/kds-sync/merge_agent_reach_project_group_full_live_search_batches.py"
OUTPUT_VALIDATOR = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
QUERY_PREFLIGHT = ROOT / "tools/kds-sync/validate_agent_reach_p8_query_quality_preflight.py"
DEFAULT_OUTPUT_JSON = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.json"
DEFAULT_OUTPUT_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md"
BATCH_IDS = ["p8-batch-1", "p8-batch-2", "p8-batch-3"]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"import_failed:{name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def auth_path_for(batch_runner, batch_id: str, authorization_dir: Path | None) -> Path:
    default_path = batch_runner.default_auth_path(batch_id)
    if authorization_dir is None:
        return default_path
    return authorization_dir / default_path.name


def build_pipeline_report(
    execute: bool,
    write_evidence: bool,
    output_json: Path,
    output_md: Path,
    authorization_dir: Path | None = None,
) -> dict[str, Any]:
    batch_runner = load_module(BATCH_RUNNER, "agent_reach_p8_batch_runner")
    merger = load_module(MERGER, "agent_reach_p8_merger")
    output_validator = load_module(OUTPUT_VALIDATOR, "agent_reach_p8_output_validator")
    query_preflight = load_module(QUERY_PREFLIGHT, "agent_reach_p8_query_quality_preflight")

    query_preflight_report = query_preflight.build_report()
    try:
        output_validator.validate_gate_evidence()
        output_gate_status = "full_project_group_live_coverage_output_quality_gate_ready"
        output_gate_reasons: list[str] = []
    except SystemExit as exc:
        output_gate_status = "full_project_group_live_coverage_output_quality_gate_rework_required"
        output_gate_reasons = [str(exc)]

    preflight_reports = {
        batch_id: batch_runner.build_report(batch_id, auth_path_for(batch_runner, batch_id, authorization_dir), execute=False)
        for batch_id in BATCH_IDS
    }
    missing_authorization = [
        batch_id
        for batch_id, report in preflight_reports.items()
        if report.get("status") == "blocked_pending_execution_authorization"
    ]
    base = {
        "id": "agent-reach-project-group-full-live-search-pipeline",
        "round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-PIPELINE-001",
        "current_admission": "limited_candidate_only",
        "execution_requested": execute,
        "write_evidence_requested": write_evidence,
        "batch_ids": BATCH_IDS,
        "quality_preflight": {
            "query_quality_status": query_preflight_report.get("status"),
            "query_quality_failing_count": query_preflight_report.get("failing_query_count"),
            "output_quality_gate_status": output_gate_status,
            "output_quality_gate_reasons": output_gate_reasons,
        },
        "preflight_status": {batch_id: report.get("status") for batch_id, report in preflight_reports.items()},
        "security_controls": {
            "live_external_search_invoked": False,
            "credential_written": False,
            "browser_cookie_extraction_invoked": False,
            "kds_canonical_write_allowed": False,
            "gfis_source_of_record_write_allowed": False,
            "production_config_write_allowed": False,
            "global_mcp_config_write_allowed": False,
            "production_integration_allowed": False,
        },
    }
    if query_preflight_report.get("status") != "p8_query_quality_preflight_pass" or output_gate_reasons:
        return {
            **base,
            "status": "blocked_quality_preflight_rework_required",
            "batch_reports": preflight_reports,
        }
    if missing_authorization:
        return {
            **base,
            "status": "blocked_pending_batch_authorization",
            "missing_authorization_batches": missing_authorization,
            "batch_reports": preflight_reports,
            "next_required_authorizations": [
                f"授权执行 Agent-Reach P8 Project Group Full Live Search Batch {idx}"
                for idx, batch_id in enumerate(BATCH_IDS, 1)
                if batch_id in missing_authorization
            ],
        }
    if not execute:
        return {
            **base,
            "status": "authorized_execution_not_requested",
            "batch_reports": preflight_reports,
        }

    batch_reports: dict[str, dict[str, Any]] = {}
    batch_paths: list[Path] = []
    for batch_id in BATCH_IDS:
        auth_path = auth_path_for(batch_runner, batch_id, authorization_dir)
        batch_report = batch_runner.build_report(batch_id, auth_path, execute=True)
        batch_json = batch_runner.default_output_json(batch_id)
        batch_md = batch_runner.default_output_md(batch_id)
        batch_paths.append(batch_json)
        if write_evidence:
            batch_runner.write_evidence(batch_report, batch_json, batch_md)
        batch_reports[batch_id] = batch_report
    if not write_evidence:
        return {
            **base,
            "status": "execution_completed_evidence_not_written",
            "batch_reports": batch_reports,
        }
    merged = merger.merge_reports(batch_paths)
    merger.write_evidence(merged, output_json, output_md)
    full_markdown = output_md.read_text(encoding="utf-8")
    full_plan = output_validator.load_json(output_validator.PLAN)
    if merged.get("status") == "full_project_group_live_coverage_completed":
        output_validator.validate_report(merged, full_markdown, full_plan)
    return {
        **base,
        "status": "full_project_group_live_search_pipeline_completed"
        if merged.get("status") == "full_project_group_live_coverage_completed"
        else "full_project_group_live_search_pipeline_rework_required",
        "batch_reports": batch_reports,
        "merged_report": merged,
        "written_evidence": {
            "json": display_path(output_json),
            "markdown": display_path(output_md),
        },
        "security_controls": merged.get("security_controls", base["security_controls"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--authorization-dir", type=Path)
    parser.add_argument("--pipeline-report", type=Path)
    args = parser.parse_args()
    report = build_pipeline_report(
        args.execute,
        args.write_evidence,
        args.output_json,
        args.output_md,
        authorization_dir=args.authorization_dir,
    )
    if args.pipeline_report:
        write_json(args.pipeline_report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
