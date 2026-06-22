---
doc_id: GPCF-DOC-C1E752CB0B
title: Headroom LCX Approval Instance Precheck Evidence
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md
source_path: docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Approval Instance Precheck Evidence

## Evidence ID

`HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622`

## 结论

已生成并补齐审批包实例字段与负向实例。本 evidence 只证明字段完整性已满足 precheck-only 要求；WAES/Harness 准入裁决已变更为 `admitted_for_sanitized_measurement_precheck`，但仍不允许采集未脱敏生产 token、启动生产代理或写入真实 KDS API。

## 输出

| artifact | path |
|---|---|
| pending approval instance | `fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json` |
| negative instance fixtures | `fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json` |

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| negative_case_count | 7 |
| approval_instance_template_generated | true |
| approval_instance_precheck_gate | true |
| negative_instance_fixture_gate | true |
| authorization_complete | true |
| waes_harness_admission_decision | admitted_for_sanitized_measurement_precheck |
| production_token_measurement_allowed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |
