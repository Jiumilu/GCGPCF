---
doc_id: GPCF-DOC-CB3D761E21
title: GC-Knowledge Fabric Handler Stub Preview v0.1
project: KDS
related_projects: [GFIS, GPC, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-stub-preview-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-stub-preview-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler Stub Preview v0.1

## 1. 定位

本文是 P0-D13 的 handler stub preview 说明，不是 API server 已部署或可对外调用声明。

D13 建立一个统一 handler stub dispatcher，用于把 D11 的 handler mapping 和 D12 的 request / response dry-run 样例连接到 service preview。

## 2. 新增代码

| 文件 | 作用 |
|---|---|
| `packages/api/src/handler-stub.ts` | 统一 handler stub dispatcher |
| `fixtures/api/gckf-p0-handler-stub-preview-v0.1.json` | D13 校验 fixture |
| `scripts/api/validate_gckf_p0_handler_stub_preview.py` | D13 validator |

## 3. 调用边界

`invokeHandlerStub` 只允许：

- 根据 handler 名称查找 `HANDLER_PREFLIGHT_MAPPINGS`。
- 根据 `serviceName` / `serviceMethod` 调用已有 service preview。
- 返回 `noWrite: true` 的 preview 结果。

`invokeHandlerStub` 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 4. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_handler_stub_preview.py
```

通过条件：

- D12 的 40 个 handler request 样例均可映射到 service registry。
- 5 个 service registry 均存在。
- `packages/api/src/index.ts` 导出 `handler-stub`。
- TypeScript noEmit 通过。
- 禁止出现数据库、外部 API、SQL 写入、server listen 等运行时关键词。

## 5. 下一步

P0-D14 建议进入 handler stub runtime smoke：

- 用 Node/TypeScript 可执行路径实际调用 `invokeHandlerStub` 的 dry-run。
- 只使用本地 fixture。
- 继续不启动 server、不接数据库、不做真实写入。
