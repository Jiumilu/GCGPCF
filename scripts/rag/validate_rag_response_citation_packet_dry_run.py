#!/usr/bin/env python3
"""Validate RAG response citation packet dry-run.

This validator reads local OKF, shared type and fixture files only. It does not
run retrieval, call model providers, write KDS facts, create WAES gate results,
create KWE work items, write business systems, or call external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "rag-response-citation-packet-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "rag-response-citation-packet.ts"
FIXTURE = ROOT / "fixtures" / "rag" / "response-citation-packet-dry-run.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def camel_from_snake(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]
    packet = fixture["packet"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("RagAssistantSurface") != policy["assistant_surfaces"]:
        failures.append("RagAssistantSurface union does not match policy")
    if union_literals("RagAnswerMode") != policy["answer_modes"]:
        failures.append("RagAnswerMode union does not match policy")

    for field in policy["minimum_packet_fields"]:
        if camel_from_snake(field) not in packet:
            failures.append(f"packet missing field: {field}")
    for citation in packet["citations"]:
        for field in policy["minimum_citation_fields"]:
            if camel_from_snake(field) not in citation:
                failures.append(f"{citation['citationId']} missing field: {field}")
        if citation["citationStrength"] == "L0":
            failures.append(f"L0 citation leaked: {citation['citationId']}")
        if citation["ragAdmission"] == "blocked":
            failures.append(f"blocked RAG citation leaked: {citation['citationId']}")
        if citation["metadataOnly"] and not citation["redacted"]:
            failures.append(f"metadata-only citation must be redacted: {citation['citationId']}")

    missing_notices = set(policy["required_boundary_notices"]) - set(packet["boundaryNotices"])
    if missing_notices:
        failures.append(f"missing boundary notices: {sorted(missing_notices)}")
    if packet["answerMode"] in {"strong_answer", "business_assist"} and packet["missingEvidenceRefs"]:
        failures.append("strong or business assist answer cannot have missing evidence")

    checks = {
        "assistantSurfaceCount": len(policy["assistant_surfaces"]),
        "answerModeCount": len(policy["answer_modes"]),
        "minimumPacketFieldCount": len(policy["minimum_packet_fields"]),
        "minimumCitationFieldCount": len(policy["minimum_citation_fields"]),
        "requiredBoundaryNoticeCount": len(policy["required_boundary_notices"]),
        "citationCount": len(packet["citations"]),
        "blockedCandidateCount": len(fixture["blockedCandidates"]),
        "highestCitationStrength": packet["highestCitationStrength"],
        "metadataOnlyCitationCount": sum(1 for item in packet["citations"] if item["metadataOnly"]),
        "l0CitationCount": sum(1 for item in packet["citations"] if item["citationStrength"] == "L0"),
        "blockedRagCitationCount": sum(1 for item in packet["citations"] if item["ragAdmission"] == "blocked"),
        "missingEvidenceCount": len(packet["missingEvidenceRefs"]),
        "l0CitationAllowed": hard["l0_citation_allowed"],
        "metadataOnlyRawContentAllowed": hard["metadata_only_raw_content_allowed"],
        "l3RequiresBoundaryNotice": hard["l3_requires_boundary_notice"],
        "l4L5AutoWritebackAllowed": hard["l4_l5_auto_writeback_allowed"],
        "l5ReplacesHumanOrCommittee": hard["l5_replaces_human_or_committee"],
        "missingEvidenceAllowsStrongAnswer": hard["missing_evidence_allows_strong_answer"],
        "blockedRagAllowedInPacket": hard["blocked_rag_allowed_in_packet"],
        "t5AiOnlyAllowedAsFact": hard["t5_ai_only_allowed_as_fact"],
        "noAclAllowedInPacket": hard["no_acl_allowed_in_packet"],
        "packetPassIsFormalFact": hard["packet_pass_is_formal_fact"],
        "writesKdsFact": no_write["writes_kds_fact"],
        "writesWaesGateResult": no_write["writes_waes_gate_result"],
        "writesKweWorkItem": no_write["writes_kwe_work_item"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueOrScoreConfirmation": no_write["writes_revenue_or_score_confirmation"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("rag_response_citation_packet_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "rag_response_citation_packet_dry_run=pass "
        f"assistant_surfaces={checks['assistantSurfaceCount']} "
        f"answer_modes={checks['answerModeCount']} "
        f"packet_fields={checks['minimumPacketFieldCount']} "
        f"citation_fields={checks['minimumCitationFieldCount']} "
        f"citations={checks['citationCount']} highest={checks['highestCitationStrength']} "
        "l0_citations=0 blocked_rag_citations=0 metadata_only_citations=1 "
        "missing_evidence=0 writes_kds_fact=0 writes_waes_gate_result=0 "
        "writes_kwe_work_item=0 writes_business_system=0 "
        "writes_revenue_or_score_confirmation=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
