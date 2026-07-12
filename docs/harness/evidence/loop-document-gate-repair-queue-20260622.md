---
doc_id: GPCF-DOC-LOOPDOCUMENTGATEREPAIRQUEUE20260622
title: Loop Document Gate Repair Queue 20260622
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-document-gate-repair-queue-20260622.md
source_path: docs/harness/evidence/loop-document-gate-repair-queue-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Document Gate Repair Queue 20260622

## Evidence ID

`LOOP-DOCUMENT-GATE-REPAIR-QUEUE-20260622`

## 结论

本 evidence 将 `loop_document_gate.py --check-only` 的 `gate_reasons` 转换为文档治理修复队列。该队列只用于 GPCF 文档治理，不触发真实 KDS API 写入、业务系统写回、状态升级或委员会裁决。

## 当前门禁摘要

| 字段 | 值 |
|---|---|
| gate | `rework_required` |
| gate_reasons | `missing_metadata, missing_readme_dirs, hard_failure:project_group_real_execution_metadata_coverage, localization_debt` |
| queue_item_count | `4` |
| fixed_doc_id_drift | `False` |
| gfis_real_business_lane | `repair_required` |
| accepted | `False` |
| integrated | `False` |
| production_ready | `False` |

## 修复队列

| queue_id | reason | category | owner | priority | status | repair_action |
|---|---|---|---|---|---|---|
| LDG-REPAIR-001 | missing_metadata | document_control | GPCF document governance | P0 | open | 补齐 Markdown frontmatter doc_id/status/project/source_path 等受控元数据后重跑 document_control。 |
| LDG-REPAIR-002 | missing_readme_dirs | directory_index | GPCF document governance | P1 | open | 为缺失 README 的目录补齐目录说明和文档清单，或按受控规则登记例外。 |
| LDG-REPAIR-003 | hard_failure:project_group_real_execution_metadata_coverage | hard_failure | GPCF document governance | P0 | open | 修复 hard failure 检查项 `project_group_real_execution_metadata_coverage` 后重跑 loop_document_gate。 |
| LDG-REPAIR-004 | localization_debt | localization | GPCF document governance | P1 | open | 按中文本地化门禁报告分组修复旧英文或旧口径文档，不改变业务事实状态。 |

## 非声明

- 本 evidence 不证明 GFIS 真实业务链路完成。
- 本 evidence 不创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本 evidence 不授权生产写入、真实外部 API、数据库迁移、权限变更、提交、推送或合并。
