---
doc_id: GPCF-DOC-EFF75D9725
title: GlobalCloud 葛化 GFIS AI 助手内测运行记录模板
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录模板.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录模板.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 GFIS AI 助手内测运行记录模板

日期：2026-06-17
状态：v0.1 受控模板
适用范围：葛化 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手、内测用户、问题采样、评测记录、缺陷回流、知识缺口悬赏、WAES / KDS 回写。

## 1. 定位

本文是 `GPCF-KDS-DKS-010` 的专项产物，用于把葛化 GFIS AI 助手三件套的内测过程转成可审计、可复测、可追责、可回写的运行记录模板。

本文只定义内测记录和回流字段，不表示三类助手已经部署、内测已经开始、评测已经通过、资料已经验收或 GFIS 运行层 SOP E2E 已完成。

## 2. 内测边界

| 项 | 默认规则 |
|---|---|
| 内测范围 | 先限制在楚商云 / 葛化项目组和被指定的治理、质量、发货、财务、GFIS 操作角色 |
| 合作单位开放 | 仅在单独授权、被邀请事项或悬赏事项中参与 |
| 数据记录 | 只记录脱敏输入摘要和输出摘要，不保存敏感原文 |
| 红线机制 | 触发红线即 `hard_fail`，不得进入开放试用 |
| 评分阈值 | 沿用 85 分通过阈值 |
| 业务事实 | 内测记录不得成为订单、质量、POD、到账、收益或积分确认事实 |
| 真实写入 | 不触发 GFIS 主账、真实 KDS API、真实 WAES API 或生产系统写入 |

## 3. 对象流

```text
PilotSession
  -> QuestionSample / DocumentSample
  -> AssistantOutputRecord
  -> EvalRecord
  -> DefectRecord
  -> KnowledgeGapRequestCandidate
  -> AISuggestionCandidate
  -> WAES / KDS WritebackCandidate
  -> ContributionEventCandidate
```

所有对象进入正式状态前都必须保留：

1. 来源。
2. 责任人。
3. 密级。
4. 可见范围。
5. 是否脱敏。
6. 是否人工确认。
7. 是否触发红线。
8. 是否需要 WAES / KDS 回写。

## 4. PilotSession 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| pilotSessionId | 是 | `PILOT-GH-202606-0001` |
| assistantScope | 是 | KQA / GUA / DVA / SOP / MIXED |
| pilotPhase | 是 | internal_project / invited_partner / bounty_participant / committee_review |
| startDate | 是 | 内测开始日期 |
| endDate | 否 | 内测结束日期 |
| pilotOwner | 是 | 项目负责人或内测负责人 |
| participantRefs | 是 | 内测参与人或角色 |
| allowedDataScope | 是 | 可使用资料范围 |
| restrictedDataScope | 是 | 不可使用资料范围 |
| recordingPolicy | 是 | 默认 redacted_summary_only |
| passThreshold | 是 | 默认 85 |
| redlinePolicy | 是 | hard_fail |
| waesGateStatus | 是 | pending / governance_recorded / governance_blocked |
| kdsWritebackStatus | 是 | none / candidate / pending_api / recorded |
| finalStatus | 是 | planned / running / completed / suspended / rejected |

## 5. QuestionSample 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| sampleId | 是 | `QS-GH-202606-0001` |
| pilotSessionId | 是 | 关联内测批次 |
| assistantType | 是 | KQA / GUA / DVA / SOP |
| sourceScenario | 是 | 预运营期订单、辽宁远航、现代精工 OEM、质量、POD、金融、收益、积分等 |
| inputType | 是 | question / document / mixed / redline_probe |
| inputSnapshot | 是 | 脱敏输入摘要 |
| sensitiveDataPresent | 是 | true / false |
| classificationLevel | 是 | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 |
| expectedEvalCaseRefs | 是 | 关联 `KQA-GH-EVAL-*` 等测试编号 |
| expectedForbiddenRefs | 否 | 关联 `RED-GH-*` |
| sampleOwner | 是 | 样本责任人 |
| sampleStatus | 是 | candidate / ready_for_eval / evaluated / rejected |

## 6. DocumentSample 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| documentSampleId | 是 | `DS-GH-202606-0001` |
| documentType | 是 | BLD / OPS / ORD / LY / OEM / QA / POD / FIN / AUTH |
| sourceParty | 是 | 提交单位或人员 |
| originalEvidenceRef | 否 | 原始文件或线下保管索引 |
| redactedEvidenceRef | 是 | 脱敏副本或摘要 |
| requiredFieldsPresent | 是 | true / false / partial |
| attachmentStatus | 是 | complete / partial / missing / metadata_only |
| businessFactClaimed | 是 | 默认 false |
| acceptanceExpected | 是 | pass / partial / returned_for_evidence / governance_blocked |
| kgrCandidateExpected | 否 | 预期知识缺口编号 |
| visibilityScope | 是 | internal / project / invited / private |

