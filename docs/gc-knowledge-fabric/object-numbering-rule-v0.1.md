---
doc_id: GPCF-DOC-AA6D94609E
title: GC-Knowledge Fabric 对象编号规则 v0.1
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/object-numbering-rule-v0.1.md
source_path: docs/gc-knowledge-fabric/object-numbering-rule-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 对象编号规则 v0.1

## 1. 定位

本文档定义 P0 阶段 GC-Knowledge Fabric 的最小对象编号规则。编号用于追踪候选、事实、证据、门禁、工单、台账和 LOOP evidence，不代表对象已经被确认或正式入账。

## 2. 编号结构

标准编号格式：

```text
GCKF-{TENANT}-{DOMAIN}-{OBJECT_TYPE}-{YYYYMMDD}-{SEQ}
```

示例：

```text
GCKF-GPCF-PROJECT-FACTCAND-20260621-0001
```

## 3. 字段说明

| 字段 | 说明 | 示例 |
|---|---|---|
| `GCKF` | 固定前缀 | GCKF |
| `TENANT` | 租户或治理主体 | GPCF、GEHUA、HBLC |
| `DOMAIN` | 知识治理域 | PRIVATE、WORKSPACE、PROJECT、ORG、SUPPLY、PUBLIC、GOV |
| `OBJECT_TYPE` | 对象类型缩写 | KO、SRC、EVD、FACTCAND、SOPCAND、WBCAND、GAP、BOUNTY、CONTRIB、REV、QUOTA、DECISION、GATE、WORK、LOOP |
| `YYYYMMDD` | 创建日期 | 20260621 |
| `SEQ` | 当日顺序号 | 0001 |

## 4. P0 约束

- 编号只表示对象已登记，不表示已确认。
- AI 生成对象必须使用 candidate 类缩写。
- `FACTCAND` 不得直接改写为 `FACT`；必须通过 WAES、KWE、人工/委员会确认和 Harness evidence。
- `WBCAND` 不得直接写业务系统。
- 涉及合同、金融凭证、POD、质量争议的对象默认附加 `metadata_only=true` 或 `blocked` 状态。

## 5. validator 检查

- `id` 符合编号格式。
- `tenant`、`domain`、`object_type` 非空。
- candidate 类对象未被标记为 accepted/published/written_back。
- 高价值对象至少有一个 `poolRef`。
