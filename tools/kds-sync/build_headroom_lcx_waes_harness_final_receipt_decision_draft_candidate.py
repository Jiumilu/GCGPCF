#!/usr/bin/env python3
"""Build WAES/Harness final receipt decision draft candidate for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

REQUEST = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-request-20260623.json"
HUMAN_FILL = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-human-fill-request-20260623.json"
TEMPLATE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.template.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md"
OUT_FIXTURE = FIXTURE_DIR / "headroom-lcx-waes-harness-final-receipt-decision.response.draft.candidate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_candidate() -> dict[str, Any]:
    request = load_json(REQUEST)
    human_fill = load_json(HUMAN_FILL)
    template = load_json(TEMPLATE)
    require(request.get("status") == "waes_harness_final_receipt_decision_requested_pending", "request must remain pending")
    require(human_fill.get("status") == "waes_harness_final_receipt_decision_human_fill_request_ready", "human fill request must be ready")

    candidate = dict(template)
    candidate.update(
        {
            "decision_maker": "lujunxiang / 总架构师 (candidate only, not WAES/Harness final signer)",
            "decision_role": "candidate_draft_preparer_only",
            "decided_at": "2026-06-23T14:33:00+08:00",
            "decision_value": "admitted_for_next_precheck_only",
            "decision_reason": "Candidate draft only. Receipt is valid for precheck-only intake, all production and acceptance flags remain false, and independent WAES/Harness review is still required before any next-stage motion.",
        }
    )

    return {
        "evidence_id": "HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-20260623",
        "task_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001",
        "date": "2026-06-23",
        "status": "draft_candidate_ready_not_formal_decision",
        "scope": "candidate_draft_only_no_final_decision_recorded",
        "source_request": REQUEST.relative_to(ROOT).as_posix(),
        "source_human_fill_request": HUMAN_FILL.relative_to(ROOT).as_posix(),
        "draft_candidate_path": OUT_FIXTURE.relative_to(ROOT).as_posix(),
        "candidate_response": candidate,
        "candidate_use_boundary": {
            "candidate_only": True,
            "not_formal_response": True,
            "not_waes_harness_signed": True,
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
    OUT_FIXTURE.write_text(json.dumps(evidence["candidate_response"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    boundary_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in evidence["candidate_use_boundary"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-20260623",
            "title: Headroom LCX WAES Harness Final Receipt Decision Draft Candidate",
            "project: WAES",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: WAES",
            "kds_space: 开发",
            "kds_path: 开发/04-WAES/docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX WAES Harness Final Receipt Decision Draft Candidate",
            "",
            "## 当前结论",
            "",
            "`draft_candidate_ready_not_formal_decision`",
            "",
            "本文只提供 WAES/Harness final decision 的建议回填草稿。它不是正式 response，不代表 WAES/Harness 已签署或已裁决。",
            "",
            "## Candidate Boundary",
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
            "doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001",
            "title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Draft Candidate 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Draft Candidate 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- final receipt decision request",
            "- final receipt decision human fill request",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py`",
            "- 生成建议回填草稿，但不生成正式 response。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.json`",
            "- `fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.draft.candidate.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: draft candidate 仅供参考，仍需 WAES/Harness 独立签署正式 response。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 draft candidate evidence 与 fixture 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 草稿已生成，但仍不是 formal decision。",
            "",
            "### 下一轮",
            "",
            "- 需要 WAES/Harness 独立回填正式 response.json。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_candidate()
    write_outputs(evidence)
    print(
        "headroom_lcx_waes_harness_final_receipt_decision_draft_candidate=generated "
        "status=draft_candidate_ready_not_formal_decision "
        "real_measurement_open=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
