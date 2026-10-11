#!/usr/bin/env python3
"""Validate the XWAIL City/Spatial Profile schema-candidate review request package（pending 态）。"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/XWAIL/evidence/xwail-city-profile-schema-review-request-20261011.json"
EVIDENCE_MD = ROOT / "docs/harness/XWAIL/evidence/xwail-city-profile-schema-review-request-20261011.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-XWAIL-CITY-PROFILE-SCHEMA-REVIEW-001.md"
KDS_ROOT = ROOT.parent / "GlobalCloud KDS"
KDS_ATTACHMENTS = [
    "工业绿链/管理文件/方案与规划/2026-10-11_XWAIL_CityProfile范围定义与Schema候选草案_v0.1.md",
    "工业绿链/图谱/ontology/city-profile-poc/validate_city_profile.py",
    "工业绿链/图谱/ontology/city-profile-poc/verify_output.txt",
    "工业绿链/图谱/ontology/registry_vocab_review_request_v0.1.md",
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
        "last_reviewed: 2026-10-11",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "XWAIL-CITY-PROFILE-SCHEMA-REVIEW-REQUEST-20261011",
            "invalid evidence id")
    require(evidence.get("status") in ("request_submitted_pending_governance_review", "review_accepted"),
            "invalid status")
    require(evidence.get("scope") == "xwail_city_profile_schema_candidate_review_request_only",
            "invalid scope")
    require(evidence.get("requested_decision") == "review_and_settle_xwail_city_profile_schema_candidate",
            "requested decision mismatch")
    decision = evidence.get("current_decision")
    require(decision in ("pending_governance_review", "accepted"), f"unknown decision state: {decision}")
    if decision == "accepted":
        record = evidence.get("decision_record", {})
        require(record.get("decision") == "accepted" and record.get("date") and record.get("authority"),
                "accepted 状态需 decision_record（decision/date/authority）")
    require(evidence.get("upstream_decision") == "accepted", "upstream decision must be accepted")

    pre = evidence.get("admission_preconditions", {})
    for key in [
        "upstream_request_accepted",
        "draft_final_for_submission",
        "poc_verified_5_of_5",
        "core_readside_alignment_done",
        "no_xwail_repo_modification",
        "candidate_boundary_retained",
    ]:
        require(pre.get(key) is True, f"precondition must be true: {key}")

    boundary = evidence.get("requested_boundary", {})
    require(len(boundary.get("allowed_after_settlement", [])) >= 2, "allowed list missing")
    for item in [
        "xwail_repo_direct_modification_outside_governance",
        "waes_publication_claim",
        "production_ready_claim",
        "customer_acceptance_claim",
    ]:
        require(item in set(boundary.get("forbidden", [])), f"forbidden item missing: {item}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("submitted") is True, "submitted gate must be true")
    if decision == "accepted":
        require(gates.get("governance_reviewed") is True, "accepted 状态 governance_reviewed 必须为 true")
        require(gates.get("accepted") is True, "accepted 状态 accepted 门必须为 true")
        for key in ["waes_authorized", "published", "integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")
    else:
        for key in ["governance_reviewed", "waes_authorized", "published", "accepted",
                    "integrated", "production_ready"]:
            require(gates.get(key) is False, f"gate must be false: {key}")

    phrases = [
        "XWAIL-CITY-PROFILE-SCHEMA-REVIEW-REQUEST-20261011",
        "review_and_settle_xwail_city_profile_schema_candidate",
        "request_package_generated | true",
        "submitted | true",
        "waes_authorized | false",
        "production_ready | false",
        "定版送审",
    ]
    if decision == "accepted":
        phrases += ["governance_reviewed | true", "accepted | true", "受理记录"]
    else:
        phrases += ["pending_governance_review", "governance_reviewed | false", "accepted | false"]
    for phrase in phrases:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_xwail_city_profile_schema_review_request.py" in loop_round,
            "loop round missing validator")
    require("review_and_settle" in loop_round, "loop round missing requested decision")

    # KDS 侧附件在位检查（缺失仅 WARN，不改变退出码）
    warnings: list[str] = []
    if not KDS_ROOT.exists():
        warnings.append(f"KDS root not reachable: {KDS_ROOT}")
    else:
        for rel in KDS_ATTACHMENTS:
            if not (KDS_ROOT / rel).exists():
                warnings.append(f"KDS attachment missing: {rel}")

    for w in warnings:
        print(f"WARN: {w}")
    print(
        "xwail_city_profile_schema_review_request=pass "
        "requested_decision=review_and_settle_xwail_city_profile_schema_candidate "
        f"current_decision={decision} submitted=true "
        f"governance_reviewed={'true' if decision == 'accepted' else 'false'} "
        f"accepted={'true' if decision == 'accepted' else 'false'} integrated=false production_ready=false "
        f"kds_attachments_checked={len(KDS_ATTACHMENTS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
