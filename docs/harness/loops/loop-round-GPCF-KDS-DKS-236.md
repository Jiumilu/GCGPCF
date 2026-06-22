---
doc_id: GPCF-DOC-70EE4FF084
title: GPCF KDS DKS-236 Loop
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-236.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-236.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF KDS DKS-236 Loop

## 本轮目标

将 DKS-235 approval packet preview 推进为 DKS-236 routing queue preview，形成只读候选路由队列、队列槽位、候选负责人、证据要求、队列原因和下一步候选动作视图。

## 输入

- `okf/gfis-assistant-dks-235-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-235-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-235-routing-queue-notification-ack-escalation-digest-delivery-ack-escalation-sla-breach-review-resolution-option-approval-packet-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_235_routing_queue_notification_ack_escalation_digest_delivery_ack_escalation_sla_breach_review_resolution_option_approval_packet_preview.py`

## 输出

- `okf/gfis-assistant-dks-236-routing-queue-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-236-routing-queue-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-236-routing-queue-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_236_routing_queue_preview.py`
- `docs/gc-knowledge-fabric/gfis-assistant-dks-236-routing-queue-preview-policy.md`

## 门禁边界

- 不创建 routing queue、queue item、approval assignment 或 approval lock。
- 不创建 approval packet、approval request 或 approval decision。
- 不创建 committee decision 或 freeze action。
- 不创建 Harness evidence、WAES gate result 或 KWE work item。
- 不提升 KDS lifecycle，不写 KDS fact / accepted fact。
- 不写 GFIS、GPC、ERP、MES，不调用外部 API。

## 验证

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_236_routing_queue_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
npx tsc -p packages/shared/tsconfig.json --noEmit
npx tsc -p packages/api/tsconfig.json --noEmit
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 反馈

- 本轮只形成 routing queue 候选视图，不形成 routing queue、queue item、assignment、lock、治理证据或业务写入。
- 下一轮 DKS-237 可继续推进 routing queue notification preview，仍保持 no-write 与 evidence-only 边界。
