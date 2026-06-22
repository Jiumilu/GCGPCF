---
doc_id: GPCF-DOC-F8556A98E5
title: GlobalCloud 湖北磷材 SOP 候选写回规则到缺口悬赏与人工确认任务包
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材SOP候选写回规则到缺口悬赏与人工确认任务包.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材SOP候选写回规则到缺口悬赏与人工确认任务包.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材 SOP 候选写回规则到缺口悬赏与人工确认任务包

日期：2026-06-17  
状态：`task_package_candidate`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-037《GlobalCloud 湖北磷材 Brain 知识页评审样例到 SOP 候选写回规则》，把三类 SOP 候选写回规则拆成可分派、可悬赏、可人工确认、可回撤的任务包：

1. 拓厂项目评审前控制点。
2. 行业资料可信来源补证控制点。
3. 订单线索收益边界控制点。

本文不是悬赏发布记录，不是积分结算记录，不是收益分配记录，不是 Brain 页面发布记录，不是 WAES 放行记录，也不是 GFIS、GPC、PVAOS 或任何业务系统的主账写入记录。

## 2. 承接关系

| 来源 | 承接内容 | 本文处理 |
|---|---|---|
| DKS-025 知识缺口悬赏与真实资料回收跟踪台账 | KGR / RRT / KGB / CSR / GCR 对象、状态机和关闭条件 | 复用对象口径，不另建悬赏体系 |
| DKS-035 湖北磷材评审空白台账 | 六类页面候选、发布前问题、退回原因和悬赏候选 | 只选取 DKS-037 已形成控制点的 FEA / IND / ORD 三类先行拆任务 |
| DKS-037 SOP 候选写回规则 | `SCP-HBLC-FEA-202606-0001`、`SCP-HBLC-IND-202606-0001`、`SCP-HBLC-ORD-202606-0001` | 转成人工确认任务、缺口悬赏候选、委员会触发条件和关闭标准 |
| DKS-020 积分收益额度悬赏争议联动规则 | 增强账本必须挂接 KDS 11 池，候选不等于确认 | 保持 candidate / planned / pending 状态，不结算 |

## 3. 任务对象定义

| 对象 | 编号前缀 | 作用 | 当前边界 |
|---|---|---|---|
| ManualConfirmationTask | `MCT` | 把候选 SOP 控制点拆成人工确认动作 | 未确认前不得写回正式字段 |
| BountyActivationCandidate | `BAC` | 把知识缺口转成可讨论的悬赏候选 | 未冻结资源、未委员会确认前不得发布 |
| CommitteeTriggerCandidate | `CTC` | 标识何时进入委员会备案或裁决 | 只登记触发条件，不替代裁决 |
| ClosureCriterion | `CLC` | 定义任务关闭、部分关闭、退回和撤回标准 | 关闭必须有 evidence 和 WAES / 人工记录 |
| PkcParticipationCandidate | `PPC` | 定义个人或合作单位成员可参与的提交入口 | 只作为参与入口候选，不确认个人积分 |

## 4. ManualConfirmationTask

| taskId | linkedControlPointId | taskName | requiredInput | confirmationOwner | waesRequirement | kdsPoolRefs | enhancedLedgerRefs | outputCandidate | status |
|---|---|---|---|---|---|---|---|---|---|
| `MCT-HBLC-FEA-202606-0001` | `SCP-HBLC-FEA-202606-0001` | 拓厂项目来源人工确认 | 拓厂来源索引、区域资料、项目负责人确认、政策或第三方来源摘要 | 湖北磷材项目负责人 / 项目组评审人 | 证据规则、权限规则、发布边界规则 | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 / 悬赏池 | `project_review_candidate_confirmed_by_human` | planned |
| `MCT-HBLC-FEA-202606-0002` | `SCP-HBLC-FEA-202606-0001` | 拓厂项目 KDS 池与增强账本挂接确认 | DKS 11 池挂接、贡献账本、SOP 账本、悬赏池挂接关系 | KDS 记录人 / GPCF 治理方 | KDS 挂接规则、账本不得游离规则 | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 / 悬赏池 / 争议池 | `kds_pool_ledger_mapping_candidate_pass` | planned |
| `MCT-HBLC-IND-202606-0001` | `SCP-HBLC-IND-202606-0001` | 行业资料权威来源人工确认 | 权威来源链接、检索时间、适用范围、来源类型 | 行业资料责任方 / WAES 规则复核人 | 可信来源规则、检索时间规则、适用范围规则 | 政策池 / 数据池 / 场景池 | 贡献账本 / 悬赏池 | `trusted_source_candidate_ready_for_review` | planned |
| `MCT-HBLC-ORD-202606-0001` | `SCP-HBLC-ORD-202606-0001` | 订单线索来源与收益边界确认 | 电话、会议或邮件来源摘要、客户匿名编号、需求时间、线索责任人 | 销售或渠道责任方 / 财务口径复核人 | 收益边界规则、订单线索规则、权限规则 | 订单池 / 产能池 / 资金池 / 数据池 | 潜在产值池 / 贡献账本 / 悬赏池 | `order_lead_candidate_boundary_checked` | planned |
| `MCT-HBLC-ORD-202606-0002` | `SCP-HBLC-ORD-202606-0001` | 潜在产值候选口径确认 | 线索来源、预估范围、不可确认为正式收入的说明、后续开票和到账跟踪字段 | 销售责任方 / 财务联系人 / 委员会条件触发 | 潜在产值规则、到账收入规则、开票统计规则 | 订单池 / 资金池 / 场景池 | 潜在产值池 / 争议池 / 贡献账本 | `potential_value_candidate_tracked_only` | planned |

