#!/usr/bin/env python3
"""Build a no-write workpack for Chinese localization debt."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-workpack-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-workpack-20260622.md"
MAX_FINDINGS = 10000


def top_bucket(path: str) -> str:
    if path.startswith("docs/gc-knowledge-fabric/"):
        return "docs/gc-knowledge-fabric"
    if path.startswith("docs/harness/loops/"):
        return "docs/harness/loops"
    if path.startswith("docs/harness/evidence/"):
        return "docs/harness/evidence"
    parts = path.split("/")
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def run_localization_gate() -> dict[str, object]:
    result = subprocess.run(
        [
            sys.executable,
            "tools/kds-sync/check_chinese_localization_gate.py",
            "--json",
            "--max-findings",
            str(MAX_FINDINGS),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        summary = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"localization gate output is not JSON: {exc}") from exc
    if not isinstance(summary, dict):
        raise SystemExit("localization gate summary must be a JSON object")
    return summary


def build_workpack(summary: dict[str, object]) -> dict[str, object]:
    findings = summary.get("sample_findings", [])
    if not isinstance(findings, list):
        raise SystemExit("sample_findings must be a list")

    by_kind = Counter(str(item.get("kind", "unknown")) for item in findings if isinstance(item, dict))
    by_bucket = Counter(top_bucket(str(item.get("path", "unknown"))) for item in findings if isinstance(item, dict))
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in findings:
        if not isinstance(item, dict):
            continue
        bucket = top_bucket(str(item.get("path", "unknown")))
        if len(grouped[bucket]) < 8:
            grouped[bucket].append(item)

    work_items = []
    for index, (bucket, count) in enumerate(by_bucket.most_common(), start=1):
        dominant_kind = Counter(str(item.get("kind", "unknown")) for item in grouped[bucket]).most_common(1)
        work_items.append(
            {
                "workpack_id": f"LOC-DEBT-{index:03d}",
                "bucket": bucket,
                "finding_count": count,
                "dominant_kind": dominant_kind[0][0] if dominant_kind else "unknown",
                "priority": "P1" if bucket.startswith("docs/gc-knowledge-fabric") else "P2",
                "status": "open",
                "sample_findings": grouped[bucket],
                "repair_policy": "分批把用户可见标题、说明和长英文行改为中文优先表达；保留技术缩写、路径、API 名和受控 doc_id。",
                "no_write_boundary": {
                    "bulk_rewrite": False,
                    "business_writeback": False,
                    "real_kds_api_write": False,
                    "status_upgrade": False,
                },
            }
        )

    return {
        "evidence_id": "LOCALIZATION-DEBT-WORKPACK-20260622",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tools/kds-sync/check_chinese_localization_gate.py --json",
        "localization_gate": summary.get("localization_gate"),
        "docs_checked": summary.get("docs_checked"),
        "software_files_checked": summary.get("software_files_checked"),
        "findings": summary.get("findings"),
        "findings_by_kind": dict(by_kind),
        "bucket_count": len(by_bucket),
        "top_buckets": [{"bucket": bucket, "finding_count": count} for bucket, count in by_bucket.most_common(30)],
        "work_item_count": len(work_items),
        "work_items": work_items,
        "known_boundary": {
            "candidate_no_write": True,
            "gfis_real_business_lane": "repair_required",
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def markdown_table(rows: list[list[object]]) -> str:
    lines = ["| workpack_id | bucket | finding_count | dominant_kind | priority | status |", "|---|---|---:|---|---|---|"]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return "\n".join(lines)


def write_markdown(evidence: dict[str, object]) -> None:
    rows = [
        [
            item["workpack_id"],
            item["bucket"],
            item["finding_count"],
            item["dominant_kind"],
            item["priority"],
            item["status"],
        ]
        for item in evidence["work_items"]
    ]
    top_rows = "\n".join(
        f"- `{item['bucket']}`：{item['finding_count']}" for item in evidence["top_buckets"][:20]
    )
    content = f"""---
doc_id: GPCF-DOC-LOCALIZATIONDEBTWORKPACK20260622
title: Localization Debt Workpack 20260622
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/localization-debt-workpack-20260622.md
source_path: docs/harness/evidence/localization-debt-workpack-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Localization Debt Workpack 20260622

## Evidence ID

`{evidence["evidence_id"]}`

## 结论

本 workpack 把中文化门禁的命中项按目录分组，作为 D87 `localization_debt` 修复队列的下一层执行输入。它只生成治理 workpack，不批量改写正文，不触发真实 KDS API 写入、业务系统写回、状态升级或委员会裁决。

## 当前门禁摘要

| 字段 | 值 |
|---|---|
| localization_gate | `{evidence["localization_gate"]}` |
| findings | `{evidence["findings"]}` |
| docs_checked | `{evidence["docs_checked"]}` |
| software_files_checked | `{evidence["software_files_checked"]}` |
| bucket_count | `{evidence["bucket_count"]}` |
| work_item_count | `{evidence["work_item_count"]}` |
| gfis_real_business_lane | `{evidence["known_boundary"]["gfis_real_business_lane"]}` |
| accepted | `{evidence["known_boundary"]["accepted"]}` |
| integrated | `{evidence["known_boundary"]["integrated"]}` |
| production_ready | `{evidence["known_boundary"]["production_ready"]}` |

## 命中类型

```json
{json.dumps(evidence["findings_by_kind"], ensure_ascii=False, indent=2)}
```

## 重点目录

{top_rows}

## Workpack

{markdown_table(rows)}

## 处理原则

- 先处理当前有效受控文档和 GC-Knowledge Fabric 主线文档。
- 技术缩写、API 名、路径、doc_id、证据 ID 和专有名词可以保留英文。
- 每批修复必须 scoped、可回滚、可校验，不做全仓自动大改。
- 修复中文化债务不等于 GFIS 真实业务链路完成。

## 非声明

- 本 evidence 不证明 GFIS 真实业务链路完成。
- 本 evidence 不创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本 evidence 不授权生产写入、真实外部 API、数据库迁移、权限变更、提交、推送或合并。
"""
    EVIDENCE_MD.write_text(content, encoding="utf-8")


def main() -> int:
    summary = run_localization_gate()
    evidence = build_workpack(summary)
    EVIDENCE_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(evidence)
    print("localization_debt_workpack=generated")
    print(f"localization_gate={evidence['localization_gate']}")
    print(f"findings={evidence['findings']}")
    print(f"work_item_count={evidence['work_item_count']}")
    print("execution_mode=local_evidence_no_write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
