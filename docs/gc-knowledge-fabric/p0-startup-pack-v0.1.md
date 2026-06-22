---
doc_id: GPCF-DOC-7DBBCBB955
title: GC-Knowledge Fabric P0 启动包 v0.1
project: KDS
related_projects: [GFIS, GPC, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/p0-startup-pack-v0.1.md
source_path: docs/gc-knowledge-fabric/p0-startup-pack-v0.1.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0 启动包 v0.1

## 1. 启动包定位

本文档作为 GC-Knowledge Fabric P0-D1 启动输入，用于把已确认的需求口径、上会材料、工程实施计划、试点清单和两周排期汇总成可执行的 P0 启动包。

本启动包仍为 `draft / v0.1`，不声明业务上线，不接真实生产 DB，不写 GFIS/GPC/ERP/MES，不自动确认事实，不自动裁决，不自动积分或收益分配。

## 2. 启动输入

| 输入 | 路径 | 用途 |
|---|---|---|
| 需求确认纪要与 P0-P2 实施计划 | `docs/gc-knowledge-fabric/requirements-confirmation-and-p0-p2-implementation-plan-v0.1.md` | 锁定 Q1-Q40 需求口径 |
| 管理层摘要 | `docs/gc-knowledge-fabric/executive-summary-v0.1.md` | 上会决策与红线说明 |
| 工程实施计划 | `docs/gc-knowledge-fabric/engineering-implementation-plan-v0.1.md` | P0 工程交付结构 |
| 试点推进清单 | `docs/gc-knowledge-fabric/pilot-rollout-checklist-v0.1.md` | 葛化 P1 与湖北磷材 P2 准备 |
| P0 两周排期 | `docs/gc-knowledge-fabric/p0-two-week-execution-schedule-v0.1.md` | D1-D10 执行节奏 |

## 3. P0-D1 目标

P0-D1 只做规则冻结和启动边界确认：

- 锁定 Q1-Q40 需求口径。
- 确认 P0 no-write、candidate-only、dry-run、metadata-only 边界。
- 确认 P0 不以业务上线为验收口径。
- 确认 P0 两周排期可作为每日 LOOP 输入。
- 生成第一轮 LOOP evidence。

## 4. P0-D1 输出

| 输出 | 状态 |
|---|---|
| P0 启动包 v0.1 | draft |
| P0-D1 LOOP evidence | draft |
| 文档清单与 KDS 开发空间同步台账记录 | pending_api |
| 文档污染、KDS TOKEN、Loop 文档门禁结果 | 待运行 |

## 5. 启动边界

P0-D1 禁止以下动作：

- 真实 KDS API 写入。
- 真实 GFIS/GPC/ERP/MES 写入。
- 生产 TOKEN 写入或调用。
- 将 AI 输出升级为 accepted、published、written_back。
- 将潜在收益升级为正式收益。
- 将自购 AI 额度写入统一收益池。
- 生成委员会正式裁决结果。

## 6. 启动后下一轮

P0-D1 完成并通过门禁后，进入 P0-D2：

```text
目录与编号
-> 对象编号规则
-> KDS 十一池挂接规则
-> Domain + Pool 双维模型
-> pool binding validator 输入
```
