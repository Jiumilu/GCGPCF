---
doc_id: GPCF-DOC-XWAIL-V12-DRAFT-20260623
title: XWAIL 可扩展世界资产信息建模语言规范 V1.2 草案
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/XWAIL可扩展世界资产信息建模语言规范V1.2草案.md
source_path: 01-architecture/XWAIL可扩展世界资产信息建模语言规范V1.2草案.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# XWAIL 可扩展世界资产信息建模语言规范 V1.2 草案

## 1. 总则与定位

`XWAIL = eXtensible World Asset Information Language`。XWAIL 是 WAS 的主规范建模语言，但允许辅助 DSL、配置语言和行业工具语言存在。辅助语言不得绕过 XWAIL 的模型契约、验证、注册、授权和发布治理。

V1.2 是 V1.1 的统一命名、治理、AaaS/SCaaS 对齐升级版，不是全新规范。XWAIL 支持 XML 和 JSON 双格式序列化。

## 2. 与 GlobalCloud 世界资产体系的关系

```text
WAS 定义资产世界。
Ontology 定义资产语义。
XWAIL 描述资产世界并固化机器契约。
WAE 运行资产世界。
WAES 治理和发布资产世界。
AaaS/SCaaS 服务化运营资产世界。
```

`WAES` 是 XWAIL 的唯一正式发布入口。`Studio` 可生成和预览 XWAIL，但产物必须提交 WAES 审核发布。其他模板生成的 XWAIL 必须在 WAES 注册、授权与发布。`AAAS` 负责把已发布或已授权模型绑定到服务包和商业状态。

XWAIL 与 Ontology 是双向对齐关系。Ontology 解决语义理解，XWAIL 解决模型契约与运行约束。所有 XWAIL 核心对象均可选绑定 `ontologyRef`，用于回指 WAS 语义知识层中的术语、概念关系和推理规则。

## 3. 核心概念与术语

| 术语 | 定义 |
|---|---|
| Standard Model | 标准模型，定义跨行业通用语义 |
| Industry Profile | 行业 Profile，定义行业词表、字段、规则、模板、验证规则 |
| Scenario Instance Model | 场景实例模型，定义具体业务场景的资产组合、流程、事件、接口、权限、SLA、证据和计量 |
| Runtime Binding | 模型与运行时对象的绑定 |
| ServicePackage | 可治理、可运行、可商业绑定的服务包 |
| ontologyRef | XWAIL 对象到 Ontology 术语、概念或关系的可选语义回指 |

## 4. 模型类型与对象体系

模型类型固定为：

- `Standard Model`
- `Industry Profile`
- `Scenario Instance Model`

通用核心对象固定为：

```text
AssetGroup / AssetUnit / Dimensions / Relations / FlowRelations / StateMachine /
Policy / Integration / SecurityProfile / Templates / ModelDependency / Migration /
ServicePackage / Metering / SLA / EvidenceRequirement
```

模型状态固定为：

```text
Draft / Registered / Authorized / Published / Deprecated / Archived
```

## 5. 通用核心对象规范

| 对象 | 作用 |
|---|---|
| AssetGroup | 可组合资产组 |
| AssetUnit | 最小资产单元；可与实例对象在轻量场景中合并 |
| Dimensions | 八维画像，区分静态维度和实时维度 |
| Relations | 静态/结构关系 |
| FlowRelations | 八流动态协同模型 |
| StateMachine | 生命周期规则 |
| Policy | 规则、约束、治理策略 |
| Integration | 外部连接契约 |
| SecurityProfile | 外部集成的认证、加密、授权和安全配置 |
| Templates | 模型复用结构，不能作为运行时对象直接执行 |
| ModelDependency | 模型依赖声明 |
| Migration | 版本迁移规则 |
| ServicePackage | 服务范围、绑定模型、接口、SLA、计量、权限和证据要求 |
| Metering | 可计量资产、事件、调用、孪生小时、证据包、AI 工作单元 |
| SLA | 可用性、响应时间、处理时限、证据交付、合规期限 |
| EvidenceRequirement | 服务、事件、流程必须产生的证据要求 |

所有通用核心对象可声明 `ontologyRef`。`ontologyRef` 不替代 XWAIL 对象结构，也不替代业务事实源；它用于说明该对象对应的 Ontology 术语、版本和语义关系。

## 6. 运行时对象规范

运行时对象固定为：

```text
AssetInstance / DimensionValue / DimensionSnapshot / RelationInstance /
RelationSnapshot / FlowEvent / FlowTrace / StateInstance / StateTransitionEvent /
PolicyDecision / PolicyViolation / PolicyEvidence / IntegrationConnection /
IntegrationEvent / SyncJob / EvidenceRecord / MeteringRecord
```

`AssetGroup / AssetUnit` 与 `AssetInstance` 可分离，也可在轻量场景中合并。`Dimensions` 区分静态维度和实时维度；实时维度对应运行时值、快照和时序记录。

`EvidenceRecord` 增加语义来源字段：

```text
ontologyRef / termVersion / reasoningSource / explanationRef
```

可信推理记录不新增独立运行时对象，统一写入带 reasoning 详情的 `EvidenceRecord`。推理写入失败必须生成 `PolicyViolation` 和带 reasoning 详情的 `EvidenceRecord`。

## 7. 行业 Profile 机制

