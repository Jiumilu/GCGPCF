---
doc_id: GPCF-DOC-LOOP-COGNEE-FULL-OBJECT-COVERAGE-TEMPLATE-001
title: Loop Round - GPCF Cognee 全量对象覆盖模板 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-FULL-OBJECT-COVERAGE-TEMPLATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-FULL-OBJECT-COVERAGE-TEMPLATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 全量对象覆盖模板 001

## 输入

- `docs/harness/evidence/cognee-full-run-admission-package-20260626.md`
- `docs/harness/evidence/cognee-full-run-ledger-template-20260626.md`

## run

- 为 `COGNEE-FULL-RUN-GAP-002` 建立全量对象覆盖模板。
- 固化对象清单、对象分组、排除记录、覆盖率和账本回链字段。
- 增加对象覆盖 validator，用于区分 `template_only` 与真实覆盖。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：全量对象覆盖模板已建立，但仍缺真实全量对象清单和覆盖统计。
- 当前状态：`cognee_full_object_coverage_template=prepared`，`full_run_claim=false`。

## verify

- 必须形成：
  - full object coverage JSON template
  - full object coverage validator
  - full object coverage evidence
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`
  - `full_run_claim=false`

## recover

- 若后续对象覆盖统计没有对象清单来源或排除记录，必须退回本模板补齐，不得直接升级 full-run。

## debug

- 本轮只关闭“对象覆盖模板缺失”这一工程缺口；真实对象覆盖仍需真实 inventory 和覆盖统计支撑。
