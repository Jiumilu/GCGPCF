---
doc_id: GPCF-DOC-LOOP-SESSION-HANDOFF-REQUEST-GATE-004
title: LOOP Round GPCF Session Mainline Handoff Request Gate 004
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004.md
source_path: docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF Session Mainline Handoff Request Gate 004

## 输入

- 用户要求继续推进 LOOP 主线治理。
- 上一轮 drift-watch 已识别其它会话、跨仓执行、真实线程操作和发布动作需要授权。

## 判断

- 当前会话只能继续 `LOOP治理主线: session-mainline-control rollout`。
- 其它会话和项目族可以被纳入治理视图，但不能被当前会话自动接管。

## 动作

- 新增 handoff request gate 证据。
- 新增 validator，校验 proposal-only 规则和 fixtures。
- 将 handoff request gate 纳入总门禁和 session registry 反向检查。

## 输出

- `docs/harness/evidence/session-mainline-handoff-request-gate-20260622.json`
- `docs/harness/evidence/session-mainline-handoff-request-gate-20260622.md`
- `tools/kds-sync/validate_session_mainline_handoff_request_gate.py`

## 检查

- `python3 tools/kds-sync/validate_session_mainline_handoff_request_gate.py`
- `python3 tools/kds-sync/validate_session_mainline_drift_watch.py`
- `python3 tools/kds-sync/validate_loop_session_registry.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`

## 反馈

- 任何其它会话、跨仓执行、真实线程操作、发布或状态升级请求，必须先回答建议并等待用户确认。
- 下一轮进入 `GPCF-SESSION-MAINLINE-CROSS-THREAD-LEDGER-005`，把 repo-recorded 会话族转换为可查询的跨会话治理台账。
