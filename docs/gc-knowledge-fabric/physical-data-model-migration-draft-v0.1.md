---
doc_id: GPCF-DOC-565A8097A4
title: GC-Knowledge Fabric 物理数据模型与 Migration Draft 矩阵 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, MMC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/physical-data-model-migration-draft-v0.1.md
source_path: docs/gc-knowledge-fabric/physical-data-model-migration-draft-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 物理数据模型与 Migration Draft 矩阵 v0.1

## 1. 定位

本文是 P0-D9 的物理数据模型与 migration draft 矩阵，不是数据库迁移完成声明。

本轮只补齐 `packages/api/src/kds/v2/schema.sql` 中的 P0 表草案，并用本地 validator 解析 SQL 文本。不得执行 `migrate`、不得连接数据库、不得写生产库。

## 2. 表分组

| 分组 | 表 | 作用 |
|---|---|---|
| KDS core | `knowledge_objects`, `knowledge_sources`, `knowledge_evidence`, `knowledge_events` | 知识对象、来源、证据、事件 |
| KDS index / ACL | `knowledge_acl`, `knowledge_embeddings`, `knowledge_index_jobs`, `kds_pools`, `object_pool_bindings` | 权限、索引、池子挂接 |
| Candidate | `fact_candidates`, `sop_candidates`, `writeback_candidates` | AI / 人工 / 系统候选 |
| WAES | `waes_gate_results`, `waes_gate_policies` | 门禁结果候选与门禁策略版本 |
| KWE | `kwe_work_items`, `kwe_workpacks`, `gap_records`, `bounty_records`, `confirmation_records` | 流程、确认、缺口、悬赏 |
| Governance | `committee_records`, `dispute_records`, `decision_records`, `loop_records`, `harness_evidence_records`, `okf_policy_versions` | 委员会、争议、决策、LOOP、证据、策略版本 |
| Ledger | `contribution_records`, `revenue_records`, `quota_records` | 积分、收益、额度台账 |
| MMC / Agent | `capability_invocations`, `agent_used_knowledge` | AI / Agent / Connector 调用审计 |

## 3. P0 表清单

P0-D9 schema draft 合计 30 张表：

- `knowledge_objects`
- `knowledge_sources`
- `knowledge_evidence`
- `object_pool_bindings`
- `fact_candidates`
- `sop_candidates`
- `writeback_candidates`
- `knowledge_events`
- `knowledge_acl`
- `knowledge_embeddings`
- `knowledge_index_jobs`
- `kds_pools`
- `waes_gate_results`
- `waes_gate_policies`
- `kwe_work_items`
- `kwe_workpacks`
- `gap_records`
- `bounty_records`
- `confirmation_records`
- `committee_records`
- `dispute_records`
- `contribution_records`
- `revenue_records`
- `quota_records`
- `decision_records`
- `loop_records`
- `harness_evidence_records`
- `capability_invocations`
- `agent_used_knowledge`
- `okf_policy_versions`

## 4. 不执行项

P0-D9 不做：

- 不执行数据库迁移。
- 不连接 Postgres / SQLite / 生产库。
- 不创建真实 KDS 记录。
- 不写 WAES gate result。
- 不创建 KWE work item。
- 不写 GFIS / GPC / ERP / MES。
- 不确认收益、积分、额度、悬赏。

## 5. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_physical_data_model_schema_dry_run.py
```

通过条件：

- `schema.sql` 中 30 张 P0 表均存在。
- 每张表均有 `id TEXT PRIMARY KEY`。
- 每张表均有 `tenant_id TEXT NOT NULL`。
- schema draft 不包含 `DROP TABLE`、`ALTER TABLE`、`INSERT`、`UPDATE`、`DELETE`。
- fixture 中所有真实写入计数为 0。

## 6. 下一步

P0-D10 建议进入最小 Repository / Service 骨架：

- 只实现本地 in-memory 或 dry-run repository。
- 不连接真实数据库。
- 将 D9 schema draft 与 D7/D8 contract validator 串联。
