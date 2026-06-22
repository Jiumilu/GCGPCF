---
doc_id: GPCF-DOC-6CF5DB2D6B
title: GC-Knowledge Fabric 葛化GFIS知识库目录
project: KDS
related_projects: [GFIS, PVAOS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-葛化GFIS知识库目录.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-葛化GFIS知识库目录.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 葛化GFIS知识库目录

## 1. 定位

葛化 GFIS 知识库是 P1 阶段 GFIS 标准母版试点目录。该目录用于组织建设、运营、订单、OEM 过渡、质量、发货、POD、金融凭证与会议资料，不代表资料已经验收或写回。

## 2. 一级目录

| 目录 | 默认 Domain | 默认挂池 | 说明 |
|---|---|---|---|
| 建设资料 | project | 场景池 + 产能池 + 装备池 | 工厂建设、设备、产线规划 |
| 工厂运营资料 | project / supply_chain | 产能池 + 数据池 + 人才池 | 班组、产线、运营台账 |
| 订单资料 | project / supply_chain | 订单池 + 资金池 | 订单、客户需求、合同执行 |
| 辽宁远航链路资料 | supply_chain | 订单池 + 运力池 + 资金池 | 客户侧需求、交付、POD、回款线索 |
| 现代精工 OEM 过渡资料 | supply_chain | 产能池 + 订单池 + 数据池 | 承接方产能、质量、交付责任边界 |
| 质量资料 | project / supply_chain | 数据池 + 订单池 + 场景池 | 检验、验收、争议记录 |
| 发货与 POD 资料 | supply_chain | 运力池 + 订单池 + 数据池 | 发货单、签收、POD |
| 金融凭证门禁资料 | governance / project | 资金池 + 数据池 | 到账、开票、凭证 metadata-only |
| 会议纪要 | workspace / project | 数据池 + 场景池 | 待确认事实来源 |
| 政策与标准资料 | org / public | 政策池 | 合规、标准、政策依据 |

## 3. GFIS 助手边界

- 知识问答助手只能回答已准入知识，并提示缺口。
- 使用助手只能提供字段、流程和门禁解释。
- 文档验收助手只能给出候选验收建议。
- 三类助手均不得直接确认收益、责任、争议结论或正式写回。

## 4. P1 优先入池对象

- 建设资料入池。
- 工厂运营资料入池。
- 订单资料入池。
- 辽宁远航链路入池。
- 现代精工 OEM 过渡资料入池。
- 质量、发货、POD、金融凭证资料进入门禁登记。
