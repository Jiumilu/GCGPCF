---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001
title: LOOP Round GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P7-OUTPUT-QUALITY-GATE-001

## run

- 输入：P7 runner、P6 dry-run 准备包、P7 execution harness guard。
- 动作：新增 P7 live dry-run 输出质量 validator，并用内存正向样例自测。
- 输出：validator、evidence、Loop 轮次文档。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮未收到 P7 执行授权，不执行真实搜索；只建立执行后验收门禁。

## verify

- `validate_agent_reach_p7_limited_live_search_output.py --self-test` 必须通过。
- `validate_agent_reach_p7_limited_live_search_output.py --negative-test missing-query` 必须证明缺 query 会失败。
- `validate_agent_reach_p7_limited_live_search_output.py --negative-test query-error` 必须证明 query error 会失败。
- `validate_agent_reach_p7_limited_live_search_output.py --negative-test raw-payload` 必须证明 raw payload 持久化会失败。
- `validate_agent_reach_p7_limited_live_search_output.py --negative-test duplicate-url` 必须证明重复 URL 会失败。
- `validate_agent_reach_p7_limited_live_search_output.py --negative-test missing-channel` 必须证明缺通道候选会失败。
- validator 必须要求 `limited_live_search_dry_run_completed`。
- validator 必须要求 `authorization_valid=true`、`execution_requested=true`、`live_external_search_invoked=true`。
- validator 必须要求 `query_candidate_coverage=1.0` 且 `query_error_count=0`。
- validator 必须要求 `channel_candidate_coverage=1.0` 且 `duplicate_url_count=0`。
- validator 必须检查候选 schema、授权范围、质量阈值、安全边界、非声明和 raw payload 禁止持久化。

## recover

- 若 P7 runtime evidence 未通过 validator，删除 P7 runtime evidence，保留本轮 output quality gate evidence。
- 若 validator 误判，先补充最小 fixture 再修复 validator，不降低质量阈值。

## debug

- 当前阻塞：缺少 P7 执行授权文件，无法产生真实 runtime evidence。
- 下一轮：`GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001`
