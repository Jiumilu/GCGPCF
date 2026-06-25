---
doc_id: GPCF-DOC-LOOP-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004
title: Loop Round - GPCF Cognee P4 真实写入执行前授权评审 004
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004.md
source_path: docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# Loop Round - GPCF Cognee P4 真实写入执行前授权评审 004

## 输入

- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-002.md`
- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-003.md`
- `docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- `loop/context/cognee/policy.yaml`

## run

- 汇总并提交 004 授权评审包（面向 WAES/Owner/运行团队）：
  - 阻断修复项 `task-004`、`task-005` 已全部清零确认；
  - `pilot_gate_pass=true`、`precheck_pass_rate=1.0`、`expected_blocked_reason_rate=1.0`；
  - 回滚与运行时依赖恢复要求可解释、可验收。
- 明确 live-write 运行边界：
  - 本轮仅评估“是否允许进入 live-write”，不执行真实外部写入。
  - 要求输出确认清单（owner 授权、runtime permission、回滚链路、监控指标）。
- 为下一轮创建可执行运行指令草案：
  - `run-cognee-p4-real-writeback-live.py` 已落地，下一轮可直接进入 `LIVE-001` 演练清单执行。
- `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001` 已完成 dry-run 与 `--allow-live-write` 演练后，下一步进入 `LIVE-002` 完成人审签字。

## 输出

- `docs/harness/evidence/cognee-p4-real-writeback-precheck-20260624.md`
- `docs/harness/evidence/cognee-p4-real-writeback-live-20260624.md`
- `docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json`
- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001.md`（下一步执行稿）
- `docs/harness/evidence/cognee-p4-real-writeback-live-authorization-signoff-20260625.md`（签核模板）
- `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-002.md`（签核执行稿）

## stop

- 停止类型：`authorization_boundary`
- 停止原因：本轮为执行前授权评审边界，仍需人工确认后才能进入 live-write。
- 当前状态：`pilot_gate_pass=true`，`accepted=false`，`integrated=false`，`production_ready=false`。

## verify

- 审核通过条件：
  - `accepted_for_writeback_authorization`（人工确认）
  - `owner_token_source` 可追溯确认
  - `runtime_dependency_ok_rate=1.0`
  - `authorization_token_source_coverage=1.0`
  - `rollback_readiness_rate=1.0`
  - `cognee_p4_real_writeback_live_output=pass`
  - `live_execution_ready_rate=1.0`

## 反馈

- 目前可确认：预检阻断样例已复测修复，已进入 `LIVE-001` 执行稿；`LIVE-001` 已跑通 dry-run 与 `--allow-live-write` 两种口径，`pilot_gate_pass=True`，准备提交 owner/WAES 授权复核。
- 当前本轮仍保留授权确认边界；未出具生产外部执行放行指令前不予切入真实写入。
- 若未通过，退回 `GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-003` 处理并补充修复记录。

## 授权复核包（等待签字）

- Owner 授权项：
  - `owner_token_source` 在每条 live 记录中的来源是否一致可追溯（`owner_jwt` / `project_group_jwt`）。
  - 对 `writeback_owner_auth_gap` 场景的授权修复说明是否在变更单中闭环。
- WAES 授权项：
  - `waes_decision=pass` 且 `runtime_dependency_ok=true` 的依据是否形成复核截图或审批单。
  - `rollback_plan_verified=true` 的回滚步骤与恢复窗口是否可执行（含失败退出条件）。
- 执行边界：
  - `cognee_p4_real_writeback_live_output=pass`
  - `execution_count=5`
  - `live_execution_ready_rate=1.0`
  - `blocked_due_expected_reason_rate=0.0`

## recover

- 回归场景：如 live-write 授权确认失败，恢复到 `docs/harness/loops/loop-round-GPCF-COGNEE-P4-REAL-WRITEBACK-PRECHECK-003.md`，补齐授权链路与回滚链路后重启评审。

## debug

- 当前阻断项已清零；剩余风险仅为外部授权与执行边界确认，不涉及脚本指标回归。
