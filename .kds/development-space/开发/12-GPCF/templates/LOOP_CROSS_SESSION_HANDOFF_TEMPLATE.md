---
doc_id: GPCF-DOC-0F4B8E6C2A
title: LOOP 跨会话交接模板
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md
source_path: templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP 跨会话交接模板

## 1. 交接基本信息

| 字段 | 值 |
|---|---|
| `handoff_id` |  |
| `handoff_source` |  |
| `handoff_time` |  |
| `source_owner_session` |  |
| `target_owner_session` |  |
| `source_session_mainline` |  |
| `target_session_mainline` |  |
| `user_confirmation` | confirmed / missing |

## 2. 交接证据

| 证据类型 | 路径或命令 | 当前状态 |
|---|---|---|
| 最后一轮 `loop-round` |  |  |
| evidence JSON/Markdown |  |  |
| validator 输出 |  |  |
| Git 状态 |  |  |
| 控制板或 loop-state |  |  |
| 未完成任务包 |  |  |

## 3. 范围变化

| 字段 | 值 |
|---|---|
| `scope_delta` |  |
| `authorization_delta` |  |
| `remaining_risks` |  |
| `blocked_items` |  |
| `revalidation_required` |  |

## 4. 禁止自动接管

以下动作必须重新请求授权：

- 其它项目仓写入。
- 真实 KDS API 写入。
- 真实外部 API 写入。
- schema sync、bench migrate、deployment 或权限变更。
- commit、push、merge 或发布。
- accepted、integrated 或 production_ready 状态升级。
- 关闭其它会话结论或修改其它会话 owner 状态。

## 5. 交接判定

| 判定项 | 结果 |
|---|---|
| handoff evidence 完整 | yes / no |
| 用户确认完整 | yes / no |
| Git 状态已复核 | yes / no |
| 目标 scope 明确 | yes / no |
| 可以写入 | yes / no |
| 只能生成建议 | yes / no |

## 6. 接续动作

- `next_allowed_action`：
- `next_validator`：
- `rollback_or_pause_action`：
