---
doc_id: GPCF-DOC-61855ADD43
title: GC-Knowledge Fabric P0 Harness 治理审阅决策受理 dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/harness-governance-review-decision-intake-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/harness-governance-review-decision-intake-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 Harness 治理审阅决策受理 dry-run v0.1

## 定位

本文档定义 P0-D30 Harness Governance review decision intake 的 dry-run 口径。它承接 D29 formal evidence candidate packet assembly，定义候选包进入人工或 Harness Governance 审核后的接收、退回、拒绝和批准前置条件。

本路径不写正式 Harness evidence，不写 KDS，不升级 lifecycle，不开启业务写回，不把 P0 标记为 accepted。即使结论为 `approve_for_future_formal_write`，也只能进入后续独立正式写入动作。

## 允许决策结论

- accept_for_review
- return_for_packet_repair
- reject_candidate_packet
- approve_for_future_formal_write

## 决策必填字段

- reviewerId
- reviewedAt
- sourcePacketRef
- decisionOutcome
- decisionRationale
- evidenceRefs
- authorityRef

## 决策门禁

必须满足：

- source packet 仍为 candidate。
- source packet reviewStatus 仍为 pending。
- reviewer authority 已登记。
- decision outcome 属于允许集合。
- formal evidence 未写入。
- Harness evidence 未写入。
- approval 结论不等于写入 evidence。
- repair 与 rejection 必须有原因。
- future formal write 必须进入独立 execution。

## 禁止动作

- 不写正式 evidence。
- 不写 Harness evidence。
- 不写 KDS。
- 不提升 lifecycle。
- 不开启业务写回。
- 不标记 P0 accepted。
- 不把 approval 当成 evidence 已写入。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_harness_governance_review_decision_intake_dry_run.py
```

预期信号：

```text
gckf_p0_harness_governance_review_decision_intake_dry_run=pass status=candidate intake_type=harness_governance_review_decision_intake review_status=pending source_packet_status=candidate source_packet_review_status=pending allowed_decisions=4 required_decision_fields=7 decision_guards=9 forbidden_actions=7 required_sources=4 not_final_acceptance=covered future_formal_write_separate=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D31 建议建立 future formal write execution preflight dry-run，定义 `approve_for_future_formal_write` 之后的正式写入执行前检查，但仍不执行真实写入。
