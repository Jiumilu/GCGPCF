---
doc_id: GPCF-DOC-DB3EB9E54C
title: GPCF-L4-GFIS-REPAIR-273
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-273.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-273.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-273

## 本轮目标

把 GFIS 真项目仓 `GFIS-RUNTIME-SOP-E2E-263` 的 `CustomerRequirementOrPlatformOrder` runtime primary key negative/pollution guard 回写到 GPCF 总控。

## 已同步事实

- GFIS 运行层仍是唯一 SOP 实现主体。
- GFIS Demo E2E 只作为展示层回归，不作为业务验收主体。
- 本轮 GFIS 只处理 `01_customer_requirement_platform_order` 一个阶段。
- GFIS Demo、KDS candidate-only、报价单、Loop 文档、口述事实、mock/fixture/培训资料均不能打开运行层主键门禁。

## GFIS 263 输出

```text
source_runtime_primary_key_gate_items=1
source_runtime_primary_key_gate_blocked=1
source_valid_source_records=0
weak_primary_key_open_attempts=6
rejected_primary_key_open_attempts=6
accepted_primary_key_open_attempts=0
demo_substitution_attempts=1
kds_candidate_only_attempts=1
quotation_only_attempts=1
loop_document_claim_attempts=1
oral_statement_attempts=1
mock_fixture_attempts=1
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

- GFIS `python3 scripts/validate_gfis_sop_e2e_263.py`：pass。
- GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py`：fail，原因是 `KDS coverage must not have missing controlled sources`。
- GFIS `npm run test:e2e`：26 passed，仅作为 demo/frontend 回归。
- GFIS scoped `git diff --check -- ...`：pass。

## 真实性计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 结论

GPCF 已同步 GFIS 263。当前仍不得降低 GFIS/GPCF 阻塞级别：

- weak_primary_key_open_attempts=6
- rejected_primary_key_open_attempts=6
- accepted_primary_key_open_attempts=0
- runtime_primary_key_created=0
- runtime_primary_key_ready=0
- review_queue=0
- runtime_intake=0
- waes_review=0
- verified=0
- runtime_sop_e2e=repair_required

真正最小闭环仍未形成。只有至少一个阶段打通 `source record -> runtime primary key -> review queue -> runtime intake -> WAES review -> verified artifact`，才可进入闭环判定。
