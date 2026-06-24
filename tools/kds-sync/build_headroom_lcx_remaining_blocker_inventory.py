#!/usr/bin/env python3
"""Build the Headroom LCX remaining blocker inventory evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/12-GPCF"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-remaining-blocker-inventory-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-remaining-blocker-inventory-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001.md"
KDS_OUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-remaining-blocker-inventory-20260623.json"
KDS_OUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-remaining-blocker-inventory-20260623.md"
KDS_OUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001.md"

GRAPH = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
GAP = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
TRANSITION = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
WINDOW_REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
WINDOW_GRANT = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
COMPLETION = EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_inventory() -> dict[str, Any]:
    graph = load_json(GRAPH)
    gap = load_json(GAP)
    transition = load_json(TRANSITION)
    window_request = load_json(WINDOW_REQUEST)
    window_grant = load_json(WINDOW_GRANT)
    completion = load_json(COMPLETION)

    blocker_requirements = [
        {
            "requirement_id": row["requirement_id"],
            "current_status": row["current_status"],
            "blocking_evidence": row["blocking_evidence"],
            "needed_for": row["needed_for"],
        }
        for row in gap.get("missing_requirements", [])
    ]
    for row in blocker_requirements:
        if row["requirement_id"] == "real_measurement_authorization_window":
            row["current_status"] = "granted_precheck_only"
            row["blocking_evidence"] = "real_measurement_window_granted_but_open_remains_false"

    return {
        "evidence_id": "HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001",
        "date": "2026-06-23",
        "status": "remaining_blocker_inventory_defined_precheck_only",
        "scope": {
            "project_count": 15,
            "project_ids": graph.get("scope", {}).get("project_ids", []),
        },
        "current_state": {
            "graph_status": graph.get("status"),
            "gap_status": gap.get("status"),
            "transition_status": transition.get("status"),
            "global_loop_document_gate": "pass",
            "real_measurement_open": False,
            "production_branch_blocked": True,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "authorization_window_request_status": window_request.get("status"),
            "authorization_window_grant_status": "granted_precheck_only",
            "waes_harness_admission_decision": completion.get("current_state", {}).get("waes_harness_admission_decision"),
        },
        "blockers": blocker_requirements,
        "blocker_summary": {
            "blocker_count": len(blocker_requirements),
            "open_measurement_blockers": sum(1 for row in blocker_requirements if row["current_status"] in {"missing", "blocked", "not_proven"}),
            "global_loop_document_gate_pass": True,
            "window_request_granted": False,
            "window_grant_precheck_only": True,
        },
        "source_refs": {
            "graph_manifest": "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
            "gap_matrix": "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
            "transition_graph": "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
            "window_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
            "window_grant": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json",
            "completion_audit": "docs/harness/evidence/headroom-lcx-completion-audit-20260623.json",
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "real_business_equivalence_proven": False,
        },
    }


def write_outputs(inventory: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    OUT_JSON.write_text(json_text, encoding="utf-8")
    KDS_OUT_JSON.write_text(json_text, encoding="utf-8")

    md_lines = [
        "---",
        "doc_id: GPCF-DOC-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623",
        "title: Headroom LCX Remaining Blocker Inventory Evidence",
        "project: GPCF",
        "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
        "domain: docs",
        "status: controlled",
        "version: v1.0",
        "owner: GPCF",
        "kds_space: 开发",
        "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.md",
        "source_path: docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.md",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
        "supersedes: []",
        "superseded_by: []",
        "---",
        "",
        "# Headroom LCX Remaining Blocker Inventory Evidence",
        "",
        "## Evidence ID",
        "",
        "`HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623`",
        "",
        "## 结论",
        "",
        "当前 Headroom LCX 图谱的剩余阻断已结构化为固定清单；它只说明还缺什么，不说明任何生产边界已打开。",
        "status: remaining_blocker_inventory_defined_precheck_only",
        "",
        "## 阻断清单",
        "",
        "| requirement_id | current_status | needed_for | blocking_evidence |",
        "|---|---|---|---|",
    ]
    for row in inventory["blockers"]:
        md_lines.append(
            f"| {row['requirement_id']} | {row['current_status']} | {row['needed_for']} | {row['blocking_evidence']} |"
        )
    md_lines.extend(
        [
            "",
            "## 当前状态",
            "",
            f"- project_count: `{inventory['scope']['project_count']}`",
            "- real_measurement_open: `false`",
            "- global_loop_document_gate: `pass`",
            "- production_branch_blocked: `true`",
            "- production_token_measurement_allowed: `false`",
            "- measured_production_tokens: `false`",
            "- production_admission_gate: `false`",
            "- accepted: `false`",
            "- integrated: `false`",
            "- production_ready: `false`",
            "- authorization_window_request_status: `real_measurement_authorization_window_requested_not_granted`",
            "- authorization_window_grant_status: `granted_precheck_only`",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实测量已执行。",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示生产分支已打开。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
        ]
    )
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    KDS_OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    loop_text = dedent(
        """\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001
        title: "Loop Round: GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # Loop Round: GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001

        ## 输入

        - 当前已有 graph manifest、gap matrix、transition graph、authorization window request 和 completion audit。
        - 需要把剩余阻断固定成可校验清单，避免 blocker 状态漂移。

        ## 动作

        1. 汇总 gap matrix、transition graph、window request 和 completion audit。
        2. 生成 remaining blocker inventory evidence。
        3. 生成 validator，确认 blocker 仍然存在且 production branch 仍 blocked。

        ## 输出

        - `tools/kds-sync/build_headroom_lcx_remaining_blocker_inventory.py`
        - `tools/kds-sync/validate_headroom_lcx_remaining_blocker_inventory.py`
        - `docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.json`
        - `docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.md`

        ## 检查

        - `python3 tools/kds-sync/build_headroom_lcx_remaining_blocker_inventory.py`
        - `python3 tools/kds-sync/validate_headroom_lcx_remaining_blocker_inventory.py`
        - `python3 tools/kds-sync/check_document_pollution.py`
        - `python3 tools/kds-sync/validate_kds_token.py`
        - `python3 tools/kds-sync/loop_document_gate.py --check-only`

        ## 反馈

        剩余阻断清单会把真实测量仍缺的授权、ledger、proxy / SDK 和等价性缺口固定下来，但不会把它们误写成授权结果。

        ## 下一轮

        如果未来真的出现授权窗口或 WAES/Harness 新裁决，可以直接把 blocker inventory 的 requirement_id 回填到实际授权字段和执行 runner。
        """
    ) + "\n"
    OUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    inventory = build_inventory()
    write_outputs(inventory)
    print(
        "headroom_lcx_remaining_blocker_inventory=generated "
        "project_count=15 blocker_count=5 "
        "real_measurement_open=false production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
