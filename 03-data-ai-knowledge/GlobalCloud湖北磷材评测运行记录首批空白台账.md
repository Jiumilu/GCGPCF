---
doc_id: GPCF-DOC-C8062E9E2A
title: GlobalCloud 湖北磷材评测运行记录首批空白台账
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材评测运行记录首批空白台账.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材评测运行记录首批空白台账.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材评测运行记录首批空白台账

日期：2026-06-17  
状态：`planned_empty_run_ledger`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-030 的湖北磷材首批知识对象运行空白台账和 DKS-031 的湖北磷材拓厂评估与知识源评测集，将 FEA、RAW、IND、ORD、TPL、MIX 六类评测样本转成可填报的运行记录空白台账。

本文只建立运行记录字段、状态、评分口径、红线记录、缺口回流、写回候选和贡献候选的空白结构，不表示：

- 湖北磷材已经提交真实资料；
- 已经执行真实评测；
- 拓厂项目、原料采购、行业适用、订单、合同、POD、到账或收益已经确认；
- GFIS 深度运行已经启动；
- Brain 知识页已经发布；
- 积分、收益、额度、悬赏、争议或 SOP 已经生效；
- 已完成真实 KDS API、WAES API 或业务系统写入。

## 2. 运行总规则

| 项 | 规则 |
|---|---|
| 运行批次 | `PILOT-HBLC-KDS-202606-0001` |
| 默认状态 | `planned_empty_run_ledger` |
| 样本来源 | DKS-031 `EVS-HBLC-*` / `EVAL-HBLC-*` |
| 可填报对象 | FEA / RAW / IND / ORD / TPL / MIX |
| 评分口径 | 100 分制，运行时人工评分 |
| 通过阈值 | 单样本 >= 85 且无红线 |
| 红线机制 | 任一 `RED-HBLC-*` 触发即 `hard_fail` |
| AI 输出边界 | 只生成候选摘要、候选缺口、候选写回和候选贡献 |
| KDS 边界 | 本地镜像、候选台账和运行记录不得写成真实 KDS API 回执 |
| WAES 边界 | WAES 只记录规则、边界、证据要求和例外，不替代业务事实确认 |
| 收益边界 | 到账前不得确认正式收入；开票仅作为统计和财务过程口径 |

## 3. RunSession 空白台账

| runSessionId | evalBatchId | runScope | runOwner | participantRefs | inputStatus | outputStatus | waesGateStatus | kdsWritebackStatus | finalStatus |
|---|---|---|---|---|---|---|---|---|---|
| `RUN-HBLC-EVAL-202606-0001` | `PILOT-HBLC-KDS-202606-0001` | FEA / RAW / IND / ORD / TPL / MIX | KDS / GPCF 治理负责人 | 湖北磷材项目组、WAES、Brain、必要委员会 | waiting_source | planned | pending | candidate / no_write | planned |

## 4. EvaluationRunRecord 空白台账

| runRecordId | evalSampleId | linkedObjectRefs | inputSummary | outputSummary | sourceRefs | trustLayer | factStatus | manualScore | redlineStatus | defectRefs | nextAction | runStatus |
|---|---|---|---|---|---|---|---|---:|---|---|---|---|
| `ERR-HBLC-FEA-202606-0001` | `EVS-HBLC-FEA-001` | `HBLC-FEA-202606-0001`, `FEA-HBLC-202606-0001` | 待填 | 待填 | 待填 | T0 | waiting_source | 0 | not_checked | TBD | 补目标区域、工厂条件、政策来源和项目负责人确认 | planned |
| `ERR-HBLC-RAW-202606-0001` | `EVS-HBLC-RAW-001` | `HBLC-RAW-202606-0001`, `KSO-HBLC-RAW-202606-0001` | 待填 | 待填 | 待填 | T0 | waiting_source | 0 | not_checked | TBD | 补原料来源索引、质量指标来源和责任主体 | planned |
| `ERR-HBLC-IND-202606-0001` | `EVS-HBLC-IND-001` | `HBLC-IND-202606-0001`, `KSO-HBLC-IND-202606-0001` | 待填 | 待填 | 待填 | T0 / T3 candidate | waiting_source | 0 | not_checked | TBD | 补权威来源、检索时间、适用范围和 WAES 规则记录 | planned |
| `ERR-HBLC-ORD-202606-0001` | `EVS-HBLC-ORD-001` | `HBLC-ORD-202606-0001`, `KSO-HBLC-ORD-202606-0001` | 待填 | 待填 | 待填 | T0 | waiting_source | 0 | not_checked | TBD | 补客户确认、数量、规格、交期和责任主体 | planned |
| `ERR-HBLC-TPL-202606-0001` | `EVS-HBLC-TPL-001` | `HBLC-TPL-202606-0001`, `RTC-HBLC-TPL-202606-0001` | 待填 | 待填 | `GH-DKS-029` structure reference | T1 | candidate | 0 | not_checked | TBD | 补湖北磷材差异项、复用边界和人工作业点 | planned |
| `ERR-HBLC-MIX-202606-0001` | `EVS-HBLC-MIX-001` | `PILOT-HBLC-KDS-202606-0001` | 待填 | 待填 | DKS-030 / DKS-031 | T1 | candidate | 0 | not_checked | TBD | 检查 KDS 11 池、增强账本、WAES 和 LOOP evidence | planned |

