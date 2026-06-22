#!/usr/bin/env python3
"""Validate the OKF v0.1 summary admission gate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUNDLES = [
    ROOT / ".okf/bundles/kds-v0.1",
    ROOT / ".okf/bundles/governance-v0.1",
    ROOT / ".okf/bundles/architecture-v0.1",
]
JSON_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-admission-gate-20260620.json"
MD_OUT = ROOT / "docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md"
LEDGER = ROOT / "docs/harness/evidence/okf-v01-summary-admission-ledger-20260620.md"
APPROVAL_REQUEST_GATE = ROOT / "docs/harness/evidence/okf-v01-summary-approval-request-gate-20260620.md"
APPROVAL_EXPIRY_GATE = ROOT / "docs/harness/evidence/okf-v01-summary-approval-expiry-gate-20260621.md"

SENSITIVE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"token\\s*[:=]",
        r"api[_-]?key\\s*[:=]",
        r"password\\s*[:=]",
        r"secret\\s*[:=]",
        r"private key",
        r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
        r"合同全文",
        r"未授权客户材料",
        r"金融凭证",
    ]
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def doc_id_for(path: Path) -> str:
    digest = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:10].upper()
    return f"GPCF-DOC-{digest}"


def split_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, body


def iter_concepts() -> list[tuple[Path, dict[str, str], str]]:
    concepts: list[tuple[Path, dict[str, str], str]] = []
    for bundle in BUNDLES:
        if not bundle.exists():
            raise SystemExit(f"okf_summary_admission_gate=fail reason=missing_bundle:{rel(bundle)}")
        for path in sorted(bundle.rglob("*.md")):
            if path.name in {"index.md", "log.md"}:
                continue
            meta, body = split_frontmatter(path)
            if meta.get("type"):
                concepts.append((path, meta, body))
    return concepts


def parse_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    headers: list[str] = []
    for line in read_text(path).splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip().strip("`") for part in line.strip("|").split("|")]
        if not headers:
            headers = parts
            continue
        if all(part.startswith("---") or set(part) <= {":", "-"} for part in parts):
            continue
        if len(parts) != len(headers):
            continue
        rows.append(dict(zip(headers, parts)))
    return rows


def ledger_summary() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = parse_table(LEDGER)
    violations: list[dict[str, str]] = []
    for row in rows:
        status = row.get("status", "")
        if status not in {"pending_review", "approved", "rejected", "deferred"}:
            violations.append({"path": rel(LEDGER), "reason": f"invalid_ledger_status:{status}"})
        if status == "approved":
            missing = [
                field
                for field in [
                    "owner_approval",
                    "sensitivity_review",
                    "summary_scope",
                    "source_path",
                    "kds_path",
                ]
                if not row.get(field) or row.get(field) in {"none", "pending"}
            ]
            if missing:
                violations.append({"path": rel(LEDGER), "reason": "approved_row_missing:" + ",".join(missing)})
    return rows, violations


def validate() -> dict:
    concepts = iter_concepts()
    violations: list[dict[str, str]] = []
    approved_summaries = 0
    sensitive_hits = 0

    for path, meta, body in concepts:
        policy = meta.get("derivation_policy", "")
        if policy == "approved_summary":
            approved_summaries += 1
            violations.append(
                {
                    "path": rel(path),
                    "reason": "approved_summary_requires_owner_and_sensitivity_evidence",
                }
            )
        elif policy != "metadata_only_no_body_copy":
            violations.append({"path": rel(path), "reason": f"unsupported_derivation_policy:{policy}"})

        if "# Approved Summary" in body or "approved_summary" in body:
            approved_summaries += 1
            violations.append({"path": rel(path), "reason": "summary_section_without_admission_ledger"})

        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(body):
                sensitive_hits += 1
                violations.append({"path": rel(path), "reason": f"sensitive_pattern:{pattern.pattern}"})
                break
    ledger_rows, ledger_violations = ledger_summary()
    violations.extend(ledger_violations)
    approval_gate = subprocess.run(
        [sys.executable, "tools/kds-sync/validate_okf_summary_approval_request.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    approval_gate_output = (approval_gate.stdout + approval_gate.stderr).strip()
    if approval_gate.returncode != 0:
        violations.append({"path": rel(APPROVAL_REQUEST_GATE), "reason": approval_gate_output})
    expiry_gate = subprocess.run(
        [sys.executable, "tools/kds-sync/validate_okf_summary_approval_expiry.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    expiry_gate_output = (expiry_gate.stdout + expiry_gate.stderr).strip()
    if expiry_gate.returncode != 0:
        violations.append({"path": rel(APPROVAL_EXPIRY_GATE), "reason": expiry_gate_output})
    pending_requests = sum(1 for row in ledger_rows if row.get("status") == "pending_review")
    approved_requests = sum(1 for row in ledger_rows if row.get("status") == "approved")

    status = "pass" if not violations else "fail"
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "admission_state": "metadata_only_locked",
        "concepts": len(concepts),
        "approved_summaries": approved_summaries,
        "sensitive_hits": sensitive_hits,
        "ledger": rel(LEDGER),
        "approval_request_gate": rel(APPROVAL_REQUEST_GATE),
        "approval_request_gate_output": approval_gate_output,
        "approval_expiry_gate": rel(APPROVAL_EXPIRY_GATE),
        "approval_expiry_gate_output": expiry_gate_output,
        "ledger_rows": len(ledger_rows),
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "violations": violations,
        "required_before_summary_admission": [
            "owner approval",
            "source sensitivity review",
            "explicit summary scope",
            "active approval request within pending window",
            "no token/account/credential/financial-voucher/contract-fulltext export",
            "updated OKF source hash and collection gate",
        ],
        "boundary": {
            "source_of_record": "KDS / Git controlled documents",
            "current_derivation_policy": "metadata_only_no_body_copy",
            "does_not_admit_summaries": True,
            "does_not_upgrade_business_status": True,
        },
    }


def write_markdown(report: dict) -> None:
    requirements = "\n".join(f"- {item}" for item in report["required_before_summary_admission"])
    violation_rows = "\n".join(
        f"| `{item['path']}` | {item['reason']} |" for item in report["violations"]
    )
    if not violation_rows:
        violation_rows = "| none | none |"

    content = f"""---
