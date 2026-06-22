#!/usr/bin/env python3
"""Validate Headroom marker-preservation application policy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-MARKER-PRESERVATION-POLICY-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_marker_preservation_policy.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
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
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    builder = read(BUILDER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("marker_loss" in builder, "builder must encode marker loss")
    require(evidence.get("evidence_id") == "HEADROOM-MARKER-PRESERVATION-POLICY-20260621", "invalid evidence id")
    require(evidence.get("status") == "runtime_application_policy_defined", "invalid status")
    require(evidence.get("measured_production_tokens") is False, "must not claim production measurements")
    policy = evidence.get("policy", {})
    require(policy.get("default") == "reject_unless_saving_and_marker_gates_pass", "default policy mismatch")
    require(policy.get("marker_loss_is_hard_block") is True, "marker loss must hard block")
    require(policy.get("below_saving_threshold_is_hard_block") is True, "saving threshold must hard block")
    allowed = policy.get("allowed_scenarios", [])
    rejected = policy.get("rejected_scenarios", [])
    require("headroom_cost_measurement_output" in allowed, "cost measurement output must be allowed")
    require("headroom_metric_json_array" in allowed, "metric json scenario must be allowed")
    require("marker_preserving_log_search_adapter_output" in allowed, "marker-preserving adapter output must be allowed")
    for scenario in ["loop_validation_log", "rg_marker_search_output", "project_group_evidence_json"]:
        require(scenario in rejected, f"scenario must be rejected: {scenario}")
    entries = {item["scenario_id"]: item for item in evidence.get("entries", [])}
    require("marker_loss" in entries["loop_validation_log"]["reason_codes"], "log rejection must cite marker_loss")
    require("marker_loss" in entries["rg_marker_search_output"]["reason_codes"], "search rejection must cite marker_loss")
    require("rejected_not_smaller" in entries["project_group_evidence_json"]["reason_codes"], "evidence json rejection must cite size rejection")
    require(entries["marker_preserving_log_search_adapter_output"]["scenario_gate"] is True, "adapter output gate must pass")
    require(evidence.get("decision", {}).get("policy_gate") is True, "policy gate must pass")
    require(evidence.get("decision", {}).get("runtime_application_scope") == "structured_metric_and_marker_preserving_adapter_outputs", "scope mismatch")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-MARKER-PRESERVATION-POLICY-20260621",
        "marker_loss",
        "log_and_search_runtime_application | adapter_only",
        "structured_metric_and_marker_preserving_adapter_outputs",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_marker_preservation_policy.py" in loop_round, "loop round missing builder")
    print("headroom_marker_preservation_policy=pass allowed=3 rejected=3 log_and_search=adapter_only measured_production_tokens=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
