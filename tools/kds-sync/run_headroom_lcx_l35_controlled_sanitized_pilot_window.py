#!/usr/bin/env python3
"""Run the Headroom LCX L3.5 controlled sanitized pilot window."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_JSON = ROOT / "fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json"
READINESS_JSON = ROOT / "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json"
NEGATIVE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json"
REPLAY_JSON = ROOT / "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001.md"

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

AUTHORIZED_AT = "2026-06-22T10:00:00+08:00"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622
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


def canonical_hash(payload: object) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_smoke_records(fixture: dict) -> list[dict[str, object]]:
    records = []
    for entry in fixture.get("entries", []):
        tokens_before = int(entry["input_tokens_before"]) + int(entry["output_tokens_before"])
        tokens_after = int(entry["input_tokens_after"]) + int(entry["output_tokens_after"])
        records.append(
            {
                "task_id": entry["measurement_id"],
                "loop_round_id": "GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001",
                "project_id": entry["project"],
                "agent_id": "codex_local_l35_controlled_sanitized_pilot",
                "model_id": "not_invoked",
                "mode": "l3_5_controlled_sanitized_fixture_replay",
                "content_type": entry["scenario"],
                "tokens_before": tokens_before,
                "tokens_after": tokens_after,
                "tokens_saved": "not_calculated",
                "saving_rate": "not_calculated",
                "ccr_enabled": entry["scenario"] == "retrieval_context_metadata",
                "ccr_retrieve_count": int(entry["retrieval_miss_count"]),
                "policy_profile": "l3_5_sanitized_fixture_replay_no_raw_text",
                "waes_decision": "admitted_for_l3_5_sanitized_pilot_only",
                "answer_equivalence": "not_measured",
                "marker_gate": entry["project_marker_gate"],
                "sensitive_redaction_gate": entry["sensitive_redaction_gate"],
                "measured_production_tokens": False,
                "accepted": False,
                "integrated": False,
                "production_ready": False,
            }
        )
    return records


def build_evidence() -> dict:
    fixture = load_json(FIXTURE_JSON)
    readiness = load_json(READINESS_JSON)
    negative = load_json(NEGATIVE_JSON)
    replay = load_json(REPLAY_JSON)
    records = build_smoke_records(fixture)
    projects = {record["project_id"] for record in records}
    scenarios = {record["content_type"] for record in records}
    failures: list[str] = []
    if readiness.get("recommendation", {}).get("recommended_next_authorization") != "L3.5_controlled_sanitized_pilot":
        failures.append("readiness_recommendation_missing")
    if not readiness.get("gates", {}).get("l3_5_controlled_sanitized_pilot_recommended"):
        failures.append("readiness_gate_false")
    if negative.get("rejected") != 9 and negative.get("negative_case_count") != 9:
        failures.append("negative_gate_case_count_mismatch")
    if negative.get("accepted") not in (0, None):
        failures.append("negative_gate_accepted_nonzero")
    if replay.get("stable_hash_count") != 1:
        failures.append("replay_stability_hash_mismatch")
    if projects != set(PROJECTS):
        failures.append("project_coverage_mismatch")
    if len(records) != 45:
        failures.append("pilot_smoke_record_count_mismatch")
    for record in records:
        if record["measured_production_tokens"] is not False:
            failures.append(f"production_measurement_not_false:{record['task_id']}")
        if record["accepted"] or record["integrated"] or record["production_ready"]:
            failures.append(f"status_promotion_forbidden:{record['task_id']}")

    return {
        "evidence_id": "HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622",
        "task_id": "GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001",
        "date": "2026-06-22",
        "status": "l3_5_controlled_sanitized_pilot_window_pass_check_only" if not failures else "l3_5_controlled_sanitized_pilot_window_blocked",
        "scope": "l3_5_controlled_sanitized_fixture_replay_only",
        "authorization": {
            "authorized_window_id": "HEADROOM-LCX-L35-SANITIZED-PILOT-WINDOW-20260622-001",
            "authorized_by": "user_current_codex_session",
            "authorized_at": AUTHORIZED_AT,
            "authorization_signal": "用户回复：批准",
            "authorization_scope": "L3.5_controlled_sanitized_pilot_only",
            "sanitized_production_token_ledger": FIXTURE_JSON.relative_to(ROOT).as_posix(),
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "waes_harness_admission_decision": "admitted_for_l3_5_sanitized_pilot_only",
            "authorization_complete_for_l3_5": True,
            "authorization_complete_for_l4_l5_or_production": False,
        },
        "project_count": len(projects),
        "scenario_count": len(scenarios),
        "entry_count": len(records),
        "pilot_smoke_record_count": len(records),
        "stable_hash": canonical_hash(records),
        "evidence_inputs": {
            "readiness_package": READINESS_JSON.relative_to(ROOT).as_posix(),
            "fixture": FIXTURE_JSON.relative_to(ROOT).as_posix(),
            "negative_gate": NEGATIVE_JSON.relative_to(ROOT).as_posix(),
            "replay_stability": REPLAY_JSON.relative_to(ROOT).as_posix(),
        },
        "pilot_smoke_records": records,
        "gates": {
            "l3_5_pilot_window_generated": True,
            "authorization_complete_for_l3_5": True,
            "authorization_complete_for_l4_l5_or_production": False,
            "readiness_gate": not failures and readiness.get("gates", {}).get("l3_5_controlled_sanitized_pilot_recommended") is True,
            "negative_gate_pass": negative.get("accepted") in (0, None),
            "replay_stability_gate": replay.get("stable_hash_count") == 1,
            "project_coverage_gate": projects == set(PROJECTS),
            "pilot_smoke_gate": len(records) == 45 and not failures,
            "telemetry_off": True,
            "metadata_only": True,
            "check_only": True,
            "raw_prompt_storage": False,
            "raw_completion_storage": False,
            "unredacted_sensitive_material_processed": False,
            "headroom_learn_apply_executed": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "database_migration": False,
            "permission_change": False,
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
        frontmatter("Headroom LCX L3.5 受控脱敏试点窗口", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX L3.5 受控脱敏试点窗口",
        "",
        "## 摘要",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- authorized_window_id: `{evidence['authorization']['authorized_window_id']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- pilot_smoke_record_count: `{evidence['pilot_smoke_record_count']}`",
        "",
        "## 授权",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key, value in evidence["authorization"].items():
        lines.append(f"| {key} | {str(value).lower() if isinstance(value, bool) else value} |")
    lines.extend(["", "## 门禁", "", "| Gate | Value |", "|---|---|"])
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## 禁止声明",
            "",
            "- 本 L3.5 试点窗口仅限本机脱敏 fixture replay 和 evidence 生成。",
            "- 本窗口不授权 L4、L5、production proxy、production SDK、external API write、KDS API write、database migration、permission change 或 `headroom learn --apply`。",
            "- 本窗口不测量 production tokens，也不证明 production token savings。",
            "- 本窗口不得将 Headroom LCX 标记为 accepted、integrated 或 production_ready。",
            "",
        ]
    )
    EVIDENCE_MD.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX L3.5 Controlled Sanitized Pilot Window 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX L3.5 Controlled Sanitized Pilot Window 001

## 输入

用户回复“批准”，批准进入 L3.5 受控脱敏试点窗口。

## 动作

- run: 生成 L3.5 controlled sanitized pilot window，并对 15 项目域 45 条脱敏 fixture 做 replay smoke 记录。
- stop: 停止边界固定为 L3.5，不进入 L4/L5/生产，不启动 production proxy。
- verify: 复用 readiness package、negative gate、project-group replay stability，并运行本轮 validator。
- recover: 若 L3.5 失败，回退到 readiness package 和 project-group replay stability，不影响任何生产路径。
- debug: 当前剩余阻塞是无真实生产 token 实测、无运行时业务答案等价证明、无生产准入。

## 输出

- `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json`
- `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_l35_controlled_sanitized_pilot_window.py
python3 tools/kds-sync/validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py
```

## 反馈

L3.5 窗口只允许本机脱敏 fixture replay 和 evidence 生成。所有生产、KDS API、外部 API、状态升级能力仍关闭。

## 下一轮

扩展 L3.5 pilot 为多轮稳定性窗口，或生成 L4 真实测量授权申请包。
"""
    LOOP_ROUND.parent.mkdir(parents=True, exist_ok=True)
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = build_evidence()
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    print(
        "headroom_lcx_l35_controlled_sanitized_pilot_window="
        f"{'pass_check_only' if not evidence['failures'] else 'blocked'} "
        f"authorized_window_id={evidence['authorization']['authorized_window_id']} "
        f"project_count={evidence['project_count']} pilot_smoke_record_count={evidence['pilot_smoke_record_count']} "
        "l4_candidate=false measured_production_tokens=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0 if not evidence["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
