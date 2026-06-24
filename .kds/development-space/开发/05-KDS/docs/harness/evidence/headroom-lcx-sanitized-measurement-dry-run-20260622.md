---
doc_id: GPCF-DOC-A1E6CF72D2
title: Headroom LCX Sanitized Measurement Dry Run Evidence 20260622
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md
source_path: docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Sanitized Measurement Dry Run Evidence 20260622

## Evidence ID

`HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-20260622`

## 结论

本轮只执行 `--check-only` 脱敏台账结构检查。未计算真实生产 token 节省，未启动 Headroom proxy，未写入真实 KDS API，未触达外部 API。

## 输入

| artifact | path |
|---|---|
| sanitized ledger | `fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json` |
| WAES/Harness admitted decision | `docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.json` |
| authorized measurement precheck | `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json` |

## 门禁

| 项 | 当前值 |
|---|---|
| sanitized_measurement_dry_run_gate | true |
| check_only | true |
| waes_harness_admitted | true |
| authorized_precheck_gate | true |
| entry_count | 1 |
| saving_rate | not_calculated |
| tokens_saved | not_calculated |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| kds_api_write | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一步

下一轮可增加只读 metadata replay 校验，但仍不得读取原文、不得计算真实生产节省、不得启动生产代理。
