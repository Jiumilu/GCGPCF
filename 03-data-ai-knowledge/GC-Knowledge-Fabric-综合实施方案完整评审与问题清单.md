---
doc_id: GPCF-DOC-802968853F
title: GC-Knowledge Fabric 综合实施方案完整评审与问题清单
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-综合实施方案完整评审与问题清单.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-综合实施方案完整评审与问题清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 综合实施方案完整评审与问题清单

日期：2026-06-20  
对象：`GlobalCloud GC-Knowledge Fabric 综合实施方案与实施计划` v1.0  
结论状态：`review_completed_candidate_actions`  

## 1. 总体评分

| 维度 | 评分 | 说明 |
|---|---:|---|
| 总体完整度 | 8.2 / 10 | 已具备体系级知识工程底座雏形 |
| 战略定位清晰度 | 9 / 10 | KDS、WAES、KWE、Brain、PKC、GFIS/GPC 分工清晰 |
| 治理边界清晰度 | 9 / 10 | AI 候选、模板非事实、收益口径等边界明确 |
| 业务闭环设计 | 8 / 10 | 订单、工厂、资料、收益、悬赏、LOOP 均有入口 |
| 工程可执行性 | 6.5 / 10 | 仍需状态机、对象契约、Gate fixture 和 no-write 骨架 |
| 对象模型成熟度 | 7 / 10 | 对象清单完整，但关系图和最小字段契约不足 |
| 门禁与状态机成熟度 | 7 / 10 | 门禁类型完整，但输入输出和 hard-stop 仍需硬化 |
| 试点落地成熟度 | 7 / 10 | 葛化和湖北磷材定位清楚，但验收样例不足 |
| 验收可操作性 | 6.5 / 10 | 缺 fixture、样例输入输出和 promotion blockers |
| 风险控制意识 | 9 / 10 | 对 AI、RAG、写回、收益、模板污染的控制意识强 |

一句话评价：方案已经具备“体系级知识工程操作系统”雏形，但下一步必须从架构叙述进入受控契约、可验证样例和 no-write 工程骨架。

## 2. 核心优点

| 优点 | 价值 |
|---|---|
| 边界意识强 | 防止 AI 输出、模板、RAG、写回建议、潜在收益和自动化结果被误写成正式事实 |
| KDS / WAES / KWE / Harness / LOOP 分工合理 | 防止 Brain 变成事实主账，防止 WAES 变成业务系统，防止 AI 直接写 GFIS |
| KDS 十一池贴近业务 | 可挂接订单、运力、产能、资金、政策、装备、数据、能源、原料、人才、场景 |
| T0-T5 与 RAG 准入方向正确 | T5 默认 blocked，防止 LLM 分析污染事实底座 |
| P0-P4 路线稳健 | 先制度和契约，再 no-write 工程骨架，再试点和复制 |

## 3. P0 必须立即修正的问题

| 编号 | 问题 | 影响 | 动作 | 产物 |
|---|---|---|---|---|
| P0-R1 | 缺统一编号规则 | KDS 对象不可追溯 | 新增编号规则文档 | `GC-Knowledge-Fabric-统一编号规则.md` |
| P0-R2 | 缺统一状态机 | 状态提升不可控 | 新增状态机文档 | `GC-Knowledge-Fabric-统一状态机与状态提升规则.md` |
| P0-R3 | 缺对象关系图 | 工程建表/API 容易漂移 | 新增 ER/对象关系文档 | `GC-Knowledge-Fabric-核心对象关系与最小字段契约.md` |
| P0-R4 | WAES Gate 输入输出不够细 | 门禁无法 dry-run | 补 Gate 契约 | P0 WAES 文档 |
| P0-R5 | RAG safe 容易被误解 | 强引用风险 | 增加引用强度 L0-L5 | P0 RAG 文档 |
| P0-R6 | GFIS 写回沙箱未定义 | 容易误写主账 | 定义 Writeback Sandbox | P0 写回规则 |
| P0-R7 | 验收缺 fixture | 无法自动测试 | 建立 Gate fixture 样例 | P0 验收包 |
| P0-R8 | P0 8 文档少 3 个基础文档 | 工程底座不稳 | 扩展为 P0 11 文档包 | 总方案 v1.1 |

