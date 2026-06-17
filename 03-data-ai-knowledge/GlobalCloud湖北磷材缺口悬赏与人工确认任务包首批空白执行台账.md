---
doc_id: GPCF-DOC-77DB51C32D
title: GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批空白执行台账
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批空白执行台账.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批空白执行台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批空白执行台账

日期：2026-06-17  
状态：`blank_execution_register`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-038《GlobalCloud 湖北磷材 SOP 候选写回规则到缺口悬赏与人工确认任务包》，把 `MCT`、`BAC`、`CTC`、`CLC` 和 `PPC` 对象转成首批可填报的空白执行台账。

本文是执行登记模板，不是实际执行记录。本文不证明已收到真实资料、不发布悬赏、不冻结资源、不结算积分、不分配收益、不发放 AI 额度、不进行委员会真实裁决、不发布 Brain 页面、不放行 WAES、不写真实 KDS API、不写 GFIS、GPC、PVAOS 或其他业务系统主账。

## 2. 输入关系

| 来源 | 承接内容 | 本文处理 |
|---|---|---|
| DKS-038 任务包 | `MCT` / `BAC` / `CTC` / `CLC` / `PPC` 对象 | 转为空白执行行 |
| DKS-025 缺口悬赏台账 | KGR / RRT / KGB / CSR / GCR 机制 | 作为悬赏候选与资料回收参考，不发布 |
| DKS-035 湖北磷材评审空白台账 | FEA / IND / ORD 页面候选和发布前问题 | 保持拓厂、行业、订单三线试点 |
| DKS-020 积分收益额度悬赏争议联动规则 | 增强账本挂接、收益口径、争议处理 | 保持 candidate / planned / blank 状态 |

## 3. 执行字段定义

| 字段 | 可选值 | 含义 |
|---|---|---|
| `executionState` | planned / assigned_candidate / source_submitted_candidate / waes_rule_recorded / human_review_pending / committee_if_needed / returned / withdrawn / closed | 任务执行状态 |
| `sourceReceiptStatus` | blank / waiting_source / metadata_received / redacted_source_received / returned / blocked | 资料接收状态 |
| `waesRecordStatus` | blank / planned / recorded / returned / blocked | WAES 规则记录状态 |
| `humanReviewStatus` | blank / pending / pass / partial / returned / blocked | 人工确认状态 |
| `committeeStatus` | none / filing_planned / decision_planned / filed / decided / not_required | 委员会备案或裁决状态 |
| `bountyStatus` | candidate_only / ready_for_sponsor / resource_pending_freeze / published_if_confirmed / withdrawn / closed | 悬赏状态 |
| `settlementStatus` | not_applicable / prohibited_before_acceptance / pending_dispute_period / settled | 结算状态 |

本台账首批行均不得出现 `settled`、`published_if_confirmed`、`decided` 或 `closed`，除非后续有独立 LOOP 证据、人工确认、WAES 记录和委员会或发起方确认。

## 4. ManualConfirmationExecutionRegister

