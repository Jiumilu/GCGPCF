---
doc_id: GPCF-DOC-4E83A9C210
title: LOOP 会话总账
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, XiaoG, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_SESSION_REGISTRY.md
source_path: 02-governance/loop/LOOP_SESSION_REGISTRY.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP 会话总账

本总账用于把仓库内已记录的 LOOP 会话、会话族和跨会话交接状态纳入统一治理。它只覆盖当前 GPCF 仓库内的 `docs/harness/loops/loop-round-*.md`、`docs/harness/evidence/*session*`、`docs/harness/evidence/*mainline*` 和相关 validator，不自动读取、接管、关闭或修改 Codex 侧其它真实线程。

## 1. 覆盖边界

| 边界 | 当前值 |
|---|---|
| registry_scope | repo_recorded_loop_sessions_only |
| live_codex_threads_covered | false |
| cross_repo_sessions_covered | false |
| auto_takeover_allowed | false |
| write_without_handoff_allowed | false |
| status_promotion_allowed | false |
| validator | `python3 tools/kds-sync/validate_loop_session_registry.py` |

如需治理真实 Codex 其它线程，必须由用户单独确认，并先生成 handoff evidence。没有确认时，本总账只能登记仓库内已有记录和风险。

## 2. 当前主会话

| 字段 | 值 |
|---|---|
| session_id | current_gpcf_loop_governance_session |
| session_mainline | LOOP治理主线: session-mainline-control rollout |
| current_declaration | `docs/harness/evidence/current-session-mainline-declaration-20260622.json` |
| owner | GPCF |
| status | active_controlled |
| status_ceiling | partial |
| handoff_required | false |
| mainline_drift_detected | false |
| next_round | GPCF-SESSION-MAINLINE-PREFLIGHT-ENFORCEMENT-002 |

## 3. 仓库内会话族总账

| session_family | pattern | owner | current_control | handoff_status | allowed_next_action |
|---|---|---|---|---|---|
| GFIS L4 repair and test sync | `GPCF-L4-GFIS*`, `GPCF-GFIS*` | GPCF/GFIS | real_business_lane remains repair_required | handoff_required_for_execution | read_only_registry_or_user_confirmed_handoff |
| KDS / DKS governance | `GPCF-KDS-DKS*`, `GPCF-GCKF*` | KDS/GPCF | KDS remains source of record | handoff_required_for_writeback | read_only_registry_or_user_confirmed_handoff |
| Ontology / WAS governance | `GPCF-ONTOLOGY-WAS*`, `GPCF-WAS*` | WAES/GPCF | semantic contract only, no business completion | handoff_required_for_execution | read_only_registry_or_user_confirmed_handoff |
| CodeGraph governance | `GPCF-CODEGRAPH*` | GPCF | sync/readiness work remains evidence bounded | handoff_required_for_cross_repo_execution | read_only_registry_or_user_confirmed_handoff |
| Agent-Reach governance | `GPCF-AGENT-REACH*` | WAES/GPCF | candidate/search governance only | handoff_required_for_external_api | read_only_registry_or_user_confirmed_handoff |
| Headroom / LCX governance | `GPCF-HEADROOM*` | WAES/GPCF | cost/runtime evidence only | handoff_required_for_measurement_or_production_token | read_only_registry_or_user_confirmed_handoff |
| OKF / ODF governance | `GPCF-OKF*` | KDS/GPCF | no-write or candidate gate unless separately authorized | handoff_required_for_writeback | read_only_registry_or_user_confirmed_handoff |
| GPCF CF / governance rounds | `GPCF-CF*`, `GPCF-L4-[0-9]*`, `GPCF-L4-CORR*`, `GPCF-L4-IMPROVE*` | GPCF | historical governance rounds | handoff_required_for_continuation | read_only_registry_or_user_confirmed_handoff |
| XiaoG evidence repair | `GPCF-L4-XIAOG*` | GPCF/XiaoG | evidence repair only | handoff_required_for_project_execution | read_only_registry_or_user_confirmed_handoff |
| Project group phase goals | `GPCF-PROJECT*` | GPCF | planning/governance only | handoff_required_for_execution | read_only_registry_or_user_confirmed_handoff |
| LOOP localization/governance | `GPCF-LOOP*` | GPCF | localization debt remains blocking | handoff_required_for_bulk_repair | read_only_registry_or_user_confirmed_handoff |
| UI governance and validation | `GPCF-UI*` | GPCF/Studio | UI gate evidence only, no acceptance promotion | handoff_required_for_page_refactor | read_only_registry_or_user_confirmed_handoff |
| Session declaration and mainline | `GPCF-SESSION*` | GPCF | declaration boundary and mainline control | active_controlled | continue_current_mainline_only |

## 4. 其它会话处理规则

- 未在本总账中归类的 `loop-round-*` 必须输出 `orphan_session_family`。
- 已归类但没有当前 handoff 的会话族，只能做只读登记、风险扫描和建议。
- 任何会话族进入写入、跨仓执行、真实外部 API、真实 KDS API、生产 token、commit、push、deploy、accepted、integrated 或 production_ready 前，必须重新请求用户确认。
- 多智能体并行产生的子会话必须绑定唯一 `owner_session` 和非重叠 scope；最终集成必须回到主会话。
- 当前会话不得因为发现其它会话未完成，就自动切换主线或执行其它会话任务。

## 5. 当前已知风险

| 风险 | 状态 | 处理 |
|---|---|---|
| live_codex_threads_not_indexed | accepted_boundary | 需要用户单独授权后才能读取或治理真实 Codex 其它线程 |
| repo_dirty_large_existing_work | controlled_boundary | 本总账只做 scoped 文档和 validator，不清理无关 dirty 文件 |
| localization_debt | rework_required | `loop_document_gate.py --check-only` 继续保持 `rework_required` |
| historical_rounds_without_explicit_session_mainline | governed_by_family_registry | 通过会话族总账约束，不批量改写历史 round |

## 6. Validator

```bash
python3 tools/kds-sync/validate_loop_session_registry.py
```

该 validator 必须确认：

- 本总账为 `controlled`。
- 当前主会话声明存在并通过。
- 所有仓库内 `loop-round-*.md` 均能映射到已登记 `session_family`。
- 不存在 `write_without_handoff_allowed=true`、`auto_takeover_allowed=true` 或状态自动升级表述。
- `loop_document_gate.py` 接入 `validate_loop_session_registry.py`。
