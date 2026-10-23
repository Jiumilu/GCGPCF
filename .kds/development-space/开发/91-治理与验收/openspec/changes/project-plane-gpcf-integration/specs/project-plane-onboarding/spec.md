---
doc_id: GPCF-PROJECT-PLANE-ONBOARDING-SPEC-20261018
title: GlobalCloud Project 纳管规格
project: GPCF
related_projects: [GPCF, Project]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/openspec/changes/project-plane-gpcf-integration/specs/project-plane-onboarding/spec.md
source_path: openspec/changes/project-plane-gpcf-integration/specs/project-plane-onboarding/spec.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 独立项目基线
GlobalCloud Project SHALL 有独立本地仓库、可核验的 Plane 社区版上游提交和原始许可证文件，并在 GPCF 当前项目群登记中有唯一项目 ID。

#### Scenario: 核对项目来源
- **WHEN** 维护者检查项目仓与 GPCF 登记
- **THEN** 可找到上游地址、提交 ID、许可证和 `Project` 项目登记，且旧历史快照未被重算

### Requirement: 双主控继承
项目级总体方案和实施方案 SHALL 分别继承项目群总体方案与实施方案，并保留独立的授权和确认状态。

#### Scenario: 新建项目未验收
- **WHEN** 仅完成建仓和本地开发
- **THEN** 项目状态最高为 `partial`，不得声明集成、生产就绪或客户验收
