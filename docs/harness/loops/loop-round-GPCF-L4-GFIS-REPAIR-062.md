---
doc_id: GPCF-DOC-FF36CE622C
title: GPCF-L4-GFIS-REPAIR-062 GFIS 辽宁远航原始凭证采集清单
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-062.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-062.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-062 GFIS 辽宁远航原始凭证采集清单

## Objective

按 Loop 新真实性规则继续 GFIS 运行层修复。本轮只做 1 个真实实质轮次：把用户补充的辽宁远航样箱、江西委托生产、5 月报价和 6 月现代精工量产计划线索转成业务方可执行的 4 项原始凭证采集清单，并继续防止 KDS 候选、报价 PDF、计划文字或用户口述线索冒充 `verified_live_artifact`。

## Input

- 用户补充：今年 1 月向辽宁远航提供 23 个样箱测试，样箱委托江西一家工厂生产；5 月辽宁远航计划采购并提交项目报价单；6 月计划用现代精工产线组织量产。
- GFIS 真实仓 `AGENTS.md`：GFIS 运行层为 SOP 主体，Demo 不可替代运行层验收。
- GFIS 当前 evidence：`runtime_liaoning_yuanhang_proof_collection_package=liaoning_yuanhang_original_proof_collection_open`、`missing_live_business_inputs=5`、`runtime_sop_e2e=repair_required`。

## Real Change

- GFIS 新增 `scripts/build_gfis_liaoning_yuanhang_proof_collection_checklist.py`。
- GFIS 新增 `scripts/validate_gfis_liaoning_yuanhang_proof_collection_checklist.py`。
- GFIS 生成 `docs/harness/sop-e2e/evidence/liaoning-yuanhang-original-proof-collection-checklist.json`。
- GFIS 生成 `docs/harness/sop-e2e/liaoning-yuanhang-original-proof-collection-checklist.md`。
- GFIS 更新 loop-state、loops README、evidence-index 和 SOP evidence map。
- GPCF 更新 loop-state、状态矩阵和控制板。

## Checklist Result

| proof item | owner | candidate_count | still missing |
|---|---|---:|---|
| 辽宁远航 23 个样箱测试签收或测试反馈 | GPC | 54 | 测试记录编号、测试签收附件、客户反馈原件、客户签收单号 |
| 江西委托工厂样箱生产记录 | GFIS | 8 | 委托生产单号、完工记录编号、生产批次号、代工签收附件 |
| 2026-05 辽宁远航项目报价单 | GPC | 47 | 客户确认函 |
| 2026-06 现代精工产线量产计划或转量产批准 | WAES | 57 | 转量产批准单号、放行批准附件、量产计划编号、WAES evidence ref |

## Evidence

| Check | Result |
|---|---|
| GFIS checklist builder | pass；`items=4 open=4 verified=0 runtime_sop_e2e=repair_required` |
| GFIS checklist validator | pass；`items=4 open=4 verified=0 runtime_sop_e2e=repair_required` |
| GFIS KDS scanner | pass；`categories=8/8 missing_live_business_inputs=5` |
| GFIS runtime runner | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS runtime SOP validator | expected exit 2；`runtime_sop_e2e=repair_required`、`runtime_sop_e2e_master=failed_or_repair_required` |
| GFIS diff hygiene | pass |

## Boundary

- 未执行 Git push、生产写入、真实外部 API 写入、数据库迁移、`bench migrate`、schema sync、权限变更、部署或 accepted/integrated 状态升级。
- 未把用户业务线索、KDS 候选、会议纪要、报价 PDF、量产计划文字或治理文档升级为正式 live proof。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## Next

下一轮应建立 verified artifact intake 填报样例和导入前置校验：4 项原始凭证进入 GFIS 前必须具备 `source_record_uri`、`source_record_hash`、`kds_backlink_path` 和对应正式编号/附件；继续保持 `runtime_sop_e2e=repair_required`，直到真实凭证进入 verified live artifact intake。
