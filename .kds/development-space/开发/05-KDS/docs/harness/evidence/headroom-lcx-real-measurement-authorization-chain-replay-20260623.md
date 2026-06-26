---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623
title: Headroom LCX Real Measurement Authorization Chain Replay Evidence
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md
source_path: docs/harness/evidence/headroom-lcx-real-measurement-authorization-chain-replay-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Real Measurement Authorization Chain Replay Evidence

## Evidence ID

`HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-CHAIN-REPLAY-20260623`

## 结论

真实测量授权链已完成 precheck-only 回放，统一引用同一份脱敏 usage ledger，但未打开真实测量窗口，不允许生产 token 测量。
status: authorization_chain_replayed_precheck_only

## 链路

| step | evidence_id | ledger_reference | status |
|---|---|---|---|
| authorization_request | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623` | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` | `real_measurement_authorization_request_blocked_until_real_window` |
| authorization_field_map | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-FIELD-MAP-20260623` | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` | `authorization_field_map_defined_precheck_only` |
| approval_signed_bundle | `HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623` | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` | `signed_approval_record_created_no_production_activation` |
| authorization_window_grant | `HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-WINDOW-GRANT-20260623` | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` | `real_measurement_authorization_window_granted_precheck_only` |
| sanitized_usage_ledger | `HEADROOM-LCX-SANITIZED-PRODUCTION-TOKEN-LEDGER-20260623` | `docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json` | `metadata_only_no_production_measurement` |

## 门禁

| item | value |
|---|---|
| same_ledger_reference | `true` |
| real_measurement_open | `false` |
| production_token_measurement_allowed | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本回放不表示真实测量已执行。
- 本回放不表示生产代理或生产 SDK 已启动。
- 本回放不表示真实 KDS 写入或外部 API 写入。
- 本回放不表示 accepted、integrated 或 production_ready。
