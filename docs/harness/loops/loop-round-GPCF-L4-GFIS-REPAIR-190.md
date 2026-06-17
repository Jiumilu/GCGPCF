---
doc_id: GPCF-DOC-53A5418CDB
title: GPCF-L4-GFIS-REPAIR-190
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-190.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-190.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-190

## 输入

- GFIS `GFIS-RUNTIME-SOP-E2E-183`。
- 上一轮 `CustomerRequirementOrPlatformOrder` source-of-record 接收扫描仍为 `valid_source_records=0`。
- 用户要求 GFIS 运行层为唯一 SOP 实现主体，GFIS Demo 不得作为业务证据。

## 动作

- 在 GFIS 真实项目仓新增 `CustomerRequirementOrPlatformOrder` source-of-record 负例拒收门禁。
- 回写 GPCF 控制板、loop-state、状态矩阵、L4 评分矩阵和 evidence index。
- 保持 `repair_required`，不升级 accepted/integrated。

## 输出

- GFIS negative fixture guard：`negative_fixture_count=6 rejected_fixture_count=6 accepted_fixture_count=0`。
- GFIS 主 validator：expected exit 2，继续 `gfis_runtime_sop_e2e=repair_required`。
- GFIS Demo E2E：26 passed，但仅为 `pass_demo_only`。

## 非声明

- 不创建客户订单、平台订单或运行层主键。
- 不创建 FactoryOrder、WorkOrder、DeliveryNote、POD 或金融事实。
- 不写生产数据库、KDS、WAES 或外部 API。
- 不执行 `bench migrate`、schema sync、权限变更或部署。
- 不标记 accepted/integrated。

## 轮次计数

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 16 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 下一轮

`GFIS-RUNTIME-SOP-E2E-184`：继续围绕 `CustomerRequirementOrPlatformOrder` 建立真实源记录结构就绪扫描或接收后隔离门禁。真实 source-of-record 未到达前，继续保持 `review_queue=0`、`runtime_intake=0`、`waes_review=0`、`verified=0`。
