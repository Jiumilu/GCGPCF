#!/usr/bin/env python3
"""Build the Headroom LCX readiness and L3.5 pilot authorization package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-001.md"

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
    "docs/harness/evidence/headroom-lcx-controlled-package-20260621.json",
    "docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.json",
    "docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json",
    "docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json",
    "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json",
    "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.json",
    "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json",
    "docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260621.json",
    "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
    "docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.json",
    "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json",
    "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json",
    "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json",
    "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.json",
    "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json",
    "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json",
    "docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.json",
    "docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.json",
    "docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json",
    "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json",
    "docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.json",
    "docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json",
    "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json",
]


def read_json(path: str) -> dict:
    full_path = ROOT / path
    if not full_path.exists():
        return {"path": path, "missing": True}
    data = json.loads(full_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"path": path, "invalid": True}
    return data


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-20260622
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


def build_evidence() -> dict:
    chain = []
    missing = []
    unsafe = []
    for path in EVIDENCE_CHAIN:
        data = read_json(path)
        if data.get("missing"):
            missing.append(path)
        gates = data.get("gates", {}) if isinstance(data.get("gates", {}), dict) else {}
        for key in ["production_admission_gate", "accepted", "integrated", "production_ready"]:
            value = gates.get(key, data.get(key))
            if value is True:
                unsafe.append(f"{path}:{key}")
        chain.append(
            {
                "path": path,
                "evidence_id": data.get("evidence_id"),
                "status": data.get("status"),
                "missing": bool(data.get("missing")),
                "production_admission_gate": gates.get("production_admission_gate", data.get("production_admission_gate")),
                "accepted": gates.get("accepted", data.get("accepted")),
                "integrated": gates.get("integrated", data.get("integrated")),
                "production_ready": gates.get("production_ready", data.get("production_ready")),
            }
        )

    project_group_fixture = read_json("docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json")
    project_group_replay = read_json("docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json")
    fixture_projects = set(project_group_fixture.get("projects", []))
    replay_projects = set()
    rounds = project_group_replay.get("rounds", [])
    if rounds:
        replay_projects = {record.get("project_id") for record in rounds[0].get("records", [])}

    coverage_ok = fixture_projects == set(PROJECTS) and replay_projects == set(PROJECTS)
    stable_ok = project_group_replay.get("stable_hash_count") == 1 and project_group_replay.get("entry_count") == 45
    missing_or_unsafe = bool(missing or unsafe)
    recommended_l35 = coverage_ok and stable_ok and not missing_or_unsafe

    return {
        "evidence_id": "HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-READINESS-PILOT-AUTHORIZATION-PACKAGE-001",
        "date": "2026-06-22",
        "status": "l3_5_controlled_sanitized_pilot_recommended_not_production" if recommended_l35 else "l3_5_pilot_package_blocked",
        "scope": "project_group_l3_5_controlled_sanitized_pilot_request_package_only",
        "project_count": 15,
        "projects": PROJECTS,
        "evidence_chain_count": len(EVIDENCE_CHAIN),
        "evidence_chain": chain,
        "readiness_summary": {
            "route_project_count": 15,
            "fixture_project_count": project_group_fixture.get("project_count"),
            "fixture_entry_count": project_group_fixture.get("entry_count"),
            "replay_round_count": project_group_replay.get("round_count"),
            "replay_entry_count": project_group_replay.get("entry_count"),
            "stable_hash_count": project_group_replay.get("stable_hash_count"),
            "coverage_ok": coverage_ok,
            "stability_ok": stable_ok,
            "real_production_measurement": False,
            "runtime_compression_effectiveness_proven": False,
            "business_answer_equivalence_proven": False,
        },
        "recommendation": {
            "recommended_next_authorization": "L3.5_controlled_sanitized_pilot",
            "recommendation_gate": recommended_l35,
            "l4_candidate": False,
            "l5_candidate": False,
            "production_candidate": False,
            "reason": "15-project sanitized metadata coverage and replay stability exist, but no real production measurement or business answer equivalence exists.",
        },
        "requested_permissions": {
            "allow_local_headroom_dry_run": True,
            "allow_sanitized_fixture_replay": True,
            "allow_harness_evidence_generation": True,
            "allow_waes_gate_check": True,
            "allow_raw_prompt_or_completion": False,
            "allow_unredacted_sensitive_material": False,
            "allow_production_proxy": False,
            "allow_external_api_write": False,
            "allow_kds_api_write": False,
            "allow_database_migration": False,
            "allow_permission_change": False,
            "allow_headroom_learn_apply": False,
            "allow_status_promotion_to_accepted_integrated_or_production_ready": False,
        },
        "blocked_until": [
            "explicit_l3_5_pilot_window_id",
            "human_approver_identity_and_timestamp",
            "waes_harness_l3_5_pilot_decision",
            "rollback_plan_id_for_pilot",
            "telemetry_off_confirmation",
            "negative_gate_pass_for_l3_5_inputs",
        ],
        "gates": {
            "readiness_package_generated": True,
            "evidence_chain_present": not missing,
            "prior_evidence_has_no_status_promotion": not unsafe,
            "project_group_coverage_gate": coverage_ok,
            "project_group_replay_stability_gate": stable_ok,
            "l3_5_controlled_sanitized_pilot_recommended": recommended_l35,
            "l4_candidate": False,
            "l5_candidate": False,
            "metadata_only": True,
            "check_only": True,
            "real_production_measurement": False,
            "runtime_compression_effectiveness_proven": False,
            "business_answer_equivalence_proven": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "headroom_learn_apply_executed": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "failures": missing + unsafe,
    }


def write_md(evidence: dict) -> None:
    lines = [
        frontmatter("Headroom LCX Readiness Pilot Authorization Package", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Readiness Pilot Authorization Package",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- evidence_chain_count: `{evidence['evidence_chain_count']}`",
        "",
        "## Readiness",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    for key, value in evidence["readiness_summary"].items():
        lines.append(f"| {key} | {str(value).lower() if isinstance(value, bool) else value} |")
    lines.extend(["", "## Recommendation", "", "| Field | Value |", "|---|---|"])
    for key, value in evidence["recommendation"].items():
        lines.append(f"| {key} | {str(value).lower() if isinstance(value, bool) else value} |")
    lines.extend(["", "## Gates", "", "| Gate | Value |", "|---|---|"])
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## Requested L3.5 Pilot Boundary",
            "",
            "- Allow local Headroom dry-run and sanitized fixture replay only.",
            "- Allow Harness evidence generation and WAES gate checks only.",
            "- Do not allow production proxy, production SDK enablement, KDS API write, external API write, database migration, permission change, raw prompt/completion storage, unredacted sensitive material, or `headroom learn --apply`.",
            "- Do not promote `accepted`, `integrated`, or `production_ready`.",
            "",
            "## Non-Claims",
            "",
            "- This package recommends only an L3.5 controlled sanitized pilot authorization boundary.",
            "- This package is not L4, L5, production admission, or production token measurement evidence.",
            "- This package does not prove real runtime compression effectiveness or business answer equivalence.",
            "",
        ]
    )
    EVIDENCE_MD.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Readiness Pilot Authorization Package 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Readiness Pilot Authorization Package 001

## 输入

用户要求进入下一步。当前已有 15 项目域 sanitized fixture 与三轮 replay stability 证据。

## 动作

- run: 汇总 Headroom LCX P0-P5、授权边界、脱敏测量、metadata replay、marker/retrieval miss、5 项目 fixture、15 项目 fixture 与 replay stability 证据。
- stop: 将停止边界设为 L3.5 受控脱敏试点授权边界，不进入 L4/L5/生产。
- verify: 生成 readiness pilot authorization package 并运行专用 validator。
- recover: 若后续试点失败，回退到现有 sanitized fixture/replay evidence，不影响生产。
- debug: 当前真实阻塞仍是无生产实测、无业务答案等价证明、无 L3.5 人工窗口。

## 输出

- `docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.json`
- `docs/harness/evidence/headroom-lcx-readiness-pilot-authorization-package-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_readiness_pilot_authorization_package.py
python3 tools/kds-sync/validate_headroom_lcx_readiness_pilot_authorization_package.py
```

## 反馈

本轮只生成 L3.5 受控脱敏试点授权包。它不是 L4/L5/生产准入，不允许 accepted、integrated 或 production_ready。

## 下一轮

若用户批准 L3.5，可生成 L3.5 受控脱敏试点窗口实例，并运行 negative gate + replay smoke。
"""
    LOOP_ROUND.parent.mkdir(parents=True, exist_ok=True)
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = build_evidence()
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    print(
        "headroom_lcx_readiness_pilot_authorization_package="
        f"{'pass_check_only' if not evidence['failures'] else 'blocked'} "
        "recommended_next_authorization=L3.5_controlled_sanitized_pilot "
        f"project_count={evidence['project_count']} evidence_chain_count={evidence['evidence_chain_count']} "
        "l4_candidate=false production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0 if not evidence["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