## 4. P1 前必须完成的问题

| 编号 | 问题 | 动作 |
|---|---|---|
| P1-R1 | 葛化资料目录还需落到编号表 | 形成七类资料包对象样表 |
| P1-R2 | GFIS 三件套助手缺评测集 | 建立 KQA / Usage / Acceptance eval 样本 |
| P1-R3 | 写回候选链路缺 no-write fixture | 建立 10 条模拟写回样例 |
| P1-R4 | 敏感资料 metadata-only 未样例化 | 金融、POD、合同、质量争议各做样例 |
| P1-R5 | 辽宁远航、现代精工链路缺责任边界模板 | 增加 OEM / 承接方责任边界表 |

## 5. P2 前必须完成的问题

| 编号 | 问题 | 动作 |
|---|---|---|
| P2-R1 | 湖北磷材不能按 GFIS 深度验收 | 单独定义拓厂/原料/订单知识包验收 |
| P2-R2 | 潜在产值容易被误用 | 增加 PotentialValueRecord 规则 |
| P2-R3 | 新工厂复制模板容易污染事实 | 模板字段与事实字段分离 |
| P2-R4 | 政策池与原料池联动未细化 | 定义政策影响候选事实模型 |
| P2-R5 | 渠道贡献与正式收益关系需分离 | 增加渠道贡献候选模型 |

## 6. v1.1 修订方向

### 6.1 从原则增强为规则

规则示例：

```yaml
llmGeneratedDefault:
  trustLevel: T5
  confirmationStatus: candidate
  ragAdmission: blocked
  allowedOperations:
    - review
    - supplement_evidence
    - create_gap
  forbiddenOperations:
    - strong_rag_reference
    - gfis_writeback
    - revenue_confirmation
```

### 6.2 从对象清单增强为对象契约

对象契约示例：

```yaml
FactCandidate:
  required:
    - id
    - statement
    - sourceRefs
    - evidenceRefs
    - trustLevel
    - poolRefs
    - ownerId
    - confirmationStatus
    - waesGateRefs
  forbidden:
    - directBusinessWriteback
  default:
    trustLevel: T5
    confirmationStatus: candidate
```

### 6.3 从路线计划增强为可验收样例

WAES 最小门禁 dry-run 至少包含：

| Gate | 最小 fixture 数 |
|---|---:|
| Source Gate | 5 |
| Evidence Gate | 5 |
| RAG Gate | 8 |
| Writeback Gate | 5 |
| Revenue Gate | 3 |
| Contribution Gate | 3 |
| External Share Gate | 2 |
| Freeze Gate | 2 |

## 7. 修订后的实施顺序

1. 固化总方案 v1.1。
2. 拆出 P0 11 份受控文档。
3. 建立统一编号规则。
4. 建立统一状态机。
5. 建立核心对象关系图。
6. 建立 WAES Gate 输入输出契约。
7. 建立 RAG 准入 + 引用强度规则。
8. 建立 Gate dry-run fixture。
9. 建立葛化 / 湖北磷材目录样表。
10. 建立 P0 LOOP 记录与验收清单。
11. 建立 OKF YAML / JSON Schema。
12. 建立 KDS v2 no-write 数据骨架。
13. 建立 WAES dry-run service。
14. 建立 KWE work-item skeleton。
15. 执行 GFIS 三件套助手评测。
16. 执行 LOOP 指挥舱 dry-run。

## 8. 不升级声明

本评审不证明：

1. GC-Knowledge Fabric 已完成工程实现。
2. GFIS / GPC / KDS / WAES / Brain 已发生真实生产写入。
3. RAG 强引用已经准入。
4. 收益、积分、额度、悬赏已经结算。
5. 委员会已经完成裁决。

本评审只形成问题清单和修订任务，不自动升级任何业务状态。
