---
doc_id: GPCF-DOC-0C02118386
title: GPCF L4 GFIS Repair 029 Runtime Raw Material Repair Candidate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-029.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-029.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 029 Runtime Raw Material Repair Candidate

## Round

- round_id: GPCF-L4-GFIS-REPAIR-029
- date: 2026-06-14
- subject: GFIS 运行层 / GPCF 总控
- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: partial
- stop_type: authorization_boundary

## Input

- GFIS runtime self-diagnosis still reports `runtime_gap_resolution_plan=repair_required`.
- Previous round created a candidate-only repair item for `production_execution`.
- `get_runtime_raw_material_gate` still reports blocked gates: `raw_material_plan`, `raw_material_batch`, `incoming_quality_inspection`.

## Action

- GFIS runner now creates a second `GFISActionableRepairCandidate` for `raw_material_plan`.
- GFIS runtime validator now requires runtime evidence to include both `production_execution` and `raw_material_plan` repair candidate calls.
- GFIS API contract validator now covers raw material repair candidate behavior.
- GPCF integrity validator now reads GFIS runtime evidence JSON and checks both candidate gaps.

## Validation

```text
GFIS runner:
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=29
created=13
cleanup_deleted=13
runtime_gaps=22
```

```text
GFIS validator:
gfis_runtime_sop_e2e=repair_required
runtime_raw_material_gate=blocked
runtime_gfis_repair_candidate=runtime_gfis_repair_candidate_passed_temp_created_cleanup_required
runtime_live_input_gate=missing_live_business_inputs
missing_inputs=5
production_write=false
real_external_api_write=false
gfis_validator_exit=2
```

```text
GFIS API contract:
gfis work-order API contract validation passed
created_docs=13 commits=13
```

```text
GFIS Demo E2E:
26 passed
status=pass_demo_only
```

## Boundary

- No production write.
- No real external API write.
- No stock, purchase receipt, incoming QA submit, WorkOrder completion, WAES/KDS final write, POD, finance confirmation, accepted or integrated status.
- Demo remains display regression only.

## Result

The project now has another real Loop Engineering self-repair step after self-diagnosis: `raw_material_plan` can be converted into a controlled GFIS runtime repair candidate and cleaned up. The full SOP E2E remains `repair_required`, and the project-group score remains frozen at 79/100.

## Next

Continue with another GFIS-owned actionable gap from `get_runtime_sop_gap_resolution_plan`, such as `raw_material_batch` or `incoming_quality_inspection`, or collect verified live business inputs for external dependency gaps.
