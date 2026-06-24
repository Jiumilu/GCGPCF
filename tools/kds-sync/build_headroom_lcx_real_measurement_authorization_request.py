#!/usr/bin/env python3
"""Build the Headroom LCX real measurement authorization request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIELD_MAP_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json"
RUNNER_CONTRACT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json"
TRANSITION_GRAPH_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json"
GAP_MATRIX_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md"
MIRROR_JSON = ROOT / ".kds/development-space/开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json"
MIRROR_MD = ROOT / ".kds/development-space/开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md"
MIRROR_LOOP_ROUND = ROOT / ".kds/development-space/开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md"

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

EVIDENCE_CHAIN = [
    "docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json",
    "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json",
    "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json",
    "docs/harness/evidence/headroom-lcx-real-measurement-authorization-field-map-20260623.json",
    "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json",
    "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json",
    "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json",
]

REQUIRED_FIELDS = [
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_token_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def frontmatter(title: str, source_path: str, kds_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: {kds_path}
source_path: {source_path}
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---
"""


def build_package() -> dict:
    field_map = load_json(FIELD_MAP_JSON)
    runner_contract = load_json(RUNNER_CONTRACT_JSON)
    transition_graph = load_json(TRANSITION_GRAPH_JSON)
    gap_matrix = load_json(GAP_MATRIX_JSON)

    bindings = field_map.get("field_map", [])
    require(isinstance(bindings, list), "field_map must contain field_map list")
    binding_map = {item.get("field"): item for item in bindings if isinstance(item, dict)}
    missing_fields = [field for field in REQUIRED_FIELDS if field not in binding_map]
    require(missing_fields == [], f"missing field bindings: {missing_fields}")

    request = {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001",
        "date": "2026-06-23",
        "status": "real_measurement_authorization_request_blocked_until_real_window",
        "scope": "real_measurement_authorization_request_precheck_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "evidence_chain_count": len(EVIDENCE_CHAIN),
        "evidence_chain": EVIDENCE_CHAIN,
        "requested_future_decision": "open_real_measurement_window",
        "current_waes_harness_admission_decision": binding_map["waes_harness_admission_decision"].get("current_value"),
        "field_bindings": [
            {
                "field": field,
                "current_value": binding_map[field].get("current_value"),
                "source_evidence": binding_map[field].get("source_evidence"),
                "future_runner_input": binding_map[field].get("future_runner_input"),
                "binding_state": "precheck_only",
            }
            for field in REQUIRED_FIELDS
        ],
        "requested_boundary": {
            "allowed_inputs": runner_contract.get("runner_contract", {}).get("allowed_inputs", []),
            "forbidden_inputs": runner_contract.get("runner_contract", {}).get("forbidden_inputs", []),
            "allowed_actions": runner_contract.get("runner_contract", {}).get("allowed_actions", []),
            "forbidden_actions": runner_contract.get("runner_contract", {}).get("forbidden_actions", []),
        },
        "current_state": {
            "real_measurement_gap_present": field_map.get("current_state", {}).get("real_measurement_gap_present", True),
            "production_branch_blocked": field_map.get("current_state", {}).get("production_branch_blocked", True),
            "production_token_measurement_allowed": field_map.get("current_state", {}).get("production_token_measurement_allowed", False),
            "measured_production_tokens": field_map.get("current_state", {}).get("measured_production_tokens", False),
            "production_admission_gate": field_map.get("current_state", {}).get("production_admission_gate", False),
            "accepted": field_map.get("current_state", {}).get("accepted", False),
            "integrated": field_map.get("current_state", {}).get("integrated", False),
            "production_ready": field_map.get("current_state", {}).get("production_ready", False),
        },
        "execution_guard": {
            "executable_now": False,
            "requires_real_measurement_authorization_window": True,
            "requires_waes_harness_decision": True,
            "requires_sanitized_token_ledger_metadata_only": True,
            "requires_rollback_plan_id": True,
            "requires_no_production_proxy": True,
            "requires_no_real_kds_write": True,
            "requires_no_external_api_write": True,
        },
        "source_refs": {
            "field_map": FIELD_MAP_JSON.relative_to(ROOT).as_posix(),
            "runner_contract": RUNNER_CONTRACT_JSON.relative_to(ROOT).as_posix(),
            "transition_graph": TRANSITION_GRAPH_JSON.relative_to(ROOT).as_posix(),
            "gap_matrix": GAP_MATRIX_JSON.relative_to(ROOT).as_posix(),
        },
        "non_claims": {
            "real_measurement_open": False,
            "production_branch_open": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "business_answer_equivalence_proven": False,
        },
    }
    return request


