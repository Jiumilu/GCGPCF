---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001
title: LOOP Round GPCF-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P8-BATCH-MERGE-RUNNER-001

## run

- 输入：P8 三批 batch runtime evidence 约定路径。
- 动作：建立三批结果合并器和合并器 readiness validator。
- 输出：P8 merge runner evidence、Loop 轮次文档和本地验证器。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮只建立合并器，不执行真实搜索。

## verify

- 缺少 batch evidence 时阻断：通过。
- 三批自测数据可合并：通过。
- 合并结果可通过全量质量 validator：通过。
- 真实搜索调用：未执行。
- accepted / integrated / production_ready 声明：未声明。

## recover

- 若后续某批 evidence 不通过，删除合并产物，保留各批 runtime evidence 和本轮合并器 readiness evidence。
- 若全量 validator 失败，先修复对应 batch evidence，不直接编辑合并产物绕过质量门禁。

## debug

- 当前阻塞：缺少真实三批 batch runtime evidence。
- 下一轮：`GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`
- 下一轮不得声明 accepted / integrated / production_ready。
