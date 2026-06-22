---
doc_id: GPCF-DOC-724F09025F
title: KDS ACL 与外部共享视图规则
project: KDS
related_projects: [PVAOS, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/kds-acl-external-share-policy.md
source_path: docs/gc-knowledge-fabric/kds-acl-external-share-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# KDS ACL 与外部共享视图规则

## 1. 定位

KDS ACL 与外部共享视图规则定义合作单位、外部账号、供应商、客户、项目组、Brain/PKC 和 Agent 在读取知识对象时的最小权限边界。

本规则只定义本地契约与 dry-run 校验，不创建真实账号、不变更真实权限、不发布外部视图、不调用真实 KDS API。

## 2. 最小 ACL 字段

每条 ACL 记录至少包含：

- aclId
- tenantId
- subjectType
- subjectId
- objectId
- domain
- visibility
- allowedActions
- deniedActions
- poolRefs
- projectId
- supplyChainNodeId
- expiresAt
- createdBy
- createdAt

## 3. 外部共享视图字段

外部共享视图至少包含：

- viewId
- tenantId
- externalAccountId
- objectId
- visibleFields
- redactedFields
- metadataOnly
- ragAdmission
- waesGateStatus
- publicationApprovalRef
- evidenceRefs
- expiresAt

## 4. 访问动作

允许定义的动作：

- read_metadata
- read_redacted_summary
- read_full_content
- use_for_limited_rag
- use_for_safe_rag
- create_candidate
- request_promotion
- request_external_share

外部账号默认只允许 `read_metadata` 和 `read_redacted_summary`，除非 ACL、WAES external_share_gate、脱敏、publication approval 同时满足。

## 5. Hard Boundaries

- tenant 必须隔离。
- supply_chain 对象必须按供应商/客户/节点分区。
- external_account 不能默认看其他单位明细。
- sensitive metadata-only 对象不得外泄原文。
- blocked RAG 对象不得进入外部共享视图。
- T5 AI-only 内容不得作为正式外部共享事实。
- external share 必须经过 WAES external_share_gate。
- public visibility 必须有 publication approval。
- ACL pass 不等于 RAG 强引用、不等于业务写回、不等于收益或积分确认。

## 6. 本地验证边界

本规则当前只通过本地 OKF、shared type、fixture 和 validator 验证。

不得把本规则写成：

- 真实外部账号权限已经变更。
- 真实外部共享门户已经发布。
- 真实 KDS 权限已经写入。
- 真实业务系统写回、收益、积分、额度、悬赏或委员会事项已经完成。
