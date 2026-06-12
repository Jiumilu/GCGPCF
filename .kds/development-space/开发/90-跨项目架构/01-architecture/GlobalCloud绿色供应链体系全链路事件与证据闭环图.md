---
doc_id: GPCF-DOC-2425FD0964
title: GlobalCloud 绿色供应链体系全链路事件与证据闭环图
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud绿色供应链体系全链路事件与证据闭环图.md
source_path: 01-architecture/GlobalCloud绿色供应链体系全链路事件与证据闭环图.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系全链路事件与证据闭环图

日期：2026-06-07
状态：专项架构图 v1
口径：只展开业务事实、事件流、证据流、知识引用和治理确认如何形成闭环。

## 1. 全链路事件与证据闭环图

```mermaid
flowchart LR
  subgraph BIZ["业务事实源"]
    PVAOS["PVAOS"]
    GPC["GPC"]
    GFIS["GFIS"]
    EDGE["Edge"]
  end

  subgraph EVT["事件运行链"]
    APIGW["API Gateway"]
    OI["Outbox / Inbox"]
    BUS["Event Bus"]
    DLQ["DLQ / Replay"]
  end

  subgraph EVD["证据与追踪链"]
    EREC["EvidenceRecord"]
    BREF["BusinessApprovalReference"]
    TRACE["Trace / Correlation / Lineage"]
    METRIC["Metric / Snapshot / Risk"]
  end

  subgraph KNOW["知识与AI链"]
    KMS["知识主存层"]
    KE["KDS（主存）→ Brain（UI平台）"]
    AI["XiaoC / Hermes / XGD（大象）"]
    SUGG["AISuggestion"]
  end

  subgraph GOV["治理闭环"]
    WAES["WAES"]
    GAP["GovernanceApproval"]
    HCONF["HumanConfirmation"]
    STAT["StatusTransition / Acceptance"]
  end

  PVAOS --> APIGW
  GPC --> APIGW
  GFIS --> APIGW
  EDGE --> APIGW

  APIGW --> OI --> BUS
  BUS --> DLQ
  BUS --> EREC
  BUS --> TRACE
  BUS --> METRIC

  GPC --> BREF
  GFIS --> BREF
  BREF --> EREC

  KMS --> KE
  KE --> AI
  AI --> SUGG
  SUGG --> WAES
  KE --> WAES

  EREC --> WAES
  TRACE --> WAES
  METRIC --> WAES

  GAP --> WAES
  HCONF --> WAES
  WAES --> STAT

  WAES -. 业务确认结果引用 .-> BREF
  WAES -. 证据确证 / 状态升级 / 验收结论 .-> STAT
  SUGG -. 不得直接写业务事实 .-> GPC
  SUGG -. 不得直接写业务事实 .-> GFIS
```

## 2. 闭环说明

### 2.1 业务闭环

1. 业务事实由 `PVAOS / GPC / GFIS / Edge` 产生。
2. 事实通过 `API Gateway -> Outbox/Inbox -> Event Bus` 发布。
3. 业务确认仍在 `GPC` 或 `GFIS` 内部完成。

### 2.2 证据闭环

1. 事件、日志、回执、截图、业务确认引用进入 `EvidenceRecord`。
2. `WAES` 只做证据确证，不替代业务审批。

### 2.3 AI 闭环

1. AI 从知识引擎层读取已发布知识。
2. AI 形成 `AISuggestion`。
3. `WAES` 检查授权、证据和引用。
4. 需要业务动作时，回到 `GFIS / GPC` 内部流程。

### 2.4 状态闭环

1. `WAES` 汇总业务事实、证据、指标和人工确认。
2. 只对治理状态、验收状态和阶段状态做升级。
3. 不把业务动作本身当成 WAES 审批结果。
