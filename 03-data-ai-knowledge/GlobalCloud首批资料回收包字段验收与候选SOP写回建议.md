---
doc_id: GPCF-DOC-B49150CE25
title: GlobalCloud 首批资料回收包字段验收与候选 SOP 写回建议
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md
source_path: 03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 首批资料回收包字段验收与候选 SOP 写回建议

状态：`GPCF-KDS-DKS-026` 受控任务包  
日期：2026-06-17  
适用范围：葛化物流预运营期订单、辽宁远航链路、湖北磷材拓厂项目、真实脱敏资料回收包、字段验收、候选 SOP 写回建议、KDS 11 个底座资源池、增强治理账本、WAES 规则门禁、人工确认和委员会备案。

## 1. 定位

本文是 `GPCF-KDS-DKS-026` 的正式交付，用于把 `GPCF-KDS-DKS-025` 中三条真实资料回收任务转成可填报回收包、字段级验收 checklist、候选 SOP 写回格式和人工确认后的关闭记录模板。

本文只定义字段、验收、候选写回和关闭模板。本文不代表真实资料已经收到，不代表资料已经通过验收，不代表 GFIS / GCFIS、GPC、PVAOS 或其它业务主账已经写入，不代表真实 KDS API 已同步，不代表积分、收益、AI 额度、悬赏、争议、参数或 SOP 已确认生效。

## 2. 承接对象

| recoveryTaskId | requestId | packageId | 试点线 | 优先级 | 当前状态 |
|---|---|---|---|---|---|
| `RRT-GH-ORD-202606-0001` | `KGR-GH-ORD-202606-0001` | `RPK-GH-ORD-202606-0001` | 葛化预运营期订单 | P0 | waiting_source |
| `RRT-HBLC-FEA-202606-0001` | `KGR-HBLC-FEA-202606-0001` | `RPK-HBLC-FEA-202606-0001` | 湖北磷材拓厂项目 | P1 | waiting_source |
| `RRT-GH-LY-202606-0001` | `KGR-GH-LY-202606-0001` | `RPK-GH-LY-202606-0001` | 葛化辽宁远航链路 | P0 | recovery_open |

## 3. 总原则

1. 回收包只能承载真实脱敏来源索引、元数据索引、责任主体说明、人工确认和规则记录，不承载未授权原文。
2. DSR-L2 资料默认脱敏后填报；DSR-L3 资料默认只填报元数据，不进入普通 AI 问答。
3. 字段验收只判断完整性、来源、密级、脱敏、责任主体、WAES 规则和人工确认状态。
4. 候选 SOP 写回只生成建议，不自动写 GFIS、GPC、PVAOS 或其它业务主账。
5. 任何涉及积分、收益、悬赏、潜在产值、争议和重大违规的事项，必须有委员会备案或裁决路径。
6. 自购 AI 额度只做本单位自用计量，不进入本轮回收包资源或统一收益池。

## 4. 回收包公共字段

| 字段 | 含义 | 必填性 | 验收规则 |
|---|---|---|---|
| packageId | 回收包编号 | 必填 | 必须唯一，且与 recoveryTaskId 一一对应 |
| recoveryTaskId | 资料回收任务编号 | 必填 | 必须来自 DKS-025 |
| requestId | 知识缺口编号 | 必填 | 必须来自 DKS-025 |
| submitter | 提交人 | 条件必填 | 真实提交时必填；演练或模板可为 `TBD` |
| sourceOwner | 来源责任主体 | 必填 | 不得长期为空；无法确认时为 returned |
| receiver | 接收人 | 条件必填 | 真实提交时必填 |
| sourceKind | phone_note / meeting_minutes / email / platform_receipt / file_index / policy_source / third_party_source / source_system_index / other | 必填 | 必须和 sourceRefs 匹配 |
| sourceRefs | 脱敏来源索引或元数据索引 | 必填 | 至少一条；不得写未授权原文 |
| redactionMode | none / partial / metadata_only | 必填 | DSR-L2 不得为 none；DSR-L3 默认 metadata_only |
| sensitivity | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 | 必填 | 不确定时进入 returned_for_classification |
| redactedFields | 已脱敏字段清单 | 条件必填 | partial 或 metadata_only 时必填 |
| blockedFields | 禁止入库或禁止 AI 处理字段 | 条件必填 | 涉隐私、合同、金融或未授权资料时必填 |
| kdsBasePools | KDS 11 底座资源池挂接 | 必填 | 至少一个 |
| enhancedLedgerLinks | 增强治理账本挂接 | 必填 | 至少一个 |
| waesRuleRecordId | WAES 规则记录编号 | 条件必填 | 提交验收前必填或说明 pending |
| humanReviewDecisionId | 人工审核决策编号 | 条件必填 | 提交验收前必填 |
| committeeFilingId | 委员会备案或裁决编号 | 条件必填 | 涉及积分、收益、悬赏、争议或重大违规时必填 |
| candidateSopRefs | 候选 SOP 建议编号 | 可选 | 必须保持 candidate |
| forbiddenClaims | 禁止声明 | 必填 | 不得为空 |
| packageState | draft / waiting_source / received_metadata_only / received_redacted_candidate / returned / blocked / submit_ready / closed | 必填 | 不得直接为 accepted 或 integrated |

