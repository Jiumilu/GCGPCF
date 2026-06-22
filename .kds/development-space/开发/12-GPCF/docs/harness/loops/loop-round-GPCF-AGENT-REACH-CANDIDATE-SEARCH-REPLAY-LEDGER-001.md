---
doc_id: GPCF-DOC-9B31D33243
title: GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-CANDIDATE-SEARCH-REPLAY-LEDGER-001

## 输入

上一轮 `GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001` 要求生成 `candidate_search_replay_ledger`。本轮只读取既有 Exa fixed benchmark evidence，形成可复核候选台账。

## 动作

| # | 动作 | 说明 |
|---|---|---|
| 1 | 读取固定查询结果 | 使用 `agent-reach-exa-fixed-benchmark-20260620.json` |
| 2 | 生成台账 | 记录 query id、URL、延迟、provenance、admission |
| 3 | 标记评审状态 | 全部为 `pending_waes_kds_review` |
| 4 | 生成 validator | 校验不调用外部搜索、不写 canonical、不升级状态 |

## 输出

| 产物 | 路径 |
|---|---|
| Evidence JSON | `docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.json` |
| Evidence Markdown | `docs/harness/evidence/agent-reach-candidate-search-replay-ledger-20260621.md` |
| Validator | `tools/kds-sync/validate_agent_reach_candidate_search_replay_ledger.py` |

## 检查

| 检查项 | 当前结果 |
|---|---|
| external_search_invoked | false |
| entry_count | 5 |
| search_success_rate | 1.0 |
| source_provenance_rate | 1.0 |
| duplicate_rate | 0.0 |
| kds_admission | limited_candidate_only |
| rag_admission | limited |
| review_status | pending_waes_kds_review |
| status_upgrade_allowed | false |
| production_integration_allowed | false |

## 反馈

Agent-Reach 候选搜索结果已进入可回放台账，但仍未进入强引用或 canonical。下一门禁是把台账转为 WAES/KDS 人工评审队列，记录每条候选结果的 accept/reject/defer 原因。

## 轮次真实性

| 字段 | 值 |
|---|---|
| declared_rounds | 1 |
| substantive_rounds | 1 |
| generated_items | 3 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 非声明

- 本轮不调用新的外部搜索。
- 本轮不证明 Agent-Reach 已生产集成。
- 本轮不写 KDS canonical。
- 本轮不创建 GFIS source-of-record。
- 本轮不授权生产写入。
- 本轮不升级任何项目状态。
