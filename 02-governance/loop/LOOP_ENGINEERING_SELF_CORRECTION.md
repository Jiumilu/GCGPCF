---
doc_id: GPCF-DOC-744D083B96
title: LOOP_ENGINEERING_SELF_CORRECTION
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_ENGINEERING_SELF_CORRECTION.md
source_path: 02-governance/loop/LOOP_ENGINEERING_SELF_CORRECTION.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP_ENGINEERING_SELF_CORRECTION

## 关键问题重述

本文件记录 GFIS 主体错位后的 Loop 重新总结。此前曾把 `GFIS Demo` 的展示层、培训层、前端回归层结果误用于判断运行层 SOP，造成对错误主体进行开发和验收判断。正确主体必须是 `GFIS 运行层`，`GFIS Demo` 不能用于 SOP 主体证明、业务证据证明、source-of-record 证明、runtime primary key 证明、WAES review 证明或 accepted/integrated 状态证明。

本次属于 `P0 级 Loop 事故`。事故复盘结论是：`subject_drift_detected`，且 `sop_e2e_master=failed_or_repair_required`。所有后续 Loop Engineering 必须把 `pass_demo_only`、`controlled_reference_not_live_proof`、`verified live artifact` 分层处理。

## 二次复盘结论

二次复盘结论：GFIS 当前承载现代精工 OEM 代加工生产期间的运行时系统，葛化自建工厂投产后继续使用同一 GFIS 运行层；GFIS Demo 只能作为展示、培训和前端回归，不能替代 GFIS 运行层事实。

SOP Master 结论公式：

```text
SOP E2E Master 门禁 = GFIS 运行层事实 + 真实 source-of-record + runtime primary key + review/runtime/WAES/KDS evidence
GFIS Demo E2E = pass_demo_only
gfis_runtime_sop_e2e=repair_required
```

当前 `runtime_sop_chain_gate=blocked`，`work_order_runtime=runtime_api_passed_temp_created_cleanup_required`。因此不得升级业务状态。

## Loop Engineering 定义

Loop Engineering 重定义 v2：

- 主体先行：先确认 `GFIS 运行层`，再确认接口、证据和文档。
- 失败先行：E2E 测试大师失败或 `repair_required` 必须先进入复盘和修复链路。
- 证据分层：请求包、KDS 候选、用户口述、Loop 文档、GFIS Demo、controlled reference 都不是 live proof。
- 最小实质修复：每轮只落地一个可验证的最小闭环。
- 机器门禁：所有状态必须由 validator 或等价检查留证。
- 审计回放：所有关键动作必须能从文档、证据和 Git diff 回放。
- 防复发学习：每次主体错位或证据污染都必须进入防复发工程门禁。

## 自我发现失败根因

- 自我发现没有优先识别 GFIS Demo 与 GFIS 运行层的主体差异。
- 自我发现没有把 E2E 测试大师失败提升为 `P0 级 Loop 事故`。
- 自我发现没有把 `pass_demo_only` 与 `gfis_runtime_sop_e2e=repair_required` 同时写入状态天花板。
- 自我发现没有持续要求 `verified live artifact` 的 proof anchors。

## 自我发现闭环

自我发现与解决机制包含五步：

1. 自我发现：检测 subject drift、E2E failure、weak proof、status inflation。
2. 自我降级：将错误完成态降级为 `repair_required`。
3. 自我拆解：把缺口拆成 source-of-record、runtime primary key、review queue、runtime intake、WAES review、KDS write receipt。
4. 自我修复：只做一个最小实质修复，并运行 validator。
5. 自我防复发：把规则纳入防复发工程门禁和 Loop Engineering 操作模型。

## 自我发现触发器

- `subject_drift_detected`
- `sop_e2e_master=failed_or_repair_required`
- `gfis_runtime_sop_e2e=repair_required`
- `runtime_sop_chain_gate=blocked`
- E2E 测试大师失败
- GFIS Demo 被用于替代运行层事实
- controlled_reference_not_live_proof 被误判为 live proof
- 缺少 `source_record_uri`、`source_record_hash`、`verification_actor`、`verification_method`

## 解决问题路线

问题到门禁映射：

| 问题 | 门禁 |
|---|---|
| GFIS Demo 主体错位 | 主体权威门禁 |
| E2E 测试大师失败 | 失败优先门禁 |
| weak verified artifact | SOP E2E Master 门禁 |
| 缺 source-of-record | runtime source record gate |
| 缺 runtime primary key | runtime intake gate |
| 缺 WAES confirmation | WAES review gate |

下一轮工程方向继续聚焦 GFIS runtime verified artifact collection、GFIS runtime verified artifact collection dossier、采集案卷、proof anchors、open/collected 计数和全类别 ready 判定。

## 防复发工程门禁

- 主体权威门禁：所有 GFIS SOP 判断必须引用 GFIS 运行层。
- 失败优先门禁：`repair_required` 优先于展示层 pass。
- SOP E2E Master 门禁：必须同时验证 sample_request、production_release_gate、raw_material_plan、quality_inspection、delivery_note、proof_of_delivery。
- proof anchors 门禁：必须有 `source_record_uri`、`source_record_hash`、`verification_actor`、`verification_method`。
- weak proof 拒收：`weak verified artifact`、GFIS Demo、KDS 候选、用户口述、Loop 文档都不能直接转为 verified live artifact。

## Loop Engineering 操作模型

Loop Engineering 操作模型按事实层、工程层、治理层运行：

- 事实层：客户订单、平台订单、样箱测试、合同、生产、质检、库存、发货、POD、WAES confirmation、KDS write receipt。
- 工程层：GFIS runtime API、validator、builder、只读 dry-run、evidence JSON/Markdown。
- 治理层：GPCF 控制板、状态矩阵、loop-state、evidence-index、KDS 本地镜像和防污染检查。

当前高质量可用判定仍是 `repair_required`，不是 accepted/integrated。

## 当前机器事实

```text
declared_rounds=1/15
substantive_rounds=1/15
generated_items=7
batch_generated=false
substance_gate=pass
stop_type=authorization_boundary
gfis_runtime_sop_e2e=repair_required
work_order_runtime=runtime_api_passed_temp_created_cleanup_required
runtime_sop_chain_gate=blocked
project_group_score=78
pass_demo_only
controlled_reference_not_live_proof
```

本文件不创建 source-of-record、runtime primary key、review queue、runtime intake、WAES review、verified artifact、accepted 或 integrated 状态。
