---
doc_id: GPCF-DOC-1A584CFD8F
title: GlobalCloud 湖北磷材真实资料接收任务包与人工评测演练
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud湖北磷材真实资料接收任务包与人工评测演练.md
source_path: 03-data-ai-knowledge/GlobalCloud湖北磷材真实资料接收任务包与人工评测演练.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 湖北磷材真实资料接收任务包与人工评测演练

日期：2026-06-17  
状态：`planned_receipt_drill`  
批次：`PILOT-HBLC-KDS-202606-0001`

## 1. 定位

本文承接 DKS-032 的湖北磷材评测运行记录首批空白台账，定义湖北磷材第一阶段真实资料进入前的接收任务包、脱敏规则、人工评测演练流程、WAES 门禁记录和 Brain 知识页候选生成边界。

本文只定义接收与演练规则，不表示：

- 湖北磷材已经提交真实资料；
- 本轮已经接收 DSR-L2 / DSR-L3 原文；
- 已经完成真实评测、人工评分或 WAES 通过；
- Brain 知识页已经发布；
- KDS、WAES、GFIS、GPC 或其他业务系统已经发生真实写入；
- 积分、收益、额度、悬赏、争议或 SOP 已经确认。

## 2. 接收总规则

| 项 | 规则 |
|---|---|
| 接收批次 | `PILOT-HBLC-KDS-202606-0001` |
| 默认状态 | `planned_receipt_drill` |
| 接收对象 | FEA / RAW / IND / ORD / TPL / MIX |
| 接收方式 | 只接收资料索引、脱敏摘要、文件哈希、责任主体和密级声明 |
| 禁止接收 | 未授权 DSR-L3 原文、合同原文、客户订单原文、供应商报价原文、个人敏感信息 |
| AI 使用 | 仅可读取脱敏摘要和授权索引，输出候选摘要、候选缺口、候选写回建议 |
| 人工评测 | 必须由人工评测人填写评分、红线检查和放行建议 |
| WAES 门禁 | 只确认规则、证据、权限、边界和例外，不替代业务事实确认 |
| Brain 边界 | 只生成知识页候选结构，不发布正式知识页 |
| KDS 边界 | 本地镜像与候选记录不得写成真实 KDS API 回执 |

## 3. ReceiptTaskPackage 台账

| receiptTaskId | linkedRunRecordId | objectType | requestedMaterial | allowedForm | forbiddenForm | receiverRole | ownerToConfirm | defaultStatus |
|---|---|---|---|---|---|---|---|---|
| `RTP-HBLC-FEA-202606-0001` | `ERR-HBLC-FEA-202606-0001` | FEA | 拓厂需求来源、目标区域、工厂条件、政策来源、项目负责人确认 | 脱敏摘要、来源索引、责任主体、时间戳 | 投资决策原文、未经授权的合同或审批原文 | KDS / GPCF | 湖北磷材项目负责人 | planned |
| `RTP-HBLC-RAW-202606-0001` | `ERR-HBLC-RAW-202606-0001` | RAW | 原料类别、供应商脱敏摘要、质量指标、行情或报价来源 | 脱敏摘要、来源索引、区间化价格、质量指标摘要 | 供应商报价原文、商业敏感价格明细 | KDS / GPCF | 原料责任方 | planned |
| `RTP-HBLC-IND-202606-0001` | `ERR-HBLC-IND-202606-0001` | IND | 行业政策、标准、公开资料和适用范围 | 权威链接、检索时间、适用范围、引用边界 | 未核验 AI 摘要直接作为权威结论 | KDS / WAES | 行业资料责任方 | planned |
| `RTP-HBLC-ORD-202606-0001` | `ERR-HBLC-ORD-202606-0001` | ORD | 客户需求来源、报价或意向索引、规格、数量、交期 | 脱敏摘要、来源索引、客户匿名编号、潜在产值区间 | 客户订单原文、合同原文、到账证明原文 | KDS / GPCF | 销售或渠道责任方 | planned |
| `RTP-HBLC-TPL-202606-0001` | `ERR-HBLC-TPL-202606-0001` | TPL | 葛化母版结构复用点、湖北磷材差异项、候选 SOP 控制点 | 结构清单、差异项、WAES 规则记录 | 葛化未确认事实、跨单位不可见资料 | KDS / Brain | 模板编制责任方 | planned |
| `RTP-HBLC-MIX-202606-0001` | `ERR-HBLC-MIX-202606-0001` | MIX | KDS 11 池挂接、增强账本、WAES 和 LOOP evidence | 关联编号、受控文档链接、候选关系 | 游离增强账本、无来源候选记录 | GPCF / WAES | GPCF 治理负责人 | planned |

