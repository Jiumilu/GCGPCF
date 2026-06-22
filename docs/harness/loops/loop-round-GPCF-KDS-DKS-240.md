---
doc_id: GPCF-DOC-B5FFD8608D
title: GPCF KDS DKS-240 Loop
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-240.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-240.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF KDS DKS-240 Loop

## 本轮目标

将 DKS-239 acknowledgement escalation preview 推进为 DKS-240 escalation digest preview，形成只读候选摘要渠道、摘要接收人、摘要原因、阻塞摘要数和下一步候选动作视图。

## 输入

- `okf/gfis-assistant-dks-239-acknowledgement-escalation-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-239-acknowledgement-escalation-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-239-acknowledgement-escalation-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_239_acknowledgement_escalation_preview.py`

## 输出

- `okf/gfis-assistant-dks-240-escalation-digest-preview-policy.yaml`
- `packages/shared/src/knowledge/gfis-assistant-dks-240-escalation-digest-preview.ts`
- `fixtures/gfis/gfis-assistant-dks-240-escalation-digest-preview-dry-run.json`
- `scripts/gfis/validate_gfis_assistant_dks_240_escalation_digest_preview.py`
- `docs/gc-knowledge-fabric/gfis-assistant-dks-240-escalation-digest-preview-policy.md`

## 门禁边界

- 不创建 digest 或 digest delivery。
- 不创建 escalation、timeout event 或 KWE work item。
- 不创建 notification、acknowledgement、receipt 或 read receipt。
- 不更新 delivery status。
- 不发送 external notification。
- 不创建 approval assignment 或 approval lock。
- 不创建 approval packet、approval request 或 approval decision。
- 不创建 committee decision 或 freeze action。
- 不创建 Harness evidence 或 WAES gate result。
- 不提升 KDS lifecycle，不写 KDS fact / accepted fact。
- 不写 GFIS、GPC、ERP、MES，不调用外部 API。

## 验证

```bash
python3 scripts/gfis/validate_gfis_assistant_dks_240_escalation_digest_preview.py
python3 scripts/coverage/validate_okf_types_api_validator_coverage.py
npx tsc -p packages/shared/tsconfig.json --noEmit
npx tsc -p packages/api/tsconfig.json --noEmit
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 反馈

- 本轮只形成 escalation digest 候选视图，不形成摘要、摘要投递、升级事件、超时事件、KWE 工单、治理证据或业务写入。
- 下一轮 DKS-241 可继续推进 digest delivery preview，仍保持 no-write 与 evidence-only 边界。
