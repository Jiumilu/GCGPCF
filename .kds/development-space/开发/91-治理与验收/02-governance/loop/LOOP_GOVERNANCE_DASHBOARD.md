---
doc_id: GPCF-DOC-FE20CDD358
title: Loop Governance Dashboard
project: WAES
related_projects: [GFIS, WAES, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Governance Dashboard

## 当前信号

| Signal | Value | Meaning |
|---|---|---|
| quality_gate | repair_ceiling_enforced | 治理结论不得越过当前真实业务修复上限 |
| efficiency_risk | review_required | 历史轮次效率债仍需持续审查 |
| self_correction_gate | blocked_expected | 自我纠错门禁继续阻断虚假完成态 |
| boundary_safety | pass | 当前治理边界仍然清楚 |
| status_ceiling | partial_repair | 当前项目群治理状态上限仍为 `partial_repair` |
| reproducibility | local_validators_present | 本地 validator 与 evidence 仍可复跑 |

## 关键指标

| Metric | Value |
|---|---|
| runtime_primary_key_ready | 0 |
| review_queue | 0 |
| runtime_intake | 0 |
| waes_review | 0 |
| verified | 0 |
| accepted_integrated_allowed | false |

## 执行命令

- `python3 tools/kds-sync/validate_loop_governance_dashboard.py`
- `python3 tools/kds-sync/validate_loop_governance_phase_goal.py`
- `python3 tools/kds-sync/validate_loop_round_efficiency_audit.py`
- `python3 tools/kds-sync/validate_loop_self_correction_gate.py`
- `python3 tools/kds-sync/validate_loop_governance_role_boundary.py`

## 非声明事项

This dashboard does not prove source-of-record receipt.

- 本看板不创建 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本看板不证明 GFIS runtime SOP E2E 已完成。
- 本看板不证明 accepted、integrated、production_ready 或业务完成。
- 本看板不授权 production write、external API write、schema sync、bench migrate、deployment、permission change、commit 或 push。
