---
doc_id: GPCF-DOC-WAS-XWAIL-AAAS-PLAN-ALIGNMENT-20260624
title: WAS-XWAIL-AaaS 三主项目方案协同矩阵与门禁
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/WAS-XWAIL-AaaS三主项目方案协同矩阵与门禁.md
source_path: 01-architecture/WAS-XWAIL-AaaS三主项目方案协同矩阵与门禁.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS-XWAIL-AaaS 三主项目方案协同矩阵与门禁

## 1. 目的

本文用于约束三个已建立实施方案的主项目：

- `WAS世界资产体系`
- `GlobalCloud XWAIL`
- `GlobalCloud AaaS`，当前本地目录为 `GlobalCloud AAAS`

目标不是替代三个项目的实施方案，而是防止三个方案在职责、交付物、版本、状态和发布路径上产生漂移。

## 2. 总体控制链

```text
WAS 定义体系。
Ontology 定义语义。
XWAIL 定义契约。
WAE 负责资产主账和运行底座。
WAES 负责注册、授权、发布、治理和业务入口。
AaaS 负责服务包、订阅、计量、SLA 和商业运营。
```

任何实施方案不得绕过这条链路单独声明完成、发布、商业化或生产可用。

## 3. 三主项目职责矩阵

| 主项目 | 权威职责 | 核心交付物 | 不得承担 |
|---|---|---|---|
| WAS世界资产体系 | WAS 顶层语义、三层资产、八维、八流、生命周期、治理原则 | WAS 术语表、语义基线、Ontology 映射要求、WAE/WAES 边界、硬停止规则 | 不直接实现业务系统，不替代 GFIS/GPC/PVAOS 事实源，不替代 XWAIL Schema，不替代 AaaS 商业包 |
| GlobalCloud XWAIL | WAS 的机器契约、Schema、Profile、Validator、模板、示例、迁移、一致性测试 | XWAIL Schema、JSON Schema、Parser、Validator、Profile、XAP、错误码、CI 门禁、迁移规则 | 不重定义 WAS 语义，不承担 WAES 浏览器和发布治理，不承担 AaaS 定价、计量和商业状态 |
| GlobalCloud AaaS | 服务包、订阅、计量、SLA、商业交付、运营治理 | ServicePackage、服务目录、Metering、SLA、EvidenceRequirement、订阅状态、退出迁移条款 | 不私建资产模型，不绕过 XWAIL 契约，不绕过 WAES 发布，不把商业叙事替代事实和证据 |

## 4. 交付物依赖矩阵

| AaaS/SCaaS 交付物 | 必须依赖 WAS | 必须依赖 XWAIL | 必须依赖 WAES | 最低状态 |
|---|---|---|---|---|
| 资产模型服务 | WAS 术语、三层资产、八维八流 | AssetGroup、AssetUnit、Dimensions、Relations、Validator | 模型注册与授权 | `Registered` |
| 行业 Profile 服务 | 行业对象和语义边界 | Industry Profile、Profile Migration、OntologyRef | Profile 审批 | `Authorized` |
| 场景资产包服务 | 场景资产包边界和生命周期 | Scenario Instance Model、XAP、StateMachine | 发布与版本治理 | `Published` 才可对外 |
| 数字孪生服务 | 资产生命周期和状态语义 | Runtime Binding、FlowEvent、Snapshot | 运行健康、审计、回滚 | `Authorized` |
| 治理可信服务 | 权利、责任、规则和证据边界 | Policy、SecurityProfile、EvidenceRequirement | 授权、审计、证据完整性 | `Published` |
| 价值计量服务 | EconomicDimension、ValueFlow、CreditFlow | Metering、SLA、EvidenceRecord | 服务包运行治理 | `Published` |
| 商业订阅服务 | 服务化边界 | ServicePackage 绑定 | 服务包发布状态 | AaaS `subscribable` 需 WAES `Published` |

## 5. 版本兼容矩阵

任何三项目联动交付必须声明：

| 字段 | 含义 | 示例 |
|---|---|---|
| WAS version | 语义和治理基线 | `1.2.0` |
| Ontology version | 术语、关系和推理基线 | `0.2.x` |
| XWAIL version | Schema/Profile/Validator 契约版本 | `1.2.0` |
| Profile version | 行业或场景 Profile | `SupplyChain Profile 1.0` |
| AaaS ServicePackage version | 服务包版本 | `GSC ServicePackage 0.1` |
| WAES status | 注册、授权、发布状态 | `Draft / Registered / Authorized / Published` |
| Commercial status | 商业状态 | `draft / pilot / subscribable / suspended / retired / blocked` |
| decision | 兼容结论 | `compatible / migration_required / deprecated / blocked` |

没有版本兼容矩阵的方案，不得进入 `Published`、`Trusted`、`production_ready` 或商业订阅状态。

## 6. 冲突判定规则

| 冲突类型 | 判定 | 处理 |
|---|---|---|
| XWAIL 方案重定义 WAS 八维、八流、生命周期 | `blocked` | 回退到 WAS 语义基线 |
| AaaS 服务包自定义资产对象但无 XWAIL 模型 | `blocked` | 补 XWAIL 模型、Profile 和 Validator |
| AaaS 声明可订阅但 WAES 未发布 | `blocked` | 降级为 `candidate` 或 `pilot` |
| WAS 新增术语但无 XWAIL/Ontology 映射 | `repair_required` | 补映射表和兼容矩阵 |
| XWAIL 方案使用旧版本基线但未声明迁移 | `repair_required` | 增加 V1.2 迁移补充 |
| AaaS 方案引用旧 WAS 版本但未声明上位基线 | `repair_required` | 固定以 GPCF V1.2 为当前协同基线 |
| AI 推理结果被写成事实 | `blocked` | 降级为 Candidate，补 WAES 授权和证据链 |

## 7. 方案协同检查清单

每次修改三个方案之一，必须检查：

1. 是否仍声明 `WAS 定义体系，XWAIL 定义契约，AaaS 服务化运营`。
2. 是否明确 WAES 是正式注册、授权和发布入口。
3. 是否明确本地 `GlobalCloud AAAS` 等价于正式产品名 `GlobalCloud AaaS`。
4. 是否没有把 AaaS 服务目录写成资产语义源。
5. 是否没有把 XWAIL 工程实现写成业务系统完成。
6. 是否没有把 WAS 规划写成生产系统完成。
7. 是否维护版本兼容矩阵。
8. 是否对冲突给出 `compatible / migration_required / deprecated / blocked` 判定。

## 8. 自动门禁

本轮建立以下检查脚本：

```bash
python3 tools/kds-sync/validate_was_xwail_aaas_plan_alignment.py
```

该脚本只验证方案协同性和关键约束存在性，不声明三个项目已完成实现、已发布、已商业上线或已通过 WAES 审批。

## 9. 当前边界

本文和脚本只能证明三项目实施方案具备一致性控制入口。它们不证明：

- XWAIL Schema / Validator 已实现；
- WAES 已完成真实发布审批；
- AaaS 已可商业订阅；
- SCaaS 已完成客户交付；
- GFIS/GPC/PVAOS 已产生真实业务闭环。
