---
doc_id: GPCF-DOC-PG12-CONTRACT-ADJUDICATION-PACK-20261022
title: PG-12 契约冲突裁决包（2026-10-22）
project: GPCF
related_projects: [GPCF, XWAIL, WAME, AAAS, XiaoC, KDS, Brain]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pg12-contract-adjudication-pack-20261022.md
source_path: docs/harness/evidence/pg12-contract-adjudication-pack-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PG-12 契约冲突裁决包（2026-10-22）

> 依据：`09-status/globalcloud-cross-project-contract-matrix-v1.0.md`、`runtime/contract-matrix.yaml`。
> 性质：**裁决选项包**，只准备选项、影响与建议，不代替老卢裁决；不修改任何契约文件。
> 非声明：不声明契约已统一、已冻结、已集成。

## 1. CONFLICT-01：contentDigest 四种口径

| 口径 | 来源 | 现状 |
|---|---|---|
| 请求包摘要 | XAP 回执规格 `packageRef.contentDigest` | 进幂等键 |
| `sha256(contents)` | WAME 实现 | 不符即 XAP-2004 |
| `totalSha256` | XWAIL `xap_sign` | 逐文件 sha256 汇总 |
| AaaS 包体 SHA-256 | XiaoC 正式提案 | 绑定 ServicePackage，禁用 PoC 信封 digest |

### 选项

| 选项 | 做法 | 优点 | 代价/风险 |
|---|---|---|---|
| **A（建议）** | 定义 digest **命名空间**：`request-envelope-digest` / `service-package-digest` / `file-manifest-digest`；字段名带作用域，禁止跨作用域复用 | 语义清晰；兼容既有实现；一次裁决长期稳定 | 需改 XAP 回执规格与 WAME/XWAIL schema 字段名 |
| B | 统一为**单一 canonical digest**（如对规范化 JSON 取 sha256） | 最简单 | 需重写 WAME/XWAIL/AaaS 三处实现；历史 PoC 证据需重算 |
| C | 保持四种口径，增加**适配层映射表** | 改动最小 | 幂等键仍可能冲突；适配层成为新单点 |

**建议 A**，理由：四种口径服务不同对象（信封/包体/文件清单），强行统一会破坏既有签名与幂等语义；命名空间化可在不重算历史证据的前提下收敛。

### 影响与回滚

- 影响：XAP 回执规格、WAME 受理、XWAIL 签名、AaaS 包体校验、F-033 PoC 证据。
- 回滚：保留旧字段名作为 deprecated 别名一个版本；不回滚已生成证据。

## 2. CONFLICT-07：`decision` 同名双枚举

| 场景 | 当前枚举 |
|---|---|
| Manifest `decision` | compatibility：compatible / migration_required / deprecated / blocked |
| 回执 `decision` | governance：rejected / returned_for_evidence / accepted / granted / revoked |

### 选项

| 选项 | 做法 | 优点 | 代价/风险 |
|---|---|---|---|
| **A（建议）** | 按规格三义分列：`manifest.compatibilityDecision`、回执 `decision`、请求包 `requestedDecision`；配负例 | 语义唯一；与既有规格草案一致 | 需改 manifest/回执 schema 与消费者读取逻辑 |
| B | 保留 `decision`，按 **context 字段** 区分枚举 | 改动小 | 同名歧义仍在，跨团队误读风险高 |
| C | 全部重命名为不同字段（如 `manifestDecision` / `receiptDecision`） | 清晰 | 破坏既有消费者兼容，需双写过渡 |

**建议 A**，理由：规格已承认歧义并给出三义分列方向；A 是兼容性最好的收敛路径，B 只是把歧义藏进 context。

### 影响与回滚

- 影响：XAP manifest schema、回执 schema、WAME 受理/裁定、消费者（F-033 PoC、PKC/XGD 工具范围）。
- 回滚：保留 `decision` 作为 manifest 的 deprecated 别名一版；新增字段双读过渡。

## 3. P1/P2 冲突（本轮不裁决，登记）

| 冲突 | 主题 | 建议 |
|---|---|---|
| CONFLICT-02 | XAP 错误码 3 处清单不一致 | 建错误码注册表（码/语义/版本/是否可重试） |
| CONFLICT-05 | 签名/无签名边界 | Manifest Schema 显式 signature/digest；PoC 标 no_signature |
| CONFLICT-04 | 版本语义 4 处不符 | 契约版本 semver + 内容哈希双标识 |
| CONFLICT-03/06/08 | casing / 幂等键粒度 / WAES→WAME 命名 | 消费者接入规则与迁移表 |

## 4. 裁决记录（2026-10-22，已确认）

| conflict_id | 裁决 | 裁决人 | 时间 | 说明 |
|---|---|---|---|---|
| `CONFLICT-01` | **A：digest 命名空间化** | 老卢 | 2026-10-22 | request-envelope / service-package / file-manifest 三作用域；字段名带作用域，禁止跨作用域复用 |
| `CONFLICT-07` | **A：三义分列** | 老卢 | 2026-10-22 | manifest.compatibilityDecision / 回执.decision / 请求包.requestedDecision |

后续实施任务（跨仓，需属主执行）：
1. XWAIL：更新 `xap-manifest.schema.json`（compatibilityDecision、signature/digest 可选字段、命名空间字段）。
2. WAME：受理与回执按新字段名双读过渡；错误码注册表随 CONFLICT-02 处理。
3. AaaS/XiaoC：ServicePackage digest 字段对齐 service-package 命名空间。
4. 负例：manifest/回执/请求包三处 decision 误用各 1 条。

## 5. 非声明

- 不声明任何冲突已裁决；
- 不声明契约已统一或已冻结；
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
