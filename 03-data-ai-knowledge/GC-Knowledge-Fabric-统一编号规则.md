---
doc_id: GPCF-DOC-B69A039079
title: GC-Knowledge Fabric 统一编号规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-统一编号规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-统一编号规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 统一编号规则

日期：2026-06-20  
状态：`draft`  
适用范围：KDS、OKF、WAES、KWE、Brain、PKC、MMC、Harness、LOOP、GFIS/GPC 写回候选与治理账本。  

## 1. 目标

统一编号规则用于保证每个知识对象、来源、证据、候选、门禁、工单、确认、决议、收益、额度、悬赏和 LOOP 记录可审计、可回放、可追责。

编号只证明对象被登记，不证明对象已确认、已验收、已写回或已结算。

## 2. 编号结构

标准结构：

```text
{PREFIX}-{SCOPE}-{SUBJECT}-{YYYYMM}-{SEQ}
```

字段说明：

| 字段 | 含义 | 示例 |
|---|---|---|
| `PREFIX` | 对象类型前缀 | `KOBJ`、`SRC`、`EVD`、`FC` |
| `SCOPE` | 项目或业务域 | `GH`、`HBLC`、`GFIS`、`KDS` |
| `SUBJECT` | 主题或池标签 | `ORD`、`CAP`、`POL`、`RAG` |
| `YYYYMM` | 年月 | `202606` |
| `SEQ` | 4 位序号 | `0001` |

示例：

```text
KOBJ-GH-ORD-202606-0001
FC-GH-ORD-202606-0001
WBC-GFIS-ORD-202606-0001
GATE-WAES-RAG-202606-0001
LOOP-GPCF-KDS-202606-0001
```

## 3. 前缀表

| 前缀 | 对象 | 默认状态 |
|---|---|---|
| `KOBJ` | KnowledgeObject | `draft` 或 `candidate` |
| `SRC` | SourceRecord | `registered` |
| `EVD` | EvidenceRecord | `candidate` |
| `FC` | FactCandidate | `candidate` |
| `SC` | SOPCandidate | `candidate` |
| `WBC` | WritebackCandidate | `candidate` |
| `GAP` | GapRecord | `open` |
| `BNT` | BountyRecord | `candidate` |
| `CON` | ContributionRecord | `candidate` |
| `REV` | RevenueRecord | `candidate` |
| `QUO` | QuotaRecord | `registered` |
| `DSP` | DisputeRecord | `open` |
| `DEC` | DecisionRecord | `draft` |
| `EVT` | EventRecord | `recorded` |
| `GATE` | WAESGateResult | `pending` |
| `KWE` | KnowledgeWorkItem | `open` |
| `CONF` | ConfirmationRecord | `pending` |
| `HEV` | HarnessEvidenceRecord | `recorded` |
| `LOOP` | LOOPRecord | `open` |
| `AUK` | AgentUsedKnowledge | `recorded` |

## 4. Scope 代码

| 代码 | 含义 |
|---|---|
| `GH` | 葛化 |
| `HBLC` | 湖北磷材 |
| `GFIS` | GFIS |
| `GPC` | GPC |
| `KDS` | KDS |
| `WAES` | WAES |
| `BRAIN` | Brain |
| `PKC` | PKC |
| `MMC` | MMC |
| `GPCF` | GPCF 项目群治理 |
| `SC` | supply_chain 通用对象 |
| `ORG` | 组织级复用对象 |

## 5. Subject 代码

| 代码 | 对应池或主题 |
|---|---|
| `ORD` | 订单池 |
| `TRN` | 运力池 |
| `CAP` | 产能池 |
| `FIN` | 资金池 |
| `POL` | 政策池 |
| `EQP` | 装备池 |
| `DAT` | 数据池 |
| `ENG` | 能源池 |
| `MAT` | 原料池 |
| `TAL` | 人才池 |
| `SCN` | 场景池 |
| `RAG` | RAG 准入 |
| `ACL` | 权限 |
| `GOV` | 治理 |
| `SOP` | SOP |
| `WB` | 写回候选 |
| `REV` | 收益 |
| `BNT` | 悬赏 |

## 6. 状态与编号关系

编号一经创建不得复用。对象状态变化不得改编号，只能追加事件、门禁结果、确认记录和 lineage。

| 操作 | 是否生成新编号 |
|---|---|
| 草稿变候选 | 否 |
| 候选进入审核 | 否 |
| 补证后重新提交 | 否，追加 EventRecord |
| 被确认 | 否，追加 ConfirmationRecord |
| 被委员会裁决 | 否，追加 DecisionRecord |
| 写回候选被批准 | 否，追加 WritebackCandidate 状态 |
| 模板复制成新项目事实候选 | 是，新建对象编号 |
| 对象被替代 | 新对象生成新编号，旧对象进入 `superseded` |

## 7. 碰撞与保留规则

1. 同一 `PREFIX-SCOPE-SUBJECT-YYYYMM` 下序号单调递增。
2. 不允许人工复用历史编号。
3. 导入外部资料时保留外部编号为 `externalRef`，不得替代内部编号。
4. AI 生成候选必须使用 `generatedBy=ai`，并默认 `trustLevel=T5`。
5. 生产业务系统主键只能记录为 `businessSystemRef`，不得替代 KDS 编号。

## 8. 验收标准

P0 编号规则通过条件：

1. 每类核心对象有前缀。
2. 葛化、湖北磷材、GFIS、KDS、WAES、GPCF 有 scope 代码。
3. KDS 十一池有 subject 代码。
4. 编号不表达确认状态。
5. 状态变化不重写编号。
6. 模板复制成事实候选时必须生成新编号。
