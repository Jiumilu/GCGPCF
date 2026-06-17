---
doc_id: GPCF-DOC-F72C6A953D
title: GlobalCloud 底座可用知识闭环率评分脚本 dry-run 规格
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md
source_path: 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 底座可用知识闭环率评分脚本 dry-run 规格

日期：2026-06-17  
状态：`dry_run_spec_only`  
建议脚本名：`validate_base_knowledge_closure_score_dry_run.py`

## 1. 定位

本文承接 DKS-041《GlobalCloud 底座可用知识闭环率计算样表与字段字典》，定义“底座可用知识闭环率评分脚本”的 dry-run 规格，包括 JSON schema、示例输入、示例输出、计算断言、hard-stop 断言和边界。

本文不是脚本实现，不执行真实评分入账，不写真实 KDS API，不关闭缺口，不发布悬赏，不结算积分，不分配收益，不发放 AI 额度，不进入 RAG 准入，不进入指挥舱强引用，也不写 GFIS、GPC、PVAOS、WAES 或任何业务系统主账。

## 2. dry-run 输入对象

输入对象建议命名为 `BaseKnowledgeClosureScoreInput`。

```json
{
  "baseKnowledgeId": "BKC-HBLC-FEA-202606-0001",
  "sourceProject": "湖北磷材",
  "kdsPoolRefs": ["装备池", "产能池", "政策池", "数据池", "场景池"],
  "enhancedLedgerRefs": ["贡献账本", "SOP账本", "悬赏池"],
  "statusCoverageRate": 100,
  "dqScore": 65,
  "evidencePassRate": 60,
  "consistencyRate": 80,
  "automationEffectivenessRate": 0,
  "writebackClosureRate": 30,
  "oneVoteVetoFlags": [],
  "sourceRefs": ["virtual://hblc/fea/source-summary"],
  "evidenceLevel": "E2_candidate",
  "humanReviewStatus": "pending",
  "waesRecordStatus": "planned",
  "settlementStatus": "prohibited_before_acceptance",
  "ragInclude": false
}
```

## 3. JSON schema 草案

```json
{
  "type": "object",
  "required": [
    "baseKnowledgeId",
    "sourceProject",
    "kdsPoolRefs",
    "statusCoverageRate",
    "dqScore",
    "evidencePassRate",
    "consistencyRate",
    "automationEffectivenessRate",
    "writebackClosureRate",
    "oneVoteVetoFlags"
  ],
  "properties": {
    "baseKnowledgeId": {"type": "string", "minLength": 1},
    "sourceProject": {"type": "string", "minLength": 1},
    "kdsPoolRefs": {
      "type": "array",
      "minItems": 1,
      "items": {"type": "string"}
    },
    "enhancedLedgerRefs": {
      "type": "array",
      "items": {"type": "string"}
    },
    "statusCoverageRate": {"type": "number", "minimum": 0, "maximum": 100},
    "dqScore": {"type": "number", "minimum": 0, "maximum": 100},
    "evidencePassRate": {"type": "number", "minimum": 0, "maximum": 100},
    "consistencyRate": {"type": "number", "minimum": 0, "maximum": 100},
    "automationEffectivenessRate": {"type": "number", "minimum": 0, "maximum": 100},
    "writebackClosureRate": {"type": "number", "minimum": 0, "maximum": 100},
    "oneVoteVetoFlags": {
      "type": "array",
      "items": {"type": "string"}
    },
    "sourceRefs": {
      "type": "array",
      "items": {"type": "string"}
    },
    "evidenceLevel": {"type": "string"},
    "humanReviewStatus": {"type": "string"},
    "waesRecordStatus": {"type": "string"},
    "settlementStatus": {"type": "string"},
    "ragInclude": {"type": "boolean"}
  },
  "additionalProperties": false
}
```

## 4. dry-run 输出对象

输出对象建议命名为 `BaseKnowledgeClosureScoreDryRunResult`。

```json
{
  "baseKnowledgeId": "BKC-HBLC-FEA-202606-0001",
  "calculatedClosureRate": 63.25,
  "decisionBand": "repair_candidate",
  "hardStop": false,
  "allowedUse": ["repair", "bounty_candidate", "manual_confirmation_candidate"],
  "forbiddenUse": ["rag_strong_reference", "command_center_strong_reference", "business_ledger_write", "settlement"],
  "writebackCandidates": [
    {
      "target": "evidencePassRate",
      "reason": "third_party_source_missing",
      "status": "candidate_only"
    }
  ],
  "auditMessages": [
    "status coverage is complete but fact maturity is below strong reference threshold",
    "manual confirmation is pending"
  ]
}
```

## 5. 计算断言

| assertionId | 规则 | 预期 |
|---|---|---|
| `CALC-001` | 六维字段均存在且为 0-100 数值 | 允许计算 |
| `CALC-002` | `calculatedClosureRate = statusCoverageRate*0.20 + dqScore*0.25 + evidencePassRate*0.20 + consistencyRate*0.15 + automationEffectivenessRate*0.10 + writebackClosureRate*0.10` | 小数保留两位 |
| `CALC-003` | 85-100 且无否决项 | `safe_reuse_candidate` |
| `CALC-004` | 70-84 且无否决项 | `limited_report_candidate` |
| `CALC-005` | 60-69 且无否决项 | `repair_candidate` |
| `CALC-006` | 50-59 且无否决项 | `return_for_source` |
| `CALC-007` | 0-49 且无否决项 | `blocked_or_invalid` |
| `CALC-008` | 任一一票否决项存在 | 强制 `blocked_or_invalid` |

## 6. hard-stop 断言

