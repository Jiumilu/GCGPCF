---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001
title: LOOP Round GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P5-LIVE-SEARCH-PRECHECK-001

## 输入

- P4 授权包：`docs/harness/evidence/agent-reach-p4-live-search-authorization-pack-20260622.json`
- 授权提交：`fixtures/agent-reach/live-search-precheck-authorization-submission-20260622.json`
- 当前准入：`limited_candidate_only`

## 动作

- 解析授权人、授权窗口、允许通道、查询上限、禁止动作。
- 校验授权窗口是否为具体 ISO-8601 时间。
- 校验是否满足 P4 授权边界。
- 未通过时阻断真实搜索。

## 输出

- `fixtures/agent-reach/live-search-precheck-authorization-submission-20260622.json`
- `tools/kds-sync/validate_agent_reach_p5_live_search_precheck.py`
- `docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.json`
- `docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.md`

## 检查

- 授权人存在：通过。
- 允许通道在 P4 边界内：通过。
- 查询上限在 P4 边界内：通过。
- 禁止动作保留：通过。
- `authorized_at` 为具体 ISO-8601：失败。
- `expires_at` 为具体 ISO-8601：失败。
- `expires_at` 晚于 `authorized_at`：无法判断。

## 反馈

本轮预检拒绝授权，不执行真实搜索。拒绝原因是授权有效期仍包含 `<开始时间>` 和 `<结束时间>` 占位符。

## 下一轮

进入 `GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001`。补充具体有效期后，才允许再次执行授权预检。
