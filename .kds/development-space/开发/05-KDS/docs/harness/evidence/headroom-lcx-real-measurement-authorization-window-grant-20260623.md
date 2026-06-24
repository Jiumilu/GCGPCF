---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623
title: Headroom LCX 真实测量授权窗口授予证据
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 真实测量授权窗口授予证据

## 证据 ID

`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623`

## 结论

真实测量授权窗口已被记录为授予，但当前仍保持 precheck-only，不打开 production branch，也不允许生产 token 测量。
status: real_measurement_authorization_window_granted_precheck_only

## 授权字段

| field | value |
|---|---|
| authorized_window_id | `None` |
| authorized_by | `None` |
| authorized_at | `None` |
| sanitized_production_token_ledger | `None` |
| rollback_plan_id | `None` |
| waes_harness_admission_decision | `None` |

## 当前状态

| state | value |
|---|---|
| real_measurement_window_granted | `true` |
| real_measurement_open | `false` |
| production_branch_blocked | `true` |
| production_token_measurement_allowed | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本证据不表示真实业务等价性已证明。
- 本证据不表示 production branch 已打开。
- 本证据不表示生产代理、生产 SDK 或真实 KDS 写入已开启。
- 本证据不表示 accepted、integrated 或 production_ready。
