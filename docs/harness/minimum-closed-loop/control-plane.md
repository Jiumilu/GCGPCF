---
doc_id: GPCF-L4-MCL-CONTROL-PLANE
title: L4 Minimum Closed Loop Control Plane
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/minimum-closed-loop/control-plane.md
source_path: docs/harness/minimum-closed-loop/control-plane.md
sync_direction: bidirectional
last_reviewed: 2026-06-13
supersedes: []
superseded_by: []
---

# L4 Minimum Closed Loop Control Plane

## Round

| 字段 | 值 |
|---|---|
| round_id | GPCF-L4-001 |
| loop_mode | L4 minimum closed loop implementation |
| status | partial |
| gate | L4_ready_candidate |
| business_chain | 项目初始化 -> 组织/伙伴接入 -> 平台订单 -> 报价/订单评审/合同 -> 配方研发 -> 样品打样/样箱打样 -> 客户签样确认 -> 转量产门禁 -> 工厂订单 -> 工单 -> 质量/库存/批次 -> 发货 -> 签收 -> 异常 -> WAES 状态/证据 -> 日报/复盘 -> KDS 知识沉淀 -> GPCF 项目群收口 -> 下一轮 Loop |

## Control Principles

| 原则 | 控制要求 | 验证方式 |
|---|---|---|
| 样品确认独立阶段 | 样品确认位于平台订单与工厂订单之间 | `validate_l4_minimum_closed_loop.py` 检查业务链顺序 |
| 禁止绕过门禁 | 未完成客户签样、豁免或转量产门禁，不得进入工厂订单 | 对象契约必须包含 blocking rule |
| 12 项目不缺席 | 成熟项目真实运行，低成熟项目以契约、mock、dry-run 或占位验证参与 | 职责矩阵必须覆盖 12 项目 |
| GPC/GFIS 边界 | GPC 管客户签样和转量产，GFIS 管配方研发、样品打样、检测事实 | 对象契约检查 owner/producer/consumer |
| WAES 确证 | 样品签样、转量产、异常和审计动作进入 WAES evidence 门禁 | evidence 总入口必须登记 WAES 验证 |
| KDS 沉淀 | 样品规格、签样资料、SOP、复盘案例和 evidence 回指进入 KDS | evidence 总入口必须登记 KDS 路径 |
| UI 四节点一致 | 平台订单、样品确认、签收、异常状态区、证据区、风险确认一致 | L4 后续 UI smoke 或静态检查 |

## Stage Activation

| 项目 | 激活深度 | L4-001 参与方式 |
|---|---|---|
| GFIS | real/dry-run | 工厂事实与样品执行契约，后续 L4-008 落真实样本 |
| GPC | contract/dry-run | 平台订单、样品申请、签样、转量产契约，后续 L4-007 落真实仓 |
| PVAOS | contract/dry-run | 租户、组织、伙伴、项目空间和权限输入基线 |
| WAES | contract/dry-run | 样品签样、转量产、异常和审计 evidence 门禁 |
| KDS | contract/dry-run | 样品规格、签样资料、SOP、案例和 evidence 回指 |
| Brain | smoke/dry-run | SOP、案例、样品资料检索 smoke |
| PKC | mock | 样品任务、签样提醒、状态通知 mock |
| MMC | real/config | 治理模板、配置字段和样品确认策略边界 |
| XiaoC | dry-run | 样品链路任务拆解和模型路由 |
| XGD | dry-run | 转量产风险、产能影响和异常根因分析 |
| XiaoG | mock/dry-run | 样品/工单只读查询和 WAES 审计写入 mock |
| GPCF | real/governance | 控制面、评分矩阵、evidence 总入口和下一轮计划 |

## Quality Gates

| Gate | 必须满足 | 当前证据 |
|---|---|---|
| L3 baseline | 11 个业务项目 L3 Ready，GPCF governance_hub | `docs/harness/evidence/l3_admission_assessment.json` |
| Role matrix | 12 项目职责、输入、输出、验证、evidence 均存在 | `project-role-verification-matrix.md` |
| Object contracts | 核心对象有 producer、consumer、input、output、forbidden_actions、verification | `object-contracts.md` |
| Sample gate | 平台订单不得直接进入工厂订单 | `object-contracts.md` and validator |
| Evidence chain | 项目级 evidence 与项目群 evidence 双层入口存在 | `evidence-index.md` |

## Stop Boundaries

- 不执行生产写入。
- 不执行真实外部 API 写入。
- 不执行数据库迁移。
- 不执行权限变更。
- 不执行部署。
- 不读取或写入真实 TOKEN。
- 不升级 accepted 或 integrated。

