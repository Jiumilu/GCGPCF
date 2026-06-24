---
doc_id: GPCF-DOC-D23F122F5C
title: GC-Knowledge Fabric P0 两周执行任务排期表 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/p0-two-week-execution-schedule-v0.1.md
source_path: docs/gc-knowledge-fabric/p0-two-week-execution-schedule-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 两周执行任务排期表 v0.1

## 1. 排期定位

本文档将《GC-Knowledge Fabric 工程实施计划 v0.1》拆解为 P0 两周执行任务排期。P0 只交付受控文档、OKF 契约、schema/types、dry-run fixtures、validators 和 LOOP evidence，不接真实生产 DB，不写 GFIS/GPC/ERP/MES，不做自动裁决、自动积分、自动收益分配或自动悬赏结算。

## 2. 成功标准

P0 成功标准为：

```text
可审计 + 可验证 + 可复用
```

P0 不以业务上线作为验收口径。

## 3. 执行节奏

| 工作日 | 主题 | 主要任务 | 当日输出 | 验证方式 |
|---|---|---|---|---|
| D1 | 规则冻结 | 锁定 Q1-Q40 需求口径、AI 边界、no-write 边界、P0/P1/P2 范围 | 需求锁定稿、管理层摘要、工程计划、试点清单 | 文档门禁 |
| D2 | 目录与编号 | 固化对象编号、KDS 十一池挂接、Domain + Pool 双维模型 | 编号规则、挂池规则、对象目录清单 | pool binding validator |
| D3 | OKF 契约 | 建立 ontology、knowledge object schema、domain/pool/trust/flow policy | OKF v0.1 契约包 | YAML/JSON parse |
| D4 | WAES/RAG 规则 | 建立 Source/Evidence/RAG/Writeback/Contribution/Revenue gate 规则 | WAES gate policy、RAG admission policy | gate validator |
| D5 | 敏感资料与四池 | 建立 metadata-only、blocked、Contribution/Revenue/Quota/Bounty ledger 边界 | 敏感资料规则、四池台账规则 | no-write + ledger validator |
| D6 | Shared Types | 建立 KnowledgeObject、Source、Evidence、Candidate、GateResult、WorkItem、Ledger 类型 | shared types v0.1 | TypeScript 编译 |
| D7 | Fixtures | 建立候选事实、候选 SOP、候选写回、metadata-only、WAES gate、ledger dry-run 样例 | fixtures v0.1 | fixture validator |
| D8 | Validators | 建立对象覆盖、挂池、WAES、RAG、敏感资料、四池、LOOP evidence 校验 | validators v0.1 | validator pass |
| D9 | 葛化 P1 准备 | 建立葛化资料目录、四类敏感分级、GFIS 三助手边界、候选闭环样例 | 葛化 P1 admission pack | no-write dry-run |
| D10 | P0 收口 | 汇总 P0 evidence、风险、阻塞、P1 进入条件和 v1.0 升级建议 | P0 closure packet | 三项文档门禁 |

## 4. 任务包到排期映射

| 任务包 | 覆盖工作日 | 完成标准 |
|---|---|---|
| T0 规则固化 | D1-D2 | 文档和台账可追踪 |
| T1 OKF 契约 | D3-D4 | 契约文件可解析 |
| T2 KDS v2 骨架 | D3-D8 | contract/stub/fixture/validator 完整 |
| T3 WAES 最小门禁 | D4-D8 | gate result 可解释 |
| T4 KWE 最小流程 | D6-D8 | WorkItem/Gap/Bounty/Confirmation dry-run 不越权 |
| T5 葛化准备 | D9 | 进入 P1 条件可审查 |
| T6 LOOP 指挥舱 | D1-D10 | 每日有 LOOP evidence |

## 5. 每日 Definition of Done

每日 DoD 必须同时满足：

- 有明确输入资料。
- 有当日输出文件或 evidence。
- 有验证命令或人工检查项。
- 有 no-write 边界说明。
- 有风险和下一步。

任一项缺失，当日状态只能记为 `partial`，不得写为完成。

## 6. 角色与责任输入

| 角色 | P0 输入 | P0 输出确认 |
|---|---|---|
| GPCF 总控 | 规则、文档、台账、LOOP 门禁 | P0 evidence 与收口包 |
| KDS | 对象模型、池子、source/evidence、RAG 准入 | KDS v2 契约与 no-write 骨架 |
| WAES | gate 类型、policy、required_actions | gate result validator |
| KWE | work item、gap、bounty、confirmation、writeback dry-run | 流程对象和状态边界 |
| GFIS | 葛化资料目录、字段、助手边界 | P1 admission pack |
| Brain/PKC | 信息架构、入口和只读视图边界 | 后续 UI/console 合同 |
| 业务负责人 | 葛化/湖北磷材资料 owner、敏感分类、确认路径 | 人工确认责任表 |

## 7. 硬停止条件

出现以下任一情况，P0 自动暂停并进入人工确认：

- 需要真实 GFIS/GPC/ERP/MES 写入。
- 需要真实 KDS TOKEN 或生产 API 调用。
- 发现合同、金融凭证、POD、质量争议原文被开放引用。
- AI 输出被写成 accepted、published、written_back 或正式收益。
- 潜在收益被自动转为正式收益。
- 自购 AI 额度被写入统一收益池。
- 委员会未确认但生成裁决结论。

## 8. P0 收口包

D10 必须形成 P0 收口包，至少包含：

- P0 完成项清单。
- 未完成项和阻塞项。
- 所有 validator 结果。
- no-write 断言。
- 敏感资料处理结果。
- 葛化 P1 admission 判断。
- 湖北磷材 P2 准备状态。
- 是否建议 v0.1 升级 v1.0。

## 9. 下一步

本排期表经人工确认后，可作为 P0 每日 LOOP 执行输入。执行过程中仍保持 draft 边界，直到 P0 收口包和人工确认完成后再考虑升级为 v1.0。
