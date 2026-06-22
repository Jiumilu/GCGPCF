---
doc_id: GPCF-DOC-1CF8B46A53
title: GlobalCloud 葛化 GFIS AI 助手内测问答与资料回收包联动规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测问答与资料回收包联动规则.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测问答与资料回收包联动规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 GFIS AI 助手内测问答与资料回收包联动规则

## 1. 定位

本文定义葛化第一阶段三类 GFIS AI 助手在内测问答、使用引导、文档验收过程中，如何联动 DKS-025/DKS-026 已建立的知识缺口、资料回收包、候选 SOP 与 KDS/WAES 门禁。

本文只建立受控规则与候选记录结构，不表示：

- 葛化 GFIS AI 助手已经正式上线；
- 已经收到真实首批资料；
- 已经完成 GFIS、KDS 或 WAES 的真实写回；
- 已经确认任何积分、收益、产值、订单收入或 SOP 生效状态。

## 2. 适用助手

| 助手 | 内测代号 | 核心作用 | 输出边界 |
|---|---:|---|---|
| GFIS 知识问答助手 | KQA | 根据 KDS 可见知识、资料回收包与候选 SOP 回答业务问题 | 输出答案、来源引用、缺口候选、资料回收包引用；不得确认事实 |
| GFIS 使用助手 | GUA | 引导人员按 GFIS、KDS、WAES 标准流程填报字段与提交资料 | 输出字段建议、下一步动作、责任口径提示；不得替代人工提交 |
| GFIS 文档验收助手 | DVA | 对建设、运营、订单、质量、发货、POD、金融凭证、门禁资料进行候选验收 | 输出通过/部分通过/退回/阻断建议；不得完成最终验收 |

## 3. 联动对象

| 对象 | 编号示例 | 来源 | 用途 | 状态边界 |
|---|---|---|---|---|
| 知识缺口 | KGR-GH-ORD-202606-0001 | DKS-025 | 表达葛化订单运行母版缺口 | 未经确认不得转事实 |
| 资料回收任务 | RRT-GH-ORD-202606-0001 | DKS-025 | 形成资料回收动作 | 只代表任务，不代表资料已收齐 |
| 资料回收包 | RPK-GH-ORD-202606-0001 | DKS-026 | 约束字段、证据、验收口径 | 未验收前不得进入主事实账 |
| 候选 SOP | SOPC-GH-ORD-202606-0001 | DKS-026 | 形成 SOP 草案与写回建议 | 必须经 KDS/WAES/人工确认 |
| 内测问答链路 | AILR-GH-202606-0001 | DKS-027 | 连接问题、资料、缺口、候选 SOP | 只记录候选链路 |
| 缺口回流记录 | IGR-GH-202606-0001 | DKS-027 | 将内测发现回流到知识缺口或悬赏 | 委员会确认前不计正式积分 |

## 4. 首批联动范围

葛化 GFIS 内测第一阶段优先覆盖：

- 建设资料；
- 工厂运营资料；
- 订单资料；
- 辽宁远航链路；
- 现代精工 OEM 过渡资料；
- 质量、发货、POD、金融凭证、门禁资料。

湖北磷材并行线本轮只作为复制参考，不进入葛化 GFIS 深度内测。湖北磷材的拓厂项目知识库、原料/行业/订单知识库、新工厂复制模板，可在后续复用本规则中的资料回收包、候选 SOP、缺口回流、贡献候选结构。

## 5. 问答到资料回收包映射

| 场景 | 触发问题/动作 | 优先引用资料包 | 关联缺口 | 候选 SOP | 助手动作 |
|---|---|---|---|---|---|
| 预运营期订单启动 | 电话、会议或邮件出现客户需求 | RPK-GH-ORD-202606-0001 | KGR-GH-ORD-202606-0001 | SOPC-GH-ORD-202606-0001 | KQA 解释流程，GUA 引导建档，DVA 验收需求来源证据 |
| 目标工厂与 OEM 承接方并行记录 | 同一订单同时涉及葛化目标工厂与现代精工 | RPK-GH-ORD-202606-0001 | KGR-GH-ORD-202606-0001 | SOPC-GH-ORD-202606-0001 | GUA 强制区分事实责任、履约责任、证据责任 |
| 辽宁远航链路报价与交付 | 出现报价、承运、发货、POD、回款材料 | RPK-GH-LY-202606-0001 | KGR-GH-LY-202606-0001 | SOPC-GH-LY-202606-0001 | KQA 回答链路口径，DVA 检查 POD/发货/金融凭证 |
| 质量/门禁资料缺失 | 文件缺少来源、责任单位、时间、签章或业务对象 | 对应 RPK | 对应 KGR | 对应 SOPC | DVA 退回或阻断，不进入主事实账 |
| 建设期到预运营期切换 | 工厂未投产但订单或客户需求已开始 | RPK-GH-ORD-202606-0001 | KGR-GH-ORD-202606-0001 | SOPC-GH-ORD-202606-0001 | GUA 使用“预运营期订单”口径，不使用建设期订单口径 |

