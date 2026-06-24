---
doc_id: GPCF-DOC-259A611CFF
title: GPCF-L4-GFIS-REPAIR-061 GFIS KDS candidate expansion truth guard
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-061.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-061.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-061 GFIS KDS candidate expansion truth guard

## Objective

按 Loop 新真实性规则继续 GFIS 运行层修复。本轮只做 1 个真实实质轮次：响应用户“5 类真实凭证缺口可通过检索 KDS 获取”的判断，把辽宁远航、江西委托生产、现代精工 6 月量产计划相关 KDS 真源纳入 GFIS 检索，同时确保 KDS 候选只用于缩小采集范围，不得冒充 `verified_live_artifact`。

## Input

- 用户补充：2026 年 1 月向辽宁远航提供 23 个样箱测试，样箱由江西工厂受托生产；5 月辽宁远航计划采购并提交项目报价单；6 月计划用现代精工产线组织量产。
- 用户指出：5 类真实凭证缺口可通过检索 KDS 获取。
- GFIS 真实仓 `AGENTS.md`：GFIS 运行层为 SOP 主体，Demo 不可替代运行层验收。
- GFIS 当前验证事实：`missing_live_business_inputs=5`、`runtime_sop_e2e=repair_required`。

## Real Change

- GFIS `scripts/harvest_gfis_kds_gehu_inputs.py` 扩展 KDS canonical read-only 检索源，新增辽宁远航沟通纪要、canonical 报价单、报价历史、现代精工 6 月生产纪要、葛化预运营和现代精工相关会议材料。
- GFIS `FORMAL_MISSING_REASON_REFS` 增加 KDS 真实来源解释，分别对应样箱测试、江西委托生产、项目报价、现代精工量产放行。
- GFIS `scripts/run_gfis_runtime_sop_e2e_dry_run.py` 和 `scripts/validate_gfis_runtime_sop_e2e.py` 修正旧语义：`ready_category_count` 与 `collected_artifact_count` 只统计 verified live artifact intake，不统计 KDS candidate source。
- GFIS 新增 `GFIS-RUNTIME-SOP-E2E-054` 轮次记录，并更新 GFIS loop-state、loops README、evidence-index 和 SOP evidence map。

## KDS Search Result

| proof item | candidate_count | best candidate | remaining missing anchors |
|---|---:|---|---|
| 辽宁远航 23 个样箱测试签收或测试反馈 | 54 | `canonical-kds-readonly/PVA价值联盟/项目文件/辽宁远航国际物流/01_行动台账.md` | 测试记录编号、测试签收附件、客户反馈原件、客户签收单号 |
| 江西委托工厂样箱生产记录 | 8 | `canonical-kds-readonly/wiki/sources/_llmwiki_canonical/工业绿链/项目/葛化/葛化五项P0执行方案_20260521.md` | 委托生产单号、完工记录编号、生产批次号、代工签收附件 |
| 2026-05 辽宁远航项目报价单 | 47 | `canonical-kds-readonly/PVA价值联盟/项目文件/辽宁远航国际物流/报价/宝马循环周转箱_正式报价书_IGL-BMW-QT-20260520-001.pdf` | 客户确认函 |
| 2026-06 现代精工产线量产计划或转量产批准 | 57 | `canonical-kds-readonly/wiki/sources/_llmwiki_canonical/工业绿链/项目/葛化/葛化物流确认清单及预运营pmo执行方案260521V2.md` | 转量产批准单号、放行批准附件、量产计划编号、WAES evidence ref |

## Evidence

| Check | Result |
|---|---|
| GFIS `python3 -m py_compile ...` | pass |
| GFIS `python3 scripts/harvest_gfis_kds_gehu_inputs.py` | pass；`categories=8/8 missing_live_business_inputs=5` |
| GFIS proof search probe | 4 项 proof items 均为 `candidate_found_not_verified` |
| GFIS `python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=19 commits=19` |
| GFIS `python3 scripts/run_gfis_runtime_sop_e2e_dry_run.py` | partial；`runtime_calls=47 created=19 cleanup_deleted=19 runtime_gaps=34` |
| GFIS `python3 scripts/validate_gfis_runtime_sop_e2e.py` | expected exit 2；`runtime_sop_e2e=repair_required`、`missing_inputs=5` |

## Boundary

- 未执行 Git push、生产写入、真实外部 API 写入、数据库迁移、`bench migrate`、schema sync、权限变更、部署或 accepted/integrated 状态升级。
- 未把用户业务线索、KDS 会议纪要、报价历史、报价 PDF、计划材料、弱确认或内部治理文档升级为正式 live proof。

## Truth Counts

| Metric | Value |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## Next

下一轮应把 GFIS `LiaoningYuanhangProofCollectionPackage` 的 4 项开放请求转为业务方可执行的原始凭证采集清单，要求每项必须提供正式编号、附件、`source_record_uri`、`source_record_hash`、`kds_backlink_path` 和对应 WAES/GPC/GFIS 确认锚点。
