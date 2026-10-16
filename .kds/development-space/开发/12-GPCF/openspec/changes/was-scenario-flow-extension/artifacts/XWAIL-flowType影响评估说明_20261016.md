---
doc_id: GPCF-DOC-2FF258337C
title: XWAIL `flowType` 影响评估说明（场景流扩展·候选）
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/was-scenario-flow-extension/artifacts/XWAIL-flowType影响评估说明_20261016.md
source_path: openspec/changes/was-scenario-flow-extension/artifacts/XWAIL-flowType影响评估说明_20261016.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# XWAIL `flowType` 影响评估说明（场景流扩展·候选）

> 状态：draft（评估件）｜2026-10-16｜范围：场景流候选扩展对 XWAIL 契约的潜在影响——**本件只评估、不代改**。

## 1. 现状事实（源码级定位）

- `GlobalCloud XWAIL/scripts/xwail_common.py`：
  - L22：`ALLOWED_FLOWS` 为**封闭集合**，现含 V1.2 新名八流（`LogisticsFlow / InformationFlow / FinancialFlow / EnergyFlow / ServiceFlow / ControlFlow / ValueFlow / CreditFlow`）；
  - L221–222：`flowRelations[].flowType` 校验——不在 `ALLOWED_FLOWS` 即报 `XWAIL-9001（high）`，消息文案 `"flowType must be one of the WAS eight flows"`。
- GPCF《XWAIL 可扩展世界资产信息建模语言规范 V1.2 草案》：`flowType ∈ 八流`（权威指向 WAS `okf/was/was-flows.yaml`）。
- WAS `okf/was/was-flows.yaml`：现状为 **OKF P0 旧命名 8 条**（`material_flow / information_flow / capital_flow / spacetime_flow / energy_flow / commerce_flow / knowledge_flow / rule_flow`）；其 V1.2 命名迁移为**独立在案专项**（八流迁移表待交付物）。

## 2. 若场景流正式纳入，XWAIL 侧需联动的事项（建议·待 XWAIL 侧执行）

1. `ALLOWED_FLOWS`：增补 `ScenarioFlow`；校验文案从写死数字调整为 `"one of the WAS flows"`（避免数字随扩展失真）。
2. 正负样例：补一条含 `ScenarioFlow` 的正例与一条非法值负例（沿用 `models/examples/` 与 schema 回归惯例）。
3. GPCF XWAIL 规范草案：`flowType ∈ 八流` 表述与版本注记更新（与 WAS 侧发布同步）。
4. 评审通道：按 XWAIL 议题机制走（先例：议题文档 v0.10 批次）。
5. 依赖项：与 `was-flows.yaml` 的 V1.2 迁移专项**同期或先后**执行（避免旧/新命名与扩展三者叠加）。

## 3. 边界

- 本件仅为评估与建议；**不得**据此直接修改 XWAIL 仓、`was-flows.yaml`、registry 或任何校验器。
- 正式执行随场景流版本发布纳入（U16 路径），由 XWAIL/WAS 各自流程承载；状态保持 candidate。
