#!/usr/bin/env python3
"""Build local evidence for base knowledge closure dry-run scoring."""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCORER = ROOT / "tools/kds-sync/validate_base_knowledge_closure_score_dry_run.py"
FIXTURE = ROOT / "docs/harness/evidence/base-knowledge-closure-score-fixtures.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/base-knowledge-closure-score-dry-run-summary-20260618.md"
WRITEBACK_MD = ROOT / "docs/harness/evidence/base-knowledge-writeback-candidate-ledger-20260618.md"


def load_scorer() -> Any:
    spec = importlib.util.spec_from_file_location("bkc_scorer", SCORER)
    if not spec or not spec.loader:
        raise SystemExit("cannot load base knowledge closure scorer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def candidate_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seq = 1
    for item in results:
        fixture_id = item["fixtureId"]
        result = item["result"]
        for candidate in result.get("writebackCandidates", []):
            rows.append(
                {
                    "candidateId": f"WBC-DKS-044-{seq:03d}",
                    "fixtureId": fixture_id,
                    "baseKnowledgeId": result["baseKnowledgeId"],
                    "target": candidate["target"],
                    "reason": candidate["reason"],
                    "candidateStatus": candidate["status"],
                    "decisionBand": result["decisionBand"],
                    "hardStop": result["hardStop"],
                    "requiredConfirmation": "manual_or_committee_required",
                    "writeAuthority": "none_dry_run_only",
                }
            )
            seq += 1
    return rows


def build_summary() -> dict[str, Any]:
    scorer = load_scorer()
    suite = scorer.validate_fixture_suite(FIXTURE)
    results = suite["results"]
    bands = Counter(item["result"]["decisionBand"] for item in results)
    hard_stops = [item for item in results if item["result"]["hardStop"]]
    writebacks = candidate_rows(results)
    return {
        "evidenceId": "BKC-DRY-RUN-SUMMARY-20260618",
        "sourceRound": "GPCF-KDS-DKS-044",
        "sourceFixture": str(FIXTURE.relative_to(ROOT)),
        "scorer": str(SCORER.relative_to(ROOT)),
        "fixtureCount": suite["fixtures"],
        "expectedHardStops": suite["expectedHardStops"],
        "decisionBandCounts": dict(sorted(bands.items())),
        "writebackCandidateCount": len(writebacks),
        "writebackCandidates": writebacks,
        "boundary": suite["boundary"],
        "status": "dry_run_evidence_only",
    }


def write_markdown(summary: dict[str, Any]) -> None:
    band_rows = [[band, str(count)] for band, count in summary["decisionBandCounts"].items()]
    candidate_md_rows = [
        [
            item["candidateId"],
            item["fixtureId"],
            item["baseKnowledgeId"],
            item["target"],
            item["reason"],
            item["candidateStatus"],
            item["decisionBand"],
            str(item["hardStop"]).lower(),
            item["writeAuthority"],
        ]
        for item in summary["writebackCandidates"]
    ]
    md = "# 基础知识闭环评分试运行汇总\n\n"
    md += "日期：2026-06-18\n\n"
    md += "状态：`dry_run_evidence_only`\n\n"
    md += "## 概要\n\n"
    md += f"- evidence_id：`{summary['evidenceId']}`\n"
    md += f"- source_round：`{summary['sourceRound']}`\n"
    md += f"- fixture_count：`{summary['fixtureCount']}`\n"
    md += f"- expected_hard_stops：`{summary['expectedHardStops']}`\n"
    md += f"- writeback_candidate_count：`{summary['writebackCandidateCount']}`\n\n"
    md += "## 决策分档\n\n"
    md += table(["decision_band", "count"], band_rows)
    md += "\n\n"
    md += "## 边界\n\n"
    md += table(
        ["boundary", "value"],
        [[key, str(value).lower()] for key, value in summary["boundary"].items()],
    )
    md += "\n\n"
    md += "## 写回候选预览\n\n"
    md += table(
        [
            "candidate_id",
            "fixture_id",
            "base_knowledge_id",
            "target",
            "reason",
            "candidate_status",
            "decision_band",
            "hard_stop",
            "write_authority",
        ],
        candidate_md_rows,
    )
    md += "\n\n"
    md += "## 控制边界\n\n"
    md += "- This evidence is generated from local fixtures only.\n"
    md += "- All writeback rows are candidate-only and require manual or committee confirmation.\n"
    md += "- No real KDS API, WAES write, GFIS/GPC/PVAOS business ledger write, RAG admission, settlement, bounty release, revenue allocation, or AI quota allocation is performed.\n"
    md += "- Hard-stop rows remain blocked even when the calculated score is above a lower decision band.\n"
    OUTPUT_MD.write_text(preserve_frontmatter(OUTPUT_MD, md), encoding="utf-8")

    ledger = "# 基础知识回写候选账本\n\n"
    ledger += "日期：2026-06-18\n\n"
    ledger += "状态：`candidate_only`\n\n"
    ledger += "## 候选账本\n\n"
    ledger += table(
        [
            "candidate_id",
            "fixture_id",
            "base_knowledge_id",
            "target",
            "reason",
            "candidate_status",
            "required_confirmation",
            "write_authority",
        ],
        [
            [
                item["candidateId"],
                item["fixtureId"],
                item["baseKnowledgeId"],
                item["target"],
                item["reason"],
                item["candidateStatus"],
                item["requiredConfirmation"],
                item["writeAuthority"],
            ]
            for item in summary["writebackCandidates"]
        ],
    )
    ledger += "\n\n"
    ledger += "## 控制边界\n\n"
    ledger += "- Candidate rows do not close gaps.\n"
    ledger += "- Candidate rows do not create score settlement, revenue allocation, bounty publication, RAG admission, command-center strong reference, or business ledger writes.\n"
    ledger += "- Candidate rows must be confirmed by the proper human, KDS, WAES, or committee process before any downstream action.\n"
    WRITEBACK_MD.write_text(preserve_frontmatter(WRITEBACK_MD, ledger), encoding="utf-8")


def main() -> int:
    summary = build_summary()
    OUTPUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(summary)
    print(
        "base_knowledge_closure_dry_run_evidence=pass "
        f"fixtures={summary['fixtureCount']} "
        f"expected_hard_stops={summary['expectedHardStops']} "
        f"writeback_candidates={summary['writebackCandidateCount']} "
        "status=dry_run_evidence_only"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
