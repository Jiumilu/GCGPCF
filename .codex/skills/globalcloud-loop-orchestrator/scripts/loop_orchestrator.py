#!/usr/bin/env python3
"""Suggest the next GlobalCloud Loop action from local governance state."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
HEALTH_REPORT = ROOT / "09-status/globalcloud-document-health-report.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-loop-orchestrator/scripts/loop_git_gate.py"
OPERATIONAL_GATES = ROOT / ".codex/skills/globalcloud-loop-orchestrator/scripts/loop_operational_gates.py"
LOOP_STATE = ROOT / "docs/harness/loop-state.md"
LOOP_CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
LOOP_AUTONOMY_POLICY = ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"
KDS_TOKEN_VALIDATOR = ROOT / "tools/kds-sync/validate_kds_token.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_gate(text: str) -> str:
    match = re.search(r"Loop 文档门禁：`?([^`\n]+)`?", text)
    if match:
        return match.group(1).strip()
    if "gate=blocked" in text or '"gate": "blocked"' in text:
        return "blocked"
    return "unknown"


def parse_projects(matrix: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in matrix.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) < 13 or cols[0] in {"#", "---"}:
            continue
        if not cols[0].isdigit():
            continue
        rows.append(
            {
                "index": cols[0],
                "name": cols[1],
                "code": cols[2],
                "position": cols[3],
                "agent": cols[4],
                "manifest": cols[5],
                "loop_state": cols[6],
                "rounds": cols[7],
                "evidence": cols[8],
                "status": cols[9],
                "blockers": cols[10],
                "harness": cols[11],
                "next": cols[12],
            }
        )
    return rows


def kds_token_status() -> dict[str, object]:
    if not KDS_TOKEN_VALIDATOR.exists():
        return {"gate": "unknown", "reason": "validate_kds_token.py missing"}
    proc = subprocess.run(
        ["python3", str(KDS_TOKEN_VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = (proc.stdout + proc.stderr).strip()
    return {
        "gate": "pass" if proc.returncode == 0 else "blocked",
        "output": output,
    }


def kds_token_deferred_for_local_dev() -> bool:
    status = kds_token_status()
    if status.get("gate") == "pass":
        return False
    text = read(LOOP_STATE)
    return "KDS TOKEN" in text and "暂缓" in text


def loop_governance_docs_status() -> dict[str, object]:
    required = [LOOP_CONTROL_BOARD, LOOP_AUTONOMY_POLICY]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    policy = read(LOOP_AUTONOMY_POLICY)
    l3_policy_ready = "最多 15 轮或 2 小时" in policy and "Git push" in policy and "真实 API 写入" in policy
    return {
        "gate": "pass" if not missing and l3_policy_ready else "blocked",
        "missing": missing,
        "l3_policy_ready": l3_policy_ready,
        "required_reads": [
            "AGENTS.md",
            "02-governance/loop/LOOP_CONTROL_BOARD.md",
            "02-governance/loop/LOOP_AUTONOMY_POLICY.md",
            "latest docs/harness/loops/loop-round-*.md",
            "09-status/gpcf-project-status-matrix.md",
            "git status",
        ],
    }


def recommend(projects: list[dict[str, str]], gate: str) -> dict[str, object]:
    if gate == "blocked" and kds_token_deferred_for_local_dev():
        gfis = next((project for project in projects if project.get("code") == "GF"), None)
        if gfis and gfis.get("loop_state") == "是" and gfis.get("evidence") in {"80%", "85%", "88%", "90%", "92%", "94%", "96%", "97%", "98%", "99%", "100%"}:
            if gfis.get("rounds") == "30":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-030 created UAT issue disposition closure and waiver review rules, but no real sample, UAT signoff or cross-project confirmation has been received yet.",
                    "recommended_action": "Create audit-preparation rules for received signoff evidence covering evidence source, signer, issue disposition, waiver review, redaction status and next action; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-031",
                }
            if gfis.get("rounds") == "29":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-029 created sample submission package acceptance rules and redaction review checklist, but no real sample, UAT signoff or cross-project confirmation has been received yet.",
                    "recommended_action": "Create UAT issue disposition closure and waiver review rules covering severity, owner, decision, waiver reason, evidence path and next action; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-030",
                }
            if gfis.get("rounds") == "28":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-028 created the field-sample return tracking ledger and UAT issue severity template, but no real sample, UAT signoff or cross-project confirmation has been received yet.",
                    "recommended_action": "Create sample submission package acceptance rules and redaction review checklist covering package completeness, redaction result, issue severity, waiver reason and next action; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-029",
                }
            if gfis.get("rounds") == "27":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-027 prepared UAT, real-field-sample and cross-project signoff dispatch packages, but no sample, signoff or confirmation has been received yet.",
                    "recommended_action": "Create a field-sample return tracking ledger and UAT issue severity template covering received status, signer, issue severity, waiver reason and next action; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-028",
                }
            if gfis.get("rounds") == "26":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-026 converted migration-window authorization, backup, restore, rollback, cleanup, stop, UAT, cross-project signoff and KDS security sync into a controlled confirmation register, but every required human confirmation remains open and ready_to_execute is false.",
                    "recommended_action": "Create a UAT and real-field-sample signoff request pack plus cross-project confirmation dispatch list covering factory, production, quality, warehouse, GPC, Finance and WAES owners; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-027",
                }
            if gfis.get("rounds") == "25":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-025 captured pre-authorization read-only evidence and confirmed diff/runtime/sensitive checks pass, but migration authorization, backup/restore evidence and human confirmation remain missing.",
                    "recommended_action": "Create a migration-execution confirmation register and human-confirmation checklist covering authorization, backup, restore, rollback owner, cleanup owner, stop owner, UAT and cross-project signoffs; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-026",
                }
            if gfis.get("rounds") == "24":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-024 created the migration-window authorization record and dry-run runbook with authorization flags still false, but read-only pre-authorization evidence is not captured in a controlled pack.",
                    "recommended_action": "Create a pre-authorization read-only evidence package covering Git status, diff check, quality, runtime read-only checks, sensitive-file scan and unresolved blockers; do not execute bench/migrate, schema sync, write API or external integration.",
                    "next_round": "GPCF-GF-LR-025",
                }
            if gfis.get("rounds") == "23":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-023 created the runtime migration preflight package, but the migration-window authorization record and dry-run runbook are not controlled yet.",
                    "recommended_action": "Create a migration-window authorization record and dry-run runbook covering approvers, backup, rollback, cleanup and stop conditions; do not execute bench/migrate, production writes or external integration.",
                    "next_round": "GPCF-GF-LR-024",
                }
            if gfis.get("rounds") == "22":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-022 generated the P0 gap closure matrix and clarified remaining UAT, runtime, production and cross-project blockers, but the migration preflight package is not prepared.",
                    "recommended_action": "Create a runtime migration preflight package listing bench/migrate prerequisites, rollback plan, sample requirements and human confirmation points; do not execute bench/migrate or external writes.",
                    "next_round": "GPCF-GF-LR-023",
                }
            if gfis.get("rounds") == "21":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-021 added outbound/POD boundary fields and kept finance facts L4_blocked, but the LR-016/LR-017 P0 gap closure matrix has not been regenerated.",
                    "recommended_action": "Generate a P0 gap closure matrix across LR-016 and LR-017 showing code-draft coverage, remaining cross-project confirmations and runtime/UAT blockers.",
                    "next_round": "GPCF-GF-LR-022",
                }
            if gfis.get("rounds") == "20":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-020 added Stock Entry inventory field drafts while forbidding real inventory posting, but outbound/POD finance boundary smoke remains open.",
                    "recommended_action": "Draft outbound/POD boundary fields and finance L4 gate smoke so GFIS only produces evidence-package suggestions and never auto-confirms receivables, credit, payment or collection.",
                    "next_round": "GPCF-GF-LR-021",
                }
            if gfis.get("rounds") == "19":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-019 added Transition Ledger exception and rework field drafts while preserving WAES recovery gate ownership, but Stock Entry inventory fact fields remain open.",
                    "recommended_action": "Select the Stock Entry inbound inventory minimal batch and draft batch, location, quantity, transaction type and source work-order fields with a validator; do not write real inventory.",
                    "next_round": "GPCF-GF-LR-020",
                }
            if gfis.get("rounds") == "18":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-018 selected the minimal implementation batch and added 11 Work Order / Quality Inspection custom-field drafts, but transition-ledger exception and rework fields remain open.",
                    "recommended_action": "Draft the GCFIS Work Order Transition Ledger exception/rework fields with a validator while preserving WAES gate ownership; do not run bench/migrate or external writes.",
                    "next_round": "GPCF-GF-LR-019",
                }
            if gfis.get("rounds") == "17":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-017 converted the 8 P0 gaps into a controlled implementation task package, but no implementation batch has been selected or validated yet.",
                    "recommended_action": "Select the minimal implementation batch from the task pack and create Custom Field, Doctype or API contract drafts with validators; do not trigger runtime, production or external writes.",
                    "next_round": "GPCF-GF-LR-018",
                }
            if gfis.get("rounds") == "16":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-016 created a field-sample to Doctype/API gap mapping with 12 gaps and 8 P0 gaps, but the P0 implementation task package is not yet controlled.",
                    "recommended_action": "Convert the LR-016 P0 gaps into a controlled implementation task package covering field additions, API contract changes and Doctype draft priorities.",
                    "next_round": "GPCF-GF-LR-017",
                }
            if gfis.get("rounds") == "15":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-015 created the field-sample submission and redaction ingest gate, but real sample records and field-to-Doctype gap mapping are still missing.",
                    "recommended_action": "Create a field-sample to GFIS Doctype/API gap mapping template and validator so submitted samples can be converted into controlled implementation gaps.",
                    "next_round": "GPCF-GF-LR-016",
                }
            if gfis.get("rounds") == "14":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-014 created a blank field-sample workpack and validator, but real submitted samples, redaction checks and role signoffs are still missing.",
                    "recommended_action": "Create a real sample submission directory, redaction rules and ingest validator so submitted screenshots, scans or records can be checked before entering evidence.",
                    "next_round": "GPCF-GF-LR-015",
                }
            if gfis.get("rounds") == "13":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-013 created controlled field-sample and UAT preparation packs, but real field samples and role signoffs are still missing.",
                    "recommended_action": "Create a blank field-sample workpack and sample submission validator so real screenshots, scans, or field records can be ingested without polluting evidence.",
                    "next_round": "GPCF-GF-LR-014",
                }
            if gfis.get("rounds") == "12":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-012 closed the local runtime schema and persistence dry-run, but field samples, UAT, production and external integration evidence are still missing.",
                    "recommended_action": "Create field-sample capture templates and UAT confirmation pack with signoff evidence requirements and gap ownership.",
                    "next_round": "GPCF-GF-LR-013",
                }
            if gfis.get("rounds") == "11":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-011 passed runtime write API dry-run with cleanup, but runtime Dispatch Suggestion schema is not fully synchronized.",
                    "recommended_action": "Synchronize the runtime Doctype schema for Dispatch Suggestion, then rerun the controlled dry-run; otherwise create field-sample capture templates and UAT confirmation pack.",
                    "next_round": "GPCF-GF-LR-012",
                }
            if gfis.get("rounds") == "10" or gfis.get("evidence") == "99%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-010 fixed the local runtime baseline, but write API, UAT, production and external integration evidence are still missing.",
                    "recommended_action": "If the user explicitly confirms runtime write API, run a controlled dry-run with rollback evidence; otherwise create field-sample capture templates and UAT confirmation pack.",
                    "next_round": "GPCF-GF-LR-011",
                }
            if gfis.get("rounds") == "9":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-009 executed runtime preflight and found environment blockers before write API validation.",
                    "recommended_action": "Pin the local compose/image version, refresh container mounts to the current repo path, rerun prereq/app checks, or defer runtime changes and create field-sample/UAT pack.",
                    "next_round": "GPCF-GF-LR-010",
                }
            if gfis.get("rounds") == "8" or gfis.get("evidence") == "98%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-008 prepared runtime validation but execution still requires human confirmation.",
                    "recommended_action": "If the user confirms Docker/bench, run runtime preflight; otherwise create field-sample capture templates and UAT confirmation pack.",
                    "next_round": "GPCF-GF-LR-009",
                }
            if gfis.get("rounds") == "7" or gfis.get("evidence") == "97%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-007 aligned WAES gate-event fixtures and is ready for runtime validation preparation.",
                    "recommended_action": "Prepare runtime validation checklist and human confirmation pack without executing Docker/bench.",
                    "next_round": "GPCF-GF-LR-008",
                }
            if gfis.get("rounds") == "6" or gfis.get("evidence") == "96%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-006 closed P0 contract-draft gaps and is ready for WAES gate-event alignment.",
                    "recommended_action": "Create WAES gate event fixtures and align work-order transition ledger with blocked/allowed/waived decision semantics.",
                    "next_round": "GPCF-GF-LR-007",
                }
            if gfis.get("rounds") == "5" or gfis.get("evidence") == "94%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-005 API/Doctype executable gap list is ready for controlled contract-test implementation.",
                    "recommended_action": "Patch the GFIS interface contract, add fake-Frappe API contract tests, then draft guarded API/Doctype changes without touching runtime bench.",
                    "next_round": "GPCF-GF-LR-006",
                }
            if gfis.get("rounds") == "4" or gfis.get("evidence") == "92%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-004 machine-checkable work-order rules are ready for API/Doctype alignment.",
                    "recommended_action": "Align GFIS work-order rule validation with GCFIS API and Frappe Doctype drafts, then produce an executable gap list.",
                    "next_round": "GPCF-GF-LR-005",
                }
            if gfis.get("rounds") == "3" or gfis.get("evidence") == "88%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-003 business rules are ready to become machine-checkable artifacts.",
                    "recommended_action": "Convert GFIS-P0-001/GFIS-P0-002 into JSON Schema, fixtures, and validators.",
                    "next_round": "GPCF-GF-LR-004",
                }
            if gfis.get("rounds") == "2" or gfis.get("evidence") == "85%":
                return {
                    "mode": "local_development",
                    "reason": "KDS TOKEN is deferred for local development; GFIS LR-002 specification package is ready for P0 task execution.",
                    "recommended_action": "Execute GFIS-P0-001 production-demand-to-work-order mapping and GFIS-P0-002 work-order state machine.",
                    "next_round": "GPCF-GF-LR-003",
                }
            return {
                "mode": "local_development",
                "reason": "KDS TOKEN is deferred for local development; GFIS project-repo initialization is complete enough to continue local Loop development.",
                "recommended_action": "Generate GFIS data dictionary v0.1, interface contract draft, and minimal development task package.",
                "next_round": "GPCF-GF-LR-002",
            }
        return {
            "mode": "local_development",
            "reason": "KDS TOKEN is deferred for local development; formal KDS API sync and accepted/integrated upgrades remain blocked.",
            "recommended_action": "Continue GPCF-managed local Loop development and keep KDS TOKEN as a release/sync gate.",
            "next_round": "Convert GPCF-GF-LR-001 extraction package into GFIS Manifest and project-repo initialization files",
        }

    if gate == "blocked":
        return {
            "mode": "blocked",
            "reason": "KDS/document gate is blocked; status upgrade is not allowed.",
            "recommended_action": "Configure KDS dedicated token or continue only source-evidence preparation without state upgrade.",
            "next_round": "GPCF-CF-LR-001 or GPCF-GF-LR-001 as evidence-preparation only",
        }

    for project in projects:
        if project["name"].endswith("GPCF") or project["code"] == "CF":
            if project["loop_state"] == "否":
                return {
                    "mode": "initialize",
                    "project": project,
                    "recommended_action": "Create GPCF docs/harness/loop-state.md and first governance loop record.",
                    "next_round": "GPCF-CF-LR-001",
                }

    priority_codes = ["GF", "MM", "KD", "BR", "PK", "XC", "GP", "PV", "WA", "XD", "XG"]
    by_code = {p["code"]: p for p in projects}
    for code in priority_codes:
        project = by_code.get(code)
        if project and project["loop_state"] == "否":
            return {
                "mode": "initialize",
                "project": project,
                "recommended_action": f"Initialize {project['name']} loop-state and evidence directory.",
                "next_round": f"GPCF-{code}-LR-001",
            }

    return {
        "mode": "continue",
        "recommended_action": "Select the project with lowest evidence completeness and continue the next loop round.",
        "next_round": "inspect loop-state files",
    }


def git_gate() -> dict[str, object]:
    if not GIT_GATE.exists():
        return {"gate": "unknown", "reason": "loop_git_gate.py missing"}
    proc = subprocess.run(
        ["python3", str(GIT_GATE), str(ROOT)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        data = {"gate": "unknown", "raw": proc.stdout}
    if proc.stderr:
        data["stderr"] = proc.stderr.strip()
    return data


def operational_gates() -> dict[str, object]:
    if not OPERATIONAL_GATES.exists():
        return {"gate": "unknown", "reason": "loop_operational_gates.py missing"}
    proc = subprocess.run(
        ["python3", str(OPERATIONAL_GATES), str(ROOT)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError:
        data = {"gate": "unknown", "raw": proc.stdout}
    if proc.stderr:
        data["stderr"] = proc.stderr.strip()
    return data


def main() -> int:
    matrix = read(STATUS_MATRIX)
    health = read(HEALTH_REPORT)
    projects = parse_projects(matrix)
    gate = parse_gate(health)
    result = {
        "document_gate": gate,
        "loop_governance_docs": loop_governance_docs_status(),
        "kds_token_status": kds_token_status(),
        "kds_token_deferred_for_local_dev": kds_token_deferred_for_local_dev(),
        "git_gate": git_gate(),
        "operational_gates": operational_gates(),
        "project_count": len(projects),
        "status_counts": {},
        "recommendation": recommend(projects, gate),
    }
    for project in projects:
        result["status_counts"][project["status"]] = result["status_counts"].get(project["status"], 0) + 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
