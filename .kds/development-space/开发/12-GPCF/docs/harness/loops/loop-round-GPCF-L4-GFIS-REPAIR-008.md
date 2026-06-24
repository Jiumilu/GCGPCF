---
doc_id: GPCF-DOC-647E394AF0
title: GPCF-L4-GFIS-REPAIR-008 GFIS KDS Gehua Controlled Data Coverage
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-008.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-008 GFIS KDS Gehua Controlled Data Coverage

## 触发来源

长期目标要求 GFIS 运行层必须基于 KDS 中葛化项目相关全部受控数据运行 SOP E2E。上一轮已经证明运行层 evidence candidate 源码契约可用，但“使用 KDS 数据”仍主要由人工输入台账表达。本轮将其推进为机器扫描 evidence。

## 本轮目标

在不生产写入、不真实外部 API、不迁移、不重启、不升级 accepted/integrated 的边界内，新增 GFIS 侧 KDS coverage scanner，证明当前本地 KDS `开发` 空间镜像对葛化 SOP 预检资料的覆盖范围，同时继续保留真实业务凭证缺口。

## 实施内容

| 文件 | 动作 |
|---|---|
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/harvest_gfis_kds_gehu_inputs.py` | 新增 KDS 葛化受控资料扫描器 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/evidence/kds-gehu-controlled-data-coverage.json` | 生成 17 个受控来源、8/8 覆盖分类、5 项真实业务凭证缺口 |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py` | 纳入 coverage evidence 并输出 `kds_controlled_coverage=available missing_live_business_inputs=5` |
| `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/**` | 回写 scanner 命令、覆盖结果和 evidence map |
| `tools/kds-sync/validate_loop_engineering_integrity.py` | 要求 GFIS runtime validator 输出 KDS coverage 信号 |

## 验证结果

| 命令 | 结果 |
|---|---|
| `git status --short --branch` in GFIS | dirty；保护已有工作，仅做最小增量 |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/harvest_gfis_kds_gehu_inputs.py` | `kds_gehu_controlled_data_coverage=available categories=8/8 missing_live_business_inputs=5` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | `repair_required`; `kds_controlled_coverage=available missing_live_business_inputs=5` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` | pass；`created_docs=7 commits=7` |

## 真实性边界

- KDS 受控资料覆盖不等于真实业务完成。
- 真实订单、签样、原料批次、运行态主键、POD、WAES confirmation、KDS write receipt 仍为 `missing_live_business_inputs=5`。
- 未使用 GFIS Demo 作为业务主体。
- 未执行生产写入、真实外部 API 写入、`bench migrate`、schema sync、数据库迁移、权限变更、部署或 accepted/integrated 升级。

## 计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | missing_live_business_inputs |

## 下一轮建议

下一轮应优先取得用户对 GFIS 本机运行层受控重载复测的明确授权，或补齐至少一类真实葛化业务凭证后重新运行 scanner 与 runtime SOP validator。
