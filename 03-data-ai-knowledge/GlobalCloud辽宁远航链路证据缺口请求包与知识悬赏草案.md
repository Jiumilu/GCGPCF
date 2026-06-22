---
doc_id: GPCF-DOC-A948E73BB3
title: GlobalCloud 辽宁远航链路证据缺口请求包与知识悬赏草案
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud辽宁远航链路证据缺口请求包与知识悬赏草案.md
source_path: 03-data-ai-knowledge/GlobalCloud辽宁远航链路证据缺口请求包与知识悬赏草案.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GlobalCloud 辽宁远航链路证据缺口请求包与知识悬赏草案

日期：2026-06-17
状态：v0.1 受控悬赏草案
适用范围：葛化预运营期订单母版、辽宁远航链路、现代精工 OEM 过渡、KDS 知识缺口积分、知识悬赏、WAES 证据门禁。

## 1. 定位

本文是 `GPCF-KDS-DKS-005` 的专项产物，用于把辽宁远航链路的证据缺口转成可治理的知识缺口请求包和知识悬赏草案。

本文只定义缺口、悬赏、提交、验收和结算结构，不证明任何真实客户确认、样箱反馈、OEM 生产事实、质量报告、POD、金融凭证、转量产批准或收益事实已经取得。

## 2. 缺口对象模型

```text
KnowledgeGapRequest
  -> KnowledgeGapBounty
  -> KnowledgeGapSubmission
  -> WAES / 业务负责人 / 委员会验收
  -> BountySettlement
  -> ContributionEvent
  -> CandidatePoint / ConfirmedPoint
  -> 可选 PotentialValueRecord
```

所有缺口必须保留：

1. 来源对象。
2. 发起主体。
3. 缺口类型。
4. 必需证据。
5. 密级。
6. 可见范围。
7. 悬赏资源。
8. 验收角色。
9. 结算规则。
10. 争议入口。

## 3. 辽宁远航缺口请求总表

| KGR 编号 | 缺口 | 类型 | 密级建议 | 可见范围 | 验收角色 | 当前状态 |
|---|---|---|---|---|---|---|
| `KGR-GH-EVD-202606-0001` | 客户确认函 | EVD | DSR-L2 | 定向 | 项目负责人 + WAES | candidate |
| `KGR-GH-EVD-202606-0002` | 23 个样箱测试签收与反馈 | EVD | DSR-L1/DSR-L2 | 项目组内 | 质量负责人 + WAES | candidate |
| `KGR-GH-EVD-202606-0003` | 现代精工 OEM 生产事实 | EVD | DSR-L2/DSR-L3 | 定向/私密 | 项目负责人 + OEM 授权人 + WAES | candidate |
| `KGR-GH-EVD-202606-0004` | 质量报告与成品放行 | EVD | DSR-L2 | 项目组内 | 质量负责人 + WAES | candidate |
| `KGR-GH-EVD-202606-0005` | 发货与 POD | EVD | DSR-L2 | 定向 | GPC/POD 责任人 + WAES | candidate |
| `KGR-GH-EVD-202606-0006` | 金融凭证与到账/开票索引 | EVD | DSR-L3 | 私密 | 财务负责人 + WAES | candidate |
| `KGR-GH-BIZ-202606-0007` | 转量产批准 | BIZ | DSR-L2/DSR-L3 | 定向 | 项目负责人 + 委员会 | candidate |
| `KGR-GH-EVD-202606-0008` | KDS 写入回执 / WAES confirmation | EVD | DSR-L1 | 项目组内 | KDS/WAES 责任人 | candidate |

## 4. 悬赏草案

| KGB 编号 | 关联 KGR | 建议激励 | 是否允许 AI 额度 | 是否允许服务权益 | 结算口径 |
|---|---|---|---|---|---|
| `KGB-GH-EVD-202606-0001` | `KGR-GH-EVD-202606-0001` | 积分 + 服务权益 | 是 | 是 | 证据通过后给知识积分；如形成收入再追溯潜在产值 |
| `KGB-GH-EVD-202606-0002` | `KGR-GH-EVD-202606-0002` | 积分 + AI 额度 | 是 | 否 | 可按样箱数量部分结算 |
| `KGB-GH-EVD-202606-0003` | `KGR-GH-EVD-202606-0003` | 积分 + 服务权益 | 是 | 是 | 需 OEM 授权与密级确认后结算 |
| `KGB-GH-EVD-202606-0004` | `KGR-GH-EVD-202606-0004` | 积分 | 否 | 否 | 质量负责人和 WAES 双确认 |
| `KGB-GH-EVD-202606-0005` | `KGR-GH-EVD-202606-0005` | 积分 + AI 额度 | 是 | 否 | POD 完整后结算，不确认资金事实 |
| `KGB-GH-EVD-202606-0006` | `KGR-GH-EVD-202606-0006` | 积分 | 否 | 否 | 只奖励脱敏索引和凭证结构，不公开金额细节 |
| `KGB-GH-BIZ-202606-0007` | `KGR-GH-BIZ-202606-0007` | 积分 + 潜在产值贡献 | 是 | 是 | 转量产批准成立后可计潜在产值；到账后再转正式产值 |
| `KGB-GH-EVD-202606-0008` | `KGR-GH-EVD-202606-0008` | 积分 | 否 | 否 | KDS/WAES 回执有效后结算 |

