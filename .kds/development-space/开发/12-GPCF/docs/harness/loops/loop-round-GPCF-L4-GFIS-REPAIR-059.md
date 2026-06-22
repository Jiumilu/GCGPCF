---
doc_id: GPCF-DOC-50628558F3
title: GPCF-L4-GFIS-REPAIR-059 GFIS KDS 弱凭证与客户确认误判防护
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-059.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-059.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-059 GFIS KDS 弱凭证与客户确认误判防护

## Objective

按 Loop 新真实性规则继续 GFIS 运行层修复。本轮只做 1 个真实实质轮次：结合用户补充的辽宁远航样箱、江西委托、5 月报价、6 月现代精工量产计划线索，检索 KDS 并修复 GFIS 把弱业务线索误判成正式客户确认的风险。

## Real Change

- GFIS scanner 新增 KDS canonical read-only 来源：陈启光沟通纪要、潜在订单需求、辽宁远航产能适应性分析、绿色循环包装箱行动台账、报价外发报备、报价书和现代精工预运营/委托加工资料。
- GFIS scanner 新增 `weak_acknowledgement_refs`，将价格口头认可、微信发送报价、待陈启光确认、采购单位确认、需求清单、现代精工量产安排归类为弱业务凭证。
- GFIS scanner 移除正式 `客户确认函` 别名中的 `陈启光确认`，避免 `待陈启光确认` 被误判成客户确认函。
- GFIS runtime collection package 新增 `weak_acknowledgement_candidate_count`、`weak_acknowledgement_refs`、`weak_acknowledgement_policy`。
- GFIS validator 新增断言：弱凭证不能满足正式客户确认，报价项仍必须 `missing_fields=["客户确认函"]`。

## Evidence

| Check | Result |
|---|---|
| GFIS `git status --short --branch` | dirty；延续既有 GFIS repair 工作区，未回退用户/既有变更 |
| GFIS `py_compile` | pass |
| GFIS `harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=1` |
| GFIS quotation field gap probe | best missing `["客户确认函"]`；weak acknowledgement count 21 |
| GFIS `validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS local runtime reload | `bench --site frontend clear-cache` + `docker compose ... restart backend frontend` pass；无 migrate/schema sync |
| GFIS `run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS `validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_liaoning_yuanhang_proof_collection_package=liaoning_yuanhang_original_proof_collection_open` |
| GFIS `npm run test:e2e` | pass；26 passed；Demo only / `pass_demo_only` |
| GFIS `git diff --check -- .` | pass |

## Current State

GFIS SOP E2E 仍是 `repair_required`。本轮证明 Loop 能从 KDS 中发现弱业务线索，并自我修复“待确认语句误判为正式客户确认”的风险；未证明客户确认函、样箱测试签收、江西委托生产记录、现代精工转量产批准或完整 SOP E2E 完成。

## Boundaries

本轮未执行 Git push、生产写入、真实外部 API 写入、`bench migrate`、schema sync、数据库迁移、权限/Token/生产配置变更或 accepted/integrated 状态升级。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |
