#!/usr/bin/env python3
"""Validate Headroom L2 project-group dry-run evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-L2-PROJECT-GROUP-DRY-RUN-001.md"
SOURCE_FIXTURE = ROOT / "fixtures/headroom/headroom-l2-project-group-sources.json"
GENERATOR = ROOT / "tools/kds-sync/generate_headroom_l2_project_group_dry_run.py"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    fixture = load_json(SOURCE_FIXTURE)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    generator = read(GENERATOR)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("structured_surrogate" in generator, "generator must declare structured surrogate mode")

    require(evidence.get("evidence_id") == "HEADROOM-L2-PROJECT-GROUP-DRY-RUN-20260621", "invalid evidence id")
    require(evidence.get("status") == "l2_structured_surrogate_dry_run_measured", "invalid status")
    require(evidence.get("compressor_mode") == "structured_surrogate_no_headroom_runtime", "unexpected compressor mode")
    require(evidence.get("headroom_runtime_used") is False, "must not claim real headroom runtime use")
    require(evidence.get("telemetry") == "off", "telemetry must remain off")
    require(evidence.get("sensitive_raw_text_stored") is False, "must not store sensitive raw text")
    require(evidence.get("measured_project_group_sample_tokens") is True, "sample token measurement must be true")
    require(evidence.get("measured_production_tokens") is False, "must not claim production token measurement")
    require(evidence.get("projects_covered") == PROJECTS, "project coverage mismatch")
    require(evidence.get("project_count") == len(PROJECTS), "project count mismatch")
    require(fixture.get("compressor_mode") == evidence.get("compressor_mode"), "fixture compressor mode mismatch")

    aggregate = evidence.get("aggregate", {})
    require(aggregate.get("saving_rate", 0) >= evidence.get("minimum_saving_rate"), "aggregate saving rate below threshold")
    require(aggregate.get("all_admission_gates_pass") is True, "not all admission gates pass")
    require(aggregate.get("input_tokens_before", 0) > aggregate.get("input_tokens_after", 0), "aggregate tokens did not decrease")
    for key in [
        "input_tokens_before",
        "input_tokens_after",
        "baseline_cost",
        "headroom_cost",
        "gross_saving",
        "saving_rate",
    ]:
        require(f"| {key} | {aggregate.get(key)} |" in evidence_md, f"evidence md aggregate mismatch: {key}")

    measurements = evidence.get("measurements", [])
    require(len(measurements) == len(PROJECTS), "measurement count mismatch")
    for item in measurements:
        project = item.get("project")
        require(project in PROJECTS, f"unexpected project: {project}")
        require(item.get("raw_text_stored") is False, f"raw text stored for {project}")
        require(item.get("answer_equivalence") == "pass", f"answer equivalence failed for {project}")
        require(item.get("sensitive_redaction_gate") == "pass", f"redaction gate failed for {project}")
        require(item.get("retrieval_miss_count") <= item.get("agreed_retrieval_miss_threshold"), f"retrieval miss over threshold for {project}")
        require(not item.get("missing_markers"), f"missing markers for {project}")
        require(item.get("saving_rate", 0) >= evidence.get("minimum_saving_rate"), f"saving rate below threshold for {project}")
        require(item.get("admission_gate") is True, f"admission gate failed for {project}")
        require((ROOT / item.get("source_path", "")).exists(), f"missing measured source for {project}")

    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")

    for phrase in [
        "HEADROOM-L2-PROJECT-GROUP-DRY-RUN-20260621",
        "structured_surrogate_no_headroom_runtime",
        "不证明真实 `headroom-ai` runtime",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("generate_headroom_l2_project_group_dry_run.py" in loop_round, "loop round missing generator command")
    require("validate_headroom_l2_project_group_dry_run.py" in loop_round, "loop round missing validator command")

    print(
        "headroom_l2_project_group_dry_run=pass "
        "project_count=15 "
        f"saving_rate={aggregate.get('saving_rate')} "
        "all_admission_gates_pass=true "
        "compressor_mode=structured_surrogate_no_headroom_runtime "
        "headroom_runtime_used=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
