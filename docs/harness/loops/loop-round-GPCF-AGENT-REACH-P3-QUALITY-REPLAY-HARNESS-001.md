---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001
title: Agent-Reach P3 离线质量 Replay Harness Loop 记录
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P3 离线质量 Replay Harness Loop 记录

## 输入

- P2 受控 adapter skeleton 已完成，状态为 `controlled_adapter_skeleton_ready`。
- 当前准入仍为 `limited_candidate_only`。
- 本轮目标是建立 offline replay harness，不调用真实搜索。

## 动作

- 新增 `fixtures/agent-reach/quality-replay-harness.json`。
- 新增 `tools/kds-sync/run_agent_reach_quality_replay_harness.py`。
- 新增 `third_party/agent-reach/QUALITY_REPLAY_HARNESS.md`。
- 定义固定查询集、候选结果结构、评分字段、阈值和 forbidden claims。

## 输出

- `third_party/agent-reach/QUALITY_REPLAY_HARNESS.md`
- `fixtures/agent-reach/quality-replay-harness.json`
- `tools/kds-sync/run_agent_reach_quality_replay_harness.py`
- `tools/kds-sync/validate_agent_reach_p3_quality_replay_harness.py`
- `docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.json`
- `docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.md`

## 检查

- query_count 为 `3`。
- candidate_count 为 `5`。
- average_score 为 `0.882`，高于 `0.78`。
- precision_at_1 为 `1.0`，高于 `0.66`。
- required_field_coverage 为 `1.0`。
- forbidden_claim_count 为 `0`。
- `live_external_search_invoked=false`。

## 反馈

- P3 只证明质量 replay 口径和离线回归门禁可执行，不证明真实搜索质量。
- 下一轮必须先建立真实搜索授权包，明确允许通道、时间窗、凭据边界、日志脱敏、回滚和验收指标。
- 未取得授权前，不进入真实搜索、凭据读取、browser cookie 抽取或全局 MCP 配置。

## 下一轮

进入 `GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001`。