| hardStopId | 条件 | 输出 |
|---|---|---|
| `HS-NO-KDS-POOL` | `kdsPoolRefs` 为空 | `hardStop=true`; `decisionBand=blocked_or_invalid` |
| `HS-LEDGER-ORPHAN` | `enhancedLedgerRefs` 非空且 `kdsPoolRefs` 为空 | `VETO-LEDGER-ORPHAN` |
| `HS-NO-SOURCE` | `sourceRefs` 为空且 `evidencePassRate > 0` | `VETO-NO-SOURCE` |
| `HS-AI-AS-FACT` | `oneVoteVetoFlags` 包含 `VETO-AI-AS-FACT` | 阻断 RAG、报告、主账和结算 |
| `HS-REVENUE-MISCLAIM` | 包含 `VETO-REVENUE-MISCLAIM` | 触发委员会候选，不得入收益池 |
| `HS-ORDER-MISCLAIM` | 包含 `VETO-ORDER-MISCLAIM` | 不得写 GFIS 主账或订单池正式事实 |
| `HS-KDS-API-CLAIM` | 包含 `VETO-KDS-API-CLAIM` | 输出本地镜像误认风险 |
| `HS-UNAUTHORIZED-SETTLEMENT` | 包含 `VETO-UNAUTHORIZED-SETTLEMENT` | 不得结算积分、收益或 AI 额度 |
| `HS-RAG-MISMATCH` | `ragInclude=true` 但 `decisionBand` 不是 `safe_reuse_candidate` | 强制 RAG 阻断 |
| `HS-SETTLEMENT-MISMATCH` | `settlementStatus` 不是 `prohibited_before_acceptance` 且无人工确认记录 | 强制结算阻断 |

## 7. 示例输入与输出

### 7.1 repair candidate

输入：`BKC-HBLC-FEA-202606-0001`  
期望输出：

```json
{
  "calculatedClosureRate": 63.25,
  "decisionBand": "repair_candidate",
  "hardStop": false,
  "allowedUse": ["repair", "bounty_candidate", "manual_confirmation_candidate"]
}
```

### 7.2 limited report candidate

输入：`BKC-HBLC-IND-202606-0001`  
期望输出：

```json
{
  "calculatedClosureRate": 75.25,
  "decisionBand": "limited_report_candidate",
  "hardStop": false,
  "allowedUse": ["limited_report_candidate"],
  "forbiddenUse": ["rag_strong_reference", "command_center_strong_reference", "business_ledger_write"]
}
```

### 7.3 veto override

输入：`BKC-HBLC-ORD-202606-0002`  
期望输出：

```json
{
  "calculatedClosureRate": 34.5,
  "decisionBand": "blocked_or_invalid",
  "hardStop": true,
  "hardStopReasons": ["VETO-REVENUE-MISCLAIM"],
  "allowedUse": ["committee_review_candidate"],
  "forbiddenUse": ["settlement", "revenue_pool", "business_ledger_write", "rag_strong_reference"]
}
```

## 8. dry-run 退出码建议

| exitCode | 含义 |
|---:|---|
| 0 | 所有输入结构有效，且无 hard-stop |
| 1 | 输入结构或 schema 校验失败 |
| 2 | 存在 hard-stop 或一票否决项，属于预期阻断 |
| 3 | 计算结果与期望 fixture 不一致 |
| 4 | 发现越权输出，例如准入、结算、主账写入或真实 API 声明 |

## 9. 禁止输出

dry-run 脚本不得输出：

1. 真实 KDS API 同步完成声明。
2. RAG 准入完成声明。
3. 指挥舱强引用许可。
4. GFIS、GPC、PVAOS、WAES 或其他业务系统主账写入声明。
5. 积分、收益、AI 额度结算完成声明。
6. 悬赏发布完成声明。
7. 委员会裁决完成声明。
8. accepted 或 integrated 状态升级声明。

## 10. 最小 fixture 集

| fixtureId | 输入对象 | 预期 decisionBand | 预期 exitCode | 目的 |
|---|---|---|---:|---|
| `FIX-BKC-REPAIR-001` | `BKC-HBLC-FEA-202606-0001` | `repair_candidate` | 0 | 验证 60-69 修复候选 |
| `FIX-BKC-LIMITED-001` | `BKC-HBLC-IND-202606-0001` | `limited_report_candidate` | 0 | 验证 70-84 有限报告候选 |
| `FIX-BKC-BLOCK-001` | `BKC-HBLC-ORD-202606-0001` | `blocked_or_invalid` | 2 | 验证无来源否决 |
| `FIX-BKC-REVENUE-VETO-001` | `BKC-HBLC-ORD-202606-0002` | `blocked_or_invalid` | 2 | 验证收入误认否决 |
| `FIX-BKC-RAG-MISMATCH-001` | 任一 `repair_candidate` 且 `ragInclude=true` | `blocked_or_invalid` | 2 | 验证 RAG 越权阻断 |
| `FIX-BKC-LEDGER-ORPHAN-001` | 增强账本非空且无 KDS 11 池 | `blocked_or_invalid` | 2 | 验证账本游离阻断 |

## 11. 后续实现边界

若后续进入脚本实现，应遵守：

1. 只读取本地 fixture 和受控文档，不访问真实外部 API。
2. 只输出 JSON、Markdown evidence 和候选写回建议。
3. 不修改真实 KDS、WAES、GFIS、GPC、PVAOS 或其他系统。
4. 不创建真实悬赏、真实结算、真实收益分配或真实 AI 额度发放。
5. 所有 hard-stop 必须优先于分数。
6. 所有输出必须保留 `candidate_only`、`dry_run` 或 `blocked` 状态。

## 12. DKS-043 建议

下一轮建议实现 `validate_base_knowledge_closure_score_dry_run.py` 的最小本地 dry-run 脚本与 fixture，不接入真实系统，只验证 schema、计算、hard-stop 和禁止输出。
