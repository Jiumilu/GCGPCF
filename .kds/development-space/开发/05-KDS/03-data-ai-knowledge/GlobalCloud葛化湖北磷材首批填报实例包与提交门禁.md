---
doc_id: GPCF-DOC-6298DD1B0D
title: GlobalCloud 葛化湖北磷材首批填报实例包与提交门禁
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化湖北磷材首批填报实例包与提交门禁

状态：`GPCF-KDS-DKS-022` 受控实例包  
日期：2026-06-17  
适用范围：葛化物流首批资料填报、湖北磷材首批拓厂与知识源填报、MMC 首批参数备案、KDS 11 个底座资源池、增强治理账本、WAES 规则门禁、GPCF LOOP evidence。

## 1. 定位

本文是 `GPCF-KDS-DKS-022` 的正式交付，用于把 `GPCF-KDS-DKS-021` 的样本表进一步转成首批可提交的候选实例包和提交门禁。

本文只建立候选实例骨架、必填字段、阻断条件和提交流程。本文不填写真正客户、供应商、价格、订单、POD、到账、金融凭证、个人隐私或生产数据；不代表真实资料已提交，不代表真实 GFIS / GCFIS 主账已写入，不代表真实 KDS API 已同步，不代表积分、收益、额度、悬赏、争议或参数已经确认生效。

## 2. 提交总原则

1. 所有实例必须先进入 `candidate` 或 `draft`，不得直接进入 `confirmed`、`allocated`、`active` 或 `accepted_for_pilot`。
2. 所有实例必须至少挂接一个 KDS 11 底座资源池，并显式列出增强治理账本链接。
3. 真实来源未提交前，`sourceRefs` 必须填 `TBD` 或受控占位，不得伪造来源。
4. DSR-L3 资料默认只提交元数据索引，不进入普通 AI 问答。
5. AI 只能生成候选事实、候选 SOP、候选积分和候选写回建议。
6. WAES 只确认规则、证据、权限、边界和例外，不替代业务主账确认。
7. 用户保留治理权、急停权和规则治理权；委员会负责积分、收益、悬赏、争议和重大违规裁决。

## 3. 统一提交流程

```text
instance_skeleton
  -> candidate_filled
  -> source_refs_attached
  -> redaction_checked
  -> kds_candidate_registered
  -> waes_rule_checked
  -> human_review_pending
```

阻断分支：

```text
returned_for_evidence
  blocked_by_classification
  blocked_by_source_gap
  blocked_by_overreach
  disputed
  withdrawn
```

| 门禁 | 通过条件 | 阻断条件 |
|---|---|---|
| 来源门禁 | 来源类型、来源责任主体、时间和索引可追溯 | 来源为空却声明事实成立 |
| 密级门禁 | DSR-L2 / DSR-L3 已脱敏或只留元数据 | 敏感原文进入普通问答或共享正文 |
| 事实责任门禁 | 目标工厂与 OEM 承接方责任已区分 | 把 OEM 承接事实写成目标工厂已投产事实 |
| 收益门禁 | 到账证据存在后才进入正式收入口径 | 只有报价、开票或线索却写成正式收益 |
| 积分门禁 | 候选积分和确认积分分离 | AI 自动确认积分或兑换额度 |
| 参数门禁 | 参数变更有版本、理由、责任主体和备案要求 | 无备案直接 active |

## 4. 葛化首批候选实例

### 4.1 预运营期订单候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| instanceId | `GHI-GH-ORD-202606-0001` | 本实例编号 |
| sourceSampleRef | `GHS-KPK-GH-ORD-202606-0001` | 来自 DKS-021 样本位 |
| packageId | `KPK-GH-ORD-202606-0001` | 订单资料包 |
| sourceRefs | `TBD` | 电话、会议、邮件、平台线索或合作单位文件索引，未提交前不得补造 |
| sourceParty | `TBD` | 需求来源责任主体 |
| targetFactory | 葛化目标工厂 | 只表示目标工厂场景 |
| executionParty | `TBD` | 若由 OEM 承接，必须填承接方 |
| responsibilitySplit | unknown | 填报后必须改为 target_factory / oem_party / shared |
| classificationLevel | DSR-L2 | 客户、价格、规格、金额等敏感项需脱敏 |
| redactionLevel | partial | 普通问答只使用脱敏摘要 |
| kdsBasePools | 订单池、资金池、数据池、场景池 | 必挂 |
| enhancedLedgerLinks | 潜在产值池、贡献账本、SOP 账本、争议池 | 候选链接 |
| confirmationStatus | candidate | 不得直接确认 |
| waesGateStatus | pending | 待 WAES 规则记录 |
| forbiddenClaims | 正式订单、到账、收益、质量放行 | 明确禁止 |

