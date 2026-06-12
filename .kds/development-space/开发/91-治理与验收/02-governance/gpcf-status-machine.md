---
doc_id: GPCF-DOC-A33E51C815
title: GPCF Loop Engineering 状态机定义
project: WAES
related_projects: [GPC, WAES, XiaoC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/gpcf-status-machine.md
source_path: 02-governance/gpcf-status-machine.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF Loop Engineering 状态机定义

日期：2026-06-12
状态：v1.0
依赖：gpcf-loop-engineering-spec-v1.md

## 1. 正常状态流转

```
not_started
    │
    ▼
loop_ready          ←── 补齐 Manifest + loop-state.md + evidence 目录
    │
    ▼
loop_running        ←── 至少完成 1 轮微循环
    │
    ▼
evidence_ready      ←── 本轮 evidence 完整率 ≥80%
    │
    ▼
audit_ready         ←── 完成中循环审计（评衡+证验）
    │
    ▼
harness_review      ←── Harness Governance 判定
    │
    ▼
accepted            ←── 人工确认通过
    │
    ▼
integrated          ←── 小即跨项目收口完成
```

## 2. 状态定义

| 状态 | 定义 | 进入条件 | 退出条件 |
|---|---|---|---|
| not_started | 未进入 Loop Engineering 机制 | 默认初始状态 | Manifest + loop-state.md + evidence 目录补齐 |
| loop_ready | 已具备进入循环的基础条件 | 3 个必须文件补齐 | 完成第 1 轮微循环 |
| loop_running | 正在执行微循环 | 第 1 轮 loop-round-{ID}.md 提交 | evidence 完整率 ≥80% |
| evidence_ready | 本轮 evidence 已齐全 | 必备 evidence 类型收集完整 | 评衡+证验完成审计 |
| audit_ready | 已完成审计，等待 Harness 判定 | 审计报告提交 | Harness Governance 完成判定 |
| harness_review | Harness 判定中 | Harness 开始审查 | 人工确认完成 |
| accepted | 人工确认通过 | 人工确认记录就绪 | 小即完成跨项目收口 |
| integrated | 已纳入 GPCF 总状态矩阵 | 小即收口完成 | - |

## 3. 异常状态

| 状态 | 定义 | 触发条件 | 恢复路径 |
|---|---|---|---|
| blocked | 存在阻塞项无法自行消解 | 阻塞项登记且无解 | 阻塞消解 → 回到 loop_running |
| partial | 部分通过、部分未通过 | 审计部分 pass、部分 fail | 补齐未通过项 → 重新审计 |
| rework_required | 模板/状态机/evidence 规则需返工 | 规范层面发现问题 | 规范修正 → 项目重新从 loop_ready 进入 |
| manual_confirmation_required | 等待人工确认 | 提交人工确认后 | 人工确认完成 → 进入 accepted |

## 4. 状态升级权限

| 状态转换 | 执行者 | 前置条件 |
|---|---|---|
| not_started → loop_ready | 项目仓智能体 | Manifest + loop-state.md + evidence 目录 |
| loop_ready → loop_running | 项目仓智能体 | 第 1 轮微循环完成 |
| loop_running → evidence_ready | 项目仓智能体（自检） | evidence 完整率 ≥80% |
| evidence_ready → audit_ready | 评衡 + 证验 | 审计完成 |
| audit_ready → harness_review | Harness Governance | 审计报告接收 |
| harness_review → accepted | 人工 | 人工确认记录 |
| accepted → integrated | 小即 | 跨项目收口完成 |

## 5. 禁止事项

| # | 禁止 |
|---|---|
| 1 | 任何角色自行将状态升级为 accepted |
| 2 | 跳过 audit_ready 直接进入 harness_review |
| 3 | 无 evidence 支持的状态升级 |
| 4 | 从 blocked 直接跳到 accepted（必须回到 loop_running 重新验证） |
| 5 | 小即将未完成审计的项目标记为 integrated |

## 6. 与 Harness 统一状态标签的映射

| Loop Engineering 状态 | 现有 Harness 标签 |
|---|---|
| not_started | not_started |
| loop_ready | not_started（已就绪） |
| loop_running | in_progress |
| evidence_ready | partial |
| audit_ready | partial |
| harness_review | in_progress |
| accepted | accepted |
| integrated | complete |
| blocked | blocked |
| partial | partial |
| rework_required | blocked |

## 7. 版本记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.0 | 初始定义：正常状态流转、异常状态、升级权限、Harness映射 |

## 8. 状态转移矩阵

| 当前状态 | 目标状态 | 触发条件 | 判定角色 | 需 evidence |
|---|---|---|---|---|
| not_started | loop_ready | Manifest + loop-state.md + evidence 目录补齐 | 小即/总控 | 是 |
| loop_ready | loop_running | 至少创建 LR-001 | 执行智能体 | 是 |
| loop_running | evidence_ready | evidence 完整率 ≥80% | 证验 | 是 |
| evidence_ready | audit_ready | 完成评分和证据验收 | 评衡 + 证验 | 是 |
| audit_ready | harness_review | 提交 Harness 判定 | 小即 | 是 |
| harness_review | accepted | 人工确认通过 | Harness / 人工 | 是 |
| accepted | integrated | 小即跨项目收口 | 小即 | 是 |
| loop_running | blocked | 阻塞项登记且无解 | 执行智能体 | 是 |
| blocked | loop_running | 阻塞消解 | 执行智能体 | 是 |
| any | rework_required | 规范层面发现问题 | Harness Governance | 是 |
| audit_ready | partial | 审计部分通过 | 评衡 + 证验 | 是 |
| partial | audit_ready | 补齐未通过项 | 执行智能体 | 是 |
| harness_review | manual_confirmation_required | 提交人工确认后等待 | Harness Governance | 是 |
| manual_confirmation_required | accepted | 人工确认完成 | 人工 | 是 |
| evidence_ready | loop_running | 证验发现 evidence 不足 | 证验 | 是 |
| audit_ready | evidence_ready | 审计退回补证据 | 评衡 + 证验 | 是 |

## 9. 版本记录（续）

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-06-12 | v1.1 | 增加状态转移矩阵（含异常状态回退路径） |
