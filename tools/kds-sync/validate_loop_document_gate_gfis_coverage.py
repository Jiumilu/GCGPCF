#!/usr/bin/env python3
"""Validate GFIS real-fact guard coverage for loop document gate checks."""

from __future__ import annotations

import ast
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
LOOP_DOCUMENT_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"
STATUS_TERMS = [
    "accepted",
    "integrated",
    "production_ready",
    "customer_accepted",
    "ready_for_review",
    "review_queue",
    "runtime_intake",
    "verified",
]
GFIS_GUARD_TERMS = [
    "require_gfis_real_fact_entry",
    "validate_gfis_real_fact_entry",
    "validate_gfis_real_fact_entry_gate.py",
]


def direct_validator_paths() -> list[tuple[str, Path]]:
    tree = ast.parse(LOOP_DOCUMENT_GATE.read_text(encoding="utf-8"))
    validators: list[tuple[str, Path]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Dict(self, node: ast.Dict) -> None:
            for key, value in zip(node.keys, node.values):
                if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                    continue
                expression = ast.unparse(value)
                parts = [
                    part
                    for part in expression.replace('"', "'").split("'")
                    if part.startswith("tools/kds-sync/validate_")
                ]
                if parts:
                    validators.append((key.value, ROOT / parts[0]))
            self.generic_visit(node)

    Visitor().visit(tree)
    return validators


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    failures: list[str] = []
    checked = 0
    guarded = 0

    for name, path in direct_validator_paths():
        if not path.exists():
            failures.append(f"{name}:missing_validator:{path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not any(term in text for term in STATUS_TERMS):
            continue
        checked += 1
        if any(term in text for term in GFIS_GUARD_TERMS):
            guarded += 1
            if "validate_gfis_real_fact_entry_gate.py" in text and "customer_accepted" not in text:
                failures.append(f"{name}:missing_customer_accepted_false_guard:{path.relative_to(ROOT)}")
        else:
            failures.append(f"{name}:missing_gfis_real_fact_guard:{path.relative_to(ROOT)}")

    if failures:
        raise SystemExit("FAIL validate_loop_document_gate_gfis_coverage: " + "; ".join(failures))

    print(
        "loop_document_gate_gfis_coverage=pass "
        f"status_related_direct_validators={checked} "
        f"gfis_guarded_direct_validators={guarded} "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        "customer_accepted_guard=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
