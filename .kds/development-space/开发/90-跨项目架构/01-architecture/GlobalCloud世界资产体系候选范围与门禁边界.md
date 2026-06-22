---
doc_id: GPCF-DOC-45A09FDDC2
title: GlobalCloud世界资产体系候选范围与门禁边界
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud世界资产体系候选范围与门禁边界.md
source_path: 01-architecture/GlobalCloud世界资产体系候选范围与门禁边界.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud世界资产体系候选范围与门禁边界

## 1. 定位

WAS（世界资产体系）当前是候选架构对象，不是已验收项目、不是业务主账、不是 WAES 的别名，也不是新的生产写入入口。

本文件用于把 WAS 纳入 GlobalCloud Loop Engineering 的可讨论范围，先定义边界、证据来源、门禁路径和禁止动作。后续只有在用户确认后，才进入实施方案、任务拆解、文档台账同步或项目群状态矩阵更新。

## 2. 成功标准

本轮成功只到以下范围：

| 项 | 标准 |
|---|---|
| 候选对象命名 | 明确 WAS 是候选体系，不自动并入 WAES、GFIS、GPC 或 PVAOS |
| 主账边界 | 明确业务事实仍归 GFIS、GPC、PVAOS 等业务系统 |
| 治理边界 | 明确 WAES/Harness 只做门禁、证据、风险和状态裁决 |
| 知识边界 | 明确 KDS/Brain 只承载知识、索引、引用和分析，不产生 accepted fact |
| 安全边界 | 明确本轮不写生产、不写真实 KDS/WAES、不调用外部 API、不升级状态 |

本轮不追求 `accepted`、`integrated`、`production_ready` 或真实业务闭环完成。

## 3. 分层边界

| 层 | WAS 候选角色 | 当前主责系统 | 禁止替代 |
|---|---|---|---|
| 资产事实层 | 资产对象的跨域归类、统一编号候选、关系视图候选 | GFIS、GPC、PVAOS | 不替代业务主账和 source-of-record |
| 资产知识层 | 资产定义、证据说明、引用关系、可信等级 | KDS、Brain | 不替代真实业务事实和人工验收 |
| 资产治理层 | 门禁候选、风险信号、证据完整性检查 | WAES、Harness | 不直接生成正式 WAES Gate Result |
| 资产编排层 | Loop 输入、候选任务、验证路径、回滚要求 | GPCF | 不自动改状态矩阵或验收结论 |
| 资产使用层 | 可读查询、分析建议、对象关系解释 | 项目群用户界面和 AI 助手 | 不直接写业务系统 |

## 4. 候选对象类型

WAS 的候选对象应先限制在只读建模范围：

| 对象类型 | 示例 | 最低来源要求 |
|---|---|---|
| business_asset | 客户、订单、合同、样品、工单、批次、交付、POD | 业务系统 source-of-record 或正式确认文件 |
| knowledge_asset | SOP、规格、标准、政策、培训资料、受控说明 | KDS 受控文档、版本、来源和引用路径 |
| evidence_asset | 测试结果、人工复核、WAES gate 候选、Harness evidence | evidence 文件、validator 输出、审计记录 |
| relation_asset | 客户到订单、订单到工单、工单到批次、批次到交付 | 双端对象均可追溯，关系来源可解释 |
| risk_asset | 权限、敏感、收益、争议、污染、外部共享风险 | WAES precheck 或人工风险记录 |

任何 AI 摘要、用户口述、KDS 候选、测试数据、mock、fixture、Demo 输出，都只能作为候选线索，不能直接成为 WAS accepted asset。

## 5. Gate 输入

每个 WAS 候选对象进入下一步前，至少需要以下字段：

| 字段 | 含义 |
|---|---|
| `wasCandidateId` | 候选对象编号 |
| `assetType` | 候选对象类型 |
| `owningSystem` | 当前事实主责系统 |
| `sourceRefs` | 来源引用 |
| `evidenceRefs` | 证据引用 |
| `kdsRefs` | KDS 受控文档或知识引用 |
| `waesGateRefs` | WAES precheck 或正式 gate 引用 |
| `aclRefs` | 权限、租户、可见性边界 |
| `riskSignals` | 风险信号 |
| `requestedOperation` | 只读、建模、引用、写回候选等操作 |
| `dryRun` | 初期必须为 true |

## 6. Gate 输出

WAS 候选门禁只能输出候选结论：

| 字段 | 允许值 |
|---|---|
| `candidateStatus` | `candidate` / `repair_required` / `blocked` / `human_required` / `committee_required` / `metadata_only` |
| `allowedOperations` | `read_only` / `model_only` / `cite_only` / `precheck_only` |
| `requiredActions` | 补来源、补 evidence、补 owner confirmation、补 WAES precheck、人工复核 |
| `nextLoopInput` | 下一轮可执行输入 |
| `writesBusinessSystem` | 初期必须为 false |
| `writesKdsFact` | 初期必须为 false |
| `writesWaesGateResult` | 初期必须为 false |
| `createsAcceptedAsset` | 初期必须为 false |

## 7. Hard-stop

以下任一情况出现时，WAS 候选对象必须保持 blocked 或 repair_required：

| 条件 | 结果 |
|---|---|
| 缺 source-of-record | blocked |
| 缺 evidence | repair_required |
| 仅 AI/LLM 候选 | metadata_only |
| ACL 或租户边界不明 | blocked |
| 敏感原文未脱敏 | blocked |
| 业务负责人确认缺失 | human_required |
| 收益、积分、额度、悬赏或贡献归因存在争议 | committee_required |
| 与 GFIS/GPC/PVAOS 主账冲突 | blocked |
| 企图绕过 WAES/Harness 状态裁决 | blocked |

## 8. 与现有项目的关系

| 项目 | 与 WAS 的关系 |
|---|---|
| GFIS | 工厂执行事实和运行层主账来源；WAS 只能引用，不替代 |
| GPC | 公共服务平台业务入口和协作事实来源；WAS 只能建模候选关系 |
| PVAOS | 平台运营、门户、租户和运营对象来源；WAS 只能读取边界内对象 |
| WAES | 治理、证据、风险和状态门禁；WAS 不能把 precheck 写成正式裁决 |
| KDS | 受控知识主存；WAS 只能引用受控路径和摘要，不写 accepted fact |
| Brain | 知识编制和分析界面；WAS 不能把分析输出写成主账事实 |
| GPCF | 编排、文档治理和 Loop 记录；WAS 状态升级仍受项目群门禁约束 |

## 9. 当前不可做

本候选范围不授权：

- 新增生产系统；
- 写入真实 KDS、WAES、GFIS、GPC、PVAOS 或外部 API；
- 创建正式 WAES Gate Result；
- 创建 accepted asset；
- 修改项目群状态矩阵；
- 改写 GFIS/GPC/PVAOS 主账职责；
- 将测试数据、mock、fixture、Demo、用户口述或 AI 摘要升级为真实业务事实；
- 标记 `accepted`、`integrated` 或 `production_ready`。

## 10. 下一轮输入

建议下一轮以 L1 文档治理模式继续，但需用户确认：

```text
输入：确认 WAS 是否作为 GlobalCloud 项目群候选跨域资产模型继续推进。
动作：建立 WAS 候选对象字段契约、负例污染门禁和本地 no-write validator。
输出：WAS candidate schema、negative fixture、validator、Loop round evidence。
检查：document pollution、KDS token、loop document gate、no-write assertions。
反馈：若 validator 通过，进入 L2 dry-run；若缺少业务样本，保持 draft/repair_required。
```

本文件本身不构成实施完成、业务完成或状态升级依据。
