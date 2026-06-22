---
doc_id: GPCF-DOC-22C297756A
title: Headroom LCX P1 Proxy Dry-run Smoke Evidence
project: KDS
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX P1 Proxy Dry-run Smoke Evidence

## Evidence ID

`HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-20260621`

## 结论

P1 proxy dry-run smoke 已完成。本轮只在本机开发态启动随机端口 dry-run proxy，并验证 `/livez`；同时验证生产代理门禁会拒绝启动。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | 15 |
| headroom_version | 0.26.0 |
| telemetry | off |
| proxy_dry_run_gate | true |
| production_proxy_refused | true |
| dry_run_livez_pass | true |
| dry_run_livez_status | 200 |
| process_terminated | true |
| llm_request_sent | false |
| external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 不生产代理。
- 不发送 LLM 请求。
- 不真实 KDS 写入。
- 不真实外部 API 写入。
- 不处理未脱敏敏感材料。
- 不升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001`
