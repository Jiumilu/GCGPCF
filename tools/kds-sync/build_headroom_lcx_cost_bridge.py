#!/usr/bin/env python3
"""Build the Headroom LCX cost bridge evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/12-GPCF"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-cost-bridge-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-cost-bridge-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md"
KDS_OUTPUT_JSON = KDS_EVIDENCE_DIR / "headroom-lcx-cost-bridge-20260623.json"
KDS_OUTPUT_MD = KDS_EVIDENCE_DIR / "headroom-lcx-cost-bridge-20260623.md"
KDS_OUTPUT_LOOP = KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md"

COST_MODEL = EVIDENCE_DIR / "headroom-cost-sensitivity-model-20260621.json"
LOOP_COST_SERIES = EVIDENCE_DIR / "headroom-loop-cost-observation-series-20260621.json"
INDEPENDENT_REPLAY = EVIDENCE_DIR / "headroom-independent-loop-round-replay-20260621.json"
METADATA_REPLAY = EVIDENCE_DIR / "headroom-lcx-metadata-replay-check-20260622.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_bridge() -> dict:
    cost_model = read_json(COST_MODEL)
    loop_series = read_json(LOOP_COST_SERIES)
    replay = read_json(INDEPENDENT_REPLAY)
    metadata_replay = read_json(METADATA_REPLAY)
    return {
        "evidence_id": "HEADROOM-LCX-COST-BRIDGE-20260623",
        "date": "2026-06-23",
        "status": "cost_bridge_defined_replay_only",
        "project_count": 15,
        "bridge_mode": "replay_only",
        "source_evidence": {
            "cost_sensitivity_model": cost_model.get("evidence_id"),
            "loop_cost_observation_series": loop_series.get("evidence_id"),
            "independent_replay": replay.get("evidence_id"),
            "metadata_replay_check": metadata_replay.get("evidence_id"),
        },
        "current_state": {
            "cost_sensitivity_gate": cost_model.get("gate", {}).get("cost_sensitivity_gate"),
            "series_gate": loop_series.get("decision", {}).get("loop_cost_observation_series_gate"),
            "independent_round_gate": replay.get("decision", {}).get("independent_round_gate"),
            "metadata_replay_gate": metadata_replay.get("gates", {}).get("metadata_replay_gate"),
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "bridge_summary": {
            "cost_model_saving_rate": cost_model.get("gate", {}).get("min_profile_saving_rate"),
            "series_runtime_saving_rate": loop_series.get("aggregate", {}).get("runtime_saving_rate"),
            "independent_replay_runtime_saving_rate": replay.get("aggregate", {}).get("runtime_saving_rate"),
        },
        "non_claims": {
            "real_measurement_open": False,
            "real_business_equivalence_proven": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "real_kds_api_write": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(bridge: dict) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(bridge, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_JSON.write_text(json_text, encoding="utf-8")
    KDS_OUTPUT_JSON.write_text(json_text, encoding="utf-8")

    md_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-COST-BRIDGE-20260623",
            "title: Headroom LCX Cost Bridge Evidence",
            "project: GPCF",
            "related_projects: [GPCF, KDS, WAES]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Cost Bridge Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-COST-BRIDGE-20260623`",
            "",
            "## 结论",
            "",
            "本证据只把 cost model、三窗口 loop cost observation series、independent replay 和 metadata replay 连接成 replay only 成本桥接层。",
            "它不产生真实生产 token 结论，也不打开 production branch。",
            "status: cost_bridge_defined_replay_only",
            "",
            "## 支撑证据",
            "",
            f"- `cost_sensitivity_model`: `{bridge['source_evidence']['cost_sensitivity_model']}`",
            f"- `loop_cost_observation_series`: `{bridge['source_evidence']['loop_cost_observation_series']}`",
            f"- `independent_replay`: `{bridge['source_evidence']['independent_replay']}`",
            f"- `metadata_replay_check`: `{bridge['source_evidence']['metadata_replay_check']}`",
            "",
            "## 当前状态",
            "",
            f"| bridge_mode | `{bridge['bridge_mode']}` |",
            f"| cost_sensitivity_gate | `{str(bridge['current_state']['cost_sensitivity_gate']).lower()}` |",
            f"| series_gate | `{str(bridge['current_state']['series_gate']).lower()}` |",
            f"| independent_round_gate | `{str(bridge['current_state']['independent_round_gate']).lower()}` |",
            f"| metadata_replay_gate | `{str(bridge['current_state']['metadata_replay_gate']).lower()}` |",
            f"| production_token_measurement_allowed | `{str(bridge['current_state']['production_token_measurement_allowed']).lower()}` |",
            f"| measured_production_tokens | `{str(bridge['current_state']['measured_production_tokens']).lower()}` |",
            f"| production_admission_gate | `{str(bridge['current_state']['production_admission_gate']).lower()}` |",
            f"| accepted | `{str(bridge['current_state']['accepted']).lower()}` |",
            f"| integrated | `{str(bridge['current_state']['integrated']).lower()}` |",
            f"| production_ready | `{str(bridge['current_state']['production_ready']).lower()}` |",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实测量已执行。",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示生产代理或生产 SDK 已启用。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUTPUT_MD.write_text(md_text, encoding="utf-8")
    KDS_OUTPUT_MD.write_text(md_text, encoding="utf-8")

    loop_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-COST-BRIDGE-001",
            "title: Loop Round GPCF Headroom LCX Cost Bridge 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, WAES]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-COST-BRIDGE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Cost Bridge 001",
            "",
            "## 输入",
            "",
            "- 已存在 cost sensitivity model、loop cost observation series、independent replay 和 metadata replay evidence。",
            "- `python3 tools/kds-sync/build_headroom_lcx_cost_bridge.py`",
            "",
            "## 动作",
            "",
            "- 固化 replay only 成本桥接层。",
            "- 保持 production_token_measurement_allowed=false、measured_production_tokens=false。",
            "- `python3 tools/kds-sync/validate_headroom_lcx_cost_bridge.py`",
            "",
            "## 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-cost-bridge-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-cost-bridge-20260623.md`",
            "",
            "## 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_cost_bridge.py`",
            "",
            "## 反馈",
            "",
            "cost bridge 只把成本模型和 replay evidence 串成受控桥接层，不改变 production branch blocked 状态。",
            "不产生真实生产 token 结论。",
            "",
            "## 下一轮",
            "",
            "若未来拿到真实测量授权，再把 cost bridge 连接到真实 token ledger；当前继续保持 replay only。",
        ]
    ) + "\n"
    OUTPUT_LOOP.write_text(loop_text, encoding="utf-8")
    KDS_OUTPUT_LOOP.write_text(loop_text, encoding="utf-8")


def main() -> int:
    bridge = build_bridge()
    write_outputs(bridge)
    print(
        "headroom_lcx_cost_bridge=generated "
        f"project_count={bridge['project_count']} "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
