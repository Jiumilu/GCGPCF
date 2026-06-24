---
doc_id: GPCF-DOC-0F8D7C00F5
title: GC-Knowledge Fabric Handler Stub Runtime Smoke v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-stub-runtime-smoke-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-stub-runtime-smoke-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler Stub Runtime Smoke v0.1

## 1. 定位

本文是 P0-D14 的 handler stub runtime smoke 说明，不是 HTTP API 已上线、数据库已接入或 GFIS/GPC 写回已启用的声明。

D14 在 D13 的 `invokeHandlerStub` 基础上，实际调用 40 个 D12 dry-run case，证明 handler map、service preview 与 no-write repository 可以在本地执行路径内闭合。

## 2. 新增对象

| 文件 | 作用 |
|---|---|
| `fixtures/api/gckf-p0-handler-stub-runtime-smoke-v0.1.json` | D14 runtime smoke 预期摘要 |
| `scripts/api/validate_gckf_p0_handler_stub_runtime_smoke.py` | D14 runtime smoke validator |
| `docs/gc-knowledge-fabric/handler-stub-runtime-smoke-v0.1.md` | D14 说明文档 |
| `docs/harness/loops/loop-round-GPCF-GCKF-P0-D14-001.md` | D14 LOOP evidence |

## 3. 执行方式

Validator 执行以下动作：

1. 使用 `tsc` 将 `packages/api` TypeScript 编译到 `/tmp/gckf-api-smoke-runtime`。
2. 使用 Node 加载 `/tmp/gckf-api-smoke-runtime/api/src/handler-stub.js`。
3. 读取 `fixtures/api/gckf-p0-handler-request-response-dry-run-v0.1.json`。
4. 对 40 个 case 逐条调用 `invokeHandlerStub`。
5. 校验 handler、group、serviceName、serviceMethod、writeBoundary 和 preview operation 一致。
6. 校验所有响应继续保持 no-write 标志。

## 4. 边界

D14 允许：

- 临时编译到 `/tmp`。
- 本地调用 handler stub 函数。
- 读取本地 fixture。
- 验证 response preview。

D14 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 5. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_handler_stub_runtime_smoke.py
```

通过条件：

- 40 个 dry-run case 全部可调用。
- 5 个 handler group 全部覆盖。
- TypeScript runtime compile 通过。
- 所有 preview 均为 `noWrite: true`。
- 所有 preview 均声明不连接数据库、不调用外部 API、不写 KDS、不写业务系统、不写 accepted lifecycle。

## 6. 下一步

P0-D15 建议进入 handler stub negative smoke：

- 未知 handler 必须失败。
- 缺失 service method 必须失败。
- 非 candidate case 不得出现 candidate write boundary。
- candidate case 仍不得越过 WAES/KWE/人工确认边界。
