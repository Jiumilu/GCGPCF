---
doc_id: GPCF-DOC-5F4A9267DC
title: GC-Knowledge Fabric P0 正式证据写入动作门禁 dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-write-action-guard-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-write-action-guard-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据写入动作门禁 dry-run v0.1

## 定位

本文档定义 P0-D28 formal evidence write action guard 的 dry-run 口径。它承接 D27 approval-to-formal-evidence preflight，定义未来正式 Harness evidence 写入动作的权限、输入、幂等、防重复和回滚前置条件。

本路径只生成 `candidate_write_request`，不写正式 Harness evidence，不写 KDS，不升级 lifecycle，不开启业务写回，不把 P0 标记为 accepted。

## 输入来源

- D27 approval formal evidence preflight fixture
- D27 approval formal evidence preflight validator
- D27 受控说明文档
- D27 LOOP evidence

## 写入动作 guard 必填输入

候选写入请求必须包含：

- reviewerId
- reviewedAt
- evidenceRefs
- sourceCandidateRecordRef
- decisionRationale
- targetHarnessEvidenceType
- approvalPreflightRef
- idempotencyKey
- writeAuthorityRef
- rollbackPlanRef

## Guard 检查

必须满足：

- approval preflight 仍为 candidate。
- preflight type 匹配。
- 只允许 approved decision outcome。
- reviewer authority 已登记。
- idempotency key 已登记。
- 不存在重复正式 evidence。
- rollback plan 已登记。
- 正式写入必须由独立 Harness Governance execution 执行。
- 同一动作不得夹带业务写回。

## 禁止动作

- 不写正式 evidence。
- 不写 Harness evidence。
- 不写 KDS。
- 不提升 lifecycle。
- 不开启业务写回。
- 不标记 P0 accepted。
- 不绕过 Harness Governance。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_write_action_guard_dry_run.py
```

预期信号：

```text
gckf_p0_formal_evidence_write_action_guard_dry_run=pass status=candidate action_type=formal_harness_evidence_write_action_guard output_type=candidate_write_request source_preflight_status=candidate source_preflight_type=formal_harness_evidence_write_preflight required_inputs=10 guard_checks=9 forbidden_actions=7 required_sources=4 not_final_acceptance=covered idempotency=covered rollback=covered duplicate_guard=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D29 建议建立 formal evidence candidate packet assembly dry-run，将 D28 的候选写入请求组装成正式 evidence 写入前的审核包，但仍不执行真实写入。
