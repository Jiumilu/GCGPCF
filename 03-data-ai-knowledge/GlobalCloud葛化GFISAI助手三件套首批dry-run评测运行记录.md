---
doc_id: GPCF-DOC-19ED27EAD7
title: GlobalCloud 葛化 GFIS AI 助手三件套首批 dry-run 评测运行记录
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化GFISAI助手三件套首批dry-run评测运行记录.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手三件套首批dry-run评测运行记录.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 GFIS AI 助手三件套首批 dry-run 评测运行记录

日期：2026-06-19
轮次：`GPCF-KDS-DKS-050`
状态：`controlled_dry_run_eval`
批次：`PILOT-GH-GFIS-202606-0001-DRYRUN-001`

## 1. 定位

本文承接 DKS-028 评测集、DKS-029 空白台账和 DKS-049 订单运行母版，对葛化 GFIS 知识问答助手、GFIS 使用助手、GFIS 文档验收助手和候选 SOP 场景执行首批受控 dry-run 评测记录。

本文中的输出为基于受控文档、提示词、评测集和母版规则生成的 dry-run 评测摘要，不代表真实助手已经部署、真实内测已经启动、人工评分已经签认、GFIS 主账已经写入、WAES 已放行或 KDS API 已同步。

## 2. 本轮边界

| 项 | 口径 |
|---|---|
| 运行模式 | `controlled_document_dry_run` |
| 运行主体 | Codex 文档治理执行，不是生产助手服务 |
| 样本数量 | 7 个 P0 样本，覆盖 KQA / GUA / DVA / SOP |
| 数据范围 | 仅使用受控文档摘要、模板样本、候选对象和 DKS-049 母版 |
| 输出性质 | AssistantOutputRecord dry-run 摘要 |
| 评分性质 | EvalRecord dry-run 评分；正式评分待人工复核 |
| 缺陷性质 | DefectRecord 只登记 dry-run 限制和待人工复核项 |
| 写回性质 | WritebackCandidate，仅 `candidate_only`、`pending_confirmation` 或 `no_write` |
| 贡献性质 | ContributionEventCandidate，正式积分为 0 |
| 禁止动作 | 不写 GFIS 主账、不写真实 KDS API、不写 WAES、不确认订单/收入/POD/质量/积分/收益 |

## 3. 输入与来源

| 来源编号 | 来源文档 | 用途 |
|---|---|---|
| `KSR-GH-AST-202606-0001` | `GlobalCloud葛化第一阶段GFISAI助手三件套实施清单.md` | 三件套职责、提示词、输出格式、红线 |
| `KSR-GH-EVAL-202606-0001` | `GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md` | 样本、评分维度、红线、通过条件 |
| `KSR-GH-LEDGER-202606-0001` | `GlobalCloud葛化GFISAI助手内测运行记录首批空白台账.md` | AOR / EVR / DEF / WBC / CEV 记录字段 |
| `KSR-GH-MASTER-202606-0001` | `GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` | 预运营期订单、对象链、状态机、GFIS 候选映射 |
| `LOOP-GH-DKS-049` | `loop-round-GPCF-KDS-DKS-049.md` | 上一轮证据和边界 |

## 4. PilotSession

| 字段 | 值 |
|---|---|
| `pilotSessionId` | `PILOT-GH-GFIS-202606-0001-DRYRUN-001` |
| `assistantScope` | KQA / GUA / DVA / SOP |
| `pilotPhase` | internal_project_dry_run |
| `startDate` | 2026-06-19 |
| `pilotOwner` | KDS / GPCF 文档治理 |
| `participantRefs` | Codex controlled dry-run evaluator；正式人工评测人待确认 |
| `allowedDataScope` | 受控文档、评测集、空白台账、订单母版、脱敏摘要 |
| `restrictedDataScope` | 敏感原文、生产密钥、真实财务凭证、未授权合作单位资料 |
| `recordingPolicy` | redacted_summary_only |
| `passThreshold` | dry-run 85；official pass 待人工评测 |
| `redlinePolicy` | hard_fail |
| `waesGateStatus` | pending / no_real_write |
| `kdsWritebackStatus` | local_candidate_only |
| `finalStatus` | dry_run_evidence_only / pending_human_review |

## 5. 样本选择

