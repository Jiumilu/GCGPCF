---
doc_id: GPCF-DOC-3589C1EBB3
title: GC-Knowledge Fabric 工程实施计划 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/engineering-implementation-plan-v0.1.md
source_path: docs/gc-knowledge-fabric/engineering-implementation-plan-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 工程实施计划 v0.1

## 1. 工程目标

P0 工程目标是建立 GC-Knowledge Fabric 的可审计、可验证、可复用最小骨架。P0 不接真实生产 DB，不写真实业务系统，不做自动裁决、自动结算或自动收益分配。

## 2. P0 工程交付结构

| 模块 | 交付物 | 验证方式 |
|---|---|---|
| 文档 | 架构、十一池、WAES、RAG、敏感资料、写回、LOOP、四池台账规则 | 文档门禁、受控台账 |
| OKF | ontology、schema、domain、pool、trust、flow、RAG、WAES、ledger policies | YAML/JSON schema parse |
| Shared Types | KnowledgeObject、Source、Evidence、Candidate、GateResult、WorkItem、Ledger | TypeScript 编译 |
| Fixtures | 候选事实、候选 SOP、候选写回、metadata-only、ledger、WAES gate dry-run | validator fixture check |
| Validators | no-write、RAG、WAES、pool binding、sensitive data、ledger、LOOP evidence | Python/TS validator pass |
| LOOP | 每轮输入、动作、输出、检查、反馈、下一步 | Loop 文档门禁 |

## 3. P0 任务拆解

| 任务包 | 内容 | 完成标准 |
|---|---|---|
| T0 规则固化 | 总体规则、编号、十一池、AI 边界、敏感资料、写回候选 | 文档和台账可追踪 |
| T1 OKF 契约 | ontology、object schema、pool binding、WAES、RAG、ledger policies | 契约文件可解析 |
| T2 KDS v2 骨架 | 对象、来源、证据、池、候选、搜索 contract/stub | no-write fixture 通过 |
| T3 WAES 最小门禁 | Source、Evidence、RAG、Writeback、Contribution、Revenue Gate | gate result 可解释 |
| T4 KWE 最小流程 | WorkItem、Gap、Bounty、Confirmation、Writeback dry-run | 状态不越权提升 |
| T5 葛化准备 | 葛化目录、资料分类、助手边界、候选闭环样例 | 进入 P1 条件满足 |
| T6 LOOP 指挥舱 | LOOP 模板、指标、ledger read model、风险清单 | evidence 完整 |

## 4. 接口边界

### 4.1 KDS v2

P0 只做 contract/stub/validator，不接真实生产 DB。

核心接口包括：

- `POST /api/v2/search`
- `GET /api/v2/objects/{uri}`
- `POST /api/v2/sources/import`
- `POST /api/v2/fact-candidates`
- `POST /api/v2/sop-candidates`
- `POST /api/v2/writeback-candidates`
- `GET /api/v2/graph`
- `GET /api/v2/governance/evidence`

### 4.2 WAES

P0 先实现 deterministic gate result，不引入复杂规则引擎。

gate 输出必须包含：

- `gate_type`
- `gate_status`
- `policy_version`
- `reason`
- `required_actions`
- `no_write_assertion`

### 4.3 KWE

P0 只做工单、确认包、缺口、悬赏和候选流转 dry-run flow。

KWE 不直接确认事实，不直接写业务系统，不替代委员会。

## 5. 验收指标

| 指标 | 目标 |
|---|---|
| 对象模型覆盖率 | 核心对象均有契约、类型、fixture、validator |
| OKF 契约完整性 | 所有 P0 policy 可解析、可引用 |
| WAES 可解释率 | gate result 100% 输出 reason 和 required_actions |
| no-write 通过率 | P0 所有样例 100% 无生产写入 |
| LOOP evidence 完整率 | 每轮均有输入、输出、验证、风险、下一步 |
| 敏感资料处理率 | 高敏资料默认 metadata-only 或 blocked |

## 6. 工程红线

- 不写真实 KDS TOKEN。
- 不写真实 GFIS/GPC/ERP/MES。
- 不绕过 WAES。
- 不把 AI 输出写成 accepted 或 published。
- 不把模板写成业务事实。
- 不把 potential revenue 写成 formal revenue。
- 不把自购 AI 额度写入统一收益池。

## 7. P0 完成后进入 P1 的条件

1. P0 文档、OKF、types、fixtures、validators 和 LOOP evidence 通过门禁。
2. 葛化首批资料目录和敏感分类完成。
3. GFIS 三类助手边界确认。
4. 候选事实到 WAES 到人工确认到 GFIS 写回候选 dry-run 跑通。
5. 所有生产写入仍保持 no-write。