行业 Profile 定义行业词表、行业字段、行业规则、行业模板和行业验证规则。行业 Profile 可以覆盖核心字段，但必须声明覆盖原因、范围、兼容性影响和治理责任，并通过 WAES 治理审批。

模板类型固定为：

```text
Core Template / Industry Template / Scenario Template / Organization Template
```

## 8. SupplyChain Profile V1.0

SCaaS 需要独立 `SupplyChain Profile`。第一阶段核心对象为：

```text
Enterprise / Factory / VirtualFactory / Product / Material / Order / OrderPool /
Warehouse / LogisticsNode / CarbonLedger / CarbonAsset / GreenEvidence /
Certification / Settlement / Alliance / ServiceSubscription
```

`GFIS / GPC / PVAOS` 基于同一个 `SupplyChain Profile`，产生不同角色视角的场景实例模型。

## 9. 服务包、计量、SLA 与证据要求

`ServicePackage` 属于 WAES 的业务治理对象；AAAS 负责商业化优化、订阅、套餐、定价和计费。AAAS 可基于同一个 WAES 服务包生成基础版、专业版、企业版等商业套餐。

服务包运行治理由 WAES 和 AAAS 共同承担：WAES 管运行、授权、审计、证据、健康；AAAS 管商业状态、订阅、套餐和计费联动。PVAOS 负责联盟内结算，AAAS 负责通用订阅治理。

## 10. 模板、依赖与迁移

模板实例化后必须生成明确的模型版本和依赖关系，不能作为运行时对象直接执行。`ModelDependency` 必须声明依赖的标准模型、Profile、模板和外部接口。`Migration` 必须支持旧模型版本向新模型版本迁移。

版本号采用组合格式：

```text
major.minor.patch-YYYYMMDD
```

示例：`1.2.0-20260623`。

## 11. 治理生命周期与状态机

| 状态 | 含义 |
|---|---|
| Draft | 草稿，可在 Studio 或 WAE 沙箱预览 |
| Registered | 已登记，可进入治理流程 |
| Authorized | 已授权，可试运行 |
| Published | 已发布，可商业绑定和正式运行 |
| Deprecated | 已废弃，但可保留兼容与迁移 |
| Archived | 已归档，不再运行 |

商业发布只能绑定 `Published`；试运行可绑定 `Authorized`；内部测试可绑定 `Draft`。

## 12. WAES 注册、授权、发布流程

`Studio` 生成的 XWAIL 必须附带生成来源、编辑记录、模板来源和操作者信息。标准治理由 `GlobalCloud XWAIL` 项目负责；建模生产与编辑来源治理由 `Studio` 负责；业务模型治理与发布由 `WAES` 负责；服务包绑定与商业状态治理由 `AAAS` 负责。

行业 Profile 和场景模型通过自动验证后仍需 WAES 治理审批；标准模型走 GlobalCloud XWAIL 标准治理。

## 13. 验证器与错误码

Validator 类型固定为：

- `Schema Validator`
- `Policy Validator`
- `Business Validator`
- `Ontology-aware Validator`

`Business Validator` 负责 `ServicePackage / Metering / SLA / EvidenceRequirement / AAAS 绑定 / WAES 发布条件`。

`Ontology-aware Validator` 负责校验 `ontologyRef` 有效性、术语版本、上下位关系、字段语义匹配、Profile 映射、推理规则适用性。该校验不替代 Schema、Policy 或 Business Validator，而是补足语义合理性校验。

错误严重级别固定为：

```text
Low / Medium / High / Critical / Blocker
```

验证结果字段固定为：

```text
errorCode / severity / objectPath / message / suggestedFix / validator / timestamp
```

错误码采用可读格式，例如 `XWAIL-SCHEMA-001`。V1.2 错误码分类为：

| 类别 | 前缀 | 覆盖范围 |
|---|---|---|
| Schema | XWAIL-SCHEMA | 结构、类型、必填、序列化 |
| Reference | XWAIL-REFERENCE | 引用、ID、命名空间、版本指针 |
| Relation | XWAIL-RELATION | 静态关系、循环、方向、基数 |
| State | XWAIL-STATE | 状态机、转换、终态、补偿 |
| Security | XWAIL-SECURITY | SecurityProfile、认证、授权、加密 |
| Complexity | XWAIL-COMPLEXITY | 嵌套、规模、复杂度限制 |
| Dimension-Flow | XWAIL-DIMFLOW | 八维、八流、维流映射 |
| Business | XWAIL-BUSINESS | 场景完整性、权限、业务规则 |
| Governance | XWAIL-GOVERNANCE | 注册、授权、发布、审批、证据包 |
| Service | XWAIL-SERVICE | ServicePackage、服务范围、服务依赖 |
| Profile-Migration | XWAIL-PROFILE-MIGRATION | Profile 覆盖、依赖、模板继承、迁移、兼容、字段映射 |
| Metering-SLA | XWAIL-METERING-SLA | 计量、SLA、订阅、商业绑定 |

正式 V1.2 错误码表每类至少 10 个基础错误码，并且每个错误码必须提供 `suggestedFix`。

### 13.1 V1.2 基础错误码表

#### 13.1.1 Schema

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-SCHEMA-001 | High | Schema Validator | 缺少根元素或根对象 | 补充 `XWAIL` 根结构并声明版本 |
| XWAIL-SCHEMA-002 | High | Schema Validator | 缺少必填 `id` | 为对象补充文档内唯一 `id` |
| XWAIL-SCHEMA-003 | Medium | Schema Validator | `id` 格式不符合规范 | 使用稳定、可解析、无空格的标识 |
| XWAIL-SCHEMA-004 | High | Schema Validator | `modelType` 缺失或非法 | 使用 `Standard Model`、`Industry Profile` 或 `Scenario Instance Model` |
| XWAIL-SCHEMA-005 | High | Schema Validator | 必填对象结构缺失 | 按对象类型补齐必需子结构 |
| XWAIL-SCHEMA-006 | Medium | Schema Validator | 字段类型不匹配 | 按 Schema 修正字符串、数值、布尔、数组或对象类型 |
| XWAIL-SCHEMA-007 | Medium | Schema Validator | 枚举值非法 | 使用规范定义的枚举值 |
| XWAIL-SCHEMA-008 | High | Schema Validator | XML/JSON 序列化结构不一致 | 对齐 XML 与 JSON 的对象层级和字段名 |
| XWAIL-SCHEMA-009 | Medium | Schema Validator | 命名空间声明缺失 | 补充核心、行业、治理或扩展命名空间 |
| XWAIL-SCHEMA-010 | Medium | Schema Validator | 未识别扩展字段 | 为扩展字段声明命名空间、Profile 或扩展说明 |

#### 13.1.2 Reference

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-REFERENCE-001 | High | Schema Validator | 引用目标不存在 | 创建被引用对象或修正引用 ID |
| XWAIL-REFERENCE-002 | High | Schema Validator | 引用类型不匹配 | 将引用指向正确对象类型 |
| XWAIL-REFERENCE-003 | Medium | Schema Validator | 引用版本缺失 | 补充被引用模型、模板或 Profile 的版本 |
| XWAIL-REFERENCE-004 | High | Policy Validator | 跨命名空间引用未授权 | 增加授权声明或改用允许的命名空间 |
| XWAIL-REFERENCE-005 | Medium | Schema Validator | `ontologyRef` 指向不存在术语 | 修正术语 URI 或更新 Ontology 版本 |
| XWAIL-REFERENCE-006 | Medium | Schema Validator | `profileRef` 缺失 | 为行业对象绑定 Profile |
| XWAIL-REFERENCE-007 | Medium | Schema Validator | `templateRef` 缺失或不可解析 | 补充模板引用和版本 |
| XWAIL-REFERENCE-008 | High | Policy Validator | 外部接口引用无契约 | 绑定 Integration 契约 |
| XWAIL-REFERENCE-009 | Medium | Schema Validator | 重复 ID | 保证同一文档内 ID 唯一 |
| XWAIL-REFERENCE-010 | High | Policy Validator | 引用链断裂 | 补齐依赖链或移除无效依赖 |

#### 13.1.3 Relation

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-RELATION-001 | High | Policy Validator | 关系源对象不存在 | 修正 `sourceRef` |
| XWAIL-RELATION-002 | High | Policy Validator | 关系目标对象不存在 | 修正 `targetRef` |
| XWAIL-RELATION-003 | High | Policy Validator | 组成关系存在循环 | 调整资产层级，移除循环依赖 |
| XWAIL-RELATION-004 | Medium | Policy Validator | 关系类型非法 | 使用规范关系类型或声明扩展 |
| XWAIL-RELATION-005 | Medium | Policy Validator | 关系方向与语义不匹配 | 修正方向或更换关系类型 |
| XWAIL-RELATION-006 | Medium | Policy Validator | 关系基数不满足约束 | 调整一对一、一对多或多对多声明 |
| XWAIL-RELATION-007 | Medium | Policy Validator | 静态关系误用为动态流 | 将动态行为移入 `FlowRelations` |
| XWAIL-RELATION-008 | Medium | Ontology-aware Validator | 关系与 Ontology 上下位关系冲突 | 修正 `ontologyRef` 或关系类型 |
| XWAIL-RELATION-009 | Low | Policy Validator | 关系缺少描述 | 补充业务说明或治理目的 |
| XWAIL-RELATION-010 | High | Policy Validator | 关键关系缺少证据要求 | 为关键关系绑定 `EvidenceRequirement` |

#### 13.1.4 State

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-STATE-001 | High | Schema Validator | 缺少初始状态 | 为 StateMachine 定义初始状态 |
| XWAIL-STATE-002 | Medium | Schema Validator | 缺少终态 | 定义完成、退役或归档终态 |
| XWAIL-STATE-003 | High | Policy Validator | 状态转换目标不存在 | 修正 Transition 的目标状态 |
| XWAIL-STATE-004 | Medium | Policy Validator | 状态转换缺少触发条件 | 补充事件、条件或策略触发 |
| XWAIL-STATE-005 | High | Policy Validator | 状态机存在不可达状态 | 删除不可达状态或补充转换 |
| XWAIL-STATE-006 | Medium | Policy Validator | 缺少失败补偿路径 | 为关键转换定义补偿或回滚 |
| XWAIL-STATE-007 | High | Policy Validator | 生命周期阶段映射不完整 | 补齐 Plan/Design/Build/Deploy/Operate/Optimize/Retire 映射 |
| XWAIL-STATE-008 | Medium | Business Validator | 状态与服务包运行状态不一致 | 对齐模型状态和服务运行状态 |
| XWAIL-STATE-009 | Medium | Policy Validator | 退役状态缺少归档策略 | 补充证据、数据和权限归档要求 |
| XWAIL-STATE-010 | High | Business Validator | Published 模型状态机未达到 Operational 要求 | 补齐运行转换、事件和验证规则 |

