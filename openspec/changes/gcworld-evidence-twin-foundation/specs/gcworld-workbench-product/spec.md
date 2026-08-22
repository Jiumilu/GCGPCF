---
doc_id: GPCF-DOC-GCWORLD-019
title: GCWORLD 工作台产品规格
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, KWE, MMC, GFIS, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-workbench-product/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-workbench-product/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 十二个统一工作中心
工作台 SHALL 提供世界总览、组织资产、关系网络、项目世界、时间与事件、智能体、行动与协同、权限与身份、模拟实验室、事实治理、治理与审计、开发与运维十二个工作中心。各中心 MUST 使用同一世界对象、快照和权限语义，不得各自维护冲突的人员、组织、关系或项目主账。

#### Scenario: 从世界总览进入项目世界
- **WHEN** 用户从世界总览选择一个项目并进入项目世界
- **THEN** 工作台保持相同项目资产标识、世界快照和权限上下文，并展示该项目关联的组织、人员、事件、任务、承诺、智能体和证据

### Requirement: 单一组织资产档案
工作台 SHALL 为每个可识别的人员、组织、团队、角色、智能体、项目和系统提供稳定的单一资产档案。档案至少呈现当前事实、历史变化、别名、关系、角色、能力、权限、任务、行动、结果、反馈、证据和冲突；未决身份不得被静默合并。

#### Scenario: 同一人员存在多个名称
- **WHEN** 两个来源中的名称可能指向同一人员但证据不足
- **THEN** 资产档案显示未决身份候选和各自来源，不把两个主体自动合并为一个正式资产

### Requirement: 全链路权限裁剪
系统 SHALL 在字段、段落、图节点与边、搜索结果、时间线、统计聚合和智能体回答各层执行一致的权限裁剪。界面隐藏或遮蔽的内容 MUST NOT 通过导出、计数差异、提示词、检索摘要或关联跳转泄露。

#### Scenario: 用户无权查看敏感关系
- **WHEN** 用户搜索涉及敏感合作关系的组织资产
- **THEN** 搜索、关系图、聚合数字和智能体回答均按照同一裁决裁剪，且审计记录保留裁剪依据

### Requirement: 多租户协作与显式共享
系统 SHALL 以租户、组织、项目和协作空间隔离资产及运行上下文。跨租户共享 MUST 基于显式授权契约，限定对象、字段、目的、期限、再共享条件和撤销方式；共享撤销后应及时终止后续访问并保留使用证据。

#### Scenario: 合作伙伴加入联合项目空间
- **WHEN** 内部组织邀请合作伙伴进入联合项目空间
- **THEN** 合作伙伴只能看到授权契约允许的项目资产和字段，不能访问内部租户的其他关系、记忆或统计数据

### Requirement: 可解释的事实与行动界面
工作台 SHALL 对关键事实、关系、权限裁决、智能体建议、模拟结果和执行动作显示来源证据、版本、世界状态、可信度、冲突、责任主体、确认状态和结果回执。用户 MUST 能从界面追溯到允许展示的原始依据及变更历史。

#### Scenario: 用户质疑智能体建议
- **WHEN** 用户查看智能体提出的合作对象建议
- **THEN** 工作台展示使用的世界快照、事实与关系证据、规则依据、限制条件和建议生成时间，而不是只显示结论
