---
doc_id: GPCF-DOC-GCTOKEN-STATUS-20261025
title: GCToken 状态
project: GCToken
related_projects: [GCToken, GPCF, WAME]
domain: governance
status: draft
version: v0.1
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

本文件只记录 GCToken 的项目节奏状态；功能级进度与证据由后续 Feature 承载。

## 基线

| 项 | 内容 |
|---|---|
| project_id | GCToken |
| 定位 | 多家大模型、决策模型与本地模型的统一供给、配电、计量与治理面（B9） |
| 仓 | `GlobalCloud GCToken` / `Jiumilu/GCToken`（private） |
| 当前阶段 | candidate / onboarding |
| 项目群范围 | 本 PR 提议登记为第 30 个注册记录；合并前不视为生效 |

## 已记录事实

- 2026-10-25 本地 Git 初始化完成，`main` 已推送至私有远端，当前证据提交 `f897958`。
- 项目四件套、双方案、命令入口和远端规范工作流已建立。
- 在候选注册表下执行 `gc_standard.py check --repo "GlobalCloud GCToken" --fail-on error`：error 0 / warn 0。

## 缺口

- 未实现任何模型适配、路由、计量、配额、审计或运行 API。
- 项目群文档门禁实跑为 `rework_required`，状态上限 `partial`。
- 准备度脚本仍为旧 20 仓硬编码范围，未覆盖当前注册表。
- `main` 分支保护和首次远端工作流完成状态待复核。

## 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
- 不声明模型供给面已真实运行或完成客户验证。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/gctoken-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project gctoken`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 状态边界

保持 candidate / partial；任何状态提升需独立证据与人工确认。
