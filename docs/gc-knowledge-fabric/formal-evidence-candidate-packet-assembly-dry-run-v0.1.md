---
doc_id: GPCF-DOC-61AD13B50E
title: GC-Knowledge Fabric P0 正式证据候选包组装 dry-run v0.1
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/formal-evidence-candidate-packet-assembly-dry-run-v0.1.md
source_path: docs/gc-knowledge-fabric/formal-evidence-candidate-packet-assembly-dry-run-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 正式证据候选包组装 dry-run v0.1

## 定位

本文档定义 P0-D29 formal evidence candidate packet assembly 的 dry-run 口径。它承接 D28 formal evidence write action guard，把候选写入请求组装为 Harness Governance 审核包。

本路径只生成 `formal_harness_evidence_candidate_packet`，不写正式 Harness evidence，不写 KDS，不升级 lifecycle，不开启业务写回，不把 P0 标记为 accepted。

## 候选包必备章节

候选审核包必须包含：

- sourceCandidateRecord
- approvalPreflight
- writeActionGuard
- evidenceRefs
- decisionRationale
- reviewRoute
- idempotencyPlan
- duplicateCheck
- rollbackPlan
- forbiddenActionAcknowledgement

## 组装检查

必须满足：

- D28 write guard 仍为 candidate。
- D28 outputType 仍为 `candidate_write_request`。
- 候选写入请求仍为 candidate。
- formal evidence 未写入。
- Harness evidence 未写入。
- review route 已登记。
- idempotency plan 已登记。
- duplicate check 已登记。
- rollback plan 已登记。
- forbidden actions 已确认。

## 允许下一步

候选包只允许进入：

- submit_to_harness_governance_review
- return_for_packet_repair
- reject_candidate_packet

## 禁止动作

- 不写正式 evidence。
- 不写 Harness evidence。
- 不写 KDS。
- 不提升 lifecycle。
- 不开启业务写回。
- 不标记 P0 accepted。
- 不跳过 Harness review。

## 验证命令

```bash
python3 scripts/api/validate_gckf_p0_formal_evidence_candidate_packet_assembly_dry_run.py
```

预期信号：

```text
gckf_p0_formal_evidence_candidate_packet_assembly_dry_run=pass status=candidate packet_type=formal_harness_evidence_candidate_packet review_status=pending source_guard_status=candidate source_guard_output_type=candidate_write_request required_sections=10 assembly_checks=10 allowed_next_actions=3 forbidden_actions=7 required_sources=4 not_final_acceptance=covered review_route=covered idempotency=covered rollback=covered duplicate_guard=covered starts_server=0 connects_database=0 calls_external_api=0 writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 writes_harness_evidence=0 writes_formal_evidence=0 no_write=covered
```

## 下一步

D30 建议建立 Harness Governance review decision intake dry-run，定义候选包进入人工或 Harness Governance 审核后的接收、退回、拒绝和批准前置条件，但仍不执行正式 evidence 写入。
