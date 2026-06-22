---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001
title: LOOP Round GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P8-FULL-LIVE-SEARCH-PIPELINE-001

## run

- 输入：P8 batch runner、merge runner、full output quality gate。
- 动作：建立端到端执行编排器。
- 输出：P8 pipeline evidence、Loop 轮次文档和本地验证器。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮只建立执行编排器，不创建三批 `.local.json` 授权文件，不执行真实搜索。

## verify

- 无三批授权时阻断：通过。
- 编排器会串联三批执行、合并和全量质量门禁：通过。
- 真实搜索调用：未执行。
- accepted / integrated / production_ready 声明：未声明。

## recover

- 若后续端到端执行失败，保留已生成的 batch evidence，删除失败后的合并产物并重新运行质量门禁。
- 若任何 batch 授权过期，删除对应 `.local.json` 并重新申请该批授权。

## debug

- 当前阻塞：缺少三批 `.local.json` 执行授权文件。
- 下一轮：`GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`
- 下一轮不得声明 accepted / integrated / production_ready。
