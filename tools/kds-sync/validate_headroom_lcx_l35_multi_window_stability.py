#!/usr/bin/env python3
"""Validate Headroom LCX L3.5 multi-window sanitized stability evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_l35_multi_window_stability.py"

PROJECTS = {
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
}


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("range(1, 6)" in runner, "runner must define five windows")
    require("substantive_rounds" in runner, "runner must record continuous-run substance")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622", "invalid evidence id")
    require(evidence.get("status") == "l3_5_multi_window_stability_pass_check_only", "invalid status")
    require(evidence.get("window_count") == 5, "window count mismatch")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("record_count_per_window") == 45, "record count per window mismatch")
    require(evidence.get("total_record_count") == 225, "total record count mismatch")
    require(evidence.get("stable_hash_count") == 1, "stable hash count mismatch")
    require(evidence.get("failures") == [], "failures must be empty")

    session = evidence.get("continuous_session", {})
    require(session.get("mode") == "L3.5", "continuous mode mismatch")
    require(session.get("declared_rounds") == 5, "declared rounds mismatch")
    require(session.get("substantive_rounds") == 1, "substantive rounds mismatch")
    require(session.get("batch_generated") is True, "batch_generated must be true")
    require(session.get("stop_type") == "authorization_boundary", "stop type must be authorization_boundary")

    windows = evidence.get("windows", [])
    require(isinstance(windows, list) and len(windows) == 5, "windows mismatch")
    hashes = {window.get("stable_hash") for window in windows}
    require(len(hashes) == 1 and next(iter(hashes)), "window hashes must be stable")
    for window in windows:
        require(window.get("record_count") == 45, "window record count mismatch")
        require(window.get("project_count") == 15, "window project count mismatch")
        require(window.get("failures") == [], "window failures must be empty")
        records = window.get("records", [])
        require({record.get("project_id") for record in records} == PROJECTS, "window project coverage mismatch")
        for record in records:
            require(record.get("tokens_saved") == "not_calculated", "tokens_saved must not be calculated")
            require(record.get("saving_rate") == "not_calculated", "saving_rate must not be calculated")
            require(record.get("answer_equivalence") == "not_measured", "answer equivalence must not be measured")
            for key in ["measured_production_tokens", "accepted", "integrated", "production_ready"]:
                require(record.get(key) is False, f"record field must be false: {key}")

    gates = evidence.get("gates", {})
    for key in [
        "l3_5_multi_window_stability_gate",
        "source_l35_window_gate",
        "window_count_gate",
        "record_count_gate",
        "project_coverage_gate",
        "multi_window_hash_stability_gate",
        "metadata_only",
        "check_only",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "headroom_learn_apply_executed",
        "l4_candidate",
        "l5_candidate",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622",
        "window_count: `5`",
        "stable_hash_count: `1`",
        "substantive_rounds | 1",
        "stop_type | authorization_boundary",
        "l3_5_multi_window_stability_gate | true",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in ["run:", "stop:", "verify:", "recover:", "debug:"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")
    require("validate_headroom_lcx_l35_multi_window_stability.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_l35_multi_window_stability=pass_check_only "
        "window_count=5 project_count=15 record_count_per_window=45 stable_hash_count=1 "
        "substantive_rounds=1 l4_candidate=false measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
