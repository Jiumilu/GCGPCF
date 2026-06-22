#!/usr/bin/env python3
"""Validate the Loop five-direction self-evolution evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-five-direction-self-evolution-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-five-direction-self-evolution-20260622.md"
ORCHESTRATOR_SKILL = ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md"
AUTONOMY_POLICY = ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
TEMPLATE = ROOT / "templates/loop-round-v2-five-direction.yaml"
BASE_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_engineering_five_direction_implementation.py"
RUN_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_five_direction_run_001.py"
SMOKE_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_five_direction_standing_smoke.py"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_five_direction_self_evolution: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_controlled(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    orchestrator = read(ORCHESTRATOR_SKILL)
    policy = read(AUTONOMY_POLICY)
    control_board = read(CONTROL_BOARD)
    template = read(TEMPLATE)
    base_validator = read(BASE_VALIDATOR)

    for path in [RUN_VALIDATOR, SMOKE_VALIDATOR]:
        require(path.exists(), f"missing validator: {path.relative_to(ROOT)}")

    require_controlled(evidence_md, "docs/harness/evidence/loop-five-direction-self-evolution-20260622.md")

    require(evidence.get("self_evolution_id") == "GPCF-LOOP-FIVE-DIRECTION-SELF-EVOLUTION-001", "wrong self_evolution_id")
    require(evidence.get("status") == "adopted_as_default_loop_constraint", "wrong self-evolution status")
    require(evidence.get("status_ceiling") == "partial_repair", "status ceiling must remain partial_repair")
    require(evidence.get("real_business_lane") == "repair_required", "real business lane must remain repair_required")
    for key in ["accepted", "integrated", "production_ready"]:
        require(evidence.get(key) is False, f"{key} must remain false")
    for key in ["production_writes", "real_external_api_writes", "kds_fact_writes", "waes_gate_result_writes"]:
        require(evidence.get(key) == 0, f"{key} must remain zero")
    require(evidence.get("no_write_boundary_enforced") is True, "no-write boundary must be enforced")

    for key in ["orchestrator", "policy", "control_board", "template", "validator"]:
        require(key in evidence.get("change", {}), f"change missing: {key}")

    for key in ["run_001", "standing_smoke", "base_validator"]:
        require(key in evidence.get("verification", {}), f"verification missing: {key}")

    for phrase in [
        "LOOP 运行控制闭环",
        "历史别名为 LOOP 五方向",
        "run",
        "stop",
        "verify",
        "recover",
        "debug",
    ]:
        require(phrase in orchestrator, f"orchestrator missing phrase: {phrase}")

    for phrase in [
        "LOOP 运行控制闭环常驻接入规则",
        "适用于 L1、L2、L3、L3.5、L4、L5",
        "不得替代运行控制闭环结构",
    ]:
        require(phrase in policy, f"policy missing phrase: {phrase}")

    for phrase in [
        "LOOP 运行控制闭环常驻能力",
        "active / all Loop work",
        "后续所有非只读 Loop 工作必须按",
    ]:
        require(phrase in control_board, f"control board missing phrase: {phrase}")

    for phrase in [
        "official_name: \"LOOP 运行控制闭环\"",
        "legacy_alias: \"LOOP 五方向\"",
        "applies_to: all_loop_work_except_readonly_qa",
        "mandatory_for: [L1, L2, L3, L3.5, L4, L5]",
        "run:",
        "stop:",
        "verify:",
        "recover:",
        "debug:",
    ]:
        require(phrase in template, f"template missing phrase: {phrase}")

    for phrase in [
        "loop-five-direction-self-evolution-20260622",
        "GPCF-LOOP-FIVE-DIRECTION-SELF-EVOLUTION-001",
    ]:
        require(phrase in base_validator, f"base validator missing self-evolution integration: {phrase}")

    for phrase in [
        "GPCF-LOOP-FIVE-DIRECTION-SELF-EVOLUTION-001",
        "把经验编译进规则、模板和门禁",
        "adopted_as_default_loop_constraint",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")

    print(
        "loop_five_direction_self_evolution=pass "
        "status=adopted_as_default_loop_constraint "
        "next_constraint=all_non_readonly_loop_rounds_require_run_stop_verify_recover_debug "
        "real_business_lane=repair_required accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
