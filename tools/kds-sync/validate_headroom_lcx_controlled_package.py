#!/usr/bin/env python3
"""Validate Headroom LCX controlled package artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = ROOT / "loop/context/headroom"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-controlled-package-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-controlled-package-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-CONTROLLED-PACKAGE-001.md"

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

REQUIRED_FILES = [
    "README.md",
    "policy.yaml",
    "config.schema.yaml",
    "compression-profiles.yaml",
    "mcp.json",
    "proxy.env.example",
    "adapters/codex/config.yaml",
    "adapters/claude/config.yaml",
    "adapters/cursor/config.yaml",
    "adapters/litellm/config.yaml",
    "adapters/langchain/config.yaml",
    "adapters/brain/config.yaml",
    "adapters/kds-rag/config.yaml",
    "adapters/harness/config.yaml",
    "adapters/gpc/config.yaml",
    "harness/evidence.schema.yaml",
    "harness/metrics.schema.yaml",
    "waes/headroom-policy.yaml",
    "waes/sensitive-pass-through.yaml",
    "waes/ccr-retrieve-gate.yaml",
    "kds/context-optimization-component.yaml",
    "scripts/install-headroom.sh",
    "scripts/start-proxy.sh",
    "scripts/wrap-codex.sh",
    "scripts/collect-metrics.sh",
    "scripts/learn-preview.sh",
    "scripts/apply-approved-memory.sh",
    "docs/README.md",
    "docs/architecture.md",
    "docs/operating-model.md",
    "docs/security.md",
    "docs/license.md",
    "docs/rollout.md",
]


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
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    policy = read(PACKAGE_DIR / "policy.yaml")
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    evidence = load_json(EVIDENCE_JSON)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    for rel in REQUIRED_FILES:
        read(PACKAGE_DIR / rel)

    for rel in [
        "README.md",
        "docs/README.md",
        "docs/architecture.md",
        "docs/operating-model.md",
        "docs/security.md",
        "docs/license.md",
        "docs/rollout.md",
    ]:
        path = PACKAGE_DIR / rel
        require_frontmatter(path, read(path))

    route_projects = re.findall(r"^\s*-\s+project_id:\s+([A-Za-z0-9-]+)\s*$", policy, re.MULTILINE)
    require(route_projects == PROJECTS, "policy route projects must match 15-project scope")
    require(policy.count("requires_authorization: true") == 15, "every project route must require authorization")
    require(policy.count("current_gate: dry_run_only") == 15, "every project route must stay dry-run only")
    for phrase in [
        "telemetry_default: off",
        "production_admission_gate: false",
        "measured_production_tokens: false",
        "accepted: false",
        "integrated: false",
        "production_ready: false",
        "mcp_retrieve_without_waes_gate",
        "learn_apply_auto",
        "cross_project_memory_as_fact",
    ]:
        require(phrase in policy, f"policy missing phrase: {phrase}")

    mcp = load_json(PACKAGE_DIR / "mcp.json")
    require(mcp["tools"]["headroom_retrieve"]["requires_waes_gate"] is True, "MCP retrieve must require WAES gate")
    require(mcp["production_admission_gate"] is False, "MCP production gate must remain false")

    evidence_schema = read(PACKAGE_DIR / "harness/evidence.schema.yaml")
    for field in [
        "task_id",
        "loop_round_id",
        "project_id",
        "tokens_before",
        "tokens_after",
        "saving_rate",
        "ccr_retrieve_count",
        "waes_decision",
        "answer_equivalence",
        "marker_gate",
        "sensitive_redaction_gate",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(field in evidence_schema, f"evidence schema missing field: {field}")

    waes_policy = read(PACKAGE_DIR / "waes/headroom-policy.yaml")
    for rule in ["LCX-001", "LCX-002", "LCX-003", "LCX-004", "LCX-005"]:
        require(rule in waes_policy, f"WAES policy missing rule: {rule}")

    retrieve_gate = read(PACKAGE_DIR / "waes/ccr-retrieve-gate.yaml")
    require("default_action: require_evidence" in retrieve_gate, "CCR retrieve must require evidence")
    require("retrieve_reason" in retrieve_gate, "CCR retrieve reason is required")

    kds_component = read(PACKAGE_DIR / "kds/context-optimization-component.yaml")
    require("fact_authority: false" in kds_component, "KDS component must not be fact authority")
    require("evidence_authority: false" in kds_component, "KDS component must not be evidence authority")

    for rel in ["scripts/start-proxy.sh", "scripts/wrap-codex.sh", "scripts/learn-preview.sh"]:
        script = read(PACKAGE_DIR / rel)
        require("HEADROOM_TELEMETRY" in script, f"{rel} must control telemetry")
    require("HEADROOM_PRODUCTION_PROXY" in read(PACKAGE_DIR / "scripts/start-proxy.sh"), "proxy script must block production mode")
    learn_preview = read(PACKAGE_DIR / "scripts/learn-preview.sh")
    require("dry-run preview mode only" in learn_preview, "learn script must declare dry-run preview mode")
    require("--apply" not in learn_preview, "learn script must not pass --apply")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-CONTROLLED-PACKAGE-20260621", "invalid evidence id")
    require(evidence.get("projects") == PROJECTS, "evidence projects mismatch")
    gates = evidence.get("gates", {})
    for key in [
        "all_projects_have_routes",
        "proxy_configured",
        "sdk_configured",
        "mcp_configured",
        "agent_wrap_configured",
        "ccr_retrieve_gate_configured",
        "harness_evidence_schema_configured",
        "waes_policy_configured",
        "kds_candidate_component_configured",
        "cost_model_replayable",
        "telemetry_default_off",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
        "raw_sensitive_context_stored",
        "learn_apply_auto",
        "cross_project_memory_as_fact",
        "production_admission_gate",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    require(gates.get("project_route_count") == 15, "project route count must be 15")

    for phrase in [
        "HEADROOM-LCX-CONTROLLED-PACKAGE-20260621",
        "project_route_count | 15",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("GPCF-HEADROOM-LCX-P0-RUNTIME-REPLAY-001" in loop_round, "loop round missing next round")

    print(
        "headroom_lcx_controlled_package=pass "
        "project_route_count=15 proxy=true sdk=true mcp=true agent_wrap=true "
        "ccr_retrieve_gate=true production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