## 5. RedlineRunRecord 空白台账

| redlineRunId | runRecordId | redlineRef | triggerSummary | severity | decisionOwner | correctionRequired | status |
|---|---|---|---|---|---|---|---|
| `RLR-HBLC-FEA-202606-0001` | `ERR-HBLC-FEA-202606-0001` | `RED-HBLC-001` | 待检查 | major | WAES / 委员会候选 | true | planned |
| `RLR-HBLC-RAW-202606-0001` | `ERR-HBLC-RAW-202606-0001` | `RED-HBLC-002` | 待检查 | major | WAES / 委员会候选 | true | planned |
| `RLR-HBLC-IND-202606-0001` | `ERR-HBLC-IND-202606-0001` | `RED-HBLC-003` | 待检查 | major | WAES | true | planned |
| `RLR-HBLC-ORD-202606-0001` | `ERR-HBLC-ORD-202606-0001` | `RED-HBLC-004` | 待检查 | major | WAES / 委员会候选 | true | planned |
| `RLR-HBLC-TPL-202606-0001` | `ERR-HBLC-TPL-202606-0001` | `RED-HBLC-005` | 待检查 | major | WAES / 委员会候选 | true | planned |
| `RLR-HBLC-MIX-202606-0001` | `ERR-HBLC-MIX-202606-0001` | `RED-HBLC-007` | 待检查 | major | 委员会候选 | true | planned |

## 6. GapBountyRunCandidate 空白台账

| gapRunId | runRecordId | gapCandidateRef | bountyCandidateRef | gapSummary | requiredEvidence | proposedRewardType | resourceFreezeRequired | committeeRequired | status |
|---|---|---|---|---|---|---|---|---|---|
| `GBR-HBLC-FEA-202606-0001` | `ERR-HBLC-FEA-202606-0001` | `KGR-HBLC-FEA-202606-0001` | `KGB-HBLC-FEA-202606-0001` | 待运行确认 | 目标区域、工厂条件、政策来源、负责人确认 | 知识积分或 AI 服务候选 | true | true | planned |
| `GBR-HBLC-RAW-202606-0001` | `ERR-HBLC-RAW-202606-0001` | `KGR-HBLC-RAW-202606-0002` | `KGB-HBLC-RAW-202606-0002` | 待运行确认 | 原料来源、供应商脱敏摘要、质量或价格来源 | 知识积分候选 | true | true | planned |
| `GBR-HBLC-IND-202606-0001` | `ERR-HBLC-IND-202606-0001` | `KGR-HBLC-IND-202606-0003` | `KGB-HBLC-IND-202606-0003` | 待运行确认 | 政策/标准来源、适用范围、检索时间 | 知识积分候选 | false | false | planned |
| `GBR-HBLC-ORD-202606-0001` | `ERR-HBLC-ORD-202606-0001` | `KGR-HBLC-ORD-202606-0004` | `KGB-HBLC-ORD-202606-0004` | 待运行确认 | 客户需求来源、报价或意向索引、责任主体 | 潜在产值贡献候选 | true | true | planned |
| `GBR-HBLC-TPL-202606-0001` | `ERR-HBLC-TPL-202606-0001` | `KGR-HBLC-TPL-202606-0005` | `KGB-HBLC-TPL-202606-0005` | 待运行确认 | 结构复用清单、湖北磷材差异项、WAES 规则记录 | 知识积分或 SOP 贡献候选 | true | true | planned |

## 7. WritebackRunCandidate 空白台账

| writebackRunId | runRecordId | writebackCandidateRef | targetSystem | targetObjectType | writebackMode | humanConfirmationRequired | waesGateRequired | writebackStatus |
|---|---|---|---|---|---|---|---|---|
| `WBR-HBLC-FEA-202606-0001` | `ERR-HBLC-FEA-202606-0001` | `WBC-HBLC-FEA-202606-0001` | KDS / WAES | ExpansionAssessmentCandidate | candidate_only | true | true | planned |
| `WBR-HBLC-RAW-202606-0001` | `ERR-HBLC-RAW-202606-0001` | `WBC-HBLC-RAW-202606-0001` | KDS | RawMaterialKnowledgeCandidate | candidate_only | true | true | planned |
| `WBR-HBLC-IND-202606-0001` | `ERR-HBLC-IND-202606-0001` | `WBC-HBLC-IND-202606-0001` | KDS / Brain | IndustryKnowledgePageCandidate | candidate_only | true | true | planned |
| `WBR-HBLC-ORD-202606-0001` | `ERR-HBLC-ORD-202606-0001` | `WBC-HBLC-ORD-202606-0001` | KDS / WAES | OrderLeadCandidate | candidate_only | true | true | planned |
| `WBR-HBLC-TPL-202606-0001` | `ERR-HBLC-TPL-202606-0001` | `WBC-HBLC-TPL-202606-0001` | KDS / Brain | FactoryReplicationTemplateCandidate | pending_confirmation | true | true | planned |
| `WBR-HBLC-MIX-202606-0001` | `ERR-HBLC-MIX-202606-0001` | TBD | GPCF / WAES | GovernanceCheckRecordCandidate | no_write | true | true | planned |

