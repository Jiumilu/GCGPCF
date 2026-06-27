#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_PROJECTS = [
    "AAAS",
    "Brain",
    "WAS",
    "XiaoC",
    "WAES",
    "GPC",
    "Studio",
    "GPCF",
    "XWAIL",
    "GFIS",
    "MMC",
    "KDS",
    "XiaoG",
    "PVAOS",
    "SOP",
    "PKC",
    "XGD",
]

KEY_DOCS = [
    "GlobalCloud 项目群实施方案.md",
    "02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md",
    "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md",
    "02-governance/loop/LOOP_CONTROL_BOARD.md",
    "09-status/globalcloud-document-health-report.md",
    "09-status/gpcf-project-status-matrix.md",
    "09-status/globalcloud-project-group-real-execution-governance-board.md",
    "09-status/project-group-master-plan-governance-status-report.md",
    "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-ready-for-review-advancement-queue-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-pre-execution-environment-readiness-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-request-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-authorization-receipt-ledger-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-human-confirmation-request-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-objective-coverage-audit-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-governance-progress-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-real-execution-completion-gap-matrix-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-wave1-receipt-pre-execution-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-execution-receipt-pre-execution-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-authorization-to-pre-execution-total-bridge-audit-20260627.md",
    "docs/harness/evidence/globalcloud-project-group-ready-for-review-trigger-map-20260627.md",
]


def parse_related(text: str) -> list[str]:
    match = re.search(r"^related_projects:\s*\[(.*)\]\s*$", text, flags=re.MULTILINE)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def main() -> int:
    failures: list[str] = []
    expected = set(EXPECTED_PROJECTS)
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)

    for relative in KEY_DOCS:
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing key doc: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        related = parse_related(text)
        related_set = set(related)
        missing = sorted(expected - related_set)
        extra = sorted(related_set - expected)
        if missing:
            failures.append(f"{relative} missing related_projects: {missing}")
        if extra:
            failures.append(f"{relative} has unexpected related_projects: {extra}")
        if len(related) != len(EXPECTED_PROJECTS):
            failures.append(f"{relative} related_projects count is {len(related)}, expected {len(EXPECTED_PROJECTS)}")

    result = {
        "gate": "project_group_real_execution_metadata_coverage_20260626",
        "status": "fail" if failures else "pass",
        "key_doc_count": len(KEY_DOCS),
        "expected_project_count": len(EXPECTED_PROJECTS),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates frontmatter related_projects coverage only; it does not execute tasks, grant authorization, stage, commit, push, deploy, release, sync KDS API, or grant accepted/integrated/customer acceptance."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
