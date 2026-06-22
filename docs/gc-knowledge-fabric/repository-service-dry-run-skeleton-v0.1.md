---
doc_id: GPCF-DOC-41D9234F52
title: GC-Knowledge Fabric Repository / Service Dry-run 骨架 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/repository-service-dry-run-skeleton-v0.1.md
source_path: docs/gc-knowledge-fabric/repository-service-dry-run-skeleton-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Repository / Service Dry-run 骨架 v0.1

## 1. 定位

本文是 P0-D10 的 Repository / Service dry-run 骨架说明，不是运行态 API 完成声明。

D10 只建立 API 层到后续数据访问层的最小 no-write 边界：

- 不连接数据库。
- 不执行 migration。
- 不启动 API server。
- 不调用外部 API。
- 不写 KDS 正式对象。
- 不写 GFIS / GPC / ERP / MES 等业务系统。
- 不写 accepted / published / written_back 等正式状态。

## 2. 新增代码边界

| 分组 | Repository | Service | 边界 |
|---|---|---|---|
| KDS v2 | `packages/api/src/kds/v2/repository.ts` | `packages/api/src/kds/v2/service.ts` | search 为 read_only，source/fact/sop/writeback 只进入 candidate request |
| WAES | `packages/api/src/waes/repository.ts` | `packages/api/src/waes/service.ts` | gate/freeze 只生成 gate_check 预览，不写 gate result |
| KWE | `packages/api/src/kwe/repository.ts` | `packages/api/src/kwe/service.ts` | work/gap/confirmation/writeback 只生成 work_request 预览 |
| GFIS Assistant | `packages/api/src/gfis/repository.ts` | `packages/api/src/gfis/service.ts` | query 为 read_only，document/writeback 只生成 candidate request |
| Governance LOOP | `packages/api/src/governance/repository.ts` | `packages/api/src/governance/service.ts` | LOOP/evidence 为 governance_evidence_request，ledger 为 read |

共同 no-write contract：

- `packages/api/src/no-write-repository.ts`

## 3. 校验口径

D10 validator：

```bash
python3 scripts/api/validate_gckf_p0_repository_service_dry_run.py
```

通过条件：

- 5 个 API 分组均有 repository/service 文件。
- `packages/api/src/index.ts` 暴露 10 个新增 repository/service export。
- 所有 service 方法只调用 `.preview(...)`。
- 共同 contract 显式声明 `noWrite: true`、`connectsDatabase: false`、`callsExternalApi: false`、`writesKds: false`、`writesBusinessSystem: false`、`writesAcceptedLifecycle: false`。
- 禁止出现数据库、外部 API、SQL 写入、drop/truncate 等运行时关键词。
- `tsc -p packages/api/tsconfig.json --noEmit` 通过。

## 4. 下一步

P0-D11 建议进入 service handler dry-run：

- 把 route handler 名称与 service 方法建立静态映射。
- 继续不启动 server、不接数据库、不做真实写入。
- 明确哪些 handler 只返回 preview，哪些必须等待 WAES/KWE/Harness 后才能进入实现。
