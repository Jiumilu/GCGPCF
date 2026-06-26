#!/usr/bin/env python3
"""Validate SOP scenario owner review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOP_REPO = ROOT.parent / "GlobalCloud SOP"
DOC = ROOT / "docs/harness/SOP/evidence/sop-scenario-owner-review-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

SOP_PLAN = SOP_REPO / "GlobalCloud SOP 实施方案.md"
SOP_AGENTS = SOP_REPO / "AGENTS.md"
SOP_INDEX = SOP_REPO / "docs/standardization/document-index.md"
SOP_SCENARIO = SOP_REPO / "docs/operations/wuhan-city-circle-green-supply-chain-operating-system.md"
SOP_PDF_MD = SOP_REPO / "output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.md"
SOP_PDF = SOP_REPO / "output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.pdf"
SOP_DS_STORE = SOP_REPO / "output/.DS_Store"

REQUIRED_DOC_TOKENS = [
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "sop_scenario_owner_review = controlled",
    "target_status_candidate = owner_review_required / scenario_candidate_controlled",
    "validate_sop_assets = pass",
    "run_smoke_test = pass",
    "scenario_document_status = draft_for_special_team_meeting",
    "dirty_index = docs/standardization/document-index.md",
    "dirty_scenario_doc = docs/operations/wuhan-city-circle-green-supply-chain-operating-system.md",
    "dirty_pdf_md = output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.md",
    "dirty_pdf = output/pdf/武汉城市圈绿色供应链协同运营方案与SOP_对外发送版_20260625.pdf",
    "dirty_system_noise = output/.DS_Store",
    "owner_review_required = true",
    "scenario_owner_confirmed = false",
    "kds_fact_ingested = false",
    "official_sop_promoted = false",
    "customer_delivery_confirmed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "不声明武汉城市圈绿色供应链方案已确认",
    "不声明 KDS 事实主存已入库",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud SOP 实施方案",
    "project: SOP",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_AGENTS_TOKENS = [
    "保护用户已有工作",
    "main` 分支处于 dirty 状态",
    "不得直接声明 accepted、integrated 或 production_ready",
]

REQUIRED_SCENARIO_TOKENS = [
    "draft_for_special_team_meeting",
    "status_ceiling",
    "draft/candidate",
    "未经用户与相关国企/合作方确认",
    "不得声明为 `accepted`、`integrated`、`production_ready` 或正式发布制度",
]

REQUIRED_REF_TOKENS = [
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "sop-scenario-owner-review-20260625.md",
    "validate_sop_scenario_owner_review.py",
    "owner_review_required / scenario_candidate_controlled",
]

FORBIDDEN_CLAIMS = [
    "scenario_owner_confirmed = true",
    "kds_fact_ingested = true",
    "official_sop_promoted = true",
    "customer_delivery_confirmed = true",
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
    plan_text = read(SOP_PLAN, failures)
    agents_text = read(SOP_AGENTS, failures)
    index_text = read(SOP_INDEX, failures)
    scenario_text = read(SOP_SCENARIO, failures)
    refs_text = "\n".join(
        [
            read(BOARD, failures),
            read(REGISTER, failures),
            read(STATUS, failures),
            read(BASELINE, failures),
            read(TASKS, failures),
        ]
    )

    for path in [SOP_REPO, SOP_PDF_MD, SOP_PDF, SOP_DS_STORE]:
        if not path.exists():
            failures.append(f"missing SOP path: {path}")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in SOP owner review evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in SOP implementation plan: {token}")

    for token in REQUIRED_AGENTS_TOKENS:
        if token not in agents_text:
            failures.append(f"missing token in SOP AGENTS: {token}")

    for token in REQUIRED_SCENARIO_TOKENS:
        if token not in scenario_text:
            failures.append(f"missing token in SOP scenario document: {token}")

    if "docs/operations/wuhan-city-circle-green-supply-chain-operating-system.md" not in index_text:
        failures.append("SOP document index must reference the scenario document")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive SOP claim: {token}")

    result = {
        "gate": "sop_scenario_owner_review",
        "status": "pass" if not failures else "fail",
        "task_id": "SOP-SCENARIO-OWNER-REVIEW-001",
        "target_status_candidate": "owner_review_required / scenario_candidate_controlled",
        "validate_sop_assets": "pass",
        "run_smoke_test": "pass",
        "owner_review_required": True,
        "scenario_owner_confirmed": False,
        "kds_fact_ingested": False,
        "failures": failures,
        "warnings": [
            "This validates SOP owner review readiness only; it does not accept the scenario, ingest it into KDS fact storage, publish it, deliver it, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
