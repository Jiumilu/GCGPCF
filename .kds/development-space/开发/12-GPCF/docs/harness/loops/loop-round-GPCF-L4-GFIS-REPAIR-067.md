---
doc_id: GPCF-DOC-C6B459B8FC
title: GPCF-L4-GFIS-REPAIR-067 GFIS KDS retrieval checklist refresh
project: GPCF
related_projects: [GFIS, GPC, PVAOS, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-067.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-067.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-067 GFIS KDS retrieval checklist refresh

## 轮次目标

按 Loop 新真实性规则完成 1 个真实实质轮次：根据用户再次确认的辽宁远航样箱、江西委托生产、5 月报价和 6 月现代精工量产计划，复跑 GFIS KDS 检索与原始凭证采集清单生成器，把最新候选数和缺字段回写到 GFIS 独立仓与 GPCF 总控。

## 输入

- 用户补充业务事实：2026-01 向辽宁远航提供 23 个样箱测试；样箱委托江西一家工厂生产；2026-05 辽宁远航计划采购并提交项目报价单；2026-06 计划使用现代精工产线组织量产。
- GFIS `scripts/harvest_gfis_kds_gehu_inputs.py`
- GFIS `scripts/build_gfis_liaoning_yuanhang_proof_collection_checklist.py`
- GFIS `scripts/validate_gfis_liaoning_yuanhang_proof_collection_checklist.py`
- GFIS `docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json`
- GFIS `docs/harness/sop-e2e/liaoning-yuanhang-original-proof-collection-checklist.md`

## 本轮动作

- GFIS 重新运行 KDS scanner，输出 `categories=8/8 missing_live_business_inputs=5`。
- GFIS 重新生成辽宁远航原始凭证采集 JSON/Markdown 清单。
- GFIS 候选数校准为样箱测试 55、江西委外 9、报价 48、现代精工转量产 57。
- GPCF 记录该轮为候选检索与清单校准，不作为业务验真或 SOP E2E 通过。

## 验证结果

```text
python3 scripts/harvest_gfis_kds_gehu_inputs.py:
kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5

python3 scripts/build_gfis_liaoning_yuanhang_proof_collection_checklist.py:
liaoning_yuanhang_original_proof_collection_checklist=written items=4 open=4 verified=0 runtime_sop_e2e=repair_required

python3 scripts/validate_gfis_liaoning_yuanhang_proof_collection_checklist.py:
liaoning_yuanhang_original_proof_collection_checklist=pass items=4 open=4 verified=0 runtime_sop_e2e=repair_required

python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py && python3 scripts/validate_gfis_runtime_sop_e2e.py:
gfis_runtime_sop_e2e_dry_run=partial
runtime_calls=47 created=19 cleanup_deleted=19 subject=GFIS运行层 demo_substitution=false production_write=false runtime_gaps=34
gfis_runtime_sop_e2e=repair_required
missing_inputs=5 missing_kds_source_paths=0
runtime_verified_artifact_submission=missing_verified_artifact_submission
runtime_sop_e2e_master=failed_or_repair_required
validate_exit=2
```

## 真实性边界

- `verified_proof_item_count=0`。
- `missing_live_business_inputs=5`。
- `runtime_sop_e2e=repair_required`。
- KDS 候选只证明“可检索、可定位、可缩小采集范围”，不证明样箱测试、江西委托生产、报价客户确认或现代精工转量产已经验真。
- GFIS Demo E2E 仍只是 `pass_demo_only`。

## 禁止动作

- 未执行 Git push。
- 未执行生产写入。
- 未执行真实外部 API 写入。
- 未执行数据库迁移、`bench migrate` 或 schema sync。
- 未执行权限变更、部署或生产配置修改。
- 未升级 `accepted` 或 `integrated`。

## 计数

- declared_rounds: 1/15
- substantive_rounds: 1/15
- generated_items: 3
- batch_generated: false
- substance_gate: pass
- stop_type: authorization_boundary

## 下一步

优先接收首个脱敏原始凭证索引，建议从客户确认函或 2026-01 样箱测试签收/反馈原件开始；继续保持 GFIS/GPCF `repair_required`，直到 verified live artifact 与完整运行层 SOP E2E 主门禁通过。
