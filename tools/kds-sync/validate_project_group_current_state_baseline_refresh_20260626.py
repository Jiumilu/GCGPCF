#!/usr/bin/env python3
"""Validate the dynamic project-group current-state baseline refresh evidence."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CURRENT_JSON = ROOT / "docs/harness/evidence/project_group_live_status_current.json"
TZ = timezone(timedelta(hours=8))
FRESHNESS_HOURS = 12

PROJECTS = [
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
]

CORE_TOKENS = [
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "project_count = 17",
    "git_gate = partial",
    "development_queue_ready = true",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "auto_ready_for_review_upgrade = false",
    "authorization_granted = false",
    "action_executed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
]

FORBIDDEN_TOKENS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "auto_ready_for_review_upgrade = true",
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
]

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def load_current_snapshot(failures: list[str]) -> dict:
    if not CURRENT_JSON.exists():
        failures.append(f"missing current snapshot: {CURRENT_JSON}")
        return {}
    try:
        return json.loads(CURRENT_JSON.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"failed to parse current snapshot: {exc}")
        return {}


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    board = read(BOARD, failures)
    current = load_current_snapshot(failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in CORE_TOKENS:
        if token not in doc:
            failures.append(f"missing token in current baseline refresh: {token}")
    for project in PROJECTS:
        if project not in doc:
            failures.append(f"missing project in current baseline refresh: {project}")
    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in current baseline refresh: {token}")
    if "globalcloud-project-group-current-state-baseline-refresh-20260626.md" not in board:
        failures.append("governance board missing current-state baseline refresh reference")

    generated_at_raw = str(current.get("generated_at") or "")
    if generated_at_raw:
        try:
            generated_at = datetime.fromisoformat(generated_at_raw)
            if datetime.now(TZ) - generated_at > timedelta(hours=FRESHNESS_HOURS):
                failures.append("current snapshot is stale for current-state baseline refresh")
        except ValueError:
            failures.append("current snapshot generated_at is invalid")
    if int(current.get("project_count", 0)) != len(PROJECTS):
        failures.append(f"current snapshot project_count mismatch: {current.get('project_count')}")
    if not isinstance(current.get("review_boundary"), list):
        failures.append("current snapshot review_boundary missing")

    result = {
        "gate": "project_group_current_state_baseline_refresh_20260626",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "review_boundary": current.get("review_boundary", []),
        "observed_dirty": current.get("observed_dirty", []),
        "observed_ahead": current.get("observed_ahead", []),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates current-state baseline refresh evidence only; it does not execute tasks, clean repos, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
