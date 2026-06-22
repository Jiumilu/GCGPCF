---
doc_id: GPCF-DOC-3501DC0BDB
title: GC-Knowledge Fabric 需求确认纪要与 P0-P2 实施计划 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/requirements-confirmation-and-p0-p2-implementation-plan-v0.1.md
source_path: docs/gc-knowledge-fabric/requirements-confirmation-and-p0-p2-implementation-plan-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 需求确认纪要与 P0-P2 实施计划 v0.1

## 1. 文档定位

本文档固化《GC-Knowledge Fabric 综合实施方案与实施计划》问答确认结果，作为后续受控文档包、上会材料、工程拆解和试点推进的 v0.1 需求确认稿。

本稿只锁定需求口径、实施边界、验收指标和 P0-P2 计划，不声明业务系统已上线，不声明真实 GFIS/GPC 写回已完成，不声明委员会真实裁决流程已运行。

## 2. 总体结论

GC-Knowledge Fabric 的最高治理原则确认如下：

- 楚商云掌控规则、底座、门禁和停机权。
- 委员会处理具体裁决、争议、收益分配和重大违规事项。
- AI 只生成候选事实、候选 SOP、候选写回、缺口识别、验收建议和风险提示。
- KDS 作为知识事实底座和 RAG 准入状态源。
- OKF 定义对象、规则、流转、门禁和准入契约。
- WAES 执行规则门禁、风险拦截和人工/委员会路径触发。
- KWE 推动候选到可信资产的工单、确认、补证、脱敏、发布、争议和写回候选流程。
- Brain/PKC/GFIS/GPC 只消费已授权、已准入、已确认或明确标记为候选的知识。
- Harness/LOOP 保证 evidence、验收、审计和持续闭环。

## 3. 已确认需求口径

### 3.1 P0 实施边界

P0 不是只写蓝图，而是落到受控工程骨架：

- 受控文档。
- OKF 契约。
- schema/types。
- dry-run fixtures。
- validators。
- LOOP evidence。

P0 不做以下事项：

- 不接真实生产 DB。
- 不写 GFIS/GPC/ERP/MES 生产系统。
- 不自动确认事实。
- 不自动确认积分。
- 不自动分配收益。
- 不自动结算悬赏。
- 不自动执行委员会裁决。
- 不把演示样例包装成真实生产闭环。

P0 允许形成可演示样例，但必须标注 `dry-run`、`fixture`、`preview`、`candidate` 或 `no-write`。

### 3.2 试点顺序

实施顺序确认为：

1. GPCF 总控仓先固化规则、契约、验证器和 LOOP evidence。
2. P1 进入葛化 GFIS 母版试点。
3. P2 进入湖北磷材并行知识库与新工厂复制模板。
4. P3 才推进多单位复制。
5. P4 自运行与协同进化不跳级承诺，只在 P0-P2 验收后滚动推进。

### 3.3 AI 边界

AI 只能生成：

- 候选事实。
- 候选 SOP。
- 候选字段。
- 候选状态。
- 候选风险。
- 候选缺口。
- 候选积分。
- 候选收益贡献。
- 候选验收建议。
- 候选写回建议。
- 候选 RAG 引用建议。

AI 不能直接形成：

- 正式业务事实。
- 正式 GFIS/GPC 写回。
- 正式收益分配。
- 正式积分确认。
- 正式产值贡献。
- 正式 RAG 强引用。
- 重大违规结论。
- 委员会裁决结果。
- 供应链责任归因。
- 合同、金融、POD、质量争议结论。

正式事实入账必须同时满足：

```text
source + evidence + WAES + human/committee confirmation + Harness evidence
```

### 3.4 KDS 与十一池

KDS 十一池是所有高价值对象的强制挂接维度。

高价值对象必须至少有一个 `poolRef`。无法判断挂池时，先进入：

```text
数据池 + repair_required
```

P0 对象模型以以下核心对象为最小闭环：

- KnowledgeObject。
- SourceRecord。
- EvidenceRecord。
- FactCandidate。
- SOPCandidate。
- WritebackCandidate。
- WAES GateResult。
- KWE WorkItem。
- Contribution Ledger。
- Revenue Ledger。
- Quota Ledger。
- Bounty Ledger。

