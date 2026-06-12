---
doc_id: GPCF-DOC-31CB143A7C
title: GlobalCloud 绿色供应链体系 WAES 控制塔治理架构图
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md
source_path: 01-architecture/GlobalCloud绿色供应链体系WAES控制塔治理架构图.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系 WAES 控制塔治理架构图

日期：2026-06-07
状态：WAES 控制塔治理架构图 v1
口径：只看治理、证据、状态、授权和控制塔视图。

## 1. WAES 治理总图

```mermaid
flowchart TB
  subgraph Source["来源系统"]
    PVAOS["PVAOS<br/>组织 / 项目 / 伙伴"]
    GPC["GPC<br/>订单 / 运输 / POD / 外部异常"]
    GFIS["GFIS<br/>工单 / 质量 / 库存 / 发货 / 设备"]
    Edge["Edge<br/>遥测 / 报警 / 补传"]
    Brain["Brain / XiaoC / Hermes / XGD（大象）<br/>知识 / Prompt / Agent / 建议"]
  end

  subgraph WAES["WAES 控制塔与治理平面"]
    Rule["治理规则<br/>GovernanceRule / PolicyAssignment"]
    Evidence["证据台账<br/>EvidenceRecord / EvidenceVerification"]
    Status["状态治理<br/>StatusTransitionRequest / StatusAudit"]
    Metric["指标与追踪<br/>Metric / Trace / Risk / Exception"]
    AIAuth["AI 授权<br/>AgentToolGrant / AISuggestion / 越权拦截"]
    Release["发布验证<br/>ReleaseGate / ConnectorLifecycle"]
  end

  Harness["Harness<br/>Manifest / 验收 / 项目边界 / 状态纪律"]
  Human["人工确认"]

  PVAOS --> WAES
  GPC --> WAES
  GFIS --> WAES
  Edge --> WAES
  Brain --> WAES

  Harness --> WAES
  WAES --> Human

  Rule --> Evidence
  Evidence --> Status
  Metric --> Status
  AIAuth --> Status
  Release --> Status
```

## 2. WAES 主责

1. 项目发起、模板启用、发布验证。
2. 治理规则、指标口径、状态升级。
3. 证据捕获、确证、驳回、归档。
4. 控制塔监控、异常聚合、风险视图。
5. AI 授权、工具权限、越权拦截。

## 3. WAES 不做什么

1. 不审批工单。
2. 不审批质量放行。
3. 不审批库存调整。
4. 不审批发货。
5. 不审批签收。
6. 不直接写 `GFIS` 或 `GPC` 业务主账。
