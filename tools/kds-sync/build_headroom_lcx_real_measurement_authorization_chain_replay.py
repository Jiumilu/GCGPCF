#!/usr/bin/env python3
"""Build Headroom LCX real-measurement authorization chain replay evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-chain-replay-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-chain-replay-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001.md"

REQUEST = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-request-20260623.json"
FIELD_MAP = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-field-map-20260623.json"
SIGNED_BUNDLE = EVIDENCE_DIR / "headroom-lcx-real-measurement-approval-signed-bundle-20260623.json"
WINDOW_GRANT = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-grant-20260623.json"
LEDGER = EVIDENCE_DIR / "headroom-lcx-sanitized-production-usage-ledger-20260623.json"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_chain_replay() -> dict[str, Any]:
    request = load_json(REQUEST)
    field_map = load_json(FIELD_MAP)
    signed_bundle = load_json(SIGNED_BUNDLE)
    window_grant = load_json(WINDOW_GRANT)
    ledger = load_json(LEDGER)

    signed_auth = signed_bundle.get("authorization_fields", {})
    ledger_ref = LEDGER.relative_to(ROOT).as_posix()
    field_rows = field_map.get("field_map", [])
    request_bindings = request.get("field_bindings", [])

    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001",
        "date": "2026-06-23",
        "status": "authorization_chain_replayed_precheck_only",
        "scope": "real_measurement_authorization_chain_replay_no_execution",
        "project_count": 15,
        "projects": PROJECTS,
        "ledger_reference": ledger_ref,
        "chain": [
            {
                "step": "authorization_request",
                "evidence_id": request.get("evidence_id"),
                "status": request.get("status"),
                "ledger_reference": next(
                    item.get("current_value")
                    for item in request_bindings
                    if item.get("field") == "sanitized_production_token_ledger"
                ),
                "state": request.get("current_state", {}),
            },
            {
                "step": "authorization_field_map",
                "evidence_id": field_map.get("field_map_id"),
                "status": field_map.get("status"),
                "ledger_reference": next(
                    item.get("current_value")
                    for item in field_rows
                    if item.get("field") == "sanitized_production_token_ledger"
                ),
                "state": field_map.get("current_state", {}),
            },
            {
                "step": "approval_signed_bundle",
                "evidence_id": signed_bundle.get("evidence_id"),
                "status": signed_bundle.get("status"),
                "ledger_reference": signed_auth.get("sanitized_production_token_ledger"),
                "state": signed_bundle.get("completion_flags", {}),
            },
            {
                "step": "authorization_window_grant",
                "evidence_id": window_grant.get("evidence_id"),
                "status": window_grant.get("status"),
                "ledger_reference": window_grant.get("sanitized_production_token_ledger"),
                "state": {
                    "real_measurement_window_granted": window_grant.get("real_measurement_window_granted"),
                    "real_measurement_open": window_grant.get("real_measurement_open"),
                    "production_branch_blocked": window_grant.get("production_branch_blocked"),
                    "production_token_measurement_allowed": window_grant.get("production_token_measurement_allowed"),
                    "measured_production_tokens": window_grant.get("measured_production_tokens"),
                    "production_admission_gate": window_grant.get("production_admission_gate"),
                    "accepted": window_grant.get("accepted"),
                    "integrated": window_grant.get("integrated"),
                    "production_ready": window_grant.get("production_ready"),
                },
            },
            {
                "step": "sanitized_usage_ledger",
                "evidence_id": ledger.get("ledger_id"),
                "status": "metadata_only_no_production_measurement",
                "ledger_reference": ledger_ref,
                "state": {
                    "telemetry": ledger.get("telemetry"),
                    "sensitive_raw_text_stored": ledger.get("sensitive_raw_text_stored"),
                    "measured_production_tokens": ledger.get("measured_production_tokens"),
                    "production_token_measurement_allowed": ledger.get("production_token_measurement_allowed"),
                },
            },
        ],
        "chain_gate": {
            "same_ledger_reference": True,
            "real_measurement_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_real_measurement_execution": True,
            "not_production_proxy_start": True,
            "not_production_sdk_enablement": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_business_equivalence_proven": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
    }


def write_outputs(replay: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(replay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    chain_rows = [
        f"| {item['step']} | `{item['evidence_id']}` | `{item['ledger_reference']}` | `{item['status']}` |"
        for item in replay["chain"]
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623",
            "title: Headroom LCX Real Measurement Authorization Chain Replay Evidence",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement Authorization Chain Replay Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623`",
            "",
            "## 结论",
            "",
            "真实测量授权链已完成 precheck-only 回放，统一引用同一份脱敏 usage ledger，但未打开真实测量窗口，不允许生产 token 测量。",
            "status: authorization_chain_replayed_precheck_only",
            "",
            "## 链路",
            "",
            "| step | evidence_id | ledger_reference | status |",
            "|---|---|---|---|",
            *chain_rows,
            "",
            "## 门禁",
            "",
            "| item | value |",
            "|---|---|",
            f"| same_ledger_reference | `{str(replay['chain_gate']['same_ledger_reference']).lower()}` |",
            f"| real_measurement_open | `{str(replay['chain_gate']['real_measurement_open']).lower()}` |",
            f"| production_token_measurement_allowed | `{str(replay['chain_gate']['production_token_measurement_allowed']).lower()}` |",
            f"| measured_production_tokens | `{str(replay['chain_gate']['measured_production_tokens']).lower()}` |",
            f"| production_admission_gate | `{str(replay['chain_gate']['production_admission_gate']).lower()}` |",
            f"| accepted | `{str(replay['chain_gate']['accepted']).lower()}` |",
            f"| integrated | `{str(replay['chain_gate']['integrated']).lower()}` |",
            f"| production_ready | `{str(replay['chain_gate']['production_ready']).lower()}` |",
            "",
            "## 非声明",
            "",
            "- 本回放不表示真实测量已执行。",
            "- 本回放不表示生产代理或生产 SDK 已启动。",
            "- 本回放不表示真实 KDS 写入或外部 API 写入。",
            "- 本回放不表示 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement Authorization Chain Replay 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement Authorization Chain Replay 001",
            "",
            "## 输入",
            "",
            "- authorization request",
            "- authorization field map",
            "- approval signed bundle",
            "- authorization window grant",
            "- sanitized usage ledger",
            "",
            "## 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_authorization_chain_replay.py`",
            "- 回放授权链路并检查统一 ledger 引用。",
            "- 保持 precheck-only 和生产阻断状态。",
            "",
            "## 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md`",
            "",
            "## 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_chain_replay.py`",
            "",
            "## 反馈",
            "",
            "本轮只形成授权链回放证据，不打开真实测量窗口，不进入生产准入。",
            "",
            "## 下一轮",
            "",
            "若继续推进，只能生成真实测量执行前的外部授权回执模板或保持 blocked 状态。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    replay = build_chain_replay()
    ledger_refs = {item["ledger_reference"] for item in replay["chain"]}
    require(ledger_refs == {replay["ledger_reference"]}, "ledger references must be unified")
    write_outputs(replay)
    print(
        "headroom_lcx_real_measurement_authorization_chain_replay=generated "
        "project_count=15 same_ledger_reference=true real_measurement_open=false "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
