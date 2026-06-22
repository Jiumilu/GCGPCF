---
doc_id: GPCF-DOC-D7663D64F9
title: GC-Knowledge Fabric P0-D9 物理数据模型与 Migration Draft LOOP evidence
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D9-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D9-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0-D9 物理数据模型与 Migration Draft LOOP evidence

## 本轮目标

完成 P0-D9：建立物理数据模型与 migration draft 矩阵，把 P0 表草案补齐到本地 `schema.sql`，并用静态 validator 验证，不执行数据库迁移。

## 本轮输入资料

- `packages/api/src/kds/v2/schema.sql`
- `docs/gc-knowledge-fabric/shared-types-api-contract-alignment-v0.1.md`
- `fixtures/api/gckf-p0-shared-types-api-contract-alignment-v0.1.json`
- 原方案 P0 物理数据模型表清单

## 本轮新增知识对象

- `docs/gc-knowledge-fabric/physical-data-model-migration-draft-v0.1.md`
- `fixtures/api/gckf-p0-physical-data-model-schema-dry-run-v0.1.json`
- `scripts/api/validate_gckf_p0_physical_data_model_schema_dry_run.py`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D9-001.md`

## 本轮修改对象

- `packages/api/src/kds/v2/schema.sql`

## 本轮检查

| 检查项 | 结果 |
|---|---|
| P0 表数量 | 30 |
| 表分组数量 | 8 |
| 是否包含 id 主键 | 是 |
| 是否包含 tenant_id | 是 |
| 是否执行 migrate | 否 |
| 是否连接数据库 | 否 |
| 是否写 KDS / WAES / KWE / 业务系统 | 否 |
| 是否包含 DROP / ALTER / INSERT / UPDATE / DELETE | 否 |

## 风险与阻塞

| 风险 | 等级 | 处理 |
|---|---|---|
| schema draft 被误认为已迁移 | P1 | 文档和 validator 明确 `runsMigration=0` |
| 表字段仍需工程细化 | P2 | 本轮只建立 P0 表存在性与审计边界 |
| 后续真实迁移影响运行库 | P1 | D9 不连接数据库，真实迁移需单独授权 |

## 下一轮动作

进入 P0-D10：

- 建立最小 Repository / Service dry-run 骨架。
- 将 D7 API、D8 contract、D9 schema validator 串联为本地 no-write harness。
- 不连接真实数据库、不写生产库、不升级 accepted / integrated。
