---
doc_id: GPCF-DOC-895151260A
title: Loop Round GPCF-CODEGRAPH-GOAL-OPT-001
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-GOAL-OPT-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-GOAL-OPT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-CODEGRAPH-GOAL-OPT-001

日期：2026-06-20

## 输入

用户目标：制定完整实施方案，并建立目标优化 Loop 工程。

入口上下文：

- 当前 GPCF Loop 控制板仍处于 GFIS repair 主线。
- 当前工作区已有大量既有 dirty 变更，本轮只做 CodeGraph 目标优化方案和门禁，不整理既有变更。
- CodeGraph 当前未在 PATH 中发现；本轮不执行安装，不修改 MCP 配置。

## 动作

| # | 动作 | 说明 |
|---|---|---|
| 1 | 新增 CodeGraph 目标优化实施方案 | 定义定位、阶段、字段、指标、风险和 DoD |
| 2 | 新增 evidence JSON/Markdown | 固化 P0 准入事实和非声明 |
| 3 | 新增本轮 Loop 记录 | 按五段式记录输入、动作、输出、检查、反馈 |
| 4 | 新增目标优化记录模板 | 让后续启用 CodeGraph 的轮次有统一记录字段 |
| 5 | 新增 validator | 机器检查方案、evidence、loop 记录、模板和 `.gitignore` |
| 6 | 更新 `.gitignore` | 排除 `.codegraph/` 本地缓存 |

## 输出

| 产物 | 路径 |
|---|---|
| 实施方案 | `02-governance/loop/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_PLAN.md` |
| Evidence Markdown | `docs/harness/evidence/loop-codegraph-goal-optimization-20260620.md` |
| Evidence JSON | `docs/harness/evidence/loop-codegraph-goal-optimization-20260620.json` |
| 目标优化记录模板 | `templates/LOOP_CODEGRAPH_GOAL_OPTIMIZATION_RECORD_TEMPLATE.md` |
| Validator | `tools/kds-sync/validate_loop_codegraph_goal_optimization.py` |
| Git 缓存排除 | `.gitignore` |

## 检查

| 检查项 | 结果 |
|---|---|
| 受控 front matter | 待 validator 验证 |
| `.codegraph/` Git 排除 | 待 validator 验证 |
| CodeGraph 安装 | 未执行，保持授权边界 |
| MCP 配置 | 未执行，保持授权边界 |
| 生产写入 | 未执行 |
| 状态升级 | 未执行 |

## 反馈

下一轮建议：

1. 在用户明确授权后进入 P1，本机安装 CodeGraph 并只对 GPCF/GFIS 执行试点索引。
2. 选择 3 个 GFIS repair 任务作为对照样本，记录工具调用、读文件数、影响面命中率和 validator 首次通过率。
3. 将高价值查询模板沉淀进 Loop skill 或项目 checklist。

## 轮次真实性

| 字段 | 值 |
|---|---|
| declared_rounds | 1 |
| substantive_rounds | 1 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| continuous_session | not_applicable |
| stop_type | completed_p0_admission |

## 非声明

- 本轮不证明 GFIS runtime SOP E2E 已通过。
- 本轮不创建 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact、UAT 签收、客户满意、`accepted` 或 `integrated`。
- 本轮不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、推送或合并。