#### 13.1.5 Security

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-SECURITY-001 | Critical | Policy Validator | Integration 未绑定 SecurityProfile | 为每个外部 Integration 绑定 SecurityProfile |
| XWAIL-SECURITY-002 | Critical | Policy Validator | 缺少认证方式 | 声明 OAuth、API key、mTLS 或其他认证方式 |
| XWAIL-SECURITY-003 | High | Policy Validator | 权限范围过宽 | 收窄 scope、role 或 tenant 边界 |
| XWAIL-SECURITY-004 | High | Policy Validator | 缺少租户隔离声明 | 增加 tenant、org 或 data boundary |
| XWAIL-SECURITY-005 | Critical | Policy Validator | 敏感字段未声明保护策略 | 增加脱敏、加密或访问控制策略 |
| XWAIL-SECURITY-006 | High | Policy Validator | 缺少审计策略 | 补充访问、变更、发布和写入审计 |
| XWAIL-SECURITY-007 | High | Policy Validator | 外部写入缺少授权策略 | 增加 WAES 授权和写入条件 |
| XWAIL-SECURITY-008 | Critical | Policy Validator | 凭据或密钥出现在模型内容中 | 移除凭据并改用安全引用 |
| XWAIL-SECURITY-009 | Medium | Policy Validator | 加密要求未声明 | 声明传输和存储加密策略 |
| XWAIL-SECURITY-010 | Blocker | Policy Validator | 生产写入绕过 WAES | 阻断发布并改走 WAES 审批流程 |

#### 13.1.6 Complexity

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-COMPLEXITY-001 | Medium | Policy Validator | 嵌套层级超过建议阈值 | 拆分模型或使用引用 |
| XWAIL-COMPLEXITY-002 | Medium | Policy Validator | 单模型对象数量过多 | 拆分为标准模型、Profile 和场景模型 |
| XWAIL-COMPLEXITY-003 | Medium | Policy Validator | 关系数量过多 | 抽取关键关系并分层建模 |
| XWAIL-COMPLEXITY-004 | Medium | Policy Validator | 状态机转换过多 | 拆分子状态机或流程模块 |
| XWAIL-COMPLEXITY-005 | Low | Policy Validator | 模板继承层级过深 | 减少继承层级或合并模板 |
| XWAIL-COMPLEXITY-006 | Medium | Policy Validator | 依赖图过深 | 使用 ModelDependency 分组 |
| XWAIL-COMPLEXITY-007 | Medium | Policy Validator | 单对象字段过多 | 拆分维度或扩展对象 |
| XWAIL-COMPLEXITY-008 | High | Policy Validator | 推理规则组合复杂度过高 | 限制规则范围或拆分验证阶段 |
| XWAIL-COMPLEXITY-009 | Medium | Business Validator | 服务包绑定对象过多 | 拆分为多个服务包 |
| XWAIL-COMPLEXITY-010 | High | Policy Validator | 复杂度影响运行可解释性 | 补充依赖图、证据链和分层说明 |

#### 13.1.7 Dimension-Flow

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-DIMFLOW-001 | High | Policy Validator | 缺少必需 Dimensions | 补齐资产画像维度 |
| XWAIL-DIMFLOW-002 | Medium | Policy Validator | 八维映射不完整 | 明确缺失维度是否可选或补充字段 |
| XWAIL-DIMFLOW-003 | High | Policy Validator | FlowRelations 缺失 | 为动态协同对象补充流关系 |
| XWAIL-DIMFLOW-004 | Medium | Policy Validator | 八流映射不完整 | 补齐物流、信息、资金、能量、服务、控制、价值、信用映射 |
| XWAIL-DIMFLOW-005 | Medium | Ontology-aware Validator | 维度语义与 Ontology 不匹配 | 修正 `ontologyRef` 或维度归类 |
| XWAIL-DIMFLOW-006 | Medium | Policy Validator | EconomicDimension 与 FinancialFlow 混用 | 将经济状态和资金转移分开表达 |
| XWAIL-DIMFLOW-007 | Medium | Policy Validator | EnergyDimension 与 EnergyFlow 混用 | 将能源状态和能源流动分开表达 |
| XWAIL-DIMFLOW-008 | Medium | Policy Validator | RuleDimension 与 Policy 混用 | 将规则约束和治理执行策略分开表达 |
| XWAIL-DIMFLOW-009 | High | Business Validator | 关键业务事件未映射到流 | 为订单、结算、证据、物流等事件补充 FlowEvent |
| XWAIL-DIMFLOW-010 | High | Business Validator | Trusted 模型缺少证据流 | 为关键 Dimension/Flow 绑定 EvidenceRequirement |

