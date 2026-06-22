---
doc_id: GPCF-DOC-3FDBF59030
title: GFIS Assistant DKS-252 升级摘要预览候选规则
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-252-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-252-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-approval-packet-routing-queue-notification-ack-escalation-digest-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-252 升级摘要预览候选规则

DKS-252 从 DKS-251 acknowledgement escalation preview 派生 escalation digest preview。它只展示候选摘要渠道、候选接收人、摘要原因、阻断动作和下一步建议。

硬边界：不创建 digest、digest delivery、escalation、timeout event、KWE work item、notification、acknowledgement、receipt、read receipt、delivery update、approval、committee、freeze、WAES、Harness、KDS lifecycle 或任何业务写回。

验证命令：

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_252_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_approval_packet_routing_queue_notification_ack_escalation_digest_preview.py
```
