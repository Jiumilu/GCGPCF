---
doc_id: GPCF-DOC-23DDC94324
title: Loop CodeGraph P1 Pilot Admission
project: WAES
related_projects: [GFIS, GPC, WAES, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CODEGRAPH_P1_PILOT_ADMISSION.md
source_path: 02-governance/loop/LOOP_CODEGRAPH_P1_PILOT_ADMISSION.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph P1 Pilot Admission

## 1. 目标

本准入包用于把 P0 方案推进到 P1 本地试点。P1 的目标是：在用户明确授权后，为 GPCF 和 GFIS 建立本地 CodeGraph CLI/MCP/索引试点，并用真实 Loop 任务度量是否降低探索成本和返工成本。

本文件不是安装记录。当前状态为 `authorization_required`。

## 2. 当前事实

| 字段 | 当前值 |
|---|---|
| codegraph_cli_available | false |
| npm_package_visible | `@colbymchenry/codegraph@1.0.1` |
| mcp_configuration_changed | false |
| codegraph_index_created | false |
| production_write | false |
| external_api_write | false |
| status_upgrade_allowed | false |

## 3. P1 授权字段

P1 启动前必须由用户明确确认以下字段：

| 字段 | 允许值 | 当前值 |
|---|---|---|
| authorized_mode | `P1-codegraph-local-pilot` | pending |
| authorized_repos | `GPCF`, `GFIS`, or both | pending |
| allow_global_npm_install | true / false | pending |
| allow_agent_mcp_install | true / false | pending |
| allow_codegraph_init | true / false | pending |
| allow_network_download | true / false | pending |
| allow_commit | true / false | false |
| allow_push | true / false | false |
| rollback_required | true / false | true |

缺任一字段时，P1 最高只能停在 `authorization_required`，不得静默安装或修改 MCP。

## 4. 试点范围

| 项目 | 路径 | P1 动作 | 边界 |
|---|---|---|---|
| GPCF | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF` | `codegraph init`、目标优化记录、validator 试跑 | 不提交 `.codegraph/` |
| GFIS | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` | `codegraph init`、选 3 个 repair 任务做对照 | 不执行 bench migrate/schema sync/生产写入 |

## 5. 执行命令候选

以下命令只有在授权字段满足后才可执行：

```bash
npm i -g @colbymchenry/codegraph
codegraph install
codegraph init
```

执行前必须记录：

```text
authorized_mode=P1-codegraph-local-pilot
authorized_repos=...
allow_global_npm_install=...
allow_agent_mcp_install=...
allow_codegraph_init=...
allow_network_download=...
rollback_required=true
```

## 6. 回滚方案

| 变更 | 回滚 |
|---|---|
| `.codegraph/` 本地索引 | 删除对应仓库 `.codegraph/` 目录 |
| 全局 npm 包 | `npm uninstall -g @colbymchenry/codegraph` |
| agent MCP 配置 | 使用 `codegraph uninstall`；如命令不可用，则人工移除对应 MCP 条目并记录配置路径 |
| Loop 试点记录 | 保留为受控 evidence，不回写业务完成状态 |

## 7. 首批试点任务

| Round | 仓库 | 任务 | 度量目标 |
|---|---|---|---|
| CG-P1-GPCF-001 | GPCF | 用 CodeGraph 查询 Loop validator 和文档控制相关入口 | 记录文件读取数、工具调用数、validator 命中 |
| CG-P1-GFIS-001 | GFIS | 选择一个 `CustomerRequirementOrPlatformOrder` repair gate 做影响面预检 | 记录 impacted symbols/files 与实际修改范围 |
| CG-P1-GFIS-002 | GFIS | 选择一个 runtime SOP validator 路径做相关测试选择 | 记录 validator first pass 和 impact miss |

## 8. P1 成功标准

1. 用户授权字段完整。
2. `codegraph_cli_available=true`。
3. 试点仓 `.codegraph/` 存在但不进入 Git。
4. 至少 3 个试点记录使用 `templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md` 等价字段。
5. 每个试点记录都包含 `manual_source_check` 和 `related_validators`。
6. 至少有一次对照度量：`exploration_tool_calls_after`、`file_reads_after`、`validator_first_pass`。
7. 未发生生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、推送或 accepted/integrated 升级。

## 9. P1 停止条件

| 条件 | stop_type |
|---|---|
| 授权字段缺失 | authorization_required |
| npm 安装失败 | tool_install_failed |
| MCP 配置失败 | mcp_config_failed |
| `.codegraph/` 进入 Git 候选 | git_pollution_risk |
| CodeGraph 查询与源码复核冲突 | source_check_required |
| 触及生产写入或真实外部 API | hard_stop |

## 10. 非声明

- 本准入包不证明 CodeGraph 已安装。
- 本准入包不证明 GFIS runtime SOP E2E 已通过。
- 本准入包不创建 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact、UAT 签收、客户满意、`accepted` 或 `integrated`。
- 本准入包不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、提交、推送或合并。
