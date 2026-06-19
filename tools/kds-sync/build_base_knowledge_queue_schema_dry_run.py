#!/usr/bin/env python3
"""Build candidate-only schemas for base knowledge human and committee queues."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HUMAN_QUEUE = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json"
COMMITTEE_QUEUE = ROOT / "docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json"
HUMAN_SCHEMA_JSON = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.json"
HUMAN_SCHEMA_MD = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.md"
COMMITTEE_SCHEMA_JSON = ROOT / "docs/harness/evidence/base-knowledge-committee-review-schema-20260619.json"
COMMITTEE_SCHEMA_MD = ROOT / "docs/harness/evidence/base-knowledge-committee-review-schema-20260619.md"


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def preserve_frontmatter(path: Path, body: str) -> str:
    if not path.exists():
        return body
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return body
    end = text.find("\n---\n", 4)
    if end == -1:
        return body
    return text[: end + 5] + "\n" + body.lstrip("\n")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing source queue: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def field(name: str, kind: str, required: bool, description: str, enum: list[str] | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "name": name,
        "type": kind,
        "required": required,
        "description": description,
    }
    if enum:
        item["enum"] = enum
    return item


def human_fields() -> list[dict[str, Any]]:
    return [
        field("queueItemId", "string", True, "确认记录绑定的候选队列项 ID。"),
        field("sourceCandidateId", "string", True, "来自 DKS-044 的写回候选 ID。"),
        field("baseKnowledgeId", "string", True, "底座知识对象 ID。"),
        field("confirmingUnit", "string", True, "执行确认的人员或单位。"),
        field("confirmerRole", "string", True, "确认人角色。", ["source_owner", "project_owner", "kds_operator", "waes_reviewer", "other_authorized"]),
        field("sourceRefsReviewed", "array", True, "已核验的来源、证据或台账引用。"),
        field("factStatus", "string", True, "候选事实状态。", ["confirmed", "partially_confirmed", "rejected", "more_evidence_required"]),
        field("gapClosureOpinion", "string", True, "缺口处理意见。", ["keep_open", "ready_for_committee", "ready_for_writeback_candidate", "reject_candidate"]),
        field("evidenceLevelAfterReview", "string", True, "复核后的证据等级。", ["L0_unknown", "L1_claim", "L2_documented", "L3_verified", "L4_authoritative"]),
        field("sensitiveDataCheck", "string", True, "敏感数据处理结果。", ["clear", "masked", "contains_sensitive_needs_redaction"]),
        field("ragAdmissionOpinion", "string", True, "RAG 准入意见。", ["not_allowed", "limited_report_only", "candidate_after_more_evidence"]),
        field("nextAction", "string", True, "下一步动作。", ["request_more_evidence", "submit_to_committee", "prepare_writeback_candidate", "close_as_rejected"]),
        field("reviewNotes", "string", False, "人工确认说明。"),
    ]


def committee_fields() -> list[dict[str, Any]]:
    return [
        field("queueItemId", "string", True, "复核记录绑定的候选队列项 ID。"),
        field("sourceCandidateId", "string", True, "来自 DKS-044 的写回候选 ID。"),
        field("baseKnowledgeId", "string", True, "底座知识对象 ID。"),
        field("committeeSessionId", "string", True, "委员会复核会议或批次 ID。"),
        field("committeeMembers", "array", True, "参与复核成员清单。"),
        field("conflictOfInterestDeclared", "boolean", True, "是否完成利益冲突申明。"),
        field("severity", "string", True, "复核严重度。", ["general", "major"]),
        field("decisionMethod", "string", True, "裁决方式。", ["majority_vote", "chair_recorded_majority"]),
        field("decision", "string", True, "委员会裁决候选结果。", ["reject", "request_more_evidence", "approve_repair_candidate", "approve_penalty_candidate"]),
        field("scoreImpactCandidate", "string", True, "积分影响候选。", ["none", "knowledge_only_adjustment", "potential_value_adjustment", "formal_value_adjustment", "deduct_partial", "deduct_full"]),
        field("revenuePoolImpactCandidate", "string", True, "收益池影响候选。", ["none", "record_potential_only", "formal_income_after_receipt", "exclude_self_purchased_quota"]),
        field("writebackOpinion", "string", True, "写回意见。", ["do_not_write", "candidate_after_human_confirmation", "candidate_after_evidence_repair"]),
        field("appealAllowed", "boolean", True, "是否允许申诉。"),
        field("filingRequired", "boolean", True, "是否需要备案。"),
        field("reviewNotes", "string", False, "委员会复核说明。"),
    ]


def build_schema(queue: dict[str, Any], schema_type: str, fields: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schemaId": (
            "BKC-HUMAN-CONFIRMATION-SCHEMA-20260619"
            if schema_type == "human_confirmation_schema"
            else "BKC-COMMITTEE-REVIEW-SCHEMA-20260619"
        ),
        "sourceQueueEvidenceId": queue["evidenceId"],
        "sourceQueueType": queue["queueType"],
        "sourceQueueItemCount": queue["itemCount"],
        "currentRound": "GPCF-KDS-DKS-046",
        "schemaType": schema_type,
        "fieldCount": len(fields),
        "requiredFieldCount": sum(1 for item in fields if item["required"]),
        "fields": fields,
        "controls": {
            "candidateOnly": True,
            "createsConfirmationFact": False,
            "createsCommitteeDecision": False,
            "realKdsApiWrite": False,
            "waesWrite": False,
            "businessLedgerWrite": False,
            "settlementWrite": False,
            "ragAdmission": False,
            "acceptedOrIntegratedUpgrade": False,
        },
        "status": "schema_dry_run_only",
    }


def write_schema_json(schema: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_schema_md(schema: dict[str, Any], path: Path, title: str, purpose: str) -> None:
    rows = [
        [
            item["name"],
            item["type"],
            str(item["required"]).lower(),
            ", ".join(item.get("enum", [])) or "-",
            item["description"],
        ]
        for item in schema["fields"]
    ]
    md = f"# {title}\n\n"
    md += "日期：2026-06-19\n\n"
    md += "状态：`schema_dry_run_only`\n\n"
    md += f"{purpose}\n\n"
    md += "## Summary\n\n"
    md += f"- schema_id：`{schema['schemaId']}`\n"
    md += f"- source_queue_evidence_id：`{schema['sourceQueueEvidenceId']}`\n"
    md += f"- source_queue_type：`{schema['sourceQueueType']}`\n"
    md += f"- source_queue_item_count：`{schema['sourceQueueItemCount']}`\n"
    md += f"- field_count：`{schema['fieldCount']}`\n"
    md += f"- required_field_count：`{schema['requiredFieldCount']}`\n\n"
    md += "## Fields\n\n"
    md += table(["field", "type", "required", "enum", "description"], rows)
    md += "\n\n"
    md += "## Controls\n\n"
    md += table(["control", "value"], [[key, str(value).lower()] for key, value in schema["controls"].items()])
    md += "\n\n"
    md += "## Boundary\n\n"
    md += "- This file defines schema only and does not create human confirmation facts.\n"
    md += "- This file defines schema only and does not create committee decisions.\n"
    md += "- No real KDS API, WAES, GFIS, GPC, PVAOS, finance, settlement, RAG admission, or production write is performed.\n"
    md += "- Any future use of this schema still requires explicit human or committee action and a separate controlled evidence record.\n"
    path.write_text(preserve_frontmatter(path, md), encoding="utf-8")


def main() -> int:
    human_queue = load_json(HUMAN_QUEUE)
    committee_queue = load_json(COMMITTEE_QUEUE)
    human_schema = build_schema(human_queue, "human_confirmation_schema", human_fields())
    committee_schema = build_schema(committee_queue, "committee_review_schema", committee_fields())

    write_schema_json(human_schema, HUMAN_SCHEMA_JSON)
    write_schema_json(committee_schema, COMMITTEE_SCHEMA_JSON)
    write_schema_md(
        human_schema,
        HUMAN_SCHEMA_MD,
        "Base Knowledge Human Confirmation Schema",
        "This schema defines the fields required for future manual confirmation of non-hard-stop base knowledge candidates.",
    )
    write_schema_md(
        committee_schema,
        COMMITTEE_SCHEMA_MD,
        "Base Knowledge Committee Review Schema",
        "This schema defines the fields required for future committee review of hard-stop base knowledge candidates.",
    )

    print(
        "base_knowledge_queue_schema_dry_run=pass "
        f"human_schema_fields={human_schema['fieldCount']} "
        f"committee_schema_fields={committee_schema['fieldCount']} "
        f"human_source_items={human_schema['sourceQueueItemCount']} "
        f"committee_source_items={committee_schema['sourceQueueItemCount']} "
        "status=schema_dry_run_only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
