---
doc_id: GPCF-DOC-LOOP-COGNEE-FULL-RUN-LEDGER-TEMPLATE-001
title: Loop Round - GPCF Cognee 全量运行账本模板 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-FULL-RUN-LEDGER-TEMPLATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-FULL-RUN-LEDGER-TEMPLATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 全量运行账本模板 001

## 输入

- `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- `docs/harness/evidence/cognee-full-run-gap-checklist-20260626.md`

## run

- 为 `COGNEE-FULL-RUN-GAP-005` 建立全量运行账本模板。
- 固化 batch、record、exception、coverage 和状态边界字段。
- 增加账本模板 validator，用于区分 `template_only` 与真实账本。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：账本模板已建立，但仍缺真实外部执行回执、全量对象覆盖和全量场景覆盖。
- 当前状态：`cognee_full_run_ledger_template=prepared`，`full_run_claim=false`。

## verify

- 必须形成：
  - full-run ledger JSON template
  - ledger validator
  - ledger evidence
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续真实账本与本模板字段冲突，必须先修订模板并保留替代关系，不得直接用冲突账本升级 full-run。

## debug

- 本轮只关闭“账本模板缺失”这一工程缺口；真实 full-run ledger 仍需真实外部执行和覆盖证据支撑。
