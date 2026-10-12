---
doc_id: GPCF-DOC-XAP-RECEIPT-EXECUTION-REPORT-DRAFT-20261011
title: XAP 回执与执行报告规格草案 v0.1（含错误码与幂等规则）
project: GPCF
related_projects: [GPCF, PVAOS, WAME, MMC]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/XAP回执与执行报告规格草案_v0.1.md
source_path: 01-architecture/XAP回执与执行报告规格草案_v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# XAP 回执与执行报告规格草案 v0.1（含错误码与幂等规则）

- 日期：2026-10-11 ｜ 性质：**提交侧规格草案**（P0 契约收口主项）；正式 Schema 维护归 XWAIL（GCXWAIL 流程）
- 依据：《XAP统一治理交换协议_Codex提案采纳意见_v0.1》§一/§二；《WAME统一审核请求机制_v0.1》§三
- 定位：把提案中「Receipt／Execution Report／错误／幂等」四项从**概念**落为**字段级规格**——离线导入与在线提交**同规**（服务端同一校验与授权）

## 一、Receipt（治理回执）规格

**签发方**：WAME 服务端及相应授权主体（**唯一权威裁定载体**）。

### 1.1 字段（最小集）

| 字段 | 必填 | 说明 |
|---|---|---|
| `receiptId` | ✓ | 回执唯一标识 |
| `requestId` / `correlationId` | ✓ | 关联请求与修订链 |
| `packageRef` | ✓ | `{packageId, version, contentDigest}`——绑定请求与摘要 |
| `decision` | ✓ | **治理方实际裁定**（枚举见 1.2）——**唯一权威** |
| `authorizationScope` | 条件 | 授权类回执必填：范围／权限／**有效期** |
| `decidedAt` | ✓ | 裁定时间 |
| `authority` | ✓ | 裁定人 ＋ 角色（经 MMC 可信身份核对） |
| `refs[]` | ○ | 证据引用（补证指引等） |
| `signature` | ○ | 签名位（P2 启用；预留） |

### 1.2 `decision` 枚举（回执专用）

```text
rejected              拒收/拒绝（附理由）
returned_for_evidence 待补证（可重提；关联 correlationId）
accepted              受理（进入审核/治理流程——不等于批准）
granted               批准/授权（附 authorizationScope 与有效期）
revoked               撤销/失效（对既有授权）
```

**与既有字段的消歧**（Codex 三义分离）：
- `requestedDecision`＝提交方**希望**的裁定（请求包内）；
- `compatibilityDecision`＝版本兼容性判断（XAP-1003：compatible/migration_required/deprecated/blocked）；
- 回执 `decision`＝**治理方实际裁定**（本规格）。
- 既有 manifest `decision` 字段的歧义消除＝**版本化迁移**（归 XWAIL）；提交侧在回执/请求包中已按三义分列。

## 二、Execution Report（执行报告）规格

**签发方**：PVAOS／AaaS 或其他实际执行系统。

### 2.1 字段（最小集）

| 字段 | 必填 | 说明 |
|---|---|---|
| `reportId` | ✓ | 报告唯一标识 |
| `packageRef` | ✓ | 同回执——关联到具体发布件 |
| `requestId` | ○ | 如由请求驱动 |
| `executor` | ✓ | 执行系统（pvaos / aaas / …） |
| `action` | ✓ | `import / activate / execute / rollback` |
| `outcome` | ✓ | `succeeded / failed / rolled_back / partial` |
| `facts{}` | ✓ | 结果事实（对象数/关系数/回退点等） |
| `evidenceRefs[]` | ○ | 运行证据引用 |
| `executedAt` | ✓ | 执行时间 |
| `signature` | ○ | 签名位（预留） |

## 三、错误码（请求处理族 · 建议 XAP-6xxx）

| 码 | 语义 | 可否重试 |
|---|---|---|
| `XAP-6001` | **幂等冲突**（同键不同内容） | 否（须新修订） |
| `XAP-6002` | 提交身份与声明不符（`from`≠认证身份） | 否（先修正身份） |
| `XAP-6003` | 请求类型不适用该处理器 | 否 |
| `XAP-6004` | 证据不可访问（→ 待补证或阻断） | 是（补证后） |
| `XAP-6005` | 协议版本不支持 | 否（升级协议） |
| `XAP-6006` | 必填/格式错误（引用 R03/R07 族） | 是（修正后） |

> 编号为提交侧建议；正式分配与纳入 = XWAIL（GCXWAIL 流程，与既有 22 码清单一并维护）。

## 四、幂等规则（四约束）

1. **包版本与协议版本分离**：业务包升级 ≠ 协议升级。
2. **同一包版本内容不可静默替换**：补证/修改产生**新修订**，关联旧请求（correlationId）。
3. **幂等键**＝`packageId + version + contentDigest`（或显式 `idempotencyKey`）：同键同内容 → **返回原处理结果**（不重复建单）；同键不同内容 → **拒绝（XAP-6001）**。
4. **`from`/角色/租户只是声明**：权限由可信身份（MMC）与授权记录确认——声明非权限。

## 五、状态线（三线分离）

| 状态线 | 状态序列 | 保管方 |
|---|---|---|
| **请求处理** | 已接收 → 校验中 → 待补证／待审核 → 已裁定 → 已归档 | WAME |
| **资产治理** | Draft → Registered → Authorized → Published → Deprecated／Archived | WAME（模型 lifecycle 枚举既有） |
| **运行执行** | 未导入 → 已导入 → 待激活 → 运行中／失败／已回滚 | PVAOS／AaaS |

## 六、四句铁律

> **收到请求 ≠ 批准；批准 ≠ 发布；发布 ≠ 执行成功；执行成功须报告对账方成运行事实。**

## 七、与既有件的关系

- 流程位置＝《WAME统一审核请求机制》§三 受理流程的「治理裁定 → 回执回写」环节细化的**载体规格**；
- 检查链：请求包自检 `requestcheck.py` v2（R01-R08）↔ 本规格（回执/报告为**受理侧产出**，提交侧只消费）；
- `wameEvidenceRef`（XAP-5001）＝发布态证据引用；本规格回执为其**签发源头**。

## 八、边界与不声明

- 本件为**提交侧规格草案**；不改 WAME/PVAOS/GCXWAIL；正式 Schema／错误码分配归相应流程；
- 不声明任何回执/报告已可签发（受理器未实现，S4/P1）；签名（signature）位仅在 P2 启用。
