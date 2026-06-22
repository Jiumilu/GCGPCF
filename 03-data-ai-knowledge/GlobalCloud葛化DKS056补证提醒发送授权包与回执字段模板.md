---
doc_id: GPCF-DOC-49F4A296F5
title: GlobalCloud 葛化 DKS-056 补证提醒发送授权包与回执字段模板
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, XiaoC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化DKS056补证提醒发送授权包与回执字段模板.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化DKS056补证提醒发送授权包与回执字段模板.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 DKS-056 补证提醒发送授权包与回执字段模板

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-057`  
状态：`send_authorization_package_template`

## 1. 定位

本文承接 `GPCF-KDS-DKS-056`，把 7 个 `RMD-GH-D056-*` 补证提醒草案推进为未来可人工授权、可生成发送记录、可接收回执、可撤回纠错的字段模板。

本文只定义字段、状态和门禁；不生成真实发送授权，不发送飞书、小即、邮件或其它外部通知，不接收真实回执，不保存敏感原文，不写入 GFIS、WAES、KDS API、GPC、PVAOS、Finance、收益池、积分池或生产系统主账，不确认人工签认、委员会裁决、积分、收益、悬赏、到账、POD、质量或业务完成。

## 2. 输入依据

| 来源 | 本文使用方式 |
|---|---|
| `GPCF-KDS-DKS-056` 接收目录空状态与补证提醒门禁 | 沿用 `DAR/DSC/DAQ/RMD-GH-D056-*`、空扫描和 `draft_not_sent` 状态 |
| `GPCF-KDS-DKS-055` 派发授权信封门禁 | 沿用 `DAE-GH-D055-*`、发送前人工授权和负例拒收 |
| `GPCF-KDS-DKS-054` 执行包说明 | 沿用 `SUB-GH-D054-*` 责任方、字段、退回或阻断原因 |
| GFIS/GPCF 状态矩阵 | 保持 `real_business_lane=repair_required`，不把模板写成真实业务完成 |
| 文档治理、KDS 安全、防污染规则 | 保持本地镜像、TOKEN、RAG 和真实性边界 |

## 3. 多 agent 判断

本轮是单仓受控文档推进，输出对象涉及同一主文档、同一 LOOP 记录、同一文档控制登记册和同一 KDS 本地镜像；发送授权状态、回执状态和撤回纠错口径必须单一。并行 agent 不适合写入，本轮由主 agent 串行收口。

## 4. 发送授权包字段字典

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `sendAuthorizationPackageId` | 是 | 待生成 | `SAP-GH-D057-*` |
| `sourceReminderDraftRef` | 是 | 待绑定 | 绑定 `RMD-GH-D056-*` |
| `sourceActionRef` | 是 | 待绑定 | 绑定 `DAQ-GH-D056-*` |
| `sourceEnvelopeRef` | 是 | 待绑定 | 绑定 `DAE-GH-D055-*` |
| `manualSendAuthorizationRef` | 是 | 待确认 | 用户、治理负责人或委员会授权引用 |
| `authorizedByRole` | 是 | 待确认 | 授权角色，不得用系统或 AI 替代 |
| `authorizationScope` | 是 | 待确认 | 可发送对象、内容范围、用途和有效期 |
| `targetRecipientUnit` | 是 | 待确认 | 接收单位 |
| `targetRecipientRole` | 是 | 待确认 | 接收岗位或授权角色 |
| `recipientIdentityConfirmed` | 是 | `false` | 未确认时不得发送 |
| `dispatchChannel` | 是 | 待确认 | 飞书、小即、邮件、线下签收或其它受控渠道 |
| `dispatchChannelConfirmed` | 是 | `false` | 未确认时不得发送 |
| `classificationLevel` | 是 | 待确认 | DSR-L1/L2/L3 |
| `visibleScope` | 是 | `directed` | 默认定向可见 |
| `redactionMode` | 是 | `metadata_only_if_sensitive` | 敏感对象只留脱敏索引 |
| `messagePayloadRef` | 是 | 待生成 | 只允许引用草案或脱敏摘要，不写敏感原文 |
| `kdsBacklinkRef` | 是 | 待确认 | KDS 受控文档或对象回链 |
| `waesGateRecordRef` | 是 | 待确认 | WAES 规则记录、阻断或人工确认路径 |
| `expectedSendRecordRef` | 是 | 待生成 | `SRD-GH-D057-*` |
| `expectedReceiptTemplateRef` | 是 | 待生成 | `RCT-GH-D057-*` |
| `expiryOrReviewDate` | 是 | 待确认 | 过期或复核日期 |
| `sendAllowed` | 是 | `false` | 放行前必须保持 false |
| `sendExecuted` | 是 | `false` | 本轮必须为 false |
| `externalNotificationSent` | 是 | `false` | 本轮必须为 false |
| `nextAction` | 是 | `manual_send_authorization_required` | 下一动作 |

## 5. 七类发送授权包模板

| 授权包编号 | 绑定提醒草案 | 目标角色 | 当前缺口 | 当前状态 |
|---|---|---|---|---|
| `SAP-GH-D057-LY-001` | `RMD-GH-D056-LY-001` | 项目负责人 / 订单责任方 | 缺发送授权、接收人、渠道、客户确认路径 | waiting_manual_send_authorization |
| `SAP-GH-D057-QPOD-001` | `RMD-GH-D056-QPOD-001` | 质量 / 发货 / POD 责任人 | 缺质量、发货、POD 接收字段和回执路径 | waiting_manual_send_authorization |
| `SAP-GH-D057-OEM-001` | `RMD-GH-D056-OEM-001` | 目标工厂 / OEM 责任方 | 缺 OEM 与目标工厂责任拆分确认 | waiting_manual_send_authorization |
| `SAP-GH-D057-FIN-001` | `RMD-GH-D056-FIN-001` | 财务责任人 / 资料保管人 | 缺 DSR-L3 metadata_only、保管人、封存索引和财务授权 | waiting_manual_send_authorization |
| `SAP-GH-D057-WAES-001` | `RMD-GH-D056-WAES-001` | WAES 规则记录人 | 缺 WAES 规则记录、阻断或人工确认路径 | waiting_manual_send_authorization |
| `SAP-GH-D057-AI-001` | `RMD-GH-D056-AI-001` | GFIS AI 助手内测负责人 | 缺评测记录、缺陷状态和候选写回边界 | waiting_manual_send_authorization |
| `SAP-GH-D057-KGB-001` | `RMD-GH-D056-KGB-001` | KDS 记录人 / 缺口发起方 | 缺悬赏候选资源、验收规则、争议规则和委员会候选 | waiting_manual_send_authorization |

以上授权包均为模板，不代表真实授权已经存在。

## 6. 发送记录字段模板

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `sendRecordId` | 是 | `SRD-GH-D057-*` | 发送记录模板编号 |
| `sendAuthorizationPackageRef` | 是 | 待绑定 | 绑定 `SAP-GH-D057-*` |
| `sendAttempted` | 是 | `false` | 本轮必须为 false |
| `sendTimestamp` | 条件 | 空 | 真实发送后才允许填写 |
| `senderRole` | 条件 | 空 | 真实发送后才允许填写 |
| `targetRecipientUnit` | 是 | 待确认 | 来自授权包 |
| `targetRecipientRole` | 是 | 待确认 | 来自授权包 |
| `dispatchChannel` | 是 | 待确认 | 来自授权包 |
| `messagePayloadHash` | 条件 | 空 | 真实发送前不得伪造 |
| `kdsBacklinkRef` | 是 | 待确认 | 受控文档或对象回链 |
| `waesGateRecordRef` | 是 | 待确认 | 规则、阻断或人工确认路径 |
| `deliveryState` | 是 | `not_sent` | 允许值：`not_sent`、`sent_pending_receipt`、`send_blocked`、`revoked`、`correction_required` |
| `externalNotificationSent` | 是 | `false` | 本轮必须为 false |
| `businessFactCreated` | 是 | `false` | 发送记录不得创建业务事实 |

## 7. 回执字段模板

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `receiptTemplateId` | 是 | `RCT-GH-D057-*` | 回执字段模板编号 |
| `sendRecordRef` | 是 | 待绑定 | 绑定 `SRD-GH-D057-*` |
| `receiptExpected` | 是 | `true` | 仅表示未来应收，不表示已收到 |
| `receiptFound` | 是 | `false` | 本轮必须为 false |
| `receiptTimestamp` | 条件 | 空 | 真实回执后才允许填写 |
| `receiptSubmitterRole` | 条件 | 空 | 真实回执后才允许填写 |
| `receiptType` | 是 | 待确认 | `authorization_ack`、`evidence_submission`、`return_for_evidence`、`reject_with_reason`、`no_response` |
| `sourceRefs` | 条件 | 空 | 只允许脱敏索引、hash、封存编号或线下保管索引 |
| `classificationLevel` | 是 | 待确认 | DSR-L1/L2/L3 |
| `manualReviewRequired` | 是 | `true` | 回执不得自动变成确认事实 |
| `committeeRequired` | 条件 | 待判断 | 收益、重大违规、争议、潜在产值转正式产值时必须为 true |
| `waesDecisionState` | 是 | `manual_confirmation_required` | 允许 `governance_recorded`、`blocked`、`manual_confirmation_required`、`committee_review_required` |
| `ragAdmission` | 是 | `false` | 回执未经治理不得入 RAG 强引用 |
| `businessFactCreated` | 是 | `false` | 回执模板不得创建业务事实 |

## 8. 撤回与纠错规则

| 对象 | 触发条件 | 处理规则 | 状态 |
|---|---|---|---|
| `RVK-GH-D057-SEND-001` | 未授权发送、错发、发送到错误接收人 | 立即记录撤回候选，生成 WAES 阻断记录，必要时进入委员会 | revocation_template |
| `COR-GH-D057-PAYLOAD-001` | 载荷包含敏感原文、账户、金额、合同全文或未授权截图 | hard stop，删除外发候选载荷，保留脱敏索引和审计记录 | correction_required |
| `COR-GH-D057-STATUS-001` | 发送记录或回执写成业务完成 | 纠正为 `not_sent`、`manual_confirmation_required` 或 `committee_review_required` | correction_required |
| `COR-GH-D057-REVENUE-001` | 无到账事实却写入正式收入、积分或收益 | 撤销收益候选，转委员会或人工复核 | committee_review_required |
| `COR-GH-D057-RAG-001` | 未经治理的回执进入 RAG 强引用 | 移出 RAG，记录 WAES 阻断和治理缺口 | blocked |

撤回与纠错模板只定义未来处置规则，不表示已发生发送错误、撤回或纠错事实。

## 9. 负例拒收

| 负例编号 | 负例类型 | 拒收规则 |
|---|---|---|
| `NEG-D057-AUTH-AS-SENT-001` | 授权包模板被写成已发送 | `SAP-GH-D057-*` 不得替代 `SRD-GH-D057-*` 真实发送记录 |
| `NEG-D057-MISSING-AUTH-001` | 缺人工发送授权 | 缺 `manualSendAuthorizationRef` 时 `sendAllowed=false` |
| `NEG-D057-MISSING-RECIPIENT-001` | 缺接收人确认 | 缺接收单位、角色或身份确认时不得发送 |
| `NEG-D057-MISSING-CHANNEL-001` | 缺渠道确认 | 缺渠道和渠道确认时不得发送 |
| `NEG-D057-SENSITIVE-PAYLOAD-001` | 载荷包含敏感原文 | DSR-L3 原文、账户、金额、流水、合同全文或未授权截图必须 hard stop |
| `NEG-D057-FAKE-RECEIPT-001` | 伪造回执 | 模板、截图、口述、Loop 文档、本地镜像不得替代真实回执 |
| `NEG-D057-RAG-ADMISSION-001` | 未治理回执入 RAG | 回执未经人工或 WAES 治理不得进入强引用 |
| `NEG-D057-STATUS-UPGRADE-001` | 状态越权升级 | 不得出现 accepted、complete、integrated、verified 业务完成叙事 |
| `NEG-D057-POINTS-REVENUE-001` | 自动确认积分收益 | 无人工或委员会确认不得确认积分、产值、收益、额度、悬赏或扣罚 |

## 10. WAES、RAG、积分收益边界

| 对象 | 当前口径 |
|---|---|
| WAES | 只记录规则、阻断、人工确认路径或委员会路径，不审批具体业务事务 |
| RAG | 授权包、发送记录模板和回执模板不得进入强引用；只可作为治理说明或缺口索引候选 |
| 知识积分 | 只记录候选贡献，不确认积分 |
| 产值积分 | 无到账事实时只可记录潜在产值贡献候选 |
| 收益池 | 不因授权包、发送模板或回执模板产生收益分配 |
| AI 额度 | 自购额度仍先自用，不进入统一收益池 |
| 悬赏 | 只保持候选，不发布、不冻结、不结算 |
| 委员会 | 仅在重大违规、收益分配、潜在产值转正式产值、跨单位权益争议或悬赏结算时进入 |

## 11. 全局断言

```text
sendAuthorizationPackagesPrepared=7
sendRecordTemplatesPrepared=7
receiptTemplatesPrepared=7
revocationCorrectionTemplatesPrepared=5
manualSendAuthorizationsFound=0
sendAllowed=false
sendExecuted=false
sendRecordsCreated=0
receiptsFound=0
externalNotificationSent=false
realKdsApiWrite=false
waesWrite=false
gfisWrite=false
businessLedgerWrite=false
financeLedgerWrite=false
settlementWrite=false
ragAdmission=false
createsConfirmationFact=false
createsCommitteeDecision=false
statusUpgrade=false
```

## 12. 完成定义

本文完成表示：

1. 7 个补证提醒草案已有发送授权包模板。
2. 7 个发送记录字段模板已形成。
3. 7 个回执字段模板已形成。
4. 撤回、纠错、负例拒收、WAES/RAG/积分收益边界已明确。
5. 本文纳入 LOOP、文档控制和 KDS 本地镜像。

本文不表示：

1. 任何真实发送授权已经获得。
2. 任何提醒已经发送。
3. 任何外部通知已经发送。
4. 任何真实回执已经收到。
5. 任何人工确认或委员会裁决已经完成。
6. 任何真实 GFIS、WAES、KDS API、财务或生产系统已经写入。
7. GFIS `real_business_lane=repair_required` 已关闭。
8. 本专题可升级 `accepted`、`complete` 或 `integrated`。

## 13. 下一轮建议

建议 `GPCF-KDS-DKS-058` 进入“葛化 DKS-057 发送授权包人工确认接收扫描空状态与授权缺口台账”，只扫描是否存在人工发送授权文件，建立空状态、缺口台账和责任方补证路径；未获得显式授权前仍不发送外部通知。
