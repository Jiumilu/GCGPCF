---
doc_id: GPCF-DOC-C51A5428BB
title: Loop CodeGraph Active Drift Monitor Evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.md
source_path: docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Active Drift Monitor Evidence

## 结论

本轮状态为 `codegraph_active_drift_monitor_evidenced`。

下一阶段目标已建立并执行：以 CodeGraph 为 LOOP 监控输入，持续跟踪 Brain 与 Studio 的 active drift，保持 GFIS residual 受控，并把 GPCF 自身治理索引纳入闭环。

本轮不进入 Brain、Studio、GFIS 或其他项目的业务开发，不提交、不推送、不部署，不升级 `accepted`、`integrated` 或 `production_ready`。

## 阶段目标

| 项 | 内容 |
|---|---|
| 目标 | 监控 Brain 与 Studio active drift，收集 MTTD/MTTR 起始证据 |
| 范围 | GPCF/LOOP 治理证据、validator、CodeGraph 状态采样 |
| 模式 | L1/L2 governance evidence and validator only |
| 成功标准 | drift 可量化、residual 可区分、下一轮输入可回放 |

## 监控结果

| 项目 | 状态 | Pending | 趋势 | 说明 |
|---|---|---:|---|---|
| GlobalCloud Brain | active_drift | modified=36 | drift_increased | 上轮为 modified=32，本轮增至 36 |
| GlobalCloud Studio | active_drift | added=2, modified=2 | drift_persisted | 与上轮一致，仍未闭合 |
| GlobalCloud GFIS | controlled_residual | added=1 | controlled | 继续按 `large_generated_validator_exception_candidate` 处理 |
| GlobalCoud GPCF | up_to_date_after_final_sync | none | governance_index_closed | 本轮治理文件新增后已完成 GPCF 自身 `.codegraph` 收口 |

`.codegraph/` Git 状态检查保持为 0 条，不把本地索引写入 Git。

## MTTD/MTTR 起始证据

| 指标 | 当前状态 |
|---|---|
| detected_at_utc | `2026-06-21T04:55:48Z` |
| MTTD seed | available |
| MTTR seed | unavailable |
| 未闭合原因 | Brain 与 Studio 仍为活动仓漂移；本轮没有授权同步 Brain/Studio `.codegraph` |
| 降本证据 | CodeGraph 已把排查范围从项目群不确定性缩小到 Brain modified=36、Studio added=2/modified=2 |

## 门禁结果

| 门禁 | 结果 | 说明 |
|---|---|---|
| document_gate | pass | 可继续受控文档治理 |
| KDS TOKEN | pass | fingerprint 已通过，不写入文档 |
| Git gate | partial | GPCF 工作区 dirty，本轮不提交 |
| operational gates | blocked | 既有质量、可用性、客户满意信号阻止状态升级 |

## 边界

- 不修改 Brain 业务代码。
- 不修改 Studio 业务代码。
- 不重构 GFIS validator。
- 不生产写入。
- 不提交、不推送、不部署。
- 不升级 `accepted`、`integrated` 或 `production_ready`。

## 下一轮输入

`GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002`

目标：继续只读采样 Brain 与 Studio drift，收集第二个 MTTD/MTTR 数据点，并判断是否需要用户授权执行 sync-only closure。
