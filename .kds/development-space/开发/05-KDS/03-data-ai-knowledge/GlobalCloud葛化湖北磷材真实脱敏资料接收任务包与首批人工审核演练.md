---
doc_id: GPCF-DOC-FEE06CC888
title: GlobalCloud 葛化湖北磷材真实脱敏资料接收任务包与首批人工审核演练
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化湖北磷材真实脱敏资料接收任务包与首批人工审核演练.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化湖北磷材真实脱敏资料接收任务包与首批人工审核演练.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化湖北磷材真实脱敏资料接收任务包与首批人工审核演练

状态：`GPCF-KDS-DKS-024` 受控接收任务包  
日期：2026-06-17  
适用范围：葛化物流预运营期订单候选、湖北磷材拓厂来源候选、真实脱敏资料接收、KDS 11 个底座资源池、增强治理账本、WAES 规则门禁、人工审核演练、委员会备案和 GPCF LOOP evidence。

## 1. 定位

本文是 `GPCF-KDS-DKS-024` 的正式交付，用于把 `GPCF-KDS-DKS-023` 的提交前审核工作台推进为真实脱敏资料接收任务包和首批人工审核演练。

本文只建立接收任务包、脱敏字段、演练样例、退回路径和最小审核记录。本文不代表真实脱敏资料已经收到，不代表 `TBD` 已被真实来源替换，不代表 GFIS / GCFIS、GPC、PVAOS 或其它业务主账已经写入，不代表真实 KDS API 已同步，不代表积分、收益、AI 额度、悬赏、争议、参数或 SOP 已确认生效。

## 2. 接收总原则

1. 真实脱敏资料必须先进入 `received_redacted_candidate` 或 `received_metadata_only`，不得直接进入 `submitted`、`confirmed`、`accepted` 或 `integrated`。
2. DSR-L2 资料必须脱敏后进入审核；DSR-L3 资料默认只提交元数据索引，不进入普通 AI 问答或跨单位共享正文。
3. 每个资料接收任务必须保留来源责任主体、提交人、接收人、接收时间、脱敏责任人、脱敏范围和不可见字段清单。
4. AI 只能生成候选摘要、候选字段映射、候选 SOP、候选积分和候选审核意见。
5. WAES 只确认规则、证据、权限、边界和例外，不替代业务主账确认。
6. 委员会只在积分、收益、悬赏、争议、重大违规、参数生效和分配参考事项上介入。
7. 用户保留体系治理权、急停权和规则治理权，不承担日常裁决。
8. 自购 AI 额度先自用；正式收入按到账确认。

## 3. 接收任务包字段

| 字段 | 含义 | 必填性 |
|---|---|---|
| receivingTaskId | 接收任务编号 | 必填 |
| candidateRef | 对应 DKS-022 / DKS-023 候选实例 | 必填 |
| workbenchItemId | 对应 DKS-023 工作台条目 | 必填 |
| sourceOwner | 来源责任主体或单位 | 必填 |
| submitter | 提交人 | 必填 |
| receiver | 接收人 | 必填 |
| sourceKind | phone_note / meeting_minutes / email / platform_receipt / file_index / third_party_source / other | 必填 |
| originalSensitivity | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 | 必填 |
| redactionMode | none / partial / metadata_only | 必填 |
| redactedFields | 已脱敏字段清单 | 条件必填 |
| blockedFields | 不得进入 KDS 或 AI 的字段 | 条件必填 |
| sourceRefs | 脱敏来源索引 | 必填 |
| kdsBasePools | KDS 11 底座资源池挂接 | 必填 |
| enhancedLedgerLinks | 增强治理账本挂接 | 必填 |
| waesRuleRecordId | WAES 规则记录编号 | 条件必填 |
| humanReviewDecisionId | 人工审核决策编号 | 必填 |
| committeeFilingId | 委员会备案编号 | 条件必填 |
| currentState | draft / waiting_source / received_redacted_candidate / received_metadata_only / returned / blocked / rehearsal_only | 必填 |
| forbiddenClaims | 禁止声明 | 必填 |

## 4. 首批接收任务

### 4.1 葛化预运营期订单接收任务

| 字段 | 值 |
|---|---|
| receivingTaskId | `RTP-GH-ORD-202606-0001` |
| candidateRef | `GHI-GH-ORD-202606-0001` |
| workbenchItemId | `WB-GH-ORD-202606-0001` |
| 接收目标 | 把电话、会议、邮件、平台线索或合作单位文件中的需求信息，转成脱敏预运营期订单候选来源索引 |
| sourceOwner | `TBD` |
| submitter | `TBD` |
| receiver | KDS 记录员 / 项目负责人 |
| originalSensitivity | DSR-L2 |
| redactionMode | partial |
| redactedFields | 客户名、联系人、电话、价格、金额、精确规格、合同号 |
| blockedFields | 身份证件、银行账号、未授权合同正文、未授权客户隐私、未授权金融凭证 |
| kdsBasePools | 订单池、资金池、数据池、场景池 |
| enhancedLedgerLinks | 潜在产值池、贡献账本、SOP 账本、争议池 |
| currentState | waiting_source |
| forbiddenClaims | 正式订单、到账、收益、质量放行、GFIS 主账写入 |

