---
doc_id: GPCF-DOC-3F160ABA27
title: L4 最小闭环对象契约
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/object-contracts.md
source_path: docs/harness/minimum-closed-loop/object-contracts.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# L4 最小闭环对象契约

## 核心对象

| 对象 | 归属 | 契约角色 |
|---|---|---|
| PlatformOrder | GPC | 平台订单意图与客户需求锚点 |
| SampleRequest | GPC / GFIS | 量产放行前的样品或样箱申请 |
| SampleWorkOrder | GFIS | 工厂运行层样品工单 |
| SampleApproval | GPC / WAES | 客户签收或豁免门禁 |
| ProductionRelease | WAES | FactoryOrder 之前的受控放行决策 |
| OrderMapping | GPCF | 平台记录与运行层记录之间的跨项目追踪映射 |
| FactoryOrder | GFIS | 放行门禁之后的工厂运行层订单 |
| ProofOfDelivery | GFIS / GPC | 交付与客户签收证据 |
| ExternalException | WAES | 异常与升级记录 |
| EvidenceRecord | WAES | 证据元数据与审查状态 |
| KnowledgeBacklink | KDS | 指向源材料的受控知识回链 |

## 门禁规则

- PlatformOrder 不得直接创建 FactoryOrder。
- FactoryOrder 必须满足以下其一：approved SampleApproval、approved waiver 或 approved ProductionRelease。
- SampleApproval.status in ["approved", "waived"].
- ProductionRelease.status == "approved".
- WAES.gate == "confirmed".

## 当前边界

- 这些契约只定义 L4 控制面的规则。
- GFIS runtime SOP E2E remains `repair_required`.
- 本文档不创建 customer orders、platform orders、runtime primary keys、production write、real external API write，也不升级 accepted/integrated 状态。