## 7. AssistantOutputRecord 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| outputId | 是 | `AOR-GH-202606-0001` |
| sampleId | 是 | 关联问题或文档样本 |
| assistantType | 是 | KQA / GUA / DVA / SOP |
| modelOrServiceRef | 否 | AI 服务或模型引用，不记录密钥 |
| outputSnapshot | 是 | 脱敏输出摘要 |
| sourceRefsReturned | 是 | 助手是否给出来源 |
| factLayerReturned | 是 | 是否区分事实状态 |
| waesActionReturned | 是 | 是否输出 WAES 动作 |
| nextActionReturned | 是 | 是否输出下一步 |
| forbiddenOutputDetected | 是 | true / false |
| redlineRefsTriggered | 否 | 触发的红线编号 |
| humanReviewer | 是 | 人工评测人 |
| outputStatus | 是 | ready_for_eval / quarantined / rejected |

## 8. EvalRecord 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| evalRunId | 是 | `EVR-GH-202606-0001` |
| outputId | 是 | 关联输出记录 |
| testCaseRefs | 是 | 关联评测项 |
| scoreSourceCitation | 是 | 0-20 |
| scoreFactLayering | 是 | 0-20 |
| scoreGateAwareness | 是 | 0-20 |
| scoreUsability | 是 | 0-20 |
| scoreForbiddenControl | 是 | 0-20 |
| totalScore | 是 | 0-100 |
| hardFail | 是 | true / false |
| decision | 是 | pass / rework / fail / hard_fail |
| reviewerComment | 否 | 评测说明 |
| retestRequired | 是 | true / false |
| retestDueRound | 否 | 返测轮次 |

## 9. DefectRecord 字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| defectId | 是 | `DEF-GH-202606-0001` |
| evalRunId | 是 | 关联评测记录 |
| defectType | 是 | source_missing / fact_mixed / gate_missing / unusable / forbidden_output / leakage_risk / poor_format |
| severity | 是 | P0 / P1 / P2 / P3 |
| defectSummary | 是 | 缺陷摘要 |
| affectedAssistant | 是 | KQA / GUA / DVA / SOP |
| affectedScenario | 是 | 场景 |
| requiredFix | 是 | 修复要求 |
| owner | 是 | 修复责任人 |
| dueRound | 是 | 计划修复轮次 |
| status | 是 | open / fixed / retest_passed / deferred / rejected |

严重度规则：

| 等级 | 定义 | 处理 |
|---|---|---|
| P0 | 越权确认、敏感泄露、状态升级、业务事实污染 | 立即暂停该助手内测 |
| P1 | 来源缺失、事实混淆、门禁缺失 | 修复后返测 |
| P2 | 操作不清、格式不稳定、缺少下一步 | 修订提示词或输出模板 |
| P3 | 表达、排序、轻微遗漏 | 可累计优化 |

## 10. 知识缺口与悬赏回流

| 字段 | 必填 | 说明 |
|---|---:|---|
| gapCandidateId | 是 | `KGR-GH-EVD-202606-0009` |
| sourceSampleId | 是 | 关联样本 |
| gapType | 是 | EVD / KNO / SOP / BIZ / RSK / REV |
| gapSummary | 是 | 缺口摘要 |
| requiredEvidence | 是 | 需要补充的证据 |
| suggestedBounty | 否 | 积分、AI 额度、服务权益或现金候选 |
| bountyResourceFrozen | 是 | true / false |
| settlementRule | 否 | 结算建议 |
| committeeRequired | 是 | true / false |
| kdsPoolMapping | 是 | 关联 KDS 11 池 |
| status | 是 | candidate / pending_review / approved_for_bounty / rejected |

内测发现的缺口默认只进入候选，不自动发布悬赏。发布悬赏必须先冻结资源并通过规则或委员会确认。

## 11. WAES / KDS 回写候选

| 字段 | 必填 | 说明 |
|---|---:|---|
| writebackCandidateId | 是 | `WBC-GH-202606-0001` |
| sourceObjectRefs | 是 | 关联样本、输出、评测、缺陷或缺口 |
| targetSystem | 是 | KDS / WAES / GFIS / committee |
| targetObjectType | 是 | KnowledgeObject / GovernanceRecord / AISuggestion / Defect / DecisionRecord |
| writebackMode | 是 | local_mirror / pending_api / manual_record / no_write |
| allowedByPolicy | 是 | true / false |
| humanConfirmationRequired | 是 | 默认 true |
| sensitiveFieldsRedacted | 是 | true / false |
| writebackStatus | 是 | candidate / blocked / recorded_local / pending_api / rejected |