## 5. 首批回收包

### 5.1 葛化预运营期订单回收包

| 字段 | 值 |
|---|---|
| packageId | `RPK-GH-ORD-202606-0001` |
| recoveryTaskId | `RRT-GH-ORD-202606-0001` |
| requestId | `KGR-GH-ORD-202606-0001` |
| sourceKind | phone_note / meeting_minutes / email / platform_receipt / file_index / other |
| requiredSourceRefs | 需求来源索引、来源责任主体、目标工厂、OEM 承接方、责任拆分、预运营期订单阶段说明 |
| kdsBasePools | 订单池、资金池、产能池、数据池、场景池 |
| enhancedLedgerLinks | 潜在产值池、贡献账本、SOP 账本、悬赏池、争议池 |
| waesRuleScope | evidence / classification / boundary |
| humanReviewScope | 来源、责任主体、目标工厂、OEM 承接方和责任拆分 |
| candidateSopRefs | `SOPC-GH-ORD-202606-0001` |
| forbiddenClaims | 正式订单、到账、收益、质量放行、GFIS 主账写入、SOP 生效 |
| packageState | waiting_source |

### 5.2 湖北磷材拓厂项目来源回收包

| 字段 | 值 |
|---|---|
| packageId | `RPK-HBLC-FEA-202606-0001` |
| recoveryTaskId | `RRT-HBLC-FEA-202606-0001` |
| requestId | `KGR-HBLC-FEA-202606-0001` |
| sourceKind | policy_source / third_party_source / file_index / meeting_minutes / other |
| requiredSourceRefs | 拓厂项目来源索引、区域资料、政策来源、第三方来源、装备或产能线索、项目负责人确认 |
| kdsBasePools | 装备池、产能池、政策池、数据池、场景池 |
| enhancedLedgerLinks | 贡献账本、积分池、悬赏池、SOP 账本、争议池 |
| waesRuleScope | evidence / classification / authority / boundary |
| humanReviewScope | 项目来源、政策来源、第三方来源和项目负责人确认 |
| candidateSopRefs | `SOPC-HBLC-FEA-202606-0001` |
| forbiddenClaims | 投资通过、合作确认、收益确认、GFIS 接入完成、新工厂模板正式生效 |
| packageState | waiting_source |

### 5.3 葛化辽宁远航链路回收包

| 字段 | 值 |
|---|---|
| packageId | `RPK-GH-LY-202606-0001` |
| recoveryTaskId | `RRT-GH-LY-202606-0001` |
| requestId | `KGR-GH-LY-202606-0001` |
| sourceKind | platform_receipt / file_index / email / source_system_index / other |
| requiredSourceRefs | 客户确认、样箱签收或反馈、POD、真实回执、KDS 回执、WAES confirmation、现代精工过渡责任材料 |
| kdsBasePools | 订单池、运力池、资金池、数据池、场景池 |
| enhancedLedgerLinks | 潜在产值池、贡献账本、悬赏池、争议池、SOP 账本 |
| waesRuleScope | evidence / real_receipt / classification / boundary |
| humanReviewScope | 客户链路、样箱链路、承接方链路和回执链路 |
| candidateSopRefs | `SOPC-GH-LY-202606-0001` |
| forbiddenClaims | 客户确认已取得、POD 已取得、KDS 回执已取得、WAES confirmation 已取得、GFIS verified artifact 已形成 |
| packageState | recovery_open |

