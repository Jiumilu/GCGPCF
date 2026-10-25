---
doc_id: GPCF-DOC-GCTOKEN-STATUS-20261025
title: GCToken 状态
project: GCToken
related_projects: [GCToken, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GCToken
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gctoken/STATUS.md
source_path: projects/gctoken/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-25
supersedes: []
superseded_by: []
---

# GCToken 状态

本文件只记录 GCToken（GlobalCloud Token，B9 模型供给面）的当前项目节奏状态；功能级进度由 features/证据承载。

## 基线

| 项 | 内容 |
|---|---|
| project_id | GCToken |
| 定位 | 模型供给面（B9 基座）：聚合远端大模型/决策模型/本地模型的发现、路由、容错、计量与治理；Hermes 执行、GCToken 供模型 |
| 仓 | `GlobalCloud Token` |
| 当前阶段 | `candidate / onboarding`（四件套 + 总体方案/实施方案 draft v0.1） |
| 项目群范围 | 2026-10-25 注册表登记为第 30 个项目（`current_project_count: 30`；Q87–Q93 立项决策） |

## 已记录事实

- 2026-10-25 项目创建（老卢），git 2 commits（初始化 + onboarding evidence），四件套齐全。
- 总体方案/实施方案为 draft v0.1，明确边界（不复制 Hermes 执行编排）。
- S0 已用 LiteLLM（MIT）+ PostgreSQL 验证网关能力（多模型路由/虚拟 Key/预算/鉴权/限流），见 `runtime/four-layer-workbench-20261025/60/64/65 号文`。

## 缺口

- MVP（Token MVP T-A1~A6）未实现：生产配置固化/决策 API/计量上报/四档 Key/本地模型路由/文档。
- 真实 provider 与计量链路未联调（需真实 key）。
- 运维（监控/告警/容量）未定。

## 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明模型路由/计量/生产服务已可用（沿仓内 README 边界声明）。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/gctoken-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project gctoken`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`
