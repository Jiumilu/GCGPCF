---
doc_id: GPCF-DOC-C994E78BC6
title: GC-Knowledge Fabric Shared Types 与 API Contract 对齐矩阵 v0.1
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/shared-types-api-contract-alignment-v0.1.md
source_path: docs/gc-knowledge-fabric/shared-types-api-contract-alignment-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Shared Types 与 API Contract 对齐矩阵 v0.1

## 1. 定位

本文是 P0-D8 的 contract 对齐矩阵，不是运行态接口验收。

它把 P0-D7 的 API 骨架输入矩阵映射到本仓已有的 shared types、API contracts、route skeleton 和 endpoint validators，形成后续代码实现前的最小静态校验口径。

## 2. 对齐边界

P0-D8 只检查：

- shared type 文件是否存在。
- API contract 文件是否存在。
- route skeleton 文件是否存在。
- endpoint no-write validator 是否存在。
- D7 API 分组与本地 contract 文件是否可追溯。
- 正式写入、外部 API、业务系统写入计数是否保持 0。

P0-D8 不声明：

- API server 已部署。
- endpoint 可被真实调用。
- KDS / WAES / KWE / GFIS 已产生真实写入。
- accepted / published / written_back 状态已形成。
- 收益、积分、额度、悬赏已确认。

## 3. 首批对齐矩阵

| 分组 | Shared Types | API Contract | Route Skeleton | Validator |
|---|---|---|---|---|
| KDS v2 | `object.ts`, `source.ts`, `evidence.ts`, `fact-candidate.ts`, `sop-candidate.ts`, `writeback-candidate.ts`, `pool.ts`, `rag-admission.ts`, `waes-gate.ts` | `packages/api/src/kds/v2/contracts.ts` | `packages/api/src/kds/v2/routes.ts` | `scripts/kds/validate_kds_v2_endpoint_no_write_smoke.py` |
| WAES | `waes-gate.ts` | `packages/api/src/waes/contracts.ts` | `packages/api/src/waes/routes.ts` | `scripts/waes/validate_waes_endpoint_no_write_smoke.py` |
| KWE | `gap.ts`, `bounty.ts`, `writeback-candidate.ts`, `waes-gate.ts` | `packages/api/src/kwe/contracts.ts` | `packages/api/src/kwe/routes.ts` | `scripts/kwe/validate_kwe_endpoint_no_write_smoke.py` |
| GFIS Assistant | `fact-candidate.ts`, `gap.ts`, `rag-admission.ts`, `waes-gate.ts`, `writeback-candidate.ts` | `packages/api/src/gfis/contracts.ts` | `packages/api/src/gfis/routes.ts` | `scripts/gfis/validate_gfis_endpoint_no_write_smoke.py` |
| Governance LOOP | `bounty.ts`, `contribution.ts`, `evidence.ts`, `loop.ts`, `quota.ts`, `revenue.ts` | `packages/api/src/governance/contracts.ts` | `packages/api/src/governance/routes.ts` | `scripts/governance/validate_governance_endpoint_no_write_smoke.py` |

## 4. 最小校验

D8 汇总 validator：

```bash
python3 scripts/api/validate_gckf_p0_shared_types_api_contract_alignment.py
```

通过条件：

- 5 个 API 分组均有 shared types、contracts、routes、validators。
- D7 矩阵仍为 5 组、40 个端点。
- 5 个 endpoint no-write validators 全部存在。
- forbidden mutation 合计为 0。
- 汇总输出不触发真实 API、不写 KDS、不写业务系统。

## 5. 下一步

P0-D9 建议进入数据库表与迁移草案矩阵：

- 对齐 `knowledge_objects`、`object_pool_bindings`、`waes_gate_results`、`kwe_work_items` 等 P0 表。
- 只生成 schema dry-run / migration draft，不执行数据库迁移。
- 继续保持 no-write、no-production、no-accepted。
