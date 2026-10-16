---
doc_id: GPCF-DOC-B7F7C251FF
title: spec
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/was-flow-naming-migration/specs/was-flow-naming-migration/spec.md
source_path: openspec/changes/was-flow-naming-migration/specs/was-flow-naming-migration/spec.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 八流命名迁移与单源映射

WAS 仓 SHALL 建立《WAS-V1.2 术语迁移表》作为旧名→V1.2 名的唯一映射单源；映射 MUST 覆盖全部 8 个旧名（6 更名＋1 并入＋1 重构）且 MUST NOT 改变任何流的语义边界与既有基线（八维、三层资产、生命周期）。

#### Scenario: 映射完备性核对
- **WHEN** 对迁移表执行完备性验证
- **THEN** 旧 8 名全部有明确去向；新 8 名各有一对一来源或「新增」标注；缺失即禁止提交

### Requirement: 兼容 validator

契约层 SHALL 在迁移后以 V1.2 名为主命名，并 SHALL 提供兼容窗口：数据级校验接受旧名（deprecated）；新数据 MUST 使用 V1.2 名；窗口关闭时点 MUST 为另行版本发布并在迁移表登记。

#### Scenario: 旧数据兼容
- **WHEN** 校验含旧名的既有数据（兼容窗口内）
- **THEN** 校验通过且旧名按 deprecated 处理；新引用出现旧名按漂移记录并纠正

### Requirement: 验证与留痕

迁移 SHALL 以 WAS 仓校验器复跑全 PASS 作为验证门槛（validate_all 13 项）；执行与验证结果 MUST 留存 evidence（含映射、范围、兼容决定、非声明）。

#### Scenario: 复跑门槛
- **WHEN** 迁移执行完成
- **THEN** `validate_all` 全 PASS；未过不得提交登记

### Requirement: 无编造与无状态提升

迁移 MUST NOT 为新增流（ValueFlow/CreditFlow）编造业务实例；因新增流无既有实例而精准化的校验断言 MUST 如实记录。本变更 SHALL NOT 触发 accepted / integrated / production_ready 任何声明；「迁移执行 ≠ V1.2 发布或运行层完成」（§19 纪律保留）。

#### Scenario: 状态检查
- **WHEN** 任一检查方查询迁移状态
- **THEN** 返回 `migration executed（迁移执行；V1.2 发布/运行层未完成）`，且无任何完成级声明
