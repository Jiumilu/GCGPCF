---
doc_id: GPCF-DOC-1603BD309B
title: Loop CodeGraph Goal Optimization Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md
source_path: docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Goal Optimization Evidence

## Evidence ID

`LOOP-CODEGRAPH-GOAL-OPT-20260620`

## 结论

P0 准入设计已完成：CodeGraph 被定义为本地代码图谱感知和目标优化辅助层，未安装、未配置 MCP、未生成项目索引、未触达生产、未写入真实外部 API。

## 受控产物

| 产物 | 路径 | 状态 |
|---|---|---|
| 完整实施方案 | `02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md` | controlled |
| 本 evidence | `docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md` | controlled |
| Evidence JSON | `docs/harness/evidence/loop-codegraph-goal-optimization-20260620.json` | machine evidence |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-CODEGRAPH-GOAL-OPT-001.md` | controlled |
| 目标优化记录模板 | `templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md` | controlled |
| Validator | `tools/kds-sync/validate_loop_codegraph_goal_optimization.py` | local gate |
| Git 缓存排除 | `.gitignore` | `.codegraph/` excluded |

## 目标优化字段

本轮定义每个后续 CodeGraph 试点 Loop 必须记录：

- `codegraph_enabled`
- `codegraph_scope_query`
- `impacted_symbols`
- `impacted_files`
- `manual_source_check`
- `related_validators`
- `exploration_tool_calls_before`
- `exploration_tool_calls_after`
- `file_reads_before`
- `file_reads_after`
- `scope_precision_result`
- `optimization_feedback`

## 目标优化 Loop

```text
目标声明 -> 图谱预检 -> 影响面收敛 -> 最小动作计划 -> 验证选择 -> 执行 -> 结果度量 -> 规则沉淀
```

## 当前边界

| 项 | 当前值 |
|---|---|
| installation_performed | false |
| mcp_configuration_changed | false |
| codegraph_index_created | false |
| production_write | false |
| external_api_write | false |
| status_upgrade_allowed | false |

## 非声明

- 不证明 GFIS runtime SOP E2E 已通过。
- 不创建 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact、UAT 签收、客户满意、`accepted` 或 `integrated`。
- 不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、推送或合并。
- 不把 CodeGraph 查询结果替代源码、测试、文档门禁、KDS TOKEN 门禁、Harness/WAES 判定或人工确认。
