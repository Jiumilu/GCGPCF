---
doc_id: GPCF-DOC-038B869EBF
title: GlobalCloud 底座可用知识闭环率计算样表与字段字典
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md
source_path: 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 底座可用知识闭环率计算样表与字段字典

日期：2026-06-17  
状态：`calculation_template_controlled`  
适用范围：葛化、湖北磷材、后续工厂复制线、区域绿色供应链运营单位

## 1. 定位

本文承接 DKS-040《GlobalCloud 湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练》，把“底座可用知识闭环率”固化为可复用字段字典、计算样表、证据要求和一票否决规则。

本文是治理计算模板，不是业务完成记录，不是收入确认记录，不是订单确认记录，不是项目验收记录，不是 RAG 准入结果，不是指挥舱强引用许可，也不是 GFIS、GPC、PVAOS、WAES 或 KDS 真实 API 写入记录。

## 2. 指标公式

```text
底座可用知识闭环率 =
状态覆盖率 x 20%
+ 事实成熟度 DQ x 25%
+ 来源/证据合格率 x 20%
+ registry/台账/报告一致性 x 15%
+ 自动化处理有效率 x 10%
+ 写回缺口闭环率 x 10%
```

计算结果只用于判断一条底座知识数据是否具备可治理、可追溯、可有限调用、可补缺口的能力。它不能替代人工确认、WAES 规则、委员会裁决或业务主账。

## 3. 字段字典

| field | 类型 | 取值范围 | 权重 | 字段说明 | 最低证据要求 | 不得用于 |
|---|---|---:|---:|---|---|---|
| `baseKnowledgeId` | string | 受控编号 | - | 底座知识对象编号 | KDS 11 池或增强账本挂接记录 | 替代业务主键 |
| `sourceProject` | enum | GFIS / 湖北磷材 / 葛化 / 其他 | - | 数据来源项目或单位 | 项目登记或任务包来源 | 证明项目完成 |
| `kdsPoolRefs` | list | KDS 11 池 | - | 至少挂接一个底座池 | 池挂接表 | 让增强账本游离 |
| `enhancedLedgerRefs` | list | 积分池 / 收益池 / 额度池 / 悬赏池 / 争议池 / 潜在产值池 / SOP 账本 / 贡献账本 | - | 增强账本挂接 | 必须挂接到 KDS 11 池 | 替代 KDS 11 池 |
| `statusCoverageRate` | number | 0-100 | 20% | 是否完成入池和状态位覆盖 | 状态字段、台账行、池挂接 | 证明事实已确认 |
| `dqScore` | number | 0-100 | 25% | 事实成熟度评分 | DQ 评分、字段完整性、核验记录 | 替代人工核验 |
| `evidencePassRate` | number | 0-100 | 20% | 来源、证据、脱敏、权限是否合格 | source_refs、证据等级、脱敏记录 | 证明合同、金额或收入 |
| `consistencyRate` | number | 0-100 | 15% | registry、台账、报告、页面之间是否一致 | registry、台账、报告交叉检查 | 覆盖冲突事实 |
| `automationEffectivenessRate` | number | 0-100 | 10% | 自动回读、自动补证、自动提示是否有效 | 自动化运行记录、dry-run 或门禁结果 | 自动关闭缺口 |
| `writebackClosureRate` | number | 0-100 | 10% | 缺口是否被补齐、关闭或明确不适用 | 写回记录、人工确认、不适用说明 | 由 AI 自动关闭 |
| `calculatedClosureRate` | number | 0-100 | 100% | 加权计算结果 | 六维评分明细 | 直接发布或入账 |
| `oneVoteVetoFlags` | list | 见第 6 节 | - | 一票否决项 | 证据检查或人工复核 | 被分数抵消 |
| `decisionBand` | enum | safe_reuse_candidate / limited_report_candidate / repair_candidate / return_for_source / blocked_or_invalid | - | 按分数和否决项形成的判定 | 计算记录和边界说明 | 自动发布 |
| `allowedUse` | list | candidate / limited_report / repair / blocked | - | 允许用途 | 判定说明 | 越权调用 |
| `forbiddenUse` | list | 自定义 | - | 明确禁止用途 | 红线规则 | 绕过治理 |

## 4. 六维评分口径

