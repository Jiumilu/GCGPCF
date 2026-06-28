#!/usr/bin/env python3
"""Parse and validate LOOP task_interface blocks from controlled task docs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TASK = ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.md"
REQUIRED_TOP_LEVEL_FIELDS = [
    "id",
    "project",
    "objective",
    "task_type",
    "lifecycle",
    "loop_mode",
    "autonomy_level",
    "risk_gate",
    "inputs",
    "outputs",
    "agents",
    "tools",
    "methods",
    "execution",
    "file_locks",
    "evidence",
    "success_criteria",
    "stop_conditions",
]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL parse_loop_task_interface: {message}")


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_task_interface_block(text: str) -> str:
    for match in re.finditer(r"```yaml\n(?P<body>.*?)```", text, re.S):
        body = match.group("body")
        if "task_interface:" in body:
            return body
    fail("missing fenced yaml task_interface block")


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def next_container(lines: list[str], start: int, parent_indent: int) -> Any:
    for index in range(start, len(lines)):
        stripped = lines[index].strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(lines[index]) - len(lines[index].lstrip(" "))
        if indent <= parent_indent:
            break
        if stripped.startswith("- "):
            return []
        return {}
    return {}


def parse_yaml_subset(block: str) -> dict[str, Any]:
    lines = block.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for index, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()

        container = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(container, list):
                fail(f"list item without list container: {stripped}")
            container.append(parse_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            fail(f"invalid task_interface line: {stripped}")

        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value:
            value = parse_scalar(raw_value)
        else:
            value = next_container(lines, index + 1, indent)

        if not isinstance(container, dict):
            fail(f"mapping entry inside list is not supported: {stripped}")

        container[key] = value
        if isinstance(value, (dict, list)):
            stack.append((indent, value))

    return root


def validate_task_interface(task: dict[str, Any]) -> tuple[list[str], list[str]]:
    missing_fields = [field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in task]
    conflicts: list[str] = []

    tools = task.get("tools", {})
    required_tools = tools.get("required", [])
    readonly_tools = tools.get("readonly", [])
    forbidden_tools = set(tools.get("forbidden", []))

    for tool in required_tools + readonly_tools:
        candidate = ROOT / "tools/kds-sync" / str(tool)
        if tool.endswith(".py") and not candidate.exists():
            missing_fields.append(f"tool:{tool}")

    overlap = forbidden_tools.intersection(required_tools + readonly_tools)
    if overlap:
        conflicts.append(f"forbidden tool overlap: {sorted(overlap)}")

    execution = task.get("execution", {})
    if "mode" not in execution:
        missing_fields.append("execution.mode")
    if "serial_required" not in execution:
        missing_fields.append("execution.serial_required")

    if "required" not in task.get("agents", {}):
        missing_fields.append("agents.required")

    if "explicit_non_claims" not in task.get("evidence", {}):
        missing_fields.append("evidence.explicit_non_claims")

    return missing_fields, conflicts


def yaml_dump(data: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(data, dict):
        lines: list[str] = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(yaml_dump(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {value}")
        return "\n".join(lines)
    if isinstance(data, list):
        lines = []
        for value in data:
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(yaml_dump(value, indent + 2))
            else:
                lines.append(f"{prefix}- {value}")
        return "\n".join(lines)
    return f"{prefix}{data}"


def parse_task_file(path: Path) -> dict[str, Any]:
    block = extract_task_interface_block(read_text(path))
    parsed = parse_yaml_subset(block)
    task = parsed.get("task_interface")
    if not isinstance(task, dict):
        fail("task_interface root is missing or invalid")
    missing_fields, conflicts = validate_task_interface(task)
    return {
        "task_interface_parse_result": {
            "status": "pass" if not missing_fields and not conflicts else "fail",
            "task_id": task.get("id", "unknown"),
            "execution_mode": task.get("execution", {}).get("mode", "unknown"),
            "required_agents": task.get("agents", {}).get("required", []),
            "required_tools": task.get("tools", {}).get("required", []),
            "missing_fields": missing_fields,
            "forbidden_conflicts": conflicts,
        },
        "task_interface": task,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_file", nargs="?", default=str(DEFAULT_TASK))
    args = parser.parse_args()

    result = parse_task_file(Path(args.task_file).resolve())
    sys.stdout.write(yaml_dump(result["task_interface_parse_result"]) + "\n")
    return 0 if result["task_interface_parse_result"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
