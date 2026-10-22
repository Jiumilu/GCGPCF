#!/usr/bin/env python3
"""Validate the frozen evidence rule version (PG-08) and its done-feature audit."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULE = ROOT / "09-status/globalcloud-evidence-rule-version-v1.0.md"
AUDIT = ROOT / "09-status/globalcloud-done-feature-audit-20261022.md"
DONE = ROOT / "features/done"

RULE_TOKENS = [
    "evidence_rule_version = GCPF-EVIDENCE-RULE-1.0",
    "effective_date = 2026-10-22",
    "freeze_status = frozen",
    "change_requires = change_proposal + human_confirmation",
    "historical_done_policy = re_verify_or_register_exception",
    "auto_close = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

AUDIT_TOKENS = [
    "audit_rule_version = GCPF-EVIDENCE-RULE-1.0",
    "auto_close = false",
]

FEATURES = [
    "F-001-supplier-onboarding",
    "F-002-project-group-feature-queue",
    "F-003-evidence-gate-profile",
    "F-006-knowledge-e2e-flow",
    "F-007-reports-data-flow",
    "F-008-icp-project-group-admission",
    "F-009-project-group-openspec-coverage",
    "F-018-gpcf-governance-console",
    "F-020-aaas-service-console",
    "F-028-plane-gpcf-feature-evidence-integration",
]

FORBIDDEN = ["accepted = true", "integrated = true", "production_ready = true", "customer_accepted = true"]


def fail(msg: str) -> int:
    print("evidence_rule_version = fail")
    print(f"reason = {msg}")
    return 1


def main() -> int:
    for p in (RULE, AUDIT):
        if not p.exists():
            return fail(f"missing file: {p.relative_to(ROOT)}")
    rule = RULE.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    missing = [t for t in RULE_TOKENS if t not in rule]
    if missing:
        return fail("rule doc missing tokens: " + "; ".join(missing))
    for token in ("done_feature_count", "pass_count", "fail_count"):
        if not re.search(rf"{token}\s*=\s*\d+", audit):
            return fail(f"audit doc missing {token} = <n>")
    missing = [t for t in AUDIT_TOKENS if t not in audit]
    if missing:
        return fail("audit doc missing tokens: " + "; ".join(missing))
    missing = [f for f in FEATURES if f not in audit]
    if missing:
        return fail("audit doc missing features: " + ", ".join(missing))
    forbidden = [t for t in FORBIDDEN if t in rule or t in audit]
    if forbidden:
        return fail("forbidden positive claims: " + "; ".join(forbidden))

    done_dirs = sorted(p.name for p in DONE.iterdir() if p.is_dir()) if DONE.exists() else []
    if len(done_dirs) < len(FEATURES):
        return fail(f"features/done count is {len(done_dirs)}, expected >= {len(FEATURES)}")

    print("evidence_rule_version = pass")
    print("evidence_rule_version = GCPF-EVIDENCE-RULE-1.0")
    print("freeze_status = frozen")
    print(f"done_feature_count = {len(done_dirs)}")
    print(f"audited_feature_count = {len(FEATURES)}")
    audit_pass = re.search(r"pass_count\s*=\s*(\d+)", audit).group(1)
    audit_fail = re.search(r"fail_count\s*=\s*(\d+)", audit).group(1)
    print(f"pass_count = {audit_pass}")
    print(f"fail_count = {audit_fail}")
    print("auto_close = false")
    print("accepted = false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