#### 13.1.8 Business

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-BUSINESS-001 | High | Business Validator | 场景目标缺失 | 补充场景目标、边界和业务结果 |
| XWAIL-BUSINESS-002 | High | Business Validator | 业务 owner 缺失 | 指定负责组织、角色或系统 |
| XWAIL-BUSINESS-003 | High | Business Validator | 事实源缺失 | 绑定 GFIS、GPC、PVAOS 或其他事实源 |
| XWAIL-BUSINESS-004 | Medium | Business Validator | 权责关系不清 | 补充责任方、审批方和运营方 |
| XWAIL-BUSINESS-005 | High | Business Validator | 场景模型缺少输入输出 | 补充输入、处理、输出和反馈 |
| XWAIL-BUSINESS-006 | High | Business Validator | 价值口径缺失 | 补充成本、收益、风险或合规价值口径 |
| XWAIL-BUSINESS-007 | Medium | Business Validator | 跨系统边界不清 | 明确各系统职责和数据流 |
| XWAIL-BUSINESS-008 | High | Business Validator | 缺少 SLA 或运营要求 | 绑定 SLA 对象 |
| XWAIL-BUSINESS-009 | High | Business Validator | 缺少证据要求 | 绑定 EvidenceRequirement |
| XWAIL-BUSINESS-010 | Critical | Business Validator | 将推理结果误标为业务事实 | 降级为 Candidate 或补齐 WAES 授权与证据链 |

#### 13.1.9 Governance

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-GOVERNANCE-001 | High | Policy Validator | 模型状态缺失 | 设置 Draft/Registered/Authorized/Published/Deprecated/Archived |
| XWAIL-GOVERNANCE-002 | High | Policy Validator | Published 缺少发布审批 | 补充 WAES 或标准治理审批记录 |
| XWAIL-GOVERNANCE-003 | High | Policy Validator | Published 证据包缺失 | 补充验证报告、审批记录、差异、兼容性和迁移说明 |
| XWAIL-GOVERNANCE-004 | Medium | Policy Validator | Authorized 缺少试运行边界 | 补充试运行范围、期限和回滚 |
| XWAIL-GOVERNANCE-005 | High | Policy Validator | Deprecated 缺少迁移路径 | 补充 Migration 和替代版本 |
| XWAIL-GOVERNANCE-006 | Medium | Policy Validator | 缺少发布人或发布时间 | 补充发布元数据 |
| XWAIL-GOVERNANCE-007 | High | Policy Validator | 行业 Profile 覆盖未审批 | 提交 WAES 治理审批 |
| XWAIL-GOVERNANCE-008 | Critical | Policy Validator | 商业绑定使用 Draft 模型 | 改为 Published，或降为内部测试 |
| XWAIL-GOVERNANCE-009 | Medium | Policy Validator | 缺少版本兼容矩阵 | 补充 WAS/Ontology/XWAIL/Profile 兼容记录 |
| XWAIL-GOVERNANCE-010 | Blocker | Policy Validator | 尝试绕过 WAES 正式发布入口 | 阻断并转入 WAES 注册、授权、发布流程 |

#### 13.1.10 Service

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-SERVICE-001 | High | Business Validator | ServicePackage 缺失服务范围 | 补充服务边界、对象和能力范围 |
| XWAIL-SERVICE-002 | High | Business Validator | ServicePackage 未绑定模型 | 绑定 Published 或 Authorized 模型版本 |
| XWAIL-SERVICE-003 | High | Business Validator | 服务接口缺失 | 绑定 Integration 或接口契约 |
| XWAIL-SERVICE-004 | High | Business Validator | 服务权限缺失 | 补充角色、租户、授权策略 |
| XWAIL-SERVICE-005 | Medium | Business Validator | 服务依赖未声明 | 补充 ModelDependency 或系统依赖 |
| XWAIL-SERVICE-006 | High | Business Validator | 服务包缺少运行健康要求 | 补充健康检查和运营状态 |
| XWAIL-SERVICE-007 | High | Business Validator | AAAS 绑定状态不合法 | 按 Draft/Authorized/Published 商业边界修正 |
| XWAIL-SERVICE-008 | Medium | Business Validator | 商业套餐与服务包边界不一致 | 在 AAAS 中调整套餐或服务包映射 |
| XWAIL-SERVICE-009 | High | Business Validator | 服务启停缺少治理策略 | 补充 WAES 运行治理规则 |
| XWAIL-SERVICE-010 | Critical | Business Validator | 服务包使用未授权事实源 | 改用授权事实源或补充授权记录 |

#### 13.1.11 Profile-Migration

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-PROFILE-MIGRATION-001 | High | Policy Validator | Profile 缺少名称或版本 | 补充 Profile 标识和版本 |
| XWAIL-PROFILE-MIGRATION-002 | High | Policy Validator | Profile 覆盖核心字段未声明 | 补充覆盖原因、范围、兼容性和责任 |
| XWAIL-PROFILE-MIGRATION-003 | Medium | Ontology-aware Validator | Profile 术语与 Ontology 不一致 | 更新映射表或修正术语 |
| XWAIL-PROFILE-MIGRATION-004 | High | Policy Validator | Profile 依赖缺失 | 补充标准模型、模板或外部接口依赖 |
| XWAIL-PROFILE-MIGRATION-005 | Medium | Policy Validator | 模板继承冲突 | 调整继承顺序或显式覆盖规则 |
| XWAIL-PROFILE-MIGRATION-006 | High | Policy Validator | 版本迁移规则缺失 | 为破坏性变更补充 Migration |
| XWAIL-PROFILE-MIGRATION-007 | Medium | Policy Validator | 字段映射不完整 | 补齐旧字段到新字段的映射 |
| XWAIL-PROFILE-MIGRATION-008 | High | Policy Validator | 兼容性等级下降未声明 | 补充影响说明和审批 |
| XWAIL-PROFILE-MIGRATION-009 | Medium | Policy Validator | SupplyChain Profile 分阶段对象未声明 | 补充阶段、对象范围和启用条件 |
| XWAIL-PROFILE-MIGRATION-010 | Critical | Policy Validator | 迁移导致证据链断裂 | 阻断迁移并补充证据迁移策略 |

