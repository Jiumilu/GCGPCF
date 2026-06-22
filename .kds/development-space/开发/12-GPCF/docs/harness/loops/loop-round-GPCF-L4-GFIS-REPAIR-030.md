---
doc_id: GPCF-DOC-1E1A4202C8
title: GPCF L4 GFIS Repair 030 运行时原料批次修复候选
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-030.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-030.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF L4 GFIS Repair 030 运行时原料批次修复候选

## 轮次

- round_id: GPCF-L4-GFIS-REPAIR-030
- date: 2026-06-14
- subject: GFIS 运行层 / GPCF 总控
- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: partial
- stop_type: authorization_boundary

## 输入

- GFIS 运行时自诊断仍报告 `runtime_gap_resolution_plan=repair_required`。
- 上一轮已为 `raw_material_plan` 创建 candidate-only 修复项。
- `get_runtime_raw_material_gate` still reports blocked gates: `raw_material_plan`, `raw_material_batch`, `incoming_quality_inspection`.

## 动作

- GFIS runner 现在为 `raw_material_batch` 创建第三个 `GFISActionableRepairCandidate`。
- GFIS 运行时验证器现在要求运行时 evidence 包含 `production_execution`、`raw_material_plan` 和 `raw_material_batch` 修复候选调用。
- GFIS API contract 验证器现在覆盖原料批次修复候选行为。
- GPCF 完整性验证器现在读取 GFIS 运行时 evidence JSON，并检查全部三个候选缺口。

## 验证

```text
GFIS runner:
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=30
created=14
cleanup_deleted=14
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
created_docs=14 commits=14
```

```text
GFIS Demo E2E:
26 passed
status=pass_demo_only
```

## 边界

- 不进行生产写入。
- 不进行真实外部 API 写入。
- 不创建库存、批次、采购收货、来料 QA 提交、WorkOrder 完成、WAES/KDS 最终写入、POD、财务确认、accepted 或 integrated 状态。
- Demo 仍仅作为显示回归验证。

## 结果

项目现在具备自诊断后的另一个真实 Loop Engineering 自修复步骤：`raw_material_batch` 可以转换为受控 GFIS 运行时修复候选并完成清理。完整 SOP E2E 仍保持 `repair_required`，项目群评分继续冻结在 79/100。

## 下一步

继续处理 `get_runtime_sop_gap_resolution_plan` 中另一个 GFIS 负责的可执行缺口，例如 `incoming_quality_inspection`，或为外部依赖缺口收集已验证真实业务输入。
