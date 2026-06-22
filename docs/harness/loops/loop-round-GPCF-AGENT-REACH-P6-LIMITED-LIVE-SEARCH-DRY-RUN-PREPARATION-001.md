---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001
title: LOOP Round GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001

## run

- 输入：`docs/harness/evidence/agent-reach-p5b-live-search-precheck-corrected-authorization-20260622.json`
- 动作：建立最小真实搜索 dry-run 的 query 清单、输出契约、质量阈值、日志脱敏和回滚计划。
- 输出：P6 fixture、evidence、Loop 轮次文档和验证器。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮只准备 P7 dry-run，不执行真实搜索；P7 仍需要显式执行授权。

## verify

- query_count 为 `5`，未超过 P5B 上限。
- allowed_channels 为 `web` / `rss` / `bilibili`，未超出 P4/P5B 边界。
- max_results_per_query 为 `10`。
- 候选记录 schema、质量阈值、日志脱敏、回滚计划均已定义。
- 真实搜索调用：未执行。

## recover

- P7 若失败，只删除 P7 输出证据，不覆盖 P6 准备证据。
- 若 query 清单需要收窄，追加 P6B 修订证据，不覆盖本轮证据。

## debug

- 当前阻塞：P7 执行前还缺少明确 live dry-run 执行授权。
- 下一轮：`GPCF-AGENT-REACH-P7-LIMITED-LIVE-SEARCH-DRY-RUN-001`
- P7 授权必须说明是否允许调用 Agent-Reach binary；若不允许，只能使用受控外部读取替代路径。
