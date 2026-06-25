---
doc_id: GPCF-DOC-8C7F2F6002
title: Cognee P4 真实写入 live 授权签核包（待签）
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md
source_path: docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Cognee P4 真实写入 live 授权签核包（待签）

## 1. 说明

本包为 `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002` 人审签字模板，不代表生产执行已完成；不表示生产写入权限已开启。

## 2. 证据引用

- 预检证据：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- 演练证据：`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`

## 3. 需签字段（Owner）

| 字段 | 当前状态 | 说明 |
|---|---|---|
| `owner_signer_name` | REQUIRED_USER_INPUT | Owner 签署人 |
| `owner_signer_role` | REQUIRED_USER_INPUT | 签署人角色 |
| `owner_signer_token_source` | REQUIRED_USER_INPUT | `owner_jwt` / `project_group_jwt` 等 |
| `owner_signed_at` | REQUIRED_USER_INPUT | ISO-8601 时间 |
| `owner_decision` | REQUIRED_USER_INPUT | `approve_live_write` 或 `reject` |
| `owner_decision_evidence` | REQUIRED_USER_INPUT | 与决策一致的审批说明或截图编号 |

## 4. 需签字段（WAES）

| 字段 | 当前状态 | 说明 |
|---|---|---|
| `waes_signer_name` | REQUIRED_USER_INPUT | WAES 签署人 |
| `waes_signer_role` | REQUIRED_USER_INPUT | WAES 审批角色 |
| `waes_signed_at` | REQUIRED_USER_INPUT | ISO-8601 时间 |
| `waes_decision` | REQUIRED_USER_INPUT | `pass` 或 `block` |
| `waes_runtime_dependency_ok` | REQUIRED_USER_INPUT | `true` / `false` |
| `waes_rollback_plan_verified` | REQUIRED_USER_INPUT | `true` / `false` |

## 5. 非声明（本轮签核不变更）

- 不声明 `production_write=true`
- 不声明 `external_api_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`

## 6. 签核后切换条件

需同时满足：

- `cognee_p4_real_writeback_live_output=pass`
- `record_count=5`
- `requested_write_count=5`
- `execution_count=5`
- `pilot_gate_pass=True`
- `live_execution_ready_rate=1.0`
- Owner/WAES 两签字段均非 `REQUIRED_USER_INPUT`，且 `owner_decision=approve_live_write`、`waes_decision=pass`。
