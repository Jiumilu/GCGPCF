---
doc_id: GPCF-DOC-660DA56C65
title: GPCF-L4-GFIS-REPAIR-272
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-272.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-272.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-272

## 本轮目标

把 GFIS 真项目仓 `GFIS-RUNTIME-SOP-E2E-262` 的 `CustomerRequirementOrPlatformOrder` runtime primary key gate 回写到 GPCF 总控。

## 已同步事实

- GFIS 运行层仍是唯一 SOP 实现主体。
- GFIS Demo E2E 只作为展示层回归，不作为业务验收主体。
- 本轮 GFIS 只处理 `01_customer_requirement_platform_order` 一个阶段。
- 当前没有 valid source record，因此 runtime primary key gate 必须阻断。

## GFIS 262 输出

```text
source_record_index_files_found=0
valid_source_records=0
source_record_to_runtime_primary_key_ready=0
runtime_primary_key_gate_items=1
runtime_primary_key_gate_blocked=1
runtime_primary_key_created=0
runtime_primary_key_ready=0
review_queue=0
runtime_intake=0
waes_review=0
verified=0
blocked=1
runtime_sop_e2e=repair_required
```

## 验证

- GFIS `python3 scripts/validate_gfis_sop_e2e_262.py`：pass。
- GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py`：fail，原因是 `KDS coverage must not have missing controlled sources`。
- GFIS `npm run test:e2e`：26 passed，仅作为 demo/frontend 回归。
- GFIS `git diff --check -- .`：pass。

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 结论

GPCF 已同步 GFIS 262。当前仍不得降低 GFIS/GPCF 阻塞级别：

- valid_source_records=0
- runtime_primary_key_gate_blocked=1
- runtime_primary_key_created=0
- runtime_primary_key_ready=0
- review_queue=0
- runtime_intake=0
- waes_review=0
- verified=0
- runtime_sop_e2e=repair_required

真正最小闭环仍未形成。只有至少一个阶段打通 `source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact`，才可进入闭环判定。
