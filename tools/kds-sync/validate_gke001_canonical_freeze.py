#!/usr/bin/env python3
"""Validate the isolated GKE-001 canonical v0.1 candidate freeze."""

from __future__ import annotations

import argparse
import copy
import hashlib
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / "features/active/F-013-knowledge-asset-model-system/artifacts/gke-001-canonical-v0.1-76ac-freeze-20260821.yaml"
CANDIDATE_SHA = "76ac8d37d61e8904edd8383c246bcadbe5bec0197a50d4bb90085f6d2308e9bf"
HISTORICAL_SHA = "8537f3acda011610c1cb67ec13ea690d42a16b5d5ace030ab31762da8969a1de"


class FreezeError(ValueError):
    """Raised when the candidate freeze loses its controlled boundary."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise FreezeError(reason)


def sha256(path: Path) -> str:
    require(path.is_file(), f"missing_file:{path.relative_to(ROOT)}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_freeze() -> dict[str, Any]:
    require(FREEZE.is_file(), f"missing_file:{FREEZE.relative_to(ROOT)}")
    data = yaml.safe_load(FREEZE.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "freeze_root_not_mapping")
    freeze = data.get("canonical_v01_candidate_freeze")
    require(isinstance(freeze, dict), "freeze_payload_missing")
    return freeze


def validate(freeze: dict[str, Any]) -> None:
    require(freeze.get("id") == "GKE-001-CANONICAL-FREEZE-20260821-001", "freeze_id_mismatch")
    require(freeze.get("engineering_domain") == "GKE-001", "engineering_domain_mismatch")
    require(freeze.get("feature") == "F-013", "feature_mismatch")
    decision = freeze.get("decision")
    require(isinstance(decision, dict), "decision_missing")
    require(decision.get("revision") == "v0.1", "revision_mismatch")
    require(decision.get("selected_candidate_manifest_sha256") == CANDIDATE_SHA, "candidate_declaration_mismatch")
    require(decision.get("preserves_historical_anchor_sha256") == HISTORICAL_SHA, "historical_declaration_mismatch")
    require(decision.get("status") == "controlled_candidate_pending_independent_review", "candidate_status_mismatch")
    require(decision.get("release_unblocked") is False, "release_unblock_boundary_drift")

    controls = freeze.get("current_control_plane")
    require(isinstance(controls, list) and len(controls) == 7, "control_plane_scope_mismatch")
    for item in controls:
        require(isinstance(item, dict), "control_plane_entry_not_mapping")
        path = ROOT / str(item.get("path") or "")
        require(item.get("sha256") == sha256(path), f"control_plane_hash_mismatch:{path.relative_to(ROOT)}")
    require(controls[0].get("path") == "okf/knowledge-asset-contract-manifest.yaml", "manifest_not_first_control")
    require(controls[0].get("sha256") == CANDIDATE_SHA, "manifest_candidate_hash_mismatch")

    anchors = freeze.get("historical_anchors")
    require(isinstance(anchors, list) and len(anchors) == 3, "historical_anchor_scope_mismatch")
    for item in anchors:
        require(isinstance(item, dict), "historical_anchor_not_mapping")
        path = ROOT / str(item.get("path") or "")
        require(item.get("sha256") == sha256(path), f"historical_anchor_hash_mismatch:{path.relative_to(ROOT)}")
        require(HISTORICAL_SHA in path.read_text(encoding="utf-8"), f"historical_anchor_token_missing:{path.relative_to(ROOT)}")

    review = freeze.get("independent_review")
    require(isinstance(review, dict), "independent_review_missing")
    require(review.get("required") is True, "independent_review_not_required")
    require(review.get("status") == "independently_reviewed", "independent_review_status_mismatch")
    require(review.get("review_turn_id") == "01a021c3-27f5-7681-9649-e2e27fd23f97", "independent_review_turn_mismatch")
    require(
        review.get("classification") == "canonical_v01_76ac_controlled_candidate_freeze_independently_reviewed_release_still_blocked",
        "independent_review_classification_mismatch",
    )
    authorization = freeze.get("authorization")
    require(isinstance(authorization, dict), "authorization_missing")
    require(authorization.get("canonical_candidate_freeze_record") is True, "freeze_record_not_authorized")
    for key, value in authorization.items():
        if key != "canonical_candidate_freeze_record":
            require(value is False, f"authorization_boundary_drift:{key}")
    status = freeze.get("status")
    require(status == {"engineering": "active", "cross_project": "partial", "completion": "not_complete"}, "status_boundary_drift")


def run_self_test(freeze: dict[str, Any]) -> None:
    bad = copy.deepcopy(freeze)
    bad["decision"]["selected_candidate_manifest_sha256"] = "0" * 64
    try:
        validate(bad)
    except FreezeError as error:
        require(str(error) == "candidate_declaration_mismatch", "self_test_wrong_failure")
    else:
        raise FreezeError("self_test_candidate_drift_not_detected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        freeze = load_freeze()
        validate(freeze)
        if args.self_test:
            run_self_test(freeze)
    except (FreezeError, OSError, TypeError, yaml.YAMLError) as error:
        print(f"gke001_canonical_freeze=fail reason={error}")
        return 1
    print(
        "gke001_canonical_freeze=pass "
        f"candidate_sha256={CANDIDATE_SHA} historical_anchor_sha256={HISTORICAL_SHA} "
        f"independent_review=independently_reviewed self_test={'pass' if args.self_test else 'not_run'} "
        "status=active_partial_not_complete"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