def write_md(request: dict, source_path: str, kds_path: str) -> str:
    lines = [
        frontmatter("Headroom LCX Real Measurement Authorization Request", source_path, kds_path),
        "# Headroom LCX Real Measurement Authorization Request",
        "",
        "## Evidence ID",
        "",
        "`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623`",
        "",
        "## 结论",
        "",
        "本文件只把未来真实测量授权请求结构化成可审计条目；当前仍然 precheck-only，不打开真实测量窗口。",
        "",
        "## 请求摘要",
        "",
        "| 项 | 当前值 |",
        "|---|---|",
        f"| requested_future_decision | {request['requested_future_decision']} |",
        f"| current_waes_harness_admission_decision | {request['current_waes_harness_admission_decision']} |",
        f"| project_count | {request['project_count']} |",
        f"| real_measurement_gap_present | {str(request['current_state']['real_measurement_gap_present']).lower()} |",
        f"| production_branch_blocked | {str(request['current_state']['production_branch_blocked']).lower()} |",
        f"| production_token_measurement_allowed | {str(request['current_state']['production_token_measurement_allowed']).lower()} |",
        f"| production_admission_gate | {str(request['current_state']['production_admission_gate']).lower()} |",
        f"| accepted | {str(request['current_state']['accepted']).lower()} |",
        f"| integrated | {str(request['current_state']['integrated']).lower()} |",
        f"| production_ready | {str(request['current_state']['production_ready']).lower()} |",
        "",
        "## 字段绑定",
        "",
        "| field | current_value | future_runner_input | binding_state |",
        "|---|---|---|---|",
    ]
    for item in request["field_bindings"]:
        lines.append(
            f"| {item['field']} | {item['current_value']} | {item['future_runner_input']} | {item['binding_state']} |"
        )
    lines.extend(
        [
            "",
            "## 请求边界",
            "",
            "| allow | value |",
            "|---|---|",
        ]
    )
    for key, value in request["requested_boundary"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## 执行门禁",
            "",
            "| Gate | Value |",
            "|---|---|",
        ]
    )
    for key, value in request["execution_guard"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## 非声明",
            "",
            "- 本请求不表示真实测量已执行。",
            "- 本请求不表示真实业务等价性已证明。",
            "- 本请求不表示生产分支已打开。",
            "- 本请求不表示 accepted、integrated 或 production_ready。",
            "",
            "## 下一步",
            "",
            "等待 WAES/Harness 对真实测量窗口作出新的授权裁决；在此之前仅保持 precheck-only 和 blocked 状态。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_loop_round(source_path: str, kds_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623
title: Loop Round GPCF Headroom LCX Real Measurement Authorization Request 001
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: {kds_path}
source_path: {source_path}
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Real Measurement Authorization Request 001

## 输入

- 真实测量字段映射与 runner contract 已存在，但仍为 precheck-only。
- 当前目标是把真实测量授权请求结构化，不打开生产窗。

## 动作

- 运行 `python3 tools/kds-sync/build_headroom_lcx_real_measurement_authorization_request.py`
- 归档真实测量授权请求 evidence。
- 不启动生产代理、不触达真实 KDS 写入。

## 输出

- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json`
- `docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_authorization_request.py`

## 反馈

- 当前仍缺真实测量授权窗口。
- 当前仍不得进入生产 token 测量或真实业务等价证明。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

等待 WAES/Harness 对真实测量窗口作出新的授权裁决。
"""


def main() -> int:
    request = build_package()
    source_md = write_md(
        request,
        OUTPUT_MD.relative_to(ROOT).as_posix(),
        "开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md",
    )
    source_json = json.dumps(request, ensure_ascii=False, indent=2) + "\n"
    loop_round = write_loop_round(
        LOOP_ROUND.relative_to(ROOT).as_posix(),
        "开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md",
    )
    mirror_md = write_md(
        request,
        OUTPUT_MD.relative_to(ROOT).as_posix(),
        "开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md",
    )
    mirror_loop = write_loop_round(
        LOOP_ROUND.relative_to(ROOT).as_posix(),
        "开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md",
    )
    write(OUTPUT_JSON, source_json)
    write(OUTPUT_MD, source_md)
    write(LOOP_ROUND, loop_round)
    write(MIRROR_JSON, source_json)
    write(MIRROR_MD, mirror_md)
    write(MIRROR_LOOP_ROUND, mirror_loop)
    print(
        "headroom_lcx_real_measurement_authorization_request=pass_check_only "
        "project_count=15 requested_future_decision=open_real_measurement_window "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