| registerId | taskId | linkedControlPointId | executionState | sourceReceiptStatus | waesRecordStatus | humanReviewStatus | committeeStatus | kdsPoolRefs | enhancedLedgerRefs | evidenceSlot | nextAction |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `MER-HBLC-FEA-202606-0001` | `MCT-HBLC-FEA-202606-0001` | `SCP-HBLC-FEA-202606-0001` | planned | blank | planned | blank | none | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 / 悬赏池 | 待填来源索引、脱敏摘要、负责人确认 | 等待湖北磷材项目组确认拓厂来源接收口径 |
| `MER-HBLC-FEA-202606-0002` | `MCT-HBLC-FEA-202606-0002` | `SCP-HBLC-FEA-202606-0001` | planned | blank | planned | blank | none | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 / 悬赏池 / 争议池 | 待填 KDS 池挂接与增强账本挂接表 | 等待 KDS 记录人复核挂接关系 |
| `MER-HBLC-IND-202606-0001` | `MCT-HBLC-IND-202606-0001` | `SCP-HBLC-IND-202606-0001` | planned | blank | planned | blank | none | 政策池 / 数据池 / 场景池 | 贡献账本 / 悬赏池 | 待填权威来源链接、检索时间、适用范围 | 等待行业资料责任方提交来源索引 |
| `MER-HBLC-ORD-202606-0001` | `MCT-HBLC-ORD-202606-0001` | `SCP-HBLC-ORD-202606-0001` | planned | blank | planned | blank | none | 订单池 / 产能池 / 资金池 / 数据池 | 潜在产值池 / 贡献账本 / 悬赏池 | 待填电话、会议或邮件来源摘要、客户匿名编号 | 等待销售或渠道责任方提交线索摘要 |
| `MER-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | `SCP-HBLC-ORD-202606-0001` | planned | blank | planned | blank | filing_planned | 订单池 / 资金池 / 场景池 | 潜在产值池 / 争议池 / 贡献账本 | 待填潜在产值说明、开票统计字段、到账跟踪字段 | 等待财务口径复核到账与开票区分 |

## 5. BountyActivationExecutionRegister

| registerId | bountyActivationId | linkedTaskId | bountyStatus | settlementStatus | sourceReceiptStatus | eligibleParticipants | visibility | resourceBoundary | evidenceSlot | nextAction |
|---|---|---|---|---|---|---|---|---|---|---|
| `BER-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | `MCT-HBLC-FEA-202606-0001` | candidate_only | prohibited_before_acceptance | blank | 湖北磷材项目组 / 受邀合作单位 / 项目组授权人员 | directed | 未确认资源来源，不冻结积分、收益或 AI 额度 | 待填悬赏范围、验收标准、资源来源 | 等待发起方确认是否进入悬赏准备 |
| `BER-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | `MCT-HBLC-IND-202606-0001` | candidate_only | prohibited_before_acceptance | blank | 所有授权人员或单位 / 受邀专家 / 资料责任方 | semi_public_or_directed | 不得直接确认高可信结论或政策适用结论 | 待填来源范围、可信层级规则 | 等待 WAES 规则记录 |
| `BER-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | `MCT-HBLC-ORD-202606-0001` | candidate_only | prohibited_before_acceptance | blank | 销售责任方 / 渠道方 / 受邀合作单位 | directed | 无到账不得确认正式产值积分或正式收益分配 | 待填线索来源、客户匿名编号、收益边界 | 等待线索责任方补齐来源摘要 |
| `BER-HBLC-ORD-202606-0002` | `BAC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | candidate_only | prohibited_before_acceptance | blank | 销售责任方 / 财务联系人 / 项目组授权人员 | private_or_directed | 开票只作统计、财务和流程口径；正式收入按到账 | 待填潜在产值、开票统计、到账跟踪 | 等待财务复核字段定义 |

## 6. CommitteeTriggerExecutionRegister

| registerId | triggerId | linkedObject | triggerCondition | committeeStatus | freezeRule | userBoundary | evidenceSlot | nextAction |
|---|---|---|---|---|---|---|---|---|
| `CER-HBLC-FEA-202606-0001` | `CTC-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | 悬赏奖励、跨单位贡献比例、重大复用争议或拓厂机会收益预期不清 | filing_planned | 争议期冻结候选贡献，不冻结自购 AI 额度 | 用户保留规则治理权、急停权和体系治理权 | 待填备案材料和多数决记录 | 等待是否触发备案 |
| `CER-HBLC-IND-202606-0001` | `CTC-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | 权威来源层级、适用范围或引用权属发生争议 | filing_planned | 争议期不升级可信层级 | 用户可调整规则原则，不替代具体归属判断 | 待填来源争议说明 | 等待来源复核是否存在争议 |
| `CER-HBLC-ORD-202606-0001` | `CTC-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | 潜在产值贡献、渠道贡献、收入归属、开票与到账口径发生争议 | filing_planned | 冻结候选贡献，等待到账或证据补齐 | 用户保留急停和规则边界，不裁决收益比例 | 待填争议事实、收入状态、财务口径 | 等待订单线索进入人工复核 |
| `CER-HBLC-ORD-202606-0002` | `CTC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | 候选记录误写为正式订单、正式收入或 GFIS 主账 | decision_planned | 一般违规酌情溯源扣除，重大违规按事实比例或全部扣除 | 用户可急停越权写回 | 待填违规事实、影响范围、追溯建议 | 等待是否出现越权写回迹象 |

## 7. ClosureExecutionRegister

| registerId | closureId | linkedTaskId | executionState | closeAsPassEvidence | closeAsPartialEvidence | returnEvidence | withdrawEvidence | currentBoundary |
|---|---|---|---|---|---|---|---|---|
| `CLR-HBLC-FEA-202606-0001` | `CLC-HBLC-FEA-202606-0001` | `MCT-HBLC-FEA-202606-0001` | planned | 待填来源索引、区域资料、项目负责人确认、WAES 记录 | 待填部分来源说明 | 待填来源缺失或责任主体不清说明 | 待填来源证伪或授权撤回说明 | 未满足关闭条件 |
| `CLR-HBLC-FEA-202606-0002` | `CLC-HBLC-FEA-202606-0002` | `MCT-HBLC-FEA-202606-0002` | planned | 待填 KDS 11 池和增强账本完整挂接表 | 待填增强账本待补说明 | 待填账本游离或池挂接错误说明 | 待填误挂接风险说明 | 未满足关闭条件 |
| `CLR-HBLC-IND-202606-0001` | `CLC-HBLC-IND-202606-0001` | `MCT-HBLC-IND-202606-0001` | planned | 待填权威来源链接、检索时间、适用范围、可信层级建议 | 待填适用范围继续评估说明 | 待填缺来源或缺检索时间说明 | 待填来源失效或授权不可用说明 | 未满足关闭条件 |
| `CLR-HBLC-ORD-202606-0001` | `CLC-HBLC-ORD-202606-0001` | `MCT-HBLC-ORD-202606-0001` | planned | 待填线索来源、客户匿名编号、需求时间、责任人、收益边界 | 待填客户匿名编号或责任人待补说明 | 待填误写正式订单、开票或到账收入说明 | 待填线索撤回或证伪说明 | 未满足关闭条件 |
| `CLR-HBLC-ORD-202606-0002` | `CLC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | planned | 待填潜在产值候选、开票统计、到账跟踪区分记录 | 待填暂无开票或到账跟踪说明 | 待填以开票替代到账或误入正式收益池说明 | 待填线索无效或客户撤回说明 | 未满足关闭条件 |

