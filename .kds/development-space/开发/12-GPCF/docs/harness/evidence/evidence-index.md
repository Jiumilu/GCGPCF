---
doc_id: GPCF-DOC-5D0159ED7D
title: Evidence Index — GPCF
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/evidence-index.md
source_path: docs/harness/evidence/evidence-index.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Evidence Index — GPCF

## 证据索引

| 轮次 | Round ID | evidence 类型 | 文件 | 是否完整 | Harness 结论 |
|---|---|---|---|---|---|
| 1 | GPCF-CF-LR-001 | loop state | `docs/harness/loop-state.md` | yes | partial |
| 1 | GPCF-CF-LR-001 | loop record | `docs/harness/loops/loop-round-GPCF-CF-LR-001.md` | yes | partial |
| 1 | GPCF-CF-LR-001 | maturity matrix | `09-status/globalcloud-project-document-loop-maturity-matrix.md` | yes | partial |
| 1 | GPCF-CF-LR-001 | document register | `09-status/globalcloud-document-control-register.md` | yes | controlled |
| 1 | GPCF-CF-LR-001 | command log | 本次对话工具输出 | partial | 未独立落盘 |
| 1 | GPCF-CF-LR-001 | Git evidence | `git status --short --branch` | partial | 工作区 dirty |
| 1 | GPCF-CF-LR-001 | KDS token evidence | `python3 tools/kds-sync/validate_kds_token.py` | yes | blocked |
| - | - | audit report | `docs/harness/status-audit-2026-06-10.md` | yes | 历史首轮纳入 |

## 完整率统计

| 统计项 | 值 |
|---|---|
| 已完成轮次 | 1 |
| evidence 完整轮次 | 0 |
| 证据完整率 | 60% |

## 缺口

- 本轮 command log 未独立落盘。
- KDS TOKEN 未配置，KDS API 级双向同步无法判定完成。
- Git 工作区存在未提交治理变更，尚不能作为 clean evidence。