## 6. 字段级验收 checklist

验收结果只允许：

| 结果 | 含义 | 后续动作 |
|---|---|---|
| pass | 字段满足当前阶段要求 | 可进入 submit_ready 或候选 SOP 复核 |
| partial | 字段可用但证据不足 | 保持候选，列出补证项 |
| returned | 字段缺失、来源不足或责任主体不清 | 退回来源责任主体 |
| blocked | 密级、权限、越权声明或真实性风险阻断 | 不进入 AI 问答、不写回 |
| disputed | 责任、贡献、收益、悬赏或违规争议 | 进入委员会备案或裁决 |

| 检查项 | GH-ORD | HBLC-FEA | GH-LY | 验收说明 |
|---|---|---|---|---|
| packageId 唯一 | required | required | required | 不唯一则 returned |
| recoveryTaskId 可追溯 | required | required | required | 必须能回溯 DKS-025 |
| requestId 可追溯 | required | required | required | 必须能回溯 KGR |
| sourceOwner 明确 | required | required | required | `TBD` 只能用于模板，不得通过验收 |
| sourceRefs 非空 | required | required | required | 至少一条脱敏来源索引或元数据索引 |
| sourceKind 匹配 | required | required | required | 类型与索引内容一致 |
| sensitivity 完成 | required | required | required | 不确定则 returned_for_classification |
| redactionMode 合规 | required | required | required | DSR-L2 / DSR-L3 按规则处理 |
| blockedFields 明确 | conditional | conditional | conditional | 涉隐私、合同、金融或未授权资料时必填 |
| kdsBasePools 挂接 | required | required | required | 至少挂接一个 KDS 11 池 |
| enhancedLedgerLinks 挂接 | required | required | required | 至少挂接一个增强账本 |
| WAES 记录 | conditional | conditional | conditional | 提交验收前必填或说明 pending |
| 人工审核记录 | conditional | conditional | conditional | 提交验收前必填 |
| 委员会备案 | conditional | conditional | conditional | 涉积分、收益、悬赏、争议或重大违规时必填 |
| forbiddenClaims 完整 | required | required | required | 不得缺失，不得自相矛盾 |
| candidateSopRefs 保持候选 | optional | optional | optional | 不得写成生效 SOP |

## 7. 候选 SOP 写回格式

### 7.1 公共格式

```yaml
candidateSopId:
sourcePackageId:
sourceRequestId:
sourceRecoveryTaskId:
targetSystem:
targetObject:
candidateType:
candidateSummary:
requiredHumanConfirmation:
requiredWaesRecord:
requiredCommitteeRecord:
kdsBasePools:
enhancedLedgerLinks:
writebackState: candidate
writebackGate: blocked_until_confirmed
forbiddenClaims:
loopEvidenceRefs:
```

### 7.2 首批候选 SOP 建议

| candidateSopId | sourcePackageId | targetSystem | targetObject | candidateType | candidateSummary | writebackState |
|---|---|---|---|---|---|---|
| `SOPC-GH-ORD-202606-0001` | `RPK-GH-ORD-202606-0001` | GFIS / KDS / Brain | 预运营期订单 | order_sop_candidate | 从需求来源开始建立预运营期订单识别、责任拆分、资料补证和人工确认步骤 | candidate |
| `SOPC-HBLC-FEA-202606-0001` | `RPK-HBLC-FEA-202606-0001` | KDS / Brain / GPCF | 拓厂项目来源评估 | expansion_project_sop_candidate | 从项目来源、区域资料、政策来源和第三方来源形成拓厂来源评估步骤 | candidate |
| `SOPC-GH-LY-202606-0001` | `RPK-GH-LY-202606-0001` | GFIS / KDS / WAES | 辽宁远航补证链路 | evidence_recovery_sop_candidate | 围绕客户确认、样箱反馈、POD、真实回执和规则记录形成补证闭环步骤 | candidate |

## 8. 写回门禁

| 门禁 | 通过条件 | 阻断条件 |
|---|---|---|
| 来源门禁 | sourceRefs 非空且 sourceOwner 明确 | 无来源、来源责任主体不清 |
| 密级门禁 | DSR 分级和脱敏完成 | DSR-L2 未脱敏、DSR-L3 提交正文 |
| 规则门禁 | WAES 记录完成或 pending 原因明确 | 无规则记录且试图写回 |
| 人工门禁 | 人工审核 pass 或 partial 且边界明确 | 未审核、审核退回或越权声明 |
| 委员会门禁 | 涉积分、收益、悬赏、争议时已备案 | 涉分配事项但无备案 |
| 主账门禁 | 业务系统确认允许候选进入后续处理 | 试图自动创建正式订单、收益、POD 或 verified artifact |

