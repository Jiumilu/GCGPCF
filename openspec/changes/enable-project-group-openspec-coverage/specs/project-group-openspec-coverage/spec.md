---
doc_id: GPCF-OS-OPEN-SPEC-COVERAGE-SPEC-20260712
title: spec
project: GPCF
related_projects: [GPC, WAES, GPCF, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/enable-project-group-openspec-coverage/specs/project-group-openspec-coverage/spec.md
source_path: openspec/changes/enable-project-group-openspec-coverage/specs/project-group-openspec-coverage/spec.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 完整覆盖当前项目
治理系统 SHALL 精确枚举当前 18 个 GlobalCloud 项目，并为每个项目提供一条 OpenSpec 适用性记录。

#### Scenario: 当前项目全部存在
- **WHEN** OpenSpec 覆盖校验器读取当前项目注册表和适用性矩阵
- **THEN** 校验结果包含 18 个唯一项目，且不存在缺失或意外条目

### Requirement: 入口或受控豁免
每个项目 MUST 具有受控的中央 OpenSpec 入口，或具有包含理由、责任人、复核条件和到期/复核日期的治理豁免。

#### Scenario: 项目使用中央入口
- **WHEN** 项目被标记为 `required` 或 `conditional`
- **THEN** 其记录明确 GPCF OpenSpec 规划空间和项目专属 change 命名规则

#### Scenario: 项目获得豁免
- **WHEN** 项目被标记为 `waived`
- **THEN** 若理由、责任人、复核条件或复核日期缺失，校验器拒绝该记录

### Requirement: Feature 与 Loop 可追溯
每条适用性记录 SHALL 将项目映射到 GPCF Feature 创建入口、默认 Delivery 或 Governance Loop、Evidence Gate 和 Harness 交接。

#### Scenario: Change 进入实施
- **WHEN** 任一已覆盖项目的 OpenSpec change 进入 apply
- **THEN** 它绑定到 active GPCF Feature，并保留 Loop、evidence 和 Harness 可追溯关系

### Requirement: 当前与历史范围分离
当前项目控制门禁 SHALL 校验 18 项目注册表；历史 17 项目证据 SHALL 保留其原始日期范围。

#### Scenario: 校验当前元数据
- **WHEN** 当前控制文档被检查
- **THEN** 校验器要求包含 ICP 在内的全部 18 个当前项目

#### Scenario: 检查历史证据
- **WHEN** 带日期的历史基线明确记录原 17 项目范围
- **THEN** 系统不会仅为满足当前注册表而改写该历史断言

### Requirement: 验收边界
OpenSpec artifact 完成、任务完成、规格同步或归档 MUST NOT 授予 `accepted`、`integrated`、`production_ready` 或 `customer_accepted` 状态。

#### Scenario: Change 完成
- **WHEN** 全部 OpenSpec artifacts 和 tasks 完成
- **THEN** 该 change 仍须通过 Feature Evidence Gate、文档门禁、Harness Governance 和必要的人工确认
