#!/usr/bin/env python3
"""Validate the authorized GKE-001 Studio/KDS/Brain coordination envelope."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
ENVELOPE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-three-lane-coordination-envelope.yaml"
STUDIO_A4 = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-studio-intake-amendment-a4.yaml"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
SESSION_REGISTRY = ROOT / "02-governance/loop/LOOP_SESSION_REGISTRY.md"
LOOP_EVIDENCE = ROOT / "docs/harness/loops/loop-round-GPCF-GKE-001-COORDINATION-003.md"
FEATURE = ROOT / "features/active/F-013-knowledge-asset-model-system/feature.yaml"
SUMMARY = ROOT / "features/active/F-013-knowledge-asset-model-system/evidence/summary.md"

COORDINATION_ID = "GKE-001-COORDINATION-20260803-001"
COORDINATOR_THREAD = "019f0697-c8ce-7110-8ac8-9a7dbc6ba2a5"
ENVELOPE_SHA256 = "e95307a21c4197798d692a7efe18be22f7d305c145942ce47a1afc24f06ceeff"
STUDIO_A4_ID = "GKE-001-COORDINATION-20260803-001-A4"
STUDIO_A4_SHA256 = "c1c7963b0f66e5c66d471817c0f25219fe1653182362c5b4b3fe01010bfc6f3a"
LANE_THREADS = {
    "studio": "019ee242-2575-73f1-b5bb-d43e7e49468e",
    "kds": "019fc4e3-bce5-7541-85e3-8885c7e78aea",
    "brain": "019edfb4-21ef-77e1-afdb-891df25c4068",
}
LANE_CHANGES = {
    "studio": "restore-studio-backend-runtime",
    "kds": "extend-kds-document-extraction",
    "brain": "brain-studio-readonly-kds-bridge",
}


def fail(message: str) -> None:
    print(f"gke001_three_lane_coordination=fail reason={message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    envelope_text = read(ENVELOPE)
    envelope_sha = hashlib.sha256(envelope_text.encode("utf-8")).hexdigest()
    require(envelope_sha == ENVELOPE_SHA256, f"envelope_sha_mismatch:{envelope_sha}")
    data = yaml.safe_load(envelope_text).get("coordination_envelope", {})
    require(data.get("id") == COORDINATION_ID, "coordination_id_mismatch")
    require(data.get("engineering_domain") == "GKE-001", "engineering_domain_mismatch")
    require(data.get("canonical_feature") == "F-013", "canonical_feature_mismatch")
    require(data.get("coordinator", {}).get("thread_id") == COORDINATOR_THREAD, "coordinator_thread_mismatch")
    require(data.get("coordinator", {}).get("role") == "sole_gke001_coordinator", "coordinator_role_mismatch")
    require(data.get("status", {}).get("completion") == "not_complete", "completion_boundary_mismatch")
    require(data.get("status", {}).get("status_ceiling") == "partial", "status_ceiling_mismatch")

    lanes = data.get("lanes", {})
    require(set(lanes) == set(LANE_THREADS), "lane_set_mismatch")
    require(len({lane.get("thread_id") for lane in lanes.values()}) == 3, "duplicate_lane_thread")
    require(len({lane.get("repository") for lane in lanes.values()}) == 3, "duplicate_lane_repository")
    require(len({lane.get("coordination_lock_id") for lane in lanes.values()}) == 3, "duplicate_lane_lock")
    for lane_name, thread_id in LANE_THREADS.items():
        lane = lanes[lane_name]
        require(lane.get("thread_id") == thread_id, f"thread_mismatch:{lane_name}")
        require(lane.get("change_id") == LANE_CHANGES[lane_name], f"change_mismatch:{lane_name}")
        require(bool(lane.get("file_allowlist")), f"empty_allowlist:{lane_name}")
        require(bool(lane.get("forbidden_scope")), f"empty_forbidden_scope:{lane_name}")
        require(set(lane.get("file_allowlist", ())).isdisjoint(lane.get("forbidden_scope", ())), f"scope_overlap:{lane_name}")

    kds = lanes["kds"]
    for excluded in ("_registries/global-object-registry.yaml", "entities/green-supply-chain-role-view-entity.md"):
        require(excluded in kds.get("forbidden_scope", ()), f"kds_external_file_not_forbidden:{excluded}")
        require(excluded not in kds.get("file_allowlist", ()), f"kds_external_file_in_allowlist:{excluded}")
    for regression_test in ("tests/test_knowledge_intake_api.py", "tests/test_knowledge_intake_postgres.py"):
        require(regression_test in kds.get("file_allowlist", ()), f"kds_regression_test_not_allowed:{regression_test}")
    require(lanes["brain"].get("execution_mode") == "freeze_and_wait", "brain_not_frozen")
    studio = lanes["studio"]
    require(".harness/opsx.lock" in studio.get("file_allowlist", ()), "studio_ephemeral_lock_not_allowed")
    require("docs/harness/loops/loop-round-GPCF-STUDIO-LR-872.md" in studio.get("file_allowlist", ()), "studio_lr872_not_allowed")
    require(studio.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "studio_lock_handling_mismatch")
    amendments = {item.get("id"): item for item in data.get("scope_amendments", [])}
    require("GKE-001-COORDINATION-20260803-001-A1" in amendments, "studio_amendment_missing")
    require("GKE-001-COORDINATION-20260803-001-A2" in amendments, "kds_amendment_missing")
    require("GKE-001-COORDINATION-20260803-001-A3" in amendments, "kds_review_amendment_missing")
    require(".harness/opsx.lock" in kds.get("file_allowlist", ()), "kds_ephemeral_lock_not_allowed")
    require(kds.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "kds_lock_handling_mismatch")
    require(set(lanes["brain"].get("allowed_kds_operations", ())) == {"search", "graph", "page-content"}, "brain_operation_scope_mismatch")
    require(data.get("serial_order") == [
        "kds_stage_b_implementation_and_tests",
        "f013_independent_readonly_review",
        "studio_intake_evidence_review_task_integration",
        "brain_search_wikipreview_chat_readonly_e2e",
        "mmc_delegation_and_human_confirmation_validation",
    ], "serial_order_mismatch")

    required_handoff = set(data.get("handoff_requirements", {}).get("required", ()))
    expected_handoff = {
        "exact_changed_files", "tests", "acl_read", "acl_count", "audit", "lineage",
        "mirror_sha256", "migration_dry_run", "rollback", "authorization_status", "unresolved_risks",
    }
    require(required_handoff == expected_handoff, "handoff_requirement_mismatch")
    authorization = data.get("authorization", {})
    require(authorization.get("kds_stage_b_local_development") is True, "kds_stage_b_dev_not_authorized")
    for key in ("real_kds_write", "long_term_memory_write", "relationship_confirmation", "business_state_change", "commit", "push", "deployment", "status_promotion", "human_confirmation_completed"):
        require(authorization.get(key) is False, f"authorization_boundary_drift:{key}")
    require(data.get("gckf_boundary", {}).get("satisfied_resume_triggers") == 0, "gckf_resume_trigger_drift")
    require(data.get("gckf_boundary", {}).get("creates_d191") is False, "unexpected_d191")

    studio_a4_text = read(STUDIO_A4)
    studio_a4_sha = hashlib.sha256(studio_a4_text.encode("utf-8")).hexdigest()
    require(studio_a4_sha == STUDIO_A4_SHA256, f"studio_a4_sha_mismatch:{studio_a4_sha}")
    studio_a4 = yaml.safe_load(studio_a4_text).get("studio_intake_amendment", {})
    require(studio_a4.get("id") == STUDIO_A4_ID, "studio_a4_id_mismatch")
    require(studio_a4.get("parent_envelope", {}).get("sha256") == ENVELOPE_SHA256, "studio_a4_parent_sha_mismatch")
    require(studio_a4.get("lane", {}).get("thread_id") == LANE_THREADS["studio"], "studio_a4_thread_mismatch")
    require(studio_a4.get("lane", {}).get("change_id") == "integrate-studio-kds-knowledge-intake", "studio_a4_change_mismatch")
    require(studio_a4.get("canonical_contract", {}).get("revision") == "v0.1", "studio_a4_contract_revision_mismatch")
    require(studio_a4.get("canonical_contract", {}).get("manifest_sha256") == "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de", "studio_a4_manifest_sha_mismatch")
    require(studio_a4.get("status", {}).get("phase_1") == "authorized_local_tdd_contract_and_ui", "studio_a4_phase1_not_authorized")
    require(studio_a4.get("status", {}).get("phase_2") == "blocked_by_mmc_prepare_retry_delegated_operation_review", "studio_a4_phase2_boundary_mismatch")
    require(studio_a4.get("authorization", {}).get("phase_1_local_product_edits") is True, "studio_a4_product_edits_not_authorized")
    for key in ("phase_2_disposable_kds_write", "shared_or_persistent_kds_write", "real_business_asset", "relationship_confirmation", "long_term_memory_write", "business_state_change", "commit", "push", "deployment", "status_promotion"):
        require(studio_a4.get("authorization", {}).get(key) is False, f"studio_a4_authorization_drift:{key}")
    studio_a4_allowlist = set(studio_a4.get("file_allowlist", ()))
    for required_path in (
        ".harness/opsx.lock",
        "packages/server/src/routes/governance/knowledge-intake.ts",
        "packages/client/src/components/studio/ProjectKnowledgeIntakePanel.vue",
        "openspec/changes/integrate-studio-kds-knowledge-intake/**",
        "docs/harness/loops/loop-round-GPCF-STUDIO-LR-873.md",
    ):
        require(required_path in studio_a4_allowlist, f"studio_a4_allowlist_missing:{required_path}")
    require(studio_a4.get("ephemeral_files", [])[0].get("handling") == "execution_only_never_stage_commit_or_handoff", "studio_a4_lock_handling_mismatch")
    endpoint_admission = {
        item.get("path"): item.get("mmc_admission")
        for item in studio_a4.get("canonical_contract", {}).get("endpoints", {}).get("stage_a_write", ())
    }
    require(endpoint_admission.get("/api/v1/knowledge-assets/intake") == "blocked_not_seeded", "studio_a4_prepare_admission_drift")
    require(endpoint_admission.get("/api/v1/knowledge-assets/{asset_id}/retry") == "blocked_not_seeded", "studio_a4_retry_admission_drift")
    require(studio_a4.get("audit_sources", {}).get("KDS", "").startswith("authoritative_for_"), "studio_a4_kds_audit_authority_missing")

    combined = "\n".join(read(path) for path in (CONTROL_BOARD, SESSION_REGISTRY, LOOP_EVIDENCE, SUMMARY))
    for marker in (COORDINATION_ID, COORDINATOR_THREAD, ENVELOPE_SHA256, STUDIO_A4_ID, STUDIO_A4_SHA256, *LANE_THREADS.values(), *LANE_CHANGES.values()):
        require(marker in combined, f"governance_marker_missing:{marker}")
    feature = yaml.safe_load(read(FEATURE))
    require(feature.get("coordination", {}).get("id") == COORDINATION_ID, "feature_coordination_missing")
    require(feature.get("status") == "active", "feature_status_mismatch")
    require(feature.get("ui_product_first_control", {}).get("status_ceiling") == "partial", "feature_status_ceiling_mismatch")
    blockers = set(feature.get("blockers") or ())
    for blocker in (
        "gke001_three_lane_execution_handoffs_pending",
        "kds_p1_apply_blocked_by_dirty_worktree",
        "kds_stage_b_review_verified_waiting_studio_intake",
        "studio_intake_phase1_authorized_phase2_blocked_by_mmc_prepare_retry_policy_review",
        "unexpected_external_kds_local_mirror_write_requires_review",
        "brain_readonly_e2e_waiting_studio_intake",
        "mmc_delegation_and_human_confirmation_pending",
    ):
        require(blocker in blockers, f"feature_blocker_missing:{blocker}")
    require(feature.get("loop", {}).get("iteration", 0) >= 38, "feature_iteration_reconciliation_missing")
    require(feature.get("coordination", {}).get("studio_intake_amendment") == str(STUDIO_A4.relative_to(ROOT)), "studio_a4_feature_path_missing")
    require(feature.get("coordination", {}).get("studio_intake_amendment_sha256") == STUDIO_A4_SHA256, "studio_a4_feature_sha_missing")
    require(feature.get("coordination", {}).get("dispatch_status") == "studio_intake_a4_phase1_authorized_phase2_waiting_mmc_prepare_retry_policy", "dispatch_status_mismatch")
    require("dispatch_status: studio_intake_a4_phase1_authorized_phase2_waiting_mmc_prepare_retry_policy" in read(CONTROL_BOARD), "control_board_dispatch_missing")
    for marker in ("### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in read(LOOP_EVIDENCE), f"loop_marker_missing:{marker}")

    print(
        "gke001_three_lane_coordination=pass "
        f"coordination_id={COORDINATION_ID} lanes=3 unique_locks=3 "
        "brain_mode=freeze_and_wait kds_external_role_view_excluded=true "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        f"studio_a4={STUDIO_A4_ID} studio_a4_sha256={STUDIO_A4_SHA256} "
        "status=active/partial/not_complete dispatch_status=studio_intake_a4_phase1_authorized_phase2_waiting_mmc_prepare_retry_policy"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
