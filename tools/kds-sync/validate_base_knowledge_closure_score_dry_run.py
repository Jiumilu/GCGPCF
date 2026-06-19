#!/usr/bin/env python3
"""Dry-run scorer for base knowledge closure candidates.

This tool validates local fixtures only. It does not call KDS, WAES, GFIS,
GPC, PVAOS, settlement services, RAG indexes, or any external API.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "docs/harness/evidence/base-knowledge-closure-score-fixtures.json"

KDS_11_POOLS = {
    "订单池",
    "运力池",
    "产能池",
    "资金池",
    "政策池",
    "装备池",
    "数据池",
    "能源池",
    "原料池",
    "人才池",
    "场景池",
}
OPTIONAL_ARRAY_FIELDS = {"enhancedLedgerRefs", "sourceRefs", "oneVoteVetoFlags"}
NUMERIC_FIELDS = {
    "statusCoverageRate",
    "dqScore",
    "evidencePassRate",
    "consistencyRate",
    "automationEffectivenessRate",
    "writebackClosureRate",
}
REQUIRED_FIELDS = {
    "baseKnowledgeId",
    "sourceProject",
    "kdsPoolRefs",
    *NUMERIC_FIELDS,
    "oneVoteVetoFlags",
}
ALLOWED_FIELDS = {
    *REQUIRED_FIELDS,
    *OPTIONAL_ARRAY_FIELDS,
    "evidenceLevel",
    "humanReviewStatus",
    "waesRecordStatus",
    "settlementStatus",
    "ragInclude",
}
FORBIDDEN_OUTPUT_MARKERS = {
    "real_kds_api_synced",
    "rag_admitted",
    "command_center_strong_reference_allowed",
    "business_ledger_written",
    "settlement_completed",
    "bounty_published",
    "committee_decision_completed",
    "accepted",
    "integrated",
}


class ValidationError(Exception):
    """Input structure failure."""


class CalculationMismatch(Exception):
    """Fixture expectation failure."""


class UnauthorizedOutput(Exception):
    """Dry-run output crossed an authority boundary."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def as_list(value: Any, field: str) -> list[Any]:
    require(isinstance(value, list), f"{field} must be an array")
    return value


def validate_input(item: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - item.keys())
    require(not missing, f"missing required fields: {','.join(missing)}")
    extra = sorted(set(item.keys()) - ALLOWED_FIELDS)
    require(not extra, f"additional properties are not allowed: {','.join(extra)}")
    require(isinstance(item["baseKnowledgeId"], str) and item["baseKnowledgeId"], "baseKnowledgeId must be a non-empty string")
    require(isinstance(item["sourceProject"], str) and item["sourceProject"], "sourceProject must be a non-empty string")

    kds_refs = as_list(item["kdsPoolRefs"], "kdsPoolRefs")
    unknown_pools = sorted(str(ref) for ref in kds_refs if ref not in KDS_11_POOLS)
    require(not unknown_pools, f"unknown KDS pool refs: {','.join(unknown_pools)}")
    for field in OPTIONAL_ARRAY_FIELDS:
        if field in item:
            as_list(item[field], field)

    for field in NUMERIC_FIELDS:
        value = item[field]
        require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{field} must be numeric")
        require(0 <= value <= 100, f"{field} must be between 0 and 100")

    if "ragInclude" in item:
        require(isinstance(item["ragInclude"], bool), "ragInclude must be boolean")


def calculate_rate(item: dict[str, Any]) -> float:
    value = (
        item["statusCoverageRate"] * 0.20
        + item["dqScore"] * 0.25
        + item["evidencePassRate"] * 0.20
        + item["consistencyRate"] * 0.15
        + item["automationEffectivenessRate"] * 0.10
        + item["writebackClosureRate"] * 0.10
    )
    return round(value + 1e-9, 2)


def band_for(rate: float) -> str:
    if rate >= 85:
        return "safe_reuse_candidate"
    if rate >= 70:
        return "limited_report_candidate"
    if rate >= 60:
        return "repair_candidate"
    if rate >= 50:
        return "return_for_source"
    return "blocked_or_invalid"


def hard_stop_reasons(item: dict[str, Any], initial_band: str) -> list[str]:
    reasons: list[str] = []
    kds_refs = item.get("kdsPoolRefs", [])
    enhanced_refs = item.get("enhancedLedgerRefs", [])
    source_refs = item.get("sourceRefs", [])
    veto_flags = item.get("oneVoteVetoFlags", [])

    if not kds_refs:
        reasons.append("HS-NO-KDS-POOL")
    if enhanced_refs and not kds_refs:
        reasons.append("VETO-LEDGER-ORPHAN")
    if not source_refs and item.get("evidencePassRate", 0) > 0:
        reasons.append("VETO-NO-SOURCE")
    for flag in veto_flags:
        if flag in {
            "VETO-AI-AS-FACT",
            "VETO-REVENUE-MISCLAIM",
            "VETO-ORDER-MISCLAIM",
            "VETO-KDS-API-CLAIM",
            "VETO-UNAUTHORIZED-SETTLEMENT",
        }:
            reasons.append(str(flag))
    if item.get("ragInclude") is True and initial_band != "safe_reuse_candidate":
        reasons.append("HS-RAG-MISMATCH")
    settlement_status = item.get("settlementStatus", "prohibited_before_acceptance")
    human_review_status = item.get("humanReviewStatus", "pending")
    if settlement_status != "prohibited_before_acceptance" and human_review_status not in {"accepted", "confirmed"}:
        reasons.append("HS-SETTLEMENT-MISMATCH")

    return sorted(set(reasons))


