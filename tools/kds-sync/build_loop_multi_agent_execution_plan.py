#!/usr/bin/env python3
"""Build a controlled multi-agent execution plan from a task_interface block."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from parse_loop_task_interface import DEFAULT_TASK, parse_task_file, yaml_dump


AGENT_STAGE_MAP = {
    "contract": "Contract Agent",
    "runtime_intake": "Runtime Intake Agent",
    "primary_key_validation": "Primary Key / Source Validation Agent",
    "review_queue": "Review Queue Agent",
    "waes_artifact": "WAES Candidate / Artifact Agent",
    "boundary_validation": "Boundary Validator Agent",
    "orchestrator_summary": "LOOP Orchestrator",
}


def build_plan(task: dict[str, Any]) -> dict[str, Any]:
    execution = task["execution"]
    file_locks = task["file_locks"]

    serial_required = execution.get("serial_required", [])
    handoff_plan = []
    for index, stage in enumerate(serial_required, start=1):
        handoff_plan.append(
            {
                "order": index,
                "stage": stage,
                "agent": AGENT_STAGE_MAP.get(stage, "LOOP Orchestrator"),
            }
        )

    return {
        "multi_agent_execution_plan": {
            "task_id": task["id"],
            "execution_mode": execution["mode"],
            "default_loop": execution["default_loop"],
            "governance_level": execution["governance_level"],
            "phase_a": execution.get("parallel_allowed", []),
            "phase_b": serial_required,
            "required_agents": task["agents"]["required"],
            "required_tools": task["tools"]["required"],
            "readonly_tools": task["tools"].get("readonly", []),
            "file_lock_plan": {
                "orchestrator_only": file_locks.get("orchestrator_only", []),
                "single_writer_per_file": file_locks.get("single_writer_per_file", False),
            },
            "handoff_plan": handoff_plan,
            "success_criteria_checklist": task.get("success_criteria", []),
            "stop_conditions": task.get("stop_conditions", []),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_file", nargs="?", default=str(DEFAULT_TASK))
    args = parser.parse_args()

    parsed = parse_task_file(Path(args.task_file).resolve())
    if parsed["task_interface_parse_result"]["status"] != "pass":
        sys.stdout.write(yaml_dump(parsed["task_interface_parse_result"]) + "\n")
        return 1

    plan = build_plan(parsed["task_interface"])
    sys.stdout.write(yaml_dump(plan) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
