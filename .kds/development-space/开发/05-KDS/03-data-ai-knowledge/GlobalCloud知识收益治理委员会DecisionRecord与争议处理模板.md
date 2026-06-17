---
doc_id: GPCF-DOC-9B5D646E38
title: GlobalCloud 知识收益治理委员会 DecisionRecord 与争议处理模板
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud知识收益治理委员会DecisionRecord与争议处理模板.md
source_path: 03-data-ai-knowledge/GlobalCloud知识收益治理委员会DecisionRecord与争议处理模板.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 知识收益治理委员会 DecisionRecord 与争议处理模板

日期：2026-06-17
状态：v0.1 受控模板
适用范围：绿色供应链分布式知识系统、KDS 11 池底座、积分池、收益池、知识缺口悬赏、AI 建议、葛化母版、湖北磷材拓厂模板。

## 1. 定位

本文是 `GPCF-KDS-DKS-007` 的专项产物，用于把知识收益治理委员会的多数决、备案、争议处理、扣分追溯、收益分配和潜在产值转正机制固化为可填写、可审计、可回放的记录模板。

本文不替代业务合同、财务制度、法律意见或公司章程。本文只定义 KDS / WAES 中的治理对象、字段和流程。

## 2. 基本原则

1. 用户保留体系治理权、急停权、规则发布权和最终边界设定权。
2. 具体积分、收益、悬赏和争议裁决由委员会按多数决处理。
3. AI 只能生成建议、风险提示、候选事实和 SOP 建议，不得自动裁决。
4. WAES 只确认规则、证据、权限和边界；规则以内可记录，规则以外必须进入人工确认或委员会。
5. KDS 11 池是所有知识、事实、积分、收益和治理动作的事实底座。
6. 自购 AI 额度先自用，不进入统一收益池；贡献或共享额度必须另行备案。
7. 到账后才进入正式收入和收益分配口径；开票用于统计和财务过程口径。

## 3. 委员会对象模型

```text
Committee
  -> CommitteeMember
  -> MeetingRecord
  -> DecisionRecord
  -> DisputeCase
  -> SettlementRecord
  -> ContributionAdjustment
  -> RevenuePoolEntry
  -> KDS 11 池事实对象
```

## 4. 委员会角色

| 角色 | 职责 | 是否投票 | 备注 |
|---|---|---:|---|
| 主持人 | 发起议题、确认会议有效性、组织投票 | 是 | 可由平台或项目指定 |
| KDS 记录人 | 记录议题、证据、表决、结论和回写状态 | 否 | 不参与裁决 |
| WAES 边界审核人 | 审核规则、权限、密级、门禁状态 | 可选 | 涉及边界时建议参与 |
| 项目代表 | 提供项目事实和执行意见 | 是 | 与争议直接相关时需回避 |
| 合作单位代表 | 代表本单位贡献、权益和异议 | 是 | 只参与本单位或被邀请事项 |
| 财务代表 | 确认到账、开票、收益池和财务口径 | 可选 | 涉及收入时必须参与 |
| 质量 / 交付代表 | 确认质量、发货、POD、验收事实 | 可选 | 涉及证据时参与 |
| 外部专家 | 对行业、政策、标准、技术给出意见 | 可选 | 可参与但需备案 |
| 用户治理代表 | 发布边界、触发急停、要求复核 | 否 | 不做具体裁决 |

## 5. 表决规则

| 事项 | 最低表决要求 | 回避规则 | 输出 |
|---|---|---|---|
| 一般积分确认 | 参会投票成员多数决 | 直接提交人回避 | `DecisionRecord` |
| 重大积分扣除 | 参会投票成员多数决 + WAES 边界意见 | 被扣除方可陈述但不投票 | `DecisionRecord` + `ContributionAdjustment` |
| 收益池分配 | 多数决 + 财务代表确认到账 | 直接受益方可陈述但需按规则回避 | `SettlementRecord` |
| 悬赏结算 | 多数决或悬赏发布规则自动结算后备案 | 同一提交竞争者相互回避 | `BountySettlement` |
| 潜在产值转正式产值 | 多数决 + 到账证据 | 直接业务方可陈述 | `RevenuePoolEntry` |
| 密级 / 可见范围争议 | 多数决 + WAES 边界意见 | 涉密责任方按需回避 | `AccessDecision` |
| AI 建议采纳 | 项目负责人确认；重大事项进委员会 | AI 不具备投票资格 | `AISuggestionDecision` |

