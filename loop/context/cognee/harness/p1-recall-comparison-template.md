---
doc_id: GPCF-DOC-7A2A6D4F05
title: COGNEE P1 召回对照表模板（并行）
project: GPC
related_projects: [GPC, WAES, GPCF]
domain: general
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/loop/context/cognee/harness/p1-recall-comparison-template.md
source_path: loop/context/cognee/harness/p1-recall-comparison-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# COGNEE P1 召回对照表模板（并行）

> 用于 `headroom`（主链）与 `cognee`（候选链）对照的最小字段。

| task_id | round_id | project_id | scenario | query | headroom_hit@k | cognee_hit@k | retrieval_match | token_before | token_after | latency_ms | recall_precision | marker_gate | answer_equivalence | write_requested | unauthorized_write_blocked | decision | note |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| `task-001` | `loop-round-xxx` | `GPCF` | `loop_gate` | `简短问题描述（脱敏）` | `0` | `0` | `false` | `1200` | `1140` | `120` | `0.00` | `pass` | `unknown` | `false` | `true` | `hold` | `首次样例` |

- `retrieval_match`：两个链路推荐候选是否等价（`true/false`）。
- `decision`：`hold|pass|fail`，与 WAES 票据/门禁统一口径。
- `write_requested` 和 `unauthorized_write_blocked` 仅记录 preview 阶段的内存写意向与拦截。
