---
doc_id: GPCF-DOC-LOOP-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-004
title: Loop Round - GPCF Cognee 外部执行正式回执与回填清单 004
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-004.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 外部执行正式回执与回填清单 004

## 输入

- `docs/harness/evidence/cognee-external-execution-fixed-command-pack-20260626.md`
- `docs/harness/evidence/cognee-external-execution-postfill-evidence-draft-20260626.md`
- `docs/harness/evidence/cognee-external-execution-receipt-completed-example-20260626.md`

## run

- 输出真实执行后的正式回执模板。
- 输出真实执行后的回填检查清单。
- 固化“外部执行验证完成”与“全量运行完成”之间的边界。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：已具备回执模板与回填清单，但仍缺真实外部执行回执。
- 当前状态：`external_execution_receipt_template=prepared`，`external_execution_postfill_checklist=ready`，`full_run_claim=false`。

## verify

- 必须新增：
  - 正式回执模板
  - 回填检查清单
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若真实执行后回填出现歧义，统一回到本轮模板与清单，不得并行产生第二套回执结构。

## debug

- 当前最短路径仍然是“等待真实执行并按既定模板回填”，不是提前宣布 Cognee 已经 full-run。
