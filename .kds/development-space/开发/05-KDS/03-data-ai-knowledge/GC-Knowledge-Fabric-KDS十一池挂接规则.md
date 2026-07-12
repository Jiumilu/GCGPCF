---
doc_id: GPCF-DOC-60E4A89F37
title: GC-Knowledge Fabric KDS十一池挂接规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-KDS十一池挂接规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-KDS十一池挂接规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric KDS十一池挂接规则

## 1. 定位

KDS 十一池用于把知识对象挂接到绿色供应链底座。Domain 解决治理归属，Pool 解决资源事实或场景规则归属。一个对象可以有一个或多个 `poolRefs`；涉及24字产业节点时可增加 `industryNodeRefs`。

分层边界固定为：前十池是资源事实层，第十一池场景池是规则编排层。场景池不得单独证明合同、金额、产能、交付、回款或收益。

## 2. 十一池定义

| 池 | 代码 | 主要对象 |
|---|---|---|
| 订单池 | order_pool | 订单、客户需求、合同执行、交付计划 |
| 运力池 | logistics_pool | 发货、运输、POD、承运资料 |
| 产能池 | capacity_pool | 工厂、产线、班次、OEM 承接能力 |
| 资金池 | finance_pool | 到账、开票、金融凭证、回款线索 |
| 政策池 | policy_pool | 政策、标准、行业规范、合规依据 |
| 装备池 | equipment_pool | 设备、工艺装备、产线配置 |
| 数据池 | data_pool | 文档、台账、报告、系统数据、质量记录 |
| 能源池 | energy_pool | 能耗、碳、绿电、能源数据 |
| 原料池 | material_pool | 原料、供应商、采购、库存线索 |
| 人才池 | talent_pool | 团队、专家、服务商、责任人 |
| 场景池 | scenario_pool | 场景准入、资源调用、证据门禁、退出与确认规则 |

上述 snake_case 代码是规范输出值。历史 `ORDER`、`LOGISTICS`、`CAPACITY`、`FINANCE`、`POLICY`、`EQUIPMENT`、`DATA`、`ENERGY`、`MATERIAL`、`TALENT`、`SCENARIO` 仅作为输入兼容别名，读取后必须规范化，不得用于新记录输出。

## 3. 默认挂接规则

| 内容类型 | 默认挂池 |
|---|---|
| 订单事实、客户需求、交付约定 | 订单池 |
| 发货单、物流轨迹、POD | 运力池 |
| 工厂资料、产线资料、OEM 承接资料 | 产能池 |
| 到账、开票、金融凭证 | 资金池 |
| 政策、标准、合规解释 | 政策池 |
| 设备、产线、工艺装备 | 装备池 |
| 文档、台账、会议纪要、系统导出 | 数据池 |
| 能耗、碳排、绿色能源 | 能源池 |
| 原料、材料、供应商 | 原料池 |
| 团队、专家、服务商 | 人才池 |
| 拓厂项目、区域机会、复制模板 | 场景池 |

## 4. 复合挂接规则

- 预运营期 OEM 订单资料：订单池 + 产能池 + 运力池 + 资金池。
- 质量验收资料：数据池 + 场景池 + 订单池。
- 政策驱动的原料机会：政策池 + 原料池 + 场景池。
- 新工厂复制模板：场景池 + 产能池 + 装备池 + 人才池。
- 回款争议资料：资金池 + 订单池 + 运力池 + 数据池。

## 5. 例外处理

当对象无法明确挂池时，先进入数据池并标记 `repair_required`，由 KWE 生成补充分类工单。不得因为挂池不明确而直接进入强引用、写回或收益确认。

## 6. 24字产业节点扩展

- `poolRefs` 继续必填，表示对象挂接的十一池。
- `industryNodeRefs` 可选，表示对象涉及的24字产业节点；节点代码由 KDS `工业绿链/底座/24字十一池主次映射矩阵.yaml` 控制。
- 场景对象必须增加 `requiredPoolRefs`、`supportingPoolRefs`、`entryGate`、`evidenceRequirements`、`exitConditions`、`confirmationStatus` 和 `noWriteAssertion`。
- `candidate/partial` 场景不得自动写回、自动确认收益或晋升 `accepted/published/integrated/production_ready/customer_accepted`。
