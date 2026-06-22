---
doc_id: GPCF-DOC-AGENT-REACH-P8-REWORK-QUEUE-20260622
title: Agent-Reach P8 返工队列证据 2026-06-22
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p8-rework-queue-20260622.md
source_path: docs/harness/evidence/agent-reach-p8-rework-queue-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P8 返工队列证据 2026-06-22

- status: `p8_rework_queue_ready`
- source_report_status: `full_project_group_live_coverage_rework_required`
- rework_item_count: `4`
- live_external_search_invoked: `False`

## run

- 从失败的 P8 全量报告生成 query 级返工队列。
- 覆盖缺候选、查询错误、重复 URL、低分、低可追溯、缺渠道和平均分不足。

## stop

- 本轮只生成返工队列，不执行真实搜索。
- 返工执行仍需新的 P8 batch 授权。

## verify

- 自测 fixture 产生非空返工队列。
- 每个返工项都有 batch、project、channel、当前 query、建议 query 和原因。

## recover

- 若返工队列不合理，先调整建议 query 生成规则，再重新运行本验证器。

## debug

- 真实搜索执行后，如输出门禁失败，应先运行本队列生成器再申请下一轮返工授权。

## 非声明

- 本证据仅为候选证据。
- 本证据不声明 accepted / integrated / production_ready 状态。
- 本证据不写 KDS canonical Markdown。
- 本证据不写 GFIS source-of-record。
- 本证据不执行真实搜索。
