---
doc_id: GPCF-DOC-CF45B45B64
title: GC-Knowledge Fabric Handler Request / Response Dry-run 样例 v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-request-response-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-request-response-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler Request / Response Dry-run 样例 v0.1

## 1. 定位

本文是 P0-D12 的 handler request / response dry-run 样例说明，不是 API server 可调用验收。

D12 只从现有 route skeleton 派生 40 个 handler 的最小 request / response 样例，用于确认每个 handler 的输入、输出和 no-write 边界。

## 2. 产物

| 产物 | 路径 | 作用 |
|---|---|---|
| 生成器 | `scripts/api/generate_gckf_p0_handler_request_response_fixture.py` | 从 route skeleton 生成 40 条 dry-run 样例 |
| Fixture | `fixtures/api/gckf-p0-handler-request-response-dry-run-v0.1.json` | 保存 40 条 request / response 样例 |
| Validator | `scripts/api/validate_gckf_p0_handler_request_response_dry_run.py` | 校验样例 no-write 边界与 TypeScript noEmit |

## 3. 样例边界

每个 response 必须保留：

- `noWrite: true`
- `directBusinessWrite: false`
- `acceptedLifecycleWrite: false`
- `externalApiWrite: false`
- `writeBoundary`

每个 request 必须保留：

- `tenantId`
- `requestId`
- `dryRun: true`

## 4. 校验命令

```bash
python3 scripts/api/generate_gckf_p0_handler_request_response_fixture.py
python3 scripts/api/validate_gckf_p0_handler_request_response_dry_run.py
```

通过条件：

- 40 个 handler 均有 request / response 样例。
- 5 个 API 分组均覆盖。
- 每条 request 都是 dry-run。
- 每条 response 都不写业务系统、不写 accepted lifecycle、不调用外部 API。
- TypeScript noEmit 通过。

## 5. 下一步

P0-D13 建议进入 route handler stub：

- 以 D12 fixture 为输入，为 40 个 handler 建立最小 handler stub。
- handler stub 只能调用 service preview。
- 继续不启动 server、不接数据库、不做真实写入。
