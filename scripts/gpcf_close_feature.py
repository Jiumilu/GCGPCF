#!/usr/bin/env python3
"""Close a GPCF 2.0 Feature when its Evidence Gate passes."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import ACTIVE, append_journal, evidence_complete, feature_file, find_feature, move_feature_to_done, read_feature, update_queue_entry, write_feature


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_id")
    args = parser.parse_args()

    feature_dir = find_feature(args.feature_id)
    if feature_dir.parent != ACTIVE:
        raise SystemExit(f"FAIL: feature is not active: {feature_dir}")
    data = read_feature(feature_file(feature_dir))
    if not evidence_complete(data):
        pending = ", ".join(f"{key}={value}" for key, value in data["evidence"].items())
        raise SystemExit(f"FAIL: evidence gate not complete: {pending}")

    data["status"] = "done"
    data["loop"]["current_step"] = "commit"
    data["loop"]["iteration"] = int(data["loop"].get("iteration", 0)) + 1
    write_feature(feature_file(feature_dir), data)
    append_journal(
        feature_dir,
        iteration=data["loop"]["iteration"],
        answers=[
            "Close Feature through Evidence Gate.",
            "Marked feature.yaml status as done.",
            "Verified all evidence fields are pass or waived.",
            "No close blocker found.",
            "yes, as submit candidate only; commit/push still require explicit authorization.",
        ],
    )
    target = move_feature_to_done(feature_dir)
    update_queue_entry(data["id"], status="closed", role="Recorder")
    print(f"feature_closed={data['id']} path={target.relative_to(ACTIVE.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
