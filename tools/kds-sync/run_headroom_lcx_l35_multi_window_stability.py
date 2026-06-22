#!/usr/bin/env python3
"""Run Headroom LCX L3.5 multi-window sanitized stability replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
L35_WINDOW_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001.md"

PROJECTS = {
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
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_hash(payload: object) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/{source_path}
source_path: {source_path}
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---
"""


def build_window_records(base_records: list[dict[str, object]], window_id: int) -> list[dict[str, object]]:
    records = []
    for record in base_records:
        records.append(
            {
                "task_id": record["task_id"],
                "loop_round_id": f"GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-{window_id:02d}",
                "project_id": record["project_id"],
                "agent_id": record["agent_id"],
                "model_id": record["model_id"],
                "mode": "l3_5_multi_window_sanitized_fixture_replay",
                "content_type": record["content_type"],
                "tokens_before": record["tokens_before"],
                "tokens_after": record["tokens_after"],
                "tokens_saved": "not_calculated",
                "saving_rate": "not_calculated",
                "ccr_enabled": record["ccr_enabled"],
                "ccr_retrieve_count": record["ccr_retrieve_count"],
                "policy_profile": record["policy_profile"],
                "waes_decision": "admitted_for_l3_5_multi_window_sanitized_stability_only",
                "answer_equivalence": "not_measured",
                "marker_gate": record["marker_gate"],
                "sensitive_redaction_gate": record["sensitive_redaction_gate"],
                "measured_production_tokens": False,
                "accepted": False,
                "integrated": False,
                "production_ready": False,
            }
        )
    return records


