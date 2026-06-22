---
doc_id: GPCF-DOC-89872D1387
title: GlobalCloud 绿色供应链分布式知识系统数据对象最小落库与 API 契约草案
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统数据对象最小落库与API契约草案.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链分布式知识系统数据对象最小落库与 API 契约草案

日期：2026-06-20
轮次：`GPCF-KDS-DKS-059`
状态：`controlled_no_write_api_contract`

## 1. 状态边界

本文定义 P0 阶段最小数据对象、存储边界和 API 契约。本文是 no-write / candidate-only 契约草案，不代表数据库已迁移、接口已上线、GFIS 已写入、WAES 已裁决、KDS API 已真实同步或业务事实已确认。

P0 默认写入模式：

| 模式 | 说明 |
|---|---|
| `no_write` | 只读、问答、评测、字段校验 |
| `candidate_only` | 只创建候选对象或本地受控文档记录 |
| `metadata_only` | 只记录编号、摘要、哈希、保管人、密级和状态 |
| `sandbox_ready` | 未来可进入沙箱，但需另行授权 |

禁止模式：

| 模式 | 说明 |
|---|---|
| `production_write` | P0 禁止 |
| `approved_business_fact` | P0 禁止 |
| `accepted_integrated` | P0 禁止 |

## 2. 最小数据表草案

| 表 | 主键 | 用途 | P0 写入模式 |
|---|---|---|---|
| `knowledge_objects` | `object_id` | 统一知识对象 | candidate_only |
| `knowledge_sources` | `source_id` | 来源登记 | candidate_only |
| `knowledge_evidence` | `evidence_id` | 证据登记 | metadata_only / candidate_only |
| `assistant_outputs` | `assistant_output_id` | GFIS 三件套输出 | candidate_only |
| `assistant_evals` | `eval_id` | 三件套评测 | candidate_only |
| `assistant_defects` | `defect_id` | 评测缺陷 | candidate_only |
| `fact_candidates` | `fact_candidate_id` | AI 候选事实 | candidate_only |
| `sop_candidates` | `sop_candidate_id` | 候选 SOP | candidate_only |
| `writeback_candidates` | `writeback_candidate_id` | 候选写回 | no_write / candidate_only |
| `pre_operation_orders` | `pre_operation_order_id` | 预运营期订单候选 | candidate_only |
| `oem_responsibility_records` | `oem_record_id` | OEM 责任拆分 | candidate_only |
| `quality_evidence_records` | `quality_record_id` | 质量证据索引 | metadata_only |
| `delivery_pod_records` | `pod_record_id` | 发货/POD 索引 | metadata_only |
| `finance_evidence_indexes` | `finance_index_id` | 金融凭证脱敏索引 | sensitive_metadata_only |
| `gap_records` | `gap_id` | 知识缺口 | candidate_only |
| `bounty_records` | `bounty_id` | 悬赏候选 | candidate_only |
| `contribution_records` | `contribution_id` | 积分贡献候选 | candidate_only |
| `revenue_records` | `revenue_id` | 收益候选 | candidate_only |
| `quota_records` | `quota_id` | AI 额度计量 | candidate_only |
| `decision_records` | `decision_id` | 委员会或人工决议 | draft / candidate_only |
| `dispute_records` | `dispute_id` | 争议 | candidate_only |
| `waes_gate_records` | `waes_gate_id` | 门禁结果 | candidate_only |
| `rag_admission_records` | `rag_id` | RAG 准入 | candidate_only |
| `loop_records` | `loop_id` | LOOP evidence | controlled_document |

## 3. 通用 API 请求字段

所有 P0 API 请求必须包含：

| 字段 | 要求 |
|---|---|
| `requestId` | 唯一请求编号 |
| `actorRef` | 调用人或系统，必须可追溯 |
| `sourceProject` | 来源项目 |
| `sourceUnit` | 来源单位 |
| `operationMode` | `no_write` / `candidate_only` / `metadata_only` |
| `sourceRefs` | 来源引用 |
| `evidenceRefs` | 证据引用，可为空但必须说明缺口 |
| `classificationLevel` | DSR-L0 至 DSR-L3 |
| `trustLevel` | T0 至 T5 |
| `basePoolRefs` | 至少一个 KDS 底座池 |
| `waesGateIntent` | 是否需要 WAES |
| `humanConfirmationRequired` | 默认 true |
| `committeeRequired` | 触及收益、重大违规、争议、潜在产值转正式产值时 true |
| `forbiddenOperations` | 禁止动作 |
| `loopEvidenceRef` | LOOP 记录 |

