---
doc_id: GPCF-DOC-19C576EDF8
title: GC-Knowledge Fabric 四池台账 P0 压缩规则
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/four-pool-ledger-p0-policy.md
source_path: docs/gc-knowledge-fabric/four-pool-ledger-p0-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 四池台账 P0 压缩规则

## 1. 定位

本文件定义知识积分池、收益池、AI 额度池、知识悬赏池在 P0 阶段的最小台账边界。

P0 只允许登记、候选、审查、冻结和证据引用，不允许自动积分确认、收益分配、额度划拨或悬赏结算。

## 2. 四池 P0 允许动作

| 池 | P0 允许动作 | P0 禁止动作 |
|---|---|---|
| 知识积分池 | 登记贡献、候选分、确认状态、证据引用 | 自动确认积分、自动扣减、自动兑换 |
| 收益池 | 登记正式/开票/潜在/渠道/知识潜在价值口径 | 自动分配、潜在收益自动转正式收益 |
| AI 额度池 | 登记额度类型、owner、amount、usedAmount、是否可进收益池 | 自购额度进入统一收益池、自动划拨 |
| 悬赏池 | 登记缺口、提交、验收状态、争议期、候选奖励 | 自动结算、跳过争议期、AI 直接验收 |

## 3. P0 硬边界

1. 没有实际到账收入，不得进入正式收益分配。
2. 开票收入只能进入财务统计，不能自动分配。
3. 潜在收益、渠道机会、知识潜在价值不能自动转为正式收益。
4. 知识贡献可以登记候选分，但确认分必须经过人工或委员会确认。
5. 自购 AI 额度不得进入统一收益池。
6. 悬赏结算必须经过 WAES gate、人工验收、争议期结束；AI 初审只作为建议。
7. 重大争议或违规风险必须可冻结贡献、收益、额度或悬赏。

## 4. P0 验收条件

- OKF 中有四池 P0 汇总 policy。
- Shared Types 中有四池 ledger boundary、allowed actions、blocked actions 和 no-write 断言。
- Validator 能检查四池覆盖、P0 允许/禁止动作、正式收益口径、自购额度边界、悬赏争议期和 no-write 断言。
