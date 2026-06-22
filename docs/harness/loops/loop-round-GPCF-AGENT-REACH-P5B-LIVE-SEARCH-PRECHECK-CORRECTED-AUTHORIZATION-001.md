---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001
title: LOOP Round GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P5B-LIVE-SEARCH-PRECHECK-CORRECTED-AUTHORIZATION-001

## run

- 输入：`docs/harness/evidence/agent-reach-p5-live-search-precheck-20260622.json`
- 输入：`fixtures/agent-reach/live-search-precheck-corrected-authorization-20260622.json`
- 动作：校验授权人、授权窗口、允许通道、查询上限、禁止动作和 precheck-before-live 要求。
- 输出：P5B evidence、Loop 轮次文档和本地验证器。

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮只授权并执行 corrected authorization precheck，不执行真实搜索。

## verify

- `authorized_at` 为具体 ISO-8601：通过。
- `expires_at` 为具体 ISO-8601：通过。
- `expires_at` 晚于 `authorized_at`：通过。
- 允许通道在 P4 边界内：通过。
- 查询上限在 P4 边界内：通过。
- 真实搜索调用：未执行。

## recover

- 若下一轮 live-search dry-run 出现异常，删除下一轮生成的 dry-run evidence，保留 P5B 授权预检证据。
- 若授权窗口需要收窄，追加 corrected authorization 证据，不覆盖本轮证据。

## debug

- Watch：授权窗口超过一天。
- 下一轮：`GPCF-AGENT-REACH-P6-LIMITED-LIVE-SEARCH-DRY-RUN-PREPARATION-001`
- 下一轮必须先准备 query 清单、输出路径、日志脱敏和回滚步骤；本轮不声明搜索质量已验收。
