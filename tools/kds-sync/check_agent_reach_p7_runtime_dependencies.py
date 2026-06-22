#!/usr/bin/env python3
"""Check local runtime dependencies for Agent-Reach P7 live-search dry-run."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/kds-sync/run_agent_reach_limited_live_search_dry_run.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("agent_reach_p7_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("runner_import_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_dependency_report() -> dict[str, Any]:
    runner = load_runner_module()
    plan = runner.load_json(runner.PLAN_PATH)
    execution_plan = runner.build_execution_plan(plan)
    checks = []
    missing: list[str] = []
    for item in execution_plan:
        command = item.get("planned_command", [])
        binary = command[0] if command else ""
        path = shutil.which(binary) if binary else None
        checks.append(
            {
                "query_id": item["query_id"],
                "project": item["project"],
                "channel": item["channel"],
                "backend": item["backend"],
                "binary": binary,
                "available": bool(path),
                "path": path,
            }
        )
        if binary and not path:
            missing.append(binary)
    unique_missing = sorted(set(missing))
    return {
        "id": "agent-reach-p7-runtime-dependency-precheck",
        "round": "GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-PRECHECK-001",
        "status": "runtime_dependencies_ready" if not unique_missing else "runtime_dependency_rework_required",
        "current_admission": "limited_candidate_only",
        "live_external_search_invoked": False,
        "agent_reach_binary_invoked": False,
        "checked_queries": len(execution_plan),
        "dependency_checks": checks,
        "missing_binaries": unique_missing,
        "next_round": "GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001" if not unique_missing else "GPCF-AGENT-REACH-P7-RUNTIME-DEPENDENCY-REPAIR-001",
        "non_claims": [
            "not_live_search_invoked",
            "not_live_search_quality_accepted",
            "not_kds_canonical_written",
            "not_gfis_source_of_record_written",
            "not_production_integrated",
            "not_accepted",
            "not_integrated",
            "not_production_ready",
        ],
    }


def main() -> None:
    report = build_dependency_report()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
