---
doc_id: GPCF-DOC-BA893D6FF7
title: GlobalCloud 葛化 GFIS AI 助手内测运行记录首批空白台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录首批空白台账.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录首批空白台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 GFIS AI 助手内测运行记录首批空白台账

日期：2026-06-17
状态：`planned_empty_ledger`
批次：`PILOT-GH-GFIS-202606-0001`

## 1. 定位

本文承接 DKS-028 的首批评测样本，将葛化 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手与候选 SOP 场景转成可填报、可复测、可追责的首批内测运行空白台账。

本文只建立内测记录结构和首批样本编号，不表示：

- 三类助手已经正式上线；
- 内测已经开始或通过；
- 助手已经产生真实输出；
- 已收到、验收或归档真实首批资料；
- 已完成 GFIS、KDS、WAES 或生产系统真实写入；
- 已确认任何积分、收益、产值、到账、订单、POD、金融凭证或 SOP 生效。

## 2. 状态规则

| 状态 | 含义 | 边界 |
|---|---|---|
| `ready_for_eval` | 样本可用于后续内测 | 不代表已经运行 |
| `pending_run` | 等待助手输出 | 不得补写虚构输出 |
| `pending_review` | 等待人工评测或委员会确认 | 不得自动通过 |
| `candidate_only` | 只形成候选事实、候选 SOP 或候选贡献 | 不进入主事实账 |
| `no_write` | 不写入 GFIS、KDS、WAES 或生产系统 | 可留作治理记录 |
| `planned_empty_ledger` | 仅完成空白台账搭建 | 不形成业务事实 |

## 3. PilotSession 台账

| pilotSessionId | assistantScope | pilotPhase | startDate | pilotOwner | participantRefs | allowedDataScope | restrictedDataScope | passThreshold | waesGateStatus | kdsWritebackStatus | finalStatus |
|---|---|---|---|---|---|---|---|---:|---|---|---|
| `PILOT-GH-GFIS-202606-0001` | KQA / GUA / DVA / SOP | internal_project | 待确认 | GPC / KDS 治理负责人 | 楚商云、葛化项目组指定角色 | 脱敏摘要、模板样本、候选资料包、受控评测集 | 敏感原文、未授权合作单位资料、生产密钥、正式财务凭证原文 | 85 | pending | candidate / no_write | planned_empty_ledger |

## 4. QuestionSample 台账

| sampleId | assistantType | sourceScenario | inputType | inputSnapshot | classificationLevel | linkedEvalCase | linkedObjectRefs | sampleStatus | humanReviewer |
|---|---|---|---|---|---|---|---|---|---|
| `QS-GH-KQA-001` | KQA | GFIS 能力边界 | question | GFIS 是否已可支撑葛化正式生产 | DSR-L1 | `EVAL-GH-KQA-001` | `RPK-GH-ORD-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-KQA-002` | KQA | 收益口径 | question | 客户已开票是否可进入收益分配 | DSR-L1 | `EVAL-GH-KQA-002` | 订单池、资金池、收益池候选 | ready_for_eval | 待确认 |
| `QS-GH-KQA-003` | KQA | 辽宁远航报价链路 | question | 辽宁远航报价是否可算正式订单 | DSR-L1 | `EVAL-GH-KQA-003` | `RPK-GH-LY-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-GUA-001` | GUA | 预运营期订单登记 | question | 电话出现客户需求后如何登记 | DSR-L1 | `EVAL-GH-GUA-001` | `SOPC-GH-ORD-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-GUA-002` | GUA | OEM 过渡资料录入 | question | 现代精工生产资料如何录入 | DSR-L1 | `EVAL-GH-GUA-002` | `RPK-GH-ORD-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-GUA-003` | GUA | POD 与发货资料补录 | question | 发货后只有物流截图时 POD 如何补 | DSR-L2 | `EVAL-GH-GUA-003` | `RPK-GH-LY-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-SOP-001` | SOP | 候选事实转 SOP | mixed | 电话需求、报价草稿、OEM 承接说明 | DSR-L2 | `EVAL-GH-SOP-001` | `SOPC-GH-ORD-202606-0001` | ready_for_eval | 待确认 |
| `QS-GH-SOP-002` | SOP | 辽宁远航补证链路 | mixed | 辽宁远航报价、发货线索、POD 缺口 | DSR-L2 | `EVAL-GH-SOP-002` | `SOPC-GH-LY-202606-0001` | ready_for_eval | 待确认 |

