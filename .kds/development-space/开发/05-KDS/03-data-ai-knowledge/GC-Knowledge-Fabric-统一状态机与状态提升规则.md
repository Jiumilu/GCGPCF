---
doc_id: GPCF-DOC-5F592CAC71
title: GC-Knowledge Fabric 统一状态机与状态提升规则
project: KDS
related_projects: [WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-统一状态机与状态提升规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-统一状态机与状态提升规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 统一状态机与状态提升规则

日期：2026-06-20  
状态：`draft`  

## 1. 目标

统一状态机用于约束 KnowledgeObject、FactCandidate、SOPCandidate、WritebackCandidate、GapRecord、ContributionRecord、RevenueRecord、QuotaRecord、DecisionRecord 和 LOOPRecord 的状态语义。

状态提升必须基于来源、证据、WAES 门禁、KWE 流程、人工确认、委员会决议和 Harness evidence。任何自动化、AI 输出、模板或 dry-run 都不能单独提升为正式完成状态。

## 2. 生命周期状态

| 状态 | 含义 | 谁可创建 | 谁可提升 | 可 RAG | 可写回 | 可计入收益 |
|---|---|---|---|---|---|---|
| `draft` | 草稿 | 人、AI、系统 | owner / KWE | 否 | 否 | 否 |
| `candidate` | 候选 | 人、AI、系统、合作方 | KWE | 否，少数可 L1/L2 | 否 | 否 |
| `reviewing` | 审核中 | KWE | 人工 / 委员会 | L1/L2 | 否 | 否 |
| `repair_required` | 需补证 | WAES / KWE | KWE | 否或 L1 | 否 | 否 |
| `evidence_ready` | 证据就绪 | KWE | WAES | L2/L3 | 否 | 否 |
| `confirmed` | 已确认 | 人工 / 委员会 | KDS / WAES | L3/L4 | 可进入写回候选 | 可进入候选 |
| `accepted` | 已验收 | 授权人 / 委员会 | KDS | L4/L5 | 可写回，仍需业务系统门禁 | 可进入正式口径 |
| `published` | 已发布 | 授权发布人 | KDS | L4/L5 | 视对象类型而定 | 视对象类型而定 |
| `frozen` | 冻结 | WAES / 委员会 | 委员会 / 授权治理人 | 否 | 否 | 否 |
| `rejected` | 拒绝 | 人工 / 委员会 / WAES | KDS | 否 | 否 | 否 |
| `superseded` | 被替代 | KDS | KDS | 否或 L1 | 否 | 否 |
| `archived` | 归档 | KDS | KDS | 否或 L1/L2 | 否 | 否 |

## 3. RAG 引用强度

| 强度 | 含义 | 可用场景 |
|---|---|---|
| L0 | 不可引用 | blocked、敏感原文、无来源、T5 默认状态 |
| L1 | 仅检索召回，不展示 | 内部缺口发现、去重、索引提示 |
| L2 | 可展示摘要，不展示原文 | metadata-only、repair_required、敏感资料摘要 |
| L3 | 可弱引用，必须标注来源不确定 | limited、evidence_ready |
| L4 | 可强引用，可用于助手回答 | safe、confirmed |
| L5 | 可业务辅助决策引用，但仍需确认 | accepted + T0/T1 + evidence 完整 |

映射规则：

| RAG 状态 | 默认引用强度 |
|---|---|
| `blocked` | L0 |
| `sensitive_metadata_only` | L1/L2 |
| `repair_required` | L1/L2 |
| `limited` | L3 |
| `safe` | L4 |
| `confirmed + T0/T1` | L4/L5 |
| `accepted + T0/T1 + evidence 完整` | L5 |

## 4. 状态提升门禁

| 提升 | 必需条件 |
|---|---|
| `draft -> candidate` | 编号、owner、domain、objectType、poolRefs 或 pendingPoolRefs |
| `candidate -> reviewing` | sourceRefs 或明确缺口、KWE WorkItem |
| `reviewing -> repair_required` | WAES 发现来源、证据、权限、敏感资料或责任边界缺口 |
| `repair_required -> evidence_ready` | 缺口补齐、EvidenceRecord 绑定、requiredActions 关闭 |
| `evidence_ready -> confirmed` | 人工确认或委员会确认 |
| `confirmed -> accepted` | WAES 通过、Harness evidence 固化、授权人验收 |
| `accepted -> published` | 发布授权、External Share Gate、Sensitive Data Gate |
| `任何状态 -> frozen` | 重大争议、违规风险、收益争议、RAG 风险、外部共享风险 |
| `任何状态 -> rejected` | 确认失败、证据造假、来源不合格、委员会拒绝 |
| `accepted/published -> superseded` | 新版本替代并建立 lineage |
| `任何状态 -> archived` | 不再使用且保留追溯 |

## 5. 候选对象必须解释不能升级的原因

所有 `candidate`、`repair_required`、`reviewing` 对象必须具备 promotionBlockers：

```yaml
promotionBlockers:
  - reasonCode: SOURCE_MISSING
    missingEvidence:
      - sourceRefs
    requiredReviewer: project_owner
    requiredGate: SourceGate
    nextAction: submit_source_record
```

常用 reasonCodes：

| reasonCode | 含义 |
|---|---|
| `SOURCE_MISSING` | 缺来源 |
| `EVIDENCE_MISSING` | 缺证据 |
| `BUSINESS_OWNER_REQUIRED` | 缺业务负责人 |
| `COMMITTEE_REQUIRED` | 需委员会 |
| `SENSITIVE_ORIGINAL_BLOCKED` | 敏感原文禁止开放 |
| `ACL_UNCLEAR` | 权限不明 |
| `NO_ACTUAL_INCOME` | 无到账收入 |
| `TEMPLATE_NOT_FACT` | 模板不能作为事实 |
| `LLM_OUTPUT_NOT_SOURCE_BACKED` | LLM 输出无来源支撑 |
| `WRITEBACK_NOT_ALLOWED` | 不允许写回 |

## 6. 禁止提升规则

1. T5 对象不得直接提升为 `confirmed`。
2. 模板不得直接提升为业务事实。
3. `safe` 不等于业务系统可写回。
4. `confirmed` 不等于正式收益。
5. `evidence_ready` 不等于 accepted。
6. LOOP 记录不得自动把业务状态升为 complete。
7. dry-run 结果不得作为生产完成证据。

## 7. 验收标准

P0 状态机通过条件：

1. 每个状态有含义、创建人、提升人、RAG、写回、收益边界。
2. 每个提升路径有必需证据和门禁。
3. 每个候选对象能解释不能升级的原因。
4. 冻结、拒绝、被替代、归档路径明确。
5. RAG 引用强度 L0-L5 与状态关联明确。