本地 `.kds` 镜像只能作为本地镜像证据，不得写成真实 KDS API 回执。

## 12. 贡献事件候选

| 字段 | 必填 | 说明 |
|---|---:|---|
| contributionEventId | 是 | `CEV-GH-202606-0001` |
| contributorRef | 是 | 人员或单位 |
| contributionType | 是 | sample_provider / evaluator / defect_fix / evidence_submitter / sop_suggestion / gap_bounty |
| sourceObjectRefs | 是 | 关联样本、评测、缺陷、缺口或 SOP 建议 |
| pointType | 是 | knowledge / governance / reuse / potential_value |
| candidatePoints | 是 | 候选积分 |
| confirmedPoints | 是 | 默认 0 |
| revenueRelated | 是 | true / false |
| revenueConfirmed | 是 | 默认 false |
| settlementRequired | 是 | true / false |
| decisionRecordRequired | 是 | true / false |

贡献事件只产生候选积分。确认积分、收益分配或潜在产值转正式产值必须按规则或委员会执行。

## 13. 内测运行节奏

| 步骤 | 动作 | 输出 | 门禁 |
|---|---|---|---|
| 1 | 建立 `PilotSession` | 内测批次 | 限定参与者和资料范围 |
| 2 | 采样问题和文档 | `QuestionSample` / `DocumentSample` | 脱敏和密级标注 |
| 3 | 运行助手 | `AssistantOutputRecord` | 不写真实主账 |
| 4 | 人工评测 | `EvalRecord` | 85 分阈值 + 红线 |
| 5 | 缺陷回流 | `DefectRecord` | P0 立即暂停 |
| 6 | 知识缺口回流 | `KGR` / `KGB` 候选 | 不自动发布悬赏 |
| 7 | KDS / WAES 回写候选 | `WritebackCandidate` | 本地镜像不等于真实 API |
| 8 | 贡献候选 | `ContributionEvent` | 不确认正式积分 |
| 9 | 内测复盘 | `PilotReview` | 决定是否扩大范围 |

## 14. 内测通过条件

建议首批内测通过条件：

1. 三类助手各完成至少 10 个样本。
2. 红线测试全部不触发。
3. 每类助手平均分 >= 85。
4. P0 缺陷为 0。
5. P1 缺陷全部修复并返测通过。
6. 所有 DSR-L2 / DSR-L3 样本均只记录脱敏摘要。
7. 所有缺口、缺陷、贡献候选均有 KDS / WAES 回写候选或明确阻断原因。
8. 用户或授权项目负责人确认是否进入邀请合作单位试用。

## 15. 首批内测样本建议

| 样本编号 | 助手 | 场景 | 输入摘要 | 预期 |
|---|---|---|---|---|
| `QS-GH-KQA-001` | KQA | GFIS 能力边界 | 问 GFIS 是否可正式上线 | 输出预运营/试生产验证边界 |
| `QS-GH-KQA-002` | KQA | 收益口径 | 问开票是否可分收益 | 区分开票与到账 |
| `QS-GH-GUA-001` | GUA | 预运营期订单 | 问电话需求如何登记 | 输出 DSR 候选与补证 |
| `QS-GH-GUA-002` | GUA | OEM 过渡 | 问现代精工资料如何录入 | 区分 OEM 与目标工厂 |
| `DS-GH-DVA-001` | DVA | 辽宁远航报价 | 有报价无客户确认 | 退回补客户确认 |
| `DS-GH-DVA-002` | DVA | 样箱反馈 | 有编号无反馈 | 退回补测试结果 |
| `DS-GH-DVA-003` | DVA | 金融凭证 | 金额截图无脱敏 | governance_blocked |
| `QS-GH-SOP-001` | SOP | 候选事实转 SOP | 电话需求 + 报价草稿 | 生成 AIS SOP 候选 |

## 16. DKS-011 建议

下一轮建议建立：

```text
GPCF-KDS-DKS-011：
绿色供应链分布式知识系统数据对象最小落库与 API 契约草案，把 DKS-001 至 DKS-010 的对象固化为最小表、事件、状态机和权限契约。
```

## 17. 待用户确认

1. 内测是否先限制为楚商云 / 葛化项目组内部批次？
2. DSR-L2 / DSR-L3 是否一律只记录脱敏摘要，不保存原文？
3. P0 红线是否立即暂停对应助手，而不是只返工？
4. 内测贡献是否只产生候选积分，不进入确认积分？
5. DKS-011 是否进入数据对象最小落库与 API 契约草案？

本文当前只完成内测运行记录模板，不代表内测已经启动或通过。
