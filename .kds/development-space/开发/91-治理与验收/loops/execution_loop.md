---
doc_id: GPCF-DOC-4F0E8E6D9C
title: 执行闭环
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/loops/execution_loop.md
source_path: loops/execution_loop.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# 执行闭环

GPCF 2.0 执行闭环：

```text
Plan -> Implement -> Evaluate -> Repair -> Commit
```

每轮只回答五个问题：

```text
1. 这轮做什么？
2. 改了什么？
3. 怎么验证？
4. 发现什么问题？
5. 是否可以提交？
```

运行状态必须写入：

```text
runtime/queue.json
runtime/state.json
```

角色流转：

```text
Dispatcher -> Planner -> Builder -> Evaluator -> Repair -> Recorder
```

Loop 只更新 Feature Workspace 和 runtime 状态，不创建额外过程文档。

Runtime 调度命令：

```bash
python scripts/gpcf_dispatch.py <FEATURE_ID>
```

关闭命令：

```bash
python scripts/gpcf_close_feature.py <FEATURE_ID>
```
