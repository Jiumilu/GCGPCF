---
doc_id: GPCF-DOC-52A3C9B7E1
title: GPCF Session Mainline Declaration 001
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DECLARATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-SESSION-MAINLINE-DECLARATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF Session Mainline Declaration 001

## 输入

- 用户连续指令：`下一步`。
- 上一轮输出：LOOP 会话主线控制包、主线声明模板、跨会话 handoff 模板和 `validate_loop_session_mainline_control.py` 已通过。
- 当前约束：不得偏离当前 LOOP 治理主线去执行 GFIS、CodeGraph、Agent-Reach、Headroom 或其它会话任务。

## 判断

当前主线应固定为 `LOOP治理主线: session-mainline-control rollout`。本轮只生成当前会话声明记录和 validator，不接管其它会话，不跨项目执行，不执行真实 API 写入、commit、push、deploy 或状态升级。

## 动作

- 新增 `docs/harness/evidence/current-session-mainline-declaration-20260622.json`。
- 新增 `docs/harness/evidence/current-session-mainline-declaration-20260622.md`。
- 新增 `tools/kds-sync/validate_current_session_mainline_declaration.py`。
- 将当前声明 validator 接入 `validate_loop_session_mainline_control.py` 和 `loop_document_gate.py`。

## 输出

- 当前会话 `session_mainline` 已声明。
- `mainline_drift_detected=false`。
- `handoff_required=false`。
- `status_ceiling=partial`。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 检查

```bash
python3 tools/kds-sync/validate_current_session_mainline_declaration.py
python3 tools/kds-sync/validate_loop_session_mainline_control.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

下一轮进入 `GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002`：每次继续前先读取当前声明记录，并将用户新请求与 `session_mainline`、`scope_in`、`scope_out`、`forbidden_actions` 对照。若不一致，报告 `mainline_drift_detected` 并请求确认。
