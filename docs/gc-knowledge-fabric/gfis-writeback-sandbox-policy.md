---
doc_id: GPCF-DOC-40772C7D57
title: GC-Knowledge Fabric GFIS Writeback Sandbox 契约
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-writeback-sandbox-policy.md
source_path: docs/gc-knowledge-fabric/gfis-writeback-sandbox-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric GFIS Writeback Sandbox 契约

## 1. 定位

本文件定义 GFIS 写回候选的沙箱契约，用于把 AI 候选事实、WAES Writeback Gate、业务负责人确认和 GFIS/GPC/ERP/MES 正式写回之间的边界拆清。

本文件只定义候选写回的字段级 diff、模式和 no-write/sandbox/approved-write 边界，不执行真实 GFIS/GPC/ERP/MES 写回。

## 2. 写回模式

| 模式 | 含义 | P0/P1 是否允许 |
|---|---|---|
| `no_write` | 只生成候选和检查结果，不写任何目标系统 | 允许 |
| `sandbox` | 写入隔离沙箱或本地 fixture，用于 diff 与验收演练 | 允许 |
| `approved_write` | 通过 WAES、KWE、业务负责人和 Harness 后的受控正式写回 | P1 前禁止 |
| `production_write` | 生产主账写入 | P1 前禁止，后续也必须专项授权 |

## 3. 最小字段

每个 GFIS Writeback Sandbox record 至少包含：

- `candidateId`
- `sourceFactId`
- `targetSystem`
- `targetModule`
- `targetField`
- `currentValue`
- `proposedValue`
- `diffReason`
- `evidenceRefs`
- `waesResult`
- `businessOwner`
- `confirmationStatus`
- `writebackMode`
- `finalAction`
- `noWrite`

## 4. 硬边界

1. `no_write` 和 `sandbox` 不能产生真实目标系统写入回执。
2. `approved_write` 必须要求 WAES Writeback Gate passed、业务负责人确认、confirmation record、Harness evidence。
3. `production_write` 必须额外要求专项授权、回滚计划、目标系统 receipt 和审计记录。
4. AI/Agent 只能创建 `no_write` 或 `sandbox` 候选，不能创建 `approved_write` 或 `production_write`。
5. 没有 evidence refs、WAES result 或 business owner 的记录必须 blocked。
6. `finalAction=accepted` 不等于 GFIS 主账已写入；只有目标系统 receipt 与 Harness evidence 同时存在才可证明写回完成。

## 5. P0/P1 验收条件

- OKF 中有独立 GFIS Writeback Sandbox policy。
- Shared Types 中有模式、最终动作、字段级 diff 和 hard boundary 类型。
- Validator 能检查最小字段、模式边界、AI 限制、approved/production 前置条件和 no-write 断言。
- 所有验证只使用本地文件和 fixture，不触达真实 GFIS/GPC/ERP/MES 或外部 API。
