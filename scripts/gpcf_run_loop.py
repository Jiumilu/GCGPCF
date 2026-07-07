#!/usr/bin/env python3
"""Advance a GPCF 2.0 Feature execution loop state."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import STEPS, append_journal, feature_file, find_feature, read_feature, update_queue_entry, write_feature


ROLE_BY_STEP = {
    "plan": "Planner",
    "implement": "Builder",
    "evaluate": "Evaluator",
    "repair": "Repair",
    "commit": "Recorder",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_id")
    parser.add_argument("--step", choices=STEPS)
    parser.add_argument("--plan", default="Advance Feature delivery loop.")
    parser.add_argument("--changed", default="Updated Feature loop state only.")
    parser.add_argument("--verified", default="Manual loop-state update; run evidence gate before close.")
    parser.add_argument("--problem", default="none")
    parser.add_argument("--commit", default="no, commit/push require explicit authorization.")
    args = parser.parse_args()

    feature_dir = find_feature(args.feature_id)
    data = read_feature(feature_file(feature_dir))
    current = str(data["loop"].get("current_step", "plan"))
    next_step = args.step or STEPS[(STEPS.index(current) + 1) % len(STEPS)]
    data["loop"]["current_step"] = next_step
    data["loop"]["iteration"] = int(data["loop"].get("iteration", 0)) + 1
    write_feature(feature_file(feature_dir), data)
    update_queue_entry(data["id"], status=next_step, role=ROLE_BY_STEP[next_step])
    append_journal(
        feature_dir,
        iteration=data["loop"]["iteration"],
        answers=[args.plan, args.changed, args.verified, args.problem, args.commit],
    )
    print(f"feature_loop_updated={data['id']} step={next_step} iteration={data['loop']['iteration']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