## 4. RedactionRule 台账

| redactionRuleId | materialClass | mustKeep | mustRemoveOrMask | allowedForAI | escalation |
|---|---|---|---|---|---|
| `RDR-HBLC-FEA-001` | 拓厂资料 | 来源类型、责任主体、时间、区域级别、摘要 | 具体未公开投资金额、审批原文、个人信息 | true | 涉及审批或投资承诺时进 WAES |
| `RDR-HBLC-RAW-001` | 原料资料 | 原料类别、质量指标摘要、来源类型、责任主体 | 供应商实名、报价原文、商业敏感价格明细 | true | 涉及采购事实或价格确认时进 WAES / 人工 |
| `RDR-HBLC-IND-001` | 行业政策/标准 | 来源链接、检索时间、适用范围、引用边界 | 无授权全文复制、未核验结论 | true | T3 升级必须保留来源证据 |
| `RDR-HBLC-ORD-001` | 订单线索 | 需求来源、客户匿名编号、规格摘要、潜在区间 | 客户订单原文、合同原文、到账证明原文 | redacted_only | 涉及正式订单、合同或收益时进人工/委员会 |
| `RDR-HBLC-TPL-001` | 复制模板 | 结构、流程、控制点、差异项 | 葛化未确认事实、跨单位不可见资料 | true | 复用争议进 WAES / 委员会 |

## 5. ManualEvaluationDrill 台账

| drillId | linkedReceiptTaskId | evaluatorRole | checkItems | scoringTarget | redlineCheck | outputRecord | drillStatus |
|---|---|---|---|---|---|---|---|
| `MED-HBLC-FEA-202606-0001` | `RTP-HBLC-FEA-202606-0001` | 人工评测人 / WAES 规则复核 | 来源完整性、政策适用、区域条件、项目负责人确认 | `ERR-HBLC-FEA-202606-0001` | `RED-HBLC-001` | 评分、缺口、下一步 | planned |
| `MED-HBLC-RAW-202606-0001` | `RTP-HBLC-RAW-202606-0001` | 人工评测人 / 原料责任方 | 来源、质量指标、报价边界、采购事实隔离 | `ERR-HBLC-RAW-202606-0001` | `RED-HBLC-002` | 评分、脱敏缺口、悬赏候选 | planned |
| `MED-HBLC-IND-202606-0001` | `RTP-HBLC-IND-202606-0001` | 人工评测人 / WAES 规则复核 | 来源可信级别、检索时间、适用范围 | `ERR-HBLC-IND-202606-0001` | `RED-HBLC-003` | 评分、T3 候选、Brain 候选 | planned |
| `MED-HBLC-ORD-202606-0001` | `RTP-HBLC-ORD-202606-0001` | 人工评测人 / 销售责任方 | 需求来源、客户匿名编号、潜在产值边界 | `ERR-HBLC-ORD-202606-0001` | `RED-HBLC-004` | 评分、潜在产值候选、补证动作 | planned |
| `MED-HBLC-TPL-202606-0001` | `RTP-HBLC-TPL-202606-0001` | 人工评测人 / Brain 编制责任方 | 结构复用、差异项、候选 SOP 控制点 | `ERR-HBLC-TPL-202606-0001` | `RED-HBLC-005` | 评分、模板候选、知识页候选 | planned |

## 6. WAESGateRecordCandidate 台账

| waesGateCandidateId | linkedTaskId | gateType | ruleToConfirm | evidenceRequired | allowedOutcome | currentStatus |
|---|---|---|---|---|---|---|
| `WGR-HBLC-FEA-202606-0001` | `RTP-HBLC-FEA-202606-0001` | source_boundary | 拓厂候选不得等同投资通过 | 来源索引、责任主体、人工评分 | record / return / block | planned |
| `WGR-HBLC-RAW-202606-0001` | `RTP-HBLC-RAW-202606-0001` | purchase_boundary | 原料线索不得等同采购事实 | 脱敏来源、质量指标、价格边界 | record / return / block | planned |
| `WGR-HBLC-IND-202606-0001` | `RTP-HBLC-IND-202606-0001` | trusted_source | T3 可信来源升级条件 | 来源链接、检索时间、适用范围 | record / return / block | planned |
| `WGR-HBLC-ORD-202606-0001` | `RTP-HBLC-ORD-202606-0001` | revenue_boundary | 订单线索不得等同正式订单或到账收入 | 客户匿名编号、来源索引、财务口径说明 | record / return / block | planned |
| `WGR-HBLC-TPL-202606-0001` | `RTP-HBLC-TPL-202606-0001` | reuse_boundary | 葛化母版只复用结构和控制点 | 结构清单、差异项、授权边界 | record / return / block | planned |

