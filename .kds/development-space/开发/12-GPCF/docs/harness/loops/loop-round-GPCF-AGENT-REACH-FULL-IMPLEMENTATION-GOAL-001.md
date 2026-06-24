---
doc_id: GPCF-DOC-AGENT-REACH-FULL-GOAL-LOOP-20260622
title: Loop Round GPCF Agent-Reach Full Implementation Goal 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF Agent-Reach Full Implementation Goal 001

## 输入

- 用户目标：在项目群及 Loop 中实现 Agent-Reach 全量能力。
- 当前边界：`limited_candidate_only`。
- 上游核验：`Panniantong/Agent-Reach` HEAD `22d7f03a59401b5740b380c3ad43e3ff7a9dc373`。

## 动作

- 建立目标：Agent-Reach 全量能力实施提示词与阶段计划。
- 核验上游仓库结构、版本、CLI、通道 registry 和 doctor 能力。
- 生成全量实施方案与执行提示词。
- 生成本轮 evidence 和 validator。

## 输出

- `02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md`
- `docs/harness/evidence/agent-reach-full-implementation-goal-20260622.json`
- `docs/harness/evidence/agent-reach-full-implementation-goal-20260622.md`
- `tools/kds-sync/validate_agent_reach_full_implementation_goal.py`

## 检查

- current_admission 必须保持 `limited_candidate_only`。
- production_integration_allowed 必须为 `false`。
- kds_canonical_write_allowed 必须为 `false`。
- live_external_search_invoked 必须为 `false`。
- phase_count 必须为 `9`。
- capability_domain_count 必须不小于 `17`。
- project_scope_count 必须为 `14`。

## 反馈

本轮只是把“全量能力”转成受控实施提示词和阶段目标。下一轮才能进入 P0 Source Lock；未进入 P6/L3.5 前不执行真实接口读验证，未进入 P8 且未人工批准前不允许生产准入。

## 下一轮

`GPCF-AGENT-REACH-P0-SOURCE-LOCK-001`