def build_evidence() -> dict:
    l35 = load_json(L35_WINDOW_JSON)
    base_records = l35.get("pilot_smoke_records", [])
    failures: list[str] = []
    if l35.get("status") != "l3_5_controlled_sanitized_pilot_window_pass_check_only":
        failures.append("l35_window_not_passed")
    if len(base_records) != 45:
        failures.append("base_record_count_mismatch")

    windows = []
    stable_hashes = set()
    for window_id in range(1, 6):
        records = build_window_records(base_records, window_id)
        normalized_records = [
            {key: value for key, value in record.items() if key != "loop_round_id"}
            for record in records
        ]
        stable_hash = canonical_hash(normalized_records)
        stable_hashes.add(stable_hash)
        projects = {record["project_id"] for record in records}
        window_failures = []
        if projects != PROJECTS:
            window_failures.append("project_coverage_mismatch")
        if len(records) != 45:
            window_failures.append("record_count_mismatch")
        for record in records:
            if record["tokens_saved"] != "not_calculated" or record["saving_rate"] != "not_calculated":
                window_failures.append(f"calculation_forbidden:{record['task_id']}")
            for key in ["measured_production_tokens", "accepted", "integrated", "production_ready"]:
                if record[key] is not False:
                    window_failures.append(f"status_or_measurement_forbidden:{record['task_id']}:{key}")
        if window_failures:
            failures.extend([f"window_{window_id}:{item}" for item in window_failures])
        windows.append(
            {
                "window_id": f"HEADROOM-LCX-L35-MULTI-WINDOW-{window_id:02d}",
                "record_count": len(records),
                "project_count": len(projects),
                "stable_hash": stable_hash,
                "records": records,
                "gates": {
                    "project_coverage_gate": projects == PROJECTS,
                    "record_count_gate": len(records) == 45,
                    "metadata_only": True,
                    "check_only": True,
                    "measured_production_tokens": False,
                    "production_admission_gate": False,
                    "accepted": False,
                    "integrated": False,
                    "production_ready": False,
                },
                "failures": window_failures,
            }
        )

    if len(stable_hashes) != 1:
        failures.append("multi_window_hash_drift")

    return {
        "evidence_id": "HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622",
        "task_id": "GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001",
        "date": "2026-06-22",
        "status": "l3_5_multi_window_stability_pass_check_only" if not failures else "l3_5_multi_window_stability_blocked",
        "scope": "l3_5_multi_window_sanitized_fixture_stability_only",
        "source_window": L35_WINDOW_JSON.relative_to(ROOT).as_posix(),
        "window_count": len(windows),
        "project_count": 15,
        "record_count_per_window": 45,
        "total_record_count": sum(window["record_count"] for window in windows),
        "stable_hash_count": len(stable_hashes),
        "stable_hash": next(iter(stable_hashes)) if len(stable_hashes) == 1 else None,
        "windows": windows,
        "continuous_session": {
            "mode": "L3.5",
            "declared_rounds": 5,
            "substantive_rounds": 1,
            "generated_items": 5,
            "batch_generated": True,
            "substance_gate": "pass_as_single_substantive_round",
            "stop_type": "authorization_boundary",
            "stop_evidence": "L3.5 multi-window stability complete; L4/L5/production requires separate authorization.",
        },
        "gates": {
            "l3_5_multi_window_stability_gate": not failures,
            "source_l35_window_gate": l35.get("status") == "l3_5_controlled_sanitized_pilot_window_pass_check_only",
            "window_count_gate": len(windows) == 5,
            "record_count_gate": all(window["record_count"] == 45 for window in windows),
            "project_coverage_gate": all(window["project_count"] == 15 for window in windows),
            "multi_window_hash_stability_gate": len(stable_hashes) == 1,
            "metadata_only": True,
            "check_only": True,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "headroom_learn_apply_executed": False,
            "l4_candidate": False,
            "l5_candidate": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "failures": failures,
    }


def write_md(evidence: dict) -> None:
    lines = [
        frontmatter("Headroom LCX L3.5 多窗口脱敏稳定性证据", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX L3.5 多窗口脱敏稳定性证据",
        "",
        "## 摘要",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- window_count: `{evidence['window_count']}`",
        f"- total_record_count: `{evidence['total_record_count']}`",
        f"- stable_hash_count: `{evidence['stable_hash_count']}`",
        "",
        "## 连续运行边界",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key, value in evidence["continuous_session"].items():
        lines.append(f"| {key} | {str(value).lower() if isinstance(value, bool) else value} |")
    lines.extend(["", "## 门禁", "", "| Gate | Value |", "|---|---|"])
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## 禁止声明",
            "",
            "- 本证据仅证明 L3.5 脱敏 fixture 多窗口 replay hash 稳定。",
            "- 本证据不计算 token 节省，不测量 production tokens，也不证明生产成本收益。",
            "- 本证据不授权 production proxy、external API write、KDS API write 或 `headroom learn --apply`。",
            "- 本证据不得将 Headroom LCX 标记为 accepted、integrated 或 production_ready。",
            "",
        ]
    )
    EVIDENCE_MD.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX L3.5 Multi Window Stability 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX L3.5 Multi Window Stability 001

## 输入

用户要求进入下一轮。上一轮已完成 L3.5 受控脱敏试点窗口。

## 动作

- run: 基于 L3.5 单窗口证据生成 5 个脱敏 replay 窗口。
- stop: 停止边界固定为 authorization_boundary，不进入 L4/L5/生产。
- verify: 检查 5 个窗口的 15 项目覆盖、45 条记录、hash 稳定性和生产禁用门禁。
- recover: 若窗口漂移，回退到单窗口证据并阻断扩大试点。
- debug: 当前剩余阻塞仍是无真实生产 token 实测、无业务答案等价证明、无 L4/L5 授权。

## 输出

- `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json`
- `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_l35_multi_window_stability.py
python3 tools/kds-sync/validate_headroom_lcx_l35_multi_window_stability.py
```

## 反馈

本轮是批量生成的多窗口稳定性检查，按连续运行真实性门禁计为 1 个实质轮次，不作为 L4/L5/生产准入。

## 下一轮

生成 L4 真实测量授权申请包，或继续扩展 L3.5 的业务答案等价脱敏样例。
"""
    LOOP_ROUND.parent.mkdir(parents=True, exist_ok=True)
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = build_evidence()
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    print(
        "headroom_lcx_l35_multi_window_stability="
        f"{'pass_check_only' if not evidence['failures'] else 'blocked'} "
        f"window_count={evidence['window_count']} project_count=15 "
        f"record_count_per_window={evidence['record_count_per_window']} stable_hash_count={evidence['stable_hash_count']} "
        "substantive_rounds=1 l4_candidate=false measured_production_tokens=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0 if not evidence["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