def writeback_candidates(item: dict[str, Any], reasons: list[str]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    if "VETO-NO-SOURCE" in reasons:
        candidates.append({"target": "sourceRefs", "reason": "source_refs_missing", "status": "candidate_only"})
    if item["evidencePassRate"] < 70:
        candidates.append({"target": "evidencePassRate", "reason": "evidence_level_below_reuse_threshold", "status": "candidate_only"})
    if item["automationEffectivenessRate"] == 0:
        candidates.append({"target": "automationEffectivenessRate", "reason": "automation_not_effective_yet", "status": "candidate_only"})
    if item["writebackClosureRate"] < 60:
        candidates.append({"target": "writebackClosureRate", "reason": "gap_writeback_not_closed", "status": "candidate_only"})
    return candidates


def uses_for(band: str, reasons: list[str]) -> tuple[list[str], list[str]]:
    forbidden = {
        "rag_strong_reference",
        "command_center_strong_reference",
        "business_ledger_write",
        "settlement",
        "revenue_pool",
    }
    if reasons:
        return ["committee_review_candidate"], sorted(forbidden)
    if band == "safe_reuse_candidate":
        return ["safe_reuse_candidate", "limited_report_candidate"], sorted({"business_ledger_write", "settlement", "revenue_pool"})
    if band == "limited_report_candidate":
        return ["limited_report_candidate"], sorted(forbidden)
    if band == "repair_candidate":
        return ["repair", "bounty_candidate", "manual_confirmation_candidate"], sorted(forbidden)
    if band == "return_for_source":
        return ["source_repair_candidate"], sorted(forbidden)
    return ["blocked_review_candidate"], sorted(forbidden)


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    validate_input(item)
    rate = calculate_rate(item)
    initial_band = band_for(rate)
    reasons = hard_stop_reasons(item, initial_band)
    decision_band = "blocked_or_invalid" if reasons or item.get("oneVoteVetoFlags") else initial_band
    allowed, forbidden = uses_for(decision_band, reasons)
    result = {
        "mode": "dry_run",
        "status": "candidate_only" if not reasons else "blocked",
        "baseKnowledgeId": item["baseKnowledgeId"],
        "calculatedClosureRate": rate,
        "decisionBand": decision_band,
        "hardStop": bool(reasons),
        "hardStopReasons": reasons,
        "allowedUse": allowed,
        "forbiddenUse": forbidden,
        "writebackCandidates": writeback_candidates(item, reasons),
        "auditMessages": [
            "dry-run only; no real KDS, WAES, GFIS, GPC, PVAOS, RAG, settlement, or business ledger write",
            "hard-stop rules take precedence over score bands",
        ],
    }
    assert_authorized_output(result)
    return result


def assert_authorized_output(result: dict[str, Any]) -> None:
    text = json.dumps(result, ensure_ascii=False)
    hits = sorted(marker for marker in FORBIDDEN_OUTPUT_MARKERS if marker in text)
    if hits:
        raise UnauthorizedOutput(f"forbidden output markers: {','.join(hits)}")


def validate_fixture_suite(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    fixtures = payload.get("fixtures", [])
    if not isinstance(fixtures, list) or not fixtures:
        raise ValidationError("fixture file must contain non-empty fixtures array")

    results: list[dict[str, Any]] = []
    expected_hard_stops = 0
    for fixture in fixtures:
        fixture_id = fixture.get("fixtureId", "")
        item = fixture.get("input", {})
        expected = fixture.get("expected", {})
        result = score_item(item)
        if result["decisionBand"] != expected.get("decisionBand"):
            raise CalculationMismatch(f"{fixture_id}: expected decisionBand {expected.get('decisionBand')} got {result['decisionBand']}")
        if result["hardStop"] != expected.get("hardStop", False):
            raise CalculationMismatch(f"{fixture_id}: expected hardStop {expected.get('hardStop')} got {result['hardStop']}")
        if result["hardStop"]:
            expected_hard_stops += 1
        expected_rate = expected.get("calculatedClosureRate")
        if expected_rate is not None and result["calculatedClosureRate"] != expected_rate:
            raise CalculationMismatch(f"{fixture_id}: expected rate {expected_rate} got {result['calculatedClosureRate']}")
        for reason in expected.get("hardStopReasons", []):
            if reason not in result["hardStopReasons"]:
                raise CalculationMismatch(f"{fixture_id}: missing hard-stop reason {reason}")
        results.append({"fixtureId": fixture_id, "result": result})

    return {
        "gate": "pass",
        "mode": "fixture_suite",
        "fixtures": len(results),
        "expectedHardStops": expected_hard_stops,
        "results": results,
        "boundary": {
            "realKdsApiWrite": False,
            "waesWrite": False,
            "businessLedgerWrite": False,
            "settlementWrite": False,
            "ragAdmission": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", default=str(DEFAULT_FIXTURE), help="fixture suite JSON path")
    parser.add_argument("--input", help="single BaseKnowledgeClosureScoreInput JSON path")
    args = parser.parse_args()

    try:
        if args.input:
            result = score_item(load_json(Path(args.input)))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 2 if result["hardStop"] else 0
        suite = validate_fixture_suite(Path(args.fixture))
        print(json.dumps(suite, ensure_ascii=False, indent=2))
        return 0
    except ValidationError as exc:
        print(json.dumps({"gate": "fail", "exitCode": 1, "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    except CalculationMismatch as exc:
        print(json.dumps({"gate": "fail", "exitCode": 3, "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 3
    except UnauthorizedOutput as exc:
        print(json.dumps({"gate": "fail", "exitCode": 4, "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