## 6. 内测记录结构

### 6.1 PilotSessionLinkRecord

| 字段 | 示例 | 说明 |
|---|---|---|
| pilotSessionId | PILOT-GH-GFIS-202606-0001 | 内测批次编号 |
| pilotScope | 葛化 GFIS 三类助手第一阶段 | 内测范围 |
| state | planned | planned / running / closed |
| assistantTypes | KQA, GUA, DVA | 参与助手 |
| linkedPackages | RPK-GH-ORD-202606-0001, RPK-GH-LY-202606-0001 | 关联资料包 |
| linkedSopCandidates | SOPC-GH-ORD-202606-0001, SOPC-GH-LY-202606-0001 | 关联候选 SOP |
| writebackMode | no_write | no_write / candidate_only / pending_confirmation |
| owner | GPC | 治理责任 |

### 6.2 AssistantQuestionToRecoveryPackageMap

| 字段 | 示例 | 说明 |
|---|---|---|
| questionId | QS-GH-KQA-001 | 问答样本编号 |
| assistantType | KQA | KQA/GUA/DVA |
| businessScenario | 预运营期订单启动 | 场景 |
| sourceTrigger | 电话纪要/会议纪要/邮件/第三方资料 | 需求起点 |
| linkedRpk | RPK-GH-ORD-202606-0001 | 资料包 |
| linkedKgr | KGR-GH-ORD-202606-0001 | 缺口 |
| linkedSopc | SOPC-GH-ORD-202606-0001 | 候选 SOP |
| answerStatus | candidate | candidate / needs_evidence / rejected |
| evidenceRequired | true | 是否必须补证 |

### 6.3 RecoveryPackageFeedbackRecord

| 字段 | 示例 | 说明 |
|---|---|---|
| feedbackId | RPF-GH-ORD-202606-0001 | 资料包反馈编号 |
| linkedRpk | RPK-GH-ORD-202606-0001 | 资料包 |
| missingFields | 客户确认、履约责任、POD、回款凭证 | 缺失字段 |
| validationResult | partial | pass / partial / returned / blocked |
| suggestedAction | 补齐客户确认与责任区分后再提交 | 建议动作 |
| waesRuleImpact | within_rule | within_rule / rule_review_required |
| humanConfirmationRequired | true | 是否人工确认 |

### 6.4 WritebackCandidateRoutingRecord

| 字段 | 示例 | 说明 |
|---|---|---|
| writebackCandidateId | WCR-GH-ORD-202606-0001 | 写回候选编号 |
| sourceQuestionId | QS-GH-SOP-001 | 来源问题或文档 |
| targetSystem | KDS / GFIS / WAES | 目标系统 |
| targetLedger | SOP 账本 / 贡献账本 / 订单池 | 目标账本或底座池 |
| basePoolRefs | 订单池, 产能池, 数据池 | 必须挂接 KDS 11 底座池 |
| writebackLevel | candidate_only | candidate_only / human_record / pending_api |
| confirmationGate | KDS + WAES + 人工 | 门禁 |
| currentState | pending_confirmation | 当前状态 |

### 6.5 InnerTestGapReturnRecord

| 字段 | 示例 | 说明 |
|---|---|---|
| gapReturnId | IGR-GH-202606-0001 | 缺口回流编号 |
| sourceAssistant | KQA | 来源助手 |
| sourceObject | QS-GH-KQA-001 | 来源对象 |
| gapType | field_gap | field_gap / evidence_gap / sop_gap / authority_gap |
| suggestedKgr | KGR-GH-ORD-202606-0001 | 可关联或新建缺口 |
| bountyCandidate | KGB-GH-ORD-202606-0001 | 可进入悬赏候选 |
| contributionCandidate | true | 是否形成贡献候选 |
| committeeRequired | true | 是否需要委员会确认 |

