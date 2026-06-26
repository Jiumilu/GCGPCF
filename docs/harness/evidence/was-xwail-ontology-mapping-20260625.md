---
doc_id: GPCF-DOC-WAS-XWAIL-ONTOLOGY-MAPPING-20260625
title: WAS-XWAIL-Ontology 映射证据 2026-06-25
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/was-xwail-ontology-mapping-20260625.md
source_path: docs/harness/evidence/was-xwail-ontology-mapping-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# WAS-XWAIL-Ontology 映射证据 2026-06-25

## 1. 任务标识

| 项 | 值 |
|---|---|
| task_id | `WAS-XWAIL-ONTOLOGY-MAPPING-001` |
| 目标状态 | `xwail_mapping_candidate` |
| 结果 | `was_xwail_ontology_mapping = controlled` |
| WAS 基线 | `WAS semantic contract`，来源 `WAS世界资产体系/okf/was/*` |
| Ontology 基线 | `0.1.0`，来源 `WAS世界资产体系/okf/ontology.yaml` |
| XWAIL 基线 | `1.1.0`，来源 `GlobalCloud XWAIL/models/examples/warehouse-basic.xwail.json` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

machine_status: `accepted = false`、`integrated = false`、`production_ready = false`、`customer_accepted = false`

本文只建立 WAS、Ontology 与 XWAIL 的映射候选证据，不修改 WAS 主术语、不写入 KDS API、不写入 GFIS runtime、不发布 WAES、不绑定 AaaS 服务。

## 2. 已执行命令

| 项 | 仓库 | 命令 | 结果 |
|---|---|---|---|
| WAS validators | `WAS世界资产体系` | `python3 okf/validators/validate_all.py` | pass，12 个 WAS validator 通过 |
| XWAIL validator | `GlobalCloud XWAIL` | `python3 scripts/validate_xwail.py --all` | pass，checked 2，issue_count 0 |
| XAP build check | `GlobalCloud XWAIL` | `python3 scripts/build_xap.py --check` | pass，checked 1，check_only true |
| XAP verify | `GlobalCloud XWAIL` | `python3 scripts/verify_xap.py --all` | pass，checked 1，issue_count 0 |
| GPCF mapping gate | `GlobalCoud GPCF` | `python3 tools/kds-sync/validate_was_xwail_ontology_mapping.py` | 本文新增后执行 |

## 3. 职责边界

| 层 | 权威职责 | 禁止替代 |
|---|---|---|
| WAS | 定义三层资产、八维、八流、生命周期与治理原则 | 不替代业务事实源，不声明真实业务完成 |
| Ontology | 定义概念、词表、关系、语义约束和推理结构 | 不替代 XWAIL 契约，不直接写入运行主账 |
| XWAIL | 定义机器可读模型、字段、Profile、Validator、XAP 包和发布候选契约 | 不重定义 WAS 语义，不绕过 WAES 发布和 AaaS 绑定 |
| WAES | 对模型注册、授权、发布和运行绑定进行业务实现 | 本证据不声明 WAES 已发布 |
| KDS/Brain | 使用语义和证据进行知识治理、检索和推理 | 推理结果不得直接升级为业务事实 |

## 4. WAS 八维到 XWAIL Dimensions 映射

| WAS dimension | Ontology 语义 | XWAIL contract | 示例证据 |
|---|---|---|---|
| `physical_asset` | 物理世界资产 | `Dimensions.Physical` | `warehouse-001`、`forklift-001` |
| `rule_asset` | 规则与治理资产 | `Dimensions.Rule` | `rule:warehouse-safety-basic` |
| `intelligence_asset` | 知识、算法、技能与方法 | `Dimensions.Intellectual` | `knowledge:warehouse-ops-basic` |
| `data_asset` | 数据、记录、指标和证据 | `Dimensions.Data` | `data:inventory-snapshot` |
| `economic_asset` | 价值、成本、收益与结算 | `Dimensions.Economic` | `cc-logistics`、`assetValue` |
| `energy_asset` | 能源供应、消耗、计量和效率 | `Dimensions.Energy` | `energy:warehouse-main` |
| `organization_asset` | 组织、角色、责任人与权限 | `Dimensions.Organization` | `org:globalcloud-demo` |
| `spacetime_asset` | 位置、时间、路线和里程碑 | `Dimensions.SpaceTime` | `geo:demo-park`、`Asia/Shanghai` |

## 5. WAS 八流到 XWAIL FlowRelations 映射

