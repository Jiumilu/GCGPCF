---
doc_id: GPCF-DOC-AGENT-REACH-INGESTION-PLAN-20260622
title: Agent-Reach Limited Candidate Ingestion Plan 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.md
source_path: docs/harness/evidence/agent-reach-limited-candidate-ingestion-plan-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Limited Candidate Ingestion Plan 2026-06-22

本轮执行 `GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-PLAN-001`，结论为 `limited_candidate_ingestion_plan_ready`。

## 阶段目标

下一阶段目标不是生产集成，而是建立 Agent-Reach 已核验候选项的 limited candidate ingestion plan。该计划只允许生成 dry-run 候选台账，不写 KDS canonical Markdown，不创建 GFIS source-of-record，不配置生产 Agent-Reach，不升级 accepted / integrated / production_ready。

## 输入状态

| 项 | 状态 |
| --- | --- |
| authoritative source verification | `limited_verification_complete` |
| accept_limited_count | `4` |
| reject_count | `1` |
| KDS admission | `limited_candidate_only` |
| RAG admission | `limited` |
| production_integration_allowed | `false` |
| kds_canonical_write_allowed | `false` |

## 允许进入 dry-run 的候选

| id | decision | ingestion_scope | blocked_outputs |
| --- | --- | --- | --- |
| knowledge_provenance_rag | accept_limited | candidate_reference_metadata_only | KDS canonical / strong RAG / production config |
| green_supply_chain_policy | accept_limited | official_standard_metadata_reference | KDS canonical / strong RAG / GFIS source-of-record |
| ai_agent_evidence_gate | accept_limited | open_source_tool_candidate_only | tool installation / production config / WAES policy replacement |
| agent_reach_capability | accept_limited | agent_reach_capability_metadata_only | production integration / global MCP config / KDS canonical |

## 明确拒绝

| id | decision | ingestion_allowed | reason |
| --- | --- | --- | --- |
| factory_execution_traceability | reject | false | Vendor explanatory material cannot define GlobalCloud GFIS source-of-record behavior or architecture boundaries. |

## Dry-run 计划

| 控制项 | 规则 |
| --- | --- |
| execution_mode | `candidate_metadata_dry_run_only` |
| output_artifact | `agent-reach-limited-candidate-ingestion-dry-run-ledger` |
| allowed write targets | `docs/harness/evidence`, `docs/harness/loops`, `tools/kds-sync` |
| blocked write targets | KDS canonical Markdown、GFIS source-of-record、production configuration、global MCP configuration、strong RAG corpus |
| promotion requirement | required fields 完整、source provenance 显式、review status 保持 limited、rollback 不触碰 canonical、status_upgrade_allowed=false |

## 质量门禁

- candidate_count 必须为 `4`。
- rejected_count 必须为 `1`。
- 每条候选必须带 source provenance、accepted scope、verification reason、review status。
- credential leakage、canonical write、production write 均必须为 `0`。
- 不允许 accepted / integrated / production_ready 声明。

## 下一轮

进入 `GPCF-AGENT-REACH-LIMITED-CANDIDATE-INGESTION-DRY-RUN-001`：按本计划生成 dry-run ledger，并验证 4 条 limited candidate 可回放、1 条 reject 不进入摄取。