### 4.2 湖北磷材拓厂来源接收任务

| 字段 | 值 |
|---|---|
| receivingTaskId | `RTP-HBLC-FEA-202606-0001` |
| candidateRef | `FEA-HBLC-202606-0001` |
| workbenchItemId | `WB-HBLC-FEA-202606-0001` |
| 接收目标 | 把拓厂项目来源、区域资料、政策资料、装备与产能线索转成脱敏拓厂来源评估资料 |
| sourceOwner | `TBD` |
| submitter | `TBD` |
| receiver | KDS 记录员 / 湖北磷材项目负责人 |
| originalSensitivity | DSR-L1 / DSR-L2 |
| redactionMode | partial / metadata_only |
| redactedFields | 合作方联系人、未公开投资条件、报价、内部产能计划、未授权区域资源信息 |
| blockedFields | 未授权商业计划全文、未授权财务资料、未授权合同正文 |
| kdsBasePools | 装备池、产能池、政策池、数据池、场景池 |
| enhancedLedgerLinks | 贡献账本、积分池、悬赏池、SOP 账本 |
| currentState | waiting_source |
| forbiddenClaims | 投资通过、合作确认、GFIS 接入完成、收益确认 |

## 5. 接收状态机

```text
waiting_source
  -> source_received_private
  -> redaction_checked
  -> received_redacted_candidate
  -> waes_rule_recorded
  -> human_review_pending
  -> submit_ready
```

阻断分支：

```text
returned_for_evidence
  blocked_by_classification
  blocked_by_overreach
  metadata_only_required
  disputed
  withdrawn
```

状态说明：

| 状态 | 含义 | 是否可进入 submitted |
|---|---|---|
| waiting_source | 等待真实脱敏来源 | 否 |
| source_received_private | 原始资料已私下接收但未脱敏 | 否 |
| redaction_checked | 脱敏检查已完成 | 否 |
| received_redacted_candidate | 脱敏候选资料已形成 | 条件允许 |
| received_metadata_only | 仅元数据入库 | 条件允许 |
| rehearsal_only | 仅演练，不是真实资料 | 否 |
| submit_ready | 人工确认后可提交 | 条件允许 |

## 6. 首批人工审核演练

本节只做演练，不使用真实客户、供应商、价格、合同、POD、到账或金融凭证。演练记录不得进入业务主账，不得作为收益、积分、额度或参数生效依据。

### 6.1 葛化预运营期订单演练

| 字段 | 值 |
|---|---|
| rehearsalId | `RHR-GH-ORD-202606-0001` |
| receivingTaskId | `RTP-GH-ORD-202606-0001` |
| candidateRef | `GHI-GH-ORD-202606-0001` |
| rehearsalSourceType | synthetic_redacted_rehearsal |
| sourceSummary | 某合作单位提出潜在需求，需确认来源、目标工厂、OEM 承接方和责任拆分 |
| AI candidate output | 建议进入预运营期订单候选，并生成字段映射和 SOP 建议 |
| WAES decision | return |
| Human decision | returned_for_evidence |
| 原因 | 真实来源索引、来源责任主体、执行方和责任拆分仍为 `TBD` |
| 可转正式条件 | 提交脱敏来源索引、来源责任主体、目标工厂 / OEM 责任拆分和 WAES 规则记录 |

### 6.2 湖北磷材拓厂来源演练

| 字段 | 值 |
|---|---|
| rehearsalId | `RHR-HBLC-FEA-202606-0001` |
| receivingTaskId | `RTP-HBLC-FEA-202606-0001` |
| candidateRef | `FEA-HBLC-202606-0001` |
| rehearsalSourceType | synthetic_redacted_rehearsal |
| sourceSummary | 某区域拓厂机会具备政策、装备和产能线索，需进入拓厂来源评估 |
| AI candidate output | 建议进入拓厂来源候选，并复用葛化母版结构 |
| WAES decision | return |
| Human decision | returned_for_evidence |
| 原因 | 缺真实脱敏区域资料、来源责任主体、政策来源索引和项目负责人确认 |
| 可转正式条件 | 提交脱敏项目来源索引、政策或第三方来源、项目负责人确认和 WAES 规则记录 |

