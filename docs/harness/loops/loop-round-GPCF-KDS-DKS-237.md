---
doc_id: GPCF-DOC-3B0B60DBA5
title: GPCF KDS DKS-237 Loop
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-237.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-237.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF KDS DKS-237 Loop

## 本轮目标

将 DKS-236 routing queue preview 推进为 DKS-237 routing queue notification preview，形成只读候选通知类型、候选通知渠道、候选收件人、通知原因、阻塞通知数和下一步候选动作视图。

## 输入

- `okf/gfis-assistant-dks-236-routing-queue-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-236-routing-queue-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-236-routing-queue-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_236_routing_queue_preview.py`

## 输出

- `okf/gfis-assistant-dks-237-routing-queue-notification-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-237-routing-queue-notification-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-237-routing-queue-notification-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_237_routing_queue_notification_preview.py`
- `docs/gc-knowledge-fabric/gfis-assistant-dks-237-routing-queue-notification-preview-policy.md`

## 门禁边界

- 不创建 notification、notification delivery、message 或 inbox item。
- 不发送 external notification。
- 不创建 routing queue、queue item、approval assignment 或 approval lock。
- 不创建 approval packet、approval request 或 approval decision。
- 不创建 committee decision 或 freeze action。
- 不创建 Harness evidence、WAES gate result 或 KWE work item。
- 不提升 KDS lifecycle，不写 KDS fact / accepted fact。
- 不写 GFIS、GPC、ERP、MES，不调用外部 API。

## 验证

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_237_routing_queue_notification_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
npx tsc -p packages/shared/tsconfig.json --noEmit
npx tsc -p packages/api/tsconfig.json --noEmit
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 反馈

- 本轮只形成 routing queue notification 候选视图，不形成通知、投递、消息、队列、审批、治理证据或业务写入。
- 下一轮 DKS-238 可继续推进 routing queue notification acknowledgement preview，仍保持 no-write 与 evidence-only 边界。
