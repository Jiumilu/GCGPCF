---
doc_id: GPCF-DOC-F4E22D8C24
title: F-032 方向裁定（2026-10-24）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/f032-direction-ruling-20261024.md
source_path: docs/reports/f032-direction-ruling-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-032 方向裁定（2026-10-24）

- 裁定人：老卢（问答，决策模型辅助）｜时间：2026-10-24 07:40
- 背景：另一会话在 1 天多内把 F-032 重定义为「PQC 对外询价服务（经 PVA PVAAI 承载）+ 合成数据分阶段试点，不声明生产就绪」；而 `AUTH-PG-PQC-REAL-PILOT-20261022` 批的是**真实客户一单 A1–A4**

## 1. 裁定结论

| 议题 | 决策模型 | 裁定 |
|---|---|---|
| F-032 方向 | 保留真实优先 **96.0%** / 先合成后真实 2.1% / 以新 scope 为准 1.9% | **真实客户 A1–A4 仍为主线**；新 scope 的合成数据试点仅作**前置工程验证**，其结果**不得**计入 `C_real`、不得据此声明生产就绪 |

## 2. 落地规则

1. **允许**：按新 scope 完成设计评审、契约冻结（PQC↔PVA）、合成数据分阶段试点、回滚路径验证——这些是工程成熟度证据；
2. **禁止**：用合成/联调测试客户数据推进任何 VU 到 S4（`gpcf_promote_vu_stage.py` 已强制校验 `data_class: real`）；
3. **C_real 破 0 的唯一路径**：真实客户一单（`AUTH-PG-PQC-REAL-PILOT-20261022` A1–A4）→ 真实回执 → S4；
4. 两条路线可并行，但**证据分账**：合成试点证据入 F-032 常规 evidence（标注 synthetic/fixture），真实试点证据单独命名 `pilot-receipt-*.json`。

## 3. 对队列的影响

- F-032 当前 `queued`（dispatched=false），evidence 全 pending：**不改变其 blocked/evaluated 判定**，也不产生 `C_real`；
- 真实试点启动条件不变：PQC 属主报客户候选单 → 老卢确认 → 执行手册 S1–S7。

## 4. 非声明

本裁定不构成任何状态提升；不声明 accepted/integrated/production_ready/customer_accepted。
