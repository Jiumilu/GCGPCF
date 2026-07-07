---
doc_id: GPCF-DOC-E6A5B97688
title: Feature Workspace 标准
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/standards/feature-workspace.md
source_path: docs/standards/feature-workspace.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# Feature Workspace 标准

Feature Workspace 是 GPCF 2.0 的最小交付单元。每个功能工作区只保存结构化状态、五问日志、结果证据和交付产物，避免过程文档继续膨胀。

## 目录结构

```text
features/active/F-001-example/
feature.yaml
journal.md
evidence/
artifacts/
```

## feature.yaml 模板

```yaml
id: F-001
name: example
project: gpcf
status: active
goal: 完成一个可验证交付
owner: agent-dev-01
priority: P0
scope:
  in: []
  out: []
acceptance: []
loop:
  current_step: plan
  iteration: 0
evidence:
  tests: pending
  build: pending
  screenshots: pending
  api: pending
  summary: pending
blockers: []
created_at: ""
updated_at: ""
```

## journal.md 模板

```text
1. 这轮做什么？
2. 改了什么？
3. 怎么验证？
4. 发现什么问题？
5. 是否可以提交？
```

## Evidence Gate

关闭 Feature 前必须运行：

```bash
python scripts/gpcf_check_evidence.py <FEATURE_ID>
```

证据状态只允许：

```text
pending
pass
fail
waived
```

`waived` 只能用于 scope 不适用的截图或接口证据，并必须在 evidence 文件中写明原因。`fail` 或 `pending` 均不得关闭 Feature。
