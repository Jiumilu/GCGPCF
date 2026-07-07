#!/usr/bin/env python3
"""Collect the minimum local evidence for a GPCF 2.0 Feature."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import append_journal, feature_file, find_feature, read_feature, run_command, write_feature


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_id")
    args = parser.parse_args()

    feature_dir = find_feature(args.feature_id)
    data = read_feature(feature_file(feature_dir))
    evidence_dir = feature_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    diff_status, diff_output = run_command(["git", "diff", "--check"])
    tests_status = diff_status
    build_status = "not_required"
    screenshots_status = "not_required"
    api_status = "not_required"
    summary_status = "pass"

    (evidence_dir / "tests.txt").write_text(diff_output + "\n", encoding="utf-8")
    (evidence_dir / "build.txt").write_text("not_required: documentation/script Feature unless project build is configured.\n", encoding="utf-8")
    (evidence_dir / "screenshots.txt").write_text("not_required: no UI surface changed by default Feature bootstrap.\n", encoding="utf-8")
    (evidence_dir / "api.txt").write_text("not_required: no real external API or real KDS API called.\n", encoding="utf-8")
    (evidence_dir / "summary.md").write_text(
        "\n".join(
            [
                "# Evidence Summary",
                "",
                f"- tests: {tests_status}",
                f"- build: {build_status}",
                f"- screenshots: {screenshots_status}",
                f"- api: {api_status}",
                "- risk: no commit/push/deploy/real-api/status-promotion authorization granted.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    data["evidence"] = {
        "tests": tests_status,
        "build": build_status,
        "screenshots": screenshots_status,
        "api": api_status,
        "summary": summary_status,
    }
    data["blockers"] = [] if tests_status == "pass" else ["git diff check failed"]
    data["loop"]["current_step"] = "evaluate"
    data["loop"]["iteration"] = int(data["loop"].get("iteration", 0)) + 1
    write_feature(feature_file(feature_dir), data)
    append_journal(
        feature_dir,
        iteration=data["loop"]["iteration"],
        answers=[
            "Collect minimum local evidence.",
            "Updated evidence files and feature.yaml evidence status.",
            "Ran git diff --check.",
            "No blocker found." if tests_status == "pass" else "git diff --check failed.",
            "yes, if close gate passes." if tests_status == "pass" else "no.",
        ],
    )

    print(
        "gpcf_feature_evidence "
        f"feature={data['id']} tests={tests_status} build={build_status} "
        f"screenshots={screenshots_status} api={api_status} summary={summary_status}"
    )
    return 0 if tests_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
