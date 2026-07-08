#!/usr/bin/env python3
"""Close a GPCF 2.0 Feature when its Evidence Gate passes."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import ACTIVE, append_journal, append_runtime_log, evidence_complete, feature_file, find_feature, move_feature_to_done, read_feature, update_queue_entry, write_feature


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
            "通过 Evidence Gate 关闭 Feature。",
            "将 feature.yaml 状态标记为 done。",
            "验证所有 evidence 字段均为 pass 或 waived。",
            "未发现关闭阻塞项。",
            "是，仅作为提交候选；commit/push 仍需明确授权。",
        ],
    )
    target = move_feature_to_done(feature_dir)
    target_rel = target.relative_to(ACTIVE.parents[1]).as_posix()
    update_queue_entry(data["id"], status="closed", role="Recorder", workspace=target_rel)
    append_runtime_log(
        data["id"],
        role="Recorder",
        status="closed",
        input_summary="Evidence Gate 已通过。",
        output_summary=f"Feature 已移动到 {target_rel}。",
        evidence="feature.yaml status=done；queue status=closed。",
    )
    print(f"feature_closed={data['id']} path={target_rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