#### 13.1.12 Metering-SLA

| code | severity | validator | message | suggestedFix |
|---|---|---|---|---|
| XWAIL-METERING-SLA-001 | High | Business Validator | Metering 对象缺失 | 补充计量对象和计量单位 |
| XWAIL-METERING-SLA-002 | High | Business Validator | 计量口径不明确 | 定义统计窗口、去重、失败和重试规则 |
| XWAIL-METERING-SLA-003 | Medium | Business Validator | 计量单位非法 | 使用规范计量单位或声明扩展 |
| XWAIL-METERING-SLA-004 | High | Business Validator | 计量记录未绑定运行对象 | 绑定 AssetInstance、FlowEvent 或 EvidenceRecord |
| XWAIL-METERING-SLA-005 | High | Business Validator | SLA 缺失 | 补充服务可用性、响应、处理或交付期限 |
| XWAIL-METERING-SLA-006 | Medium | Business Validator | SLA 指标不可测量 | 修改为可采集、可复算指标 |
| XWAIL-METERING-SLA-007 | High | Business Validator | SLA 缺少违约或补偿策略 | 补充告警、补偿、降级或回滚规则 |
| XWAIL-METERING-SLA-008 | Critical | Business Validator | 计费绑定未授权模型 | 改为 Published 模型或取消商业计费 |
| XWAIL-METERING-SLA-009 | High | Business Validator | EvidenceRequirement 与 SLA 不一致 | 对齐证据交付要求和 SLA |
| XWAIL-METERING-SLA-010 | Critical | Business Validator | 计量影响结算但缺少审计证据 | 补充 EvidenceRecord 和审计链 |

## 14. 安全集成与 SecurityProfile

每个外部 `Integration` 必须绑定 `SecurityProfile`。缺失安全绑定不得进入正式发布。

## 15. XML / JSON 序列化

XML 最小示例：

```xml
<XWAIL version="1.2.0-20260623" modelType="ScenarioInstanceModel">
  <AssetGroup id="vf-001" profile="SupplyChain">
    <Dimensions>
      <OrganizationDimension owner="enterprise-001"/>
      <PhysicalDimension type="VirtualFactory"/>
    </Dimensions>
  </AssetGroup>
</XWAIL>
```

JSON 最小示例：

```json
{
  "xwailVersion": "1.2.0-20260623",
  "modelType": "ScenarioInstanceModel",
  "assetGroup": {
    "id": "vf-001",
    "profile": "SupplyChain",
    "dimensions": {
      "organization": {"owner": "enterprise-001"},
      "physical": {"type": "VirtualFactory"}
    }
  }
}
```

## 16. 版本、兼容性与证据包

兼容性等级固定为：

| 等级 | 要求 |
|---|---|
| Core | 满足基础模型结构、八维、八流、状态机和基础验证 |
| Operational | 可进入 WAE/WAES 运行，具备 Integration、SecurityProfile、Runtime Binding、服务包和计量 |
| Trusted | 具备证据包、审计、Policy、SLA、合规和可追溯能力 |

`Published` 模型至少必须达到 `Operational`。涉及合规、碳账本、结算、认证、审计的模型必须达到 `Trusted`。`Authorized` 模型可以是 `Core` 或 `Operational`，用于试运行。`Draft / Registered` 不强制兼容性等级，但 Validator 可以给出预评估等级。

证据包规则：

| 状态 | 证据包要求 |
|---|---|
| Published | 强制 |
| Authorized | 可选 |
| Draft / Registered | 不强制 |

Published 证据包包含验证报告、审批记录、差异说明、兼容性影响和迁移说明。

WAS、Ontology、XWAIL、SupplyChain Profile 必须维护版本兼容矩阵。示例字段：

```text
WAS version / Ontology version / XWAIL version / SupplyChain Profile version / compatibility / migrationRequired
```

## 16.1 可信推理写入

推理结果状态固定为：

```text
Candidate / Verified / Trusted / Rejected
```

只有 `Verified` 和 `Trusted` 推理结果可以进入 WAE。`Trusted` 推理必须满足：证据完整、来源可信、规则通过、置信度达标、WAES 授权、可审计、可回滚。

可信推理写入 WAE 必须经过 WAES 策略授权，并绑定原始证据或来源记录。Brain 只能读取正式 Ontology、XWAIL 和 WAE 数据，不能绕过 WAES 修改正式模型。

## 17. 示例模型

本章示例用于说明 V1.2 的最小建模方式，不代表生产模型已经发布。正式发布仍必须经过 WAES 注册、授权、发布流程。

### 17.1 VirtualFactory 示例

`VirtualFactory` 是 SupplyChain Profile 核心对象，用于描述由多个供应商、产线、仓库、物流节点和订单能力组成的虚拟化生产组织，必须映射 WAS 八维。

