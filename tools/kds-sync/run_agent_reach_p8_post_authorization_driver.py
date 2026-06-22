#!/usr/bin/env python3
"""Drive Agent-Reach P8 from authorization text to gated pipeline execution."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
INTAKE = ROOT / "tools/kds-sync/ingest_agent_reach_p8_authorization_text.py"
PIPELINE = ROOT / "tools/kds-sync/run_agent_reach_project_group_full_live_search_pipeline.py"
OUTPUT_GATE = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
REWORK_QUEUE = ROOT / "tools/kds-sync/validate_agent_reach_p8_rework_queue.py"
DEFAULT_PIPELINE_REPORT = ROOT / "docs/harness/evidence/agent-reach-p8-post-authorization-pipeline-report-20260622.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"import_failed:{name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def gate_status(path: Path, module_name: str, function_name: str | None = None) -> dict[str, Any]:
    module = load_module(path, module_name)
    if function_name is None:
        return {"status": "loaded"}
    try:
        getattr(module, function_name)()
        return {"status": "pass", "reasons": []}
    except SystemExit as exc:
        return {"status": "fail", "reasons": [str(exc)]}


def build_report(
    *,
    authorization_text_path: Path,
    write_local_auth: bool,
    execute_live: bool,
    write_evidence: bool,
    authorization_output_dir: Path | None = None,
    pipeline_report_path: Path | None = None,
) -> dict[str, Any]:
    intake = load_module(INTAKE, "agent_reach_p8_authorization_text_intake")
    pipeline = load_module(PIPELINE, "agent_reach_p8_pipeline")
    intake_report = intake.build_report(
        authorization_text_path=authorization_text_path,
        write_local_auth=write_local_auth,
        authorization_output_dir=authorization_output_dir,
    )
    if intake_report.get("status") == "rejected":
        return {
            "id": "agent-reach-p8-post-authorization-driver",
            "status": "rejected_by_authorization_text_intake",
            "current_admission": "limited_candidate_only",
            "authorization_text_path": display_path(authorization_text_path),
            "intake_report": intake_report,
            "pipeline_report": None,
            "security_controls": intake_report["security_controls"],
        }
    if execute_live and not write_evidence:
        return {
            "id": "agent-reach-p8-post-authorization-driver",
            "status": "rejected_execute_requires_write_evidence",
            "current_admission": "limited_candidate_only",
            "authorization_text_path": display_path(authorization_text_path),
            "intake_report": intake_report,
            "pipeline_report": None,
            "security_controls": intake_report["security_controls"],
        }
    pipeline_report = pipeline.build_pipeline_report(
        execute=execute_live,
        write_evidence=write_evidence,
        output_json=pipeline.DEFAULT_OUTPUT_JSON,
        output_md=pipeline.DEFAULT_OUTPUT_MD,
        authorization_dir=authorization_output_dir,
    )
    if pipeline_report_path is not None:
        write_json(pipeline_report_path, pipeline_report)
    output_gate = gate_status(OUTPUT_GATE, "agent_reach_p8_output_gate", "validate_gate_evidence")
    rework_queue = gate_status(REWORK_QUEUE, "agent_reach_p8_rework_queue", "validate_gate_evidence")
    if pipeline_report.get("status") == "full_project_group_live_search_pipeline_completed":
        status = "completed_with_quality_gate_required"
    elif pipeline_report.get("status") == "full_project_group_live_search_pipeline_rework_required":
        status = "completed_with_rework_required"
    else:
        status = pipeline_report.get("status")
    return {
        "id": "agent-reach-p8-post-authorization-driver",
        "status": status,
        "current_admission": "limited_candidate_only",
        "authorization_text_path": display_path(authorization_text_path),
        "write_local_auth_requested": write_local_auth,
        "execute_live_requested": execute_live,
        "write_evidence_requested": write_evidence,
        "authorization_output_dir": display_path(authorization_output_dir)
        if authorization_output_dir is not None
        else "default_fixture_path",
        "pipeline_report_path": display_path(pipeline_report_path)
        if pipeline_report_path is not None
        else None,
        "intake_report": intake_report,
        "pipeline_report": pipeline_report,
        "output_quality_gate_precheck": output_gate,
        "rework_queue_module": rework_queue,
        "security_controls": pipeline_report.get("security_controls", intake_report["security_controls"]),
        "non_claims": [
            "not_accepted",
            "not_integrated",
            "not_production_ready",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization-text-file", type=Path, required=True)
    parser.add_argument("--write-local-auth", action="store_true")
    parser.add_argument("--execute-live", action="store_true")
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--authorization-output-dir", type=Path)
    parser.add_argument("--pipeline-report", type=Path, default=DEFAULT_PIPELINE_REPORT)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = build_report(
        authorization_text_path=args.authorization_text_file,
        write_local_auth=args.write_local_auth,
        execute_live=args.execute_live,
        write_evidence=args.write_evidence,
        authorization_output_dir=args.authorization_output_dir,
        pipeline_report_path=args.pipeline_report,
    )
    if args.report:
        write_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if str(report.get("status", "")).startswith("rejected"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