| WAS flow | Ontology 语义 | XWAIL contract | 当前状态 |
|---|---|---|---|
| `material_flow` | 物理资产移动、存储、转化与交付 | `FlowRelations.flowType` 中的物流/物料类流 | 当前示例以 `LogisticsFlow` 表达，需要后续 canonical enum 对齐 |
| `information_flow` | 数据采集、验证、发布、同步和引用 | `FlowRelations.flowType = InformationFlow` | 已有示例 |
| `capital_flow` | 投资、付款、结算与分配 | `FlowRelations.flowType` 中的资金类流 | 当前最小示例未覆盖，后续 Profile 增补 |
| `spacetime_flow` | 定位、调度、追踪、周期化 | `FlowRelations.flowType` 中的时空类流 | 当前最小示例未覆盖，后续 Profile 增补 |
| `energy_flow` | 能源供应、消耗、转换和优化 | `FlowRelations.flowType` 中的能源类流 | 当前最小示例未覆盖，后续 Profile 增补 |
| `commerce_flow` | 报价、订单、合同、采购和服务交付 | `FlowRelations.flowType` 中的商业/服务类流 | 当前最小示例未覆盖，后续 SCaaS Profile 增补 |
| `knowledge_flow` | 知识创建、迁移、训练、推理和复用 | `FlowRelations.flowType` 中的知识类流 | 当前最小示例未覆盖，后续 Brain/KDS Profile 增补 |
| `rule_flow` | 规则执行、审批、阻断、审查和确认 | `FlowRelations.flowType` 中的治理类流 | 当前最小示例未覆盖，后续 WAES gate Profile 增补 |

## 6. Ontology 到 XWAIL 回指规则

| 对象 | 必须字段 | 规则 |
|---|---|---|
| XWAIL model | `wasBaseline`、`ontologyVersion` | 必须声明所使用的 WAS 与 Ontology 基线 |
| XWAIL asset | `ontologyRef` | 表示 WAS/Ontology 概念时必须回指语义来源 |
| XWAIL profile | `profile` | 行业或场景扩展必须声明 Profile 名称 |
| XWAIL package | XAP manifest | 发布候选必须可被 build check 和 verify 检查 |
| Evidence | source refs、evidence refs、boundary | 映射证据不得升级为业务事实或客户验收 |

## 7. 版本兼容候选

| WAS | Ontology | XWAIL | 兼容判断 | 限制 |
|---|---|---|---|---|
| `WAS semantic contract` | `0.1.0` | `1.1.0` | `mapping_candidate` | 只证明本地语义映射与最小 XWAIL 契约可对齐 |

后续若 WAS 主术语、Ontology term、XWAIL Schema/Profile/Validator 任一变化，必须更新本映射证据或生成后继版本，并触发依赖矩阵中 `WAS -> Ontology -> XWAIL` 的重新审查。

## 8. 依赖传导

| 依赖边 | 本轮影响 |
|---|---|
| `WAS -> Ontology -> XWAIL` | 从 `semantic_foundation_candidate` 推进到 `xwail_mapping_candidate` |
| `WAES -> XWAIL -> AaaS` | 只提供语义映射前置，不解除 WAES repair_required/authorization_boundary |
| `GFIS/GPC/PVAOS -> SCaaS` | 为后续 SCaaS Profile 提供八维八流映射依据，但不证明真实 source-of-record |
| `KDS -> Brain` | 为知识治理和推理回指提供语义基线，但不允许 Brain 直接写入业务事实 |

## 9. 回滚与降级

- 若 WAS validator 失败，回滚本证据并保持 `semantic_foundation_candidate`。
- 若 XWAIL validator、XAP build check 或 XAP verify 失败，保持 `ready_for_review / local_dev_boundary`，不进入 `xwail_mapping_candidate`。
- 若映射与主术语冲突，必须登记 rework，不得修改主术语绕过门禁。
- 若后续 WAES、AaaS、GFIS、KDS 或 Brain 使用本映射产生冲突，以项目群主方案和人工确认优先。

## 10. 禁止声明

- 不声明 WAS 主方案已 accepted。
- 不声明 Ontology 已覆盖全部业务语义。
- 不声明 XWAIL 完整工具链完成。
- 不声明 WAES 已发布。
- 不声明 AaaS 已绑定或可订阅。
- 不声明 GFIS/GPC/PVAOS/SCaaS 真实业务闭环完成。
- 不声明 KDS API 已真实同步。
- 不声明 Brain 推理可直接写入业务事实。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
