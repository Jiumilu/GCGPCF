---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001
title: LOOP Round GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-OUTPUT-QUALITY-GATE-001

## run

- 输入：`fixtures/agent-reach/project-group-full-live-search-coverage-plan-20260622.json`
- 动作：建立 P8 全量真实搜索结果质量 validator。
- 输出：P8 output quality gate evidence、Loop 轮次文档和本地验证器。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮只建立输出质量门禁，不执行 P8 batch 真实搜索。

## verify

- 14 项目覆盖要求：已编码为 validator 必检项。
- query 覆盖要求：已编码为 validator 必检项。
- channel 覆盖要求：已编码为 validator 必检项。
- duplicate URL、query error、credential leak、forbidden claim：已编码为 validator 必检项。
- raw provider payload persistence：已编码为 validator 必检项。
- 真实搜索调用：未执行。

## recover

- 若后续 P8 runtime evidence 不通过，删除该 runtime evidence 并保留本轮门禁证据。
- 若 P8 batch 授权范围变化，先更新 plan，再重新运行本轮 validator。

## debug

- 当前阻塞：缺少 P8 batch 真实搜索执行授权。
- 下一轮：`GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-BATCH-001`
- 下一轮不得声明 accepted / integrated / production_ready。
