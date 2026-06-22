#!/usr/bin/env python3
"""Merge Agent-Reach P8 batch evidence into one full-coverage report."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json"
OUTPUT_VALIDATOR = ROOT / "tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_output.py"
DEFAULT_OUTPUT_JSON = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.json"
DEFAULT_OUTPUT_MD = ROOT / "docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def default_batch_paths() -> list[Path]:
    return [
        ROOT / "docs/harness/evidence/agent-reach-p8-full-live-search-batch-1-20260622.json",
        ROOT / "docs/harness/evidence/agent-reach-p8-full-live-search-batch-2-20260622.json",
        ROOT / "docs/harness/evidence/agent-reach-p8-full-live-search-batch-3-20260622.json",
    ]


def load_output_validator():
    spec = importlib.util.spec_from_file_location("agent_reach_p8_output_validator", OUTPUT_VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("output_validator_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_markdown(report: dict[str, Any]) -> str:
    quality = report.get("quality_report", {})
    controls = report.get("security_controls", {})
    return "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-AGENT-REACH-PROJECT-GROUP-FULL-LIVE-COVERAGE-20260622",
            "title: Agent-Reach 项目群全量真实搜索覆盖证据 2026-06-22",
            "project: KDS",
            "related_projects: [GPCF, KDS, WAES, Brain, GFIS, GPC, PVAOS, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md",
            "source_path: docs/harness/evidence/agent-reach-project-group-full-live-coverage-20260622.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-22",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Agent-Reach 项目群全量真实搜索覆盖证据 2026-06-22",
            "",
            f"- status: `{report.get('status')}`",
            f"- execution_requested: `{report.get('execution_requested')}`",
            f"- live_external_search_invoked: `{controls.get('live_external_search_invoked', False)}`",
            f"- candidate_count: `{quality.get('candidate_count', 0)}`",
            f"- project_coverage: `{quality.get('project_coverage', 0)}`",
            f"- query_candidate_coverage: `{quality.get('query_candidate_coverage', 0)}`",
            f"- channel_candidate_coverage: `{quality.get('channel_candidate_coverage', 0)}`",
            f"- duplicate_url_count: `{quality.get('duplicate_url_count', 0)}`",
            f"- query_error_count: `{quality.get('query_error_count', 0)}`",
            f"- threshold_pass: `{quality.get('threshold_pass', False)}`",
            "",
            "## 非声明",
            "",
            "- This evidence is candidate-only.",
            "- This evidence does not claim accepted, integrated, or production_ready status.",
            "- Raw provider payloads are not persisted.",
            "",
        ]
    )


def merge_reports(batch_paths: list[Path]) -> dict[str, Any]:
    plan = load_json(PLAN)
    missing = [display_path(path) for path in batch_paths if not path.exists()]
    if missing:
        return {
            "id": "agent-reach-project-group-full-live-coverage-runtime",
            "round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-001",
            "status": "blocked_pending_batch_evidence",
            "current_admission": "limited_candidate_only",
            "execution_requested": False,
            "batch_paths": [display_path(path) for path in batch_paths],
            "missing_batch_evidence": missing,
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
            "candidates": [],
            "query_errors": [],
            "quality_report": {"threshold_pass": False},
        }
    batches = [load_json(path) for path in batch_paths]
    incomplete = [batch.get("batch_id", "unknown") for batch in batches if batch.get("status") != "p8_live_search_batch_completed"]
    query_errors = [error for batch in batches for error in batch.get("query_errors", [])]
    candidates = [candidate for batch in batches for candidate in batch.get("candidates", [])]
    controls = {
        "live_external_search_invoked": all(batch.get("security_controls", {}).get("live_external_search_invoked") is True for batch in batches),
        "credential_written": any(batch.get("security_controls", {}).get("credential_written") is True for batch in batches),
        "browser_cookie_extraction_invoked": any(batch.get("security_controls", {}).get("browser_cookie_extraction_invoked") is True for batch in batches),
        "kds_canonical_write_allowed": any(batch.get("security_controls", {}).get("kds_canonical_write_allowed") is True for batch in batches),
        "gfis_source_of_record_write_allowed": any(batch.get("security_controls", {}).get("gfis_source_of_record_write_allowed") is True for batch in batches),
        "production_config_write_allowed": any(batch.get("security_controls", {}).get("production_config_write_allowed") is True for batch in batches),
        "global_mcp_config_write_allowed": any(batch.get("security_controls", {}).get("global_mcp_config_write_allowed") is True for batch in batches),
        "production_integration_allowed": any(batch.get("security_controls", {}).get("production_integration_allowed") is True for batch in batches),
    }
    validator = load_output_validator()
    quality = validator.compute_quality(plan, candidates, query_errors)
    requirements = plan.get("quality_requirements", {})
    quality["threshold_pass"] = (
        not incomplete
        and controls["live_external_search_invoked"] is True
        and controls["credential_written"] is False
        and controls["browser_cookie_extraction_invoked"] is False
        and controls["kds_canonical_write_allowed"] is False
        and controls["gfis_source_of_record_write_allowed"] is False
        and controls["production_config_write_allowed"] is False
        and controls["global_mcp_config_write_allowed"] is False
        and controls["production_integration_allowed"] is False
        and quality["project_coverage"] == 1.0
        and quality["query_candidate_coverage"] == 1.0
        and quality["channel_candidate_coverage"] == 1.0
        and quality["duplicate_url_count"] == 0
        and quality["query_error_count"] == 0
        and quality["required_field_coverage"] == 1.0
        and quality["average_overall_score"] >= requirements.get("minimum_average_overall_score", 0)
        and quality["minimum_candidate_overall_score"] >= requirements.get("minimum_candidate_overall_score", 0)
        and quality["minimum_traceability_score"] >= requirements.get("minimum_traceability_score", 0)
        and quality["credential_leak_count"] == 0
        and quality["forbidden_claim_count"] == 0
    )
    return {
        "id": "agent-reach-project-group-full-live-coverage-runtime",
        "round": "GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-001",
        "status": "full_project_group_live_coverage_completed" if quality["threshold_pass"] else "full_project_group_live_coverage_rework_required",
        "current_admission": "limited_candidate_only",
        "execution_requested": True,
        "batch_paths": [display_path(path) for path in batch_paths],
        "incomplete_batches": incomplete,
        "security_controls": controls,
        "candidates": candidates,
        "query_errors": query_errors,
        "quality_report": quality,
    }


def write_evidence(report: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-json", action="append", type=Path, dest="batch_json")
    parser.add_argument("--write-evidence", action="store_true")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()
    batch_paths = args.batch_json or default_batch_paths()
    report = merge_reports(batch_paths)
    if args.write_evidence:
        write_evidence(report, args.output_json, args.output_md)
        report = {**report, "written_evidence": {"json": display_path(args.output_json), "markdown": display_path(args.output_md)}}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
