---
doc_id: GPCF-DOC-LOOP-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-INTAKE-001
title: Loop Round - GPCF Cognee 真实外部执行回执 Intake 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-INTAKE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-INTAKE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 真实外部执行回执 Intake 001

## 输入

- `docs/harness/evidence/cognee-full-run-readiness-rollup-20260626.md`
- `docs/harness/evidence/cognee-external-execution-receipt-template-20260626.md`

## run

- 为 `COGNEE-FULL-RUN-GAP-001` 建立真实外部执行回执接收入口。
- 固化真实回执必须字段、接收状态、计数要求和 GAP-001 ready 条件。
- 增加 intake validator，用于区分 `pending_real_receipt` 与真实回执已记录。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：真实外部执行回执 intake 已建立，但当前没有收到真实回执。
- 当前状态：`cognee_real_external_execution_receipt_intake=pending_real_receipt`，`gap_001_ready=false`。

## verify

- 必须形成：
  - real external execution receipt intake JSON
  - intake validator
  - intake evidence
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续有人把 completed example 当成真实回执，必须退回本 intake，要求真实 receipt ref、真实计数和真实接收记录。

## debug

- 当前 full-run 的下一真实阻断点是外部执行回执未收到；模板链已经足够，下一步需要真实回执或真实执行输入。
