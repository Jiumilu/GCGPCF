---
doc_id: GPCF-DOC-LOOP-COGNEE-FULL-SCENARIO-MATRIX-TEMPLATE-001
title: Loop Round - GPCF Cognee 全量场景矩阵模板 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-FULL-SCENARIO-MATRIX-TEMPLATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-FULL-SCENARIO-MATRIX-TEMPLATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 全量场景矩阵模板 001

## 输入

- `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- `docs/harness/evidence/cognee-full-run-ledger-template-20260626.md`
- `docs/harness/evidence/cognee-full-object-coverage-template-20260626.md`

## run

- 为 `COGNEE-FULL-RUN-GAP-003` 建立全量场景矩阵模板。
- 固化场景清单、场景分组、失败记录、排除记录、通过率和账本回链字段。
- 增加场景矩阵 validator，用于区分 `template_only` 与真实场景矩阵。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：全量场景矩阵模板已建立，但仍缺真实全量场景清单、执行记录和通过统计。
- 当前状态：`cognee_full_scenario_matrix_template=prepared`，`full_run_claim=false`。

## verify

- 必须形成：
  - full scenario matrix JSON template
  - full scenario matrix validator
  - full scenario matrix evidence
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续场景矩阵缺少场景清单来源、失败记录或排除记录，必须退回本模板补齐，不得直接升级 full-run。

## debug

- 本轮只关闭“场景矩阵模板缺失”这一工程缺口；真实场景通过仍需真实 scenario inventory 和执行记录支撑。
