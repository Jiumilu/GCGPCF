---
doc_id: GPCF-DOC-5C02110A55
title: spec
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/was-scenario-flow-extension/specs/was-scenario-flow-extension/spec.md
source_path: openspec/changes/was-scenario-flow-extension/specs/was-scenario-flow-extension/spec.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 场景流受控扩展登记

WAS 体系 SHALL 以「扩展登记件」形式登记「场景流 ScenarioFlow」为流集合的受控兼容扩展；登记件 MUST 引用统一单源定义（2026-10-16 裁定文本与 GCWORLD V1.0.1 九流表），MUST NOT 引入平行定义或替代、改名、合并任何既有流。

#### Scenario: 登记件与定义单源一致性核对
- **WHEN** 对登记件执行术语一致性验证
- **THEN** 登记件的场景流定义与裁定文本、GCWORLD V1.0.1 逐字一致（归一化后）；不一致不得提交复核

### Requirement: 兼容性声明

本扩展 SHALL 按 WAS 仓《AGENTS.md》跨项目变更协议声明六项（WAS 基线版本、Ontology 影响、XWAIL 影响、AaaS 影响、WAME 影响、迁移决定）；迁移决定 MUST 为 `compatible`，且 MUST NOT deprecated 任何既有术语。

#### Scenario: 未决项处理
- **WHEN** 任一声明项无法确定
- **THEN** 该项标记 `candidate/partial` 并阻止状态提升，不得以默认值填充

### Requirement: 版本化纳入路径

契约层 8+8 基线 SHALL 保持不变；场景流 MUST 按「候选登记 → 治理复核 → 版本发布纳入」路径推进；正式纳入前，任何引用 MUST 标注「已裁定候选扩展（待 WAS 版本化纳入）」口径。

#### Scenario: 提前引用防护
- **WHEN** 某文档在正式纳入前引用场景流
- **THEN** 引用须携带候选标注；无标注引用按漂移记录并纠正

### Requirement: 无状态提升

本变更 SHALL NOT 触发 accepted / integrated / production_ready / customer_accepted 任何声明；登记完成不等于纳入完成。

#### Scenario: 状态检查
- **WHEN** 任一检查方查询本扩展状态
- **THEN** 返回 `candidate（已登记，待版本化纳入）`，且无任何完成级声明
