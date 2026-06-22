---
doc_id: GPCF-DOC-234FFF6184
title: GC-Knowledge Fabric Handler Stub Negative Smoke v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-stub-negative-smoke-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-stub-negative-smoke-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler Stub Negative Smoke v0.1

## 1. 定位

本文是 P0-D15 的 handler stub negative smoke 说明，不是 API server 已上线、数据库已接入或 GFIS/GPC 写回已启用的声明。

D15 在 D14 正向 runtime smoke 之后补齐失败路径和越权边界验证，确保 handler stub 对未知入口、缺失 service method、read-only / candidate 边界和 accepted lifecycle 写入保持阻断。

## 2. 新增对象

| 文件 | 作用 |
|---|---|
| `fixtures/api/gckf-p0-handler-stub-negative-smoke-v0.1.json` | D15 negative smoke 预期摘要 |
| `scripts/api/validate_gckf_p0_handler_stub_negative_smoke.py` | D15 negative smoke validator |
| `docs/gc-knowledge-fabric/handler-stub-negative-smoke-v0.1.md` | D15 说明文档 |
| `docs/harness/loops/loop-round-GPCF-GCKF-P0-D15-001.md` | D15 LOOP evidence |

## 3. Negative smoke 覆盖

| Case | 预期 |
|---|---|
| unknown handler | 必须抛出 `Unknown handler stub` |
| missing service method | 注入探针映射后必须抛出 `Missing service method` |
| read-only boundary | 不得变成 `candidate_request` |
| candidate request | 必须保持 `candidate_request`，但仍为 no-write |
| accepted lifecycle | 必须保持 blocked，不得写 accepted / published / written_back |

## 4. 边界

D15 允许：

- 临时编译到 `/tmp`。
- 本地调用 handler stub 函数。
- 在编译后的内存对象中注入 negative probe mapping。
- 读取本地 fixture。

D15 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 5. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_handler_stub_negative_smoke.py
```

通过条件：

- 5 个 negative case 全部通过。
- 2 个错误路径均抛出预期错误。
- 3 个 guard case 均保持 no-write。
- candidate case 仍需 WAES/KWE 后续流程，不形成正式事实。

## 6. 下一步

P0-D16 建议进入 handler stub response envelope contract：

- 统一成功响应 envelope。
- 统一错误响应 envelope。
- 明确 traceId / requestId / dryRun / gateRequired 字段。
- 继续不启 server、不连库、不写业务系统。
