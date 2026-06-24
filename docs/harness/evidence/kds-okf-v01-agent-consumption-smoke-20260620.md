---
doc_id: GPCF-DOC-931CDE09CE
title: KDS OKF v0.1 Agent 消费 smoke 测试证据
project: KDS
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md
source_path: docs/harness/evidence/kds-okf-v01-agent-consumption-smoke-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# KDS OKF v0.1 Agent 消费 smoke 测试证据

generated_at: 2026-06-22T01:27:02.819197+00:00

## 范围

本 smoke test 检查 agent-style keyword queries 是否能从 OKF v0.1 派生 bundle 中找回预期的 KDS source document。它不是 semantic search benchmark，也不证明业务完成。

## 摘要

| metric | value |
| --- | --- |
| status | pass |
| bundle | `.okf/bundles/kds-v0.1` |
| concepts | 36 |
| queries | 4 |

## 结果

| query | expected_source_path | top_source_path | top_okf_path | status |
| --- | --- | --- | --- | --- |
| KDS 开发空间安全规范 | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `.okf/bundles/kds-v0.1/concepts/02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | pass |
| ODF Phase 7 小批量样本 | `09-status/odf-phase7-small-batch-execution-plan.md` | `09-status/odf-phase7-small-batch-execution-plan.md` | `.okf/bundles/kds-v0.1/concepts/09-status/odf-phase7-small-batch-execution-plan.md` | pass |
| KDS OKF v0.1 全量派生层实施方案 | `09-status/kds-okf-v01-full-implementation-plan.md` | `09-status/kds-okf-v01-full-implementation-plan.md` | `.okf/bundles/kds-v0.1/concepts/09-status/kds-okf-v01-full-implementation-plan.md` | pass |
| KDS Markdown 化 OKF 兼容层闭环方案 | `09-status/kds-md-okf-implementation-closure-plan.md` | `09-status/kds-md-okf-implementation-closure-plan.md` | `.okf/bundles/kds-v0.1/concepts/09-status/kds-md-okf-implementation-closure-plan.md` | pass |

## 边界

- OKF 是派生消费层。
- KDS/Git 受控文档仍是 source of record。
- 本测试只验证 discoverability，不验证 acceptance 或 integration status。
