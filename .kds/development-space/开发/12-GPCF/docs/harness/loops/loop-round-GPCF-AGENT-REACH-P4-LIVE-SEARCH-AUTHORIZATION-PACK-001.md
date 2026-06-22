---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001
title: LOOP Round GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P4-LIVE-SEARCH-AUTHORIZATION-PACK-001

## 输入

- P3 证据：`docs/harness/evidence/agent-reach-p3-quality-replay-harness-20260622.json`
- 当前准入：`limited_candidate_only`
- 当前授权状态：`pending_human_authorization`

## 动作

- 建立真实搜索授权模板。
- 建立授权负向用例。
- 建立授权边界文档。
- 建立 P4 证据和本地验证器。

## 输出

- `fixtures/agent-reach/live-search-authorization-pack.template.json`
- `fixtures/agent-reach/live-search-authorization-negative-fixtures.json`
- `third_party/agent-reach/LIVE_SEARCH_AUTHORIZATION.md`
- `tools/kds-sync/validate_agent_reach_p4_live_search_authorization_pack.py`
- `docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.json`
- `docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.md`

## 检查

- 授权状态保持 `pending_human_authorization`。
- `live_search_authorized` 保持 `false`。
- 负向用例全部预期拒绝。
- 不调用真实搜索。
- 不调用 Agent-Reach binary。
- 不写入 KDS canonical、GFIS source-of-record、生产配置或全局 MCP 配置。

## 反馈

本轮只完成真实搜索前置授权包。它不是授权本身，也不是搜索质量验收。

## 下一轮

进入 `GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001`。若仍未收到完整真人授权包，下一轮只能继续执行授权前检查或等待授权，不得执行真实搜索。