## 8. PKCParticipationExecutionRegister

| registerId | participationId | linkedBountyActivationId | participantScope | allowedContribution | restrictedContribution | settlementBoundary | submissionSlot | nextAction |
|---|---|---|---|---|---|---|---|---|
| `PER-HBLC-FEA-202606-0001` | `PPC-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | 湖北磷材项目组、受邀合作单位成员、授权专家 | 拓厂来源摘要、区域资料索引、政策来源索引、差异项说明 | 未授权原文、敏感价格、合同原文或个人信息 | 验收前只形成个人贡献候选 | 待填提交入口和脱敏要求 | 等待参与范围确认 |
| `PER-HBLC-IND-202606-0001` | `PPC-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | 所有授权人员或单位、受邀专家 | 权威来源链接、检索时间、适用范围说明 | 非权威资料不得写成高可信结论 | 可信层级升级必须经 WAES 和人工确认 | 待填来源提交入口 | 等待可信来源标准确认 |
| `PER-HBLC-ORD-202606-0001` | `PPC-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | 销售责任方、渠道方、受邀合作单位成员 | 线索来源摘要、客户匿名编号、需求时间、责任主体候选 | 客户实名、未授权合同原文、正式收入声明 | 到账前不得确认正式产值积分或收益分配 | 待填线索提交入口和权限说明 | 等待订单线索脱敏模板确认 |

## 9. 证据清单

每一行进入 `source_submitted_candidate` 或更高状态前，至少需要登记：

1. 来源索引或资料接收编号。
2. 脱敏摘要和权限说明。
3. KDS 11 池挂接关系。
4. 增强账本挂接关系。
5. WAES 规则记录或规则内记录说明。
6. 人工确认记录。
7. 需要委员会时的备案或裁决记录。
8. LOOP 轮次证据与回滚说明。

## 10. 底座可用知识闭环率

为避免只看“有没有数据”而忽略事实成熟、来源证据、台账一致性和缺口写回，本文将关键指标定义为：

```text
底座可用知识闭环率 =
状态覆盖率 x 20%
+ 事实成熟度 DQ x 25%
+ 来源/证据合格率 x 20%
+ registry/台账/报告一致性 x 15%
+ 自动化处理有效率 x 10%
+ 写回缺口闭环率 x 10%
```

该指标用于判断一条底座数据是否完成：

```text
入池 -> 有状态 -> 有来源 -> 经核验 -> 可追溯 -> 可被指挥舱/RAG安全调用 -> 缺口可写回闭环
```

### 10.1 当前初评口径

| 维度 | 当前观察 | 初评 |
|---|---|---|
| 状态覆盖率 | active 十池状态覆盖均值为 100% | 池骨架和状态位已齐 |
| 事实成熟度 DQ | 十池事实成熟度均值为 53% | 中等，仍有较多 `pending_*`、`planning`、`covered_partial` |
| 来源/证据合格率 | 数据池 project_id 覆盖 100%，RAG 准入失败 0，敏感命中 0 | 治理质量较好，但仍需逐条看证据等级 |
| registry/台账/报告一致性 | 数据质量评分体系要求 registry、项目页、台账、报告一致 | 可作为强门禁维度 |
| 自动化处理有效率 | 底座相关 ACTIVE automation 当前为 0 | 自动回读、自动补证、自动关闭缺口仍需补强 |
| 写回缺口闭环率 | 写回队列仍有 12 个 open | 缺口闭环尚未跑实 |

一句话评价：底座已经“有数、有结构、有治理”，但尚未完全达到“事实成熟、自动闭环、经营强引用”的状态。

### 10.2 使用边界

1. `底座可用知识闭环率` 是治理与调用可用性指标，不是业务收入、订单完成、项目验收或工厂运营完成指标。
2. 状态覆盖率可证明“有状态位”，不能证明事实已确认。
3. DQ 可作为事实成熟度参考，但遇到一票否决项时不得进入经营强引用。
4. RAG 安全调用必须满足数据分层、证据等级、敏感信息和 `rag_include` 门禁。
5. 写回缺口关闭必须有来源补齐、人工确认或明确不适用记录，不得由 AI 自动关闭。
6. 本指标进入 KDS 11 池体系时，历史十池运行报告口径应继续保留来源说明；增强账本和缺口悬赏不得替代 KDS 11 池事实底座。

## 11. 硬停止条件

出现以下任一情况时，本台账只能记录为 `blocked` 或 `returned`，不得升级：

1. 把候选资料写成真实业务事实。
2. 把线索写成正式订单、正式收入或正式产值。
3. 把开票统计写成到账收入。
4. 把自购 AI 额度纳入统一收益池、悬赏池或再分配池。
5. 未经确认发布悬赏、冻结资源、结算积分或分配收益。
6. 未经委员会备案或裁决处理重大争议。
7. 未经授权写入真实 KDS API、WAES 放行或业务系统主账。
8. 未经人工确认发布 Brain 页面或升级 SOP 生效。
9. 将本文档或本地镜像写成 `accepted` 或 `integrated` 完成。

## 12. 运行原则

1. 每个执行行必须挂接至少一个 KDS 11 池，不允许增强账本游离。
2. 积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本和贡献账本都是增强账本，不替代 KDS 11 池。
3. 正式收入按到账确认；开票只作为统计、财务和流程口径。
4. 有实际收入的建议才可进入产值类正式贡献；无收入只能进入知识或潜在产值候选。
5. 合作单位自购 AI 额度先自用，不进入统一收益池或悬赏资源池。
6. 一般违规可酌情溯源扣除，重大违规按事实比例或全部扣除，具体由委员会机制处理。
7. AI 只产生候选事实、候选 SOP、候选悬赏和候选写回建议，不替代人工确认、WAES 规则、委员会裁决或业务主账。

## 13. 完成定义

本文完成条件：

1. DKS-038 的 `MCT`、`BAC`、`CTC`、`CLC`、`PPC` 首批对象均有空白执行行。
2. 每行均有状态字段、证据槽、下一步动作和硬边界。
3. 每行均挂接 KDS 11 池或说明其增强账本归属。
4. 明确不得发布悬赏、冻结资源、结算积分、分配收益或写入主账。
5. 明确正式收入、开票统计、自购 AI 额度和潜在产值的边界。
6. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。
7. 明确 `底座可用知识闭环率` 的计算口径、初评边界和不得替代业务事实的约束。

## 14. DKS-040 建议

下一轮建议进入“湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练”，使用脱敏虚拟样例填报少量行，验证字段完整性、退回规则、委员会触发和硬停止条件；仍不得使用真实资料、发布悬赏、结算积分、写入真实 KDS API 或业务主账。
