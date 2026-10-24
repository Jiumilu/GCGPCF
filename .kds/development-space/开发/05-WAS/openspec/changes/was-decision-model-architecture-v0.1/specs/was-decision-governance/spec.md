---
doc_id: GPCF-DOC-CANDIDATE-WAS-DECISION-MODEL-ARCH-SPEC
title: 能力规格 — WAS 决策模型体系架构（候选）
project: WAS
related_projects: [GPCF, XWAIL, WAME, Ontology]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/specs/was-decision-governance/spec.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/specs/was-decision-governance/spec.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 能力规格：WAS 决策模型体系架构（候选）

本规格登记能力要求与验收口径，不实现、不冻结 schema、不授权执行。

## ADDED Requirements

### Requirement: 决策术语候选准入

WAS 决策域术语 MUST 以 candidate 形式登记，MUST NOT 在 GPCF 词表准入与人工确认前写入正式 `okf/ontology.yaml`；术语 MUST 保持对象/关系/状态族分离，不得合并为单一 lifecycle。

#### Scenario: 未准入不得转正
- **WHEN** 任一变更试图把 `decision_terms` 写入正式 ontology 版本
- **THEN** 必须存在 GPCF admission_ref、评审记录与人工确认；否则必须保持 candidate

#### Scenario: 状态族不得混写
- **WHEN** 决策记录、授权记录、执行记录与结果记录同时存在
- **THEN** 各状态族 MUST 分别校验，MUST NOT 因一个状态变化静默提升其他状态

### Requirement: 决策契约与负例校验

决策契约 MUST 提供正例、负例与多层 Validator；MUST 阻断模型建议升格事实、状态混写、越权执行、缺证据强决策、过期/撤销授权、商业权利缺失与转授权扩权。

#### Scenario: 负例必须被拒绝
- **WHEN** 使用 15 个候选负例运行四层 Validator
- **THEN** 每个负例 MUST 至少被一层拒绝，并给出预期原因

### Requirement: WAME no-write 运行时边界

WAME 决策运行时 MUST 在适配器调用前完成预检；MUST 将模型失败统一为 fail-closed 五态；MUST NOT 把模型概率/verdict 转为授权；执行门禁默认 disabled，通过时仅写隔离 no-write sink；审计 MUST append-only。

#### Scenario: 未登记/暂停模型阻断
- **WHEN** 模型未登记或处于 Paused
- **THEN** 预检 MUST 阻断，适配器 MUST NOT 被调用

#### Scenario: 失败态 fail-closed
- **WHEN** 适配器返回/抛出 unavailable/refusal/ood/missing_evidence/timeout
- **THEN** Assessment MUST 标记 fail-closed 且不得产生授权或执行

### Requirement: 兼容与迁移可回滚

决策能力 MUST 以 additive_profile_first 方式引入；MUST NOT 静默给旧字段补写决策语义；回滚 MUST 能撤回 Profile 并保留旧引用与历史记录。

#### Scenario: 旧对象继续有效
- **WHEN** 使用方未采纳 DecisionProfile
- **THEN** 既有 WAS Core 对象与引用 MUST 保持有效

## MODIFIED Requirements

（本候选首版无修改既有 Requirement。）

## REMOVED Requirements

（本候选首版无移除。）
