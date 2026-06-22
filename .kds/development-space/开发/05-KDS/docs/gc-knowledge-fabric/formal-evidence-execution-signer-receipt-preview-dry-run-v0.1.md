---
doc_id: GPCF-DOC-25CDA28633
title: GC-Knowledge Fabric P0 正式证据执行签署人回执预览 dry-run v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-execution-signer-receipt-preview-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-execution-signer-receipt-preview-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据执行签署人回执预览 dry-run v0.1

## 1. 定位

本文档定义 P0-D43 的正式 evidence 执行签署回执预览 dry-run。

D43 只预览 D42 re-entry approval packet 的签署回执收集、拒收、超时升级、重发调度和审计快照要求，不发送通知、不记录回执、不执行审批、不重试、不解冻、不写入正式 evidence。

## 2. 输入

| 输入 | 路径 |
|---|---|
| D43 fixture | `fixtures/api/gckf-p0-formal-evidence-execution-signer-receipt-preview-dry-run-v0.1.json` |
| D43 validator | `scripts/api/validate_gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run.py` |
| D42 approval packet preview | `fixtures/api/gckf-p0-formal-evidence-execution-reentry-approval-packet-preview-dry-run-v0.1.json` |
| D42 Loop evidence | `docs/harness/loops/loop-round-GPCF-GCKF-P0-D42-001.md` |

## 3. 覆盖范围

| 范围 | 预览要求 |
|---|---|
| 签署角色 | 覆盖 request_owner、repair_reviewer、waes_gate_owner、kwe_workflow_owner、harness_reviewer、committee_representative、stop_authority_owner、business_system_owner |
| 回执通道 | 覆盖 controlled_register_ack、harness_review_queue_ack、committee_queue_ack、business_owner_ack |
| 回执状态 | 覆盖 pending、acknowledged、refused、needs_repair、timed_out、escalation_required、voided |
| 拒收路径 | 要求 refusal_reason_policy_ref，不把拒收自动转成结论 |
| 超时升级 | 要求 timeout_escalation_policy_ref，不自动发送升级通知 |
| 重发调度 | 只生成 resend_dispatch_candidate_ref，不执行重发 |
| 审计快照 | 只预览 receipt_audit_snapshot_ref，不写 Harness evidence |

## 4. 禁止动作

- 不发送通知。
- 不记录签署回执。
- 不执行重发。
- 不执行升级。
- 不执行审批。
- 不执行 retry / unfreeze。
- 不写 KDS。
- 不写 GFIS / GPC / 业务系统。
- 不写 Harness evidence。
- 不写 formal evidence。
- 不提升 lifecycle。
- 不标记 accepted / integrated / production_ready。

## 5. 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run.py
```

预期输出必须包含：

```text
gckf_p0_formal_evidence_execution_signer_receipt_preview_dry_run=pass
status=candidate_preview
execution_mode=dry_run_no_write
sends_notification=0
records_signer_receipt=0
executes_resend=0
executes_escalation=0
executes_approval=0
executes_retry=0
executes_unfreeze=0
writes_kds=0
writes_business_system=0
writes_harness_evidence=0
writes_formal_evidence=0
no_write=covered
```

## 6. 结论

D43 仍是 candidate_preview，不是正式验收、正式审批或正式 evidence 写入。后续若进入 D44，应继续只做签署回执升级摘要预览或等价 no-write 预演，不得跳过 Harness/WAES/KWE 人工确认边界。
