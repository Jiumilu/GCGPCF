---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623
title: Headroom LCX 真实测量授权窗口请求证据
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX 真实测量授权窗口请求证据

## 证据 ID

`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-REQUEST-20260623`

## 结论

已请求真实测量授权窗口，但当前仍未授予；该请求只作为 precheck-only 边界证据，不打开 production branch。
状态：真实测量授权窗口已请求，但当前仍未授予
status: real_measurement_authorization_window_requested_not_granted

## 请求字段

| field | value |
|---|---|
| requested_window_id | `LCX-MEASURE-20260622-001` |
| requested_by | `lujunxiang / GPCF owner` |
| requested_at | `2026-06-22T08:42:06+08:00` |
| requested_future_decision | `open_real_measurement_window` |
| current_waes_harness_admission_decision | `admitted_for_sanitized_measurement_precheck` |

## 当前状态

| state | value |
|---|---|
| real_measurement_open | `false` |
| production_branch_blocked | `true` |
| production_token_measurement_allowed | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本证据不表示真实授权窗口已打开。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产代理、生产 SDK、真实 KDS 写入或真实外部 API 写入已开启。
- 本证据不表示 accepted、integrated 或 production_ready。
