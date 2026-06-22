---
doc_id: GPCF-DOC-2F3CC2EAA1
title: GC-Knowledge Fabric 核心对象关系与最小字段契约
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-核心对象关系与最小字段契约.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-核心对象关系与最小字段契约.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 核心对象关系与最小字段契约

日期：2026-06-20  
状态：`draft`  

## 1. 目标

本文档定义 GC-Knowledge Fabric P0 阶段核心对象关系和最小字段契约，用于约束后续 OKF YAML、JSON Schema、KDS v2 表结构、WAES Gate、KWE 工单、GFIS 写回沙箱、Harness evidence 和 LOOP 记录。

本文档不代表数据库已创建，也不代表 API 已实现。

## 2. 核心关系图

```text
SourceRecord
  -> EvidenceRecord
  -> KnowledgeObject
  -> FactCandidate / SOPCandidate / GapRecord
  -> WAESGateResult
  -> KWEWorkItem / ConfirmationWorkpack
  -> ConfirmationRecord / DecisionRecord
  -> WritebackCandidate / ContributionRecord / RevenueRecord
  -> HarnessEvidenceRecord / LOOPRecord
```

关系说明：

| 上游 | 下游 | 关系 |
|---|---|---|
| SourceRecord | EvidenceRecord | 来源产生或支撑证据 |
| EvidenceRecord | KnowledgeObject | 证据绑定知识对象 |
| KnowledgeObject | FactCandidate | 知识对象可派生候选事实 |
| KnowledgeObject | SOPCandidate | 知识对象可派生候选 SOP |
| KnowledgeObject | GapRecord | 缺来源、缺证据、缺字段时生成缺口 |
| FactCandidate | WAESGateResult | 候选事实必须过门禁 |
| SOPCandidate | WAESGateResult | 候选 SOP 必须过门禁 |
| WritebackCandidate | WAESGateResult | 写回候选必须过写回门禁 |
| WAESGateResult | KWEWorkItem | 门禁要求人工、补证或委员会时创建工单 |
| KWEWorkItem | ConfirmationRecord | 人工确认结果 |
| KWEWorkItem | DecisionRecord | 委员会裁决结果 |
| ConfirmationRecord | WritebackCandidate | 确认后可进入写回候选 |
| DecisionRecord | ContributionRecord | 裁决后可确认贡献 |
| DecisionRecord | RevenueRecord | 裁决后可确认收益 |
| GapRecord | BountyRecord | 缺口可生成悬赏候选 |
| 所有治理动作 | HarnessEvidenceRecord | 固化 evidence |
| 所有本轮动作 | LOOPRecord | 纳入 LOOP 追踪 |

## 3. KnowledgeObject 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | KDS 内部编号 |
| `uri` | 是 | 可追溯 URI |
| `tenantId` | 是 | 租户 |
| `domain` | 是 | 七类知识域 |
| `objectType` | 是 | 对象类型 |
| `poolRefs` | 是 | KDS 十一池挂接 |
| `ownerType` | 是 | user/team/project/org/external_account/system |
| `ownerId` | 是 | owner 标识 |
| `visibility` | 是 | private/restricted/internal/external_shared/public |
| `lifecycle` | 是 | 统一状态机状态 |
| `trustLevel` | 是 | T0-T5 |
| `ragAdmission` | 是 | safe/limited/repair_required/blocked/sensitive_metadata_only |
| `citationStrength` | 是 | L0-L5 |
| `confirmationStatus` | 是 | not_required/ai_checked/human_required/human_confirmed/committee_required/committee_confirmed/rejected |
| `sourceRefs` | 是 | 来源引用 |
| `evidenceRefs` | 是 | 证据引用 |
| `lineageRefs` | 是 | lineage 引用 |
| `promotionBlockers` | 否 | 不能升级的原因 |
| `createdAt` | 是 | 创建时间 |
| `updatedAt` | 是 | 更新时间 |

## 4. FactCandidate 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 候选事实编号 |
| `sourceObjectId` | 是 | 来源知识对象 |
| `statement` | 是 | 候选事实陈述 |
| `factType` | 是 | order/factory/production/quality/delivery/pod/finance/policy/supplier/customer/oem_transition |
| `poolRefs` | 是 | 挂池 |
| `generatedBy` | 是 | ai/user/system/partner |
| `trustLevel` | 是 | AI 默认 T5 |
| `confidence` | 否 | 置信度 |
| `sourceRefs` | 是 | 来源 |
| `evidenceRefs` | 是 | 证据 |
| `waesGateRefs` | 是 | WAES 门禁 |
| `confirmationStatus` | 是 | 确认状态 |
| `promotionBlockers` | 否 | 升级阻塞 |

禁止字段：`directBusinessWriteback`。