### 4.2 辽宁远航链路补证候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| instanceId | `GHI-GH-LY-202606-0001` | 本实例编号 |
| sourceSampleRef | `GHS-KPK-GH-LY-202606-0001` | 来自 DKS-021 样本位 |
| packageId | `KPK-GH-LY-202606-0001` | 辽宁远航链路资料包 |
| sourceRefs | `TBD` | 报价、样箱、反馈、合同链或回执索引 |
| missingEvidence | 客户确认、样箱反馈、POD 或回执待确认 | 只能作为缺口，不得写成已收到 |
| kdsBasePools | 订单池、运力池、资金池、数据池、场景池 | 必挂 |
| enhancedLedgerLinks | 悬赏池、潜在产值池、贡献账本、争议池 | 候选链接 |
| knowledgeGapCandidate | `KGR-GH-EVD-202606-0001` | 可进入知识缺口候选 |
| bountyCandidate | `KGB-GH-EVD-202606-0001` | 可进入悬赏候选，不等于已发布 |
| confirmationStatus | candidate | 待补证 |
| waesGateStatus | pending | 待规则检查 |

### 4.3 GFIS AI 评分候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| scoreRecordId | `GSR-GH-KQA-202606-0001` | 首批问答评分候选 |
| sampleId | `KQA-GH-ORD-001` | 问题：电话需求如何进入预运营期订单候选 |
| inputSummary | `TBD` | 只填脱敏输入摘要 |
| assistantOutputSummary | `TBD` | 只填 AI 输出摘要 |
| sourceCitationScore | blank | 0-20，待人工评分 |
| factLayerScore | blank | 0-20，待人工评分 |
| gateAwarenessScore | blank | 0-20，待人工评分 |
| actionabilityScore | blank | 0-20，待人工评分 |
| overreachControlScore | blank | 0-20，待人工评分 |
| totalScore | blank | 不得预填通过 |
| hardFailReason | none / TBD | 如越权则直接 hard_fail |
| reviewStatus | draft | 不得写 accepted_for_pilot |
| waesGateRefs | pending | 待 WAES 或项目负责人复核 |

## 5. 湖北磷材首批候选实例

### 5.1 拓厂项目来源候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| assessmentRecordId | `FEA-HBLC-202606-0001` | 拓厂项目来源评估 |
| packageId | `KPK-HBLC-FEA-202606-0001` | 拓厂项目资料包 |
| expansionProjectRef | `TBD` | 目标区域或项目来源索引 |
| ghTemplateVersion | `GH-DKS-021` | 复用葛化母版结构，不复用未确认事实 |
| sourceRefs | `TBD` | 电话、会议、邮件、合作单位文件或第三方资料索引 |
| kdsBasePools | 装备池、产能池、政策池、数据池、场景池 | 必挂 |
| enhancedLedgerLinks | 贡献账本、积分池、悬赏池、SOP 账本 | 候选链接 |
| evidenceCompletenessGate | partial | 未提交资料前不得 pass |
| waesGateStatus | pending | 待规则检查 |
| recommendation | collect_more | 首轮默认补资料 |
| forbiddenClaims | 投资通过、合作确认、GFIS 接入完成、收益确认 | 明确禁止 |

### 5.2 原料知识源候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| knowledgeSourceId | `KSO-HBLC-RAW-202606-0001` | 原料知识源候选 |
| sourceCategory | raw_material | 原料类别、供应商、行情、质量指标等 |
| sourceName | `TBD` | 不得填未经提交的供应商或报价事实 |
| sourceRefs | `TBD` | 文件、网站、会议、邮件或线下索引 |
| trustLevel | T0 | 初始为线索，提交后再升级 |
| classificationLevel | DSR-L1 / DSR-L2 / DSR-L3 | 根据内容确定 |
| usableForAI | redacted_only | 默认脱敏后可用 |
| kdsBasePools | 原料池、资金池、数据池、场景池 | 必挂 |
| enhancedLedgerLinks | 贡献账本、积分池、悬赏池、争议池 | 候选链接 |
| waesGateRefs | pending | 待 WAES 记录 |

### 5.3 订单线索候选实例

| 字段 | 当前值 | 填报要求 |
|---|---|---|
| knowledgeSourceId | `KSO-HBLC-ORD-202606-0001` | 订单线索候选 |
| sourceCategory | order_lead | 销售订单线索 |
| customerOrScenario | `TBD` | 未提交前不得写真实客户名 |
| sourceRefs | `TBD` | 报价、采购意向、电话、会议或邮件索引 |
| revenueStatus | potential_value | 无到账前只能潜在产值 |
| kdsBasePools | 订单池、资金池、原料池、数据池、场景池 | 必挂 |
| enhancedLedgerLinks | 潜在产值池、贡献账本、收益池、争议池 | 候选链接，收益池仅作到账后路径 |
| waesGateStatus | pending | 待规则检查 |
| forbiddenClaims | 正式订单、到账、合同成立、收益分配 | 明确禁止 |

