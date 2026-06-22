---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-INGESTION-PLAN-001
title: GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001

## 输入

- 上轮主线恢复：`GPCF-AGENT-REACH-RECENTER-001`
- 上轮下一门禁：`limited_candidate_ingestion_plan`
- 已核验状态：4 条 `accept_limited`，1 条 `reject`，KDS admission 仍为 `limited_candidate_only`。

## 动作

- 读取 Agent-Reach recenter、authoritative source verification 和 candidate replay ledger。
- 定义 4 条 limited candidate 的 dry-run record schema。
- 定义 1 条 reject 的禁止摄取规则。
- 定义 dry-run 允许写入范围和 blocked write targets。
- 新增 validator，重放上游 Agent-Reach validator 并校验本计划。

## 输出

- `docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.json`
- `docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.md`
- `tools/kds-sync/validate_agent_reach_limited_candidate_ingestion_plan.py`

## 检查

- candidate_count=`4`。
- rejected_count=`1`。
- `factory_execution_traceability` 不允许进入摄取。
- KDS admission 保持 `limited_candidate_only`。
- canonical write、production write、strong RAG upgrade 均为 false。
- 下一轮为 dry-run ledger，不是生产集成。

## 反馈

本轮把 Agent-Reach 主线从“已核验 limited candidate”推进到“可执行 dry-run ingestion plan”。这仍是候选摄取计划，不是 KDS canonical 写入，不是生产 Agent-Reach 集成。

## 非声明

- 不声明 Agent-Reach 已生产集成。
- 不声明 KDS canonical write 已执行。
- 不声明 GFIS source-of-record 已创建。
- 不声明 limited candidates 已成为强 RAG 引用。
- 不声明 accepted / integrated / production_ready。

## 下一轮

`GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001`
