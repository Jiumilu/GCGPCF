#!/usr/bin/env python3
"""Validate the Headroom LCX graph manifest evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependency
    raise SystemExit(f"PyYAML is required: {exc}") from exc


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-GRAPH-MANIFEST-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_graph_manifest.py"
POLICY = ROOT / "loop/context/headroom/policy.yaml"
WINDOW_REQUEST = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json"
NEXT_STAGE_PACKAGE = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json"
METADATA_REPLAY = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json"
SANITIZED_LEDGER = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
LOOP_COST_SERIES = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"
INDEPENDENT_REPLAY = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json"

PROJECT_IDS = [
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


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a YAML object")
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
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    manifest = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    policy = load_yaml(POLICY)
    window_request = load_json(WINDOW_REQUEST)
    next_stage_package = load_json(NEXT_STAGE_PACKAGE)
    metadata_replay = load_json(METADATA_REPLAY)
    sanitized_ledger = load_json(SANITIZED_LEDGER)
    loop_cost_series = load_json(LOOP_COST_SERIES)
    independent_replay = load_json(INDEPENDENT_REPLAY)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("build_headroom_lcx_graph_manifest" in runner, "runner missing graph builder name")
    require("validate_headroom_lcx_graph_manifest" in read(Path(__file__)), "validator self reference missing")

    require(manifest.get("graph_id") == "HEADROOM-LCX-GRAPH-MANIFEST-20260623", "invalid graph id")
    require(manifest.get("status") == "controlled_pending_real_measurement", "invalid graph status")
    require(manifest.get("scope", {}).get("project_count") == 15, "project count mismatch")
    require(manifest.get("scope", {}).get("project_ids") == PROJECT_IDS, "project ids mismatch")

    routes = manifest.get("project_routes", [])
    require(len(routes) == 15, "route count mismatch")
    require({route.get("project_id") for route in routes} == set(PROJECT_IDS), "route project coverage mismatch")
    required_fields = {
        "project_id",
        "source_path",
        "allowed_modes",
        "blocked_modes",
        "requires_authorization",
        "cost_fields",
        "sensitive_boundaries",
        "owner",
        "current_gate",
    }
    for route in routes:
        require(required_fields.issubset(route), f"route missing required fields: {route.get('project_id')}")

    layers = {layer["layer_id"]: layer for layer in manifest.get("layers", [])}
    for layer_id in [
        "route_layer",
        "authorization_layer",
        "authorization_bridge_layer",
        "token_ledger_bridge_layer",
        "cost_bridge_layer",
        "cost_layer",
        "runtime_layer",
        "rollback_layer",
        "equivalence_layer",
        "production_branch",
    ]:
        require(layer_id in layers, f"missing layer: {layer_id}")

    auth = manifest.get("authorization", {})
    require(auth.get("waes_harness_admission_decision") == "admitted_for_sanitized_measurement_precheck", "invalid admission decision")
    require(auth.get("production_token_measurement_allowed") is False, "production token measurement must remain false")
    require(auth.get("measured_production_tokens") is False, "measured_production_tokens must remain false")
    require(auth.get("accepted") is False, "accepted must remain false")
    require(auth.get("integrated") is False, "integrated must remain false")
    require(auth.get("production_ready") is False, "production_ready must remain false")
    require(auth.get("production_proxy_started") is False, "production_proxy_started must remain false")
    require(auth.get("production_sdk_enabled") is False, "production_sdk_enabled must remain false")
    require(auth.get("production_external_api_write") is False, "production_external_api_write must remain false")
    require(auth.get("kds_api_write") is False, "kds_api_write must remain false")
    require(auth.get("authorization_window_request_evidence_id") == window_request.get("evidence_id"), "authorization window request evidence mismatch")
    require(auth.get("next_stage_authorization_package_evidence_id") == next_stage_package.get("evidence_id"), "next stage authorization package evidence mismatch")
    require(auth.get("next_stage_authorization_package_status") == next_stage_package.get("status"), "next stage authorization package status mismatch")
    require(auth.get("sanitized_token_ledger_id") == sanitized_ledger.get("ledger_id"), "sanitized token ledger mismatch")
    require(auth.get("metadata_replay_check_evidence_id") == metadata_replay.get("evidence_id"), "metadata replay evidence mismatch")
    require(auth.get("metadata_replay_check_status") == metadata_replay.get("status"), "metadata replay status mismatch")
    require(auth.get("loop_cost_observation_series_evidence_id") == loop_cost_series.get("evidence_id"), "loop cost observation series mismatch")
    require(auth.get("loop_cost_observation_series_status") == loop_cost_series.get("status"), "loop cost observation series status mismatch")
    require(auth.get("independent_replay_evidence_id") == independent_replay.get("evidence_id"), "independent replay evidence mismatch")
    require(auth.get("independent_replay_status") == independent_replay.get("status"), "independent replay status mismatch")

    cost_graph = manifest.get("cost_graph", {})
    require(cost_graph.get("project_count") == 15, "cost graph project count mismatch")
    require(cost_graph.get("profile_count") == 3, "cost profile count mismatch")
    require(cost_graph.get("production_admission_gate") is False, "cost production gate must remain false")
    require(cost_graph.get("measured_production_tokens") is False, "cost measured production tokens must remain false")

    rollback = manifest.get("rollback_graph", {})
    require(rollback.get("rollback_plan_present") is True, "rollback plan must be present")
    require(rollback.get("rollback_plan_id") == "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001", "rollback plan id mismatch")

    equivalence = manifest.get("equivalence_graph", {})
    require(equivalence.get("business_answer_equivalence_proven") is False, "business equivalence must remain false")
    require(equivalence.get("answer_equivalence_gate") is True, "synthetic equivalence gate must pass")
    require(equivalence.get("real_business_measurement_allowed") is False, "real business measurement must remain false")

    runtime = manifest.get("runtime_graph", {})
    require(runtime.get("source_evidence_id") == "HEADROOM-LCX-PRODUCTION-RUNTIME-GRAPH-20260623", "runtime graph evidence mismatch")
    require(runtime.get("status") == "production_runtime_graph_defined_controlled_only", "runtime graph status mismatch")
    require(runtime.get("production_branch_blocked") is True, "runtime graph production branch blocked mismatch")

    non_claims = manifest.get("non_claims", {})
    for key, value in non_claims.items():
        require(value is False, f"non-claim must stay false: {key}")

    for phrase in [
        "Headroom 的项目群图谱已固化为受控 manifest",
        "production runtime graph 已作为正式层接入 manifest",
        "headroom-lcx-real-measurement-authorization-window-request-20260623.json",
        "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json",
        "headroom-lcx-metadata-replay-check-20260622.json",
        "headroom-independent-loop-round-replay-20260621.json",
        "production_token_measurement_allowed | `false`",
        "measurement_authorization_state | `admitted_for_sanitized_measurement_precheck`",
        "real_business_equivalence_measurement_allowed | `false`",
        "production_branch | blocked",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in [
        "Headroom 的项目群图谱固化为统一 manifest",
        "production branch 仍保持 blocked",
        "next-stage authorization bridge 已作为受控桥接层接入 manifest",
        "next_stage_authorization_package_granted_precheck_only",
        "sanitized token ledger bridge 已作为 metadata replay only 层接入 manifest",
        "cost bridge 已作为 replay only 层接入 manifest",
        "runtime graph 和等价性串成单一可审计 manifest",
        "build_headroom_lcx_graph_manifest.py",
        "validate_headroom_lcx_graph_manifest.py",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for phrase in [
        "production_admission_gate: false",
        "measured_production_tokens: false",
        "accepted: false",
        "integrated: false",
        "production_ready: false",
    ]:
        require(phrase in read(POLICY), f"policy missing false gate phrase: {phrase}")

    print(
        "headroom_lcx_graph_manifest=pass "
        "project_count=15 "
        "route_count=15 "
        "profile_count=3 "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
