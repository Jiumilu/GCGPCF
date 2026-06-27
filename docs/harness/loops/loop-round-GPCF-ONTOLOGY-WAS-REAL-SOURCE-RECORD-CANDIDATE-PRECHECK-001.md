---
doc_id: GPCF-DOC-0806C18276
title: Loop Round GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: ontology-governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001

## 输入

上一轮 `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001` 已建立真实 source-record intake package。当前目标是建立 P4 candidate precheck 闭环。

当前没有业务 owner 提交的真实客户订单原件或平台订单回执。

## 动作

- 新增 P4 真实 source-record candidate 模板。
- 新增 1 个正例夹具和 4 个负例夹具。
- 新增 P4 candidate precheck validator。
- 新增 P4 evidence。
- 保持无真实 source-record 时的 hold 边界。

## 输出

- `docs/harness/intake/was-real-source-record-candidate-template.yaml`
- `fixtures/was/p4-real-source-record-candidate-positive.json`
- `fixtures/was/p4-real-source-record-candidate-negative-llm-only.json`
- `fixtures/was/p4-real-source-record-candidate-negative-missing-source.json`
- `fixtures/was/p4-real-source-record-candidate-negative-missing-runtime-site-context.json`
- `fixtures/was/p4-real-source-record-candidate-negative-wrong-dimension.json`
- `docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.json`
- `docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md`
- `tools/kds-sync/validate_was_real_source_record_candidate_precheck.py`

## 检查

验证器必须证明：

- 模板存在且 `template_only=true`。
- 正例夹具可以通过 P4 语义预检。
- 4 个负例夹具全部被拒收。
- 真实 candidate 文件数为 0。
- `accepted_for_next_gate=0`。
- `hold_required=1`。
- `runtime_primary_key_ready=0`。
- `waes_review=0`。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## loop_was_context

```yaml
project_scope: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
related_asset_dimensions: [data_asset]
related_flows: [commerce_flow]
related_objects: [CustomerRequirementOrPlatformOrder]
related_events: [was_real_source_record_candidate_precheck]
source_refs: [was://scenario/gfis-runtime-sop-e2e/S01-customer-requirement-or-platform-order]
evidence_refs: [docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md]
waes_gate_refs: [waes://gate/customer-order-source-record-review]
kds_backlinks: [pending_real_source_record]
promotion_blockers: [valid_source_record_missing, customer_confirmation_missing, accepted_for_next_gate_missing]
next_action: wait_for_business_owner_real_candidate
no_write_declaration: no_gfis_runtime_write_no_kds_official_fact_no_waes_review_no_accepted_integrated_or_production_ready
```

## 反馈

P4 candidate precheck 闭环已建立，但真实 source-record 尚未出现。下一步仍需业务 owner 提交真实客户订单原件或平台订单回执；在此之前不得进入 runtime、WAES review、accepted、integrated 或 production_ready。
