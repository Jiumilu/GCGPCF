---
doc_id: GPCF-DOC-LOOP-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-002
title: Loop Round - GPCF Cognee 外部执行层接入 Intake 收口 002
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-002.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 外部执行层接入 Intake 收口 002

## 输入

- `docs/harness/evidence/cognee-external-execution-integration-validation-20260626.md`
- `docs/harness/evidence/cognee-external-execution-entry-and-receipt-template-20260626.md`
- `docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md`

## run

- 把外部执行层接入所需的最小必填参数收束到单一 intake 包。
- 冻结授权来源、记录数、回滚入口和禁止声明边界。
- 为下一轮真实外部执行接入验证准备可直接填写的 pending 实例。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：当前仍缺 `execution_target`、`execution_owner`、`execution_window_*` 和 `receipt_id`，不具备真实外部执行回执。
- 当前状态：`external_execution_integration_intake=pending_user_input`，`production_write=false`，`accepted=false`，`integrated=false`，`production_ready=false`。

## verify

- 必须保持：
  - `authorization_complete=true`
  - `owner_decision=approve_live_write`
  - `waes_decision=pass`
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
- 必须新增：
  - 外部执行层 intake JSON
  - intake validator
  - intake evidence

## recover

- 若 intake 字段再次分散到多份文档或出现未授权状态提升：退回 `GPCF-DOC-LOOP-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-001`，重新以单一 intake 包收口。

## debug

- 当前最短路径不是“再写一份接入说明”，而是把下一步真实执行前必须由人工补齐的参数集中成可校验输入。