## 5. DocumentSample 台账

| documentSampleId | documentType | sourceParty | redactedEvidenceRef | requiredFieldsPresent | attachmentStatus | businessFactClaimed | acceptanceExpected | kgrCandidateExpected | visibilityScope | sampleStatus |
|---|---|---|---|---|---|---|---|---|---|---|
| `DS-GH-DVA-001` | LY / ORD | 辽宁远航链路提交方 | 待提交脱敏摘要 | partial | metadata_only | false | returned_for_evidence | `KGR-GH-LY-202606-0001` | project | ready_for_eval |
| `DS-GH-DVA-002` | QA / OPS | 样箱反馈提交方 | 待提交脱敏摘要 | partial | metadata_only | false | partial / returned_for_evidence | `KGR-GH-LY-202606-0001` | project | ready_for_eval |
| `DS-GH-DVA-003` | FIN | 财务或金融凭证保管方 | 待提交脱敏索引 | partial | metadata_only | false | governance_blocked | 待生成金融凭证脱敏缺口候选 | private / committee | ready_for_eval |
| `DS-GH-DVA-004` | QA / AUTH | 质量或门禁资料提交方 | 待提交脱敏摘要 | partial | metadata_only | false | returned_for_evidence | 待确认 | project | ready_for_eval |

## 6. AssistantOutputRecord 空白台账

| outputId | sampleRef | assistantType | outputStatus | outputSnapshot | sourceRefsReturned | factLayerReturned | waesActionReturned | nextActionReturned | forbiddenOutputDetected | redlineRefsTriggered | humanReviewer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `AOR-GH-KQA-001` | `QS-GH-KQA-001` | KQA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-KQA-002` | `QS-GH-KQA-002` | KQA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-KQA-003` | `QS-GH-KQA-003` | KQA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-GUA-001` | `QS-GH-GUA-001` | GUA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-GUA-002` | `QS-GH-GUA-002` | GUA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-GUA-003` | `QS-GH-GUA-003` | GUA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-DVA-001` | `DS-GH-DVA-001` | DVA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-DVA-002` | `DS-GH-DVA-002` | DVA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-DVA-003` | `DS-GH-DVA-003` | DVA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-DVA-004` | `DS-GH-DVA-004` | DVA | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-SOP-001` | `QS-GH-SOP-001` | SOP | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |
| `AOR-GH-SOP-002` | `QS-GH-SOP-002` | SOP | pending_run | 待运行 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待记录 | 待确认 |

## 7. EvalRecord 空白台账

| evalRunId | outputId | testCaseRefs | scoreSourceCitation | scoreFactLayering | scoreGateAwareness | scoreUsability | scoreForbiddenControl | totalScore | hardFail | decision | retestRequired |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `EVR-GH-KQA-001` | `AOR-GH-KQA-001` | `EVAL-GH-KQA-001` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-KQA-002` | `AOR-GH-KQA-002` | `EVAL-GH-KQA-002` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-KQA-003` | `AOR-GH-KQA-003` | `EVAL-GH-KQA-003` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-GUA-001` | `AOR-GH-GUA-001` | `EVAL-GH-GUA-001` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-GUA-002` | `AOR-GH-GUA-002` | `EVAL-GH-GUA-002` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-GUA-003` | `AOR-GH-GUA-003` | `EVAL-GH-GUA-003` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-DVA-001` | `AOR-GH-DVA-001` | `EVAL-GH-DVA-001` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-DVA-002` | `AOR-GH-DVA-002` | `EVAL-GH-DVA-002` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-DVA-003` | `AOR-GH-DVA-003` | `EVAL-GH-DVA-003` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-DVA-004` | `AOR-GH-DVA-004` | `EVAL-GH-DVA-004` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-SOP-001` | `AOR-GH-SOP-001` | `EVAL-GH-SOP-001` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |
| `EVR-GH-SOP-002` | `AOR-GH-SOP-002` | `EVAL-GH-SOP-002` | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | 待评 | pending_review | 待评 |

