---
doc_id: GPCF-DOC-GCKFP0HARNESSDECISIONTEMPLATECURRENTSTATED12720260622
title: GCKF P0 Harness 决策模板当前态证据 D127
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/gckf-p0-harness-decision-template-current-state-d127-20260622.md
source_path: docs/harness/evidence/gckf-p0-harness-decision-template-current-state-d127-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GCKF P0 Harness 决策模板当前态证据 D127

## Evidence ID

`GCKF-P0-HARNESS-DECISION-TEMPLATE-CURRENT-STATE-D127-20260622`

## 结论

旧的 D24 decision template 仍可运行，但它只绑定旧 D23 `candidate / pending` 候选记录。D127 在不改写 D24 历史文件的前提下，新增 current-state decision template，使决策模板层显式吸收 D124/D125/D126 的 hold 上下文。

当前结论是：

- current-state decision template 已可写为 `candidate_with_hold`
- 最大状态仍只能是 `review_ready_with_hold`
- 当前 `default_decision_status` 只能是 `pending_with_hold`

## 当前态来源链

| 环节 | 当前结果 |
|---|---|
| D24 decision template | `pass status=candidate source_candidate_status=candidate source_review_status=pending` |
| D126 current-state candidate record | `pass candidate_record_status=candidate_with_hold review_status=pending_with_hold hold_context_refs=6` |
| D125 current-state packet | `pass packet_status=candidate_with_hold maximum_state=review_ready_with_hold hold_refs=6` |
| D124 closure packet candidate | `pass closure_packet_status=candidate_with_hold maximum_state=review_ready_with_hold completed_items=7 blockers=6` |

## 当前模板范围

| 项目 | 当前值 |
|---|---|
| decision cases | `4` |
| hold context refs | `6` |
| forbidden outputs | `8` |

## Hold 上下文

当前 decision template 必须继承以下约束：

- `formal_harness_write_allowed = false`
- `lifecycle_promotion_allowed = false`
- `runtime_writeback_allowed = false`
- `p1_admission_allowed = false`
- `v1_upgrade_recommended = false`

因此本轮只确认 `pending_with_hold`，不把决策模板误写成可直接 formal write、可放行 P1、或可升级 `v1.0` 的模板。

## 非声明

- 本 current-state decision template 不写 formal Harness evidence。
- 本 current-state decision template 不把 `pending_with_hold` 升级为 `accepted`、`integrated` 或 `production_ready`。
- 本 current-state decision template 不放行 P1 admission，也不建议升级 `v1.0`。

## 后续

下一轮应基于 D127 current-state decision template 进入 repair path workpack 或 governance decision intake 的 current-state 刷新，继续保持 no-write。
