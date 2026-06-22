---
doc_id: GPCF-DOC-6CCCF2BB73
title: GPCF KDS DKS-232 Loop
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-232.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-232.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF KDS DKS-232 Loop

## 本轮目标

将 DKS-231 routing queue notification ack escalation digest delivery ack escalation preview 推进为 DKS-232 SLA preview，形成只读 SLA 风险、时间窗口、候选负责人、证据缺口和下一步候选动作视图。

## 输入

- `okf/gfis-assistant-dks-231-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-231-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-231-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_231_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_preview.py`

## 输出

- `okf/gfis-assistant-dks-232-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-232-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-232-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_232_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_preview.py`
- `docs/gc-knowledge-fabric/gfis-assistant-dks-232-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.md`

## 门禁边界

- 不创建 SLA timer。
- 不创建 escalation、reminder、escalation task 或 KWE work item。
- 不创建 delivery acknowledgement、approval request、approval decision、Harness evidence 或 WAES gate result。
- 不提升 KDS lifecycle，不写 KDS fact / accepted fact。
- 不写 GFIS、GPC、ERP、MES，不调用外部 API。

## 验证

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_232_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
npx tsc -p packages/shared/tsconfig.json --noEmit
npx tsc -p packages/api/tsconfig.json --noEmit
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 反馈

- 本轮只形成 SLA preview 候选视图，不形成业务写入或治理证据写入。
- 下一轮 DKS-233 可继续推进 SLA breach review preview，仍保持 no-write 与 evidence-only 边界。