## 7. 样例记录

### 7.1 WAESRuleRecord 样例

| 字段 | 葛化演练值 | 湖北磷材演练值 |
|---|---|---|
| recordId | `WRR-GH-ORD-202606-0001` | `WRR-HBLC-FEA-202606-0001` |
| candidateRef | `GHI-GH-ORD-202606-0001` | `FEA-HBLC-202606-0001` |
| ruleScope | evidence / classification / boundary | evidence / classification / boundary |
| decision | return | return |
| reason | 缺真实来源索引和责任拆分 | 缺真实来源索引和项目负责人确认 |
| evidenceRefs | rehearsal_only | rehearsal_only |
| loopEvidenceRefs | `GPCF-KDS-DKS-024` | `GPCF-KDS-DKS-024` |

### 7.2 HumanReviewDecision 样例

| 字段 | 葛化演练值 | 湖北磷材演练值 |
|---|---|---|
| decisionId | `HRD-GH-ORD-202606-0001` | `HRD-HBLC-FEA-202606-0001` |
| workbenchItemId | `WB-GH-ORD-202606-0001` | `WB-HBLC-FEA-202606-0001` |
| candidateRef | `GHI-GH-ORD-202606-0001` | `FEA-HBLC-202606-0001` |
| reviewerRole | 项目负责人 / KDS 记录员 | 项目负责人 / KDS 记录员 |
| decision | returned | returned |
| returnPath | returned_for_evidence | returned_for_evidence |
| notes | 需要真实脱敏来源和责任拆分 | 需要真实脱敏来源和项目负责人确认 |

### 7.3 CommitteeFilingRecord 样例

| 字段 | 葛化演练值 | 湖北磷材演练值 |
|---|---|---|
| filingId | `CFR-GH-ORD-202606-0001` | `CFR-HBLC-FEA-202606-0001` |
| candidateRef | `GHI-GH-ORD-202606-0001` | `FEA-HBLC-202606-0001` |
| topic | potential_value / points | knowledge / points |
| votingRule | majority |
| decision | not_required_until_real_source | not_required_until_real_source |
| allocationBasis | pending_real_source | pending_real_source |
| archiveRefs | `GPCF-KDS-DKS-024` | `GPCF-KDS-DKS-024` |

## 8. 转正式接收条件

任一演练记录转为正式接收记录，必须满足：

1. 提交真实脱敏来源索引或元数据索引。
2. 填写来源责任主体、提交人、接收人和接收时间。
3. 完成 DSR 分级和脱敏检查。
4. 挂接至少一个 KDS 11 底座资源池和一个增强治理账本。
5. 生成 WAESRuleRecord 或 WAES pending 记录。
6. 生成人工审核决策。
7. 涉及积分、收益、悬赏、争议或参数事项时，生成委员会备案或裁决路径。
8. 不出现正式订单、到账、收益确认、业务主账写入、质量放行、参数生效或业务闭环完成等越权声明。

## 9. 本轮不处理范围

1. 不接收、保存或展示真实未脱敏资料正文。
2. 不创建真实账号，不配置生产权限，不调用真实外部 API。
3. 不写 GFIS/GCFIS、GPC、PVAOS 或其它业务主账。
4. 不执行真实 KDS API 写入，不把本地镜像写成真实同步。
5. 不确认客户、供应商、价格、订单、合同、POD、到账、金融凭证、积分、收益或额度。
6. 不发布真实悬赏，不执行收益分配，不执行参数 active 生效。

## 10. Definition of Done

| 检查项 | 状态 |
|---|---|
| 葛化预运营期订单接收任务 | done |
| 湖北磷材拓厂来源接收任务 | done |
| 接收任务包字段 | done |
| 接收状态机 | done |
| 首批人工审核演练 | done |
| WAES / 人工审核 / 委员会样例记录 | done |
| 转正式接收条件 | done |
| LOOP evidence 待本轮记录纳入 | done |

本轮完成后，只证明真实脱敏资料接收任务包和人工审核演练已经建立，不证明真实脱敏资料已收到、真实来源已验证、真实业务主账已写入、真实收益已确认或真实 KDS API 已同步。

## 11. 下一轮建议

`GPCF-KDS-DKS-025` 建议进入“知识缺口悬赏与真实资料回收跟踪台账”：

1. 把 DKS-024 的 `returned_for_evidence` 转成知识缺口和资料回收任务。
2. 建立葛化预运营期订单和湖北磷材拓厂来源的真实脱敏资料回收清单。
3. 明确哪些缺口可以发布悬赏候选，哪些必须由项目负责人或来源责任主体补证。
4. 继续保持候选、脱敏、WAES、人工确认和委员会备案边界。
