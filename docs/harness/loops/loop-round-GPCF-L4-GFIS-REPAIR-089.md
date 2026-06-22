---
doc_id: GPCF-DOC-70E72EA863
title: GPCF-L4-GFIS-REPAIR-089 GFIS Targeted KDS Search Candidate Gate
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-089.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-089.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-089 GFIS Targeted KDS Search Candidate Gate

## 轮次元数据

| 字段 | 值 |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-089 |
| gfis_round_id | GFIS-RUNTIME-SOP-E2E-082 |
| date | 2026-06-14 |
| project | GPCF |
| subject | GFIS运行层 |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 输入

- 用户指出 5 类真实凭证缺口可通过检索 KDS 获取。
- GFIS 上轮已把辽宁远航 2026-01 样箱测试、江西委托生产、2026-05 报价、2026-06 现代精工量产计划转成业务事实链索引。
- 本轮要求只做一个真实实质轮次，不允许批量文档冒充多轮进展。

## 执行动作

- GFIS 新增 targeted KDS search builder、JSON/Markdown 结果和 validator。
- GFIS 主 runtime SOP validator 接入 targeted KDS search validator。
- GFIS 项目仓更新 sop-e2e README、loop-state、evidence index、loops README 和 `GFIS-RUNTIME-SOP-E2E-082` 轮次记录。
- GPCF 总控更新 loop-state、evidence index、状态矩阵、控制板和本轮记录。

## 输出

- `liaoning_yuanhang_targeted_kds_search=pass items=4 ready=0 verified=0 runtime_sop_e2e=repair_required`
- `runtime_liaoning_yuanhang_targeted_kds_search=pass:items=4:ready=0:verified=0`
- GFIS 主 validator 预期仍为 exit 2：`gfis_runtime_sop_e2e=repair_required`
- GFIS Demo E2E：`26 passed`，只登记为 `pass_demo_only`

## 边界

- KDS targeted search 只证明候选可定位和可追溯，不证明正式原始凭证已收集或验真。
- 报价 PDF 可以作为报价附件候选，但缺客户确认函时不得证明客户已确认采购。
- 行动台账、沟通纪要、现代精工/葛化材料只作为上下文和候选路径，不得替代样箱测试记录、江西委托生产记录或转量产放行。
- 本轮未执行 Git push、生产写入、真实外部 API 写入、真实 KDS/WAES 写入、数据库迁移、权限变更、部署或 accepted/integrated 状态升级。

## 验证

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_liaoning_yuanhang_targeted_kds_search.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py
npm run test:e2e
git diff --check -- .
```

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/document_control.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/check_document_pollution.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/validate_kds_token.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/loop_document_gate.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/validate_loop_engineering_integrity.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/kds-sync/validate_continuous_round_substance.py
git diff --check -- .
```

## 下一轮

`GFIS-RUNTIME-SOP-E2E-083`：将 targeted search 结果转成 GFIS 运行层只读 decision package 或人工补证分派包，明确每个候选的提交条件、拒绝原因和所需原始附件。
