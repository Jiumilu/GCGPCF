---
doc_id: GPCF-DOC-FE20CDD358
title: Loop Governance Dashboard
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
source_path: 02-governance/loop/LOOP_GOVERNANCE_DASHBOARD.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Loop Governance Dashboard

## Purpose

This dashboard records LOOP governance signals for quality, efficiency, self-correction, boundary safety, reproducibility, and status ceiling.

It is a governance dashboard, not a business completion dashboard. Passing or improving these indicators does not mean GFIS, GPCF, WAES, KDS, UAT, production, finance, customer acceptance, or integrated status is complete.

## Current Snapshot

| Signal | Current Value | Meaning | Next Governance Action |
|---|---|---|---|
| phase_goal | `LOOP-GOV-PHASE-20260617` | Governance phase goal is active and machine-validated | Keep phase goal validator in governance docs gate |
| quality_gate | `repair_ceiling_enforced` | GFIS Demo, KDS candidate, request package, template, user statement, and Loop records must not replace runtime facts | Keep role boundary and self-correction validators active |
| efficiency_risk | `review_required` | Long sequence and historical round-record debt remain visible as LEDB-001 to LEDB-004 | Review backlog items without rewriting facts in bulk |
| self_correction_gate | `blocked_expected` | GFIS runtime SOP E2E remains `repair_required`; false completion remains invalidated | Keep blocker visible until implementation main process fixes runtime evidence |
| boundary_safety | `pass` | Governance process is separated from implementation main process | Continue forbidding production writes, schema sync, deployment, and accepted/integrated upgrades |
| status_ceiling | `partial_repair` | Runtime primary key, review queue, runtime intake, WAES review, and verified artifact remain 0 | Do not upgrade status while runtime SOP is repair_required |
| reproducibility | `local_validators_present` | The governance conclusions can be re-run locally | Keep command list current in evidence |

## Metric Groups

### Quality

| Metric | Value | Gate |
|---|---|---|
| false_completion_claim_allowed | false | pass |
| demo_as_runtime_allowed | false | pass |
| request_package_as_source_record_allowed | false | pass |
| accepted_integrated_without_human_allowed | false | pass |

### Efficiency

| Metric | Value | Gate |
|---|---|---|
| loop_efficiency_risk | `review_required` | visible_debt |
| hard_window_truth_fields_missing | 0 | pass |
| hard_window_five_segment_missing | 0 | pass |
| audit_window_truth_fields_missing | 14 | review_required |
| audit_window_five_segment_missing | 19 | review_required |
| max_consecutive_sequence | 183 | review_required |

### Self-Correction

| Metric | Value | Gate |
|---|---|---|
| self_correction_gate | `blocked` | expected_repair_ceiling |
| gfis_runtime_subject | `pass` | pass |
| historical_demo_evidence | `invalidated` | pass |
| runtime_sop_e2e | `repair_required` | blocked_expected |
| project_group_score | 79 | repair |

### Boundary Safety

| Metric | Value | Gate |
|---|---|---|
| governance_process_bounded | true | pass |
| implementation_process_separate | true | pass |
| production_write_allowed | false | pass |
| schema_sync_allowed | false | pass |
| git_push_allowed | false | pass |
| accepted_integrated_allowed | false | pass |

### Status Ceiling

| Metric | Value | Gate |
|---|---|---|
| runtime_primary_key_ready | 0 | blocked_expected |
| review_queue | 0 | blocked_expected |
| runtime_intake | 0 | blocked_expected |
| waes_review | 0 | blocked_expected |
| verified | 0 | blocked_expected |

## Commands

| Command | Purpose |
|---|---|
| `python3 tools/kds-sync/validate_loop_governance_dashboard.py` | Validate this dashboard and dashboard evidence |
| `python3 tools/kds-sync/validate_loop_governance_phase_goal.py` | Validate phase goal and status ceiling |
| `python3 tools/kds-sync/validate_loop_round_efficiency_audit.py` | Validate efficiency audit hard window and expose historical debt |
| `python3 tools/kds-sync/validate_loop_self_correction_gate.py` | Validate self-correction ceiling and GFIS runtime repair state |
| `python3 tools/kds-sync/validate_loop_governance_role_boundary.py` | Validate governance/implementation boundary |

## Non-Claims

- This dashboard does not prove source-of-record receipt.
- This dashboard does not create runtime primary key, review queue, runtime intake, WAES review, or verified artifact.
- This dashboard does not prove UAT, production, customer satisfaction, finance, accepted, or integrated completion.
- This dashboard does not authorize production write, external API write, schema sync, bench migrate, deployment, permission change, commit, or push.

## Next Dashboard Work

1. Review LEDB-001 to LEDB-004 and record disposition for each debt item.
2. Add trend snapshots once the same dashboard gate has run across multiple governance turns.
3. Keep implementation next steps focused on real GFIS source-record submission while governance tracks evidence quality and boundaries.
