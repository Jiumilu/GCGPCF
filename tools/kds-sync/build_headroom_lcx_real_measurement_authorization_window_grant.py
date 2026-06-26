#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement authorization window grant evidence."""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/12-GPCF"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001.md"
KDS_OUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
KDS_OUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.md"
KDS_OUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001.md"

APPROVAL_INSTANCE = EVIDENCE_DIR / "headroom-lcx-approval-instance-precheck-20260622.json"
SIGNED_BUNDLE = EVIDENCE_DIR / "headroom-lcx-real-measurement-approval-signed-bundle-20260623.json"
REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-request-20260623.json"
WINDOW_REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
TRANSITION = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
GAP = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"
RUNNER_CONTRACT = EVIDENCE_DIR / "headroom-lcx-real-measurement-runner-contract-20260623.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_headroom_lcx_real_measurement_authorization_window_grant() -> dict[str, Any]:
    approval = read_json(APPROVAL_INSTANCE)
    signed_bundle = read_json(SIGNED_BUNDLE)
    request = read_json(REQUEST)
    window_request = read_json(WINDOW_REQUEST)
    transition = read_json(TRANSITION)
    gap = read_json(GAP)
    runner = read_json(RUNNER_CONTRACT)

    fields = signed_bundle.get("authorization_fields", {})
    grant = {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001",
        "date": "2026-06-23",
        "status": "real_measurement_authorization_window_granted_precheck_only",
        "scope": "precheck_only_no_measurement",
        "project_count": 15,
        "projects": approval.get("projects", []),
        "requested_future_decision": request.get("requested_future_decision"),
        "requested_window_id": fields.get("authorized_window_id"),
        "authorized_window_id": fields.get("authorized_window_id"),
        "authorized_by": fields.get("authorized_by"),
        "authorized_at": fields.get("authorized_at"),
        "sanitized_production_token_ledger": fields.get("sanitized_production_token_ledger"),
        "rollback_plan_id": fields.get("rollback_plan_id"),
        "waes_harness_admission_decision": fields.get("waes_harness_admission_decision"),
        "real_measurement_window_granted": True,
        "real_measurement_open": False,
        "production_branch_blocked": True,
        "production_token_measurement_allowed": False,
        "measured_production_tokens": False,
        "production_admission_gate": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "source_refs": {
            "approval_instance": approval.get("evidence_id"),
            "signed_bundle": signed_bundle.get("evidence_id"),
            "authorization_request": request.get("evidence_id"),
            "authorization_window_request": window_request.get("evidence_id"),
            "transition_graph": transition.get("transition_graph_id"),
            "gap_matrix": gap.get("gap_id"),
            "runner_contract": runner.get("contract_id"),
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "real_kds_api_write": False,
        },
    }
    return grant


def write_outputs(grant: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(grant, ensure_ascii=False, indent=2) + "\n"
    OUT_JSON.write_text(json_text, encoding="utf-8")
    KDS_OUT_JSON.write_text(json_text, encoding="utf-8")

    md_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623",
            "title: Headroom LCX 真实测量授权窗口授予证据",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX 真实测量授权窗口授予证据",
            "",
            "## 证据 ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623`",
            "",
            "## 结论",
            "",
            "真实测量授权窗口已被记录为授予，但当前仍保持 precheck-only，不打开 production branch，也不允许生产 token 测量。",
            "status: real_measurement_authorization_window_granted_precheck_only",
            "",
            "## 授权字段",
            "",
            "| field | value |",
            "|---|---|",
            f"| authorized_window_id | `{grant['authorized_window_id']}` |",
            f"| authorized_by | `{grant['authorized_by']}` |",
            f"| authorized_at | `{grant['authorized_at']}` |",
            f"| sanitized_production_token_ledger | `{grant['sanitized_production_token_ledger']}` |",
            f"| rollback_plan_id | `{grant['rollback_plan_id']}` |",
            f"| waes_harness_admission_decision | `{grant['waes_harness_admission_decision']}` |",
            "",
            "## 当前状态",
            "",
            "| state | value |",
            "|---|---|",
            f"| real_measurement_window_granted | `{str(grant['real_measurement_window_granted']).lower()}` |",
            f"| real_measurement_open | `{str(grant['real_measurement_open']).lower()}` |",
            f"| production_branch_blocked | `{str(grant['production_branch_blocked']).lower()}` |",
            f"| production_token_measurement_allowed | `{str(grant['production_token_measurement_allowed']).lower()}` |",
            f"| measured_production_tokens | `{str(grant['measured_production_tokens']).lower()}` |",
            f"| production_admission_gate | `{str(grant['production_admission_gate']).lower()}` |",
            f"| accepted | `{str(grant['accepted']).lower()}` |",
            f"| integrated | `{str(grant['integrated']).lower()}` |",
            f"| production_ready | `{str(grant['production_ready']).lower()}` |",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示 production branch 已打开。",
            "- 本证据不表示生产代理、生产 SDK 或真实 KDS 写入已开启。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md_text, encoding="utf-8")
    KDS_OUT_MD.write_text(md_text, encoding="utf-8")

    loop_text = dedent(
        f"""\
        ---
        doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001
        title: "循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # 循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`

        ## 动作

        - `python3 tools/kds-sync/build_headroom_lcx_real_measurement_authorization_window_grant.py`
        - 记录 authorization window grant。
        - 将授权窗口记录为 granted，但仍保持 precheck-only。
        - 保持 production_branch_blocked=true。
        - 不把窗口授予写成生产放行。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md`

        ## 检查

        - `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_window_grant.py`

        ## 反馈

        本轮只补齐真实测量 authorization window grant 的受控记录，granted but still precheck-only，不打开 production branch，不允许真实生产 token 测量。

        ## 下一轮

        若后续要继续推进真实测量执行，再补 token ledger replay 与 WAES/Harness 进一步裁决。
        """
    ).strip() + "\n"
    OUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    grant = build_headroom_lcx_real_measurement_authorization_window_grant()
    write_outputs(grant)
    print(
        "headroom_lcx_real_measurement_authorization_window_grant=generated "
        "project_count=15 real_measurement_window_granted=true real_measurement_open=false "
        "production_branch_blocked=true production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
