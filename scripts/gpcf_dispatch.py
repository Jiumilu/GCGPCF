#!/usr/bin/env python3
"""Advance the GPCF 2.0 runtime queue as a lightweight role state machine."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import (
    ACTIVE,
    ROLE_BY_STEP,
    ROLES,
    STEP_BY_ROLE,
    append_journal,
    append_runtime_log,
    evidence_complete,
    feature_file,
    find_feature,
    queue_entries,
    read_feature,
    update_queue_entry,
    write_feature,
)


NEXT_ROLE = {
    "Dispatcher": "Planner",
    "Planner": "Builder",
    "Builder": "Evaluator",
    "Evaluator": "Recorder",
    "Repair": "Builder",
    "Recorder": "Recorder",
}


def select_feature(feature_id: str | None) -> str:
    entries = queue_entries()
    if feature_id:
        if not any(entry.get("id") == feature_id for entry in entries):
            raise SystemExit(f"FAIL: feature not in runtime queue: {feature_id}")
        return feature_id
    for entry in entries:
        if entry.get("status") not in {"closed", "archived"}:
            return str(entry["id"])
    raise SystemExit("FAIL: no dispatchable feature in runtime queue")


def queue_entry(feature_id: str) -> dict[str, object]:
    for entry in queue_entries():
        if entry.get("id") == feature_id:
            return entry
    raise SystemExit(f"FAIL: feature not in runtime queue: {feature_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_id", nargs="?")
    parser.add_argument("--role", choices=ROLES)
    parser.add_argument("--input", default="运行 Feature Runtime 调度。")
    parser.add_argument("--evidence", default="runtime/queue.json 与 runtime/state.json。")
    args = parser.parse_args()

    feature_id = select_feature(args.feature_id)
    entry = queue_entry(feature_id)
    current_role = args.role or str(entry.get("current_role", "Dispatcher"))
    if current_role not in ROLES:
        raise SystemExit(f"FAIL: unsupported role in queue: {current_role}")

    feature_dir = find_feature(feature_id)
    data = read_feature(feature_file(feature_dir))
    if feature_dir.parent != ACTIVE:
        next_role = "Recorder"
        next_status = "closed" if str(data.get("status")) == "done" else str(data.get("status"))
    elif current_role == "Evaluator" and not evidence_complete(data):
        next_role = "Repair"
        next_status = "repair"
        data["blockers"] = data.get("blockers") or ["Evidence Gate 未通过"]
    else:
        next_role = NEXT_ROLE[current_role]
        next_status = STEP_BY_ROLE[next_role]

    data["loop"]["current_step"] = next_status if next_status in ROLE_BY_STEP else "commit"
    data["loop"]["iteration"] = int(data["loop"].get("iteration", 0)) + 1
    write_feature(feature_file(feature_dir), data)
    update_queue_entry(feature_id, status=next_status, role=next_role)

    output = f"{current_role} -> {next_role}；status={next_status}"
    append_runtime_log(
        feature_id,
        role=current_role,
        status=next_status,
        input_summary=args.input,
        output_summary=output,
        evidence=args.evidence,
    )
    append_journal(
        feature_dir,
        iteration=data["loop"]["iteration"],
        answers=[
            f"{current_role} 执行 runtime 调度。",
            output,
            args.evidence,
            "未发现调度阻塞项。" if next_role != "Repair" else "Evidence Gate 未通过，进入 Repair。",
            "否，commit/push 仍需明确授权。",
        ],
    )
    print(f"gpcf_dispatch feature={feature_id} role={current_role} next_role={next_role} status={next_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