## 7. KDS 11 底座池挂接规则

所有 AI 生成的候选事实、候选 SOP、候选积分、缺口回流、收益分配依据，都必须挂接至少一个 KDS 11 底座池。

| 场景 | 必挂底座池 | 可选增强账本 |
|---|---|---|
| 预运营期订单 | 订单池、产能池、数据池 | SOP 账本、贡献账本、潜在产值池 |
| 辽宁远航链路 | 订单池、运力池、资金池、数据池 | SOP 账本、贡献账本、收益池 |
| 质量/发货/POD/金融凭证 | 订单池、资金池、数据池 | 文档验收账本、贡献账本 |
| OEM 过渡资料 | 订单池、产能池、装备池、数据池 | 责任区分账本、SOP 账本 |
| 知识缺口与悬赏 | 数据池、人才池、场景池 | 悬赏池、积分池、争议池 |

积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本、贡献账本均为增强账本，不替代 KDS 11 底座池。

## 8. WAES 与人工确认边界

| 动作 | AI 可做 | WAES 可做 | 人工/委员会必须做 |
|---|---|---|---|
| 问答解释 | 生成候选答案与来源引用 | 校验规则口径 | 确认业务采用 |
| GFIS 填报建议 | 提示字段、缺证、责任区分 | 确认是否在规则内 | 提交、修改、签认 |
| 文档验收建议 | 给出 pass/partial/returned/blocked 建议 | 识别规则内/需复核 | 最终验收与归档 |
| 候选 SOP | 生成流程草案、控制点、写回建议 | 确认规则约束 | 审批、发布、废止 |
| 积分/收益候选 | 识别知识、产值、渠道、资料贡献 | 校验规则与口径 | 委员会裁决与备案 |
| 重大违规 | 标记疑点与证据链 | 触发复核规则 | 委员会决定扣除比例或全部扣除 |

WAES 在规则以内只记录，不替代人工确认。规则外、重大影响、跨单位争议、积分/收益分配、违规扣除、正式 SOP 生效，必须进入人工或委员会流程。

## 9. 贡献与收益候选口径

- 有实际收入的事项才可进入正式产值贡献；到账作为正式收入口径，开票作为统计和财务过程口径。
- 未形成实际收入的事项只能进入知识贡献、资料贡献、潜在产值贡献或渠道贡献候选。
- 合作单位自购 AI 额度先自用，不进入统一收益池。
- 统一积分池、收益池、额度池、悬赏池、争议池、潜在产值池必须挂接 KDS 11 底座池，作为未来收益、系统收益、业务收益分配参考。
- 委员会可按阶段、项目、市场情况调整不同积分权重与兑换系数，并形成备案记录。

## 10. 红线

以下情形不得由 AI 自动通过：

- 无来源、无责任单位、无业务对象、无时间戳的材料；
- 把预运营期订单误写为建设期订单；
- 未区分目标工厂与 OEM 承接方事实责任；
- 将报价、意向、渠道线索直接计为正式收入；
- 将自购 AI 额度计入统一收益池；
- 未经授权引用合作单位不可见资料；
- 未经 KDS/WAES/人工确认直接写入主事实账；
- 未经委员会确认直接确认积分、收益、扣罚或争议结果。

## 11. DKS-027 完成定义

本轮完成条件：

- 建立 GFIS 三类助手与 RPK/KGR/SOPC 的联动规则；
- 建立内测问答、资料验收、写回候选、缺口回流记录结构；
- 明确 KDS 11 底座池与增强账本挂接规则；
- 明确 WAES、人工、委员会确认边界；
- 纳入 LOOP 轮次记录；
- 通过本轮受控文档、KDS 镜像、防污染、TOKEN、LOOP 文档门禁检查。

## 12. 下一轮建议

DKS-028 建议进入“葛化 GFIS AI 助手首批问答与文档验收评测集实化”，将现有空白评测集补齐为可执行样本，包括：

- KQA 问答样本；
- GUA 使用引导样本；
- DVA 文档验收样本；
- 预运营期订单样本；
- 辽宁远航链路样本；
- OEM 过渡责任区分样本；
- 质量/发货/POD/金融凭证/门禁资料样本；
- 对应评分、缺口、资料回收、候选 SOP、人工确认字段。
