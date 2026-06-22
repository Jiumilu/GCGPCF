---
doc_id: GPCF-DOC-5966FE20DD
title: Loop Round GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-P2-MCP-SDK-DRY-RUN-SMOKE-001

## 输入

- 上轮输出：P1 proxy dry-run smoke 通过。
- 本轮目标：验证 SDK/MCP dry-run 能力和 retrieve gate。
- 本轮边界：不执行 `headroom mcp install`，不启动持久 MCP server，不调用 `headroom_retrieve`，不恢复敏感原文。

## 动作

1. 使用合成脱敏样例执行 Headroom SDK `compress()`。
2. 验证 MCP CLI、`mcp serve --help` 和 `mcp status --help`。
3. 检查 `mcp.json` 中 `headroom_retrieve` restricted、WAES gate、reason 和 Harness evidence 要求。
4. 检查 Harness evidence schema 包含 retrieve 和 production non-claim 字段。

## 输出

- `tools/kds-sync/run_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py`
- `tools/kds-sync/validate_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py`
- `docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.json`
- `docs/harness/evidence/headroom-lcx-p2-mcp-sdk-dry-run-smoke-20260621.md`

## 检查

```bash
HEADROOM_TELEMETRY=off /tmp/gpcf-headroom-runtime-probe/bin/python tools/kds-sync/run_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py
python3 tools/kds-sync/validate_headroom_lcx_p2_mcp_sdk_dry_run_smoke.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

本轮只验证 SDK/MCP dry-run 与 retrieve gate 配置。未安装 MCP、未启动持久 MCP server、未调用 retrieve、未恢复原文、未写 KDS、未外部 API 写入、未升级 accepted、integrated 或 production_ready。

## 下一轮

`GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001`：验证 learn preview 与工作记忆写入门禁，不自动修改受控规则文件。
