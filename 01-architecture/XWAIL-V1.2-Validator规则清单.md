---
doc_id: GPCF-DOC-XWAIL-V12-VALIDATOR-RULES-20260623
title: XWAIL V1.2 Validator 规则清单
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, Brain, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/XWAIL-V1.2-Validator规则清单.md
source_path: 01-architecture/XWAIL-V1.2-Validator规则清单.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# XWAIL V1.2 Validator 规则清单

## 1. 目的

本文把 `XWAIL V1.2` 草案中的对象、错误码、示例模型和发布治理转化为 Validator 检查清单。本文是规则清单，不是已实现的验证器代码，也不代表模型已发布。

## 2. Validator 分层

| Validator | 主要职责 | 典型阻断 |
|---|---|---|
| Schema Validator | 校验结构、类型、必填、枚举、命名空间、序列化一致性 | 模型不可解析、对象缺失、字段类型错误 |
| Policy Validator | 校验治理策略、状态、关系、权限、安全、复杂度、迁移和发布前置条件 | 循环关系、未授权引用、缺 SecurityProfile、绕过 WAES |
| Business Validator | 校验场景、服务包、SLA、计量、证据、AAAS 绑定和业务边界 | 缺事实源、缺 owner、服务包不可运营、商业绑定非法 |
| Ontology-aware Validator | 校验 `ontologyRef`、术语版本、上下位关系、Profile 映射和推理规则适用性 | 语义不一致、术语版本不兼容、推理规则不适用 |

## 3. 错误码到 Validator 映射

| 错误码类别 | 主 Validator | 辅助 Validator | 说明 |
|---|---|---|---|
| `XWAIL-SCHEMA` | Schema Validator | Policy Validator | 结构、字段、类型、枚举、序列化 |
| `XWAIL-REFERENCE` | Schema Validator | Policy Validator / Ontology-aware Validator | ID、版本、命名空间、ontologyRef、profileRef |
| `XWAIL-RELATION` | Policy Validator | Ontology-aware Validator | 静态关系、循环、方向、基数、语义关系 |
| `XWAIL-STATE` | Policy Validator | Business Validator | 状态机、生命周期、补偿、运行状态 |
| `XWAIL-SECURITY` | Policy Validator | Business Validator | Integration、SecurityProfile、租户、授权、敏感字段 |
| `XWAIL-COMPLEXITY` | Policy Validator | Business Validator | 嵌套、对象数量、关系数量、规则复杂度 |
| `XWAIL-DIMFLOW` | Policy Validator | Ontology-aware Validator / Business Validator | 八维、八流、维流边界和证据流 |
| `XWAIL-BUSINESS` | Business Validator | Policy Validator | 场景目标、owner、事实源、价值口径、证据要求 |
| `XWAIL-GOVERNANCE` | Policy Validator | Business Validator | 状态、审批、证据包、发布、授权、兼容矩阵 |
| `XWAIL-SERVICE` | Business Validator | Policy Validator | ServicePackage、服务依赖、运行健康、AAAS 绑定 |
| `XWAIL-PROFILE-MIGRATION` | Policy Validator | Ontology-aware Validator | Profile 覆盖、模板继承、迁移、字段映射 |
| `XWAIL-METERING-SLA` | Business Validator | Policy Validator | Metering、SLA、结算、审计证据 |

## 4. 检查阶段

| 阶段 | 输入状态 | 目标 | 必跑 Validator |
|---|---|---|---|
| Draft Preview | Draft | Studio/WAE 沙箱预览 | Schema、Ontology-aware 预评估 |
| Registration | Draft -> Registered | 登记模型并形成依赖图 | Schema、Policy |
| Authorization | Registered -> Authorized | 试运行授权 | Schema、Policy、Business、Ontology-aware |
| Publication | Authorized -> Published | 正式发布 | 全部 Validator |
| Commercial Binding | Published -> AAAS 绑定 | 服务包商业化 | Business、Policy |
| Deprecation / Migration | Published -> Deprecated/Archived | 废弃、迁移和归档 | Policy、Business、Ontology-aware |

## 5. 兼容性等级门禁

