---
doc_id: GPCF-DOC-2471815773
title: GFIS Assistant DKS-246 Resolution Option Preview Policy
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-246-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-246-digest-delivery-acknowledgement-escalation-sla-breach-review-resolution-option-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-246 Resolution Option Preview Policy

## 定位

本文件固化 DKS-246 的本地 dry-run 规则：从 DKS-245 SLA breach review preview 派生 resolution option preview，只展示候选处理人、所需证据、resolution reason、优先级、blocked resolution count 和下一步候选建议。

## 硬边界

- 不创建 resolution。
- 不创建 dispute update、committee decision、freeze action。
- 不创建 approval request、approval decision。
- 不写 GFIS、GPC、ERP、MES。
- 不写 WAES gate result、KWE work item、Harness evidence。
- 不提升 KDS lifecycle，不生成 accepted fact。
- 不调用外部 API。

## 验证

- `scripts/gfis/validate_gfis_assistant_dks_246_digest_delivery_acknowledgement_escalation_sla_breach_review_resolution_option_preview.py`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`
