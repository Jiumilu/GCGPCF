---
doc_id: GPCF-DOC-2AD93D9881
title: GFIS 岗位到能力映射表
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/gfis-role-map.md
source_path: 08-evidence-samples/GFIS/gfis-role-map.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GFIS 岗位到能力映射表

来源：`现代精工工厂岗位培训学习资料_优化版.pdf`

Round ID：`GPCF-GF-LR-001`

## 岗位映射

| 岗位/模块 | GFIS 主责能力 | 关键记录 | 协同项目 | 边界说明 |
|---|---|---|---|---|
| 配混料班组 | 原料批次、配方投料、留样、投料核对 | 原料批次记录、配料单、留样记录 | KDS、WAES | 工艺知识进入 KDS；异常配料进入 WAES |
| 挤出生产班组 | 工单执行、产线参数、首件确认、过程巡检 | 工单、生产日报、首件确认、巡检记录 | WAES、Brain | 质量异常由 WAES 门控；分析展示可进入 Brain |
| 印刷/覆膜班组 | 工序流转、工艺参数、外观检验 | 工序流转单、外观检验记录 | GPC、WAES | 客户定制需求来自 GPC；质量放行由 WAES 约束 |
| 模切/成箱班组 | 箱型、模具、承重/尺寸检验 | 模具记录、尺寸检验、承重检验 | KDS、WAES | 模具和工艺标准沉淀到 KDS |
| 包装入库班组 | 一物一码、成品入库、库位、出库复核 | 入库单、库位记录、出库复核单 | GPC、WAES | 客户交付协同归 GPC；库存事实归 GFIS |
| 维修保障班组 | 设备点检、故障、备件、维修闭环 | 点检表、维修单、备件消耗 | WAES、KDS | 安全停机和重大故障进入 WAES |
| 品质管理 | IQC、IPQC、FQC、质量隔离、放行建议 | 来料检验、过程检验、成品检验、不合格处理 | WAES | GFIS 记录事实，WAES 形成放行门禁 |
| 仓储物流 | 库存分区、拣货复核、发货出库 | 库存台账、拣货单、出库单 | GPC | POD、客户签收和运输协同归 GPC |
| 商务销售岗 | 生产约束输入接收 | 订单约束、交期约束 | GPC | 报价、合同、回款、客户投诉主责归 GPC |
| 财务经营分析岗 | 生产成本事实提供 | 工时、材料损耗、能耗、产量 | GPC、KDS | 经营分析不是 GFIS 主责，GFIS 提供事实数据 |
| 信息化与数据 | MES/WMS 事实采集、追溯、工厂看板输入 | 追溯码、数据采集记录、异常日志 | KDS、Brain、WAES | 知识主存归 KDS；智能分析归 Brain；治理归 WAES |

## 首轮结论

GFIS 一期应以“工单、配料、生产、检验、入库、出库”作为最小主链，不把商务、财务、客户交付、治理审批纳入 GFIS 主责。
