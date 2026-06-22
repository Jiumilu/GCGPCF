---
doc_id: GPCF-DOC-BF3BEDD74F
title: Harness Evidence 引用完整性规则
project: KDS
related_projects: [WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/harness-evidence-integrity-policy.md
source_path: docs/gc-knowledge-fabric/harness-evidence-integrity-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Harness Evidence 引用完整性规则

## 1. 定位

Harness evidence 是 GC-Knowledge Fabric 的治理证据层，只记录审计、验收、门禁、委员会、Agent 调用、发布审批和目标系统回执等治理证据。

它不保存普通业务知识正文，不替代 KDS 事实存储，不替代 WAES 门禁，不替代 KWE 流程，不替代人工或委员会确认。

## 2. 最小字段

每条 evidence 至少包含：

- evidenceId
- tenantId
- evidenceKind
- title
- objectRefs
- sourceRefs
- gateRefs
- loopRefs
- decisionRefs
- contentHash
- controlledOriginalRef
- summary
- createdBy
- createdAt
- metadata

## 3. 引用完整性

Evidence 引用必须满足：

- `objectRefs` 指向 KDS 对象或候选对象。
- `sourceRefs` 指向来源记录。
- `gateRefs` 指向 WAES gate 结果或 dry-run gate request。
- `loopRefs` 指向 LOOP record。
- `decisionRefs` 指向委员会或授权决策记录。
- 高风险 evidence 必须有 `contentHash` 或 `controlledOriginalRef`。
- metadata-only 敏感资料不得包含原文。

## 4. Evidence Kind

允许的 evidence 类型：

- file_hash
- controlled_original
- acceptance_record
- audit_record
- committee_record
- permission_change
- agent_used_knowledge
- publication_approval
- target_system_receipt

## 5. Hard Boundaries

Harness evidence 不能：

- 直接创建正式事实。
- 直接写业务系统。
- 直接分配收益。
- 直接确认积分。
- 直接划拨额度。
- 直接结算悬赏。
- 直接完成委员会裁决。
- 直接允许外部共享。
- 存储敏感原文、密钥、Token、合同敏感条款、POD 原件或金融凭证原文。

Evidence 只能作为后续 KDS、WAES、KWE、Brain/PKC、委员会和 LOOP 的引用依据。

## 6. 完整性输出

引用完整性 validator 只允许输出：

- passed
- blocked
- repair_required

`passed` 只表示本地 evidence 引用结构完整，不表示业务完成或验收完成。

## 7. 本地验证边界

本规则当前只通过本地 OKF、shared type、fixture 和 validator 验证。

不得把本规则写成：

- 真实 Harness evidence 已写入。
- 真实业务事实已完成。
- 真实业务系统写回已完成。
- 收益、积分、额度、悬赏或委员会事项已完成。