| 等级 | Validator 门禁 |
|---|---|
| Core | Schema 必须通过；Policy 不得出现 High/Critical/Blocker |
| Operational | Core + Policy 必须通过；Business 对运行对象、Integration、SecurityProfile、Runtime Binding、ServicePackage、Metering 不得出现 High/Critical/Blocker |
| Trusted | Operational + Ontology-aware 必须通过；证据、审计、Policy、SLA、合规、可追溯链不得出现 High/Critical/Blocker |

`Published` 至少达到 `Operational`。涉及合规、碳账本、结算、认证、审计的模型必须达到 `Trusted`。

## 6. 示例模型检查矩阵

| 示例 | 必查对象 | 必查错误码类别 | 最低等级 |
|---|---|---|---|
| VirtualFactory | AssetGroup、Dimensions、Relations、FlowRelations、StateMachine、Policy、ontologyRef | Schema、Reference、Relation、Dimension-Flow、Business、Profile-Migration | Operational |
| CarbonLedger | CarbonLedger、CarbonAsset、GreenEvidence、EvidenceRequirement、Policy、Metering | Dimension-Flow、Business、Governance、Metering-SLA、Ontology-aware | Trusted |
| ServicePackage | ServicePackage、Metering、SLA、EvidenceRequirement、AAAS binding | Service、Metering-SLA、Business、Governance | Operational |
| 完整绿色供应链综合示例 | VirtualFactory、CarbonLedger、ServicePackage、GFIS/GPC/PVAOS 事实源、WAE/WAES/AAAS 边界 | 全部 12 类错误码 | Trusted |

## 7. Runtime Binding 检查

| Runtime Binding | 检查要求 |
|---|---|
| `AssetInstance` | 必须能回指 AssetGroup/AssetUnit 和模型版本 |
| `DimensionValue` / `DimensionSnapshot` | 必须区分静态维度、实时值和快照时间 |
| `RelationInstance` / `RelationSnapshot` | 必须匹配 Relations 的类型、方向和基数 |
| `FlowEvent` / `FlowTrace` | 必须匹配 FlowRelations 和事件来源 |
| `StateInstance` / `StateTransitionEvent` | 必须符合 StateMachine 转换规则 |
| `PolicyDecision` / `PolicyViolation` / `PolicyEvidence` | 必须记录策略、结果、证据和操作者 |
| `IntegrationConnection` / `IntegrationEvent` / `SyncJob` | 必须绑定 Integration 和 SecurityProfile |
| `EvidenceRecord` | 必须支持 `ontologyRef / termVersion / reasoningSource / explanationRef` |
| `MeteringRecord` | 必须绑定可计量对象、时间窗口、去重规则和审计证据 |

## 8. 可信推理写入检查

| 检查项 | 要求 |
|---|---|
| 推理状态 | 只有 `Verified` 和 `Trusted` 可进入 WAE |
| WAES 授权 | 写入必须经过 WAES 策略授权 |
| 来源证据 | 必须绑定原始证据或来源记录 |
| Ontology 校验 | 必须通过 ontologyRef、术语版本、上下位关系和推理规则适用性检查 |
| 写入失败 | 必须生成 `PolicyViolation` 和带 reasoning 详情的 `EvidenceRecord` |
| Brain 边界 | Brain 可提交建议，但不能绕过 WAES 写入正式模型或主账 |

## 9. 发布前 Definition of Done

发布前必须满足：

1. Schema Validator 无 High/Critical/Blocker。
2. Policy Validator 无 High/Critical/Blocker。
3. Business Validator 无 High/Critical/Blocker。
4. Ontology-aware Validator 对 Trusted 模型无 High/Critical/Blocker。
5. Published 模型证据包完整。
6. WAS/Ontology/XWAIL/SupplyChain Profile 版本兼容矩阵存在。
7. ServicePackage 只绑定允许状态的模型版本。
8. Integration 均绑定 SecurityProfile。
9. EvidenceRecord 与 MeteringRecord 可回指运行对象、语义来源和审计链。
10. 未出现绕过 WAES 注册、授权、发布流程的路径。

## 10. 非声明

本文不声明 Validator 已经实现，不声明 XWAIL V1.2 已正式发布，不声明任何 GFIS/GPC/PVAOS/WAES/AAAS 生产写入已经完成。