最小 JSON 示例：

```json
{
  "xwailVersion": "1.2.0-20260623",
  "modelType": "Scenario Instance Model",
  "status": "Draft",
  "profile": "SupplyChain Profile V1.0",
  "assetGroup": {
    "id": "vf-gc-001",
    "type": "VirtualFactory",
    "ontologyRef": "gc-ontology:supply-chain/VirtualFactory@0.2.x",
    "metadata": {
      "name": "GlobalCloud Virtual Factory Pilot",
      "owner": "gpc"
    },
    "dimensions": {
      "organization": {
        "operator": "gpc",
        "participants": ["factory-a", "factory-b", "warehouse-east", "logistics-node-01"]
      },
      "physical": {
        "realFactories": ["factory-a", "factory-b"],
        "warehouses": ["warehouse-east"],
        "logisticsNodes": ["logistics-node-01"]
      },
      "rule": {
        "orderAllocationPolicy": "policy-order-allocation-v1",
        "qualityPolicy": "policy-quality-v1"
      },
      "intellectual": {
        "processCapabilities": ["cutting", "assembly", "inspection"]
      },
      "data": {
        "factSources": ["GFIS", "GPC", "PVAOS"]
      },
      "economic": {
        "settlementModel": "alliance-settlement-v1"
      },
      "energy": {
        "greenCapabilityRequired": true
      },
      "spaceTime": {
        "serviceRegion": "CN-LN",
        "planningWindow": "P30D"
      }
    },
    "relations": [
      {"type": "composedOf", "targetRef": "factory-a"},
      {"type": "composedOf", "targetRef": "factory-b"},
      {"type": "dependsOn", "targetRef": "alliance-settlement-v1"}
    ],
    "flowRelations": [
      {"type": "InformationFlow", "event": "orderAllocated", "targetRef": "factory-a"},
      {"type": "ControlFlow", "event": "capacityConfirmed", "targetRef": "factory-b"},
      {"type": "LogisticsFlow", "event": "shipmentScheduled", "targetRef": "logistics-node-01"},
      {"type": "ValueFlow", "event": "settlementTriggered", "targetRef": "alliance-settlement-v1"}
    ]
  }
}
```

治理要求：

- `GPC` 负责编排订单、产能和协同事件；
- `GFIS` 提供工厂事实、质量事实、能耗事实；
- `PVAOS` 提供联盟、权益和结算关系；
- `WAES/WAE` 负责资产模型、状态、证据、账本和服务治理。

### 17.2 CarbonLedger 示例

`CarbonLedger` 采用“事实源分布、账本统一”原则：GFIS/GPC/PVAOS 产生事实，WAE 形成统一碳账本，WAES 负责治理与展示。

最小 JSON 示例：

```json
{
  "xwailVersion": "1.2.0-20260623",
  "modelType": "Scenario Instance Model",
  "status": "Draft",
  "profile": "SupplyChain Profile V1.0",
  "assetGroup": {
    "id": "carbon-ledger-001",
    "type": "CarbonLedger",
    "ontologyRef": "gc-ontology:supply-chain/CarbonLedger@0.2.x",
    "dimensions": {
      "organization": {
        "governedBy": "waes",
        "ledgerOwner": "wae"
      },
      "data": {
        "factSources": ["GFIS.energy", "GPC.delivery", "PVAOS.settlement"]
      },
      "economic": {
        "carbonAssetTypes": ["emission", "reduction", "quota", "credit", "certificate"]
      },
      "energy": {
        "scope": ["energyUse", "carbonEmission", "carbonReduction"]
      },
      "rule": {
        "certificationPolicy": "green-certification-policy-v1",
        "auditRequired": true
      }
    },
    "relations": [
      {"type": "aggregates", "targetRef": "factory-a"},
      {"type": "aggregates", "targetRef": "order-20260623-001"},
      {"type": "aggregates", "targetRef": "shipment-20260623-001"}
    ],
    "evidenceRequirement": {
      "required": true,
      "evidenceTypes": ["GreenEvidence", "Certification", "AuditRecord", "TraceProof"],
      "semanticFields": ["ontologyRef", "termVersion", "reasoningSource", "explanationRef"]
    },
    "compatibilityLevel": "Trusted"
  }
}
```

治理要求：

- 涉及碳账本、认证、审计、结算的模型必须达到 `Trusted`；
- 事实源可以分布，但 WAE 中的碳账本必须统一；
- 任何碳资产计量、归集或结算影响都必须生成 `EvidenceRecord`。

### 17.3 ServicePackage 示例

`ServicePackage` 是 WAES 的业务治理对象，AAAS 负责商业化优化、订阅、套餐、定价和计费。

最小 JSON 示例：

