---
doc_id: GPCF-DOC-666816F27E
title: Headroom LCX 回滚计划 20260622 001
project: KDS
related_projects: [KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md
source_path: docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX 回滚计划 20260622 001

## 回滚计划 ID

`HEADROOM-LCX-ROLLBACK-PLAN-20260622-001`

## 范围

本 rollback plan 适用于 `precheck_only_no_production_measurement`。

## 动作

| step | action | status |
|---|---|---|
| 1 | 保持 `HEADROOM_TELEMETRY=off` | required |
| 2 | 不启动 production proxy | required |
| 3 | 不启用 production SDK | required |
| 4 | 如生成 precheck cache，则删除临时 LCX cache | required before next stage |
| 5 | 保留 Harness evidence 与 validator output | required |
| 6 | 保持 `accepted=false`、`integrated=false`、`production_ready=false` | required |

## 禁止事项

- 不使用 production proxy。
- 不使用 production SDK。
- 不执行真实 KDS API write。
- 不执行 external API write。
- 不处理 sensitive raw material。
- 不执行 production token measurement。
