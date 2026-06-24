#!/usr/bin/env python3
"""Build candidate-only confirmation queue views from base knowledge writeback candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SOURCE_JSON = ROOT / "docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.json"
HUMAN_JSON = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.json"
HUMAN_MD = ROOT / "docs/harness/evidence/base-knowledge-human-confirmation-queue-20260619.md"
COMMITTEE_JSON = ROOT / "docs/harness/evidence/base-knowledge-committee-review-queue-20260619.json"
COMMITTEE_MD = ROOT / "docs/harness/evidence/base-knowledge-committee-review-queue-20260619.md"


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


def load_source() -> dict[str, Any]:
    if not SOURCE_JSON.exists():
        raise SystemExit(f"missing source summary: {SOURCE_JSON.relative_to(ROOT)}")
    return json.loads(SOURCE_JSON.read_text(encoding="utf-8"))


def queue_item(candidate: dict[str, Any], queue_type: str) -> dict[str, Any]:
    if queue_type == "human_confirmation":
        next_action = "manual_source_and_gap_confirmation"
        queue_reason = "non_hard_stop_candidate_requires_human_confirmation"
    else:
        next_action = "committee_review_required_before_any_downstream_action"
        queue_reason = "hard_stop_candidate_requires_committee_review"

    return {
        "queueItemId": candidate["candidateId"].replace("WBC-", "Q-"),
        "sourceCandidateId": candidate["candidateId"],
        "sourceRound": "GPCF-KDS-DKS-044",
        "fixtureId": candidate["fixtureId"],
        "baseKnowledgeId": candidate["baseKnowledgeId"],
        "target": candidate["target"],
        "reason": candidate["reason"],
        "decisionBand": candidate["decisionBand"],
        "hardStop": candidate["hardStop"],
        "queueType": queue_type,
        "queueReason": queue_reason,
        "requiredConfirmation": candidate["requiredConfirmation"],
        "nextAction": next_action,
        "queueStatus": "candidate_only",
        "writeAuthority": "none_dry_run_only",
        "downstreamAllowed": False,
    }


def build_queue(source: dict[str, Any], queue_type: str, hard_stop: bool) -> dict[str, Any]:
    items = [
        queue_item(candidate, queue_type)
        for candidate in source["writebackCandidates"]
        if candidate["hardStop"] is hard_stop
    ]
    return {
        "evidenceId": (
            "BKC-HUMAN-CONFIRMATION-QUEUE-20260619"
            if queue_type == "human_confirmation"
            else "BKC-COMMITTEE-REVIEW-QUEUE-20260619"
        ),
        "sourceEvidenceId": source["evidenceId"],
        "sourceRound": "GPCF-KDS-DKS-044",
        "currentRound": "GPCF-KDS-DKS-045",
        "queueType": queue_type,
        "itemCount": len(items),
        "items": items,
        "boundary": {
            "realKdsApiWrite": False,
            "waesWrite": False,
            "businessLedgerWrite": False,
            "settlementWrite": False,
            "ragAdmission": False,
            "scoreSettlement": False,
            "revenueAllocation": False,
            "bountyPublication": False,
            "committeeDecisionCompleted": False,
        },
        "status": "candidate_only",
    }


def write_queue_json(queue: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_queue_md(queue: dict[str, Any], path: Path, title: str, description: str) -> None:
    rows = [
        [
            item["queueItemId"],
            item["sourceCandidateId"],
            item["baseKnowledgeId"],
            item["target"],
            item["reason"],
            item["decisionBand"],
            str(item["hardStop"]).lower(),
            item["nextAction"],
            item["queueStatus"],
            item["writeAuthority"],
        ]
        for item in queue["items"]
    ]

    md = f"# {title}\n\n"
    md += "日期：2026-06-19\n\n"
    md += "状态：`candidate_only`\n\n"
    md += f"{description}\n\n"
    md += "## 概要\n\n"
    md += f"- evidence_id：`{queue['evidenceId']}`\n"
    md += f"- source_evidence_id：`{queue['sourceEvidenceId']}`\n"
    md += f"- source_round：`{queue['sourceRound']}`\n"
    md += f"- current_round：`{queue['currentRound']}`\n"
    md += f"- queue_type：`{queue['queueType']}`\n"
    md += f"- item_count：`{queue['itemCount']}`\n\n"
    md += "## 队列项目\n\n"
    md += table(
        [
            "queue_item_id",
            "source_candidate_id",
            "base_knowledge_id",
            "target",
            "reason",
            "decision_band",
            "hard_stop",
            "next_action",
            "queue_status",
            "write_authority",
        ],
        rows,
    )
    md += "\n\n"
    md += "## 边界\n\n"
    md += table(
        ["boundary", "value"],
        [[key, str(value).lower()] for key, value in queue["boundary"].items()],
    )
    md += "\n\n"
    md += "## 控制\n\n"
    md += "- Queue rows are candidate-only and do not confirm facts, close gaps, or write any system.\n"
    md += "- No score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger write is performed.\n"
    md += "- No real KDS API, WAES, GFIS, GPC, PVAOS, finance, settlement, or production write is performed.\n"
    md += "- Committee rows are review candidates only; committee decision is not completed in this evidence.\n"
    path.write_text(preserve_frontmatter(path, md), encoding="utf-8")


def main() -> int:
    source = load_source()
    human_queue = build_queue(source, "human_confirmation", hard_stop=False)
    committee_queue = build_queue(source, "committee_review", hard_stop=True)

    write_queue_json(human_queue, HUMAN_JSON)
    write_queue_json(committee_queue, COMMITTEE_JSON)
    write_queue_md(
        human_queue,
        HUMAN_MD,
        "基础知识人工确认队列",
        "This queue contains non-hard-stop writeback candidates that still require human confirmation before any downstream action.",
    )
    write_queue_md(
        committee_queue,
        COMMITTEE_MD,
        "基础知识委员会评审队列",
        "This queue contains hard-stop writeback candidates that require committee review before any downstream action.",
    )

    total = human_queue["itemCount"] + committee_queue["itemCount"]
    print(
        "base_knowledge_confirmation_queue_views=pass "
        f"total_candidates={total} "
        f"human_queue={human_queue['itemCount']} "
        f"committee_queue={committee_queue['itemCount']} "
        "status=candidate_only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
