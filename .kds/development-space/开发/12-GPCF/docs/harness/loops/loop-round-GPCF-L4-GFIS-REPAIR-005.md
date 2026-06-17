---
doc_id: GPCF-DOC-803F0F9555
title: GPCF-L4-GFIS-REPAIR-005 GFIS Runtime KDS Source Mirror Repair
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-005.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-005.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-005 GFIS Runtime KDS Source Mirror Repair

## Trigger

上一轮 GFIS 运行层 SOP validator 输出：

```text
gfis_runtime_sop_e2e=repair_required
missing_inputs=5 missing_kds_source_paths=4
```

其中 `missing_kds_source_paths=4` 是可自动闭合的治理缺口：真实 GFIS 仓存在 4 份运行层受控文档，但 KDS `开发/01-GFIS/docs/*` 本地镜像缺失。

## Scope

| 项 | 说明 |
|---|---|
| 本轮目标 | 补齐 KDS 开发空间本地镜像中的 4 份 GFIS 运行层文档源 |
| 正确主体 | GFIS 运行层 |
| 非目标 | 不伪造真实订单、签样、原料批次、作业卡、质检、库存、发货、POD、WAES/KDS 回执；不执行生产写入、真实外部 API、数据库迁移、权限变更、服务重启、推送或 accepted/integrated 升级 |

## Changes

| 路径 | 变更 |
|---|---|
| `.kds/development-space/开发/01-GFIS/docs/07-p0-sop-to-erpnext-doctype-mapping.md` | 从真实 GFIS 仓镜像并增加受控 front matter |
| `.kds/development-space/开发/01-GFIS/docs/17-gcfis-functional-specification.md` | 从真实 GFIS 仓镜像并增加受控 front matter |
| `.kds/development-space/开发/01-GFIS/docs/20-gcfis-core-flow-closure-matrix.md` | 从真实 GFIS 仓镜像并增加受控 front matter |
| `.kds/development-space/开发/01-GFIS/docs/21-gcfis-risk-ledger-and-uat-plan.md` | 从真实 GFIS 仓镜像并增加受控 front matter |
| `.kds/development-space/开发/01-GFIS/README.md` | 增加 4 份文档索引 |
| GFIS `docs/harness/sop-e2e/*` | 更新 KDS source path 缺口已清零的事实 |
| GPCF 总控文档 | 更新 loop-state、控制板、状态矩阵、L4 评分矩阵和 evidence index |

## Evidence

| 类型 | 命令或路径 | 结论 |
|---|---|---|
| GFIS runtime SOP validator | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` in GFIS | `repair_required`; `missing_inputs=5`; `missing_kds_source_paths=0` |
| GPCF diff hygiene | `git diff --check -- .` | pass |

## Findings

| 发现 | 判断 |
|---|---|
| KDS source path 缺口 | 已从 4 降为 0 |
| 真实业务输入缺口 | 仍为 5，必须保持 `missing_input` |
| GFIS runtime SOP E2E | 仍为 `repair_required` |
| 项目群评分 | 从 78/100 小幅校准到 79/100；仍不得恢复 100/100 |

## Round Accounting

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 7 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | missing_input_and_runtime_retest_required |

## Next Input

下一轮应选择一个真实业务输入或运行态复测目标：补齐客户订单、样品申请/客户签样、转量产批准、原料批次、作业卡、POD、WAES/KDS 回执中的至少一类；或在授权边界内受控重载 GFIS 运行服务并复测 WorkOrder API。
