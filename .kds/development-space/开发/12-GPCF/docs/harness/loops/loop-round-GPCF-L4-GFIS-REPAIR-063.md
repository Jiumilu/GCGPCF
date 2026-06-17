---
doc_id: GPCF-DOC-ABC368E7DF
title: GPCF-L4-GFIS-REPAIR-063 GFIS 辽宁远航 verified artifact intake 前置校验
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-063.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-063.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-063 GFIS 辽宁远航 verified artifact intake 前置校验

## Objective

按 Loop 新真实性规则继续 GFIS 运行层修复。本轮只做 1 个真实实质轮次：把 GFIS 辽宁远航 4 项原始凭证采集清单推进为机器可校验的 verified artifact intake 前置校验，防止报价 PDF、KDS 候选、会议纪要、计划文字或用户口述被误计为 `verified_live_artifact`。

## Input

- 用户补充业务链路：2026 年 1 月辽宁远航 23 个样箱测试、江西委托工厂生产、2026 年 5 月项目报价、2026 年 6 月现代精工产线量产计划。
- GFIS 真实仓 `AGENTS.md`：GFIS 运行层为 SOP 主体，Demo 不可替代运行层验收。
- GFIS 上轮清单：`liaoning-yuanhang-original-proof-collection-checklist.json` 中 4 项均为 `original_proof_collection_open`，`verified_proof_item_count=0`。

## Real Change

- GFIS 新增 `scripts/build_gfis_verified_artifact_intake_precheck.py`。
- GFIS 新增 `scripts/validate_gfis_verified_artifact_intake_precheck.py`。
- GFIS 生成 `docs/harness/sop-e2e/evidence/liaoning-yuanhang-verified-artifact-intake-precheck.json`。
- GFIS 生成 `docs/harness/sop-e2e/liaoning-yuanhang-verified-artifact-intake-precheck.md`。
- GFIS 更新 loop-state、loops README、evidence-index 和 SOP evidence map。
- GPCF 更新 loop-state、状态矩阵、控制板、evidence index 和 loop record。

## Precheck Result

| proof item | ready_for_runtime_intake | required before intake |
|---|---:|---|
| 辽宁远航 23 个样箱测试签收或测试反馈 | false | `source_record_uri`、`source_record_hash`、`kds_backlink_path`、测试记录编号、测试签收附件、客户反馈原件、客户签收单号 |
| 江西委托工厂样箱生产记录 | false | `source_record_uri`、`source_record_hash`、`kds_backlink_path`、委托生产单号、完工记录编号、生产批次号、代工签收附件 |
| 2026-05 辽宁远航项目报价单 | false | `source_record_uri`、`source_record_hash`、`kds_backlink_path`、客户确认函 |
| 2026-06 现代精工产线量产计划或转量产批准 | false | `source_record_uri`、`source_record_hash`、`kds_backlink_path`、转量产批准单号、放行批准附件、量产计划编号、WAES evidence ref |

## Evidence

| Check | Result |
|---|---|
| GFIS intake precheck builder | pass；`slots=4 ready=0 blocked=4 runtime_sop_e2e=repair_required` |
| GFIS intake precheck validator | pass；`slots=4 ready=0 blocked=4 runtime_sop_e2e=repair_required` |
| GFIS original checklist validator | pass；`items=4 open=4 verified=0 runtime_sop_e2e=repair_required` |
| GFIS API contract validator | pass；`created_docs=19 commits=19` |
| GFIS KDS scanner | pass；`categories=8/8 missing_live_business_inputs=5` |
| GFIS runtime runner | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS runtime SOP validator | expected exit 2；`runtime_sop_e2e=repair_required`、`runtime_sop_e2e_master=failed_or_repair_required` |
| GFIS Demo E2E regression | pass；26 passed；仅 `pass_demo_only` |
| GFIS diff hygiene | pass |

## Boundary

- 未执行 Git push、生产写入、真实外部 API 写入、数据库迁移、`bench migrate`、schema sync、权限变更、部署或 accepted/integrated 状态升级。
- 未把用户业务线索、KDS 候选、会议纪要、报价 PDF、量产计划文字或治理文档升级为正式 live proof。
- 未把 Demo E2E 通过当作 GFIS 运行层 SOP E2E 通过。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## Next

下一轮可生成可填报 intake packet 模板或真实原始凭证接收目录；业务方补齐四项原始凭证后，GFIS 才允许进入 runtime intake gate 复验。当前继续保持 `runtime_sop_e2e=repair_required`。