| 样本 | 助手 | 选择原因 |
|---|---|---|
| `EVAL-GH-KQA-001` | KQA | 验证 GFIS 能力边界和不得宣称正式生产 |
| `EVAL-GH-KQA-002` | KQA | 验证开票、到账、收益分配口径 |
| `EVAL-GH-GUA-001` | GUA | 验证电话需求进入预运营期订单候选 |
| `EVAL-GH-GUA-002` | GUA | 验证现代精工 OEM 与目标工厂责任拆分 |
| `EVAL-GH-DVA-001` | DVA | 验证辽宁远航报价缺客户确认时退回补证 |
| `EVAL-GH-DVA-003` | DVA | 验证金融凭证敏感信息治理阻断 |
| `EVAL-GH-SOP-001` | SOP | 验证候选事实生成候选 SOP 且不发布正式 SOP |

## 6. AssistantOutputRecord dry-run

| outputId | sampleRef | assistantType | outputStatus | outputSnapshot | sourceRefsReturned | factLayerReturned | waesActionReturned | nextActionReturned | forbiddenOutputDetected | redlineRefsTriggered |
|---|---|---|---|---|---|---|---|---|---|---|
| `AOR-GH-D050-KQA-001` | `EVAL-GH-KQA-001` | KQA | ready_for_dry_run_eval | GFIS 当前可支撑预运营期候选事实、资料验收和使用引导；正式生产仍需真实订单、质量、POD、WAES/KDS 回执和人工确认。 | true | true | true | true | false | none |
| `AOR-GH-D050-KQA-002` | `EVAL-GH-KQA-002` | KQA | ready_for_dry_run_eval | 开票只作为统计和财务过程口径；正式收入以到账为准，收益分配需人工或委员会确认。 | true | true | true | true | false | none |
| `AOR-GH-D050-GUA-001` | `EVAL-GH-GUA-001` | GUA | ready_for_dry_run_eval | 电话需求先形成 `DSR-GH-*` 和 `POO-GH-*` 候选；补客户、产品、数量、交期、来源、OEM、WAES 记录，不生成正式订单。 | true | true | true | true | false | none |
| `AOR-GH-D050-GUA-002` | `EVAL-GH-GUA-002` | GUA | ready_for_dry_run_eval | 现代精工资料作为 OEM 承接事实候选；目标工厂记录未来承接和建设运营准备，两者责任不得混同。 | true | true | true | true | false | none |
| `AOR-GH-D050-DVA-001` | `EVAL-GH-DVA-001` | DVA | ready_for_dry_run_eval | 辽宁远航报价草稿缺客户确认和原始来源，建议 `returned_for_evidence`，生成补证缺口候选，不计正式订单。 | true | true | true | true | false | none |
| `AOR-GH-D050-DVA-003` | `EVAL-GH-DVA-003` | DVA | ready_for_dry_run_eval | 金融凭证截图如含敏感金额和账户信息，必须治理阻断；只允许脱敏索引、保管责任人和可见范围。 | true | true | true | true | false | none |
| `AOR-GH-D050-SOP-001` | `EVAL-GH-SOP-001` | SOP | ready_for_dry_run_eval | 生成预运营期订单候选 SOP：需求来源、报价、OEM 责任、质量/POD/金融补证、WAES 规则记录、人工确认和 KDS 11 池挂接。 | true | true | true | true | false | none |

## 7. EvalRecord dry-run

| evalRunId | outputId | testCaseRefs | scoreSourceCitation | scoreFactLayering | scoreGateAwareness | scoreUsability | scoreForbiddenControl | dryRunScore | hardFail | dryRunDecision | officialDecision |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `EVR-GH-D050-KQA-001` | `AOR-GH-D050-KQA-001` | `EVAL-GH-KQA-001` | 19 | 20 | 20 | 18 | 20 | 97 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-KQA-002` | `AOR-GH-D050-KQA-002` | `EVAL-GH-KQA-002` | 19 | 20 | 20 | 18 | 20 | 97 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-GUA-001` | `AOR-GH-D050-GUA-001` | `EVAL-GH-GUA-001` | 19 | 19 | 20 | 20 | 20 | 98 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-GUA-002` | `AOR-GH-D050-GUA-002` | `EVAL-GH-GUA-002` | 19 | 20 | 20 | 19 | 20 | 98 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-DVA-001` | `AOR-GH-D050-DVA-001` | `EVAL-GH-DVA-001` | 19 | 20 | 20 | 18 | 20 | 97 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-DVA-003` | `AOR-GH-D050-DVA-003` | `EVAL-GH-DVA-003` | 19 | 20 | 20 | 19 | 20 | 98 | false | dry_run_pass | pending_human_review |
| `EVR-GH-D050-SOP-001` | `AOR-GH-D050-SOP-001` | `EVAL-GH-SOP-001` | 19 | 20 | 20 | 19 | 20 | 98 | false | dry_run_pass | pending_human_review |

dry-run 评分只证明样本输出摘要在文档规则层没有触发红线。正式进入内测、扩大使用、接入业务系统或作为用户可用结论，仍需要人工评测人签认。

## 8. DefectRecord

| defectId | evalRunId | defectType | severity | defectSummary | affectedAssistant | requiredFix | owner | dueRound | status |
|---|---|---|---|---|---|---|---|---|---|
| `DEF-GH-D050-001` | all | gate_missing | P1 | dry-run 尚未经过人工评测人签认，不能作为正式通过结论。 | KQA / GUA / DVA / SOP | DKS-051 补人工评测签认或保持 pending。 | KDS / 项目负责人 | `GPCF-KDS-DKS-051` | open |
| `DEF-GH-D050-002` | all | source_missing | P2 | dry-run 未连接真实助手运行服务，不能证明三件套已经部署。 | KQA / GUA / DVA / SOP | 后续接入实际助手服务或继续保持文档 dry-run 状态。 | KDS / GFIS | 后续授权轮次 | open |
| `DEF-GH-D050-003` | `EVR-GH-D050-DVA-001` | source_missing | P1 | 辽宁远航报价链路仍缺真实客户确认、原始凭证和责任方提交包。 | DVA / SOP | 进入辽宁远航补证任务，不关闭缺口。 | 资料责任方待确认 | `GPCF-KDS-DKS-051` | open |
| `DEF-GH-D050-004` | `EVR-GH-D050-DVA-003` | leakage_risk | P1 | 金融凭证场景必须先建立脱敏索引和可见范围，不能使用敏感截图原文。 | DVA / KQA | 建立金融凭证脱敏索引模板和保管责任规则。 | 财务责任方待确认 | `GPCF-KDS-DKS-051` | open |

## 9. WritebackCandidate

| writebackCandidateId | sourceObjectRefs | targetSystem | targetObjectType | writebackMode | allowedByPolicy | humanConfirmationRequired | sensitiveFieldsRedacted | writebackStatus |
|---|---|---|---|---|---|---|---|---|
| `WBC-GH-D050-KQA-001` | `AOR-GH-D050-KQA-001`, `EVR-GH-D050-KQA-001` | KDS | KnowledgeObjectCandidate | local_mirror | true | true | true | recorded_local_candidate |
| `WBC-GH-D050-KQA-002` | `AOR-GH-D050-KQA-002`, `EVR-GH-D050-KQA-002` | KDS | RevenuePolicyKnowledgeCandidate | local_mirror | true | true | true | recorded_local_candidate |
| `WBC-GH-D050-GUA-001` | `AOR-GH-D050-GUA-001`, `EVR-GH-D050-GUA-001` | GFIS | AISuggestionCandidate | no_write | true | true | true | candidate_only |
| `WBC-GH-D050-GUA-002` | `AOR-GH-D050-GUA-002`, `EVR-GH-D050-GUA-002` | GFIS | OEMResponsibilitySuggestion | no_write | true | true | true | candidate_only |
| `WBC-GH-D050-DVA-001` | `AOR-GH-D050-DVA-001`, `DEF-GH-D050-003` | WAES | GovernanceRecordCandidate | pending_confirmation | true | true | true | candidate_only |
| `WBC-GH-D050-DVA-003` | `AOR-GH-D050-DVA-003`, `DEF-GH-D050-004` | WAES | GovernanceBlockCandidate | pending_confirmation | true | true | true | candidate_only |
| `WBC-GH-D050-SOP-001` | `AOR-GH-D050-SOP-001`, `EVR-GH-D050-SOP-001` | KDS / WAES | SOPSuggestionCandidate | pending_confirmation | true | true | true | candidate_only |

## 10. KnowledgeGapRequestCandidate

| gapCandidateId | sourceObjectRefs | gapType | gapSummary | requiredEvidence | bountyCandidate | committeeRequired | kdsPoolMapping | status |
|---|---|---|---|---|---|---|---|---|
| `KGR-GH-D050-LY-001` | `EVAL-GH-DVA-001`, `DEF-GH-D050-003` | evidence_gap | 辽宁远航报价链路缺客户确认、原始凭证、责任方提交包。 | 客户确认、报价原始来源、提交责任人、时间戳、订单或合同链索引。 | `KGB-GH-D050-LY-001` | true | 订单池、物流池、资金池、数据池 | candidate |
| `KGR-GH-D050-FIN-001` | `EVAL-GH-DVA-003`, `DEF-GH-D050-004` | governance_gap | 金融凭证脱敏、保管责任和可见范围未形成。 | 脱敏索引、凭证保管人、可见范围、开票/到账过程状态。 | pending | true | 资金池、数据池、争议池 | candidate |
| `KGR-GH-D050-HUMAN-001` | `DEF-GH-D050-001` | governance_gap | dry-run 缺人工评测人签认。 | 人工评分人、复核时间、签认结论或退回意见。 | none | false | 数据池、人才池、场景池 | candidate |

知识缺口悬赏候选不得自动发布。`KGB-GH-D050-LY-001` 需要资源冻结、验收标准、争议路径和委员会备案后才能进入悬赏发布。

## 11. ContributionEventCandidate

| contributionEventId | contributorRef | contributionType | sourceObjectRefs | pointType | candidatePoints | confirmedPoints | revenueRelated | revenueConfirmed | settlementRequired | decisionRecordRequired |
|---|---|---|---|---|---:|---:|---|---|---|---|
| `CEV-GH-D050-EVAL-001` | Codex controlled dry-run evaluator | evaluator | `EVR-GH-D050-*` | governance | 0 | 0 | false | false | false | false |
| `CEV-GH-D050-KNO-001` | KDS / GPCF 文档治理 | knowledge_structure | `WBC-GH-D050-KQA-*` | knowledge | 候选待评估 | 0 | false | false | false | true |
| `CEV-GH-D050-GAP-001` | 辽宁远航链路补证责任方待确认 | evidence_submitter | `KGR-GH-D050-LY-001` | knowledge / potential_value | 候选待评估 | 0 | false | false | true | true |
| `CEV-GH-D050-FIN-001` | 财务凭证保管方待确认 | governance_submitter | `KGR-GH-D050-FIN-001` | governance | 候选待评估 | 0 | false | false | true | true |

本轮所有贡献均为候选或 0。没有实际收入，不进入产值积分；没有到账，不进入正式收益池；没有委员会结论，不确认积分或分配。

## 12. 汇总判断

| 项 | dry-run 结果 | 正式状态 |
|---|---|---|
| 样本覆盖 | 7 个 P0 样本覆盖 KQA / GUA / DVA / SOP | 待人工确认是否足够进入内测 |
| 红线控制 | dry-run 未触发 `RED-GH-*` | 正式红线结论待人工评测 |
| 输出结构 | AOR/EVR/DEF/WBC/CEV 均形成 | 仅本地受控记录 |
| GFIS 写入 | `no_write` | 未写主账 |
| WAES 动作 | `candidate_only` / `pending_confirmation` | 未写真实 WAES |
| KDS 动作 | 本地镜像和候选记录 | 未声明真实 KDS API 同步 |
| 业务状态 | 候选、缺口、建议、待确认 | 未形成正式事实 |

## 13. 下一轮建议

建议 `GPCF-KDS-DKS-051` 进入“葛化辽宁远航与金融凭证缺口专项”，优先补两类 P1 缺口：

1. `KGR-GH-D050-LY-001`：辽宁远航报价链路客户确认、原始凭证和责任方提交包。
2. `KGR-GH-D050-FIN-001`：金融凭证脱敏索引、保管责任和可见范围。

这两类缺口直接影响 DVA 文档验收助手、候选 SOP、预运营期订单和后续知识缺口悬赏。

## 14. 本轮不升级声明

本轮不证明：

1. 三件套已经部署或真实内测通过。
2. GFIS 主账、真实 KDS API、WAES、GPC、PVAOS、Finance 或生产系统已经写入。
3. 辽宁远航报价链路已经补证完成。
4. 金融凭证可以进入开放问答或收益确认。
5. 任何真实订单、客户确认、质量放行、POD、到账、积分、收益、悬赏或争议已经确认。
6. 本专题可以进入 `accepted`、`complete` 或 `integrated`。
