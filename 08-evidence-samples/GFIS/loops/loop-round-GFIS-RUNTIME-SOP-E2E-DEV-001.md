---
doc_id: GPCF-DOC-365757D092
title: GFIS-RUNTIME-SOP-E2E-DEV-001
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-DEV-001.md
source_path: 08-evidence-samples/GFIS/loops/loop-round-GFIS-RUNTIME-SOP-E2E-DEV-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GFIS-RUNTIME-SOP-E2E-DEV-001

## 目标

建立 GFIS 运行层 SOP E2E 开发态 synthetic master data + schema，覆盖葛化绿色供应链 12 个 SOP 阶段。

## 产出

- `docs/harness/sop-e2e/synthetic-fixtures/synthetic-gehu-sop-e2e-master.json`
- `docs/harness/sop-e2e/synthetic-fixtures/synthetic-gehu-sop-e2e.schema.json`

## 关键约束

- `synthetic=true`
- `dev_only=true`
- `dry_run=true`
- `not_source_of_record=true`
- `not_business_verified=true`
- 不进入真实 source-of-record 接收目录
- 不触发真实 runtime primary key
- 不触发真实 WAES/KDS 写入

## 状态

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 2
- batch_generated: false
- substance_gate: pass
- stop_type: continue_to_dev_002
