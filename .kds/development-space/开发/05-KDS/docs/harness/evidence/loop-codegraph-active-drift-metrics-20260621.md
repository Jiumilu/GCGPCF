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
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Active Drift Metrics Evidence

## 结论

本轮状态为 `codegraph_active_drift_metrics_evidenced`。

已执行 `GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002`：获得第二个 CodeGraph active drift metrics 数据点。Brain drift 继续增长，Studio drift 持续未闭合，GFIS residual 继续受控。MTTD 已有起始数据，MTTR 仍不可用，因为 drift 尚未关闭。

本轮不进入 Brain、Studio、GFIS 或其他项目业务开发，不执行 Brain/Studio `codegraph sync`，不提交、不推送、不部署。

## Metrics Window

| 指标 | 值 |
|---|---|
| previous_sample_utc | `2026-06-21T04:55:48Z` |
| current_sample_utc | `2026-06-21T06:54:31Z` |
| elapsed_minutes | 119 |
| MTTD | seeded |
| MTTR | unavailable_until_drift_closes |

## Drift Metrics

| 项目 | 上一数据点 | 当前数据点 | Delta | 判定 |
|---|---:|---:|---:|---|
| GlobalCloud Brain | modified=39 | modified=56 | modified=+17 | active_drift_growing |
| GlobalCloud Studio | added=2, modified=5 | added=2, modified=5 | no change | active_drift_persisting |
| GlobalCloud GFIS | added=1 | added=1 | no change | controlled_residual_persisting |
| GlobalCoud GPCF | pending=0 after sync | pending=0 after sync | no change | local_governance_index_resynchronized |

## 授权边界

Git gate 当前为 `blocked`，原因是工作区存在本轮范围外的未跟踪敏感命名文件。该阻塞不改变 CodeGraph metrics 事实，但禁止提交、推送或状态升级。

Brain 与 Studio 的 sync-only closure 尚未授权：

- `codegraph sync` in GlobalCloud Brain: requires explicit authorization
- `codegraph sync` in GlobalCloud Studio: requires explicit authorization

## 决策

当前决策为 `continue_read_only_metrics_until_sync_only_authorized`。

理由：

- Brain drift 仍增长，无法计算 MTTR。
- Studio drift 持续，无法计算 MTTR。
- Brain/Studio `.codegraph` 同步会改变项目仓索引，必须先获得明确授权。
- GPCF 自身因新增治理证据和 validator，允许并已执行本仓 `.codegraph` 收口。

## 下一轮输入

`GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003`

目标：在继续只读采样与执行 Brain/Studio sync-only closure 之间建立授权边界；若未授权，则继续 read-only metrics sampling。
