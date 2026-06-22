---
doc_id: GPCF-DOC-587CC64DA1
title: GFIS 业务对象候选清单
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/gfis-business-object-candidates.md
source_path: 08-evidence-samples/GFIS/gfis-business-object-candidates.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS 业务对象候选清单

Round ID：`GPCF-GF-LR-001`

## 核心对象

| 对象 | 主责项目 | 用途 | 最小字段候选 | 边界 |
|---|---|---|---|---|
| 生产需求 | GPC/GFIS | 将平台订单转为工厂可执行需求 | 需求编号、产品、数量、交期、客户约束、优先级 | 平台订单主账归 GPC |
| 工单 | GFIS | 生产执行主控对象 | 工单号、产品、数量、产线、计划开始/结束、状态 | 不承诺客户交期 |
| 原料批次 | GFIS | 原料追溯 | 批次号、供应商、规格、入厂日期、检验状态 | 供应商协同归 GPC |
| 配方 | KDS/GFIS | 工艺投料约束 | 配方编号、版本、材料比例、适用产品 | 知识版本归 KDS |
| 配料批次 | GFIS | 投料执行事实 | 配料批次、原料批次、重量、操作人、时间 | 异常进入 WAES |
| 产线 | GFIS | 生产资源 | 产线编号、设备组、班组、状态 | 设备安全门禁归 WAES |
| 设备 | GFIS | 点检与维修 | 设备编号、类型、状态、点检周期 | 重大安全事件归 WAES |
| 首件确认 | GFIS/WAES | 量产前确认 | 工单、样件、尺寸、外观、确认人、结果 | 放行门禁归 WAES |
| 巡检记录 | GFIS | 过程质量事实 | 时间、工序、指标、结果、异常 | 异常闭环归 WAES |
| 成品检验 | GFIS/WAES | 入库前质量事实 | 批次、尺寸、承重、外观、结果 | 放行决策归 WAES |
| 库存事务 | GFIS | 入库、移库、出库事实 | 单号、物料、数量、库位、事务类型 | 客户签收归 GPC |
| 追溯码 | GFIS/KDS | 批次级追溯 | 码值、工单、批次、库位、状态 | 知识化归 KDS/Brain |

## 不纳入 GFIS 主责的对象

| 对象 | 主责项目 | 原因 |
|---|---|---|
| 报价 | GPC | 属于客户协同和商业交易 |
| 合同 | GPC | 属于平台订单和交易主账 |
| 回款 | GPC/财务域 | 属于经营与财务闭环 |
| 客户签收/POD | GPC | 属于客户交付协同 |
| 治理审批 | WAES | 属于状态门控和审计主账 |

## 首轮结论

GFIS 对象模型必须围绕工厂事实，不得扩张为平台交易系统。
