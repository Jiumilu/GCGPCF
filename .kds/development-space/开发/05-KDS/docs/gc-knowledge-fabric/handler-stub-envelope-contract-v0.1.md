---
doc_id: GPCF-DOC-24E496EEA0
title: GC-Knowledge Fabric Handler Stub Envelope Contract v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/handler-stub-envelope-contract-v0.1.md
source_path: docs/gc-knowledge-fabric/handler-stub-envelope-contract-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Handler Stub Envelope Contract v0.1

## 1. 定位

本文是 P0-D16 的 handler stub response envelope contract，不是 HTTP API server 已上线、数据库已接入或 GFIS/GPC 写回已启用的声明。

D16 在 D13-D15 的 handler stub 之上增加统一 envelope 包装层，用于后续 route adapter、审计日志和前端 dry-run 调用对齐。

## 2. 新增对象

| 文件 | 作用 |
|---|---|
| `packages/api/src/handler-stub.ts` | 新增 `invokeHandlerStubEnvelope` 与 envelope 类型 |
| `fixtures/api/gckf-p0-handler-stub-envelope-contract-v0.1.json` | D16 envelope contract 预期摘要 |
| `scripts/api/validate_gckf_p0_handler_stub_envelope_contract.py` | D16 envelope contract validator |
| `docs/gc-knowledge-fabric/handler-stub-envelope-contract-v0.1.md` | D16 说明文档 |
| `docs/harness/loops/loop-round-GPCF-GCKF-P0-D16-001.md` | D16 LOOP evidence |

## 3. Envelope 字段

所有 envelope 必须包含：

| 字段 | 规则 |
|---|---|
| `ok` | 成功为 `true`，失败为 `false` |
| `requestId` | 调用方传入，不由 stub 生成 |
| `traceId` | 调用方传入，不由 stub 生成 |
| `dryRun` | 必须为 `true` |
| `handler` | 当前 handler 名称 |
| `noWrite` | 必须为 `true` |
| `directBusinessWrite` | 必须为 `false` |
| `acceptedLifecycleWrite` | 必须为 `false` |
| `externalApiWrite` | 必须为 `false` |

成功 envelope 额外包含：

| 字段 | 来源 |
|---|---|
| `group` | handler preflight mapping |
| `method` | handler preflight mapping |
| `path` | handler preflight mapping |
| `writeBoundary` | handler preflight mapping |
| `gateRequired` | `requiresWaesGate` |
| `kweRequired` | `requiresKweFlow` |
| `humanOrCommitteeRequired` | `requiresHumanOrCommitteeForFinality` |
| `candidateOnly` | `writeBoundary === "candidate_request"` |
| `preview` | no-write service preview |

失败 envelope 额外包含：

| 字段 | 规则 |
|---|---|
| `errorCode` | `UNKNOWN_HANDLER` 或 `MISSING_SERVICE_METHOD` |
| `errorMessage` | 本地 stub 错误说明 |

## 4. 本轮覆盖

| Case | 预期 |
|---|---|
| KDS domains read-only | 返回成功 envelope，`candidateOnly=false` |
| KDS fact candidate | 返回成功 envelope，`candidateOnly=true`，仍为 no-write |
| WAES RAG gate | 返回成功 envelope，保持 gate check 边界 |
| unknown handler | 返回失败 envelope，不抛出到上层 |
| missing service method | 返回失败 envelope，错误码为 `MISSING_SERVICE_METHOD` |

## 5. 边界

D16 允许：

- 临时编译到 `/tmp`。
- 本地调用 `invokeHandlerStubEnvelope`。
- 在编译后的内存对象中注入 missing-service-method probe。
- 读取本地 fixture。

D16 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 6. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_handler_stub_envelope_contract.py
```

通过条件：

- 3 个成功 envelope 全部通过。
- 2 个失败 envelope 全部返回受控错误码。
- 所有 envelope 均保留 no-write 标志。
- 既有 `invokeHandlerStub` 抛错语义不被改变，D15 negative smoke 可继续回归。

## 7. 下一步

P0-D17 建议进入 route adapter dry-run contract：

- 定义 HTTP-like request 到 handler envelope 的适配边界。
- 保持 no server、no database、no business write。
- 为后续真实路由挂载预留审计字段，但不启用正式写入。
