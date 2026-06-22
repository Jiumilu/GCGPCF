---
doc_id: GPCF-DOC-C9BFBCFA1B
title: GFIS Assistant DKS-248 Routing Queue Preview Policy
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-248-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-248-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-248 Routing Queue Preview Policy

## 定位

本文件固化 DKS-248 的本地 dry-run 规则：从 DKS-247 approval packet preview 派生 routing queue preview，只展示候选队列槽位、队列状态、优先级、候选处理人、所需证据、queue reason、blocked route count 和下一步候选建议。

## 硬边界

- 不创建 routing queue 或 queue item。
- 不创建 approval assignment，不锁定 approver。
- 不创建 approval packet、approval request、approval decision。
- 不创建 committee decision、freeze action。
- 不写 GFIS、GPC、ERP、MES。
- 不写 WAES gate result、KWE work item、Harness evidence。
- 不提升 KDS lifecycle，不生成 accepted fact。
- 不调用外部 API。

## 验证

- `scripts/gfis/validate_gfis_assistant_dks_248_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_preview.py`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`
