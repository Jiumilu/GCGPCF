---
doc_id: GPCF-DOC-D241F6E17C
title: GlobalCloud 葛化 DKS-054 执行包派发授权信封与负例拒收门禁
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, XiaoC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud葛化DKS054执行包派发授权信封与负例拒收门禁.md
source_path: 03-data-ai-knowledge/GlobalCloud葛化DKS054执行包派发授权信封与负例拒收门禁.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 葛化 DKS-054 执行包派发授权信封与负例拒收门禁

日期：2026-06-19  
轮次：`GPCF-KDS-DKS-055`  
状态：`dispatch_authorization_envelope_draft`

## 1. 定位

本文承接 `GPCF-KDS-DKS-054`，为 7 个可填写执行包建立派发前的授权信封、接收人确认、派发渠道确认、回执路径和负例拒收门禁。

本文只形成派发前治理规则和本地受控草案，不派发真实请求，不发送外部通知，不接收真实材料，不保存敏感原文，不写入 GFIS、WAES、KDS API、GPC、PVAOS、Finance、收益池、积分池或生产系统主账，不确认人工签认、委员会裁决、积分、收益、悬赏、到账、POD、质量或业务完成。

## 2. 输入依据

| 来源 | 本文使用方式 |
|---|---|
| `GPCF-KDS-DKS-054` 执行包说明 | 将 `SUB-GH-D054-*` 转成派发授权信封草案 |
| `GPCF-KDS-DKS-053` dry-run 验收视图 | 沿用人工确认、RAG 阻断、金融敏感和缺口队列边界 |
| 葛化订单运行母版 | 沿用预运营期订单、统一编号、OEM 责任拆分和 SOP 候选写回边界 |
| GFIS AI 助手三件套模板 | 沿用 AI 输出只作为候选、建议、缺陷和待人工核验对象 |
| 积分收益额度悬赏争议规则 | 沿用知识积分、产值积分、收益池、AI 额度、悬赏和争议的确认边界 |
| GFIS/GPCF 状态矩阵 | 保持 `real_business_lane=repair_required`，不把本地草案写成真实业务完成 |

## 3. 多 agent 判断

本轮是单仓文档门禁推进，授权信封字段、拒收规则、LOOP 记录、KDS 本地镜像和文档控制登记册必须保持单一口径；不启动多 agent 写入。只读核查可用于后续复核，但本轮由主 agent 串行写入。

## 4. 派发授权信封总规则

| 规则 | 口径 |
|---|---|
| 信封编号 | 使用 `DAE-GH-D055-*`；每个信封必须绑定一个 `SUB-GH-D054-*` 执行包 |
| 默认状态 | `authorization_envelope_draft`、`dispatch_preflight_blocked`、`waiting_manual_authorization` 或 `candidate_only` |
| 放行前置 | 人工授权、接收人身份、派发渠道、KDS 回链、WAES 规则记录、密级脱敏、回执路径均满足后才可讨论派发 |
| 缺一即阻断 | 任一放行前置缺失时，`dispatchAllowed=false`，不得生成外部通知 |
| 金融与 DSR-L3 | 默认 `blocked_by_default`，只允许 metadata_only、hash、封存编号或线下保管索引 |
| AI 输出 | 只能生成候选事实、候选字段、候选 SOP、缺口和风险，不得替代人工确认或委员会裁决 |
| 底座 11 池 | 本轮只产生底座候选元数据、缺口和 hold 记录，不写积分池、收益池、争议池、数据池正式事实 |

## 5. 授权信封字段字典

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `dispatchAuthorizationEnvelopeId` | 是 | 待生成 | `DAE-GH-D055-*` |
| `sourceSubmissionPackRef` | 是 | 待绑定 | 绑定 `SUB-GH-D054-*` |
| `targetRecipientUnit` | 是 | 待确认 | 接收单位，不可用泛称替代 |
| `targetRecipientRole` | 是 | 待确认 | 接收岗位或授权角色 |
| `recipientIdentityConfirmed` | 是 | `false` | 必须由人工或受控授权记录确认 |
| `dispatchChannel` | 是 | 待确认 | 飞书、小即、邮件、线下签收或其它受控渠道 |
| `dispatchChannelConfirmed` | 是 | `false` | 渠道未确认时不得派发 |
| `manualAuthorizationRef` | 是 | 待确认 | 用户、治理负责人或委员会授权引用 |
| `authorizationScope` | 是 | 待确认 | 可派发对象、可见范围、有效期和目的 |
| `allowedUse` | 是 | `read_and_fill_candidate` | 只能阅读、填写、补证、退回或提交人工确认 |
| `forbiddenUse` | 是 | `no_business_fact_write` | 不得写主账、不得确认收益、不得宣称完成 |
| `classificationLevel` | 是 | 待确认 | DSR-L1/L2/L3 |
| `visibleScope` | 是 | `directed` | 默认定向可见 |
| `redactionMode` | 是 | `metadata_only_if_sensitive` | 敏感对象只留脱敏索引 |
| `kdsBacklinkRef` | 是 | 待确认 | KDS 受控文档、对象或登记册回链 |
| `waesGateRecordRef` | 是 | 待确认 | WAES 规则记录、阻断或人工确认路径 |
| `expectedReceiptRef` | 是 | 待确认 | 未来回执、签收、退回或 hold 记录编号 |
| `expiryOrReviewDate` | 是 | 待确认 | 过期或复核日期 |
| `dispatchAllowed` | 是 | `false` | 放行前必须保持 false |
| `dispatchSent` | 是 | `false` | 本轮必须为 false |
| `externalNotificationSent` | 是 | `false` | 本轮必须为 false |
| `nextAction` | 是 | `manual_authorization_required` | 下一动作 |

