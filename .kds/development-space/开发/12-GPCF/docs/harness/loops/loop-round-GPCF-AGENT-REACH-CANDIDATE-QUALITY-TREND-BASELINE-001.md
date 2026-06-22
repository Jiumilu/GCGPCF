---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-QUALITY-TREND-001
title: GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001
project: GPCF
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-CANDIDATE-QUALITY-TREND-BASELINE-001

## 输入

- 上轮输出：`GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001`
- 搜索回放来源：`agent-reach-candidate-search-replay-ledger-20260621.json`
- 候选摄取来源：`agent-reach-limited-candidate-ingestion-dry-run-ledger-20260622.json`

## 动作

- 汇总搜索回放质量指标。
- 汇总候选摄取 dry-run 质量指标。
- 建立趋势 metric 和 guardrail。
- 保持 `limited_candidate_only` 和 `limited` admission。
- 新增 validator，重放上游 dry-run validator 并校验质量基线。

## 输出

- `docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.json`
- `docs/harness/evidence/agent-reach-candidate-quality-trend-baseline-20260622.md`
- `tools/kds-sync/validate_agent_reach_candidate_quality_trend_baseline.py`

## 检查

- search_success_rate=`1.0`。
- source_provenance_rate=`1.0`。
- duplicate_rate=`0.0`。
- candidate_count=`4`。
- rejected_count=`1`。
- canonical_write_count=`0`。
- production_write_count=`0`。
- status_upgrade_allowed=`false`。

## 反馈

本轮建立了 Agent-Reach 候选搜索和候选摄取的质量趋势基线。它支持后续持续进化检查，但不代表生产集成或 KDS canonical 写入。

## 非声明

- 不声明 Agent-Reach 已生产集成。
- 不声明 live external search 已重新调用。
- 不声明 KDS canonical write 已执行。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

`GPCF-AGENT-REACH-CANDIDATE-QUALITY-REGRESSION-GATE-001`
