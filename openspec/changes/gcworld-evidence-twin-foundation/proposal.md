---
doc_id: GPCF-DOC-GCWORLD-001
title: GCWORLD 证据数字孪生底座变更提案
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, MMC, GFIS, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/proposal.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## 变更原因

GlobalCloud KDS 已经包含映射人员、组织、项目、系统及其关系变化所需的事实材料，但尚未形成可治理、可衡量覆盖率的世界模型。需要建立 GCWORLD 底座，使未来的工作台和职能智能体能够基于证据运行，而不是依赖无法追溯的摘要或推断身份。

本变更属于 GKE-001 `release_0` 的规划与只读评估范围，不授权真实 KDS/MMC 写入、外部行动、部署或任何状态提升。

## 变更内容

- 定义 GCWORLD 系统边界契约：KDS 记录证据与事实；WAS-Ontology 定义世界结构；GCWORLD 承载世界实例与工作台视图；XWAIL 负责智能体规划与协同；WAES 管理权限；MMC 连接能力；业务系统执行现实动作；LOOP/Harness 记录并校验结果。
- 定义 GCWORLD 证据数字孪生契约，将证据与候选分类同事实、运行、目标、模拟四类世界状态严格分离。
- 定义人员、组织、团队、项目、系统、物理资产、职能角色及其时间限定关系的组织资产模型。
- 定义 WAS 八维资产权威继承、八流运行、双时间、世界快照、事件、行动、结果与承诺模型。
- 定义面向 KDS 来源引用、身份归一、来源追踪、未决提及和关系证据的确定性只读覆盖评估。
- 定义受治理的职能智能体模型：智能体绑定资产角色、权限、证据范围、行动边界和可审计执行账本，不得冒充真实人员。
- 定义 GCWORLD-AUTH 世界原生身份、授权与责任体系，使身份、角色定义、角色任用、授权契约、运行裁决和执行回执形成确定性闭环。
- 定义观察、解析、构造、推理、裁决、确认、执行、取证、提升与学习的标准世界运行闭环。
- 定义十二个 GCWORLD 工作中心、单一资产档案、视图裁剪和多租户协作边界。
- 定义数据分层、统一标识、领域服务、API、事件、一致性、安全、可观测性、P0—P7 路线和 Harness 验收门禁。

## 能力范围

### 新增能力

- `gcworld-evidence-twin`：建立与证据关联的组织资产世界模型，严格区分事实、运行、目标和模拟状态。
- `gcworld-coverage-assessment`：确定性、只读地评估来源到资产的覆盖情况、未决身份和关系证据缺口。
- `gcworld-role-agent-governance`：规范组织资产职能智能体的注册、权限边界和行动控制。
- `gcworld-world-auth`：定义世界身份、角色任用、授权委托、动态裁决、义务、级联撤销和责任追踪。
- `gcworld-runtime-boundary`：定义系统职责边界、首批工作中心，以及从 KDS 普查到受控执行的分阶段演进路径。
- `gcworld-world-runtime`：定义世界运行服务、事件与行动闭环、任务承诺、风险分级、模拟分支和事实提升协议。
- `gcworld-workbench-product`：定义十二个工作中心、统一资产档案、权限裁剪、可解释交互和跨租户协作。
- `gcworld-engineering-governance`：定义数据、存储、领域服务、统一标识、接口事件、安全韧性、实施路线和验收治理。

### 修改能力

无。

## 影响范围

- **项目群与发布阶段：** GKE-001 / `release_0`（客户只读试点）。
- **功能包：** F-013 `knowledge-asset-model-system`；本变更不新增后继功能包，也不改变 F-013 的阻塞状态。
- **仓库与责任方：** GPCF / GPCF；KDS 仅作为只读证据来源。
- **任务线程：** 当前 GCWORLD 任务；GKE-001 权威协调线程仍以 `governance/openspec/gke001-program-binding.yaml` 中的记录为准。
- **当前基线：** GPCF 文档门禁此前已通过；运行态 `F-013` 仍为阻塞，`F-014` 继续独立负责会议到项目控制闭环。
- **允许范围：** 本 OpenSpec 变更，以及 F-013 准入约束解除后形成的有界只读评估证据。
- **禁止范围：** KDS/MMC 写入、KDS API 使用、身份或关系回写、业务台账写入、凭据和权限变更、部署、对外沟通，以及验收、集成或生产状态声明。
- **CodeGraph 影响：** 不改变源码关系，仅声明未来从 GKE-001/KDS 证据到 GCWORLD 只读模型的领域关系。
- **回滚边界：** 仅删除本次尚未提交的 OpenSpec 变更，不修改任何来源记录或运行状态。
