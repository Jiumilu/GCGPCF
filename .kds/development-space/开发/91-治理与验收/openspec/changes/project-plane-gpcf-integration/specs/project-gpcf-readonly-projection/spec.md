---
doc_id: GPCF-PROJECT-GPCF-PROJECTION-SPEC-20261018
title: GPCF Feature 只读投影规格
project: GPCF
related_projects: [GPCF, Project]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/project-plane-gpcf-integration/specs/project-gpcf-readonly-projection/spec.md
source_path: openspec/changes/project-plane-gpcf-integration/specs/project-gpcf-readonly-projection/spec.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: GPCF 为状态事实源
适配器 SHALL 只读取 GPCF Feature 队列与本地证据状态；Plane 中的编辑 MUST NOT 改写 GPCF 队列、证据或验收结论。

#### Scenario: 本地预览
- **WHEN** 对 GPCF 仓运行默认预览
- **THEN** 输出每个 Feature 的来源 ID、项目、状态、证据状态和更新时间，且 GPCF 文件字节不变

### Requirement: 幂等投影
适配器 SHALL 使用 GPCF Feature ID 作为 Plane 外部 ID，仅在明确启用目标开发实例写入时创建或更新工作项。

#### Scenario: 重复同步
- **WHEN** 同一 Feature 连续同步两次
- **THEN** Plane 中对应同一外部 ID 的工作项保持一条，人工指派和工作流状态不被覆盖

### Requirement: 状态边界
投影 SHALL 标明 GPCF 来源状态与证据路径；没有 Evidence Gate 结果时 MUST 标记为未核验，不得推断通过。

#### Scenario: 缺少证据
- **WHEN** Feature 的证据结果缺失或门禁失败
- **THEN** Plane 投影显示 `pending` 或 `failed`，不得显示验收通过
