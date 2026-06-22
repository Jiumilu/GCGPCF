---
doc_id: GPCF-DOC-EF1AC72724
title: RAG Response Citation Packet 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/rag-response-citation-packet-policy.md
source_path: docs/gc-knowledge-fabric/rag-response-citation-packet-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# RAG Response Citation Packet 规则

## 1. 定位

RAG Response Citation Packet 是 Brain、PKC、GFIS Assistant、指挥舱和 Agent 在输出回答时必须携带的引用证据包。

它用于说明回答依据、引用强度、来源边界、ACL/WAES 过滤、敏感处理和不可自动写回边界。

本规则只定义本地契约与 dry-run 校验，不执行真实 RAG 检索，不调用真实模型，不写 KDS、WAES、KWE、GFIS/GPC 或外部 API。

## 2. 最小字段

每个 citation packet 至少包含：

- packetId
- tenantId
- userId
- assistantSurface
- query
- answerMode
- citations
- highestCitationStrength
- boundaryNotices
- missingEvidenceRefs
- waesGateRefs
- aclDecisionRefs
- generatedAt
- noWrite

## 3. Citation 最小字段

每条 citation 至少包含：

- citationId
- objectId
- sourceRefs
- evidenceRefs
- trustLevel
- ragAdmission
- citationStrength
- domain
- poolRefs
- visibility
- metadataOnly
- redacted
- canUseForAnswer
- canUseForStrongReference
- canUseForBusinessAssist

## 4. Answer Mode

允许的回答模式：

- no_answer
- metadata_only
- weak_answer
- strong_answer
- business_assist
- blocked_with_reason

## 5. Hard Boundaries

- L0 不得进入 citations。
- metadata-only 只能输出元数据、摘要或受控原件指针。
- L3 必须显示边界提示。
- L4/L5 也不得自动写回业务系统。
- L5 仍不能替代人工确认、委员会裁决、收益/积分确认或责任归因。
- missing evidence 存在时不得输出 strong answer。
- blocked RAG、T5 AI-only、无 ACL 对象不得进入回答包。
- citation packet pass 不等于正式事实、不等于业务写回、不等于收益或积分确认。

## 6. 本地验证边界

本规则当前只通过本地 OKF、shared type、fixture 和 validator 验证。

不得把本规则写成：

- 真实 RAG 服务已经上线。
- 真实模型已经调用。
- 真实 KDS 检索已经发生。
- 真实 GFIS/GPC 写回已经完成。
- 回答已经形成正式业务事实。
