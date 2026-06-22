---
doc_id: GPCF-DOC-7B2E61A9D4
title: Current Session Mainline Declaration 20260622
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/current-session-mainline-declaration-20260622.md
source_path: docs/harness/evidence/current-session-mainline-declaration-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Current Session Mainline Declaration 20260622

本文件记录当前 GPCF 会话的 `session_mainline`，用于防止本会话偏离 LOOP 治理主线去执行其它会话、其它项目或其它任务包。

## 会话主线

| 字段 | 值 |
|---|---|
| `session_mainline` | LOOP治理主线: session-mainline-control rollout |
| `objective` | 把当前会话固定在 LOOP 会话主线治理、声明记录和防偏离门禁落地范围内 |
| `owner_session` | current_gpcf_loop_governance_session |
| `current_project` | GlobalCoud GPCF |
| `loop_mode` | L2-governance |
| `status_ceiling` | partial |

## 范围

| 字段 | 值 |
|---|---|
| `scope_in` | 会话主线控制包、声明模板、handoff 模板、当前声明 evidence、相关 validator、文档门禁 |
| `scope_out` | GFIS runtime repair、CodeGraph 跨仓 recheck、Agent-Reach 外部 API、Headroom 生产 token、真实 KDS API 写回、commit、push、deploy、状态升级 |
| `allowed_actions` | 受控文档、局部 validator、本地镜像、污染检查、KDS token 检查 |
| `forbidden_actions` | production write、external API write、real KDS API write、schema sync、bench migrate、deployment、permission change、commit、push、accepted、integrated、production_ready |
| `stop_conditions` | mainline_drift_detected、handoff_required_without_evidence、authorization_required、git_conflict_or_sensitive_file_risk、validator_hard_failure_outside_scope |

## Handoff 判定

| 字段 | 值 |
|---|---|
| `handoff_required` | false |
| `handoff_source` | none |
| `scope_delta` | current request continues the same LOOP governance mainline |
| `authorization_delta` | no additional authorization for commit, push, deploy, real API write, or status promotion |

## 偏离检查

| 检查项 | 结果 |
|---|---|
| 用户请求匹配当前主线 | true |
| 工作目录在 scope 内 | true |
| dirty 状态中非本轮 scope 不触碰 | true |
| 接管其它会话任务 | false |
| 跨项目执行 | false |
| `mainline_drift_detected` | false |
| `authorization_required` | false |

## 状态边界

| 边界 | 值 |
|---|---|
| accepted | false |
| integrated | false |
| production_ready | false |
| production_write | false |
| external_api_write | false |
| real_kds_api_write | false |
| commit | false |
| push | false |
| deploy | false |

## Validator

```bash
python3 tools/kds-sync/validate_current_session_mainline_declaration.py
python3 tools/kds-sync/validate_loop_session_mainline_control.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 下一轮

进入 `GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002`：把当前声明作为后续“继续/下一步”的默认前置核对输入。
