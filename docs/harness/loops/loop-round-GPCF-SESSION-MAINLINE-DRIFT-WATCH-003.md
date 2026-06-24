---
doc_id: GPCF-DOC-8D6E4A1F29
title: GPCF Session Mainline Drift Watch 003
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DRIFT-WATCH-003.md
source_path: docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DRIFT-WATCH-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF Session Mainline Drift Watch 003

## 输入

- 当前主线：`LOOP治理主线: session-mainline-control rollout`。
- 前置证据：`docs/harness/evidence/session-mainline-preflight-enforcement-20260622.json`。
- 会话总账：`02-governance/loop/LOOP_SESSION_REGISTRY.md`。

## 判断

仅 `下一步`、`继续` 等同主线推进请求可直接继续当前治理主线。涉及其它会话族、真实 Codex 线程、跨仓执行、真实 API、commit、push、deploy 或状态升级的请求必须转为 `mainline_drift_detected` 或 `authorization_required`。

## 动作

- 新增 drift watch evidence JSON/Markdown。
- 新增 `validate_session_mainline_drift_watch.py`。
- 接入会话总账 validator 和总文档门禁。

## 输出

- `watch_mode=repo_recorded_governance_only`。
- `live_codex_threads_covered=false`。
- 负例：GFIS、CodeGraph、其它 Codex 线程、commit/push 均被拦截为 drift 或 authorization。

## 检查

```bash
python3 tools/kds-sync/validate_session_mainline_drift_watch.py
python3 tools/kds-sync/validate_session_mainline_preflight_enforcement.py
python3 tools/kds-sync/validate_loop_session_registry.py
```

## 反馈

下一轮进入 `GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004`：建立用户授权后的 handoff request gate，用于在用户明确要求治理真实其它会话时收集授权、scope 和证据。
