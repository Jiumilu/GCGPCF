---
doc_id: GPCF-DOC-3A7F6FA260
title: 唯一状态事实源（P03）落地发现与阻塞项
project: GPCF
related_projects: [GPC, WAME, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/status-source-of-truth-findings-20261022.md
source_path: docs/reports/status-source-of-truth-findings-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 唯一状态事实源（P03）落地发现与阻塞项

- 日期：2026-10-22｜范围：GlobalCloud GPCF｜裁决依据：老卢 Q2（feature.yaml 为唯一事实源）+ 回执 `AUTH-PG-STATUS-SOT-FEATUREYAML-20261022`
- 本次交付：`runtime/status-source-of-truth.yaml`（口径与映射）+ `tools/kds-sync/derive_status_views.py`（派生/一致性检查）
- 状态边界：本文件只陈述实测事实，不做状态提升

## 1. 实测结论

`python3 tools/kds-sync/derive_status_views.py --check`（38 个 Feature）→ **exit 1，22 个 Feature 的派生视图与源不一致**：

| 字段 | 不一致数 | 含义 |
|---|---:|---|
| `updated_at` | 15 | queue 侧时间戳长期未随 feature.yaml 更新（§8-6「批量时间误读」实证） |
| `status` | 17 | queue 状态与 step 不构成一一映射（见 §2） |
| `current_role` | 11 | 随 status 一起偏离 |
| `project` | 1 | **F-022：queue=gpcf / feature.yaml=was**（与 F-021 同类的归属漂移，新发现） |

另：`F-001` 在 queue 中不存在（历史关闭残留），需在 P19 一并处置。

## 2. 为什么"直接按源重写 queue"不可行（三个真实阻塞）

1. **step 词表已漂移**：feature.yaml 的 `loop.current_step` 出现非词汇表值 `verification / b2_released / registration / evidence`（词汇表仅 `plan|implement|evaluate|repair|commit`）。派生结果因此不确定。
2. **queue 状态不是 step 的函数**：同一 step 下实测并存多种 queue 状态——`evaluate` → `blocked`(6) / `queued`(2) / `evaluated`(1)；`commit` → `closed`(14) / `commit`(3) / `queued`(2)。说明 queue 还叠加了"是否已派发""治理阻塞"两个维度，而这两个维度当前**没有**写在 feature.yaml 里。
3. **并发写入**：`runtime/queue.json` 含另一会话未提交改动（F-029/F-033 等），批量重写会互相覆盖。

## 3. 需要裁决的设计点（阻塞 P03 完成）

在 feature.yaml 里补哪两个字段，才能让 queue 成为纯派生视图？

- 方案 A：加 `loop.dispatched: true|false` + `governance_blocked: true|false`，派生规则 `blocked > queued > step 映射`。
- 方案 B：直接把 queue 状态写进 feature.yaml（`loop.queue_status`），queue.json 完全由它拷贝；口径唯一但 feature.yaml 承担派生字段。
- 方案 C：不追求纯派生，改为"queue 保留独立派发维度，门禁只校验 step/role/project/priority 四项"。改动最小但违背 Q2「唯一事实源」的字面口径。

## 4. 当前可立即执行的收口动作（本轮未做，待授权）

1. 修正 F-022 归属 `gpcf → was`（与 F-021 同类，跨项目职责，需授权）。
2. 统一 step 词表：把 4 个非标准 step 值归一（需先决定语义映射，不丢信息）。
3. 静默窗口内跑 `derive_status_views.py --write` 全量重算（约 22 项），并提交。
4. 把 `derive_status_views.py --check` 接入门禁（一致性不一致即阻断）。
