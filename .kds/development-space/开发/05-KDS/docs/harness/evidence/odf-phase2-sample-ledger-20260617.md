---
doc_id: GPCF-DOC-86BB2ABBFD
title: ODF Phase 2 样本准入台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/odf-phase2-sample-ledger-20260617.md
source_path: docs/harness/evidence/odf-phase2-sample-ledger-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# ODF Phase 2 样本准入台账

日期：2026-06-17

## 试点边界

- 不全量导入 ODF。
- 不批量改写现有 Markdown 正文。
- 不把 ODF 当作 Git、KDS、OKF 或 Loop evidence 的替代品。
- 不自动升级 `accepted` 或 `integrated`。

## 样本统计

| category | count |
| --- | ---: |
| governance | 2 |
| kds-knowledge | 2 |
| okf-navigation | 1 |
| business-import | 3 |
| loop-harness-evidence | 2 |

## 样本清单

| sample_id | category | source_path | owner | status |
| --- | --- | --- | --- | --- |
| `ODF-PHASE2-20260617-001` | governance | `02-governance/GlobalCloud项目群文档综合治理规范.md` | WAES | `phase2_sample` |
| `ODF-PHASE2-20260617-002` | governance | `02-governance/GlobalCloud项目群文档防污染规则.md` | WAES | `phase2_sample` |
| `ODF-PHASE2-20260617-003` | kds-knowledge | `03-data-ai-knowledge/GlobalCloud Loop开发KDS关联数据检索机制.md` | KDS | `phase2_sample` |
| `ODF-PHASE2-20260617-004` | kds-knowledge | `03-data-ai-knowledge/GlobalCloudBrain-KDS知识编制与知识UI边界清单.md` | KDS | `phase2_sample` |
| `ODF-PHASE2-20260617-005` | okf-navigation | `.okf/index.md` | GPCF | `phase2_sample` |
| `ODF-PHASE2-20260617-006` | business-import | `03-data-ai-knowledge/GlobalCloud湖北磷材拓厂项目知识库与新工厂复制模板.md` | KDS | `phase2_sample` |
| `ODF-PHASE2-20260617-007` | business-import | `03-data-ai-knowledge/GlobalCloud葛化首批资料包入库验收与GFISAI助手试运行任务书.md` | KDS | `phase2_sample` |
| `ODF-PHASE2-20260617-008` | business-import | `03-data-ai-knowledge/GlobalCloud辽宁远航链路证据缺口请求包与知识悬赏草案.md` | KDS | `phase2_sample` |
| `ODF-PHASE2-20260617-009` | loop-harness-evidence | `docs/harness/evidence/evidence-index.md` | GPCF | `phase2_sample` |
| `ODF-PHASE2-20260617-010` | loop-harness-evidence | `docs/harness/evidence/odf-pilot-closure-report-20260617.md` | KDS | `phase2_sample` |

## 准入字段完整性

全部样本必须具备：`source_uri`、`source_hash`、`odf_hash`、`markdown_hash`、`conversion_method`、`conversion_actor`、`owner`、`source_path`、`kds_path`、`sensitivity_check`、`status`、`rollback_hint`。

## 结论

Phase 2 样本已覆盖五类场景，并完成文档控制、KDS 定向同步和门禁验证。当前状态：`phase2_closed`。下一阶段允许进入 `yes_with_gate`，但不得进入全量推广。
