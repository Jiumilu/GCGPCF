#!/usr/bin/env python3
"""Build a controlled repair queue from loop_document_gate gate_reasons."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-document-gate-repair-queue-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-document-gate-repair-queue-20260622.md"

REASON_CATALOG: dict[str, dict[str, str]] = {
    "missing_metadata": {
        "category": "document_control",
        "owner": "GPCF document governance",
        "priority": "P0",
        "repair_action": "补齐 Markdown frontmatter doc_id/status/project/source_path 等受控元数据后重跑 document_control。",
    },
    "missing_readme_dirs": {
        "category": "directory_index",
        "owner": "GPCF document governance",
        "priority": "P1",
        "repair_action": "为缺失 README 的目录补齐目录说明和文档清单，或按受控规则登记例外。",
    },
    "localization_debt": {
        "category": "localization",
        "owner": "GPCF document governance",
        "priority": "P1",
        "repair_action": "按中文本地化门禁报告分组修复旧英文或旧口径文档，不改变业务事实状态。",
    },
    "kds_token_blocked": {
        "category": "security",
        "owner": "KDS operator",
        "priority": "P0",
        "repair_action": "在本机私有环境补齐 KDS TOKEN，仅验证 fingerprint，不写入 Git、文档或日志。",
    },
    "fixed_doc_id_drift": {
        "category": "identity_integrity",
        "owner": "GPCF document governance",
        "priority": "P0",
        "repair_action": "恢复固定 doc_id，重跑固定编号漂移 validator，并复核 D75-D86 受控文档索引。",
    },
    "kds_mirror_coverage_gap": {
        "category": "kds_local_mirror",
        "owner": "KDS mirror operator",
        "priority": "P1",
        "repair_action": "重跑 scoped document_control 或本地镜像同步，确认 local mirror ledger 与 Markdown 覆盖一致。",
    },
}


def run_loop_gate() -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, "tools/kds-sync/loop_document_gate.py", "--check-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        summary = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"loop_document_gate output is not JSON: {exc}") from exc
    if not isinstance(summary, dict):
        raise SystemExit("loop_document_gate summary must be a JSON object")
    return summary


def reason_item(reason: str, index: int) -> dict[str, object]:
    if reason.startswith("hard_failure:"):
        check_name = reason.split(":", 1)[1]
        catalog = {
            "category": "hard_failure",
            "owner": "GPCF document governance",
            "priority": "P0",
            "repair_action": f"修复 hard failure 检查项 `{check_name}` 后重跑 loop_document_gate。",
        }
    else:
        catalog = REASON_CATALOG.get(
            reason,
            {
                "category": "unknown",
                "owner": "GPCF document governance",
                "priority": "P1",
                "repair_action": "确认未知 gate reason 的来源，补充 reason catalog 后再制定修复动作。",
            },
        )
    return {
        "queue_id": f"LDG-REPAIR-{index:03d}",
        "reason": reason,
        "category": catalog["category"],
        "owner": catalog["owner"],
        "priority": catalog["priority"],
        "status": "open" if reason else "not_required",
        "repair_action": catalog["repair_action"],
        "allowed_mode": "controlled_document_governance_only",
        "no_write_boundary": {
            "production_write": False,
            "business_writeback": False,
            "real_kds_api_write": False,
            "status_upgrade": False,
        },
    }


def build_evidence(summary: dict[str, object]) -> dict[str, object]:
    reasons = summary.get("gate_reasons", [])
    if not isinstance(reasons, list):
        raise SystemExit("gate_reasons must be a list")
    queue_items = [reason_item(str(reason), index) for index, reason in enumerate(reasons, start=1)]
    return {
        "evidence_id": "LOOP-DOCUMENT-GATE-REPAIR-QUEUE-20260622",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tools/kds-sync/loop_document_gate.py --check-only",
        "gate": summary.get("gate"),
        "gate_reasons": reasons,
        "queue_item_count": len(queue_items),
        "queue_items": queue_items,
        "known_boundary": {
            "candidate_no_write": True,
            "gfis_real_business_lane": "repair_required",
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "source_summary": {
            "localization_debt": summary.get("localization_debt"),
            "fixed_doc_id_drift": summary.get("fixed_doc_id_drift"),
            "missing_metadata": summary.get("missing_metadata"),
            "missing_readme_dirs": summary.get("missing_readme_dirs"),
        },
    }


def write_markdown(evidence: dict[str, object]) -> None:
    rows = []
    for item in evidence["queue_items"]:
        rows.append(
            "| {queue_id} | {reason} | {category} | {owner} | {priority} | {status} | {repair_action} |".format(
                **item
            )
        )
    queue_rows = "\n".join(rows) if rows else "| - | none | - | - | - | closed | 当前无门禁修复项 |"
    content = f"""---
doc_id: GPCF-DOC-LOOPDOCUMENTGATEREPAIRQUEUE20260622
title: Loop Document Gate Repair Queue 20260622
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/loop-document-gate-repair-queue-20260622.md
source_path: docs/harness/evidence/loop-document-gate-repair-queue-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Document Gate Repair Queue 20260622

## Evidence ID

`{evidence["evidence_id"]}`

## 结论

本 evidence 将 `loop_document_gate.py --check-only` 的 `gate_reasons` 转换为文档治理修复队列。该队列只用于 GPCF 文档治理，不触发真实 KDS API 写入、业务系统写回、状态升级或委员会裁决。

## 当前门禁摘要

| 字段 | 值 |
|---|---|
| gate | `{evidence["gate"]}` |
| gate_reasons | `{", ".join(evidence["gate_reasons"]) if evidence["gate_reasons"] else "none"}` |
| queue_item_count | `{evidence["queue_item_count"]}` |
| fixed_doc_id_drift | `{evidence["source_summary"]["fixed_doc_id_drift"]}` |
| gfis_real_business_lane | `{evidence["known_boundary"]["gfis_real_business_lane"]}` |
| accepted | `{evidence["known_boundary"]["accepted"]}` |
| integrated | `{evidence["known_boundary"]["integrated"]}` |
| production_ready | `{evidence["known_boundary"]["production_ready"]}` |

## 修复队列

| queue_id | reason | category | owner | priority | status | repair_action |
|---|---|---|---|---|---|---|
{queue_rows}

## 非声明

- 本 evidence 不证明 GFIS 真实业务链路完成。
- 本 evidence 不创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本 evidence 不授权生产写入、真实外部 API、数据库迁移、权限变更、提交、推送或合并。
"""
    EVIDENCE_MD.write_text(content, encoding="utf-8")


def main() -> int:
    summary = run_loop_gate()
    evidence = build_evidence(summary)
    EVIDENCE_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(evidence)
    print("loop_document_gate_repair_queue=generated")
    print(f"gate={evidence['gate']}")
    print(f"gate_reasons={','.join(evidence['gate_reasons']) if evidence['gate_reasons'] else 'none'}")
    print(f"queue_item_count={evidence['queue_item_count']}")
    print("execution_mode=local_evidence_no_write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