## 6. 七类执行包授权信封草案

| 信封编号 | 绑定执行包 | 目标接收方 | 派发前置 | 当前状态 |
|---|---|---|---|---|
| `DAE-GH-D055-LY-001` | `SUB-GH-D054-LY-001` | 项目负责人 / 订单责任方 | 客户确认缺口、报价来源、责任主体、人工授权、渠道确认 | dispatch_preflight_blocked |
| `DAE-GH-D055-QPOD-001` | `SUB-GH-D054-QPOD-001` | 质量 / 发货 / POD 责任人 | 样箱、质量、发货、POD 索引字段与回执路径 | dispatch_preflight_blocked |
| `DAE-GH-D055-OEM-001` | `SUB-GH-D054-OEM-001` | 目标工厂 / OEM 承接方 | 现代精工等 OEM 事实责任与目标工厂未来承接责任拆分 | dispatch_preflight_blocked |
| `DAE-GH-D055-FIN-001` | `SUB-GH-D054-FIN-001` | 财务责任人 / 资料保管人 | DSR-L3 metadata_only、封存编号、财务授权、委员会候选路径 | dispatch_preflight_blocked |
| `DAE-GH-D055-WAES-001` | `SUB-GH-D054-WAES-001` | WAES 规则记录人 | 规则内记录、阻断、人工确认或委员会路径 | waiting_manual_authorization |
| `DAE-GH-D055-AI-001` | `SUB-GH-D054-AI-001` | GFIS AI 助手内测负责人 | AI 输出评测、缺陷、候选写回和候选 SOP no_write 边界 | candidate_only |
| `DAE-GH-D055-KGB-001` | `SUB-GH-D054-KGB-001` | KDS 记录人 / 缺口发起方 | 知识缺口、资料回收、悬赏候选、资源冻结和验收规则 | candidate_only |

以上信封均为草案。未出现明确人工授权、接收人确认、渠道确认、WAES 记录和 KDS 回链前，均不得派发。

## 7. 负例拒收门禁

| 负例编号 | 负例类型 | 拒收规则 | 处置 |
|---|---|---|---|
| `NEG-D055-ORAL-001` | 口头或聊天式授权 | 只有电话、口头、即时消息片段、未备案截图，不能作为派发授权 | 进入 `open_hold`，要求补正式授权引用 |
| `NEG-D055-LOOPDOC-001` | 把 LOOP 或 KDS 本地镜像当授权 | LOOP 记录、KDS 本地镜像、文档控制通过不等于外部派发授权 | 拒收，保持 `dispatchAllowed=false` |
| `NEG-D055-MISSING-RECIPIENT-001` | 缺接收人确认 | 未确认接收单位、岗位或授权角色时不得派发 | 退回补接收人身份 |
| `NEG-D055-MISSING-CHANNEL-001` | 缺渠道确认 | 未确认飞书、小即、邮件或线下签收等受控渠道时不得派发 | 退回补渠道 |
| `NEG-D055-MISSING-KDS-BACKLINK-001` | 缺 KDS / WAES 回链 | 缺来源对象、KDS 回链、WAES 规则记录或回执路径 | 拒收并要求补证 |
| `NEG-D055-DEMO-FIXTURE-001` | Demo / mock / fixture / synthetic | 演示、样例、测试 fixture、synthetic/dev-only 不能作为真实授权或真实回执 | 拒收，不形成业务事实 |
| `NEG-D055-SENSITIVE-PAYLOAD-001` | 敏感原文外发 | DSR-L3 原文、账户、完整金额、流水、合同全文、未授权截图不得进入派发载荷 | hard stop，必要时进委员会违规候选 |
| `NEG-D055-STATUS-UPGRADE-001` | 状态越权升级 | 文档中出现 `accepted`、`complete`、`integrated`、`verified` 作为业务完成声明 | 拒收并标记状态污染风险 |
| `NEG-D055-BOUNTY-PUBLISH-001` | 悬赏越权发布 | 未经委员会或授权规则确认、未冻结资源、未定义验收和争议规则即发布悬赏 | 阻断，转委员会候选 |

## 8. 派发 hold 记录

每个未满足前置的信封必须生成或对应一个 hold 槽位。hold 只记录缺口，不代表已派发或已接收。