## 5. BountyActivationCandidate

| bountyActivationId | linkedTaskId | linkedKgrOrIssue | bountyType | suggestedRewardMix | eligibleParticipants | visibility | activationGate | forbiddenSettlement | status |
|---|---|---|---|---|---|---|---|---|---|
| `BAC-HBLC-FEA-202606-0001` | `MCT-HBLC-FEA-202606-0001` | `KGR-HBLC-FEA-202606-0001` / `PPI-HBLC-FEA-202606-0001` | 拓厂来源补证悬赏候选 | 知识积分候选 + SOP 贡献候选；不含自购 AI 额度 | 湖北磷材项目组 / 受邀合作单位 / 项目组授权人员 | directed | 发起方确认悬赏范围、验收标准和资源来源；必要时委员会备案 | 未发布前不得结算积分、收益或额度 | candidate_only |
| `BAC-HBLC-IND-202606-0001` | `MCT-HBLC-IND-202606-0001` | `PPI-HBLC-IND-202606-0001` | 权威来源补证悬赏候选 | 知识积分候选 + 可信来源贡献候选 | 所有授权人员或单位 / 受邀专家 / 资料责任方 | semi_public_or_directed | 权威来源范围、检索时间、适用行业和可信层级规则已记录 | 不得直接确认 T3 或政策适用结论 | candidate_only |
| `BAC-HBLC-ORD-202606-0001` | `MCT-HBLC-ORD-202606-0001` | `PPI-HBLC-ORD-202606-0001` | 订单线索补证悬赏候选 | 知识积分候选 + 渠道贡献候选 + 潜在产值候选；不含正式产值积分 | 销售责任方 / 渠道方 / 受邀合作单位 | directed | 线索来源、客户匿名编号、权限和收益边界已记录 | 无到账不得确认正式收入或正式收益分配 | candidate_only |
| `BAC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | `PPI-HBLC-ORD-202606-0001` | 潜在产值跟踪悬赏候选 | 潜在产值贡献候选 + 后续转正跟踪候选 | 销售责任方 / 财务联系人 / 项目组授权人员 | private_or_directed | 有开票统计或到账跟踪字段，但未到账前保持候选 | 不得以开票替代到账收入 | candidate_only |

## 6. CommitteeTriggerCandidate

| triggerId | linkedObject | triggerCondition | committeeAction | userGovernanceBoundary | status |
|---|---|---|---|---|---|
| `CTC-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | 悬赏奖励、跨单位贡献比例、重大复用争议或拓厂机会收益预期不清 | 备案或多数决裁决 | 用户只保留规则治理权、急停权和体系治理权，不做日常裁决 | planned |
| `CTC-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | 权威来源层级、适用范围或引用权属发生争议 | 确认可信来源规则适用或退回补源 | 用户可调整规则原则，但不替代委员会判断具体归属 | planned |
| `CTC-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | 潜在产值贡献、渠道贡献、收入归属、开票与到账口径发生争议 | 冻结候选贡献，等待到账或证据补齐后裁决 | 用户保留急停和规则边界，不裁决收益比例 | planned |
| `CTC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | 候选记录误写为正式订单、正式收入或 GFIS 主账 | 启动违规评议；一般违规酌情溯源扣除，重大违规按事实比例或全部扣除 | 用户可急停越权写回 | planned |

## 7. ClosureCriterion

| closureId | linkedTaskId | closeAsPass | closeAsPartial | returnCondition | withdrawCondition | evidenceRequired |
|---|---|---|---|---|---|---|
| `CLC-HBLC-FEA-202606-0001` | `MCT-HBLC-FEA-202606-0001` | 来源索引、区域资料、项目负责人确认和 WAES 规则记录齐备 | 仅部分来源齐备，可进入项目组内部候选但不得发布 | 来源缺失、责任主体不清、权限不清 | 来源被证伪或授权撤回 | 来源索引、脱敏摘要、人工确认记录、WAES 记录 |
| `CLC-HBLC-FEA-202606-0002` | `MCT-HBLC-FEA-202606-0002` | KDS 11 池和增强账本挂接完整 | 仅底座池完整但增强账本待补 | 账本游离或池挂接错误 | 发现误挂接造成权限或收益风险 | 挂接表、GPCF 复核记录、KDS 本地镜像记录 |
| `CLC-HBLC-IND-202606-0001` | `MCT-HBLC-IND-202606-0001` | 权威来源链接、检索时间、适用范围和可信层级建议齐备 | 来源齐备但适用范围需继续评估 | 缺权威来源或检索时间 | 来源失效或授权不可用 | 来源索引、检索时间、适用范围、WAES 可信来源记录 |
| `CLC-HBLC-ORD-202606-0001` | `MCT-HBLC-ORD-202606-0001` | 线索来源、客户匿名编号、需求时间、责任人和收益边界齐备 | 有线索但客户匿名编号或责任人待补 | 将线索误写为正式订单、开票或到账收入 | 线索来源撤回或被证伪 | 来源摘要、匿名编号、人工确认、收益边界记录 |
| `CLC-HBLC-ORD-202606-0002` | `MCT-HBLC-ORD-202606-0002` | 潜在产值候选、开票统计和到账跟踪字段均区分清楚 | 有潜在产值候选但暂无开票或到账跟踪 | 以开票替代到账或误入正式收益池 | 线索无效或客户撤回 | 潜在产值说明、开票统计字段、到账跟踪字段、财务口径复核 |

## 8. PkcParticipationCandidate

| participationId | linkedBountyActivationId | participantScope | allowedContribution | restrictedContribution | settlementBoundary |
|---|---|---|---|---|---|
| `PPC-HBLC-FEA-202606-0001` | `BAC-HBLC-FEA-202606-0001` | 湖北磷材项目组、受邀合作单位成员、授权专家 | 提交拓厂来源摘要、区域资料索引、政策来源索引、差异项说明 | 不提交未授权原文、敏感价格、合同原文或个人信息 | 验收前只形成个人贡献候选 |
| `PPC-HBLC-IND-202606-0001` | `BAC-HBLC-IND-202606-0001` | 所有授权人员或单位、受邀专家 | 提交权威来源链接、检索时间、适用范围说明 | 不把非权威资料写成高可信结论 | T3 升级必须 WAES 和人工确认 |
| `PPC-HBLC-ORD-202606-0001` | `BAC-HBLC-ORD-202606-0001` | 销售责任方、渠道方、受邀合作单位成员 | 提交线索来源摘要、客户匿名编号、需求时间、责任主体候选 | 不提交客户实名、未授权合同原文、正式收入声明 | 到账前不得确认正式产值积分或收益分配 |

## 9. AI 服务动作边界

| 场景 | AI 可做 | AI 不可做 |
|---|---|---|
| 任务生成 | 根据 DKS-037 控制点生成任务候选、字段缺口和验收建议 | 自动发布悬赏或分配积分 |
| 材料初审 | 检查来源、字段、脱敏、权限、KDS 池挂接和账本挂接是否完整 | 确认真实来源、真实订单、真实收入或真实业务完成 |
| SOP 建议 | 生成拓厂评审、权威来源补证和订单线索边界的候选 SOP | 使 SOP 正式生效或写入业务主账 |
| 悬赏建议 | 建议悬赏范围、参与对象、验收标准和奖励混合 | 冻结资源、结算积分、发放额度或收益分配 |
| 争议提示 | 标识可能进入委员会的触发条件 | 代替委员会裁决 |

## 10. 任务状态机

```text
task_planned
  -> candidate_assigned
  -> source_submitted_candidate
  -> waes_rule_recorded
  -> human_review_pending
  -> committee_if_needed
  -> closed_or_returned