### 3.5 权限与跨单位可见性

P0 权限模型采用最小可行 ACL：

- tenant。
- domain。
- visibility。
- owner。
- project。
- external_account。

所有对象必须有可追责 owner 和明确可见性。

跨单位数据默认采用最小可见原则。合作单位默认只能看到：

- 自己的贡献。
- 自己的积分。
- 自己的 AI 额度。
- 自己的争议状态。
- 自己参与的悬赏。
- 自己被授权的项目视图。

未经授权，不默认展示其他单位明细。

### 3.6 敏感资料边界

葛化首批资料分为四类：

| 分类 | 处理方式 |
|---|---|
| 可开放问答 | 可进入受控问答和 RAG safe/limited |
| 受限引用 | 可摘要、可提示、按 ACL 引用 |
| metadata-only | 只存编号、状态、哈希、摘要、权限、证据链位置 |
| blocked | 不进入 RAG，不对助手开放 |

合同、金融凭证、POD、质量争议、责任归因、收益分配默认进入人工或委员会路径。

金融凭证、POD、质量争议、合同敏感信息默认不暴露原文。

### 3.7 RAG 准入

RAG 引用强度确认如下：

- `safe`：允许强引用。
- `limited`：只允许弱引用或提示性引用。
- `repair_required`：不得强引用，必须提示证据缺口。
- `blocked`：禁止引用。
- `sensitive_metadata_only`：只能引用元数据，不暴露原文。
- T5/LLM 输出：默认 blocked，除非转为 source-backed 并通过确认。

### 3.8 收益、积分、额度、悬赏

贡献账与收益账必须分开：

- `Contribution Ledger` 记录知识贡献、证据贡献、渠道贡献、SOP 贡献、纠错贡献和验收贡献。
- `Revenue Ledger` 记录正式收益、开票收入、潜在收益、渠道机会和知识潜在价值。

关键边界：

- 已到账收入才是正式收益。
- 已开票收入只能进入财务统计。
- 未到账机会只能进入潜在收益。
- 知识帮助但无收入只能进入知识贡献。
- 自购 AI 额度不进入统一收益池。
- 悬赏结算必须经过 WAES gate、人工验收和争议期。

## 4. P0-P2 实施计划

### 4.1 P0：受控工程骨架

建议周期：2 周。

目标：

完成制度、编号、目录、门禁、台账、LOOP 模板和最小工程骨架固化。

交付物：

| 类别 | 交付物 |
|---|---|
| 文档 | 规则总纲、KDS 十一池挂接规则、WAES 门禁规则、RAG 准入规则、敏感资料规则、写回候选规则、LOOP 模板 |
| OKF | ontology、object schema、domain policy、pool binding、trust、flow、RAG、WAES、contribution、revenue、quota、bounty、redaction、committee、writeback |
| Types | KnowledgeObject、Source、Evidence、Candidate、GateResult、WorkItem、Ledger 相关类型 |
| Fixtures | 首批 dry-run 样例，覆盖候选、门禁、台账、metadata-only 和 no-write |
| Validators | 检查对象覆盖、挂池、RAG、WAES、no-write、敏感资料、四池边界和 LOOP evidence |
| LOOP | 每轮输入、动作、输出、检查、反馈和下一步建议 |

P0 验收指标：

| 指标 | 验收口径 |
|---|---|
| 对象模型覆盖率 | 首批核心对象均有 schema/types/fixture/validator 对应 |
| OKF 契约完整性 | P0 policy 文件可解析、可追踪、可被 validator 引用 |
| WAES gate 可解释率 | gate 输出包含 status、reason、required_actions 和 policy_version |
| no-write 通过率 | 所有 P0 样例不得写真实业务系统或外部 API |
| LOOP evidence 完整率 | 每轮有输入、输出、验证、风险、下一步 |
| 敏感资料处理率 | 合同、金融、POD、质量争议默认 metadata-only 或 blocked |

P0 成功标准：

```text
可审计 + 可验证 + 可复用
```

P0 不作为业务上线标准。

