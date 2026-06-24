---
doc_id: GPCF-DOC-C77F7196EB
title: GC-Knowledge Fabric P0 正式证据执行证据预览 dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-execution-evidence-preview-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-execution-evidence-preview-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据执行证据预览 dry-run v0.1

## 定位

本文档定义 P0-D37 formal evidence execution evidence preview 的 dry-run 口径。它承接 D36 final execution request，只预览未来 Harness execution 可能生成的 evidence 字段。

本路径只形成 evidence preview 候选，不把 preview 写成正式 evidence，不写 Harness evidence，不写 KDS，不写业务系统，不升级 lifecycle，不把 P0 标记为 accepted 或 production ready。

## 预览字段

- evidenceId
- evidenceType
- tenantId
- projectId
- sourceRequestRef
- sourceGuardRef
- sourceStepRef
- authorityRefs
- humanAuthorizationRef
- committeeAuthorizationRef
- freezeGateResultRef
- duplicateCheckRef
- idempotencyKey
- executionLockRef
- preWriteSnapshotRef
- postWriteVerificationPlanRef
- rollbackPlanRef
- auditTrailRef
- createdBy
- createdAt
- status

## 预览检查

必须满足：

- source final execution request 仍为 candidate_request。
- source final execution request executionStatus 仍为 not_executed。
- source final execution request 仍为 dryRunOnly。
- execution mode 为 `dry_run_no_write`。
- preview status 为 `candidate_preview`。
- preview 包含 source request、source guard、source step 引用。
- preview 包含 authority、human authorization、committee authorization、freeze gate、duplicate check、idempotency、execution lock、snapshot、verification、rollback 与 audit 引用。
- preview 不写 Harness evidence。
- preview 不写 formal evidence。
- preview 后续仍需 future Harness execution。

## 阻断条件

任一条件成立时不得形成 evidence preview：

- source request not candidate request
- source request already executed
- source request not dry run only
- missing source request ref
- missing authority refs
- missing human authorization
- missing committee authorization
- missing freeze gate result
- missing duplicate check
- missing idempotency key
- missing execution lock
- missing pre-write snapshot
- missing post-write verification plan
- missing rollback plan
- missing audit trail

## 禁止动作

- 不写正式 evidence。
- 不写 Harness evidence。
- 不执行正式写入。
- 不写 KDS。
- 不写业务系统。
- 不提升 lifecycle。
- 不标记 P0 accepted。
- 不标记 production ready。
- 不把 preview 转成 evidence。
- 不把 request 升级为 approved。
- 不释放 execution lock。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_execution_evidence_preview_dry_run.py
```

预期信号：

```text
gckf_p0_formal_evidence_execution_evidence_preview_dry_run=pass status=candidate_preview preview_type=formal_evidence_execution_evidence_preview preview_status=candidate_preview execution_status=not_executed execution_mode=dry_run_no_write source_request_status=candidate_request source_request_execution_status=not_executed covered_request_status=candidate_request preview_fields=21 preview_checks=22 blocking_conditions=15 forbidden_actions=11 required_sources=4 not_final_acceptance=covered dry_run_only=covered source_lineage=covered authority_refs=covered future_harness_execution=covered preview_not_evidence=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D38 建议建立 formal evidence execution verification plan preview dry-run，用于预览正式写入后的验证计划，但仍不执行、不写 evidence。
