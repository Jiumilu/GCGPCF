---
doc_id: GPCF-DOC-9D362F48F8
title: Headroom LCX Authorized Measurement Authorization Template Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md
source_path: docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX Authorized Measurement Authorization Template Evidence

## Evidence ID

`HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621`

## 结论

已生成授权字段模板和审计包。本文件不构成授权完成，不允许采集生产 token，不允许启动生产代理，不允许真实 KDS 或外部 API 写入。

## 模板路径

`fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json`

## 必填字段

| field | required | current placeholder |
|---|---|---|
| `authorized_window_id` | required | `REQUIRED_USER_INPUT` |
| `authorized_by` | required | `REQUIRED_USER_INPUT` |
| `authorized_at` | required | `REQUIRED_USER_INPUT` |
| `sanitized_production_token_ledger` | required | `REQUIRED_USER_INPUT` |
| `rollback_plan_id` | required | `REQUIRED_USER_INPUT` |
| `waes_harness_admission_decision` | required | `REQUIRED_USER_INPUT` |

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| authorization_template_generated | true |
| authorization_complete | false |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS

## 下一步

由授权人补齐模板字段，并附 WAES/Harness 准入裁决后，重新运行授权测量前置检查。
