---
doc_id: GPCF-DOC-46C72A325B
title: "Proposal: Sprint 4 — 知识协作"
project: WAES
related_projects: [WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-v3.2-sprint4-20260611-005427/proposal.md
source_path: .harness/runs/gbrain-v3.2-sprint4-20260611-005427/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Proposal: Sprint 4 — 知识协作

## Scope
- 页面批注 (comments): 段落级评论、@提及、解决/重开
- 变更建议 (proposals): 类似 PR 的变更提案→评审→合并流程
- 订阅管理 (subscriptions): 页面/空间变更通知订阅
- 通知集成: 利用已有 notifications 表推送协作事件

## Tasks (8)
T4.1: Comments service (server/collaboration/comments.py)
T4.2: Proposals service (server/collaboration/proposals.py)
T4.3: Subscriptions service (server/operations/subscriptions.py)
T4.4: Collaboration routes (server/routes/collaboration.py)
T4.5: Admin collaboration module
T4.6: Update main.py
T4.7: Unit tests
T4.8: Evidence collection

## Non-Goals
- 不做实时协同编辑
- 不做工作流引擎
