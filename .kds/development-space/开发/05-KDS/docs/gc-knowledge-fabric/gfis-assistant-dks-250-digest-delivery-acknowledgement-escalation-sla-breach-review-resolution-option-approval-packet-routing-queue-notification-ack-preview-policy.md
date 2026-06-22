---
doc_id: GPCF-DOC-633179942F
title: GFIS Assistant DKS-250 通知确认预览候选规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-250-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-250-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-250 通知确认预览候选规则

## 定位

DKS-250 从 DKS-249 notification preview 派生 notification acknowledgement preview。它只用于 Brain、PKC、GFIS Assistant 展示候选确认状态、候选确认人、确认期限、阻断原因和下一步建议。

## 硬边界

- 不创建 acknowledgement。
- 不创建 receipt / read receipt。
- 不更新 delivery status。
- 不创建 notification、message、inbox item。
- 不创建 routing queue、queue item、approval assignment、approval packet。
- 不创建 WAES / KWE / Harness 记录。
- 不推动 KDS lifecycle。
- 不写 GFIS / GPC / ERP / MES。
- 不调用外部 API。

## 输入

- DKS-249 notification preview。
- DKS-248 routing queue preview refs。
- DKS-247 approval packet preview refs。
- DKS-246 resolution option preview refs。
- DKS-245 breach review preview refs。

## 输出

- `acknowledgementPreviews` dry-run fixture。
- OKF policy。
- Shared TypeScript 类型。
- GFIS validator。

## 验收

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_250_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_preview.py
```

预期输出必须包含：

```text
gfis_assistant_dks_250_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_preview=pass
```