委员会会议有效性建议满足：

1. 至少 3 名有投票资格成员。
2. 涉及收益时必须有财务代表或财务授权意见。
3. 涉及证据真实性时必须有 WAES 或证据责任人意见。
4. 涉及合作单位权益时，合作单位应被通知并允许提交陈述。
5. 所有表决必须形成可回放记录。

## 6. DecisionRecord 字段模板

| 字段 | 必填 | 说明 |
|---|---:|---|
| decisionId | 是 | `DRC-{类型}-{YYYYMM}-{序号}` |
| decisionType | 是 | POINT / REVENUE / BOUNTY / ACCESS / PENALTY / SOP / AI / POTENTIAL_VALUE |
| sourceObjectRefs | 是 | 关联 `AIS`、`KGR`、`KGB`、`KGS`、订单、证据包、收益池记录等 |
| requestingParty | 是 | 发起单位或人员 |
| affectedParties | 是 | 受影响单位或人员 |
| issueSummary | 是 | 议题摘要 |
| evidenceRefs | 是 | 证据或脱敏索引 |
| waesGateStatus | 是 | pending / governance_recorded / governance_blocked / governance_rejected |
| classificationLevel | 是 | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 |
| proposedDecision | 是 | 候选结论 |
| voteEligibleMembers | 是 | 有投票资格成员清单 |
| recusedMembers | 否 | 回避成员及原因 |
| voteResult | 是 | agree / disagree / abstain 数量 |
| decisionOutcome | 是 | approved / rejected / partially_approved / returned_for_evidence / suspended |
| effectiveDate | 是 | 生效日期 |
| reviewDate | 否 | 复核日期 |
| kdsWritebackRefs | 是 | 写入 KDS 11 池的对象引用 |
| userGovernanceNote | 否 | 用户治理边界、急停或复核要求 |

## 7. DisputeCase 字段模板

| 字段 | 必填 | 说明 |
|---|---:|---|
| disputeId | 是 | `DSP-{类型}-{YYYYMM}-{序号}` |
| disputeType | 是 | POINT / REVENUE / BOUNTY / EVIDENCE / ACCESS / AUTHORITY / CONFIDENTIALITY / PENALTY / POTENTIAL_VALUE |
| sourceDecisionId | 否 | 原 `DecisionRecord` |
| claimant | 是 | 争议发起方 |
| respondent | 是 | 被争议方 |
| disputedObjects | 是 | 关联知识、证据、订单、悬赏、收益池或积分池对象 |
| claimSummary | 是 | 争议主张 |
| responseSummary | 否 | 被争议方回应 |
| evidenceRefs | 是 | 证据或脱敏索引 |
| riskLevel | 是 | normal / major |
| temporaryMeasure | 否 | 冻结、暂停、限制可见、待补证 |
| hearingRecord | 否 | 陈述记录 |
| committeeDecisionId | 否 | 形成的 `DecisionRecord` |
| appealAllowed | 是 | 是否允许复核 |
| finalStatus | 是 | open / in_review / decided / appealed / closed |

## 8. 争议类型与处理

| 争议类型 | 典型场景 | 临时措施 | 最终输出 |
|---|---|---|---|
| POINT | 多人提交同一知识、贡献比例不清 | 冻结候选积分 | 积分确认或比例拆分 |
| REVENUE | 收益池分配比例争议 | 冻结争议份额 | 收益分配记录 |
| BOUNTY | 悬赏提交质量或先后顺序争议 | 暂缓结算 | 悬赏结算记录 |
| EVIDENCE | 证据真实性、完整性或权属争议 | 降级为候选事实 | 证据验收结论 |
| ACCESS | 密级、可见范围、脱敏程度争议 | 先按更高密级保护 | 可见范围决定 |
| AUTHORITY | 是否有权代表单位提交或确认 | 暂停采纳 | 授权确认记录 |
| CONFIDENTIALITY | 涉密信息扩散或披露争议 | 立即限制访问 | 处罚或整改 |
| PENALTY | 一般或重大违规扣分比例争议 | 冻结相关积分 | 扣除 / 复核结论 |
| POTENTIAL_VALUE | 潜在产值贡献是否可追溯 | 保留潜在记录 | 转正、维持或撤销 |

