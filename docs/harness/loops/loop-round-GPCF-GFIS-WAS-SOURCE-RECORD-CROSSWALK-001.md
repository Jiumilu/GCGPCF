---
doc_id: GPCF-DOC-B683C73FBF
title: Loop Round GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001.md
source_path: docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001

## 目标

把 GFIS 原生 source-record 字段和 WAS/Ontology 字段形成可填写、可审核、可机检的 crosswalk，降低未来真实客户订单或平台订单回执进入前的填报歧义。

## 本轮变更

- 新增 `docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.json`。
- 新增 `docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.md`。
- 新增 `tools/kds-sync/validate_gfis_was_source_record_field_crosswalk.py`。
- 更新 GPCF Loop 控制板和项目群状态矩阵。

## 检查

validator 必须证明：

- GFIS 原生必填字段为 12 项。
- WAS/Ontology 必填字段为 12 项。
- crosswalk entries 为 12 项。
- `objectFamily` 和 `kdsBacklink` 有明确等价规则。
- `assetDimension`、`flowType`、`lifecycle`、`trustLevel`、`nextAction` 有固定 WAS S01 规则。
- 不写入 GFIS 接收目录，不创建真实 source-of-record。

## loop_was_context

```yaml
project_scope: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
related_asset_dimensions: [data_asset]
related_flows: [commerce_flow]
related_objects: [CustomerRequirementOrPlatformOrder]
related_events: [gfis_was_source_record_field_crosswalk]
source_refs: [was://scenario/gfis-runtime-sop-e2e/S01-customer-requirement-or-platform-order]
evidence_refs: [docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.md]
waes_gate_refs: [waes://gate/customer-order-source-record-review]
kds_backlinks: [pending_real_source_record]
promotion_blockers: [valid_source_record_missing, customer_confirmation_missing]
next_action: wait_for_business_owner_candidate_then_apply_crosswalk
no_write_declaration: no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready
```

## 反馈

GFIS-WAS source-record crosswalk 已具备可填写和可审核基线。下一轮仍需要真实客户订单原件或平台订单回执；无真实输入前保持 hold 和 repair_required。