| 维度 | 100 分条件 | 70 分条件 | 50 分条件 | 0 分条件 |
|---|---|---|---|---|
| 状态覆盖率 | 已入池、状态位齐备、责任状态明确 | 已入池但部分状态待补 | 有候选但未完整入池 | 无池挂接或无状态 |
| 事实成熟度 DQ | 字段齐备、事实经来源或人工确认 | 主要字段齐备但仍有待核验项 | 字段缺口明显，只能作候选 | 事实来源不可用或明显错误 |
| 来源/证据合格率 | source_refs、证据等级、脱敏和权限齐备 | 来源基本齐备但证据等级或权限待补 | 来源摘要存在但不可追溯 | 无来源、来源失效或敏感越界 |
| registry/台账/报告一致性 | registry、台账、报告、页面一致 | 小差异可解释且不影响判断 | 存在冲突，需修复后再用 | 状态冲突且无法解释 |
| 自动化处理有效率 | 自动回读、检查、提示和记录均有效 | 有 dry-run 或局部自动提示 | 只有人工记录，无自动处理证据 | 自动化缺失或误处理 |
| 写回缺口闭环率 | 缺口已补齐、关闭或明确不适用 | 关键缺口已处理，次要缺口待补 | 缺口已识别但未关闭 | 缺口未识别或被误关闭 |

## 5. 判定分层

| calculatedClosureRate | decisionBand | 允许动作 | 必须提示 | 禁止动作 |
|---:|---|---|---|---|
| 85-100 | `safe_reuse_candidate` | 可进入人工发布前复核和受控知识复用候选 | 仍需确认是否满足 RAG 或经营强引用门禁 | 自动发布、自动写主账、自动结算 |
| 70-84 | `limited_report_candidate` | 可进入有限报告候选 | 必须显示待确认、置信度或适用边界 | RAG 强引用、经营强引用 |
| 60-69 | `repair_candidate` | 可生成补源、悬赏候选、人工确认任务 | 必须登记缺口和责任方 | 关闭缺口、确认事实 |
| 50-59 | `return_for_source` | 退回补源或补责任主体 | 必须说明退回原因 | 进入报告、RAG、主账 |
| 0-49 | `blocked_or_invalid` | 阻断、退回或触发违规评议候选 | 必须说明硬停止或否决项 | 进入任何业务链路 |

一票否决项优先于分数。出现一票否决时，`decisionBand` 必须降为 `blocked_or_invalid` 或对应硬停止状态。

## 6. 一票否决规则

| vetoCode | 触发条件 | 处理 |
|---|---|---|
| `VETO-NO-SOURCE` | 当前判断没有来源 | 阻断，退回补源 |
| `VETO-AI-AS-FACT` | AI 推测被写成事实 | 阻断，标记污染风险 |
| `VETO-REVENUE-MISCLAIM` | 开票、线索、潜在产值被写成到账收入 | 阻断，触发委员会候选 |
| `VETO-ORDER-MISCLAIM` | 线索或会议摘要被写成正式订单 | 阻断，退回并记录违规候选 |
| `VETO-LEDGER-ORPHAN` | 增强账本未挂接 KDS 11 池 | 阻断，补挂接 |
| `VETO-SENSITIVE-LEAK` | 合同金额、账号、签章、客户实名等敏感内容越界 | 阻断，脱敏和权限复核 |
| `VETO-REGISTRY-CONFLICT` | registry 与项目页、台账或报告状态冲突 | 阻断，先修复一致性 |
| `VETO-WAes-OVERWRITE` | 把 WAES 规则记录写成业务主账 | 阻断，恢复为规则记录 |
| `VETO-KDS-API-CLAIM` | 把 KDS 本地镜像写成真实 KDS API 同步 | 阻断，改回 `pending_api` 或真实审计流水 |
| `VETO-UNAUTHORIZED-SETTLEMENT` | 未经确认结算积分、收益或 AI 额度 | 阻断，触发争议或违规候选 |

## 7. 计算样表

| baseKnowledgeId | sourceProject | kdsPoolRefs | enhancedLedgerRefs | statusCoverageRate | dqScore | evidencePassRate | consistencyRate | automationEffectivenessRate | writebackClosureRate | oneVoteVetoFlags | calculatedClosureRate | decisionBand |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| `BKC-HBLC-FEA-202606-0001` | 湖北磷材 | 装备池 / 产能池 / 政策池 / 数据池 / 场景池 | 贡献账本 / SOP 账本 / 悬赏池 | 100 | 65 | 60 | 80 | 0 | 30 | none | 63.25 | `repair_candidate` |
| `BKC-HBLC-IND-202606-0001` | 湖北磷材 | 政策池 / 数据池 / 场景池 | 贡献账本 / 悬赏池 | 100 | 82 | 90 | 85 | 0 | 40 | none | 75.25 | `limited_report_candidate` |
| `BKC-HBLC-ORD-202606-0001` | 湖北磷材 | 订单池 / 产能池 / 资金池 / 数据池 | 潜在产值池 / 贡献账本 / 悬赏池 | 100 | 45 | 35 | 50 | 0 | 20 | `VETO-NO-SOURCE` | 47.75 | `blocked_or_invalid` |
| `BKC-HBLC-ORD-202606-0002` | 湖北磷材 | 订单池 / 资金池 / 场景池 | 潜在产值池 / 争议池 / 贡献账本 | 100 | 30 | 20 | 20 | 0 | 0 | `VETO-REVENUE-MISCLAIM` | 34.50 | `blocked_or_invalid` |
| `BKC-GH-FIS-202606-0001` | 葛化 | 订单池 / 产能池 / 数据池 / 场景池 | SOP 账本 / 贡献账本 | 100 | 55 | 55 | 70 | 20 | 25 | none | 61.25 | `repair_candidate` |

