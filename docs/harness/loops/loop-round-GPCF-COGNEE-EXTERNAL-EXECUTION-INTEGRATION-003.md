---
doc_id: GPCF-DOC-LOOP-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-003
title: Loop Round - GPCF Cognee 外部执行固定命令包与回填草稿 003
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-003.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee 外部执行固定命令包与回填草稿 003

## 输入

- `docs/harness/evidence/cognee-external-execution-integration-intake-20260626.md`
- `docs/harness/evidence/cognee-external-execution-integration-validation-20260626.md`
- `fixtures/cognee/cognee-external-execution-receipt.completed.example.json`

## run

- 冻结外部执行前固定命令包。
- 输出真实执行后的标准回填 evidence 草稿。
- 保证后续真实执行时只需要回填结果，不再重新设计字段结构。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：已完成执行前命令包和执行后回填结构，但仍未取得真实执行回执。
- 当前状态：`external_execution_command_pack=prepared`，`external_execution_postfill_evidence=draft_ready`，`production_write=false`，`accepted=false`，`integrated=false`，`production_ready=false`。

## verify

- 必须形成：
  - 固定命令包
  - 预期门禁结果
  - postfill evidence draft
- 必须保持：
  - `production_write=false`
  - `accepted=false`
  - `integrated=false`
  - `production_ready=false`

## recover

- 若后续真实执行产生结果但无法回填：以本草稿为唯一结构源，禁止重新发散到多份冲突文档。

## debug

- 当前最短路径已经从“补参数”转成“等真实执行回执后回填结果”，而不是继续扩写更多说明文档。
