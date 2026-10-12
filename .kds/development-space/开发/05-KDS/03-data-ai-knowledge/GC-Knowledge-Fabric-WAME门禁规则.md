---
doc_id: GPCF-DOC-63E07DE019
title: GC-Knowledge Fabric WAES门禁规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-WAES门禁规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-WAES门禁规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric WAES门禁规则

## 1. 定位

WAES 是 GC-Knowledge Fabric 的规则与门禁治理层，负责判断候选内容是否可以进入 RAG、写回、收益、积分、共享、冻结或委员会流程。WAES 不替代 KDS 存储、GFIS 执行或委员会裁决。

## 2. Gate 类型

| Gate | 判断事项 | 典型结果 |
|---|---|---|
| Source Gate | 来源等级、来源范围、来源时间 | passed / repair_required / blocked |
| Evidence Gate | 证据完整性、证据链、哈希或原件位置 | passed / human_required / blocked |
| DSR Gate | 租户、ACL、角色、供应链隔离 | passed / blocked |
| RAG Gate | 是否可引用、引用强度、脱敏要求 | safe / limited / repair_required / blocked |
| Writeback Gate | 是否可进入 GFIS / GPC / ERP / MES 候选写回 | passed / human_required / committee_required |
| Revenue Gate | 是否可计入正式收益、财务统计或潜在收益 | passed / committee_required / blocked |
| Contribution Gate | 是否可进入积分候选或确认积分 | passed / human_required / rejected |
| Bounty Gate | 是否可结算悬赏 | passed / dispute_required / blocked |
| Committee Gate | 是否触发委员会 | committee_required / not_required |
| Freeze Gate | 是否冻结对象、积分、收益、RAG 准入 | freeze_required / not_required |
| External Share Gate | 是否可对外共享 | passed / redaction_required / blocked |
| Sensitive Data Gate | 是否必须 metadata-only 或受控原件 | metadata_only / redaction_required / blocked |

## 3. 标准结果

- `passed`：通过当前门禁，但不代表业务已经完成。
- `blocked`：禁止进入目标动作。
- `repair_required`：需要补证、补字段、补来源或补权限。
- `human_required`：需要授权人员确认。
- `committee_required`：需要委员会流程。
- `redaction_required`：需要脱敏后才可继续。
- `freeze_required`：需要冻结对象或相关台账。
- `metadata_only`：只允许登记元数据和受控引用，不暴露原文。

## 4. 写回门禁底线

GFIS、GPC、ERP、MES 只接收已经确认的业务事实。AI、Agent 或 Connector 只能生成 `WritebackCandidate`，不得直接生成正式业务写回。

## 5. 收益与积分门禁底线

无到账收入不得进入正式收益分配。知识贡献、渠道贡献、潜在产值可以登记为候选或潜在记录，但不得自动转成正式收益依据。
