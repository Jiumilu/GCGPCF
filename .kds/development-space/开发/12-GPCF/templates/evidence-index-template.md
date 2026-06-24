---
doc_id: GPCF-DOC-33F4C1195D
title: 证据索引模板 — {项目名}
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/evidence-index-template.md
source_path: templates/evidence-index-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 证据索引模板 — {项目名}

> 证据索引表。存放位置：项目仓 `docs/harness/evidence/evidence-index.md`。

## 证据索引

| 轮次 | Round ID | evidence 类型 | 文件 | 是否完整 | Harness 结论 |
|---|---|---|---|---|---|
| 1 | GPCF-{XX}-LR-001 | loop record | loop-round-GPCF-{XX}-LR-001.md | yes/no | |
| 1 | GPCF-{XX}-LR-001 | diff evidence | diff-GPCF-{XX}-LR-001.patch | yes/no | |
| 1 | GPCF-{XX}-LR-001 | command log | command-log-GPCF-{XX}-LR-001.txt | yes/no | |
| 1 | GPCF-{XX}-LR-001 | test result | test-result-GPCF-{XX}-LR-001.md | yes/no | |
| 1 | GPCF-{XX}-LR-001 | metric json | metrics-GPCF-{XX}-LR-001.json | yes/no | |
| - | - | audit report | status-audit-YYYY-MM-DD.md | yes/no | |

## 完整率统计

| 统计项 | 值 |
|---|---|
| 已完成轮次 | {N} |
| evidence 完整轮次 | {M} |
| 证据完整率 | {M/N * 100}% |