### 4.2 P1：葛化 GFIS 母版试点

建议周期：4 到 6 周。

目标：

形成第一个可复制的 GFIS 知识母版。

交付物：

- 葛化 GFIS 知识目录。
- 建设资料入池。
- 工厂运营资料入池。
- 订单资料入池。
- 辽宁远航链路资料入池。
- 现代精工 OEM 过渡资料入池。
- 质量、发货、POD、金融凭证资料门禁。
- GFIS 知识问答助手。
- GFIS 使用助手。
- GFIS 文档验收助手。
- 候选事实到 WAES 到人工确认到 GFIS 写回候选 dry-run 闭环。

P1 验收闭环：

```text
真实资料目录
-> 候选事实样例
-> WAES 判断
-> 人工确认路径
-> GFIS 写回候选 dry-run
-> Harness evidence
```

P1 不直接跳过人工确认，不直接写正式 GFIS。

### 4.3 P2：湖北磷材并行线

建议周期：4 到 6 周。

目标：

建设拓厂、原料、行业、订单、新工厂复制模板知识体系。

交付物：

- 拓厂项目知识库。
- 原料/行业/订单知识库。
- 新工厂复制模板。
- 区域绿色供应链知识图谱。
- 潜在产值与渠道贡献计量。
- 政策池与原料池联动。

P2 验收闭环：

```text
拓厂知识包
-> 原料/行业/订单知识包
-> 新工厂复制模板
-> 潜在收益/渠道贡献台账
-> WAES/RAG/LOOP evidence
```

P2 不依赖 GFIS 深度闭环，也不把葛化模板自动转成湖北磷材业务事实。

## 5. 风险分级

| 风险等级 | 风险类型 | 默认处理 |
|---|---|---|
| P0 | 生产写入、敏感泄露、收益误分配、重大违规结论误判 | hard stop，冻结对象或流程，进入治理/委员会 |
| P1 | 事实误确认、错误 RAG 强引用、责任归因错误 | 阻断 promotion，人工或委员会复核 |
| P2 | 流程延误、证据缺口、挂池不完整、ACL 缺失 | repair_required，生成 KWE work item |
| P3 | 普通目录缺漏、文档格式问题、非关键字段缺失 | 记录缺口，纳入下一轮 LOOP |

## 6. 上会材料拆分

后续上会材料拆为三份：

1. 管理层摘要：讲清定位、价值、治理权、试点路径、风险边界。
2. 工程实施计划：讲清 P0-P2 交付物、接口、数据模型、验证器、门禁和排期。
3. 试点推进清单：讲清葛化和湖北磷材各自资料、角色、待办、验收闭环和阻塞项。

## 7. 决策项清单

| 编号 | 决策项 | 推荐结论 | 状态 |
|---|---|---|---|
| D-01 | P0 是否声明业务上线 | 不声明，只声明工程治理底座可用 | 已确认 |
| D-02 | 是否允许真实业务写回 | P0 不允许，只做 no-write candidate/dry-run | 已确认 |
| D-03 | AI 是否可直接确认事实 | 不可以 | 已确认 |
| D-04 | 委员会是否 P0 真实运行 | P0 只固化规则和记录模型 | 已确认 |
| D-05 | 葛化与湖北磷材顺序 | 葛化 P1 主线，湖北磷材 P2 并行准备 | 已确认 |
| D-06 | 自购 AI 额度是否进收益池 | 不进入统一收益池 | 已确认 |
| D-07 | 模板是否自动成为事实 | 不自动成为事实 | 已确认 |
| D-08 | 是否生成 v0.1 受控文档 | 是，先 draft，确认后再升级 v1.0 | 已确认 |

## 8. 下一步动作

1. 本文档作为 v0.1 draft 进入 GPCF 受控文档目录。
2. 运行文档污染检查、KDS TOKEN 检查和 Loop 文档门禁。
3. 由人工确认是否将 v0.1 升级为受控 v1.0。
4. v1.0 确认后，拆分生成管理层摘要、工程实施计划和试点推进清单。
5. P0 工程实施继续保持 no-write、dry-run、candidate-only 和 evidence-first 边界。
