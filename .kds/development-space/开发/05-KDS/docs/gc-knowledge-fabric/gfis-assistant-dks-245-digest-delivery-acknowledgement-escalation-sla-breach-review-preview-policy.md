---
doc_id: GPCF-DOC-653FE10892
title: GFIS Assistant DKS-245 SLA Breach Review Preview Policy
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-245-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-245-digest-delivery-acknowledgement-escalation-sla-breach-review-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-245 SLA Breach Review Preview Policy

## 定位

本文件固化 DKS-245 的本地 dry-run 规则：从 DKS-244 digest delivery acknowledgement escalation SLA preview 派生 SLA breach review preview，只展示候选审阅人、证据缺口、breach reason、严重度、超时分钟、blocked review count 和下一步候选建议。

## 硬边界

- 不创建 breach record。
- 不创建 dispute、committee case、freeze request。
- 不创建 reminder、approval request、approval decision。
- 不写 GFIS、GPC、ERP、MES。
- 不写 WAES gate result、KWE work item、Harness evidence。
- 不提升 KDS lifecycle，不生成 accepted fact。
- 不调用外部 API。

## 验证

- `scripts/gfis/validate_gfis_assistant_dks_245_digest_delivery_acknowledgement_escalation_sla_breach_review_preview.py`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`