## 6. MMC 首批参数备案候选

| parameterChangeId | parameterId | 变更类型 | 当前状态 | 备案要求 |
|---|---|---|---|---|
| `MPC-MMP-WGT-202606-0001` | `MMP-WGT-202606-0001` | 初始阶段权重 | draft | 明确知识、产值、渠道、治理、悬赏、纠错的初始权重 |
| `MPC-MMP-COF-202606-0001` | `MMP-COF-202606-0001` | 兑换系数 | draft | 明确不同积分类型和项目阶段的兑换系数版本 |
| `MPC-MMP-THR-202606-0001` | `MMP-THR-202606-0001` | GFIS AI 评分阈值 | draft | 保留 85 分试运行通过线和 hard_fail 规则 |

参数备案候选不等于参数生效。参数进入 `active` 前必须保留 MMC 责任主体、WAES 门禁记录、变更理由、适用范围、版本号和必要的委员会备案。

## 7. 提交包字段完整性检查

| 检查项 | 最低要求 | 不满足时 |
|---|---|---|
| 编号 | instanceId / assessmentRecordId / knowledgeSourceId / parameterChangeId 不为空 | returned_for_evidence |
| 来源 | sourceRefs、sourceParty 或 sourceOwner 至少有可追溯索引 | blocked_by_source_gap |
| 密级 | classificationLevel 和 redactionLevel / usableForAI 已设置 | blocked_by_classification |
| 底座池 | kdsBasePools 至少一个，且必须来自 KDS 11 池 | returned_for_evidence |
| 增强账本 | enhancedLedgerLinks 至少一个 | returned_for_evidence |
| WAES | waesGateStatus 或 waesGateRefs 已有 pending / rule_recorded | returned_for_evidence |
| 禁止声明 | forbiddenClaims 明确列出 | blocked_by_overreach |
| LOOP | loopEvidenceRefs 指向 `GPCF-KDS-DKS-022` | returned_for_evidence |

## 8. 可见范围

| 实例类型 | 默认可见范围 | 扩大范围条件 |
|---|---|---|
| 葛化资料实例 | 葛化项目组、平台治理、WAES、必要委员会 | 项目负责人授权或悬赏邀请 |
| 葛化 AI 评分记录 | 项目组、评分人、WAES、平台治理 | 进入复用母版后可脱敏展示 |
| 湖北磷材拓厂实例 | 湖北磷材项目组、平台治理、WAES、必要委员会 | 合作单位确认或委员会邀请 |
| 湖北磷材知识源 | 本单位、平台治理、WAES | DSR-L0 / DSR-L1 可脱敏扩展 |
| MMC 参数候选 | MMC、WAES、平台治理、委员会 | 生效后按规则发布摘要 |

合作单位可查看本单位记录。跨单位查看必须基于邀请、悬赏、授权、委员会裁决或脱敏知识产品。

## 9. 本轮不处理范围

1. 不创建飞书、小即、KDS、GFIS、GPC、PVAOS 或其他真实账号。
2. 不配置生产权限、生产密钥、生产 API 或真实 KDS API 写入。
3. 不写 GFIS/GCFIS、GPC、PVAOS 等业务主账。
4. 不确认客户、供应商、价格、订单、合同、POD、到账、收益、积分或额度。
5. 不发布真实悬赏，不进行收益分配，不执行参数 active 生效。

## 10. Definition of Done

| 检查项 | 状态 |
|---|---|
| 葛化预运营期订单候选实例 | done |
| 葛化辽宁远航链路补证候选实例 | done |
| 葛化 GFIS AI 评分候选实例 | done |
| 湖北磷材拓厂来源候选实例 | done |
| 湖北磷材原料知识源候选实例 | done |
| 湖北磷材订单线索候选实例 | done |
| MMC 首批参数备案候选 | done |
| 提交包字段完整性检查 | done |
| 可见范围和不处理范围 | done |
| LOOP evidence 待本轮记录纳入 | done |

本轮不要求真实资料已提交、真实评估已通过、真实参数已生效、真实悬赏已发布、真实积分收益已确认或真实业务主账已写入。

## 11. 下一轮建议

`GPCF-KDS-DKS-023` 建议进入“提交前审核清单与人工确认工作台”：

1. 把 DKS-022 的 6 类候选实例转成一张可勾选审核清单。
2. 明确每类实例提交前由谁确认、确认什么、缺什么就退回到哪里。
3. 建立 WAES 规则记录、委员会备案和用户急停的最小记录表。
4. 准备后续真实脱敏资料进入时的 `submitted` 状态迁移规则。
