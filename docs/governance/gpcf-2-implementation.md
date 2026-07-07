---
doc_id: GPCF-DOC-12C308D619
title: GPCF 2.0 实施基线
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
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