悬赏资源来源可为合作单位自有积分、项目激励池或体系激励池。未冻结资源前，悬赏不得发布为有效任务。

## 5. 提交包字段

| 字段 | 必填 | 说明 |
|---|---:|---|
| submissionId | 是 | `KGS-GH-202606-0001` 格式 |
| bountyId | 是 | 关联 KGB |
| submitterId | 是 | 个人或单位 |
| submitterRole | 是 | 项目成员、合作单位、财务、质量、OEM 授权人、外部专家 |
| evidenceRefs | 是 | 原始证据、脱敏索引或受控副本 |
| redactionLevel | 是 | none、partial、metadata_only |
| classificationLevel | 是 | DSR-L0 / DSR-L1 / DSR-L2 / DSR-L3 |
| sourceAuthenticityStatement | 是 | 提交人对来源真实性的声明 |
| aiAssisted | 是 | 是否使用 AI 辅助整理 |
| businessFactClaimed | 是 | 默认 false；不得由提交包直接确认业务事实 |
| waesGateStatus | 是 | pending、governance_recorded、governance_blocked、governance_rejected |
| settlementCandidate | 否 | 候选积分或潜在产值建议 |

## 6. 验收规则

| 缺口 | 最低通过条件 | 不通过条件 |
|---|---|---|
| 客户确认函 | 可识别客户、项目、产品/样箱/订单关系、确认人、日期和来源 | 只有口述、截图无来源、无确认人或无法识别客户 |
| 23 个样箱反馈 | 每个样箱有编号或对应关系，至少包含签收、测试反馈或问题记录之一 | 仅有“已测试”笼统描述，无样箱明细 |
| OEM 生产事实 | 能区分现代精工 OEM 承接和葛化目标工厂责任，含生产/质量/入库/发货至少两类证据 | 把 OEM 事实写成葛化自建工厂已投产事实 |
| 质量报告 | 有检验对象、指标、结果、检验人/机构、时间和放行状态 | 无检验对象或无法追溯到样箱/订单 |
| POD | 有发货单、签收主体、签收时间、附件或物流回执 | 只有发货计划，无签收事实 |
| 金融凭证 | 只提交脱敏索引、凭证类型、开票/到账状态引用和保管责任人 | 暴露敏感金额或把凭证包写成资金事实确认 |
| 转量产批准 | 有客户或内部授权方的明确批准记录，或委员会待确认事项记录 | 仅有销售预期或口头可能性 |
| KDS/WAES 回执 | 有真实回执或受控 confirmation 引用 | 用 `.kds` 本地镜像替代真实 API/流程回执 |

## 7. 结算规则

1. 未通过验收的提交不产生确认积分。
2. 部分通过可按有效证据比例结算候选积分。
3. DSR-L3 私密证据可只提交脱敏索引，具体原件由授权角色线下核验。
4. 如证据后续被判定失真，一般问题按影响范围酌情溯源扣除；重大违规按事实比例或全部扣除。
5. 转量产、正式订单或业务收入未发生前，只可计知识贡献或潜在产值贡献。
6. 到账后才可进入正式收入和收益池分配口径；开票仅用于统计和财务过程口径。

## 8. 委员会与争议

进入争议的场景：

1. 多方提交同一证据，贡献比例无法确认。
2. 证据密级、可见范围或可披露性存在冲突。
3. 证据真实性、完整性或来源权属被质疑。
4. 潜在产值贡献是否可追溯存在争议。
5. 悬赏结算比例无法协商。

争议必须形成 `DisputeCase` 和 `DecisionRecord`。委员会按多数决裁决，用户保留治理急停权但不做具体裁决。

## 9. DKS-006 建议

下一轮建议建立：

```text
GPCF-KDS-DKS-006：
湖北磷材拓厂项目知识库与新工厂复制模板，把葛化母版转成 HBLC 的拓厂评估表、原料/行业/订单知识源清单和预运营期订单加权模型。
```

## 10. 待用户确认

1. 悬赏资源初期是否先使用项目激励池，而不动用合作单位自有积分？
2. 辽宁远航客户确认函是否可以作为 DSR-L2 定向悬赏，不公开原件？
3. 23 个样箱反馈是否允许按样箱逐项部分结算？
4. 现代精工 OEM 事实是否需要先由合作单位确认可披露范围？
5. 金融凭证是否只建立脱敏索引，不进入共享知识库正文？

本文当前只完成缺口请求和悬赏草案，不证明任何悬赏已发布、提交已验收、积分已确认或收益已分配。