## 7. BrainKnowledgePageCandidate 台账

| brainCandidateId | linkedTaskId | candidatePageType | allowedInputs | forbiddenInputs | outputStatus |
|---|---|---|---|---|---|
| `BKC-HBLC-FEA-202606-0001` | `RTP-HBLC-FEA-202606-0001` | 拓厂项目知识页候选 | 脱敏摘要、区域级别、政策索引、候选评分 | 投资通过结论、审批原文 | planned |
| `BKC-HBLC-RAW-202606-0001` | `RTP-HBLC-RAW-202606-0001` | 原料知识页候选 | 原料类别、质量指标摘要、来源索引 | 报价原文、供应商敏感信息 | planned |
| `BKC-HBLC-IND-202606-0001` | `RTP-HBLC-IND-202606-0001` | 行业资料页候选 | 来源链接、适用范围、可信级别 | 未核验权威结论 | planned |
| `BKC-HBLC-ORD-202606-0001` | `RTP-HBLC-ORD-202606-0001` | 订单线索页候选 | 客户匿名编号、需求摘要、潜在区间 | 客户订单原文、合同原文 | planned |
| `BKC-HBLC-TPL-202606-0001` | `RTP-HBLC-TPL-202606-0001` | 新工厂复制模板页候选 | 葛化结构、湖北磷材差异项、候选 SOP | 跨单位不可见事实 | planned |

## 8. 接收演练流程

| 步骤 | 动作 | 责任主体 | 输出 |
|---|---|---|---|
| 1 | 发起资料接收任务包 | GPCF / KDS | `RTP-HBLC-*` 任务 |
| 2 | 合作单位提交脱敏摘要或来源索引 | 湖北磷材对应责任方 | `sourceRefs` 候选 |
| 3 | 执行脱敏规则检查 | KDS / 人工评测人 | `RDR-HBLC-*` 结果 |
| 4 | 人工评分和红线检查 | 人工评测人 | `ERR-HBLC-*` 更新候选 |
| 5 | WAES 记录规则与例外 | WAES | `WGR-HBLC-*` 候选 |
| 6 | 形成 Brain 知识页候选 | Brain | `BKC-HBLC-*` 候选 |
| 7 | 进入缺口、悬赏、写回或贡献候选 | KDS / GPCF | 仅候选，不确认 |

## 9. 硬停止规则

出现以下情形必须停止接收或退回：

1. 提交未授权 DSR-L3 原文。
2. 把订单线索写成正式订单、合同或到账收入。
3. 把原料线索写成采购事实或确认价格。
4. 把拓厂候选写成投资通过、合作确认或建设启动。
5. 把葛化事实直接复制为湖北磷材事实。
6. Brain 页面候选包含未经授权的原文或跨单位不可见信息。
7. KDS 本地镜像或候选记录被写成真实 KDS API 已同步。
8. 未经委员会确认写入正式积分、收益、悬赏或争议结论。

## 10. 完成定义

本文完成条件：

1. 六类接收任务包均具备统一编号。
2. 每类资料均明确允许形式、禁止形式、责任主体和默认状态。
3. 脱敏规则覆盖拓厂、原料、行业、订单和模板资料。
4. 人工评测演练能回写到 DKS-032 的运行记录编号。
5. WAES 门禁候选和 Brain 知识页候选均保持 planned 状态。
6. 所有输出只形成候选，不确认真实事实、正式积分、正式收益或正式 SOP。
7. 本文纳入 LOOP 文档治理、KDS 本地镜像、防污染、TOKEN 与文档门禁检查。

## 11. DKS-034 建议

下一轮建议建立“湖北磷材 Brain 知识页候选结构与发布门禁”，把接收演练中的脱敏资料结构转成知识页面候选、发布前检查表、权限过滤规则和 WAES 放行边界。
