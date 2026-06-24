---
doc_id: GPCF-DOC-9B7D44D8F2
title: Loop Round - GPCF-CODEGRAPH-TASK-INTAKE-GATE-001
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-TASK-INTAKE-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-TASK-INTAKE-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - GPCF-CODEGRAPH-TASK-INTAKE-GATE-001

## 输入

- 现有 CodeGraph 准入、Harness 门禁、影响指标基线与归一化清单已经建立。
- 需要把“任务开工前必过 CodeGraph”沉到可回放的门禁证据。

## 动作

1. 建立任务 Intake 门禁文档。
2. 建立任务 Intake 门禁 validator。
3. 建立 task intake gate evidence 与正负例 fixture。
4. 将门禁纳入 Harness/Loop 索引。

## 输出

- `docs/codegraph/codegraph-task-intake-gate.md`
- `tools/kds-sync/validate_codegraph_task_intake_gate.py`
- `docs/harness/evidence/codegraph-task-intake-gate-20260623.json`
- `docs/harness/evidence/codegraph-task-intake-gate-20260623.md`

## 检查

- `python3 tools/kds-sync/validate_codegraph_task_intake_gate.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

任务开工前门禁已可以通过正负例回放，`affected_tests=[]` 无 fallback 时会阻断进入实现。

## 下一轮

将任务 Intake 门禁作为后续真实业务任务的默认入口，再继续保持 14 仓监控与 GPCF/Studio drift watch。
