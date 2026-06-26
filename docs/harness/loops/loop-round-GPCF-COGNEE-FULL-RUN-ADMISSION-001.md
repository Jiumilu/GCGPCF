---
doc_id: GPCF-DOC-LOOP-COGNEE-FULL-RUN-ADMISSION-001
title: Loop Round - GPCF Cognee 全量运行准入包 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-FULL-RUN-ADMISSION-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-FULL-RUN-ADMISSION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 全量运行准入包 001

## 输入

- `docs/harness/evidence/cognee-full-run-gap-checklist-20260626.md`
- `docs/harness/evidence/cognee-external-execution-postfill-checklist-20260626.md`
- `docs/harness/evidence/cognee-external-execution-receipt-template-20260626.md`

## run

- 把 Cognee 从外部执行验证进入 full-run 前的准入条件收束成单一 evidence。
- 明确哪些前置已经具备，哪些 gap 仍阻断 full-run admission。
- 生成下一轮最小动作：全量运行账本模板、全量对象覆盖模板、全量场景矩阵模板。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：full-run admission package 已形成，但 `external_execution_validation_recorded=false`，且 full object / scenario / ledger 仍未闭合。
- 当前状态：`cognee_full_run_admission=not_admitted`，`full_run_claim=false`。

## verify

- 必须形成：
  - full-run admission package
  - admission gate 字段
  - 下一轮最小动作
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续出现“外部执行验证完成即 full-run 完成”的错误结论，回退到本准入包，以五个 gap 为准入门槛。

## debug

- 当前主要阻断不是签核或 intake，而是真实外部执行回执、全量对象覆盖、全量场景覆盖、生产状态提升证据和全量运行账本。