```json
{
  "xwailVersion": "1.2.0-20260623",
  "modelType": "Scenario Instance Model",
  "status": "Authorized",
  "servicePackage": {
    "id": "sp-virtual-factory-collaboration-v1",
    "name": "虚拟工厂协同服务包",
    "ontologyRef": "gc-ontology:service/VirtualFactoryCollaborationService@0.2.x",
    "boundModels": [
      {
        "modelRef": "vf-gc-001",
        "requiredStatus": "Authorized"
      },
      {
        "modelRef": "carbon-ledger-001",
        "requiredStatus": "Published",
        "requiredCompatibility": "Trusted"
      }
    ],
    "serviceScope": [
      "orderAllocation",
      "capacityConfirmation",
      "greenEvidenceCollection",
      "shipmentCoordination",
      "settlementTrigger"
    ],
    "metering": [
      {"unit": "ManagedScenario", "objectRef": "vf-gc-001"},
      {"unit": "ProcessedEvent", "eventTypes": ["orderAllocated", "capacityConfirmed", "greenEvidenceSubmitted"]},
      {"unit": "EvidenceRecord", "evidenceTypes": ["GreenEvidence", "AuditRecord"]}
    ],
    "sla": {
      "availability": "99.5%",
      "orderAllocationResponse": "PT30M",
      "evidenceDeliveryWindow": "P1D"
    },
    "evidenceRequirement": {
      "required": true,
      "minimumLevel": "Trusted"
    },
    "commercialBinding": {
      "managedBy": "AAAS",
      "plans": ["basic", "professional", "enterprise"]
    }
  }
}
```

治理要求：

- 商业发布只能绑定 `Published` 模型；
- 试运行可绑定 `Authorized` 模型；
- 内部测试可绑定 `Draft`，但不能商业发布；
- AAAS 可生成多个商业套餐，但不能绕过 WAES 的服务包运行治理。

### 17.4 完整绿色供应链综合示例

综合示例说明 `VirtualFactory`、`CarbonLedger`、`GreenEvidence`、`ServicePackage`、`Metering`、`SLA` 和 `EvidenceRequirement` 的组合关系。

XML 骨架示例：

```xml
<XWAIL version="1.2.0-20260623" modelType="Scenario Instance Model" status="Draft">
  <Profile ref="SupplyChain Profile V1.0"/>
  <AssetGroup id="vf-gc-001" type="VirtualFactory" ontologyRef="gc-ontology:supply-chain/VirtualFactory@0.2.x">
    <Dimensions>
      <OrganizationDimension operator="gpc" governedBy="waes"/>
      <PhysicalDimension factories="factory-a factory-b" warehouses="warehouse-east"/>
      <RuleDimension policyRef="policy-order-allocation-v1"/>
      <DataDimension factSources="GFIS GPC PVAOS"/>
      <EconomicDimension settlementModel="alliance-settlement-v1"/>
      <EnergyDimension greenCapabilityRequired="true"/>
      <SpaceTimeDimension serviceRegion="CN-LN" planningWindow="P30D"/>
    </Dimensions>
    <Relations>
      <Relation type="composedOf" targetRef="factory-a"/>
      <Relation type="composedOf" targetRef="factory-b"/>
      <Relation type="usesLedger" targetRef="carbon-ledger-001"/>
    </Relations>
    <FlowRelations>
      <Flow type="InformationFlow" event="orderAllocated" targetRef="factory-a"/>
      <Flow type="ControlFlow" event="capacityConfirmed" targetRef="factory-b"/>
      <Flow type="LogisticsFlow" event="shipmentScheduled" targetRef="logistics-node-01"/>
      <Flow type="ValueFlow" event="settlementTriggered" targetRef="alliance-settlement-v1"/>
    </FlowRelations>
  </AssetGroup>

  <AssetGroup id="carbon-ledger-001" type="CarbonLedger" ontologyRef="gc-ontology:supply-chain/CarbonLedger@0.2.x">
    <EvidenceRequirement required="true" minimumLevel="Trusted"/>
  </AssetGroup>

  <ServicePackage id="sp-green-supply-chain-v1" managedBy="WAES" commercialManagedBy="AAAS">
    <BoundModel ref="vf-gc-001" requiredStatus="Authorized"/>
    <BoundModel ref="carbon-ledger-001" requiredStatus="Published" requiredCompatibility="Trusted"/>
    <Metering unit="ManagedScenario" objectRef="vf-gc-001"/>
    <Metering unit="ProcessedEvent" eventTypes="orderAllocated capacityConfirmed greenEvidenceSubmitted"/>
    <SLA availability="99.5%" evidenceDeliveryWindow="P1D"/>
  </ServicePackage>
</XWAIL>
```

综合治理规则：

- `GFIS` 负责工厂执行事实和绿色事实；
- `GPC` 负责订单、供需、物流、交易协同和虚拟工厂编排；
- `PVAOS` 负责联盟运营、权益、结算、服务订阅和价值分配；
- `WAE` 负责统一资产主账、状态事件、关系图谱、碳账本和计量记录；
- `WAES` 负责模型注册、授权、发布、服务包治理、证据完整性和运行健康；
- `AAAS` 负责商业套餐、订阅、通用订阅治理和商业计费联动；
- `Brain` 可读取模型、证据和 Ontology 进行分析，但不能绕过 WAES 修改正式模型。

## 18. 附录

附录应包括完整错误码表、XML Schema、JSON Schema、Policy 规则样例、SupplyChain Profile 分阶段对象表、WAES 发布表单、AAAS 服务包绑定清单和迁移模板。

附录还应包括 `Ontology Term -> XWAIL Object/Field/Profile` 映射表、`ontologyRef` 字段规范、Ontology-aware Validator 规则样例和可信推理 EvidenceRecord 样例。

本草案只固化本轮问答确认的 V1.2 最小可行规范结构，不声明规范已完成发布。
