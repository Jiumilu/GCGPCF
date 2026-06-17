#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "docs/harness/sop-e2e/evidence/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-release-attempt-hard-stop-audit.json"
DOC_PATH = ROOT / "docs/harness/sop-e2e/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-release-attempt-hard-stop-audit.md"
SOURCE_PATH = ROOT / "docs/harness/sop-e2e/evidence/liaoning-yuanhang-runtime-document-evidence-slot-owner-response-submission-package-quarantine-scanner.json"
API_PATH = ROOT / "gcfis_custom/gcfis_custom/api.py"

EXPECTED_BLOCKERS = {
    "submission_package_missing",
    "submission_package_structure_not_valid",
    "source_of_record_live_proof_missing",
    "manual_authorization_envelope_missing",
    "anti_pollution_declaration_missing",
    "quarantine_review_not_available",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return value


def install_fake_frappe() -> None:
    frappe = types.SimpleNamespace()
    frappe.whitelist = lambda *args, **kwargs: (lambda func: func) if not args else args[0]

    class FrappeException(Exception):
        pass

    def throw(message: str, *args: Any, **kwargs: Any) -> None:
        raise FrappeException(message)

    frappe.throw = throw
    frappe.FrappeException = FrappeException
    sys.modules["frappe"] = frappe


def load_api_module():
    install_fake_frappe()
    spec = importlib.util.spec_from_file_location("gfis_api_submission_package_release_attempt_hard_stop_audit", API_PATH)
    require(spec is not None and spec.loader is not None, "cannot load api module spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules["gfis_api_submission_package_release_attempt_hard_stop_audit"] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    audit = load_json(AUDIT_PATH)
    source = load_json(SOURCE_PATH)
    require(DOC_PATH.exists(), f"missing doc: {DOC_PATH.relative_to(ROOT)}")
    doc = DOC_PATH.read_text(encoding="utf-8")

    expected_counts = {
        "runtime_objects": 12,
        "proof_slots": 62,
        "expected_submission_packages": 62,
        "attempted_release_count": 62,
        "hard_stop_count": 62,
        "total_blocker_count": 372,
        "submission_packages_found": 0,
        "structure_valid_submission_packages": 0,
        "quarantine_candidates": 0,
        "quarantined_packages": 0,
        "accepted_packages": 0,
        "rejected_packages": 0,
        "release_allowed": 0,
        "review_queue": 0,
        "runtime_intake": 0,
        "waes_review": 0,
        "verified": 0,
    }
    require(audit.get("subject") == "GFIS运行层", "subject must be GFIS runtime layer")
    require(audit.get("round_id") == "GFIS-RUNTIME-SOP-E2E-162", "round id mismatch")
    require(audit.get("source_quarantine_scanner_round_id") == "GFIS-RUNTIME-SOP-E2E-161", "source quarantine round mismatch")
    require(source.get("submission_packages_found") == 0, "source scanner must still find zero packages")
    require(audit.get("runtime_sop_e2e") == "repair_required", "runtime SOP must stay repair_required")
    require(
        audit.get("state") == "owner_response_submission_package_release_attempt_hard_stopped_no_submission_packages",
        "state mismatch",
    )
    for key, value in expected_counts.items():
        require(audit.get(key) == value, f"count mismatch: {key}")

    items = audit.get("audit_items")
    require(isinstance(items, list) and len(items) == 62, "must include 62 audit items")
    objects = set()
    for item in items:
        require(isinstance(item, dict), "audit item must be object")
        objects.add(item.get("object"))
        require(item.get("submission_package_id"), "submission package id missing")
        require(item.get("handoff_id"), "handoff id missing")
        require(item.get("response_id"), "response id missing")
        require(item.get("transition_id"), "transition id missing")
        require(item.get("slot_id"), "slot id missing")
        require(item.get("attempted_release") is True, "attempted_release must be true")
        require(item.get("attempted_review_queue") is True, "attempted_review_queue must be true")
        require(item.get("attempted_runtime_intake") is True, "attempted_runtime_intake must be true")
        require(item.get("attempted_waes_review") is True, "attempted_waes_review must be true")
        require(item.get("hard_stop") is True, "hard_stop must be true")
        require(item.get("blocker_count") == 6, "blocker count mismatch")
        require(set(item.get("blockers", [])) == EXPECTED_BLOCKERS, "blockers mismatch")
        require(item.get("release_allowed") is False, "release must not be allowed")
        require(item.get("review_queue_allowed") is False, "review queue must not be allowed")
        require(item.get("runtime_intake_allowed") is False, "runtime intake must not be allowed")
        require(item.get("waes_review_allowed") is False, "WAES review must not be allowed")
        require(item.get("verified_artifact_allowed") is False, "verified artifact must not be allowed")
        require(item.get("state") == "release_attempt_hard_stopped_no_submission_package", "item state mismatch")
    require(len(objects) == 12, "audit must cover 12 runtime objects")

    for section in ["external_runtime_boundary", "guardrails"]:
        value = audit.get(section)
        require(isinstance(value, dict), f"{section} must be object")
        for key, flag in value.items():
            require(flag is False, f"{section}.{key} must remain false")

    for phrase in [
        "expected_submission_packages: `62`",
        "attempted_release_count: `62`",
        "hard_stop_count: `62`",
        "total_blocker_count: `372`",
        "submission_packages_found: `0`",
        "release_allowed: `0`",
        "review_queue: `0`",
        "runtime_intake: `0`",
        "runtime_sop_e2e: `repair_required`",
        "现代精工 OEM",
        "source-of-record live proof",
        "Hermes 仍为只读边界",
    ]:
        require(phrase in doc, f"Markdown missing phrase: {phrase}")

    api = load_api_module()
    require(
        hasattr(api, "get_runtime_liaoning_yuanhang_runtime_document_evidence_slot_owner_response_submission_package_release_attempt_hard_stop_audit"),
        "API function missing",
    )
    api_result = api.get_runtime_liaoning_yuanhang_runtime_document_evidence_slot_owner_response_submission_package_release_attempt_hard_stop_audit(audit)
    require(api_result.get("ok") is True, "API result must be ok")
    require(api_result.get("action_level") == "只读", "API action must be read-only")
    require(api_result.get("state") == "owner_response_submission_package_release_attempt_hard_stopped_no_submission_packages", "API state mismatch")
    require(api_result.get("runtime_sop_e2e") == "repair_required", "API runtime SOP mismatch")
    for key, value in expected_counts.items():
        require(api_result.get(key) == value, f"API count mismatch: {key}")

    print(
        "liaoning_yuanhang_runtime_document_evidence_slot_owner_response_submission_package_release_attempt_hard_stop_audit=pass "
        "objects=12 proof_slots=62 expected_submission_packages=62 attempted_release=62 "
        "hard_stops=62 blockers=372 submission_packages_found=0 structure_valid_submission_packages=0 "
        "quarantine_candidates=0 quarantined_packages=0 accepted_packages=0 rejected_packages=0 "
        "release_allowed=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "state=owner_response_submission_package_release_attempt_hard_stopped_no_submission_packages runtime_sop_e2e=repair_required"
    )


if __name__ == "__main__":
    main()
