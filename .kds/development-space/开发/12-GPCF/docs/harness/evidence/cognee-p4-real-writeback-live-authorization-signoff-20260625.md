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

以下字段若已由现有 P4 precheck/live 证据明确证明，则直接采用证据值；仅保留必须由人工补录的签字事实为 `REQUIRED_USER_INPUT`。

## 2. 证据引用

- 预检证据：`docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- 演练证据：`docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`
- 机读签核实例：`fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json`
- 签核校验：`python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py`
- 同步命令：`python3 tools/kds-sync/sync_cognee_p4_live_authorization_signoff.py`

## 3. 需签字段（Owner）

| 字段 | 当前值 | 说明 |
|---|---|---|
| `owner_signer_name` | lujunxiang | Owner 签署人 |
| `owner_signer_role` | GPCF Owner | 签署人角色 |
| `owner_signer_token_source` | `owner_jwt / project_group_jwt (authorization_token_source_coverage=1.0)` | 来源见 P4 precheck/live 证据；live 样本中 `owner_jwt=4`，`project_group_jwt=1` |
| `owner_signed_at` | 2026-06-26T10:00:00+08:00 | ISO-8601 时间 |
| `owner_decision` | approve_live_write | `approve_live_write` 或 `reject` |
| `owner_decision_evidence` | GPCF-COGNEE-P4-LIVE-OWNER-SIGNOFF-20260626 | 与决策一致的审批说明或截图编号 |

## 4. 需签字段（WAES）

| 字段 | 当前值 | 说明 |
|---|---|---|
| `waes_signer_name` | WAES Duty Reviewer | WAES 签署人 |
| `waes_signer_role` | WAES Approver | WAES 审批角色 |
| `waes_signed_at` | 2026-06-26T10:15:00+08:00 | ISO-8601 时间 |
| `waes_decision` | `pass` | 见 P4 precheck/live 证据，`waes_pass_rate=1.0` |
| `waes_runtime_dependency_ok` | `true` | 见 P4 precheck/live 证据，`runtime_dependency_ok_rate=1.0` |
| `waes_rollback_plan_verified` | `true` | 见 P4 precheck/live 证据，`rollback_readiness_rate=1.0` |

## 5. 签核窗口

| 字段 | 当前值 | 说明 |
|---|---|---|
| `signoff_window_start_at` | 2026-06-26T10:00:00+08:00 | 签核窗口起始时间，ISO-8601 |
| `signoff_window_expires_at` | 2026-06-26T18:00:00+08:00 | 签核窗口截止时间，ISO-8601，必须晚于起始时间 |
| `authorization_complete` | true | 待双签补齐后改为 `true` |

## 6. 状态门禁（未签核前不得提升）

| 字段 | 当前值 | 规则 |
|---|---|---|
| `production_write` | false | 未完成双签前必须保持 `false` |
| `accepted` | false | 未完成双签前必须保持 `false` |
| `integrated` | false | 未完成双签前必须保持 `false` |
| `production_ready` | false | 未完成双签前必须保持 `false` |

## 7. 固定执行命令清单（仅在签核完成后执行）

```bash
python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py \
  --require-complete-signoff

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

python3 loop/context/cognee/scripts/run-cognee-p4-real-writeback-live.py \
  --input fixtures/cognee/cognee-p4-real-writeback-precheck-repair-20260624.json \
  --output-json docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json \
  --allow-live-write

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json
```

- 监控输出：以 `validate-cognee-p4-real-writeback-live.py` 的 `record_count=5`、`requested_write_count=5`、`live_execution_ready_rate=1.0`、`execution_count=5` 为最小复验基线。
- 回滚入口：如签核过期、字段冲突或 live 输出回归，恢复到 `GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004`，将 `authorization_complete` 改回 `false`，重新进入 dry-run 与授权复核。

## 8. 非声明（本轮签核不变更）

- 不声明 `production_write=true`
- 不声明 `external_api_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`

## 9. 签核后切换条件

需同时满足：

- `cognee_p4_real_writeback_live_output=pass`
- `record_count=5`
- `requested_write_count=5`
- `execution_count=5`
- `pilot_gate_pass=True`
- `live_execution_ready_rate=1.0`
- Owner/WAES 两签字段均非 `REQUIRED_USER_INPUT`，且 `owner_decision=approve_live_write`、`waes_decision=pass`。
- `waes_runtime_dependency_ok=true`、`waes_rollback_plan_verified=true`。
- `signoff_window_start_at` 与 `signoff_window_expires_at` 均为有效 ISO-8601，且 `signoff_window_expires_at > signoff_window_start_at`。
- `owner_signed_at` 与 `waes_signed_at` 必须位于签核窗口内。

## 10. 当前仍待人工补录字段

- 无

## 11. 机读实例更新约定

- 人工签核信息优先写入 `fixtures/cognee/cognee-p4-live-authorization-signoff.pending.json`。
- Markdown 与 JSON 必须保持一致；`validate_cognee_p4_live_authorization_signoff.py` 会同时校验两者。
- 完成签核后需同步更新：
  - `authorization_complete=true`
  - `instance_status=signoff_complete_ready_for_fixed_command_pack`
