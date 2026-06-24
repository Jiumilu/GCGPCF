---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623
title: Headroom LCX Real Measurement Runner Contract Evidence
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement Runner Contract Evidence

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623`

## 结论

当前 runner contract 只定义未来真实测量执行的 precheck-only 边界，不打开 production branch。
status: runner_contract_defined_precheck_only

## 允许输入

`authorized_window_id`, `authorized_by`, `authorized_at`, `sanitized_production_token_ledger`, `rollback_plan_id`, `waes_harness_admission_decision`

## 禁止输入

`raw_prompt`, `raw_completion`, `customer_contract`, `pod`, `financial_voucher`, `secret`, `production_credential`, `production_proxy`, `production_sdk`, `real_kds_write`, `external_api_write`

## 允许动作

- `read_sanitized_ledger_metadata`
- `calculate_token_saving_estimate`
- `write_harness_evidence`

## 禁止动作

- `production_proxy_start`
- `production_sdk_enable`
- `real_kds_api_write`
- `external_api_write`
- `database_migration`
- `permission_change`
- `headroom_learn_apply`
- `memory_as_kds_fact_source`

## 当前状态

- execution_allowed_now: `false`
- real_measurement_gap_present: `true`
- production_branch_blocked: `true`
- production_token_measurement_allowed: `false`
- measured_production_tokens: `false`
- production_admission_gate: `false`
- accepted: `false`
- integrated: `false`
- production_ready: `false`

## 非声明

- 本证据不表示真实测量已执行。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产分支已打开。
- 本证据不表示 accepted、integrated 或 production_ready。
