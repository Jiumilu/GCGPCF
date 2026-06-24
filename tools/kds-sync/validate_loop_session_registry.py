#!/usr/bin/env python3
"""Validate the LOOP session registry against repo-recorded loop rounds."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "02-governance/loop/LOOP_SESSION_REGISTRY.md"
CURRENT_DECLARATION = ROOT / "docs/harness/evidence/current-session-mainline-declaration-20260622.json"
CURRENT_DECLARATION_VALIDATOR = ROOT / "tools/kds-sync/validate_current_session_mainline_declaration.py"
PREFLIGHT_VALIDATOR = ROOT / "tools/kds-sync/validate_session_mainline_preflight_enforcement.py"
DRIFT_WATCH_VALIDATOR = ROOT / "tools/kds-sync/validate_session_mainline_drift_watch.py"
HANDOFF_REQUEST_GATE_VALIDATOR = ROOT / "tools/kds-sync/validate_session_mainline_handoff_request_gate.py"
LOOP_DOCUMENT_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"
LOOPS_DIR = ROOT / "docs/harness/loops"
README = ROOT / "02-governance/loop/README.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_session_registry: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def classify(round_id: str) -> str | None:
    if round_id.startswith(("GPCF-L4-GFIS", "GPCF-GFIS")):
        return "GFIS L4 repair and test sync"
    if round_id.startswith(("GPCF-KDS-DKS", "GPCF-GCKF")):
        return "KDS / DKS governance"
    if round_id.startswith(("GPCF-ONTOLOGY-WAS", "GPCF-WAS")):
        return "Ontology / WAS governance"
    if round_id.startswith("GPCF-CODEGRAPH"):
        return "CodeGraph governance"
    if round_id.startswith("GPCF-COGNEE"):
        return "COGNEE pilot / writeback"
    if round_id.startswith("GPCF-AGENT-REACH"):
        return "Agent-Reach governance"
    if round_id.startswith("GPCF-HEADROOM"):
        return "Headroom / LCX governance"
    if round_id.startswith("GPCF-OKF"):
        return "OKF / ODF governance"
    if round_id.startswith(("GPCF-CF", "GPCF-L4-CORR", "GPCF-L4-IMPROVE")):
        return "GPCF CF / governance rounds"
    if round_id.startswith("GPCF-L4-"):
        token = round_id.removeprefix("GPCF-L4-").split("-", 1)[0]
        if token.isdigit():
            return "GPCF CF / governance rounds"
    if round_id.startswith("GPCF-L4-XIAOG"):
        return "XiaoG evidence repair"
    if round_id.startswith("GPCF-PROJECT"):
        return "Project group phase goals"
    if round_id.startswith("GPCF-LOOP"):
        return "LOOP localization/governance"
    if round_id.startswith("GPCF-UI"):
        return "UI governance and validation"
    if round_id.startswith("GPCF-SESSION"):
        return "Session declaration and mainline"
    return None


def iter_round_ids() -> list[str]:
    ids: list[str] = []
    for path in sorted(LOOPS_DIR.glob("loop-round-*.md")):
        ids.append(path.stem.removeprefix("loop-round-"))
    return ids


def main() -> int:
    registry = read(REGISTRY)
    readme = read(README)
    current_validator = read(CURRENT_DECLARATION_VALIDATOR)
    preflight_validator = read(PREFLIGHT_VALIDATOR)
    drift_watch_validator = read(DRIFT_WATCH_VALIDATOR)
    handoff_request_gate_validator = read(HANDOFF_REQUEST_GATE_VALIDATOR)
    loop_document_gate = read(LOOP_DOCUMENT_GATE)
    require(CURRENT_DECLARATION.exists(), "current session declaration evidence missing")

    for phrase in [
        "status: controlled",
        "source_path: 02-governance/loop/LOOP_SESSION_REGISTRY.md",
        "sync_direction: bidirectional",
        "LOOP 会话总账",
        "repo_recorded_loop_sessions_only",
        "live_codex_threads_covered | false",
        "auto_takeover_allowed | false",
        "write_without_handoff_allowed | false",
        "status_promotion_allowed | false",
        "current_gpcf_loop_governance_session",
        "LOOP治理主线: session-mainline-control rollout",
        "orphan_session_family",
        "handoff_required_for_execution",
        "validate_loop_session_registry.py",
    ]:
        require(phrase in registry, f"registry missing phrase: {phrase}")

    families = [
        "GFIS L4 repair and test sync",
        "KDS / DKS governance",
        "Ontology / WAS governance",
        "CodeGraph governance",
        "COGNEE pilot / writeback",
        "Agent-Reach governance",
        "Headroom / LCX governance",
        "OKF / ODF governance",
        "GPCF CF / governance rounds",
        "XiaoG evidence repair",
        "Project group phase goals",
        "LOOP localization/governance",
        "UI governance and validation",
        "Session declaration and mainline",
    ]
    for family in families:
        require(family in registry, f"missing session family: {family}")

    forbidden = [
        "write_without_handoff_allowed | true",
        "auto_takeover_allowed | true",
        "status_promotion_allowed | true",
        "允许自动接管",
        "允许自动升级 accepted",
        "允许自动升级 integrated",
    ]
    for phrase in forbidden:
        require(phrase not in registry, f"forbidden registry claim present: {phrase}")

    unknown: list[str] = []
    counts: dict[str, int] = {family: 0 for family in families}
    for round_id in iter_round_ids():
        family = classify(round_id)
        if family is None:
            unknown.append(round_id)
        else:
            counts[family] += 1
    require(not unknown, "orphan_session_family: " + ", ".join(unknown[:20]))
    require(sum(counts.values()) == len(iter_round_ids()), "session family count mismatch")

    require("current_session_mainline_declaration=pass" in current_validator, "current declaration validator missing pass marker")
    require(
        "loop_session_registry" in loop_document_gate
        and "validate_loop_session_registry.py" in loop_document_gate,
        "loop document gate missing session registry validator",
    )
    require(
        "session_mainline_preflight_enforcement" in loop_document_gate
        and "validate_session_mainline_preflight_enforcement.py" in loop_document_gate,
        "loop document gate missing session mainline preflight validator",
    )
    require(
        "session_mainline_drift_watch" in loop_document_gate
        and "validate_session_mainline_drift_watch.py" in loop_document_gate,
        "loop document gate missing session mainline drift watch validator",
    )
    require(
        "session_mainline_handoff_request_gate" in loop_document_gate
        and "validate_session_mainline_handoff_request_gate.py" in loop_document_gate,
        "loop document gate missing session mainline handoff request gate validator",
    )
    require(
        "LOOP 会话总账 | 02-governance/loop/LOOP_SESSION_REGISTRY.md" in readme,
        "loop README missing session registry entry",
    )
    require(
        "session_mainline_preflight_enforcement=pass" in preflight_validator
        and "preflight_decision=continue_current_mainline_only" in preflight_validator,
        "preflight validator missing pass markers",
    )
    require(
        "session_mainline_drift_watch=pass" in drift_watch_validator
        and "watch_mode=repo_recorded_governance_only" in drift_watch_validator,
        "drift watch validator missing pass markers",
    )
    require(
        "session_mainline_handoff_request_gate=pass" in handoff_request_gate_validator
        and "gate_mode=explicit_user_confirmation_required" in handoff_request_gate_validator,
        "handoff request gate validator missing pass markers",
    )

    counts_text = ",".join(f"{key.replace(' ', '_').replace('/', '_')}={value}" for key, value in counts.items())
    print(
        "loop_session_registry=pass "
        f"repo_recorded_loop_rounds={len(iter_round_ids())} "
        "orphan_session_family=0 "
        "live_codex_threads_covered=false "
        "auto_takeover_allowed=false "
        f"{counts_text}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