## 8. DefectRecord 预留台账

| defectId | evalRunId | defectType | severity | defectSummary | affectedAssistant | requiredFix | owner | dueRound | status |
|---|---|---|---|---|---|---|---|---|---|
| `DEF-GH-KQA-001` | `EVR-GH-KQA-001` | 待触发 | 待定 | 待运行后填写 | KQA | 待定 | 待确认 | 待确认 | not_created |
| `DEF-GH-GUA-001` | `EVR-GH-GUA-001` | 待触发 | 待定 | 待运行后填写 | GUA | 待定 | 待确认 | 待确认 | not_created |
| `DEF-GH-DVA-001` | `EVR-GH-DVA-001` | 待触发 | 待定 | 待运行后填写 | DVA | 待定 | 待确认 | 待确认 | not_created |
| `DEF-GH-SOP-001` | `EVR-GH-SOP-001` | 待触发 | 待定 | 待运行后填写 | SOP | 待定 | 待确认 | 待确认 | not_created |

## 9. KnowledgeGapRequestCandidate 台账

| gapCandidateId | sourceSampleId | gapType | gapSummary | requiredEvidence | suggestedBounty | bountyResourceFrozen | committeeRequired | kdsPoolMapping | status |
|---|---|---|---|---|---|---|---|---|---|
| `KGR-GH-ORD-202606-0001` | `QS-GH-GUA-001` | field_gap | 预运营期订单字段与责任拆分缺口 | 客户需求来源、客户确认、产品、数量、交期、责任主体 | 积分或 AI 服务候选 | false | true | 订单池、产能池、数据池、场景池 | candidate |
| `KGR-GH-LY-202606-0001` | `DS-GH-DVA-001` | evidence_gap | 辽宁远航报价、发货、POD、回款链路缺口 | 客户确认、原始凭证、发货证据、POD、到账或开票过程资料 | 积分或 AI 服务候选 | false | true | 订单池、运力池、资金池、数据池 | candidate |
| `KGR-GH-FIN-202606-0001` | `DS-GH-DVA-003` | governance_gap | 金融凭证脱敏、可见范围和保管责任缺口 | 脱敏索引、保管责任人、可见范围、复核规则 | 待委员会确认 | false | true | 资金池、数据池、争议池 | candidate |

## 10. WritebackCandidate 台账

| writebackCandidateId | sourceObjectRefs | targetSystem | targetObjectType | writebackMode | allowedByPolicy | humanConfirmationRequired | sensitiveFieldsRedacted | writebackStatus |
|---|---|---|---|---|---|---|---|---|
| `WBC-GH-KQA-001` | `QS-GH-KQA-001`, `EVR-GH-KQA-001` | KDS | KnowledgeObjectCandidate | candidate_only | true | true | true | planned |
| `WBC-GH-GUA-001` | `QS-GH-GUA-001`, `EVR-GH-GUA-001` | GFIS | AISuggestionCandidate | no_write | true | true | true | planned |
| `WBC-GH-DVA-001` | `DS-GH-DVA-001`, `EVR-GH-DVA-001` | WAES | GovernanceRecordCandidate | candidate_only | true | true | true | planned |
| `WBC-GH-DVA-003` | `DS-GH-DVA-003`, `EVR-GH-DVA-003` | WAES | GovernanceBlockCandidate | candidate_only | true | true | true | planned |
| `WBC-GH-SOP-001` | `QS-GH-SOP-001`, `EVR-GH-SOP-001` | KDS / Brain | SOPDisplayCandidate | pending_confirmation | true | true | true | planned |
| `WBC-GH-SOP-002` | `QS-GH-SOP-002`, `EVR-GH-SOP-002` | KDS / WAES | EvidenceRecoverySopCandidate | pending_confirmation | true | true | true | planned |

## 11. ContributionEventCandidate 台账

