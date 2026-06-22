---
doc_id: GPCF-DOC-0935141FBE
title: GFIS Assistant DKS-244 摘要投递确认升级 SLA 预览策略
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-244-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-244-digest-delivery-acknowledgement-escalation-sla-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-244 摘要投递确认升级 SLA 预览策略

## 定位

本文件固化 DKS-244 的本地 dry-run 规则：从 DKS-243 digest delivery acknowledgement escalation preview 派生 SLA preview，只展示 SLA 窗口、SLA 风险、候选负责人、证据缺口、blocked SLA 计数和下一步候选建议。

## 硬边界

- 不创建 SLA timer。
- 不创建 escalation、reminder、escalation task。
- 不创建 delivery acknowledgement、approval request、approval decision。
- 不写 GFIS、GPC、ERP、MES。
- 不写 WAES gate result、KWE work item、Harness evidence。
- 不提升 KDS lifecycle，不生成 accepted fact。
- 不调用外部 API。

## 验证

- `scripts/gfis/validate_gfis_assistant_dks_244_digest_delivery_acknowledgement_escalation_sla_preview.py`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`
