---
doc_id: GPCF-DOC-58AA82BBE3
title: Loop Round GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001

## 输入

- 用户授权执行 `GPCF-HEADROOM-LCX-P1-PROXY-DRY-RUN-SMOKE-001`。
- 授权边界：允许本机开发态 `HEADROOM_TELEMETRY=off` 启动/验证 proxy dry-run；禁止生产代理、真实 KDS 写入、外部 API 写入和未脱敏敏感材料处理。
- 上轮输出：P0 runtime replay 通过。

## 动作

1. 补齐隔离环境中的 `headroom-ai[proxy]==0.26.0` proxy extra。
2. 验证生产代理门禁：`HEADROOM_PRODUCTION_PROXY=true` 时 `start-proxy.sh` 必须拒绝启动。
3. 在随机本地端口启动 dry-run proxy。
4. 访问 `/livez` 验证本机 proxy 可用。
5. 终止 dry-run proxy，并记录没有发送 LLM 请求、没有外部写入、没有 KDS 写入。

## 输出

- `tools/kds-sync/run_headroom_lcx_p1_proxy_dry_run_smoke.py`
- `tools/kds-sync/validate_headroom_lcx_p1_proxy_dry_run_smoke.py`
- `docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.json`
- `docs/harness/evidence/headroom-lcx-p1-proxy-dry-run-smoke-20260621.md`

## 检查

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_lcx_p1_proxy_dry_run_smoke.py
python3 tools/kds-sync/validate_headroom_lcx_p1_proxy_dry_run_smoke.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮只验证本机开发态 proxy dry-run smoke。未发送 LLM 请求，未处理敏感材料，未生产代理，未真实 KDS 写入，未外部 API 写入，未升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001`：验证 MCP/SDK dry-run 能力和 retrieve gate，不恢复敏感原文，不写生产链路。