doc_id: {doc_id_for(MD_OUT)}
title: OKF v0.1 Summary Admission Gate Evidence
project: GPCF
related_projects: [GPCF, KDS, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md
source_path: docs/harness/evidence/okf-v01-summary-admission-gate-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-20
supersedes: []
superseded_by: []
---

# OKF v0.1 Summary Admission Gate Evidence

generated_at: {report["generated_at"]}

## Summary

| metric | value |
| --- | --- |
| status | {report["status"]} |
| admission_state | {report["admission_state"]} |
| concepts | {report["concepts"]} |
| approved_summaries | {report["approved_summaries"]} |
| sensitive_hits | {report["sensitive_hits"]} |
| ledger | `{report["ledger"]}` |
| approval_request_gate | `{report["approval_request_gate"]}` |
| approval_expiry_gate | `{report["approval_expiry_gate"]}` |
| ledger_rows | {report["ledger_rows"]} |
| pending_requests | {report["pending_requests"]} |
| approved_requests | {report["approved_requests"]} |
| json | `{rel(JSON_OUT)}` |

## Required Before Summary Admission

{requirements}

## Violations

| path | reason |
| --- | --- |
{violation_rows}

## Boundary

- This gate keeps OKF at metadata-only unless explicit admission evidence exists.
- KDS/Git controlled documents remain the source of record.
- This evidence does not approve summaries and does not upgrade business, acceptance or integration status.
"""
    write_text(MD_OUT, content)


def main() -> int:
    report = validate()
    write_text(JSON_OUT, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_markdown(report)
    print(
        "okf_summary_admission_gate={status} concepts={concepts} "
        "approved_summaries={approved} pending_requests={pending} approved_requests={approved_requests} "
        "sensitive_hits={sensitive} violations={violations}".format(
            status=report["status"],
            concepts=report["concepts"],
            approved=report["approved_summaries"],
            pending=report["pending_requests"],
            approved_requests=report["approved_requests"],
            sensitive=report["sensitive_hits"],
            violations=len(report["violations"]),
        )
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
