---
doc_id: GPCF-DOC-95CB463CBF
title: Loop Agent-Reach L3候选搜索流水线目标
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_AGENT_REACH_L3_CANDIDATE_PIPELINE.md
source_path: 02-governance/loop/LOOP_AGENT_REACH_L3_CANDIDATE_PIPELINE.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Agent-Reach L3候选搜索流水线目标

## 目标

建立 `GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001`，把 Agent-Reach 从一次性 PoC/benchmark 推进为可回放、可评分、可进入 WAES/KDS 人工评审的只读候选搜索流水线。

本目标不代表生产集成，不写 KDS canonical Markdown，不创建 GFIS source-of-record，不升级 GPCF accepted/integrated/production_ready 状态。

## 成功标准

| 项 | 标准 |
|---|---|
| 输入证据 | 必须引用 L2 zero-config、Exa local pilot、Exa fixed benchmark、candidate review |
| 执行模式 | read_only_replay_plan |
| 查询来源 | 只使用已登记固定查询集，不新增外部搜索调用 |
| 输出强度 | `kds_admission=limited_candidate_only`，`rag_admission=limited` |
| 安全 | `credential_leakage_count=0`，`production_write_count=0`，`kds_canonical_write_count=0` |
| 回滚 | 继续要求 `rollback_verified=true` |
| 评审 | 输出进入 WAES/KDS review queue，不自动 accepted 或 integrated |

## 流水线阶段

| 阶段 | 输入 | 动作 | 输出 | 门禁 |
|---|---|---|---|---|
| P0 Source Intake | 固定查询集与历史结果 | 读取已登记证据 | candidate_source_batch | provenance present |
| P1 Normalize | URL、query、channel | 去重、补齐来源字段 | normalized_candidate_set | duplicate_rate <= 20% |
| P2 Score | latency、provenance、trust hint | 计算候选评分 | scored_candidate_set | source_provenance_rate = 1.0 |
| P3 Admit | scored candidates | 标记 RAG admission | limited_admission_ledger | no strong citation |
| P4 Review | limited ledger | 交给 WAES/KDS 人工评审 | review_queue_item | no auto accept |

## 下一阶段约束

- 只允许只读 replay 和离线评分。
- 不允许配置 Cookie 或主账号登录态。
- 不允许写生产、KDS canonical、GFIS、GPC、WAES 状态。
- 不允许把搜索结果直接转为强引用。
- 不允许把本流水线作为 Agent-Reach 已生产集成证据。

## 输出产物

| 产物 | 路径 |
|---|---|
| Evidence JSON | `docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.json` |
| Evidence Markdown | `docs/harness/evidence/agent-reach-l3-candidate-pipeline-20260621.md` |
| Loop round | `docs/harness/loops/loop-round-GPCF-AGENT-REACH-L3-CANDIDATE-PIPELINE-001.md` |
| Validator | `tools/kds-sync/validate_agent_reach_l3_candidate_pipeline.py` |

## 非声明

- 不证明 Agent-Reach 已生产集成。
- Agent-Reach 未生产集成。
- Agent-Reach 未写入 KDS canonical。
- Agent-Reach 未创建 GFIS source-of-record。
- Agent-Reach 未获得 Cookie/登录态平台授权。
- Agent-Reach 未升级任何项目状态。
