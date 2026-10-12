---
doc_id: GPCF-DOC-LOOP-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001
title: LOOP Round GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-AGENT-REACH-P8-PROJECT-GROUP-FULL-LIVE-COVERAGE-PLAN-001

## run

把 Agent-Reach 从 P7 的 5 项目 pilot 扩展为 P8 的 14 项目全量 live coverage 计划。按每批最多 5 个 query 拆为 3 批，每批都要求单独授权。

## stop

停止类型：`authorization_boundary`。本轮只生成计划，不执行真实搜索，不创建 runtime evidence。

## verify

验证命令：

```bash
python3 tools/kds-sync/validate_agent_reach_project_group_full_live_coverage_plan.py
```

预期结果：`full_project_group_live_coverage_plan_ready`，`project_coverage=14/14`，`live_external_search_invoked=false`。

## recover

若后续任一 batch 执行失败，删除该 batch runtime evidence，保留本轮 full coverage plan，按失败 batch 重新授权与重跑。

## debug

剩余缺口：P8 每批执行授权、各 batch 真实 runtime evidence、合并后的 14 项目质量报告、人工复核与生产准入。
