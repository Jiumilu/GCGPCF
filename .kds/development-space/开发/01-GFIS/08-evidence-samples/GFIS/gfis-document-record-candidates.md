---
doc_id: GPCF-DOC-192890AD56
title: GFIS 单据与记录候选清单
project: GFIS
related_projects: [GFIS, GPC, WAES, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/gfis-document-record-candidates.md
source_path: 08-evidence-samples/GFIS/gfis-document-record-candidates.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS 单据与记录候选清单

Round ID：`GPCF-GF-LR-001`

## 单据与记录

| 阶段 | 单据/记录 | GFIS 用途 | 必填字段候选 | 验证方式 |
|---|---|---|---|---|
| 来料 | 来料检验单 | 原料入厂质量事实 | 批次、供应商、规格、检验项、结果 | 抽样检验记录 |
| 配料 | 配料批次记录 | 投料追溯 | 工单、配方版本、原料批次、重量、操作人 | 称重记录、复核 |
| 生产 | 生产日报 | 工单执行事实 | 工单、班组、产量、损耗、异常 | 班组日报 |
| 首件 | 首件确认单 | 量产前门禁 | 尺寸、外观、承重、确认人、结论 | 质检确认 |
| 过程 | 巡检记录 | 过程质量监控 | 时间、工序、指标、偏差、处理 | 巡检签名 |
| 成品 | 成品检验单 | 入库前质量事实 | 批次、检验项、结果、隔离状态 | FQC |
| 入库 | 入库单 | 成品库存增加 | 批次、数量、库位、追溯码 | 仓库复核 |
| 出库 | 出库单 | 发货出库事实 | 批次、数量、目的地、复核人 | 出库复核 |
| 设备 | 点检表 | 设备健康事实 | 设备、点检项、状态、异常 | 点检记录 |
| 维修 | 维修单 | 故障闭环 | 设备、故障、备件、处理、停机时间 | 维修验收 |
| 追溯 | 一物一码绑定记录 | 批次追溯 | 码值、工单、批次、库位、状态 | 扫码记录 |

## 记录分级

| 等级 | 含义 | 示例 |
|---|---|---|
| P0 | 没有记录不得进入下一阶段 | 首件确认、成品检验、入库单 |
| P1 | 缺失会影响追溯或成本核算 | 配料批次、生产日报、出库复核 |
| P2 | 缺失影响分析但不阻断主链 | 设备点检、维修详情 |

## 首轮结论

GFIS 首批开发应优先支持 P0/P1 记录，P2 可作为二期增强。
