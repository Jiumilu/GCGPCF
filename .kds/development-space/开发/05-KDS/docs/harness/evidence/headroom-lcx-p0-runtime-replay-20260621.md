---
doc_id: GPCF-DOC-0F02316005
title: Headroom LCX P0 Runtime Replay Evidence
project: KDS
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p0-runtime-replay-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX P0 Runtime Replay Evidence

## Evidence ID

`HEADROOM-LCX-P0-RUNTIME-REPLAY-20260621`

## 结论

P0 runtime replay 已在隔离 Headroom runtime 下完成。Headroom CLI help、脚本语法、成本模型回放和 LCX 受控 package payload 压缩测量均已执行。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| headroom_version | 0.26.0 |
| telemetry | off |
| runtime_replay_gate | true |
| headroom_cli_help_pass | true |
| script_syntax_gate | true |
| cost_model_replay_gate | true |
| marker_gate | true |
| tokens_before | 3285 |
| tokens_after | 3285 |
| tokens_saved | 0 |
| saving_rate | 0.0 |
| production_proxy_started | false |
| learn_apply_executed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 不生产代理。
- 不真实 KDS 写入。
- 不真实外部 API 写入。
- 不数据库迁移。
- 不权限变更。
- 不部署。
- 不升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001`
