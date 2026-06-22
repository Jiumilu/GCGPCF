---
doc_id: GPCF-DOC-2F7E9A6C31
title: GPCF Session Mainline Preflight Enforcement 002
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002.md
source_path: docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF Session Mainline Preflight Enforcement 002

## 输入

- 用户请求：`下一步`。
- 当前主线声明：`docs/harness/evidence/current-session-mainline-declaration-20260622.json`。
- 仓库内会话总账：`02-governance/loop/LOOP_SESSION_REGISTRY.md`。

## 判断

本轮请求匹配当前 LOOP 治理主线。没有请求读取或接管真实 Codex 其它线程，没有请求跨仓执行、真实 API 写入、commit、push、deploy 或状态升级。

## 动作

- 新增 preflight evidence JSON/Markdown。
- 新增 `validate_session_mainline_preflight_enforcement.py`。
- 将 preflight validator 接入 `validate_loop_session_registry.py` 和 `loop_document_gate.py`。

## 输出

- `preflight_decision=continue_current_mainline_only`。
- `mainline_drift_detected=false`。
- `handoff_required=false`。
- `authorization_required=false`。
- `orphan_session_family=0`。

## 检查

```bash
python3 tools/kds-sync/validate_session_mainline_preflight_enforcement.py
python3 tools/kds-sync/validate_loop_session_registry.py
python3 tools/kds-sync/validate_loop_session_mainline_control.py
```

## 反馈

下一轮进入 `GPCF-SESSION-MAINLINE-DRIFT-WATCH-003`：对后续用户请求建立 drift watch，若请求指向其它会话族、跨仓执行、真实 API、提交推送或状态升级，则输出 `mainline_drift_detected` 或 `authorization_required`，并先请求确认。
