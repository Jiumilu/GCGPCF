---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-REWORK-QUEUE-001
title: Agent-Reach P8 返工队列 Loop 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-REWORK-QUEUE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-REWORK-QUEUE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Agent-Reach P8 返工队列 Loop 001

## run

建立失败搜索输出到下一轮 query 返工队列的转换闭环。

## stop

停止类型为 `authorization_boundary`；队列状态 `p8_rework_queue_ready`。

## verify

返工项数量 `4`；真实外搜 `False`。

## recover

回滚为删除本轮新增验证器和 evidence/loop 文档。

## debug

真实搜索仍等待 P8 执行授权；返工执行也必须重新授权。
