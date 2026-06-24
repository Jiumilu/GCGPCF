#!/usr/bin/env python3
"""Build the Headroom LCX real-measurement authorization window request evidence."""

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

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001.md"
KDS_OUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
KDS_OUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.md"
KDS_OUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001.md"

PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
FIELD_MAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-request-20260623.json"
TRANSITION_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-transition-graph-20260623.json"
GAP_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-gap-matrix-20260623.json"


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
    field_map = load_json(FIELD_MAP_JSON)
    request = load_json(REQUEST_JSON)
    transition = load_json(TRANSITION_JSON)
    gap = load_json(GAP_JSON)

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001",
        "date": "2026-06-23",
        "status": "real_measurement_authorization_window_requested_not_granted",
        "scope": "requested_window_precheck_only",
        "project_count": 15,
        "projects": request.get("projects", []),
        "requested_window_id": field_map.get("current_state", {}).get("authorization_window_id", "LCX-MEASURE-20260622-001"),
        "requested_by": field_map.get("current_state", {}).get("authorized_by", "lujunxiang / GPCF owner"),
        "requested_at": field_map.get("current_state", {}).get("authorized_at", "2026-06-22T08:42:06+08:00"),
        "requested_future_decision": request.get("requested_future_decision"),
        "current_waes_harness_admission_decision": precheck.get("waes_harness_admission_decision"),
        "authorization_complete": False,
        "real_measurement_open": False,
        "production_branch_blocked": True,
        "production_token_measurement_allowed": False,
        "measured_production_tokens": False,
        "production_admission_gate": False,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "source_refs": {
            "precheck": "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
            "field_map": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json",
            "authorization_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json",
            "transition_graph": "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
            "gap_matrix": "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "transition_anchor": {
            "transition_graph_id": transition.get("transition_graph_id"),
            "transition_graph_status": transition.get("status"),
        },
        "gap_anchor": {
            "gap_id": gap.get("gap_id"),
            "real_measurement_gap_present": gap.get("gates", {}).get("real_measurement_gap_present", True),
        },
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623",
            "title: Headroom LCX 真实测量授权窗口请求证据",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX 真实测量授权窗口请求证据",
            "",
            "## 证据 ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623`",
            "",
            "## 结论",
            "",
            "已请求真实测量授权窗口，但当前仍未授予；该请求只作为 precheck-only 边界证据，不打开 production branch。",
            "status: real_measurement_authorization_window_requested_not_granted",
            "",
            "## 请求字段",
            "",
            "| field | value |",
            "|---|---|",
            f"| requested_window_id | `{pkg['requested_window_id']}` |",
            f"| requested_by | `{pkg['requested_by']}` |",
            f"| requested_at | `{pkg['requested_at']}` |",
            f"| requested_future_decision | `{pkg['requested_future_decision']}` |",
            f"| current_waes_harness_admission_decision | `{pkg['current_waes_harness_admission_decision']}` |",
            "",
            "## 当前状态",
            "",
            "| state | value |",
            "|---|---|",
            f"| real_measurement_open | `{str(pkg['real_measurement_open']).lower()}` |",
            f"| production_branch_blocked | `{str(pkg['production_branch_blocked']).lower()}` |",
            f"| production_token_measurement_allowed | `{str(pkg['production_token_measurement_allowed']).lower()}` |",
            f"| measured_production_tokens | `{str(pkg['measured_production_tokens']).lower()}` |",
            f"| production_admission_gate | `{str(pkg['production_admission_gate']).lower()}` |",
            f"| accepted | `{str(pkg['accepted']).lower()}` |",
            f"| integrated | `{str(pkg['integrated']).lower()}` |",
            f"| production_ready | `{str(pkg['production_ready']).lower()}` |",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实授权窗口已打开。",
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
        doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001
        title: "循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001"
        project: GPCF
        related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
        domain: docs
        status: controlled
        version: v1.0
        owner: GPCF
        kds_space: 开发
        kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001.md
        source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001.md
        sync_direction: bidirectional
        last_reviewed: 2026-06-23
        supersedes: []
        superseded_by: []
        ---

        # 循环回合：GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-001

        ## 输入

        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json`

        ## 动作

        - 把真实测量授权窗口请求显式记录为 requested_not_granted。
        - 保持 production branch blocked，保留 precheck-only 边界。
        - 不把请求包写成授权已授予。

        ## 输出

        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`
        - `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md`
        - `tools/kds-sync/build_headroom_lcx_real_measurement_authorization_window_request.py`
        - `tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_window_request.py`

        ## 检查

        ```bash
        python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_window_request.py
        ```

        ## 反馈

        authorization window request 已被显式记录，但该请求包只增加窗口请求证据，不改变当前 blocked 状态。

        ## 下一轮

        等待 WAES/Harness 对真实授权窗口做出新的裁决，或继续把窗口请求纳入总图谱引用。
        """
    ).strip() + "\n"
    OUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    pkg = build_package()
    write_outputs(pkg)
    print(
        "headroom_lcx_real_measurement_authorization_window_request=generated "
        "real_measurement_open=false production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
