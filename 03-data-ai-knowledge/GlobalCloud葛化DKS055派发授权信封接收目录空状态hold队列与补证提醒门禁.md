---
doc_id: GPCF-DOC-AACA2824CD
title: GlobalCloud 葛化 DKS-055 派发授权信封接收目录空状态 hold 队列与补证提醒门禁
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, XiaoC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化DKS055派发授权信封接收目录空状态hold队列与补证提醒门禁.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化DKS055派发授权信封接收目录空状态hold队列与补证提醒门禁.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 DKS-055 派发授权信封接收目录空状态 hold 队列与补证提醒门禁

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-056`  
状态：`dispatch_authorization_receiving_empty_hold_gate`

## 1. 定位

本文承接 `GPCF-KDS-DKS-055`，把 7 个 `DAE-GH-D055-*` 派发授权信封草案推进为可扫描、可挂起、可补证、可生成提醒草案的受控接收目录状态。

本文只建立本地治理对象、空状态扫描口径、hold/action queue 和补证提醒草案；不创建真实接收目录文件，不派发请求，不发送飞书、小即、邮件或其它外部通知，不接收真实材料，不保存敏感原文，不写入 GFIS、WAES、KDS API、GPC、PVAOS、Finance、收益池、积分池或生产系统主账，不确认人工签认、委员会裁决、积分、收益、悬赏、到账、POD、质量或业务完成。

## 2. 输入依据

| 来源 | 本文使用方式 |
|---|---|
| `GPCF-KDS-DKS-055` 派发授权信封与负例拒收门禁 | 沿用 `DAE-GH-D055-*`、`DHR-GH-D055-*`、负例拒收和全局断言 |
| `GPCF-KDS-DKS-054` 执行包说明 | 沿用 `SUB-GH-D054-*` 责任方、字段、退回或阻断原因 |
| `GPCF-KDS-DKS-053` dry-run 验收视图 | 沿用人工确认、RAG 阻断、金融敏感和缺口队列边界 |
| 葛化订单运行母版 | 沿用预运营期订单、OEM 责任拆分和候选 SOP 写回边界 |
| GFIS/GPCF 状态矩阵 | 保持 `real_business_lane=repair_required`，不把本地空扫描写成真实业务完成 |

## 3. 多 agent 判断

本轮仍是单仓受控文档推进，输出对象涉及同一 DKS 主文档、同一 LOOP 记录、同一文档控制登记册和同一 KDS 本地镜像。并行 agent 容易造成 hold 状态、提醒状态和门禁证据冲突；本轮不启动多 agent 写入，由主 agent 串行收口。

## 4. 接收目录对象规则

| 规则 | 口径 |
|---|---|
| 接收目录编号 | 使用 `DAR-GH-D056-*`，每个目录绑定一个 `DAE-GH-D055-*` |
| 扫描记录编号 | 使用 `DSC-GH-D056-*`，记录空状态、异常文件、有效授权数和回执数 |
| hold/action 编号 | 使用 `DAQ-GH-D056-*`，把缺授权、缺接收人、缺渠道、缺 KDS/WAES 回链转成责任方动作 |
| 提醒草案编号 | 使用 `RMD-GH-D056-*`，只能是 `draft_not_sent` |
| 默认状态 | `receiving_directory_defined`、`empty_scan`、`open_hold`、`action_required`、`reminder_draft_not_sent` |
| 缺一即阻断 | 缺人工授权、接收人、渠道、KDS 回链、WAES 记录、密级脱敏或回执路径时，`releaseAllowed=false` |
| 禁止外发 | 未获得显式人工授权前，不得发送任何外部通知或真实补证请求 |

## 5. 接收目录空状态扫描矩阵

| 接收目录编号 | 绑定信封 | 责任方向 | 扫描记录 | expectedFiles | filesFound | validAuthorizations | receiptsFound | 当前状态 |
|---|---|---|---|---:|---:|---:|---:|---|
| `DAR-GH-D056-LY-001` | `DAE-GH-D055-LY-001` | 项目负责人 / 订单责任方 | `DSC-GH-D056-LY-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-QPOD-001` | `DAE-GH-D055-QPOD-001` | 质量 / 发货 / POD 责任人 | `DSC-GH-D056-QPOD-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-OEM-001` | `DAE-GH-D055-OEM-001` | 目标工厂 / OEM 承接方 | `DSC-GH-D056-OEM-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-FIN-001` | `DAE-GH-D055-FIN-001` | 财务责任人 / 资料保管人 | `DSC-GH-D056-FIN-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-WAES-001` | `DAE-GH-D055-WAES-001` | WAES 规则记录人 | `DSC-GH-D056-WAES-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-AI-001` | `DAE-GH-D055-AI-001` | GFIS AI 助手内测负责人 | `DSC-GH-D056-AI-001` | 1 | 0 | 0 | 0 | empty_scan |
| `DAR-GH-D056-KGB-001` | `DAE-GH-D055-KGB-001` | KDS 记录人 / 缺口发起方 | `DSC-GH-D056-KGB-001` | 1 | 0 | 0 | 0 | empty_scan |

空状态只证明当前未收到合格授权文件或回执，不证明责任方已被通知、已拒绝、已确认或已完成补证。

## 6. hold/action queue

| actionId | 来源目录 | 来源信封 | actionType | actionOwner | missingPreconditions | currentState | releaseAllowed |
|---|---|---|---|---|---|---|---|
| `DAQ-GH-D056-LY-001` | `DAR-GH-D056-LY-001` | `DAE-GH-D055-LY-001` | 补人工授权、接收人、渠道和客户确认路径 | 项目负责人 / 订单责任方 | `manualAuthorizationRef`、`recipientIdentityConfirmed`、`dispatchChannelConfirmed`、`customerConfirmationRef` | open_hold | false |
| `DAQ-GH-D056-QPOD-001` | `DAR-GH-D056-QPOD-001` | `DAE-GH-D055-QPOD-001` | 补质量、发货、POD 接收字段和回执路径 | 质量 / 发货 / POD 责任人 | `qualityEvidenceRefs`、`deliveryEvidenceRefs`、`podRefs`、`expectedReceiptRef` | open_hold | false |
| `DAQ-GH-D056-OEM-001` | `DAR-GH-D056-OEM-001` | `DAE-GH-D055-OEM-001` | 补 OEM 与目标工厂责任拆分和产能调度需求 | 目标工厂 / OEM 责任方 | `responsibilitySplit`、`productionFactOwner`、`futureOperationOwner`、`capacityDispatchNeed` | open_hold | false |
| `DAQ-GH-D056-FIN-001` | `DAR-GH-D056-FIN-001` | `DAE-GH-D055-FIN-001` | 补 DSR-L3 metadata_only、保管人、封存索引和财务授权 | 财务责任人 / 资料保管人 | `custodianRole`、`redactionStatus`、`sourceHashOrOfflineSeal`、`manualAuthorizationRef` | open_hold | false |
| `DAQ-GH-D056-WAES-001` | `DAR-GH-D056-WAES-001` | `DAE-GH-D055-WAES-001` | 补 WAES 规则记录、阻断或人工确认路径 | WAES 规则记录人 | `waesGateRecordRef`、`classificationLevel`、`ruleDecision`、`blockedReason` | open_hold | false |
| `DAQ-GH-D056-AI-001` | `DAR-GH-D056-AI-001` | `DAE-GH-D055-AI-001` | 补 AI 评测人、缺陷处理、候选写回 no_write 记录 | GFIS AI 助手内测负责人 | `EvalRecord`、`DefectRecord`、`WritebackCandidate`、`forbiddenOutputDetected` | open_hold | false |
| `DAQ-GH-D056-KGB-001` | `DAR-GH-D056-KGB-001` | `DAE-GH-D055-KGB-001` | 补悬赏候选资源、验收规则、争议规则和委员会候选 | KDS 记录人 / 缺口发起方 | `frozenResourceState`、`acceptanceRule`、`disputeRule`、`committeeCandidateRef` | open_hold | false |

## 7. 补证提醒草案

提醒草案只用于人工复核，不代表已发送。

| reminderId | 来源 action | 目标角色 | 草案目的 | 禁止内容 | 状态 |
|---|---|---|---|---|---|
| `RMD-GH-D056-LY-001` | `DAQ-GH-D056-LY-001` | 项目负责人 / 订单责任方 | 请求补授权、接收人、渠道、客户确认路径 | 不写客户原文、不称已派发、不称已确认 | draft_not_sent |
| `RMD-GH-D056-QPOD-001` | `DAQ-GH-D056-QPOD-001` | 质量 / 发货 / POD 责任人 | 请求补样箱、质量、发货、POD 索引或缺口说明 | 不写 POD 原件、不称已签收 | draft_not_sent |
| `RMD-GH-D056-OEM-001` | `DAQ-GH-D056-OEM-001` | 目标工厂 / OEM 责任方 | 请求补 OEM 当前责任与目标工厂未来责任拆分 | 不称目标工厂已投产 | draft_not_sent |
| `RMD-GH-D056-FIN-001` | `DAQ-GH-D056-FIN-001` | 财务责任人 / 资料保管人 | 请求补 metadata_only、保管人、封存索引和授权 | 不写账户、完整金额、流水、合同全文 | draft_not_sent |
| `RMD-GH-D056-WAES-001` | `DAQ-GH-D056-WAES-001` | WAES 规则记录人 | 请求补规则记录、阻断或人工确认路径 | 不把 WAES 规则写成业务批准 | draft_not_sent |
| `RMD-GH-D056-AI-001` | `DAQ-GH-D056-AI-001` | GFIS AI 助手内测负责人 | 请求补评测记录、缺陷状态、候选写回边界 | 不写 confirmed_fact、accepted、complete、integrated | draft_not_sent |
| `RMD-GH-D056-KGB-001` | `DAQ-GH-D056-KGB-001` | KDS 记录人 / 缺口发起方 | 请求补悬赏候选、资源冻结、验收和争议规则 | 不发布悬赏、不冻结资源、不结算 | draft_not_sent |

## 8. 发送前人工授权门禁

任一提醒草案从 `draft_not_sent` 进入可发送前，必须同时满足：

1. `manualSendAuthorizationRef` 存在且可追溯。
2. `targetRecipientUnit`、`targetRecipientRole` 和 `recipientIdentityConfirmed=true`。
3. `dispatchChannel` 与 `dispatchChannelConfirmed=true`。
4. `classificationLevel`、`visibleScope` 和 `redactionMode` 已确认。
5. DSR-L3 对象只包含 metadata_only、hash、封存编号或线下保管索引。
6. `kdsBacklinkRef` 与 `waesGateRecordRef` 已登记。
7. `expectedReceiptRef` 已定义。
8. `forbiddenUse` 明确包含 `no_business_fact_write`、`no_status_upgrade`、`no_revenue_or_points_confirmation`。

任一条件不满足时，提醒状态必须保持 `draft_not_sent`，并把缺口回写到 `DAQ-GH-D056-*`。

## 9. 负例拒收

| 负例编号 | 负例类型 | 拒收规则 |
|---|---|---|
| `NEG-D056-DRAFT-SENT-001` | 草案被写成已发送 | `draft_not_sent` 不得改写成 `sent`、`delivered`、`read` 或 `confirmed` |
| `NEG-D056-EMPTY-AS-REJECTED-001` | 空目录被写成责任方拒绝 | `filesFound=0` 只代表未收到，不代表拒绝 |
| `NEG-D056-LOOP-AS-AUTH-001` | LOOP 记录当授权 | LOOP 通过不等于人工发送授权 |
| `NEG-D056-KDS-MIRROR-AS-API-001` | KDS 本地镜像当真实 API 同步 | 本地镜像不等于真实 KDS API 写入 |
| `NEG-D056-SENSITIVE-REMINDER-001` | 提醒草案包含敏感原文 | DSR-L3 原文、账户、金额、流水、合同全文或未授权截图必须 hard stop |
| `NEG-D056-STATUS-UPGRADE-001` | 提醒草案宣称业务完成 | 不得出现 accepted、complete、integrated、verified 业务完成叙事 |
| `NEG-D056-BOUNTY-AUTO-PUBLISH-001` | 自动发布悬赏 | 未经人工或委员会确认，不得发布、冻结、验收或结算悬赏 |

## 10. WAES、RAG、积分收益边界

| 对象 | 当前口径 |
|---|---|
| WAES | 只记录规则、阻断、人工确认路径或委员会路径，不审批具体业务事务 |
| RAG | 空扫描、hold 和提醒草案不得进入强引用；仅可作为治理说明或缺口索引候选 |
| 知识积分 | 只记录候选贡献，不确认积分 |
| 产值积分 | 无到账事实时只可记录潜在产值贡献候选 |
| 收益池 | 不因提醒草案、空扫描或 hold 产生收益分配 |
| AI 额度 | 自购额度仍先自用，不进入统一收益池 |
| 悬赏 | 只保持候选，不发布、不冻结、不结算 |

## 11. 全局断言

```text
receivingDirectoriesDefined=true
filesFound=0
validAuthorizations=0
receiptsFound=0
reminderDraftsPrepared=7
remindersSent=0
externalNotificationSent=false
dispatchAllowed=false
releaseAllowed=false
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

1. DKS-055 的 7 个派发授权信封已有接收目录对象。
2. 7 个接收目录均记录为空扫描状态。
3. 7 个 hold/action queue 已形成。
4. 7 个补证提醒草案已形成且状态为 `draft_not_sent`。
5. 发送前人工授权门禁、负例拒收、WAES/RAG/积分收益边界已明确。
6. 本文纳入 LOOP、文档控制和 KDS 本地镜像。

本文不表示：

1. 任何真实授权已经获得。
2. 任何提醒已经发送。
3. 任何外部通知已经发送。
4. 任何真实材料已经收到。
5. 任何人工确认或委员会裁决已经完成。
6. 任何真实 GFIS、WAES、KDS API、财务或生产系统已经写入。
7. GFIS `real_business_lane=repair_required` 已关闭。
8. 本专题可升级 `accepted`、`complete` 或 `integrated`。

## 13. 下一轮建议

建议 `GPCF-KDS-DKS-057` 进入“葛化 DKS-056 补证提醒发送授权包与回执字段模板”，只定义未来提醒发送前的人工授权包、发送记录字段、回执字段、撤回和纠错规则；未获得显式授权前仍不发送外部通知。
