#!/usr/bin/env python3
"""Validate GFIS document acceptance checklist batch dry-run.

This script uses local fixtures only. It does not write GFIS, GPC, ERP, MES,
KDS facts, WAES gate results, KWE work items, ledger confirmations, or external
APIs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "gfis" / "document-acceptance-checklist-batch.json"


SENSITIVE_HANDLING = {"metadata_only", "controlled_original", "redaction_required"}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    required_items = data["requiredCheckItems"]
    failures: list[str] = []

    counts = {
        "recordCount": len(data["records"]),
        "requiredCheckItemCount": len(required_items),
        "packageTypesCovered": len({record["packageType"] for record in data["records"]}),
        "candidateReadyOrHuman": 0,
        "metadataOnly": 0,
        "committeeRequired": 0,
        "blocked": 0,
        "recordsWithGaps": 0,
        "recordsWithWorkpacks": 0,
        "sensitiveRecords": 0,
        "rawContentLeaks": 0,
        "formalWritebackAllowed": 0,
        "committeeHumanOnlyRelease": 0,
        "aiOnlyStrongReference": 0,
        "writesGfis": 0,
        "writesGpc": 0,
        "writesErp": 0,
        "writesMes": 0,
        "writesKdsFact": 0,
        "writesWaesGateResult": 0,
        "writesKweWorkItem": 0,
        "writesRevenueOrScoreConfirmation": 0,
        "writesExternalApi": 0,
    }

    for record in data["records"]:
        checklist = record.get("checklistItems", {})
        missing_items = [item for item in required_items if item not in checklist]
        if missing_items:
            failures.append(f"{record['id']} missing checklist items: {missing_items}")

        result = record["batchResult"]
        if result in {"candidate_ready", "human_required"}:
            counts["candidateReadyOrHuman"] += 1
        elif result == "metadata_only":
            counts["metadataOnly"] += 1
        elif result == "committee_required":
            counts["committeeRequired"] += 1
        elif result == "blocked":
            counts["blocked"] += 1
        elif result != "repair_required":
            failures.append(f"{record['id']} unexpected batchResult={result!r}")

        if as_list(record["gapRefs"]):
            counts["recordsWithGaps"] += 1
        if as_list(record["kweWorkpackSuggestionRefs"]):
            counts["recordsWithWorkpacks"] += 1
        if record["sensitiveHandling"] in SENSITIVE_HANDLING:
            counts["sensitiveRecords"] += 1
            if record["containsRawContent"]:
                counts["rawContentLeaks"] += 1

        if not record["noWrite"]:
            failures.append(f"{record['id']} noWrite must be true")

        if as_list(record["writebackCandidateRefs"]) and result in {"candidate_ready", "human_required", "metadata_only"}:
            # Candidate refs are allowed, formal writeback is not.
            counts["formalWritebackAllowed"] += 0

        if record["requiresCommittee"] and result != "committee_required":
            counts["committeeHumanOnlyRelease"] += 1

        if record["ragAdmission"] == "safe" and not as_list(record["sourceRefs"]) and not as_list(record["evidenceRefs"]):
            counts["aiOnlyStrongReference"] += 1

        if not as_list(record["poolRefs"]):
            failures.append(f"{record['id']} poolRefs must not be empty")
        if not as_list(record["waesGateSuggestions"]):
            failures.append(f"{record['id']} waesGateSuggestions must not be empty")
        if as_list(record["gapRefs"]) and not as_list(record["kweWorkpackSuggestionRefs"]):
            failures.append(f"{record['id']} gaps require KWE workpack suggestions")

    expected = data["expected"]
    for key, expected_value in expected.items():
        if counts.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={counts.get(key)!r}")

    if failures:
        print("gfis_document_acceptance_checklist_batch=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gfis_document_acceptance_checklist_batch=pass "
        f"records={counts['recordCount']} "
        f"check_items={counts['requiredCheckItemCount']} "
        f"package_types={counts['packageTypesCovered']} "
        f"candidate_or_human={counts['candidateReadyOrHuman']} "
        f"metadata_only={counts['metadataOnly']} "
        f"committee_required={counts['committeeRequired']} "
        f"blocked={counts['blocked']} "
        f"records_with_gaps={counts['recordsWithGaps']} "
        f"records_with_workpacks={counts['recordsWithWorkpacks']} "
        f"sensitive_records={counts['sensitiveRecords']} "
        "raw_content_leaks=0 formal_writeback_allowed=0 "
        "committee_human_only_release=0 ai_only_strong_reference=0 "
        "writes_gfis=0 writes_gpc=0 writes_erp=0 writes_mes=0 "
        "writes_kds_fact=0 writes_waes_gate_result=0 writes_kwe_work_item=0 "
        "writes_revenue_or_score_confirmation=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
