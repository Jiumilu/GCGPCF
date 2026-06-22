---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-QUALITY-REGRESSION-001
title: GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001
project: GPCF
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001

## 输入

- 上轮输出：`GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001`
- 质量基线：search success、source provenance、duplicate、latency、candidate ingestion safety
- 主边界：`limited_candidate_only`

## 动作

- 定义搜索质量回归门禁。
- 定义候选摄取安全门禁。
- 定义 status upgrade 阻断门禁。
- 定义 5 条负向夹具。
- 新增 validator，重放质量趋势基线 validator 并校验回归门禁定义。

## 输出

- `docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.json`
- `docs/harness/evidence/agent-reach-candidate-quality-regression-gate-20260622.md`
- `tools/kds-sync/validate_agent_reach_candidate_quality_regression_gate.py`

## 检查

- regression_gate_count=`8`。
- negative_fixture_count=`5`。
- source_provenance_rate 必须保持 `1.0`。
- canonical_write_count 必须保持 `0`。
- production_write_count 必须保持 `0`。
- KDS admission 必须保持 `limited_candidate_only`。

## 反馈

本轮将 Agent-Reach 候选搜索质量基线转成回归门禁。下一轮才能执行 fixture replay；本轮不调用 live search，也不执行生产集成。

## 非声明

- 不声明 Agent-Reach 已生产集成。
- 不声明 live external search 已重新调用。
- 不声明 KDS canonical write 已执行。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

`GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-FIXTURE-REPLAY-001`
