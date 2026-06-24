---
doc_id: GPCF-DOC-73CBDABF8E
title: GPCF-L4-GFIS-REPAIR-073 GFIS KDS canonical discovery truth guard
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-073.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-073.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-073 GFIS KDS canonical discovery truth guard

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：围绕用户指出的“5 类真实凭证缺口可通过检索 KDS 获取”，把 GFIS 的 KDS 检索范围从固定白名单扩展为全 KDS canonical read-only 自动发现，同时建立自动发现材料不得直接验真的防污染门禁。

## 输入

- GFIS `scripts/harvest_gfis_kds_gehu_inputs.py`
- GFIS `scripts/validate_gfis_runtime_sop_e2e.py`
- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`
- KDS canonical root：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS`

## 本轮动作

- GFIS 新增 `kds_canonical_discovered_readonly` 自动发现源。
- 自动发现必须覆盖报价发出审批规则、销售订单管控体系、葛化供应链代运营协议、葛化项目深度分析报告。
- 首次发现过宽后，GFIS 已排除 `.codex`、`.harness` 工程痕迹，并按业务路径与业务关键词排序。
- GFIS 主 validator 新增 discovery 门禁，防止后续退回固定白名单检索。
- GFIS harvester 增加 `discovered_kds_source_requires_formal_intake_not_auto_verified` 阻断原因，防止 KDS 历史描述、功能说明或治理材料自动成为 `verified_live_artifact`。

## 验证结果

```text
kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5
kds_canonical_discovered_readonly_source_count=260
required_discovered_sources=true
liaoning_yuanhang_sample_test_record candidates=161 status=candidate_found_not_verified
jiangxi_subcontract_sample_production_record candidates=50 status=candidate_found_not_verified
liaoning_yuanhang_project_quotation candidates=271 status=candidate_found_not_verified
modern_jinggong_mass_production_release candidates=237 status=candidate_found_not_verified
gfis_runtime_sop_e2e=repair_required
runtime_liaoning_yuanhang_quotation_confirmation=formal_customer_confirmation_missing:formal=0:weak=7:attachments=7
runtime_verified_artifact_submission_counts=real_submissions:0,structure_valid:0,rejected_examples:1,pending_business_verification_examples:1,verified_artifacts:0
```

## 真实性边界

- KDS discovery 证明候选材料覆盖更广，不证明业务事实完成。
- 自动发现材料不能绕过 formal intake、source record hash、KDS backlink、验证人/方法、客户确认函、签收附件、转量产批准或 WAES evidence ref。
- `missing_live_business_inputs=5`、`real_submissions=0`、`verified_artifacts=0`、`runtime_sop_e2e=repair_required` 保持不变。
- 不恢复 100/100，不升级 accepted/integrated。

## 禁止动作

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行数据库迁移、bench migrate 或 schema sync。
- 未执行权限、Token 或生产配置变更。
- 未写 WAES/KDS/POD 真实业务事实。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 5
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

继续围绕 top priority `liaoning_yuanhang_project_quotation` 补收辽宁远航客户确认函、客户盖章/签字确认或等效正式确认原件的脱敏索引。若 KDS 只能提供报价 PDF、报价发出审批、口头认可、微信发送、采购计划或会议纪要，则仍保持 `repair_required`。
