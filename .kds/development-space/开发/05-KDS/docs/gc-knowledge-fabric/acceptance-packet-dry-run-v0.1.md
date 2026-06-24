---
doc_id: GPCF-DOC-F59EC32059
title: GC-Knowledge Fabric Acceptance Packet Dry-run v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/acceptance-packet-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/acceptance-packet-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Acceptance Packet Dry-run v0.1

## 1. 定位

本文是 P0-D18 的 acceptance packet dry-run contract，不是 Harness 最终验收、正式 evidence 写入或业务系统上线声明。

D18 把 D17 route adapter 的输出聚合成可审计验收候选包，用于后续人工 review、Harness evidence 固化和 LOOP 收口。

## 2. 新增对象

| 文件 | 作用 |
|---|---|
| `packages/api/src/acceptance-packet.ts` | acceptance packet dry-run 类型与聚合函数 |
| `fixtures/api/gckf-p0-acceptance-packet-dry-run-v0.1.json` | D18 acceptance packet fixture |
| `scripts/api/validate_gckf_p0_acceptance_packet_dry_run.py` | D18 validator |
| `docs/gc-knowledge-fabric/acceptance-packet-dry-run-v0.1.md` | D18 说明文档 |
| `docs/harness/loops/loop-round-GPCF-GCKF-P0-D18-001.md` | D18 LOOP evidence |

## 3. Packet 输入

`AcceptancePacketDryRunRequest` 必须包含：

| 字段 | 规则 |
|---|---|
| `packetId` | 验收包编号 |
| `title` | 验收包标题 |
| `routeRequests` | D17 HTTP-like route request 列表 |
| `evidenceRefs` | fixture、validator、contract doc、LOOP evidence 引用 |
| `requestedBy` | 发起人或系统 |
| `requestId` | 调用方传入 |
| `traceId` | 调用方传入 |
| `dryRun` | 必须为 `true` |

## 4. Packet 输出

`AcceptancePacketDryRunResponse` 必须包含：

| 字段 | 规则 |
|---|---|
| `status` | 全部 route 成功为 `ready_for_review`，存在失败为 `repair_required` |
| `routeResults` | D17 route adapter dry-run 输出 |
| `gateEvidenceRefs` | 验收证据引用，不写 Harness |
| `requiredHumanReview` | 必须为 `true` |
| `requiredHarnessEvidence` | 必须为 `true` |
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
| ready-for-review packet | 全部 route 成功，状态为 `ready_for_review` |
| repair-required packet | 至少一个 route 失败，状态为 `repair_required` |
| evidence refs | fixture、validator、contract doc、LOOP evidence 均存在 |
| human review | 必须保留人工 review 要求 |
| Harness evidence | 必须保留后续 Harness evidence 要求，但本轮不写入 |

## 6. 边界

D18 允许：

- 临时编译到 `/tmp`。
- 本地调用 `createAcceptancePacketDryRun`。
- 读取本地 fixture、validator、文档和 LOOP evidence。
- 聚合 route adapter 输出。

D18 不允许：

- 启动 HTTP server。
- 连接数据库。
- 执行 migration。
- 调用外部 API。
- 写 KDS 正式对象。
- 写 GFIS / GPC / ERP / MES 等业务系统。
- 写 Harness evidence store。
- 写 accepted / published / written_back。

## 7. 校验命令

```bash
python3 scripts/api/validate_gckf_p0_acceptance_packet_dry_run.py
```

通过条件：

- 2 个 acceptance packet case 全部通过。
- ready-for-review 与 repair-required 两种状态均被覆盖。
- evidence refs 全部存在。
- 所有 packet 与 route result 均保留 no-write、no-server、no-db、no-external-api 标志。

## 8. 下一步

P0-D19 建议进入 acceptance packet ledger dry-run：

- 生成验收包台账候选记录。
- 汇总 D9-D18 的 validator 输出索引。
- 继续不写真实 Harness evidence、不升级 accepted。
