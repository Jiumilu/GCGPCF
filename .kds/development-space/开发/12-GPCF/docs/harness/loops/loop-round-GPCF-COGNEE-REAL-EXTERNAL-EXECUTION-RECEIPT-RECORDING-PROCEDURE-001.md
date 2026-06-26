---
doc_id: GPCF-DOC-LOOP-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-RECORDING-PROCEDURE-001
title: Loop Round - GPCF Cognee 真实外部执行回执登记流程 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-RECORDING-PROCEDURE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-REAL-EXTERNAL-EXECUTION-RECEIPT-RECORDING-PROCEDURE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 真实外部执行回执登记流程 001

## 输入

- `docs/harness/evidence/cognee-real-external-execution-receipt-intake-20260626.md`
- `docs/harness/evidence/cognee-full-run-readiness-rollup-20260626.md`

## run

- 定义真实外部执行回执到来后的登记步骤。
- 固化禁止输入、必跑命令和 readiness 更新边界。
- 增加 procedure validator，确保流程定义本身可审计。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：登记流程已定义，但真实外部执行回执仍未收到。
- 当前状态：`cognee_real_external_execution_receipt_recording_procedure=defined_pending_real_receipt`。

## verify

- 必须形成：
  - recording procedure JSON
  - procedure validator
  - procedure evidence
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续登记时误用 completed example 或 template receipt，必须退回本流程，重新取得真实 receipt ref 和真实计数。

## debug

- 当前流程入口已经具备；下一步需要真实外部执行回执，或者先建立真实执行授权后的回执采集责任分配。