## 8. ContributionRunCandidate 空白台账

| contributionRunId | runRecordId | contributionEventRef | contributorRef | contributionType | pointType | candidatePoints | confirmedPoints | revenueRelated | revenueConfirmed | status |
|---|---|---|---|---|---|---:|---:|---|---|---|
| `CRN-HBLC-FEA-202606-0001` | `ERR-HBLC-FEA-202606-0001` | `CEV-HBLC-FEA-202606-0001` | 待确认 | project_source_submitter | knowledge / potential_value | 待评估 | 0 | false | false | planned |
| `CRN-HBLC-RAW-202606-0001` | `ERR-HBLC-RAW-202606-0001` | `CEV-HBLC-RAW-202606-0001` | 待确认 | raw_material_source_submitter | knowledge | 待评估 | 0 | false | false | planned |
| `CRN-HBLC-IND-202606-0001` | `ERR-HBLC-IND-202606-0001` | `CEV-HBLC-IND-202606-0001` | 待确认 | industry_source_submitter | knowledge | 待评估 | 0 | false | false | planned |
| `CRN-HBLC-ORD-202606-0001` | `ERR-HBLC-ORD-202606-0001` | `CEV-HBLC-ORD-202606-0001` | 待确认 | order_lead_submitter | potential_value / channel | 待评估 | 0 | false | false | planned |
| `CRN-HBLC-TPL-202606-0001` | `ERR-HBLC-TPL-202606-0001` | `CEV-HBLC-TPL-202606-0001` | 待确认 | sop_template_contributor | knowledge / reuse | 待评估 | 0 | false | false | planned |

## 9. KDS 11 池运行挂接检查

| runRecordId | 必挂底座池 | 增强账本候选 | 当前状态 |
|---|---|---|---|
| `ERR-HBLC-FEA-202606-0001` | 装备池、产能池、政策池、数据池、场景池 | SOP 账本、贡献账本、积分池、悬赏池 | pass_for_template |
| `ERR-HBLC-RAW-202606-0001` | 原料池、数据池、资金池、场景池 | 贡献账本、积分池、悬赏池、争议池 | pass_for_template |
| `ERR-HBLC-IND-202606-0001` | 政策池、数据池、场景池 | 贡献账本、积分池、悬赏池 | pass_for_template |
| `ERR-HBLC-ORD-202606-0001` | 订单池、资金池、原料池、数据池、场景池 | 潜在产值池、收益池、贡献账本、争议池 | pass_for_template |
| `ERR-HBLC-TPL-202606-0001` | 装备池、产能池、人才池、数据池、场景池 | SOP 账本、贡献账本、积分池、权限账本 | pass_for_template |
| `ERR-HBLC-MIX-202606-0001` | 数据池、场景池 | 贡献账本、争议池、SOP 账本 | pass_for_template |

## 10. 填报与确认规则

1. `inputSummary` 只能填脱敏摘要、来源索引或资料包编号。
2. `sourceRefs` 必须指向来源索引、受控资料包或明确写明来源不足。
3. `manualScore` 默认 0，真实评分必须由人工评测人填写。
4. `redlineStatus` 默认 `not_checked`，真实运行时必须逐项检查 `RED-HBLC-*`。
5. `confirmedPoints` 默认 0，委员会确认前不得填非 0。
6. `revenueConfirmed` 默认 false，到账前不得改为 true。
7. 自购 AI 额度只可计量自用，不进入统一收益池。
8. 所有 `writebackStatus` 默认 planned，不得写成 completed。
9. Brain 只能消费已授权的事实摘要和结构，不得替代 KDS 事实主存。
10. WAES 只确认规则、证据、权限、边界和例外，不替代业务主账确认。

## 11. 完成定义

本台账完成条件：

1. 六类运行记录均具备统一编号。
2. 运行记录覆盖输入摘要、输出摘要、来源、可信级别、事实状态、人工评分、红线、缺陷、下一步和运行状态。
3. 缺口悬赏、写回和贡献候选均能追溯到 DKS-030 / DKS-031 对象。
4. 所有增强账本候选均挂接至少一个 KDS 11 底座池。
5. 所有真实评分、正式积分、正式收益和真实写回保持未确认。
6. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 12. DKS-033 建议

下一轮建议建立“湖北磷材真实资料接收任务包与人工评测演练”，在不接收 DSR-L3 原文、不调用真实外部 API、不写真实业务系统的前提下，定义资料接收清单、脱敏规则、人工评分流程、WAES 门禁记录和 Brain 知识页候选生成边界。