| holdId | 来源信封 | blockedReason | requiredRemediation | ownerRole | state | releaseAllowed |
|---|---|---|---|---|---|---|
| `DHR-GH-D055-LY-001` | `DAE-GH-D055-LY-001` | 缺人工授权、接收人、渠道、客户确认路径 | 补授权引用、接收人身份、渠道和回执路径 | 项目负责人 / 订单责任方 | open_hold | false |
| `DHR-GH-D055-QPOD-001` | `DAE-GH-D055-QPOD-001` | 缺质量、发货、POD 接收与回执路径 | 补责任人、字段范围、回执路径和 WAES 记录 | 质量 / 发货 / POD 责任人 | open_hold | false |
| `DHR-GH-D055-OEM-001` | `DAE-GH-D055-OEM-001` | 缺 OEM 与目标工厂责任确认 | 补责任拆分、产能调度需求和争议路径 | 目标工厂 / OEM 责任方 | open_hold | false |
| `DHR-GH-D055-FIN-001` | `DAE-GH-D055-FIN-001` | DSR-L3 缺财务授权与脱敏载荷 | 补 metadata_only、保管人、封存索引和委员会候选路径 | 财务责任人 | open_hold | false |
| `DHR-GH-D055-WAES-001` | `DAE-GH-D055-WAES-001` | 缺 WAES 规则记录授权 | 补规则记录人、规则口径和阻断路径 | WAES 规则记录人 | open_hold | false |
| `DHR-GH-D055-AI-001` | `DAE-GH-D055-AI-001` | AI 输出仍为候选 | 补评测人、缺陷处理和 no_write 记录 | AI 助手内测负责人 | open_hold | false |
| `DHR-GH-D055-KGB-001` | `DAE-GH-D055-KGB-001` | 悬赏未获授权且资源未冻结 | 补委员会候选、资源冻结、验收和争议规则 | KDS 记录人 / 缺口发起方 | open_hold | false |

## 9. WAES、RAG、DSR 与 AI 调用边界

| 对象 | 当前口径 |
|---|---|
| WAES | 只确认规则、阻断或人工确认路径；规则以内可记录，但不自动业务确认 |
| RAG | 本轮信封、hold 和负例均不得进入强引用；只可作为治理说明或缺口索引候选 |
| DSR-L1 | 可作为通用规则说明，仍需注明来源 |
| DSR-L2 | 只在授权项目范围内使用脱敏索引和摘要 |
| DSR-L3 | 默认 blocked_by_default；财务、合同、账户、完整金额和金融凭证原文不得派发 |
| AI 建议 | 可提出 SOP 建议、字段候选、缺口、风险和映射；必须区分建议、候选、待确认、阻断和人工确认 |

## 10. 积分、收益、AI 额度与悬赏

| 对象 | 本轮允许 | 本轮禁止 |
|---|---|---|
| 知识积分 | 记录候选贡献来源和缺口补证需求 | 写入 confirmed_points |
| 产值积分 | 记录潜在产值贡献候选 | 把无到账事实写成正式产值 |
| 收益池 | 记录未来分配前置条件 | 到账前分配收益或确认收入 |
| AI 自购额度 | 记录自用范围和计量字段候选 | 纳入统一收益池或共享分配 |
| 贡献 / 共享额度 | 记录候选用途和备案需求 | 未确认即发放额度 |
| 悬赏 | 记录悬赏候选、冻结需求、验收规则和争议规则 | 发布悬赏、冻结资源或结算 |
| 争议 | 记录争议候选和委员会路径 | 主 agent 或 AI 自行裁决 |

正式收入以到账为准；开票只进入统计和财务流程口径。任何收益分配、重大违规扣减、潜在产值转正式产值、跨单位争议和悬赏结算都必须进入人工或委员会机制。

## 11. 全局断言

本轮所有对象必须满足：

```text
dispatchAllowed=false
dispatchSent=false
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

1. DKS-054 的 7 个执行包已有派发授权信封草案。
2. 派发前置字段、默认阻断状态和缺一即阻断规则已明确。
3. 9 类负例拒收规则已形成。
4. 派发 hold 记录槽位已形成。
5. WAES、RAG、DSR、AI、积分、收益、额度、悬赏和委员会边界已明确。
6. 本文纳入 LOOP、文档控制和 KDS 本地镜像。

本文不表示：

1. 任何真实授权已经获得。
2. 任何请求已经派发。
3. 任何外部通知已经发送。
4. 任何真实材料已经收到。
5. 任何人工确认或委员会裁决已经完成。
6. 任何真实 GFIS、WAES、KDS API、财务或生产系统已经写入。
7. GFIS `real_business_lane=repair_required` 已关闭。
8. 本专题可升级 `accepted`、`complete` 或 `integrated`。

## 13. 下一轮建议

建议 `GPCF-KDS-DKS-056` 进入“葛化 DKS-055 派发授权信封接收目录空状态 hold/action queue 与责任方补证提醒门禁”，只建立授权信封接收目录、空状态扫描、hold/action queue、责任方补证提醒草案和继续阻断规则；未获得显式授权前仍不发送外部通知。
