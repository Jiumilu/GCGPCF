---
doc_id: GPCF-DOC-980866F10E
title: Agent-Reach Candidate Search Review Evidence 20260620
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-candidate-search-review-20260620.md
source_path: docs/harness/evidence/agent-reach-candidate-search-review-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Candidate Search Review Evidence 20260620

## 结论

Agent-Reach 可进入 WAES/KDS 候选搜索能力 review，状态为 `ready_for_review`。本结论只覆盖候选搜索、证据回放和质量评估，不代表生产集成、KDS canonical 写入、GFIS source-of-record 创建或项目状态升级。

## 证据链

| 证据 | 作用 | 结论 |
|---|---|---|
| `docs/harness/evidence/agent-reach-zero-config-repair-20260620.json` | 零配置公开通道修复 | web/github/rss 可作为公开候选搜索入口 |
| `docs/harness/evidence/agent-reach-exa-local-pilot-20260620.json` | 授权范围内 Exa local pilot | Exa search 可临时配置、可查询、可回滚 |
| `docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json` | 固定查询集质量基准 | 5/5 查询成功，URL provenance 完整 |

## 指标

| 指标 | 值 |
|---|---|
| zero_config_success_rate | 1.0 |
| exa_fixed_query_success_rate | 1.0 |
| source_provenance_rate | 1.0 |
| latency_p50_seconds | 3.889 |
| latency_p95_seconds | 4.633 |
| credential_leakage_count | 0 |
| production_write_count | 0 |
| kds_canonical_write_count | 0 |
| rollback_verified | true |

## 准入边界

| 字段 | 判定 |
|---|---|
| waes_review_status | `ready_for_review` |
| kds_admission | `limited_candidate_only` |
| rag_admission | `limited` |
| status_upgrade_allowed | false |
| production_integration_allowed | false |
| accepted_or_integrated_claim_allowed | false |

## 持续进化控制

- 固定查询集必须可回放，并继续记录成功率、延迟和 URL provenance。
- 候选搜索进入 KDS/RAG 前必须经过下游人工或 WAES 评审。
- `source_provenance_rate` 必须保持 1.0 才能作为候选准入输入。
- Exa/MCP 配置必须保持临时隔离并完成 rollback verified。
- Cookie 或登录态平台不得继承本轮结论，必须另设授权、脱敏和回滚门禁。

## 非声明

- 不证明 Agent-Reach 已生产集成。
- 不写 KDS canonical Markdown。
- 不创建 GFIS source-of-record。
- 不升级 GPCF accepted/integrated/production_ready 状态。
- 不把 Exa 结果转成强 RAG 引用。
- 不纳入 Twitter/Reddit/Xiaohongshu 等 Cookie 或登录态通道。

## 下一门禁

`waes_kds_review_or_l3_candidate_pipeline`