| contributionEventId | contributorRef | contributionType | sourceObjectRefs | pointType | candidatePoints | confirmedPoints | revenueRelated | revenueConfirmed | settlementRequired | decisionRecordRequired |
|---|---|---|---|---|---:|---:|---|---|---|---|
| `CEV-GH-SAMPLE-001` | 样本提供方待确认 | sample_provider | `QS-GH-*`, `DS-GH-*` | knowledge | 待评估 | 0 | false | false | false | true |
| `CEV-GH-EVAL-001` | 评测人待确认 | evaluator | `EVR-GH-*` | governance | 待评估 | 0 | false | false | false | true |
| `CEV-GH-GAP-001` | 补证方待确认 | evidence_submitter | `KGR-GH-*` | knowledge / potential_value | 待评估 | 0 | false | false | true | true |
| `CEV-GH-SOP-001` | SOP 建议方待确认 | sop_suggestion | `WBC-GH-SOP-*` | reuse / knowledge | 待评估 | 0 | false | false | true | true |

有实际收入的事项才可进入正式产值贡献。到账作为正式收入确认口径，开票作为统计和财务过程口径。未到账事项只可记录为知识贡献、资料贡献、渠道贡献或潜在产值贡献候选。

## 12. KDS 11 底座池挂接

| 对象 | 必挂底座池 | 增强账本 |
|---|---|---|
| 预运营期订单样本 | 订单池、产能池、数据池、场景池 | SOP 账本、贡献账本、潜在产值池 |
| 辽宁远航链路样本 | 订单池、运力池、资金池、数据池 | SOP 账本、贡献账本、收益池候选 |
| OEM 过渡资料样本 | 订单池、产能池、装备池、数据池 | 责任区分账本、SOP 账本 |
| 质量、发货、POD、金融凭证样本 | 订单池、资金池、数据池 | 文档验收账本、贡献账本、争议池 |
| 知识缺口与悬赏候选 | 数据池、人才池、场景池 | 悬赏池、积分池、额度池 |

积分池、收益池、额度池、悬赏池、争议池、潜在产值池、SOP 账本、贡献账本均为增强账本，不替代 KDS 11 底座池。

## 13. 运行检查清单

| 检查项 | 通过规则 | 当前状态 |
|---|---|---|
| 样本编号完整 | QS / DS / AOR / EVR / WBC / CEV 均有编号 | pass_for_template |
| 真实输出留空 | 所有助手输出均为待运行 | pass_for_template |
| 评分留空 | 所有评分均为待评 | pass_for_template |
| 敏感数据控制 | 只记录脱敏摘要或索引 | pass_for_template |
| 写回控制 | 仅 candidate_only、pending_confirmation 或 no_write | pass_for_template |
| 收益控制 | 不确认正式收入或收益分配 | pass_for_template |
| 贡献控制 | 只记录候选积分，confirmedPoints 为 0 | pass_for_template |

## 14. 红线暂停规则

后续真实内测中出现以下任一情形，必须暂停相关样本或助手范围：

- 将候选事实写成正式事实；
- 将预运营期订单写成建设期订单或正式订单；
- 混同葛化目标工厂与 OEM 承接方事实责任；
- 将报价、意向、电话、会议或邮件直接计为正式收入；
- 将开票直接作为收益分配依据；
- 将自购 AI 额度写入统一收益池；
- 未经确认直接确认积分、收益、扣罚、争议或 SOP 生效；
- 输出敏感原文、金融凭证、客户资料或未授权合作单位资料；
- 将本地 KDS 镜像写成真实 KDS API 已同步。

## 15. 完成定义

本台账完成条件：

1. 首批样本、资料、输出、评分、缺陷、缺口、写回、贡献候选均具备统一编号。
2. 所有样本均保持待运行或待评状态。
3. 所有写回均保持候选或不写入状态。
4. 所有贡献均保持候选，正式确认值为 0。
5. 所有对象均挂接 KDS 11 底座池或明确待补挂接。
6. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 16. DKS-030 建议

下一轮建议建立“葛化 GFIS AI 助手首批内测执行与评分记录表”，在人工确认可运行后，对本文样本逐条补入：

- 助手脱敏输出摘要；
- 来源引用；
- 事实分层；
- 门禁动作；
- 人工评分；
- 缺陷记录；
- 缺口、悬赏、写回和贡献候选；
- 是否允许进入下一批内测。