```

悬赏候选状态机：

```text
bounty_candidate_only
  -> ready_for_committee_or_sponsor
  -> resource_pending_freeze
  -> published_if_confirmed
  -> submission_review
  -> accepted_partial_returned_or_disputed
  -> settlement_after_dispute_period
```

本文只建立 `task_planned` 和 `bounty_candidate_only` 结构，不进入发布、冻结、提交、结算或分配。

## 11. 完成定义

本文完成条件：

1. DKS-037 三个 SOP 候选控制点均拆成人工确认任务。
2. 每个人工确认任务均具备 KDS 11 池挂接、增强账本挂接、WAES 要求和输出候选。
3. 形成知识缺口悬赏候选、委员会触发候选、关闭标准和 PKC 参与候选。
4. 明确自购 AI 额度不进入统一收益池或悬赏资源池。
5. 明确正式收入按到账确认，开票只作为统计、财务和流程口径。
6. 明确 AI 只能建议，不发布悬赏、不结算积分、不裁决争议、不写业务主账。
7. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 12. DKS-039 建议

下一轮建议建立“湖北磷材缺口悬赏与人工确认任务包首批空白执行台账”，把本文 `MCT`、`BAC`、`CTC`、`CLC` 和 `PPC` 对象转成可逐项填报的运行台账，便于后续真实脱敏资料进入时逐项登记。
