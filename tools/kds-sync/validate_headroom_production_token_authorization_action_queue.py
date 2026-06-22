#!/usr/bin/env python3
"""Validate Headroom production-token authorization action queue evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-ACTION-QUEUE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_production_token_authorization_action_queue.py"
AUTHORIZATION_PACKAGE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"


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
    runner = read(RUNNER)
    authorization_package = load_json(AUTHORIZATION_PACKAGE)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("ACTIONS" in runner, "runner must define action queue")
    require(evidence.get("evidence_id") == "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-ACTION-QUEUE-20260621", "invalid evidence id")
    require(evidence.get("status") == "authorization_action_queue_defined_blocking", "invalid status")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    require(authorization_package.get("authorization", {}).get("status") == "pending", "authorization package must remain pending")
    actions = evidence.get("actions", [])
    require(isinstance(actions, list) and len(actions) == 6, "action count mismatch")
    action_ids = {action.get("action_id") for action in actions}
    for expected in [
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-001",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-002",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-003",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-004",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-005",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-006",
    ]:
        require(expected in action_ids, f"missing action: {expected}")
    for action in actions:
        require(action.get("owner"), "each action must have owner")
        require(action.get("due_loop") == "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001", "due loop mismatch")
        require(action.get("gate") is False, "action gate must remain false")
        require(str(action.get("status", "")).startswith("pending"), "action status must remain pending")
    gate = evidence.get("gate", {})
    require(gate.get("action_count") == 6, "gate action count mismatch")
    require(gate.get("all_actions_have_owner") is True, "owners must be present")
    require(gate.get("all_actions_have_due_loop") is True, "due loops must be present")
    require(gate.get("all_actions_closed") is False, "actions must not be closed")
    require(gate.get("authorization_action_queue_gate") is False, "action queue gate must remain false")
    require(gate.get("production_admission_gate") is False, "production admission must remain false")
    require(evidence.get("decision", {}).get("production_admission_gate") is False, "decision production gate must remain false")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-ACTION-QUEUE-20260621",
        "authorization_action_queue_gate | false",
        "production_admission_gate | false",
        "measured_production_tokens | false",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-001",
        "HEADROOM-PROD-TOKEN-AUTH-ACTION-006",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_production_token_authorization_action_queue.py" in loop_round, "loop round missing runner")
    require("validate_headroom_production_token_authorization_action_queue.py" in loop_round, "loop round missing validator")
    print(
        "headroom_production_token_authorization_action_queue=pass "
        "action_count=6 authorization_action_queue_gate=false "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
