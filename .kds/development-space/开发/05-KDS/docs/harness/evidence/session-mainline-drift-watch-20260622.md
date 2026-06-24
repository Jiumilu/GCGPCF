---
doc_id: GPCF-DOC-3A9B82D614
title: Session Mainline Drift Watch 20260622
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/session-mainline-drift-watch-20260622.md
source_path: docs/harness/evidence/session-mainline-drift-watch-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Session Mainline Drift Watch 20260622

本证据定义当前会话后续请求的 drift watch。它只覆盖当前仓库内 LOOP 治理主线，不覆盖真实 Codex 其它线程。

## Watch Mode

| 字段 | 值 |
|---|---|
| current_session_mainline | LOOP治理主线: session-mainline-control rollout |
| watch_mode | repo_recorded_governance_only |
| live_codex_threads_covered | false |
| next_round | GPCF-SESSION-MAINLINE-HANDOFF-REQUEST-GATE-004 |

## 规则

| rule_id | match | decision | requires_authorization |
|---|---|---|---|
| same_mainline_continue | 下一步 / 继续 | continue_current_mainline_only | false |
| other_session_family | GFIS / CodeGraph / Agent-Reach / Headroom / Ontology-WAS / OKF / LCX | mainline_drift_detected | true |
| live_thread_access | 其它 Codex 线程 / 真实其它线程 / 接管会话 / 关闭会话 | authorization_required | true |
| write_or_release_action | commit / push / deploy / 真实 KDS API / 外部 API / schema sync / accepted / integrated / production_ready | authorization_required | true |

## Fixtures

| request | expected_decision | expected_authorization_required |
|---|---|---|
| 下一步 | continue_current_mainline_only | false |
| 继续 | continue_current_mainline_only | false |
| 继续 GFIS runtime repair | mainline_drift_detected | true |
| 执行 CodeGraph 跨仓 recheck | mainline_drift_detected | true |
| 接管其它 Codex 线程 | authorization_required | true |
| 提交并推送这些改动 | authorization_required | true |

## Forbidden Actions

- auto_takeover_live_codex_threads
- auto_execute_other_session_task
- auto_cross_repo_execution
- auto_external_api_write
- auto_real_kds_api_write
- auto_commit
- auto_push
- auto_deploy
- auto_status_promotion

## Validators

```bash
python3 tools/kds-sync/validate_session_mainline_drift_watch.py
python3 tools/kds-sync/validate_session_mainline_preflight_enforcement.py
python3 tools/kds-sync/validate_loop_session_registry.py
```
