---
doc_id: GPCF-DOC-85ADC1863C
title: GFIS Assistant DKS-241 Digest Delivery Preview Policy
project: KDS
related_projects: [GFIS, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-assistant-dks-241-digest-delivery-preview-policy.md
source_path: docs/gc-knowledge-fabric/gfis-assistant-dks-241-digest-delivery-preview-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS Assistant DKS-241 Digest Delivery Preview Policy

## 定位

DKS-241 在 DKS-240 escalation digest preview 的基础上生成 digest delivery preview，只展示候选投递对象、候选通道、投递原因、阻塞投递数量和下一步候选动作。

## 边界

本轮不创建真实 digest delivery、delivery、digest、escalation、timeout event、KWE work item、notification、acknowledgement、receipt、read receipt、approval assignment、approval packet、committee decision、freeze action、Harness evidence、WAES gate result，也不更新 KDS lifecycle、业务事实或任何外部 API。

## 验证

专项验证器为 `scripts/gfis/validate_gfis_assistant_dks_241_digest_delivery_preview.py`，输入为：

- `okf/gfis-assistant-dks-241-digest-delivery-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-241-digest-delivery-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-241-digest-delivery-preview-dry-run.json`

通过标准：6 条预览、Brain 2 条、PKC 1 条、GFIS Assistant 3 条、候选收件人与候选通道各 6 个、必需 evidence 6 个、阻塞投递 3 个，并且所有写入与创建标记为 0/false。
