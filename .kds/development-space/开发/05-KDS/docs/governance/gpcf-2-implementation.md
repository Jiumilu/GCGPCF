---
doc_id: GPCF-DOC-12C308D619
title: GPCF 2.0 实施基线
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/governance/gpcf-2-implementation.md
source_path: docs/governance/gpcf-2-implementation.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# GPCF 2.0 实施基线

## 目标

把当前体系从重治理、细颗粒、慢闭环，升级为轻治理、Feature 驱动、快速交付闭环。

## 原则

```text
Program 定方向
Project 管节奏
Feature 做交付
Loop 只服务执行
Evidence 只保留结果
```

## 新路径

```text
Feature -> Workspace -> Loop -> Evidence -> Merge
```

最小交付单元是 Feature。每个 Feature 只保留：

```text
feature.yaml
journal.md
evidence/
artifacts/
```

## 执行闭环

统一为：

```text
Plan -> Implement -> Evaluate -> Repair -> Commit
```

每次循环只回答：

```text
1. 这轮做什么？
2. 改了什么？
3. 怎么验证？
4. 发现什么问题？
5. 是否可以提交？
```

## 非授权边界

GPCF 2.0 不授权 commit、push、deploy、真实外部 API、真实 KDS API、生产写入、权限变更、accepted、integrated、production_ready 或 customer_accepted。

## GPCF-2-FEATURE-RUN-001 执行口径

GPCF 2.0 从静态规约进入 Feature 运行态。当前最小运行集合：

```text
F-002 project-group-feature-queue
F-003 evidence-gate-profile
F-004 loop-governance-slimming
```

三个 Feature 均保持在 `features/active/`，并写入 `runtime/queue.json`。`runtime/state.json` 必须显示 `mode=feature_delivery`、当前 Feature、active Feature 数和角色集合。

Evidence Gate 不再默认使用 `not_required`。本地可执行证据至少覆盖：

```text
tests: validate_gpcf_2_feature_workspace.py
build: python -m py_compile
lint: git diff --check
screenshots/api: 按 Feature scope.in 判定，非适用项写为 waived 并说明原因
```

历史 LOOP 治理结果只作为可回放参考证据。新开发不得继续以单独 progress、review、task、status、log、notes 或 decision 文档扩张过程。

## GPCF-2-RUNTIME-DISPATCH-001 执行口径

Runtime 队列必须通过脚本推进，不再只手工维护 JSON：

```bash
python scripts/gpcf_dispatch.py <FEATURE_ID>
```

角色流转固定为：

```text
Dispatcher -> Planner -> Builder -> Evaluator -> Repair -> Recorder
```

每次调度必须写入：

```text
runtime/logs/F-xxx.jsonl
```

`F-002` 作为出口验证样本，必须通过 `gpcf_close_feature.py` 从 `features/active/` 移动到 `features/done/`，并在 `runtime/queue.json` 中保留 `status=closed`、`current_role=Recorder` 的关闭记录。

## GPCF-2-RUNTIME-CHAIN-001 执行口径

Runtime 必须至少保留一个完整角色链业务样本：

```text
F-005 factory-exception-intake-dry-run
```

该样本用于验证 GFIS 业务 Feature 可按以下链路推进：

```text
Dispatcher -> Planner -> Builder -> Evaluator -> Repair -> Builder -> Evaluator -> Recorder
```

`runtime/logs/F-005.jsonl` 必须包含六类角色记录。`F-003` 作为第二个出口样本，必须关闭到 `features/done/`，用于证明关闭出口不是单例。
