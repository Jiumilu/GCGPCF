---
doc_id: GPCF-SPACEAI-FLOOD-SPEC-20261016
title: spec
project: GPCF
related_projects: [GPCF, WAME]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/spaceai-was-city-flood-replay/specs/spaceai-city-slice-replay/spec.md
source_path: openspec/changes/spaceai-was-city-flood-replay/specs/spaceai-city-slice-replay/spec.md
sync_direction: bidirectional
last_reviewed: '2026-10-16'
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: Reuse approved slice contracts
系统 MUST 使用现有 XWAIL 切片网络 Schema，逐片声明 synthetic，包含主体、流、方法、证据与明确时区；正式校验无错误和警告。

#### Scenario: Validate the local scenario
- **WHEN** 校验本轮内涝样例
- **THEN** Schema 层明确执行，结构校验返回零错误零警告

### Requirement: Replay only information available at the cursor
系统 SHALL 用发生时间与获知时间过滤记录，real 仅用记录时间，trusted 额外考虑验证时间，evolution 额外考虑推演时间，记录时间不得早于发生时间；边也按记录时间过滤。

#### Scenario: Late verification and relation
- **WHEN** 游标早于验证完成或关系记录时间
- **THEN** 该验证或关系不得出现在当时已知视图

### Requirement: Preserve corrections and idempotence
系统 SHALL 保留原始记录与 correctsRef，勘误须保持类型、主体、三世界身份、发生时间、指标和单位；相同 ID 相同输入不重复计数，冲突 ID 拒绝。

#### Scenario: Correct a late measurement
- **WHEN** 08:20 的测量在 08:28 收到勘误且游标为 08:22
- **THEN** 当时已知保留原测量，最新修正显示勘误并标迟到，原始记录仍可查

#### Scenario: Replay the same batch twice
- **WHEN** 输入同一批记录两次
- **THEN** 投影节点和计数与输入一次完全一致

### Requirement: Separate observation verification and inference
系统 SHALL 保留三世界身份，过期指标显示未知，回执与预测不得解除观测风险。

#### Scenario: Receipt without recovery evidence
- **WHEN** 已收到泵站作业回执但没有恢复观测
- **THEN** 积水观测和验证记录不得被改写为恢复

#### Scenario: Expired observation
- **WHEN** 游标超过指标 validUntil
- **THEN** 当前可用值显示未知且历史记录原值保留

### Requirement: Filter graph references consistently
系统 SHALL 在本地 scope 过滤后只输出允许范围的节点、边及切片/资产证据引用。

#### Scenario: Hidden endpoint
- **WHEN** 一端资产不在允许集合
- **THEN** 该节点及其相邻边和证据引用均不出现在投影

### Requirement: Render projected data in Chinese
界面 SHALL 仅展示投影输出，支持时间与回放口径切换、切片证据查看，未生成切片不得展示标题。

#### Scenario: Change replay context
- **WHEN** 用户切换时点或当时已知/最新修正
- **THEN** 节点、关系、计数和详情同步采用同一 snapshot，并持续标注合成数据

### Requirement: Open the CWME application independently
系统 SHALL 在当前项目 apps/city-model 提供完整本地网页，复用已有模型与投影；成品打开不得依赖会话宿主、Python、业务接口或外部资源。

#### Scenario: Open locally without a server
- **WHEN** 用户直接打开 index.html 且网络不可用
- **THEN** 中文模型图、时点切换、口径切换及证据查看正常，并持续注明合成数据

#### Scenario: Rebuild from the model
- **WHEN** 在具备文档所列重建依赖的环境执行 build.py
- **THEN** 先执行既有Schema与投影校验，再生成与当前模型一致的独立应用