## 9. 扣分与追溯规则

| 等级 | 定义 | 处理原则 |
|---|---|---|
| 一般问题 | 信息不完整、引用错误、轻微误判、未造成重大业务影响 | 酌情溯源扣除，允许补证恢复 |
| 重大违规 | 伪造证据、越权确认、泄密、虚构收入、恶意篡改贡献 | 按事实比例或全部扣除，并可冻结后续收益 |

扣分追溯必须满足：

1. 有明确事实对象和证据。
2. 有受影响积分、收益或潜在产值的范围。
3. 有陈述机会。
4. 有委员会表决记录。
5. 有 KDS 回写和 WAES 边界记录。

## 10. 积分池与收益池写入

所有确认结果统一写入 KDS 11 池底座。

| 池 | 写入对象 | 触发条件 |
|---|---|---|
| KnowledgePool | 知识条目、证据摘要、SOP 建议、行业资料 | 知识验收通过 |
| ContributionPointPool | 候选积分、确认积分、扣分、冻结积分 | 委员会或规则确认 |
| RevenuePool | 到账收入、收益分配、争议冻结份额 | 到账确认后 |
| PotentialValuePool | 潜在产值贡献、转正条件、撤销原因 | 未到账但具有业务价值 |
| BountyPool | 悬赏发布、冻结资源、提交、结算 | 知识缺口悬赏生效 |
| AICreditPool | AI 额度贡献、共享、消耗、兑换 | 非自购额度进入共享或贡献 |
| GovernancePool | 会议、表决、争议、复核、急停 | 任何治理动作 |
| AccessPool | 密级、可见范围、授权、脱敏索引 | 权限变更或争议 |

## 11. 首批模板编号

| 编号 | 对象 | 用途 | 状态 |
|---|---|---|---|
| `DRC-POINT-202606-0001` | 贡献积分确认模板 | 用于知识、证据、SOP 建议贡献确认 | template |
| `DRC-REVENUE-202606-0001` | 收益池分配模板 | 用于到账后的收益分配 | template |
| `DRC-BOUNTY-202606-0001` | 悬赏结算模板 | 用于知识缺口悬赏结算 | template |
| `DRC-PENALTY-202606-0001` | 扣分追溯模板 | 用于一般或重大违规处理 | template |
| `DSP-POINT-202606-0001` | 积分争议模板 | 用于贡献比例争议 | template |
| `DSP-REVENUE-202606-0001` | 收益争议模板 | 用于收益池争议 | template |
| `DSP-ACCESS-202606-0001` | 密级争议模板 | 用于访问和脱敏争议 | template |

## 12. 与葛化和湖北磷材的连接

| 单位 / 线索 | 可进入委员会的事项 | 默认处理 |
|---|---|---|
| 葛化预运营期订单 | OEM 事实责任、POD、质量、金融凭证、转量产批准 | 规则内先记录，争议进委员会 |
| 辽宁远航链路 | 客户确认、样箱反馈、悬赏结算、潜在产值追溯 | 先作为缺口和悬赏处理 |
| 湖北磷材拓厂 | 拓厂评估权重、原料/行业资料可信度、订单线索贡献 | 先计知识和潜在产值，不确认收入 |
| 新工厂复制模板 | 母版复用贡献、区域渠道贡献、建设期知识贡献 | 建立候选积分，待事实成熟确认 |

## 13. DKS-008 建议

下一轮建议建立：

```text
GPCF-KDS-DKS-008：
葛化第一阶段 AI 助手三件套实施清单，定义 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手的知识源、权限、提示词、验收门禁和首批问答场景。
```

## 14. 待用户确认

1. 委员会是否先按 3 至 5 人小组启动，再根据项目扩展？
2. 用户治理代表是否默认只有急停和复核权，不进入具体投票？
3. 收益事项是否必须财务代表参与，否则只能形成候选结论？
4. 重大违规是否需要自动触发临时冻结，等待委员会表决？
5. DKS-008 是否进入葛化 AI 助手三件套实施清单？

本文当前只定义模板，不表示任何委员会已经成立、任何争议已经裁决、任何积分或收益已经确认。
