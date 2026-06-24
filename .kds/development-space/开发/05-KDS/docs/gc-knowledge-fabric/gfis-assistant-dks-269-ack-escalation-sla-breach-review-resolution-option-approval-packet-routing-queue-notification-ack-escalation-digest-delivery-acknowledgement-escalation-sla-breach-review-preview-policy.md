---
doc_id: GPCF-DOC-4ED6BDDC91
title: GFIS Assistant DKS-269 SLA Breach Review Preview Policy
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-269 SLA Breach Review Preview Policy

## 定位

本文件定义 DKS-269 routing notification ack escalation digest delivery acknowledgement escalation SLA breach review preview。它从 DKS-268 SLA preview 派生，只展示候选 reviewer、evidence gap、breach reason、severity、overdue minutes、阻断数量、边界和下一步建议。

## 上游输入

- `gfis-assistant-dks-268-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-preview`

## 硬边界

DKS-269 不创建 breach record、dispute、committee case、freeze request、reminder、approval request、approval decision、WAES gate result、Harness evidence、KWE work item、KDS lifecycle 或任何业务写回。

## 验证

- Validator: `scripts/gfis/validate_gfis_assistant_dks_269_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_acknowledgement_escalation_sla_breach_review_preview.py`
- Fixture: `fixtures/gfis/gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-dry-run.json`
- OKF: `okf/gfis-assistant-dks-269-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.yaml`