所有响应必须包含：

| 字段 | 要求 |
|---|---|
| `resultStatus` | `accepted_as_candidate` / `returned_for_evidence` / `blocked` / `no_write_completed` |
| `createdObjectRefs` | 本地候选对象编号，P0 不代表业务主账 |
| `waesRequiredActions` | WAES 或人工下一步 |
| `promotionBlockers` | 不能升级原因 |
| `ragAdmission` | 默认 `repair_required` 或 `blocked`，除非证据充分 |
| `auditRefs` | LOOP / Harness / 文档引用 |

## 4. GFIS 三件套 API 契约

### 4.1 知识问答

`POST /api/dks/v0/gfis/knowledge-qa`

请求追加字段：

| 字段 | 说明 |
|---|---|
| `question` | 用户问题 |
| `allowedKnowledgeRefs` | 允许使用的知识对象 |
| `assistantType` | 固定 `gfis_knowledge_qa` |

响应追加字段：

| 字段 | 说明 |
|---|---|
| `answerSummary` | 回答摘要 |
| `sourceCoverage` | 来源覆盖 |
| `factStatus` | controlled / candidate / missing_evidence / forbidden_to_confirm |
| `redlineHit` | 是否触发红线 |
| `assistantOutputRef` | `AST-GH-KQA-*` |

P0 副作用：只生成 `AssistantOutputRecord` 候选，不写 GFIS。

### 4.2 使用助手

`POST /api/dks/v0/gfis/usage-guide`

请求追加字段：

| 字段 | 说明 |
|---|---|
| `userScenario` | 预运营期订单、OEM、质量、POD、金融凭证等 |
| `targetGfisObject` | GFIS 候选对象 |
| `writeIntent` | P0 必须为 `no_write` 或 `candidate_only` |

响应追加字段：

| 字段 | 说明 |
|---|---|
| `guidedSteps` | 操作步骤 |
| `requiredFields` | 必填字段 |
| `requiredEvidence` | 必要证据 |
| `waesGate` | 门禁建议 |
| `writebackCandidateRef` | 如有，生成 `WBC-*` |

P0 副作用：只生成指导和候选写回，不写 GFIS 主账。

### 4.3 文档验收助手

`POST /api/dks/v0/gfis/document-acceptance`

请求追加字段：

| 字段 | 说明 |
|---|---|
| `documentType` | 建设、运营、订单、辽宁远航、OEM、质量、POD、金融 |
| `documentMetadata` | 文档元数据 |
| `redactionProfile` | 脱敏策略 |

响应追加字段：

| 字段 | 说明 |
|---|---|
| `acceptanceStatus` | pass_candidate / partial / returned_for_evidence / blocked |
| `missingFields` | 缺字段 |
| `gapRecordRefs` | 缺口 |
| `sopCandidateRefs` | 候选 SOP |
| `sensitiveHandling` | metadata_only / sealed / blocked |

P0 副作用：只生成验收候选、缺口和 SOP 建议。

## 5. 候选事实、SOP 与写回 API

| API | 用途 | P0 结果 |
|---|---|---|
| `POST /api/dks/v0/fact-candidates` | 创建候选事实 | `FAC-*` |
| `POST /api/dks/v0/sop-candidates` | 创建候选 SOP | `SOP-*` |
| `POST /api/dks/v0/writeback-candidates` | 创建候选写回 | `WBC-*` |
| `POST /api/dks/v0/waes/gates/check` | 本地门禁检查 | `WGR-*` |
| `POST /api/dks/v0/rag/admission/check` | RAG 准入检查 | `RAG-*` |

写回候选必须包含：

| 字段 | 要求 |
|---|---|
| `targetSystem` | GFIS / GPC / KDS / WAES / PVAOS / Finance |
| `targetObject` | 目标对象类型 |
| `writeMode` | P0 固定 `no_write` 或 `candidate_only` |
| `requiredApprovals` | 人工、WAES、委员会 |
| `businessFactCreated` | P0 必须 false |
| `productionWriteExecuted` | P0 必须 false |

