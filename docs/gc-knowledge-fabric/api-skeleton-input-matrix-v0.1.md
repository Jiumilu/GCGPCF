---
doc_id: GPCF-DOC-D2F7AF0B4D
title: GC-Knowledge Fabric API 骨架输入矩阵 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/api-skeleton-input-matrix-v0.1.md
source_path: docs/gc-knowledge-fabric/api-skeleton-input-matrix-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric API 骨架输入矩阵 v0.1

## 1. 定位

本文是 P0-D7 的 API 骨架输入矩阵，不是接口实现完成声明。

它把 P0-D2 至 P0-D6 的编号、挂池、WAES、KWE、KDS 状态候选 dry-run 统一映射到首批 API 端点，形成后续工程拆解的最小 contract 输入。

## 2. 总边界

P0 API 骨架只允许三类输出：

- `read_only`：只读查询、聚合、检索。
- `candidate_only`：创建候选输入，不形成正式事实。
- `request_only`：创建审核、门禁、流程或证据请求，不直接写 accepted / published / written_back。

P0 API 骨架禁止：

- 直接写入正式业务事实。
- 直接写入 GFIS / GPC / ERP / MES。
- 直接写入 `accepted`、`published`、`written_back`。
- 直接确认积分、收益、额度或悬赏结算。
- 直接生成委员会裁决。
- 绕过 WAES、KWE、Harness evidence。

## 3. 端点分组

| 分组 | 端点数 | 允许输出 | 关键边界 |
|---|---:|---|---|
| KDS v2 | 11 | read_only / candidate_only | source、fact、SOP、writeback 只能入 candidate |
| WAES | 7 | gate_check / freeze_request | 只返回门禁结果候选，不写业务系统 |
| KWE | 10 | read_only / request_only | 只创建流程请求，不完成最终确认 |
| GFIS Assistant | 4 | assistant_query / document_check / writeback_candidate | 可建议，不可正式写回 |
| Governance LOOP | 8 | read_only / evidence_request / knowledge_ci_dry_run | 可登记请求，不可升级状态 |

合计首批端点：40 个。

## 4. API 到 P0 evidence 的引用

| API 分组 | 输入 fixture | 依赖 P0 evidence |
|---|---|---|
| KDS v2 | `fixtures/kds/v2-endpoint-no-write-smoke.json` | P0-D2、P0-D3、P0-D6 |
| WAES | `fixtures/waes/endpoint-no-write-smoke.json` | P0-D4 |
| KWE | `fixtures/kwe/endpoint-no-write-smoke.json` | P0-D5 |
| GFIS Assistant | `fixtures/gfis/endpoint-no-write-smoke.json` | P0-D4、P0-D5、P0-D6 |
| Governance LOOP | `fixtures/governance/endpoint-no-write-smoke.json` | P0-D1 至 P0-D6 |
| 汇总矩阵 | `fixtures/api/gckf-p0-api-skeleton-input-matrix-v0.1.json` | P0-D7 |

## 5. 最小验收规则

P0-D7 通过条件：

- 5 个分组均有 endpoint fixture。
- 首批端点总数为 40。
- 所有端点均为 `read_only`、`candidate_only`、`request_only` 或门禁 dry-run。
- 所有正式写入计数为 0。
- 所有 GFIS 写回路径必须保持 `writeback_candidate`。
- 所有收益、积分、额度、悬赏相关路径必须保持 review / ledger read / candidate 状态。
- LOOP API 不得把状态自动升为完成。

## 6. 下一步工程拆解

P0-D8 建议进入 Shared Types 与 API contract 对齐：

- 对齐 `packages/shared/src/knowledge/*` 的核心对象类型。
- 对齐 `packages/api/src/*/contracts.ts` 的请求与响应模型。
- 将 D7 矩阵转为最小 validator。
- 继续保持无真实外部 API 写入、无生产写入、无 accepted / integrated 升级。
