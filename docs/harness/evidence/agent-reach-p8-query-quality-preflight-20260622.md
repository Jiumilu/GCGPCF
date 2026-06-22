---
doc_id: GPCF-DOC-AGENT-REACH-P8-QUERY-QUALITY-PREFLIGHT-20260622
title: Agent-Reach P8 查询质量预检证据 2026-06-22
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-query-quality-preflight-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P8 查询质量预检证据 2026-06-22

- status: `p8_query_quality_preflight_pass`
- query_count: `14`
- project_coverage: `1.0`
- channel_coverage: `1.0`
- duplicate_normalized_query_count: `0`
- failing_query_count: `0`
- live_external_search_invoked: `False`

## run

- 对 P8 三批 14 条计划查询执行离线质量预检。
- 检查项目词、意图词、非泛化词、长度、重复查询和渠道范围。

## stop

- 本轮只校验查询计划，不执行真实搜索。
- 若后续修改查询计划，必须重新运行本预检。

## verify

- 14/14 项目仍在计划覆盖内。
- web/rss/bilibili 三类渠道仍在计划覆盖内。
- 预检不创建授权文件，不调用外部网络。

## recover

- 若预检失败，优先修订对应 query 文本，不扩大 batch 数量或授权范围。

## debug

- 下一步仍需 P8 三批执行授权，授权后才能运行真实搜索 pipeline。

## 非声明

- 本证据仅为候选证据。
- 本证据不声明 accepted / integrated / production_ready 状态。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
- 本证据不持久化 raw provider payload。
