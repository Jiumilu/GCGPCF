---
doc_id: GPCF-DOC-B4D3E41E0F
title: GPCF-L4-GFIS-REPAIR-090 GFIS Targeted KDS Decision Package
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-090.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-090.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-090 GFIS Targeted KDS Decision Package

## 轮次元数据

| 字段 | 值 |
|---|---|
| round_id | GPCF-L4-GFIS-REPAIR-090 |
| date | 2026-06-15 |
| project | GPCF |
| subject | GFIS运行层 |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 8 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 输入

- GFIS `GFIS-RUNTIME-SOP-E2E-082` 已生成辽宁远航 targeted KDS search 结果。
- 用户补充事实：2026 年 1 月向辽宁远航提供 23 个样箱测试，样箱委托江西工厂生产；2026 年 5 月辽宁远航计划采购并提交项目报价单；2026 年 6 月计划用现代精工产线组织量产。
- 当前四类 proof item 均仍缺正式原始凭证和 proof anchors。

## 执行动作

- GFIS 新增 targeted KDS decision package JSON/Markdown、builder、validator。
- GFIS 新增 `get_runtime_liaoning_yuanhang_targeted_kds_decision_package` 只读 API 契约。
- GFIS 主 runtime SOP validator 接入 decision package validator。
- GPCF 回写 loop-state、evidence index、status matrix、control board 和本轮 loop record。

## 输出

- `liaoning_yuanhang_targeted_kds_decision_package=pass decisions=4 runtime_ready=0 review_ready=0 verified=0 runtime_sop_e2e=repair_required`
- `runtime_liaoning_yuanhang_targeted_kds_decision_package=pass:decisions=4:runtime_ready=0:review_ready=0:verified=0`
- `gfis_runtime_sop_e2e=repair_required`
- `runtime_verified_artifact_submission=missing_verified_artifact_submission`

## 验证

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_gfis_liaoning_yuanhang_targeted_kds_decision_package.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_liaoning_yuanhang_targeted_kds_decision_package.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py
```

`validate_gfis_runtime_sop_e2e.py` 预期 exit 2，代表完整 SOP E2E 仍为 `repair_required`。

## 边界

- 本轮只证明补证分派判断可机器校验。
- KDS 候选、报价 PDF、行动台账、沟通纪要和用户口述均不能替代正式原始凭证。
- 不生产写入、不真实外部 API 写入、不 bench migrate、不 schema sync、不真实 KDS/WAES 写入、不部署、不推送、不升级 accepted/integrated。

## 下一轮

`GFIS-RUNTIME-SOP-E2E-084`：将 decision package 转成逐项正式原始凭证采集 handoff/checklist，继续保持 candidate-only。
