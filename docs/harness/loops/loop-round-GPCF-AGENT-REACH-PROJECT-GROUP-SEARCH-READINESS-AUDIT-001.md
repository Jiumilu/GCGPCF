---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001
title: LOOP Round GPCF-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-PROJECT-GROUP-SEARCH-READINESS-AUDIT-001

## run

审计 Agent-Reach 项目群搜索目标的当前可执行状态。输入包括全量实施目标、P3 离线 replay、P6 dry-run 准备、P7 授权预检、P7 运行依赖、P7 web backend 修复和 P7 输出质量门禁。

## stop

停止类型：`authorization_boundary`。当前缺少 P7 执行授权文件，默认 runner 返回 `blocked_pending_execution_authorization`，不得执行真实外部搜索。

## verify

验证命令：

```bash
python3 tools/kds-sync/validate_agent_reach_project_group_search_readiness_audit.py
```

预期结果：`search_readiness_verified_pending_p7_authorization`。该结果只能证明准备态和质量门禁存在，不能证明项目群全量真实搜索已完成。

## recover

若后续 P7 dry-run 输出失败，删除 P7 runtime evidence，保留 P3/P6/P7 readiness evidence，并回退到本轮审计状态继续修复。

## debug

剩余缺口：P7 执行授权、真实 runtime evidence、真实候选质量报告、14 项目 live coverage、人工复核与生产准入。
