---
doc_id: GPCF-DOC-8C267BC542
title: CodeGraph WAES 门禁说明
project: KDS
related_projects: [PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-waes-gate.md
source_path: docs/codegraph/codegraph-waes-gate.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# CodeGraph WAES 门禁说明

WAES 使用 CodeGraph 作为高风险变更的影响分析输入，而不是把 CodeGraph 作为裁决者。

强制门禁范围：

- 权限、RBAC、认证。
- 租户隔离。
- 资金、结算、积分、收益池。
- WAES 规则。
- KDS schema。
- Ontology/WAS schema。
- API contract。
- Harness/Loop policy。
- 多 Agent 协议。

WAES gate 至少需要：

- `codegraph_impact_report`
- `changed_files`
- `impacted_symbols`
- `impacted_tests`
- `risk_score`
- `evidence_bundle`

输出只能是 `pass`、`conditional_pass`、`reject` 或 `require_committee_review`。AI Agent 不能代替人员或委员会批准。
