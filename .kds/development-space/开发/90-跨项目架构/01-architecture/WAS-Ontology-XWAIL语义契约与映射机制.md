---
doc_id: GPCF-DOC-WAS-ONTOLOGY-XWAIL-MAPPING-20260623
title: WAS-Ontology-XWAIL 语义契约与映射机制
project: GPCF
related_projects: [GPCF, GFIS, GPC, PVAOS, WAES, KDS, Brain, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/WAS-Ontology-XWAIL语义契约与映射机制.md
source_path: 01-architecture/WAS-Ontology-XWAIL语义契约与映射机制.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# WAS-Ontology-XWAIL 语义契约与映射机制

## 1. 定位

WAS、XWAIL、Ontology 都服务于把现实世界对象结构化为可理解、可治理、可计算的资产模型，但三者层级不同：

```text
WAS 定义体系。
Ontology 定义语义。
XWAIL 定义契约。
```

Ontology 正式定位为 WAS 的语义知识层，不是独立于 WAS 的另一套顶层体系，不替代 XWAIL，也不替代 GFIS、GPC、PVAOS 等真实业务事实源。

## 2. 三者关系

| 项 | WAS | Ontology | XWAIL |
|---|---|---|---|
| 核心定位 | 顶层体系与资产世界观 | 语义本体、概念关系、知识图谱基础 | 规范性建模语言与机器契约 |
| 回答问题 | 什么是资产，资产如何分类、流动、演化、治理 | 概念之间是什么关系，机器如何理解资产语义 | 如何把资产写成可验证、可交换、可运行的模型 |
| 抽象层级 | 最高层 | 语义知识层 | 工程表达层 |
| 主要对象 | 三层资产、八维、八流、生命周期、治理原则 | 类、属性、关系、约束、推理规则、词表、本体图谱 | AssetGroup、AssetUnit、Dimensions、Relations、FlowRelations、StateMachine、Policy |
| 使用者 | 架构、产品、治理、商业设计 | Brain、KDS、知识图谱、语义检索、推理系统 | 平台、验证器、WAES/WAE、Studio、AAAS |
| 主要价值 | 保证方向一致 | 保证语义一致 | 保证模型一致 |

协同链路：

```text
WAS
定义资产世界的顶层语义和治理框架
  ↓
Ontology
沉淀概念、词表、关系、语义规则和推理结构
  ↔
XWAIL
把资产、关系、流程、状态、策略、证据写成机器契约
  ↓
WAE / WAES
注册、运行、治理、发布和服务化运营
```

## 3. Ontology 到 XWAIL 映射表

必须建立 `Ontology Term -> XWAIL Object/Field/Profile` 映射表。第一阶段以 SupplyChain Profile 为主。

| Ontology Term | 语义说明 | XWAIL Object | XWAIL Field/Profile | 备注 |
|---|---|---|---|---|
| `Asset` | 可识别、可治理、可计算的资产对象 | `AssetGroup` / `AssetUnit` | `modelType`、`assetType` | 对应 WAS 资产总概念 |
| `Enterprise` | 供应链企业主体 | `AssetUnit` | `SupplyChain Profile / Enterprise` | 组织维核心对象 |
| `Factory` | 实体工厂 | `AssetGroup` | `SupplyChain Profile / Factory` | GFIS 主要事实源 |
| `VirtualFactory` | 多主体协同形成的虚拟化生产组织 | `AssetGroup` | `SupplyChain Profile / VirtualFactory` | GPC 负责编排，GFIS/PVAOS 提供事实 |
| `Order` | 订单与履约对象 | `AssetUnit` / `FlowRelations` | `SupplyChain Profile / Order` | 触发物流、结算、绿色证据归集 |
| `CarbonAsset` | 碳排放、减排、配额、信用、证书等资产 | `AssetUnit` | `SupplyChain Profile / CarbonAsset` | 必须达到 Trusted 场景要求 |
| `CarbonLedger` | 统一碳账本 | `AssetGroup` / `ServicePackage` | `SupplyChain Profile / CarbonLedger` | 事实源分布、账本统一 |
| `GreenEvidence` | 绿色事实、认证材料、审计、检测、溯源证明 | `EvidenceRequirement` / `EvidenceRecord` | `SupplyChain Profile / GreenEvidence` | 绑定 `ontologyRef` 和来源记录 |
| `ServicePackage` | 可服务化运营的能力包 | `ServicePackage` | `serviceScope`、`metering`、`sla` | WAES 治理，AAAS 商业优化 |

## 4. XWAIL 回指 Ontology

所有 XWAIL 核心对象均可选绑定 `ontologyRef`。该字段用于回指 Ontology 术语、概念、关系或推理规则。

建议字段：

```text
ontologyRef / termVersion / ontologyNamespace / semanticRelation / mappingConfidence
```

`ontologyRef` 的作用是让 XWAIL 模型对象不成为孤立工程字段。它不替代 XWAIL Schema，不替代业务事实源，也不代表推理结果自动可信。

## 5. 版本兼容矩阵

必须维护三者版本兼容矩阵：

| WAS version | Ontology version | XWAIL version | SupplyChain Profile version | 兼容性 | 迁移要求 |
|---|---|---|---|---|---|
| 1.1.0 | 0.2.x | 1.2.0-20260623 | 1.0 | compatible | 需要补充 `ontologyRef` 和 EvidenceRecord 语义来源字段 |

版本矩阵用于判断模型、Profile、验证器、推理规则和运行时绑定是否可共同发布。若 Ontology 术语或推理规则发生破坏性变更，相关 XWAIL Profile 必须触发 Migration。

## 6. Ontology-aware Validator

新增 `Ontology-aware Validator`，用于校验 XWAIL 模型的语义合理性。校验范围包括：

- `ontologyRef` 有效性；
- 术语版本；
- 上下位关系；
- 字段语义匹配；
- Profile 映射；
- 推理规则适用性。

Ontology-aware Validator 不替代 Schema Validator、Policy Validator 或 Business Validator。它负责语义一致性，其他验证器分别负责结构、策略和业务发布条件。

## 7. 可信推理写入规则

推理结果状态固定为：

```text
Candidate / Verified / Trusted / Rejected
```

只有 `Verified` 和 `Trusted` 推理结果可以进入 WAE。`Trusted` 推理必须满足：

- 证据完整；
- 来源可信；
- 规则通过；
- 置信度达标；
- WAES 授权；
- 可审计；
- 可回滚。

可信推理写入 WAE 必须经过 WAES 策略授权，并绑定原始证据或来源记录。Brain 只能读取正式 Ontology、XWAIL、WAE 数据，不能绕过 WAES 修改正式模型。

写入失败必须生成：

- `PolicyViolation`
- 带 reasoning 详情的 `EvidenceRecord`

不新增独立 `ReasoningRecord` 运行时对象。

## 8. EvidenceRecord 语义来源

`EvidenceRecord` 必须支持以下语义来源字段：

```text
ontologyRef / termVersion / reasoningSource / explanationRef
```

这些字段用于解释证据与 Ontology 术语、推理规则和解释依据之间的关系。它们不等同于业务事实源；真实事实仍必须来自 GFIS、GPC、PVAOS 等系统或经 WAES 授权的可信推理链。

## 9. Brain 写入边界

Brain 可以读取 Ontology、XWAIL、WAE 数据，提供知识问答、规则解释、异常分析、决策建议和高级工作台能力。Brain 不能绕过 WAES 直接修改正式 Ontology、XWAIL 或 WAE 主账。

Brain 可提交变更建议或推理结果，但写入必须经过 WAES 授权策略、证据绑定、验证器检查和审计记录。

## 10. Hard-stop

以下情况不得写入正式 WAE 主账：

| 条件 | 结果 |
|---|---|
| 推理结果仍为 `Candidate` 或 `Rejected` | 阻断 |
| 缺原始证据或来源记录 | 阻断 |
| 未通过 WAES 策略授权 | 阻断 |
| `ontologyRef` 无效或术语版本不兼容 | 阻断 |
| 置信度、规则或解释依据不满足 Trusted 要求 | 阻断 |
| Brain 试图绕过 WAES 直接写入 | 阻断 |

本文件只定义语义契约和映射机制，不声明 Ontology、XWAIL 或 WAE 的生产写入能力已经完成。
