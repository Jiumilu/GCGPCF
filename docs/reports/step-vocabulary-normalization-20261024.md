---
doc_id: GPCF-DOC-CC8241B09C
title: 状态步骤词表归一（P03 延伸，2026-10-24）
project: GPCF
related_projects: [GPCF, WAME, XiaoC]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/step-vocabulary-normalization-20261024.md
source_path: docs/reports/step-vocabulary-normalization-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# 状态步骤词表归一（P03 延伸，2026-10-24）

- 依据：Q2/Q3 裁定（feature.yaml 为唯一事实源；派生优先级）+ 老卢 2026-10-24「自动按决策模型推荐采纳」授权
- 背景：`loop.current_step` 存在 4 个非词表值，导致派生视图无法映射（F-016 的 queue 状态曾为空）

## 1. 模型推荐与实际采纳

| Feature | 原 step | 决策模型（top1 概率） | 采纳 | 说明 |
|---|---|---|---|---|
| F-016 绿链图谱只读试点 | `b2_released` | **commit 72.6%**（evaluate 23.1%） | `commit` | B2 阶段已发布，证据 tests/build/summary 均 pass → queue `commit` / `Recorder`（此前为空） |
| F-022 WAS 场景流扩展 | `registration` | **plan 95.3%** | `plan` | 登记阶段 → 计划步；因 dispatched=false，queue 仍 `queued` |
| F-023 WAS 流程命名迁移 | `verification` | **evaluate 72.8%**（none 15.2%） | `evaluate` | 验证阶段 → 证据复核；queue 仍 `queued` |
| F-033 R1 生态集成（XiaoC） | `evidence` | evaluate 48.1% **但 none_probability 37.3% → needs_human** | **未采纳，保持原值** | 模型明示"所给选项可能都不合适"，按纪律转人工；待人工裁定后再归一 |

## 2. 结果

- 词表外 step 由 4 个降为 **1 个**（仅 F-033，已标注待人工）；
- F-016 派生视图恢复（`commit` / `Recorder`）；`derive --check` 0 不一致；
- 决策台账 d047–d049 记录本次自动采纳（auth_id `AUTH-PLAN-20261024-AUTOADOPT`）。

## 3. 待办

- F-033 的 step 语义需人工确认（是"证据收集中"→implement，还是"证据复核"→evaluate）；确认后按同一流程归一。
