---
doc_id: GPCF-DOC-CONTRACTS-REMAINING-PACK-20261022
title: 剩余契约冲突裁决包（2026-10-22）
project: GPCF
related_projects: [GPCF, XWAIL, WAME, KDS, XiaoC, GFIS, GPC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/contracts-remaining-adjudication-pack-20261022.md
source_path: docs/harness/evidence/contracts-remaining-adjudication-pack-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 剩余契约冲突裁决包（2026-10-22）

> 范围：CONFLICT-03 / 04 / 05 / 06 / 08（01/02/07 已 closed）。
> 性质：选项与建议，不代替老卢裁决；未修改任何契约文件。

## 1. CONFLICT-03 字段命名与 casing

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | 线上契约 camelCase、存储 snake_case、转换点唯一；转换点写入消费者接入清单 | 语义稳定；兼容三套现状 | 需登记转换点 |
| B | 全部 snake_case | 统一 | 破坏 XAP 既有 camelCase 消费者 |
| C | 全部 camelCase | 统一 | 破坏知识资产/KDS 既有 snake_case |

**建议 A**。

## 2. CONFLICT-04 版本语义

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | 契约版本 semver + 内容哈希双标识；内容变则哈希变，破坏性变更升主版本 | 可判定、可缓存、可回放 | 需三套契约补哈希 |
| B | 仅 semver | 简单 | 同版本多哈希问题仍在 |
| C | 仅内容哈希 | 内容可追溯 | 无法表达兼容性 |

**建议 A**。

## 3. CONFLICT-05 签名与无签名边界

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | manifest 显式 `signature`/`digest`（可选但可判）；正式治理要求签名，PoC 标 `no_signature` 且不作为治理证据 | 强度可区分 | 需改 schema 与台账 |
| B | 全部可选 | 改动最小 | 证据强度混淆 |
| C | 强制签名（PoC 走例外登记） | 最严 | PoC 与历史证据需重跑 |

**建议 A**。

## 4. CONFLICT-06 幂等键构成

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | 三段映射：业务动作幂等键 → 事件 `idempotencyKey` → XAP 包幂等键；事件信封加 `packageRef` | 跨链路可对账 | 需改事件信封与两端实现 |
| B | 以 XAP 包幂等键为准 | 改动小 | 事件链路仍可能重复 |
| C | 两条链路各自独立 | 零改动 | 补偿规则失效 |

**建议 A**。

## 5. CONFLICT-08 WAES → WAME 命名漂移

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | 统一 WAME 命名，保留 WAES legacy 映射一版（文档 + 连接器别名） | 收敛且可过渡 | 需改连接器编号/域名 |
| B | 保留 WAES | 零改动 | 与 WAME 合并口径冲突 |
| C | 双写 | 兼容 | 长期双份维护 |

**建议 A**。

## 6. 裁决记录（2026-10-22，已确认）

| conflict_id | 裁决 | 说明 |
|---|---|---|
| CONFLICT-03 | A | 线上 camelCase / 存储 snake_case / 转换点唯一 |
| CONFLICT-04 | A | semver + 内容哈希双标识 |
| CONFLICT-05 | A | manifest 显式 signature/digest；正式要求签名，PoC 标 no_signature |
| CONFLICT-06 | A | 业务动作→事件 idempotencyKey→XAP 包幂等键三段映射 |
| CONFLICT-08 | A | 统一 WAME 命名，保留 WAES legacy 映射一版 |

实施属主与回滚待各仓落仓时登记。

## 7. 原模板

```text
conflict_id:
裁决选项: A / B / C
裁决人: 老卢
裁决时间:
实施属主:
回滚:
```

## 7. 非声明

- 不声明任何冲突已裁决；
- 不声明契约统一/冻结；
- 不声明任何项目状态提升。
