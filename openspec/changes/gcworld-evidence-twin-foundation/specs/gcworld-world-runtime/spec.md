---
doc_id: GPCF-DOC-GCWORLD-017
title: GCWORLD 世界运行时规格
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, KWE, MMC, GFIS, Brain]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-world-runtime/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-world-runtime/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 世界运行服务职责分离
系统 SHALL 将世界注册、身份解析、世界投影、上下文构造、事件引擎、行动运行时、智能体运行时、模拟引擎、治理适配以及查询与视图作为边界明确的运行服务。各服务 MUST 使用稳定对象标识、版本化契约和证据引用协作，不得复制 KDS、WAS、WAES 或业务系统的权威职责。

#### Scenario: 构造项目决策上下文
- **WHEN** 智能体请求某项目的决策上下文
- **THEN** 身份解析服务先归一相关主体，世界投影与上下文构造服务基于同一世界快照组装事实、关系、权限和证据，查询与视图服务仅返回被允许的数据

### Requirement: 标准世界运行闭环
系统 SHALL 按观察、解析、构造世界快照、推理、裁决、确认、执行、固化证据、状态提升和学习的顺序运行。任何需要真实写入或外部影响的动作 MUST 在裁决和确认完成后才可执行；任一阶段失败时必须保留失败原因和已完成阶段，不得伪造后续结果。

#### Scenario: 动作缺少人工确认
- **WHEN** 高风险动作已经完成推理和权限裁决但缺少规定的人工确认
- **THEN** 运行闭环停留在待确认状态，不调用执行系统，也不产生成功回执

### Requirement: 任务与承诺闭环
系统 SHALL 将任务与承诺建模为可追溯对象，至少记录责任主体、提出方、受益方、目标、范围、截止时间、依赖、状态、验收条件、来源证据和关联行动。任务或承诺只有在验收条件满足且结果证据已固化后才能关闭。

#### Scenario: 承诺被口头声明完成
- **WHEN** 责任主体声明承诺已完成但没有结果证据或验收记录
- **THEN** 系统保持承诺为待核验状态，并显示缺失证据和责任主体

### Requirement: 行动风险分级与执行回执
系统 SHALL 将行动分为 R0 观察、R1 建议或草稿、R2 内部低风险写入、R3 关键业务或对外动作、R4 高影响或不可逆动作。每次执行 MUST 生成行动回执，记录请求、裁决、确认、执行者、目标系统、输入输出摘要、时间、结果、错误和证据；可补偿动作还必须记录补偿策略与补偿回执。

#### Scenario: 关键业务动作执行失败
- **WHEN** R3 动作在目标系统部分完成后失败
- **THEN** 系统记录部分完成回执并按已批准策略触发或请求补偿，不得把动作标记为成功

### Requirement: 模拟分支隔离与事实提升
模拟世界 SHALL 使用独立分支、基线快照、假设集、执行记录和评估结果，不得修改事实世界或直接产生真实权限。模拟结果只有经过证据补全、规则校验、影响评估、人工确认和正式写入链后，才能以新的事实候选进入提升流程。

#### Scenario: 模拟方案获得最佳评分
- **WHEN** 模拟实验室产生评分最高的组织调整方案
- **THEN** 系统仅生成带来源和假设的提升候选，不修改正式组织关系、权限或业务系统