## 8. 计算伪代码

```text
if oneVoteVetoFlags is not empty:
  decisionBand = blocked_or_invalid
else:
  calculatedClosureRate =
    statusCoverageRate * 0.20
    + dqScore * 0.25
    + evidencePassRate * 0.20
    + consistencyRate * 0.15
    + automationEffectivenessRate * 0.10
    + writebackClosureRate * 0.10

  decisionBand = score_to_band(calculatedClosureRate)
```

任何计算结果都必须保留六维明细、来源、证据等级、否决项和人工确认状态，不得只保留总分。

## 9. RAG 与指挥舱调用门禁

| decisionBand | RAG 强引用 | 有限报告 | 指挥舱强引用 | 说明 |
|---|---|---|---|---|
| `safe_reuse_candidate` | 需另行满足 RAG 准入 | candidate | 需另行满足经营强引用门禁 | 总分高也不自动准入 |
| `limited_report_candidate` | no | candidate | no | 只能有限报告，必须显示边界 |
| `repair_candidate` | no | no | no | 只可触发补源、悬赏候选或人工确认 |
| `return_for_source` | no | no | no | 退回补源 |
| `blocked_or_invalid` | no | no | no | 阻断或违规候选 |

## 10. 适用到葛化与湖北磷材

| 单位 | 首批适用对象 | 评分重点 | 边界 |
|---|---|---|---|
| 葛化 | GFIS 知识问答、GFIS 使用、GFIS 文档验收、建设和订单运行母版 | 来源证据、GFIS 主账边界、预运营期订单、质量/发货/POD/金融凭证门禁 | 不把候选事实写成 GFIS 主账，不把预运营期订单写成已到账收入 |
| 湖北磷材 | 拓厂项目知识库、原料/行业/订单知识库、新工厂复制模板 | 拓厂来源、行业权威来源、订单线索收益边界、缺口悬赏 | 不做 GFIS 深度，不把线索写成正式订单或收入 |
| 后续工厂复制线 | 新工厂复制模板、区域绿色供应链运营知识库 | KDS 11 池挂接、SOP 复用、缺口闭环、贡献积分候选 | 必须先复用母版，再按项目差异补证 |

## 11. 输出对象建议

| 输出对象 | 作用 | 生成条件 | 状态边界 |
|---|---|---|---|
| `BaseKnowledgeClosureScore` | 保存六维计算结果 | 有完整评分字段 | candidate_only |
| `KnowledgeGapWritebackCandidate` | 指出缺口写回位置 | 任一维度低于 70 或出现待补字段 | candidate_only |
| `BountyPreparationCandidate` | 准备悬赏草案 | 缺口可由合作单位或个人补齐 | 未确认前不发布 |
| `CommitteeReviewCandidate` | 进入委员会候选 | 收益、权属、重大违规或跨单位争议 | 不替代裁决 |
| `RagAdmissionCandidate` | RAG 准入候选 | 总分高且无否决项 | 仍需 RAG 独立门禁 |

## 12. 完成定义

本文完成条件：

1. 六个评分字段均有字段定义、取值范围、权重和证据要求。
2. 一票否决规则覆盖来源、AI 事实污染、收入误认、订单误认、账本游离、敏感越界、registry 冲突、WAES 主账误写、KDS API 误认和未授权结算。
3. 计算样表覆盖湖北磷材拓厂、行业、订单和葛化 GFIS 候选。
4. 明确 RAG、有限报告和指挥舱强引用边界。
5. 明确该指标为治理与调用可用性指标，不替代业务事实。
6. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 13. DKS-042 建议

下一轮建议建立“底座可用知识闭环率评分脚本 dry-run 规格”，把本文字段字典转成可机器校验的 JSON schema、示例输入、示例输出和 hard-stop 断言；仍只做 dry-run，不写真实 KDS API、不关闭缺口、不发布悬赏。