## 5. WAESGateResult 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `gateId` | 是 | 门禁编号 |
| `gateType` | 是 | Source/Evidence/DSR/RAG/Writeback/Revenue/Contribution/Bounty/Committee/Freeze/ExternalShare/SensitiveData |
| `targetObjectType` | 是 | 目标对象类型 |
| `targetObjectId` | 是 | 目标对象编号 |
| `inputRefs` | 是 | source/evidence/policy/acl refs |
| `riskSignals` | 是 | 风险信号 |
| `result` | 是 | passed/human_required/committee_required/repair_required/blocked/redaction_required/freeze_required/metadata_only |
| `reasonCodes` | 是 | 解释代码 |
| `requiredActions` | 是 | 下一步动作 |
| `nextState` | 是 | 建议下一个状态 |
| `allowedOperations` | 是 | 允许操作 |
| `forbiddenOperations` | 是 | 禁止操作 |
| `reviewer` | 否 | 审查人 |
| `timestamp` | 是 | 时间 |
| `harnessEvidenceRef` | 否 | evidence 引用 |

## 6. WritebackCandidate 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `candidateId` | 是 | 写回候选 ID |
| `sourceFactId` | 是 | 来源事实或候选事实 |
| `targetSystem` | 是 | GFIS/GPC/ERP/MES/KDS/WAES |
| `targetModule` | 是 | 目标模块 |
| `targetField` | 是 | 目标字段 |
| `currentValue` | 否 | 当前值 |
| `proposedValue` | 是 | 候选值 |
| `diffReason` | 是 | 差异原因 |
| `evidenceRefs` | 是 | 证据 |
| `waesResult` | 是 | 门禁结果 |
| `businessOwner` | 是 | 业务负责人 |
| `confirmationStatus` | 是 | 确认状态 |
| `writebackMode` | 是 | no-write/sandbox/approved-write/production-write |
| `finalAction` | 否 | accepted/rejected/returned |

P1 前只允许 `no-write` 和 `sandbox`。

## 7. RevenueRecord 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 收益记录编号 |
| `revenueType` | 是 | formal_revenue/invoiced_revenue/potential_revenue/channel_opportunity/knowledge_potential_value |
| `amount` | 否 | 金额 |
| `currency` | 否 | 币种 |
| `basis` | 是 | cash_received/invoice/contract/opportunity/manual_estimate |
| `poolRefs` | 是 | 挂池 |
| `contributionRefs` | 是 | 贡献引用 |
| `distributionStatus` | 是 | not_applicable/candidate/under_review/committee_required/confirmed/distributed/frozen |
| `evidenceRefs` | 是 | 证据 |
| `promotionBlockers` | 否 | 升级阻塞 |

规则：`potential_revenue` 不得自动转为 `formal_revenue`。

## 8. LOOPRecord 最小字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | LOOP 编号 |
| `tenantId` | 是 | 租户 |
| `loopName` | 是 | LOOP 名称 |
| `projectId` | 否 | 项目 |
| `goal` | 是 | 本轮目标 |
| `inputRefs` | 是 | 输入资料 |
| `newObjectRefs` | 是 | 新增对象 |
| `newGapRefs` | 是 | 新增缺口 |
| `candidateFactRefs` | 是 | 候选事实 |
| `candidateSopRefs` | 是 | 候选 SOP |
| `waesResultRefs` | 是 | WAES 结果 |
| `confirmationRefs` | 是 | 人工确认 |
| `committeeRefs` | 是 | 委员会事项 |
| `risk` | 是 | 风险 |
| `nextActions` | 是 | 下一步 |
| `statusBoundary` | 是 | 本轮不得升级声明 |

## 9. 最小 fixture 示例

```yaml
caseId: rag-gate-t5-blocked-001
input:
  objectType: fact_candidate
  trustLevel: T5
  sourceRefs: []
  evidenceRefs: []
expected:
  result: blocked
  ragAdmission: blocked
  citationStrength: L0
  reasonCodes:
    - LLM_OUTPUT_NOT_SOURCE_BACKED
```

```yaml
caseId: writeback-no-owner-blocked-001
input:
  targetSystem: GFIS
  evidenceRefs:
    - EVD-GH-ORD-202606-0001
  businessOwner: null
expected:
  result: blocked
  reasonCodes:
    - BUSINESS_OWNER_REQUIRED
```

```yaml
caseId: revenue-potential-not-formal-001
input:
  revenueType: potential_revenue
  paymentEvidence: null
expected:
  result: blocked
  reasonCodes:
    - NO_ACTUAL_INCOME
```

## 10. 验收标准

P0 对象关系与字段契约通过条件：

1. 核心对象关系链完整。
2. KnowledgeObject、FactCandidate、WAESGateResult、WritebackCandidate、RevenueRecord、LOOPRecord 有最小字段。
3. Gate、RAG、写回、收益有最小 fixture。
4. 字段契约明确禁止直接业务写回。
5. P1 前写回模式限制为 `no-write` 和 `sandbox`。