## 9. 人工确认后关闭记录模板

```yaml
gapClosureRecord:
  closureRecordId:
  requestId:
  recoveryTaskId:
  packageId:
  closeType: full / partial / returned / blocked / disputed / withdrawn
  acceptedSourceRefs:
  rejectedSourceRefs:
  waesRuleRecordId:
  humanReviewDecisionId:
  committeeFilingId:
  candidateSopRefs:
  remainingGaps:
  kdsBasePools:
  enhancedLedgerLinks:
  forbiddenClaims:
  loopEvidenceRefs:
  effectiveState: candidate_only
```

示例编号：

| closureRecordId | requestId | packageId | 当前建议状态 |
|---|---|---|---|
| `GCR-GH-ORD-202606-0001` | `KGR-GH-ORD-202606-0001` | `RPK-GH-ORD-202606-0001` | template_only |
| `GCR-HBLC-FEA-202606-0001` | `KGR-HBLC-FEA-202606-0001` | `RPK-HBLC-FEA-202606-0001` | template_only |
| `GCR-GH-LY-202606-0001` | `KGR-GH-LY-202606-0001` | `RPK-GH-LY-202606-0001` | template_only |

## 10. AI 助手使用边界

| 助手类型 | 可使用内容 | 输出 | 禁止事项 |
|---|---|---|---|
| GFIS 知识问答助手 | 已授权的 KDS 摘要、字段说明、缺口状态 | 问答、补证路径、资料位置 | 输出未授权原文或确认业务完成 |
| GFIS 使用助手 | 字段级 checklist、候选 SOP、人工确认规则 | 填写建议、流程提示 | 自动创建正式单据 |
| GFIS 文档验收助手 | 回收包字段、DSR、WAES、人工审核状态 | pass / partial / returned / blocked 建议 | 替代人工审核 |
| 湖北磷材拓厂知识助手 | 拓厂来源、政策来源、第三方来源、复制模板 | 项目来源评估建议 | 确认投资通过或收益 |
| KDS / Brain 知识编制 | 候选事实、候选 SOP、缺口摘要 | 知识页面和 SOP 展示候选 | 替代 KDS 主存或业务主账 |

## 11. 本轮不处理范围

1. 不接收、保存或展示真实未脱敏资料正文。
2. 不发布真实悬赏，不冻结真实资源，不结算积分。
3. 不写 GFIS/GCFIS、GPC、PVAOS 或其它业务主账。
4. 不调用真实外部 API，不配置真实生产权限。
5. 不执行真实 KDS API 写入，不把本地镜像写成真实同步。
6. 不确认客户、供应商、价格、订单、合同、POD、到账、金融凭证、积分、收益、AI 额度或参数生效。
7. 不升级 accepted 或 integrated。

## 12. Definition of Done

| 检查项 | 状态 |
|---|---|
| 三条 RRT 回收包字段 | done |
| 公共字段验收规则 | done |
| 字段级 checklist | done |
| 候选 SOP 写回公共格式 | done |
| 三条候选 SOP 建议 | done |
| 写回门禁 | done |
| 关闭记录模板 | done |
| AI 助手使用边界 | done |
| LOOP evidence 待本轮记录纳入 | done |

本轮完成后，只证明首批资料回收包字段、验收 checklist、候选 SOP 写回格式和关闭记录模板已经建立，不证明真实资料已收到、真实 SOP 已生效、真实主账已写入、真实积分已确认、真实收益已分配或真实 KDS API 已同步。

## 13. 下一轮建议

`GPCF-KDS-DKS-027` 建议进入“葛化 GFIS AI 助手内测问答与资料回收包联动规则”：

1. 把本轮 `RPK` 与 GFIS 知识问答、使用助手、文档验收助手的问题样本联动。
2. 定义用户提问触发知识缺口、回收包、候选 SOP 和人工确认的路径。
3. 建立内测记录中缺口回流到 `KGR` / `RRT` / `SOPC` 的规则。
