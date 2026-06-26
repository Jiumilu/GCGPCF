#!/usr/bin/env python3
"""Validate KDS funding report and sync-run hold review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KDS_REPO = ROOT.parent / "GlobalCloud KDS"
DOC = ROOT / "docs/harness/KDS/evidence/kds-brain-report-hold-review-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

KDS_AGENTS = KDS_REPO / "AGENTS.md"
KDS_PLAN = KDS_REPO / "GlobalCloud KDS 实施方案.md"
FUNDING_REPORT = KDS_REPO / "工业绿链/reports/合同资金追踪报告.md"
FEISHU_RUN = KDS_REPO / "_governance/sync-runs/feishu-xiaog-closure-20260625-112003/report.md"
MACMINI_RUN_111819 = KDS_REPO / "_governance/sync-runs/macmini-workwiki-20260625-111819/report.md"
MACMINI_RUN_111935 = KDS_REPO / "_governance/sync-runs/macmini-workwiki-20260625-111935/report.md"

REQUIRED_DOC_TOKENS = [
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "kds_brain_report_hold_review = controlled",
    "target_status_candidate = owner_review_required / kds_report_hold_controlled",
    "funding_report_modified = true",
    "funding_report_path = 工业绿链/reports/合同资金追踪报告.md",
    "funding_report_type = contract_funding_report",
    "sync_run_feishu_xiaog_closure = _governance/sync-runs/feishu-xiaog-closure-20260625-112003/report.md",
    "sync_run_macmini_workwiki_111819 = _governance/sync-runs/macmini-workwiki-20260625-111819/report.md",
    "sync_run_macmini_workwiki_111935 = _governance/sync-runs/macmini-workwiki-20260625-111935/report.md",
    "owner_review_required = true",
    "funding_report_owner_confirmed = false",
    "kds_api_sync_executed = false",
    "production_index_updated = false",
    "brain_ingestion_confirmed = false",
    "waes_evidence_published = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "不声明资金追踪报告已经业务确认",
    "不声明真实 KDS API 已同步",
]

REQUIRED_AGENTS_TOKENS = [
    "Treat Markdown files in this repository as the source of record",
    "Do not treat GBrain search output as canonical unless it points back to Markdown evidence",
    "After meaningful Markdown edits, refresh the local GBrain index",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud KDS 实施方案",
    "project: KDS",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "本地镜像被误认为真实 KDS API 同步",
    "知识候选被误认为事实",
]

REQUIRED_REPORT_TOKENS = [
    "type: contract_funding_report",
    "合同资金追踪报告",
    "资金节点索引已填充",
    "0/4",
    "待确认",
]

REQUIRED_SYNC_TOKENS = [
    "Macmini WorkWiki 全量分析同步报告",
    "隔离 mirror",
    "未直接覆盖本机 KDS canonical 根目录",
    "remote-only",
    "changed",
    "local-only",
]

REQUIRED_REF_TOKENS = [
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "kds-brain-report-hold-review-20260625.md",
    "validate_kds_brain_report_hold_review.py",
    "owner_review_required / kds_report_hold_controlled",
]

FORBIDDEN_CLAIMS = [
    "funding_report_owner_confirmed = true",
    "kds_api_sync_executed = true",
    "production_index_updated = true",
    "brain_ingestion_confirmed = true",
    "waes_evidence_published = true",
    "production_ready = true",
    "accepted = true",
    "integrated = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    agents_text = read(KDS_AGENTS, failures)
    plan_text = read(KDS_PLAN, failures)
    report_text = read(FUNDING_REPORT, failures)
    feishu_text = read(FEISHU_RUN, failures)
    macmini_111819_text = read(MACMINI_RUN_111819, failures)
    macmini_111935_text = read(MACMINI_RUN_111935, failures)
    refs_text = "\n".join(
        [
            read(BOARD, failures),
            read(REGISTER, failures),
            read(STATUS, failures),
            read(BASELINE, failures),
            read(TASKS, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in KDS hold review evidence: {token}")

    for token in REQUIRED_AGENTS_TOKENS:
        if token not in agents_text:
            failures.append(f"missing token in KDS AGENTS: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in KDS implementation plan: {token}")

    for token in REQUIRED_REPORT_TOKENS:
        if token not in report_text:
            failures.append(f"missing token in funding report: {token}")

    sync_combined = "\n".join([macmini_111819_text, macmini_111935_text])
    for token in REQUIRED_SYNC_TOKENS:
        if token not in sync_combined:
            failures.append(f"missing token in Macmini sync reports: {token}")

    for token in ["飞书小即", "WorkWiki", "KDS", "闭环核查"]:
        if token not in feishu_text:
            failures.append(f"missing token in Feishu closure report: {token}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive KDS claim: {token}")

    result = {
        "gate": "kds_brain_report_hold_review",
        "status": "pass" if not failures else "fail",
        "task_id": "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
        "target_status_candidate": "owner_review_required / kds_report_hold_controlled",
        "owner_review_required": True,
        "funding_report_owner_confirmed": False,
        "kds_api_sync_executed": False,
        "brain_ingestion_confirmed": False,
        "failures": failures,
        "warnings": [
            "This validates KDS report hold review readiness only; it does not confirm funding facts, execute KDS API sync, refresh production index, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
