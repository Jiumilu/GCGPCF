---
doc_id: GPCF-DOC-03A3C0DFE5
title: GC-Knowledge Fabric Handler 到 Service Dry-run Preflight v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-service-preflight-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-service-preflight-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler 到 Service Dry-run Preflight v0.1

## 1. 定位

本文是 P0-D11 的 handler-level no-write preflight 说明，不是 API handler 已运行声明。

D11 只建立 route handler 到 service 方法的静态映射，目标是保证 P0 API 骨架中的 40 个 endpoint 都有明确的 service 落点和 no-write 边界。

## 2. 映射对象

| 分组 | Endpoint 数 | Route | Service | Handler map |
|---|---:|---|---|---|
| KDS v2 | 11 | `packages/api/src/kds/v2/routes.ts` | `packages/api/src/kds/v2/service.ts` | `packages/api/src/handler-map.ts` |
| WAES | 7 | `packages/api/src/waes/routes.ts` | `packages/api/src/waes/service.ts` | `packages/api/src/handler-map.ts` |
| KWE | 10 | `packages/api/src/kwe/routes.ts` | `packages/api/src/kwe/service.ts` | `packages/api/src/handler-map.ts` |
| GFIS Assistant | 4 | `packages/api/src/gfis/routes.ts` | `packages/api/src/gfis/service.ts` | `packages/api/src/handler-map.ts` |
| Governance LOOP | 8 | `packages/api/src/governance/routes.ts` | `packages/api/src/governance/service.ts` | `packages/api/src/handler-map.ts` |

## 3. 门禁边界

每个 mapping 必须显式保持：

- `directBusinessWrite: false`
- `acceptedLifecycleWrite: false`
- `externalApiWrite: false`
- `noWrite: true`

D11 仍不允许：

- 启动 API server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 4. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_handler_service_preflight.py
```

通过条件：

- 5 个 API 分组共 40 个 route handler 全部进入 `HANDLER_PREFLIGHT_MAPPINGS`。
- 每个 handler 的 `serviceMethod` 在对应 service 文件中存在。
- `packages/api/src/index.ts` 导出 `handler-map`。
- TypeScript noEmit 通过。
- 禁止出现数据库、外部 API、SQL 写入、server listen 等运行时关键词。

## 5. 下一步

P0-D12 建议进入 handler request/response fixture：

- 为 40 个 handler 生成最小 request/response dry-run 样例。
- 继续不启动 server、不接数据库、不做真实写入。
- 明确候选、门禁、工单、证据、台账的返回边界。
