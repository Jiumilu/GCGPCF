---
doc_id: GPCF-DOC-9377D0E7EE
title: Loop CodeGraph Active Drift Metrics Evidence
project: KDS
related_projects: [KDS, GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.md
source_path: docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop CodeGraph Active Drift Metrics Evidence

## 结论

本轮状态为 `codegraph_active_drift_metrics_evidenced`。

已执行 `GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002`：获得第二个 CodeGraph active drift metrics 数据点。Brain drift 已收敛为 zero pending，Studio drift 缩回到 watch threshold，GFIS residual 已清零。MTTD 仍保留起始数据，但 MTTR 仍不可用，因为当前监控仍处于 watch 而非完全闭合。

本轮不进入 Brain、Studio、GFIS 或其他项目业务开发，不执行 Brain/Studio `codegraph sync`，不提交、不推送、不部署。

## Metrics Window

| 指标 | 值 |
|---|---|
| previous_sample_utc | `2026-06-21T06:54:31Z` |
| current_sample_utc | `2026-06-26T04:19:31Z` |
| elapsed_minutes | 7045 |
| MTTD | seeded |
| MTTR | unavailable_until_watch_converges |

## Drift Metrics

| 项目 | 上一数据点 | 当前数据点 | Delta | 判定 |
|---|---:|---:|---:|---|
| GlobalCloud Brain | modified=56 | modified=0 | modified=-56 | drift_closed |
| GlobalCloud Studio | added=2, modified=5 | added=1, modified=2 | added=-1, modified=-3 | watch_with_pending_changes |
| GlobalCloud GFIS | added=1 | added=0 | cleared | residual_cleared |
| GlobalCoud GPCF | pending=0 after sync | pending=0 after sync | no change | local_governance_index_resynchronized |

## 授权边界

Git gate 当前为 `blocked`，原因是工作区存在本轮范围外的未跟踪敏感命名文件。该阻塞不改变 CodeGraph metrics 事实，但禁止提交、推送或状态升级。

Brain 与 Studio 的 sync-only closure 尚未授权：

- `codegraph sync` in GlobalCloud Brain: requires explicit authorization
- `codegraph sync` in GlobalCloud Studio: requires explicit authorization

## 决策

当前决策为 `continue_read_only_metrics_until_sync_only_authorized`。

理由：

- Brain green，drift 已关闭，当前不再增长。
- Studio 仍在 watch threshold 内，尚未需要 sync-only closure。
- Brain/Studio `.codegraph` 同步仍属于受控动作，但当前监控不需要立即执行。
- GPCF 自身因新增治理证据和 validator，允许并已执行本仓 `.codegraph` 收口。

## 下一轮输入

`GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`

目标：在继续只读采样与执行 Brain/Studio sync-only closure 之间建立授权边界；若未授权，则继续 read-only metrics sampling。
