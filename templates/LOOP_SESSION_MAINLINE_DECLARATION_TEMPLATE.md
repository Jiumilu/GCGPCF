---
doc_id: GPCF-DOC-9A5D7C1B3E
title: LOOP 会话主线声明模板
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md
source_path: templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP 会话主线声明模板

## 1. 会话主线

| 字段 | 值 |
|---|---|
| `session_mainline` |  |
| `objective` |  |
| `owner_session` |  |
| `current_project` |  |
| `current_worktree` |  |
| `loop_mode` | L0 / L1 / L2 / L3 / L3.5 / L4 / L5 |
| `status_ceiling` | partial / repair_required / evidence_ready / ready_for_review |

## 2. 范围

| 字段 | 值 |
|---|---|
| `scope_in` |  |
| `scope_out` |  |
| `allowed_actions` |  |
| `forbidden_actions` | production write / external API write / real KDS API write / schema sync / deployment / permission change / commit / push / accepted / integrated / production_ready |
| `stop_conditions` |  |

## 3. 输入证据

| evidence_inputs | 路径或命令 | 是否已读取 |
|---|---|---|
| AGENTS.md |  |  |
| LOOP_CONTROL_BOARD.md |  |  |
| LOOP_AUTONOMY_POLICY.md |  |  |
| 最近一轮 loop-round |  |  |
| Git 状态 |  |  |
| 相关 validator |  |  |

## 4. 偏离检查

| 检查项 | 当前值 | 结果 |
|---|---|---|
| 用户请求是否匹配 `session_mainline` |  | pass / mainline_drift_detected |
| 当前路径是否在 `scope_in` |  | pass / mainline_drift_detected |
| Git dirty 是否包含非本轮 scope |  | pass / mainline_drift_detected |
| 是否接续其它会话任务 |  | no / handoff_required |
| 是否需要重新授权 |  | no / authorization_required |

## 5. 本轮结论

- `mainline_status`：
- `next_allowed_action`：
- `confirmation_required`：
- `notes`：
