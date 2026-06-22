---
doc_id: GPCF-DOC-C07C93A828
title: GC-Knowledge Fabric P0 Formal Evidence Execution Request Dry-run v0.1
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-execution-request-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-execution-request-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Formal Evidence Execution Request Dry-run v0.1

## 定位

本文档定义 P0-D32 formal evidence execution request 的 dry-run 口径。它承接 D31 future formal write execution preflight，将执行前检查转为正式 evidence 写入的候选执行请求。

本路径只形成执行请求候选，不执行正式写入，不写 Harness evidence，不写 KDS，不升级 lifecycle，不开启业务写回，不把 P0 标记为 accepted。

## 执行请求必填输入

- preflightRef
- approvalDecisionRef
- executionRequestId
- requesterId
- requestedAt
- authorityRef
- evidenceRefs
- idempotencyKey
- duplicateCheckRef
- rollbackPlanRef
- executionLockRef
- auditTrailRef
- harnessReviewRouteRef

## 请求检查

必须满足：

- source preflight 仍为 candidate。
- source preflight executionStatus 仍为 candidate。
- decision outcome 为 `approve_for_future_formal_write`。
- source preflight checks 已覆盖。
- approval decision 引用存在。
- authority 引用存在。
- idempotency key 存在。
- 不存在重复正式 evidence。
- rollback plan 存在。
- execution lock 存在。
- audit trail 引用存在。
- Harness review route 存在。
- 仍需单独执行批准。
- 本请求不执行正式写入。

## 禁止动作

- 不执行正式写入。
- 不写正式 evidence。
- 不写 Harness evidence。
- 不写 KDS。
- 不提升 lifecycle。
- 不开启业务写回。
- 不标记 P0 accepted。
- 不绕过 Harness review。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_execution_request_dry_run.py
```

预期信号：

```text
gckf_p0_formal_evidence_execution_request_dry_run=pass status=candidate request_type=formal_evidence_execution_request request_status=candidate execution_status=not_executed source_preflight_status=candidate source_preflight_execution_status=candidate covered_decision=approve_for_future_formal_write required_inputs=13 request_checks=14 forbidden_actions=8 required_sources=4 not_final_acceptance=covered dry_run_only=covered harness_review_route=covered separate_execution_approval=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D33 建议建立 formal evidence execution approval dry-run，对 D32 执行请求进行 Harness 审批候选确认，但仍不执行真实写入。
