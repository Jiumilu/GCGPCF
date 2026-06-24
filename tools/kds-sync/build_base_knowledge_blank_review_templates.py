#!/usr/bin/env python3
"""Build blank review templates for base knowledge confirmation queues."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HUMAN_SCHEMA = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-schema-20260619.json"
COMMITTEE_SCHEMA = ROOT / "docs/harness/evidence/base-knowledge-committee-review-schema-20260619.json"
HUMAN_QUEUE = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json"
COMMITTEE_QUEUE = ROOT / "docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json"
HUMAN_TEMPLATE_JSON = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.json"
HUMAN_TEMPLATE_MD = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md"
COMMITTEE_TEMPLATE_JSON = ROOT / "docs/harness/evidence/base-knowledge-committee-review-template-20260619.json"
COMMITTEE_TEMPLATE_MD = ROOT / "docs/harness/evidence/base-knowledge-committee-review-template-20260619.md"

DOC_META = {
    HUMAN_TEMPLATE_MD: {
        "doc_id": "GPCF-DOC-7797BB4F55",
        "title": "基础知识人工确认模板",
        "project": "KDS",
        "kds_path": "开发/05-KDS/docs/harness/evidence/base-knowledge-human-confirmation-template-20260619.md",
    },
    COMMITTEE_TEMPLATE_MD: {
        "doc_id": "GPCF-DOC-8066745911",
        "title": "基础知识委员会评审模板",
        "project": "KDS",
        "kds_path": "开发/05-KDS/docs/harness/evidence/base-knowledge-committee-review-template-20260619.md",
    },
}


def table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def frontmatter(path: Path, title: str) -> str:
    meta = DOC_META[path]
    return "\n".join(
        [
            "---",
            f"doc_id: {meta['doc_id']}",
            f"title: {title}",
            f"project: {meta['project']}",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            f"owner: {meta['project']}",
            "kds_space: 开发",
            f"kds_path: {meta['kds_path']}",
            f"source_path: {path.relative_to(ROOT).as_posix()}",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-12",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
        ]
    )


def preserve_frontmatter(path: Path, body: str, title: str) -> str:
    if not path.exists():
        return frontmatter(path, title) + body.lstrip("\n")
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return frontmatter(path, title) + body.lstrip("\n")
    end = text.find("\n---\n", 4)
    if end == -1:
        return frontmatter(path, title) + body.lstrip("\n")
    return text[: end + 5] + "\n" + body.lstrip("\n")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing input: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def blank_value(field: dict[str, Any]) -> Any:
    kind = field["type"]
    if kind == "array":
        return []
    if kind == "boolean":
        return None
    return ""


def blank_record(schema: dict[str, Any], queue_item: dict[str, Any]) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for field in schema["fields"]:
        name = field["name"]
        if name in {"queueItemId", "sourceCandidateId", "baseKnowledgeId"}:
            record[name] = queue_item[name]
        else:
            record[name] = blank_value(field)
    return {
        "templateRecordId": queue_item["queueItemId"].replace("Q-", "T-"),
        "sourceQueueItemId": queue_item["queueItemId"],
        "sourceCandidateId": queue_item["sourceCandidateId"],
        "templateStatus": "blank_template_only",
        "record": record,
        "createsConfirmationFact": False,
        "createsCommitteeDecision": False,
        "downstreamAllowed": False,
    }


def build_template(schema: dict[str, Any], queue: dict[str, Any], template_type: str) -> dict[str, Any]:
    records = [blank_record(schema, item) for item in queue["items"]]
    return {
        "templateId": (
            "BKC-HUMAN-CONFIRMATION-TEMPLATE-20260619"
            if template_type == "human_confirmation_template"
            else "BKC-COMMITTEE-REVIEW-TEMPLATE-20260619"
        ),
        "sourceSchemaId": schema["schemaId"],
        "sourceQueueEvidenceId": queue["evidenceId"],
        "currentRound": "GPCF-KDS-DKS-047",
        "templateType": template_type,
        "recordCount": len(records),
        "records": records,
        "controls": {
            "blankTemplateOnly": True,
            "createsConfirmationFact": False,
            "createsCommitteeDecision": False,
            "realKdsApiWrite": False,
            "waesWrite": False,
            "businessLedgerWrite": False,
            "settlementWrite": False,
            "ragAdmission": False,
            "acceptedOrIntegratedUpgrade": False,
        },
        "status": "blank_template_only",
    }


def write_json(template: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(template: dict[str, Any], path: Path, title: str, purpose: str) -> None:
    preview_rows = [
        [
            record["templateRecordId"],
            record["sourceQueueItemId"],
            record["sourceCandidateId"],
            record["templateStatus"],
            str(record["downstreamAllowed"]).lower(),
        ]
        for record in template["records"]
    ]
    md = f"# {title}\n\n"
    md += "日期：2026-06-19\n\n"
    md += "状态：`blank_template_only`\n\n"
    md += f"{purpose}\n\n"
    md += "## 概要\n\n"
    md += f"- template_id：`{template['templateId']}`\n"
    md += f"- source_schema_id：`{template['sourceSchemaId']}`\n"
    md += f"- source_queue_evidence_id：`{template['sourceQueueEvidenceId']}`\n"
    md += f"- template_type：`{template['templateType']}`\n"
    md += f"- record_count：`{template['recordCount']}`\n\n"
    md += "## 空白记录\n\n"
    md += table(
        ["template_record_id", "source_queue_item_id", "source_candidate_id", "template_status", "downstream_allowed"],
        preview_rows,
    )
    md += "\n\n"
    md += "## 控制项\n\n"
    md += table(["control", "value"], [[key, str(value).lower()] for key, value in template["controls"].items()])
    md += "\n\n"
    md += "## 边界\n\n"
    md += "- 空白记录仅作模板，不包含真实的确认或委员会决策。\n"
    md += "- 预填身份字段仅保留与来源候选人的可追溯链路。\n"
    md += "- 不会执行真实 KDS API、WAES、GFIS、GPC、PVAOS、财务入账、清算、RAG 入场或生产写入。\n"
    md += "- 未来填充记录需另行提供受控证据并由人工或委员会处理。\n"
    path.write_text(preserve_frontmatter(path, md, title), encoding="utf-8")


def main() -> int:
    human_schema = load_json(HUMAN_SCHEMA)
    committee_schema = load_json(COMMITTEE_SCHEMA)
    human_queue = load_json(HUMAN_QUEUE)
    committee_queue = load_json(COMMITTEE_QUEUE)

    human_template = build_template(human_schema, human_queue, "human_confirmation_template")
    committee_template = build_template(committee_schema, committee_queue, "committee_review_template")

    write_json(human_template, HUMAN_TEMPLATE_JSON)
    write_json(committee_template, COMMITTEE_TEMPLATE_JSON)
    write_md(
        human_template,
        HUMAN_TEMPLATE_MD,
        "基础知识人工确认模板",
        "本文件基于 DKS-046 人工确认模式，提供未来人工确认所需的空白记录模板。",
    )
    write_md(
        committee_template,
        COMMITTEE_TEMPLATE_MD,
        "基础知识委员会评审模板",
        "本文件基于 DKS-046 委员会评审模式，提供未来委员会评审所需的空白记录模板。",
    )

    print(
        "base_knowledge_blank_review_templates=pass "
        f"human_template_records={human_template['recordCount']} "
        f"committee_template_records={committee_template['recordCount']} "
        "status=blank_template_only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
