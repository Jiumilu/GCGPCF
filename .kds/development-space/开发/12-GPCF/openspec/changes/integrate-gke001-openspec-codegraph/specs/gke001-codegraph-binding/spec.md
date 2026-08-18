---
doc_id: GPCF-DOC-12EA88652E
title: spec
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-codegraph-binding/spec.md
source_path: openspec/changes/integrate-gke001-openspec-codegraph/specs/gke001-codegraph-binding/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-11
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 将 GKE-001 表达为工程域
CodeGraph 治理模型 SHALL 将 GKE-001 表达为连接既有仓库的 engineering-domain 节点，并且 MUST NOT 增加真实仓库计数。

#### Scenario: Registry 包含 GKE-001
- **WHEN** CodeGraph 绑定校验器读取仓库 registry
- **THEN** `repo_count` 保持 14，且 `engineering_domains` 条目引用 GKE-001 绑定

### Requirement: CodeGraph 绑定覆盖 Program 结构
GKE-001 CodeGraph 绑定 SHALL 包含 Program 协调器、F-013、canonical manifest、应用路线图、Release 0 至 Release 3、KDS、MMC、Studio、Brain、业务权威系统、消费项目、OpenSpec 和证据的节点与边。

#### Scenario: 查询 Program 影响
- **WHEN** 某项变更将 GKE-001 或 F-013 标记为工程域或 Feature
- **THEN** 绑定解析受影响仓库、能力边界、必需 handoff 和下游客户 Release 门禁

### Requirement: 项目范围与索引仓库范围保持分离
CodeGraph 绑定 MUST 分别标识 18 个受治理项目和既有 14 个索引仓库。

#### Scenario: 受治理项目没有索引仓库条目
- **WHEN** AAAS、XWAIL 或 SOP 通过受治理项目绑定参与，但在当前 registry 中没有专用仓库
- **THEN** 该项目仍保留在 GKE-001 项目范围内，且不得被表达为虚构的索引仓库

### Requirement: CodeGraph 证据保持有界
CodeGraph 同步、状态和查询证据 SHALL 分类为本地代码智能治理证据，并且 MUST NOT 被视为 KDS 运行时、客户 E2E、集成或生产就绪证明。

#### Scenario: CodeGraph 同步和查询通过
- **WHEN** 本地 GPCF 索引为当前版本且 GKE-001 文件可查询
- **THEN** 结果以 `partial/not_complete` 状态记录为治理证据，所有生产或客户状态提升标志保持 false

### Requirement: 检测 CodeGraph 映射漂移
当 GKE-001 绑定丢失 canonical hash、应用路线图 hash、必需仓库角色、Release 节点、F-013 关系或状态边界时，校验器 SHALL 失败。

#### Scenario: Canonical hash 漂移
- **WHEN** 绑定 hash 与当前 canonical manifest 或应用路线图不一致
- **THEN** 在任何下游 GKE-001 handoff 将图谱视为当前版本之前，校验必须失败
