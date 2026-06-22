---
doc_id: GPCF-DOC-4B4BB186A8
title: GFIS Assistant DKS-208 Routing Queue Notification Ack Escalation Digest Delivery Ack Escalation SLA Preview No-write 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-208-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-208-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-208 Routing Queue Notification Ack Escalation Digest Delivery Ack Escalation SLA Preview No-write 规则

## 目标

DKS-208 将 DKS-207 acknowledgement escalation preview 推进为 SLA preview，只展示候选 SLA 风险、SLA 时间窗口、候选升级负责人、证据要求和下一步候选动作。

## 严格边界

- 不创建 SLA timer。
- 不创建 escalation、reminder、escalation task 或 KWE work item。
- 不创建 delivery acknowledgement、approval request、approval decision、Harness evidence 或 WAES gate result。
- 不提升 KDS lifecycle，不写 KDS fact / accepted fact。
- 不写 GFIS、GPC、ERP、MES，不调用外部 API。

## 验证

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_208_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
```
