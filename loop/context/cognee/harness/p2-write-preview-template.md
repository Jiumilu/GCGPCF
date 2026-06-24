---
doc_id: GPCF-DOC-7A2A6D4F06
title: COGNEE P2 写入预览模板（最小字段）
project: GPC
related_projects: [GPC, GPCF]
domain: general
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/loop/context/cognee/harness/p2-write-preview-template.md
source_path: loop/context/cognee/harness/p2-write-preview-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# COGNEE P2 写入预览模板（最小字段）

> 用于受控环境下对 `remember_preview / forget_preview / retrieve_preview` 的对照跑，记录授权边界与阻断结果。

| task_id | round_id | project_id | scenario | operation | owner | payload_tier | waes_decision | write_requested | write_allowed | owner_authorization_present | unauthorized_write_blocked | token_before | token_after | latency_ms | marker_gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `cognee-p2-task-001` | `loop-round-xxx` | `GPCF` | `loop_gate` | `remember_preview` | `GPCF` | `preview` | `pass` | `true` | `false` | `false` | `true` | `1200` | `1100` | `90` | `pass` |

- `operation`: `remember_preview` / `forget_preview` / `retrieve_preview`
- `payload_tier`: 仅允许 `preview` 或 `non_business_only`
- `harness_evidence_ref`：必须为已提交 evidence 记录
- `write_allowed` 在无生产授权时预期为 `false`