## 6. 葛化链路 API 契约

| API | 对象 | P0 状态 |
|---|---|---|
| `POST /api/dks/v0/gehu/pre-operation-orders` | `POO-GH-*` | candidate_only |
| `POST /api/dks/v0/gehu/liaoning-yuanhang/gaps` | `KGR-GH-LY-*` | open |
| `POST /api/dks/v0/gehu/oem-responsibility` | `OEM-GH-MJ-*` | responsibility_candidate |
| `POST /api/dks/v0/gehu/quality-gates` | `QER-GH-*` | metadata_only |
| `POST /api/dks/v0/gehu/pod-gates` | `POD-GH-*` | metadata_only |
| `POST /api/dks/v0/gehu/finance-indexes` | `FEI-GH-*` | sensitive_metadata_only |

这些 API 不发送外部通知，不写 GFIS，不写 Finance，不生成正式订单。

## 7. 湖北磷材 API 契约

| API | 对象 | P0 状态 |
|---|---|---|
| `POST /api/dks/v0/hblc/factory-expansion-assessments` | `FEA-HBLC-*` | candidate_only |
| `POST /api/dks/v0/hblc/raw-material-knowledge` | `KNO-HBLC-RAW-*` | candidate_only |
| `POST /api/dks/v0/hblc/industry-knowledge` | `KNO-HBLC-IND-*` | candidate_only |
| `POST /api/dks/v0/hblc/order-knowledge` | `KNO-HBLC-ORD-*` | candidate_only |
| `POST /api/dks/v0/hblc/factory-copy-template` | `SOP-HBLC-TPL-*` | template_candidate |

湖北磷材 P0 不做 GFIS 深度，不生成真实订单、采购、原料价格事实或收益事实。

## 8. 增强治理账本 API

| API | 对象 | P0 状态 |
|---|---|---|
| `POST /api/dks/v0/ledger/contributions` | `CTR-*` | candidate |
| `POST /api/dks/v0/ledger/revenue` | `REV-*` | candidate |
| `POST /api/dks/v0/ledger/quota` | `QUO-*` | registered |
| `POST /api/dks/v0/ledger/bounties` | `KGB-*` | bounty_candidate |
| `POST /api/dks/v0/ledger/disputes` | `DSP-*` | open |
| `POST /api/dks/v0/committee/decisions` | `DEC-*` | draft |

收益 API 必须区分：

| 字段 | 说明 |
|---|---|
| `invoiceAmount` | 统计和财务过程口径 |
| `cashReceivedAmount` | 到账口径 |
| `formalRevenueAllowed` | 只有到账和确认后可 true |
| `allocationAllowed` | 只有人工或委员会确认后可 true |

AI 额度 API 必须区分：

| 字段 | 说明 |
|---|---|
| `quotaType` | platform / self_purchased / contributed / shared / reward |
| `poolEntryAllowed` | 自购额度必须 false |
| `usageMeter` | 使用计量 |
| `beneficiaryUnit` | 受益单位 |

## 9. WAES 与 RAG Gate 响应

WAES Gate 统一结果：

| 结果 | 含义 |
|---|---|
| `governance_recorded` | 规则内记录 |
| `manual_confirmation_required` | 需人工确认 |
| `committee_review_required` | 需委员会 |
| `blocked` | 阻断 |
| `repair_required` | 补证后再试 |

RAG 统一结果：

| 结果 | 含义 |
|---|---|
| `safe` | 可强引用 |
| `limited` | 有限引用 |
| `repair_required` | 需补证 |
| `blocked` | 禁止引用 |
| `sensitive_metadata_only` | 仅元数据 |

## 10. 验证口径

P0 API 契约验证必须确认：

1. 所有请求都包含来源、状态、证据或缺口、责任主体和 LOOP 引用。
2. 所有响应都包含 `promotionBlockers`。
3. 所有写回候选的 `productionWriteExecuted=false`。
4. 所有收益候选未到账时 `formalRevenueAllowed=false`。
5. 所有自购额度 `poolEntryAllowed=false`。
6. 所有 LLM 分析默认不得进入 `safe`。
7. 所有 DSR-L3 对象默认 `sensitive_metadata_only` 或 `blocked`。
