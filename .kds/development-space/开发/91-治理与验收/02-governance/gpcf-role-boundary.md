---
doc_id: GPCF-DOC-D67341FE2B
title: GPCF Loop Engineering 角色边界定义
project: WAES
related_projects: [GPC, WAES, XiaoC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/gpcf-role-boundary.md
source_path: 02-governance/gpcf-role-boundary.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF Loop Engineering 角色边界定义

日期：2026-06-12
状态：v1.0
依赖：gpcf-loop-engineering-spec-v1.md

## 1. 角色与 CAN/CANNOT

### 执行智能体（各专项智能体）

| CAN | CANNOT |
|---|---|
| 修改本域业务文件 | 自行宣布项目 complete/accepted |
| 产出 evidence 并自检 | 修改跨域主责边界 |
| 推动本域微循环 | 将 AI 建议写成业务事实（需经 SUGG→WAES） |
| 登记阻塞项 | 绕过审计直接升级状态 |
| 更新 loop-state.md 中本域字段 | 一个循环同时修改多个不相关模块 |

### 评衡（评估审计）

| CAN | CANNOT |
|---|---|
| 对项目执行量化评分 | 修改业务文件 |
| 发现和登记问题 | 补充缺失的 evidence |
| 形成量化报告 | 自行升级项目状态 |
| 建议状态变更 | 代替证验做证据确证 |

### 证验（证据验收）

| CAN | CANNOT |
|---|---|
| 验证 evidence 完整性 | 替执行层补证据（缺失即标记缺失） |
| 判断 evidence 可复现性 | 修改业务文件 |
| 形成证据审计报告 | 自行升级项目状态 |
| 建议阻塞项 | 代替评衡做量化评分 |

### Harness Governance

| CAN | CANNOT |
|---|---|
| 状态判定 | 绕过人工确认直接标记 accepted |
| 门禁裁决 | 修改项目仓业务文件 |
| 读取并审计 evidence | 代替小即做跨项目收口 |
| 判定 blocked/rework_required | 在无 evidence 时做正面判定 |

### 小即（总控）

| CAN | CANNOT |
|---|---|
| 跨项目收口 | 直接替代项目微循环 |
| 统一命名 | 绕过项目仓 evidence 做收口 |
| 状态升级申请 | 未审计完成时标记 integrated |
| 版本冻结 | 修改项目仓业务内容 |
| 推广决策 | 在试点未完成时启动全量推广 |

## 2. 核心约束

1. 验收层可以判定，不可以代替执行层修正业务内容
2. 集成层可以收口，不可以绕过项目仓 evidence
3. 任何角色不得在无 evidence 支持下升级项目状态
4. 人工确认是 accepted 状态的唯一入口

## 3. 越权判定

若发现以下情况，证验或 Harness Governance 应立即标记为 `rework_required`：

- 执行智能体自行标记 accepted
- 评衡/证验修改了业务文件
- Harness Governance 跳过人工确认标记 accepted
- 小即在试点审计未完成时推广

## 4. 版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 初始定义：5 个角色 CAN/CANNOT、核心约束、越权判定 |
