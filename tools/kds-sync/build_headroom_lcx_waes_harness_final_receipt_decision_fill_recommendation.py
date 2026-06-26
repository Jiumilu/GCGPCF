#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision fill recommendation for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

DRAFT = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.json"
HUMAN_FILL = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001.md"
OUT_FIXTURE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.recommended.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_recommendation() -> dict[str, Any]:
    draft = load_json(DRAFT)
    human_fill = load_json(HUMAN_FILL)
    require(draft.get("status") == "draft_candidate_ready_not_formal_decision", "draft must be ready")
    require(human_fill.get("status") == "waes_harness_final_receipt_decision_human_fill_request_ready", "human fill request must be ready")
    recommended = dict(draft["candidate_response"])
    recommended["decision_maker"] = "WAES/Harness reviewer to confirm"
    recommended["decision_role"] = "WAES/Harness final receipt reviewer to confirm"
    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001",
        "date": "2026-06-23",
        "status": "fill_recommendation_ready_not_formal_decision",
        "scope": "recommendation_only_no_formal_response",
        "source_draft_candidate": DRAFT.relative_to(ROOT).as_posix(),
        "source_human_fill_request": HUMAN_FILL.relative_to(ROOT).as_posix(),
        "recommended_response_path": OUT_FIXTURE.relative_to(ROOT).as_posix(),
        "recommended_response": recommended,
        "recommendation_boundary": {
            "recommendation_only": True,
            "not_formal_response": True,
            "requires_waes_harness_confirmation": True,
            "can_open_real_measurement": False,
            "real_measurement_open": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(evidence: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_FIXTURE.write_text(json.dumps(evidence["recommended_response"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    boundary_rows = [
        f"| {k} | `{str(v).lower()}` |"
        for k, v in evidence["recommendation_boundary"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Fill Recommendation",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Fill Recommendation",
            "",
            "## 当前结论",
            "",
            "`fill_recommendation_ready_not_formal_decision`",
            "",
            "本文提供正式 response 的建议回填内容，但它仍然只是建议，不是正式 WAES/Harness 决策结果。",
            "",
            "## Recommendation Boundary",
            "",
            "| item | value |",
            "|---|---|",
            *boundary_rows,
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Fill Recommendation 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-FILL-RECOMMENDATION-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Fill Recommendation 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- final decision draft candidate",
            "- final decision human fill request",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation.py`",
            "- 生成正式 response 的建议回填内容。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-fill-recommendation-20260623.json`",
            "- `fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.recommended.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: recommendation 仍需 WAES/Harness 确认后才能转成正式 response。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 recommendation evidence 与 fixture 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 建议回填内容已生成，但仍不是 formal response。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立确认并回填正式 response.json。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_recommendation()
    write_outputs(evidence)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_fill_recommendation=generated "
        "status=fill_recommendation_ready_not_formal_decision "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
