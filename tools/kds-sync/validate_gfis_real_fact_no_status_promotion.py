#!/usr/bin/env python3
"""Ensure GFIS zero-entry facts cannot be read as status promotion."""

from __future__ import annotations

import re
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]

CONTROL_DOCS = [
    "02-governance/loop/LOOP_CONTROL_BOARD.md",
    "docs/harness/loop-state.md",
    "09-status/globalcloud-document-health-report.md",
    "09-status/gpcf-project-status-matrix.md",
    "09-status/globalcloud-project-implementation-control-register.md",
    "09-status/globalcloud-project-group-real-execution-governance-board.md",
    "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md",
    "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md",
]

BOOLEAN_PROMOTION_PATTERNS = [
    re.compile(r"\baccepted\s*=\s*true\b"),
    re.compile(r"\bintegrated\s*=\s*true\b"),
    re.compile(r"\bproduction_ready\s*=\s*true\b"),
    re.compile(r"\bcustomer_accepted\s*=\s*true\b"),
    re.compile(r"\|\s*`?(accepted|integrated|production_ready|customer_accepted)`?\s*\|\s*`?true`?\s*\|"),
]

CHINESE_PROMOTION_PHRASES = [
    "已验收",
    "客户验收完成",
    "生产可用",
    "业务事实完成",
    "真实闭环完成",
]

NEGATION_MARKERS = [
    "不声明",
    "不得声明",
    "不证明",
    "不代表",
    "未",
    "等待",
    "除非",
    "前需要",
]

REQUIRED_BOUNDARY_TOKENS = [
    "real_source_records=0",
    "formal_confirmation_files=0",
    "runtime_primary_key",
    "review_queue",
    "runtime_intake",
    "WAES review",
    "verified",
    "status_ceiling=repair_required",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_gfis_real_fact_no_status_promotion: {message}")


def line_has_forbidden_chinese_promotion(line: str) -> bool:
    if not any(phrase in line for phrase in CHINESE_PROMOTION_PHRASES):
        return False
    return not any(marker in line for marker in NEGATION_MARKERS)


def main() -> int:
    require_gfis_real_fact_entry(ROOT)
    missing_docs: list[str] = []
    findings: list[str] = []
    combined_text: list[str] = []

    for rel in CONTROL_DOCS:
        path = ROOT / rel
        if not path.exists():
            missing_docs.append(rel)
            continue
        text = path.read_text(encoding="utf-8")
        combined_text.append(text)
        for lineno, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            if any(pattern.search(lowered) for pattern in BOOLEAN_PROMOTION_PATTERNS):
                findings.append(f"{rel}:{lineno}:positive_boolean")
            if line_has_forbidden_chinese_promotion(line):
                findings.append(f"{rel}:{lineno}:positive_chinese_phrase")

    require(not missing_docs, "missing control docs: " + ",".join(missing_docs))
    require(not findings, "status promotion claims under GFIS zero entry: " + ",".join(findings[:20]))

    all_text = "\n".join(combined_text)
    missing_tokens = [token for token in REQUIRED_BOUNDARY_TOKENS if token not in all_text]
    require(not missing_tokens, "missing GFIS boundary tokens: " + ",".join(missing_tokens))

    print(
        "gfis_real_fact_no_status_promotion=pass "
        f"checked_docs={len(CONTROL_DOCS)} "
        "positive_status_claims=0 "
        "gfis_status_ceiling=repair_required "
        "accepted=false integrated=false production_ready=false customer_accepted=false "
        "strong_block=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
