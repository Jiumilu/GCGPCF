---
doc_id: GPCF-DOC-666816F27E
title: Headroom LCX Rollback Plan 20260622-001
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md
source_path: docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Rollback Plan 20260622-001

## Evidence ID

`HEADROOM-LCX-ROLLBACK-PLAN-20260622-001`

## 结论

本计划定义 Headroom 在真实测量或生产 branch 发生偏移时的回滚顺序。它只覆盖停止、隔离、恢复、验证，不授予生产准入，也不表示真实生产测量已发生。

## 触发条件

- 发现 production proxy 被打开
- 发现 production SDK 被启用
- 发现 real KDS write 或 external API write
- 发现未脱敏敏感材料被处理
- 发现头部证据被误写成 accepted、integrated 或 production_ready

## 回滚顺序

| step | action | owner | evidence |
|---|---|---|---|
| 1 | 立即停止受控 runner，冻结当前 round | GPCF | `loop_round_id` |
| 2 | 保持 `production_token_measurement_allowed=false`，`measured_production_tokens=false` | GPCF | graph manifest |
| 3 | 确认无 production proxy / SDK / external write / real KDS write | WAES | sensitive gate evidence |
| 4 | 回收并归档受控日志、token 计数、route manifest | KDS | harness evidence |
| 5 | 重新读取授权前置、measurement request 和 WAES/Harness decision | WAES/Harness | admission evidence |
| 6 | 仅在授权窗口重新成立后，恢复到 sanitized precheck，而不是 production | GPCF | precheck evidence |

## 验证

- `production_proxy_started=false`
- `production_sdk_enabled=false`
- `production_external_api_write=false`
- `kds_api_write=false`
- `sensitive_material_processed=false`
- `accepted=false`
- `integrated=false`
- `production_ready=false`

## 非声明

- 本计划不表示生产分支已打开。
- 本计划不表示真实业务等价性已证明。
- 本计划不表示真实生产 token 已测量。
- 本计划不表示 accepted、integrated 或 production_ready。
