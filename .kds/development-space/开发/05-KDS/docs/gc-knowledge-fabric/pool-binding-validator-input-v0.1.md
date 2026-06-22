---
doc_id: GPCF-DOC-B7709DC69E
title: GC-Knowledge Fabric Pool Binding Validator 输入清单 v0.1
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/pool-binding-validator-input-v0.1.md
source_path: docs/gc-knowledge-fabric/pool-binding-validator-input-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric Pool Binding Validator 输入清单 v0.1

## 1. 定位

本文档定义 P0-D2 pool binding validator 的最小输入清单。该清单仅用于 dry-run 校验，不写入真实 KDS，不写 GFIS/GPC，不形成正式事实。

## 2. 最小输入字段

| 字段 | 必填 | 说明 |
|---|---|---|
| id | 是 | GCKF 标准编号 |
| tenantId | 是 | 租户或治理主体 |
| domain | 是 | private/workspace/project/org/supply_chain/public/governance |
| objectType | 是 | source、evidence、fact_candidate、sop_candidate、writeback_candidate 等 |
| lifecycle | 是 | draft/candidate/reviewing/verified/accepted/published/archived/frozen |
| ragAdmission | 是 | safe/limited/repair_required/blocked/sensitive_metadata_only |
| confirmationStatus | 是 | not_required/ai_checked/human_required/human_confirmed/committee_required/committee_confirmed/rejected |
| poolRefs | 是 | KDS 十一池 poolCode 数组 |
| sourceRefs | 是 | 来源引用 |
| evidenceRefs | 否 | 证据引用 |
| metadataOnly | 否 | 是否仅元数据入库 |
| noWriteAssertion | 是 | P0 必须为 true |

## 3. dry-run 样例

```json
{
  "id": "GCKF-GPCF-PROJECT-FACTCAND-20260621-0001",
  "tenantId": "GPCF",
  "domain": "project",
  "objectType": "fact_candidate",
  "lifecycle": "candidate",
  "ragAdmission": "repair_required",
  "confirmationStatus": "human_required",
  "poolRefs": ["ORDER", "CAPACITY", "DATA"],
  "sourceRefs": ["SRC-GEHUA-ORDER-001"],
  "evidenceRefs": [],
  "metadataOnly": false,
  "noWriteAssertion": true
}
```

## 4. validator 必须拦截

- `poolRefs` 为空。
- `domain` 为空或不在七个治理域内。
- candidate 对象被标记为 `accepted`、`published` 或 `written_back`。
- `noWriteAssertion` 不是 true。
- 敏感对象缺少 `metadataOnly` 或 `blocked` 标记。
- `ragAdmission=blocked` 但仍标记为可强引用。
