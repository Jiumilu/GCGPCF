#!/usr/bin/env python3
"""Build the Headroom LCX next-stage real-measurement authorization package."""

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

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001.md"
KDS_OUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json"
KDS_OUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md"
KDS_OUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001.md"

PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
WINDOW_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
WINDOW_GRANT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
FIELD_MAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
RUNNER_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json"
GAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
COMPLETION_JSON = EVIDENCE_DIR / "headroom-lcx-completion-audit-20260623.json"
BOUNDARY_JSON = EVIDENCE_DIR / "headroom-lcx-authorization-boundary-review-20260621.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_package() -> dict[str, Any]:
    precheck = load_json(PRECHECK_JSON)
    window = load_json(WINDOW_JSON)
    window_grant = load_json(WINDOW_GRANT_JSON)
    field_map = load_json(FIELD_MAP_JSON)
    runner = load_json(RUNNER_JSON)
    gap = load_json(GAP_JSON)
    completion = load_json(COMPLETION_JSON)
    boundary = load_json(BOUNDARY_JSON)

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001",
        "date": "2026-06-23",
        "status": "next_stage_authorization_package_granted_precheck_only",
        "scope": "bridge_precheck_complete_to_real_measurement_window_request",
        "project_count": 15,
        "projects": window.get("projects", []),
        "source_evidence": {
            "boundary_review": boundary.get("evidence_id"),
            "authorized_measurement_precheck": precheck.get("evidence_id"),
            "authorization_window_request": window.get("evidence_id"),
            "authorization_window_grant": window_grant.get("evidence_id"),
            "authorization_field_map": field_map.get("field_map_id"),
            "runner_contract": runner.get("contract_id"),
            "gap_matrix": gap.get("gap_id"),
            "completion_audit": completion.get("audit_id"),
        },
        "bridge_state": {
            "authorization_complete": precheck.get("precheck", {}).get("authorization_complete"),
            "missing_required_field_count": precheck.get("precheck", {}).get("missing_required_field_count"),
            "waes_harness_admitted": precheck.get("precheck", {}).get("waes_harness_admitted"),
            "real_measurement_window_requested": True,
            "real_measurement_window_granted": True,
            "real_measurement_open": False,
            "production_branch_blocked": True,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "required_next_decision": "open_real_measurement_window",
        "required_next_actions": [
            "obtain explicit human authorization window",
            "keep precheck-only boundary intact",
            "do not start production proxy or production SDK",
            "do not write real KDS or external API",
            "do not process sensitive material without redaction",
        ],
        "current_guard": {
            "real_measurement_gap_present": gap.get("gates", {}).get("real_measurement_gap_present", True),
            "production_branch_blocked": gap.get("gates", {}).get("production_branch_blocked", True),
            "production_token_measurement_allowed": gap.get("gates", {}).get("production_token_measurement_allowed", False),
            "measured_production_tokens": gap.get("gates", {}).get("measured_production_tokens", False),
            "production_admission_gate": gap.get("gates", {}).get("production_admission_gate", False),
            "accepted": gap.get("gates", {}).get("accepted", False),
            "integrated": gap.get("gates", {}).get("integrated", False),
            "production_ready": gap.get("gates", {}).get("production_ready", False),
        },
        "non_claims": {
            "not_real_measurement_window_granted": False,
            "not_real_measurement_open": True,
            "not_production_branch_open": True,
            "not_production_token_measurement": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "notes": [
            "This package bridges the completed sanitized precheck to the missing real measurement window decision.",
            "It is evidence of the next-stage bridge boundary, not evidence of execution.",
            "It keeps the production branch blocked until WAES/Harness issues a new real-measurement decision.",
        ],
    }


def write_outputs(pkg: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(pkg, ensure_ascii=False, indent=2) + "\n"
    OUT_JSON.write_text(json_text, encoding="utf-8")
    KDS_OUT_JSON.write_text(json_text, encoding="utf-8")

    md_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260623",
            "title: Headroom LCX Real Measurement Next-Stage Authorization Package Evidence",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement Next-Stage Authorization Package Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260623`",
            "",
            "## 结论",
            "",
            "授权测量前置检查已完成，真实测量授权窗口已预检授予，但仍未打开。",
            "status: next_stage_authorization_package_granted_precheck_only",
            "",
            "## 现状",
            "",
            "| item | value |",
            "|---|---|",
            f"| authorization_complete | `{str(pkg['bridge_state']['authorization_complete']).lower()}` |",
            f"| missing_required_field_count | `{pkg['bridge_state']['missing_required_field_count']}` |",
            f"| waes_harness_admitted | `{str(pkg['bridge_state']['waes_harness_admitted']).lower()}` |",
            f"| real_measurement_window_requested | `{str(pkg['bridge_state']['real_measurement_window_requested']).lower()}` |",
            f"| real_measurement_window_granted | `{str(pkg['bridge_state']['real_measurement_window_granted']).lower()}` |",
            f"| real_measurement_open | `{str(pkg['bridge_state']['real_measurement_open']).lower()}` |",
            f"| production_branch_blocked | `{str(pkg['bridge_state']['production_branch_blocked']).lower()}` |",
            f"| production_token_measurement_allowed | `{str(pkg['bridge_state']['production_token_measurement_allowed']).lower()}` |",
            f"| measured_production_tokens | `{str(pkg['bridge_state']['measured_production_tokens']).lower()}` |",
            f"| production_admission_gate | `{str(pkg['bridge_state']['production_admission_gate']).lower()}` |",
            f"| accepted | `{str(pkg['bridge_state']['accepted']).lower()}` |",
            f"| integrated | `{str(pkg['bridge_state']['integrated']).lower()}` |",
            f"| production_ready | `{str(pkg['bridge_state']['production_ready']).lower()}` |",
            "",
            "## 支撑证据",
            "",
            f"- boundary_review: `{pkg['source_evidence']['boundary_review']}`",
            f"- authorized_measurement_precheck: `{pkg['source_evidence']['authorized_measurement_precheck']}`",
            f"- authorization_window_request: `{pkg['source_evidence']['authorization_window_request']}`",
            f"- authorization_window_grant: `{pkg['source_evidence']['authorization_window_grant']}`",
            f"- authorization_field_map: `{pkg['source_evidence']['authorization_field_map']}`",
            f"- runner_contract: `{pkg['source_evidence']['runner_contract']}`",
            f"- gap_matrix: `{pkg['source_evidence']['gap_matrix']}`",
            f"- completion_audit: `{pkg['source_evidence']['completion_audit']}`",
            "",
            "## 下一步决策",
            "",
            f"`{pkg['required_next_decision']}`",
            "",
            "## 下一步动作",
            "",
        ]
        + [f"- {action}" for action in pkg["required_next_actions"]]
        + [
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实测量授权窗口已打开。",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示生产代理、生产 SDK、真实 KDS 写入或真实外部 API 写入已开启。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md_text, encoding="utf-8")
    KDS_OUT_MD.write_text(md_text, encoding="utf-8")

    loop_text = dedent(
        f"""\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001
        title: "循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # 循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-NEXT-STAGE-AUTHORIZATION-PACKAGE-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json`
        - `docs/harness/evidence/headroom-lcx-completion-audit-20260623.json`

        ## 动作

        - 把“预检已完成、真实窗口未开”整理成单一桥接包。
        - bridge_precheck_complete_to_real_measurement_window_request
        - obtain explicit human authorization window
        - keep precheck-only boundary intact
        - do not start production proxy or production SDK
        - 维持 production branch blocked。
        - 不把桥接包写成真实测量执行。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.md`
        - `tools/kds-sync/build_headroom_lcx_real_measurement_next_stage_authorization_package.py`
        - `tools/kds-sync/validate_headroom_lcx_real_measurement_next_stage_authorization_package.py`

        ## 检查

        ```bash
        python3 tools/kds-sync/validate_headroom_lcx_real_measurement_next_stage_authorization_package.py
        ```

        ## 反馈

        桥接包将预检完成状态与真实窗口缺口收束到同一入口，但不改变 blocked 状态。

        ## 下一轮

        继续等待 WAES/Harness 的真实授权窗口裁决，或在获批后再切到真实测量 runner。
        """
    ).strip() + "\n"
    OUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    pkg = build_package()
    write_outputs(pkg)
    print(
        "headroom_lcx_real_measurement_next_stage_authorization_package=generated "
        "real_measurement_window_requested=true real_measurement_window_granted=true "
        "real_measurement_open=false production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
