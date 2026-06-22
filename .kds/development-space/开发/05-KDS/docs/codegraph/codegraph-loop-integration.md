---
doc_id: GPCF-DOC-F7ADE9DF11
title: CodeGraph Loop 集成规范
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-loop-integration.md
source_path: docs/codegraph/codegraph-loop-integration.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph Loop 集成规范

Loop 任务必须把 CodeGraph 结果从临时上下文提升为 evidence。

## 标准流程

```text
Task Intake
  -> CodeGraph Context
  -> Impact Analysis
  -> Patch Plan
  -> Implementation
  -> Test Mapping
  -> Evidence Capture
  -> WAES Gate
  -> KDS / OKF Candidate Record
  -> Loop Feedback
```

## Loop evidence 字段

```yaml
codegraph:
  required: true
  snapshot_id:
  context_queries:
  explored_symbols:
  impact_paths:
  impacted_tests:
  risk_flags:
  evidence_ref:
```

## 阶段边界

- intake：仓库概览、符号检索、架构上下文。
- planning：影响分析、依赖追踪、风险区域识别。
- implementation：符号探索、调用链追踪、相关文件定位。
- validation：影响测试、覆盖映射、架构规则检查。
- evidence：快照、查询日志、受影响符号、变更路径。
- closure：文档候选、KDS candidate。

Loop 不得把 CodeGraph 结果直接升级成 accepted、integrated 或 production_ready。
