---
doc_id: GPCF-DOC-D891BBBCA4
title: GFIS 与 GPC 边界说明
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/gfis-gpc-boundary-notes.md
source_path: 08-evidence-samples/GFIS/gfis-gpc-boundary-notes.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GFIS 与 GPC 边界说明

Round ID：`GPCF-GF-LR-001`

## 主责边界

| 事项 | GFIS | GPC | 说明 |
|---|---|---|---|
| 客户需求 | 接收生产约束 | 主责 | GFIS 不管理客户协同全流程 |
| 报价/合同 | 不主责 | 主责 | GFIS 只接收产品、数量、交期和特殊工艺要求 |
| 工单 | 主责 | 触发来源 | 平台订单转为工厂工单后由 GFIS 执行 |
| 生产报工 | 主责 | 读取状态 | GPC 可读取进度，不写工厂事实 |
| 质量事实 | 主责记录 | 读取影响交付 | 放行门禁由 WAES 约束 |
| 入库/出库 | 主责工厂库存事实 | 读取交付状态 | 客户签收/POD 归 GPC |
| 物流异常 | 记录工厂出库事实 | 主责客户交付协同 | 出厂后异常主要归 GPC |
| 回款/投诉 | 不主责 | 主责 | GFIS 可提供追溯和质量事实 |

## 接口候选

| 接口 | 方向 | 最小数据 | 目的 |
|---|---|---|---|
| 生产需求下发 | GPC -> GFIS | 需求号、产品、数量、交期、工艺约束 | 生成工单 |
| 生产进度回写 | GFIS -> GPC | 工单状态、产量、预计完成 | 客户协同 |
| 质量状态回写 | GFIS -> GPC/WAES | 批次、检验状态、隔离状态 | 交付判断和治理门禁 |
| 出库事实回写 | GFIS -> GPC | 出库单、批次、数量、时间 | 物流和签收协同 |
| 异常升级 | GFIS -> WAES | 异常类型、证据、影响范围 | 审批、阻断、审计 |
| 工艺知识沉淀 | GFIS -> KDS | 配方、工艺参数、质量经验 | 知识主存 |

## 首轮结论

GFIS 最小闭环必须聚焦工厂执行事实主账。凡涉及客户协同、合同、报价、POD、回款的内容，应进入 GPC 主线。
