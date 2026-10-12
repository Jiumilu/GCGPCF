---
doc_id: GPCF-DOC-B4EAB2D0DA
title: GC-Knowledge Fabric Route Adapter Dry-run Contract v0.1
project: KDS
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/route-adapter-dry-run-contract-v0.1.md
source_path: docs/gc-knowledge-fabric/route-adapter-dry-run-contract-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Route Adapter Dry-run Contract v0.1

## 1. 定位

本文是 P0-D17 的 route adapter dry-run contract，不是 HTTP API server 已上线、路由框架已接入、数据库已接入或 GFIS/GPC 写回已启用的声明。

D17 只建立 HTTP-like request 到 D16 handler envelope 的本地适配边界，用于后续真实路由挂载前的契约预检。

## 2. 新增对象

| 文件 | 作用 |
|---|---|
| `packages/api/src/route-adapter.ts` | HTTP-like request 到 handler envelope 的 dry-run adapter |
| `fixtures/api/gckf-p0-route-adapter-dry-run-contract-v0.1.json` | D17 route adapter 预期摘要 |
| `scripts/api/validate_gckf_p0_route_adapter_dry_run_contract.py` | D17 route adapter validator |
| `docs/gc-knowledge-fabric/route-adapter-dry-run-contract-v0.1.md` | D17 说明文档 |
| `docs/harness/loops/loop-round-GPCF-GCKF-P0-D17-001.md` | D17 LOOP evidence |

## 3. Adapter 输入

`RouteAdapterDryRunRequest` 必须包含：

| 字段 | 规则 |
|---|---|
| `method` | `GET` 或 `POST` |
| `path` | P0 API route path |
| `body` | 可选 dry-run body |
| `query` | 可选 dry-run query |
| `requestId` | 调用方传入 |
| `traceId` | 调用方传入 |
| `dryRun` | 必须为 `true` |

## 4. Adapter 输出

`RouteAdapterDryRunResponse` 必须包含：

| 字段 | 规则 |
|---|---|
| `ok` | 来源于 handler envelope |
| `statusCode` | `200` / `404` / `405` |
| `handler` | 命中 route 时返回 |
| `envelope` | D16 handler envelope |
| `noWrite` | 必须为 `true` |
| `startsServer` | 必须为 `false` |
| `connectsDatabase` | 必须为 `false` |
| `callsExternalApi` | 必须为 `false` |
| `directBusinessWrite` | 必须为 `false` |
| `acceptedLifecycleWrite` | 必须为 `false` |
| `externalApiWrite` | 必须为 `false` |

## 5. 本轮覆盖

| Case | 预期 |
|---|---|
| `GET /api/v2/domains` | 适配到 `listDomains`，返回 `200` |
| `POST /api/v2/fact-candidates` | 适配到 `createFactCandidate`，保持 `candidateOnly=true` |
| `POST /api/v2/waes/rag-admission/check` | 适配到 `checkRagAdmission` |
| `POST /api/v2/gfis/document-acceptance/check` | 适配到 `checkGfisDocumentAcceptance` |
| `GET /api/v2/governance/ledger/revenue` | 适配到 `getRevenueLedger` |
| 方法不允许 | 返回 `405`，不抛出到上层 |
| 未知路径 | 返回 `404`，不抛出到上层 |

## 6. 边界

D17 允许：

- 临时编译到 `/tmp`。
- 本地调用 `adaptRouteDryRun`。
- 读取本地 fixture。
- 检查 40 条 P0 route 映射完整性。

D17 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 accepted / published / written_back。

## 7. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_route_adapter_dry_run_contract.py
```

通过条件：

- 40 条 route adapter dry-run route 全部可枚举。
- 5 个成功 route case 返回 `200`。
- 2 个失败 route case 返回受控 `404` / `405`。
- 所有响应均保留 no-write、no-server、no-db、no-external-api 标志。

## 8. 下一步

P0-D18 建议进入 API acceptance packet dry-run：

- 将 route adapter 输出整理为 acceptance packet。
- 绑定 validator、fixture、LOOP evidence。
- 继续不启 server、不连库、不写业务系统。
