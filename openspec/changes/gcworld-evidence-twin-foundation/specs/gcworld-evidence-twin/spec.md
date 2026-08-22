---
doc_id: GPCF-DOC-GCWORLD-004
title: GCWORLD 证据数字孪生规格
project: GPCF
related_projects: [KDS, WAS, WAES]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-evidence-twin/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-evidence-twin/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 证据关联的组织资产
系统 SHALL 将 GCWORLD 资产表示为人员、组织、团队、项目、系统、物理资产、文档、角色或关系端点之一。每条资产记录 SHALL 包含稳定世界标识、来源系统标识、租户标识、WAS 资产维度、权威类型、生命周期、本体版本、来源引用、证据引用、可信等级，以及已知情况下的有效时间与记录时间。系统 MUST 保留别名和不确定性，禁止自动合并身份。

#### Scenario: 发现存在歧义的人员提及
- **WHEN** 来源记录中的人名可能对应多个身份
- **THEN** 系统记录带来源证据的候选引用，将身份标记为未决，不得直接关联到权威人员资产

### Requirement: 四类世界状态隔离
系统 SHALL 将每条世界状态记录唯一标记为 `fact`（事实）、`operational`（运行）、`target`（目标）或 `simulation`（模拟）之一。证据层级和候选分类 MUST 与世界状态分开保存。目标和模拟记录在未经独立授权复核前 MUST NOT 展示为事实观察，也不得写入 KDS 权威事实。

#### Scenario: 模拟产生项目延期结果
- **WHEN** 情景模型依据明确假设计算出可能延期
- **THEN** 输出以 `simulation` 保存，并记录输入版本和假设，不得展示为项目实际状态

#### Scenario: 记录项目计划
- **WHEN** 项目计划陈述预期产能或收入结果
- **THEN** 系统将其以 `target` 保存并记录来源与计划周期，不得视为已经实现的事实

### Requirement: 证据关联的时态关系
系统 SHALL 使用主体资产、关系谓词、客体资产、上下文引用、主流类型、流组合、证据引用、证据状态和已知有效时间范围表示每条关系。当关系谓词、上下文、流类型或有效时间范围不同时，系统 MUST 允许同一组资产之间存在多条关系。

#### Scenario: 人员的组织角色发生变化
- **WHEN** 证据表明某人在指定日期后承担新角色
- **THEN** 系统保留带有效时间范围的原角色关系，并为新角色建立或提出另一条时间限定关系

### Requirement: WAS 权威语义与八流继承
系统 SHALL 从 WAS 权威注册表加载资产维度、关系、事件、动作、生命周期和流类型，并记录 `assetDimension`、`ontologyVersion` 和 `schemaRef`。GCWORLD MUST NOT 建立与 WAS 竞争的本地枚举。关系和业务过程 SHALL 声明物质流、信息流、资金流、能量流、商流、知识流、规则流或时空流中的主流类型；涉及多类流时使用 `flowBundle`。

#### Scenario: 新资产维度尚未通过 WAS 治理
- **WHEN** GCWORLD 收到一个不在当前 WAS 权威注册表中的资产维度
- **THEN** 系统拒绝将其作为正式世界资产实例，并要求先完成 WAS 版本治理与校验

### Requirement: 双时间与不可变世界快照
系统 SHALL 为资产、关系、角色、授权和状态分别保存现实有效时间与系统记录时间。关键查询和行动 MUST 绑定不可变世界快照，快照至少包含快照标识、截止时间、本体版本、事实集版本、身份版本、策略版本、资源版本、租户上下文、项目上下文、来源引用、证据引用和快照哈希。

#### Scenario: 补录历史任职事实
- **WHEN** 系统在当前时间录入一条过去已经生效的任职事实
- **THEN** 有效时间记录其现实生效区间，记录时间保存本次获知时点，历史快照查询能够区分两者

### Requirement: 事件、行动、结果与承诺对象
系统 SHALL 分离建模事件、行动、结果和承诺。事件记录参与主体、发生与记录时间、地点、状态变化、流组合和来源；行动记录权利主体、执行者、智能体、目标资源、目的和裁决标识；结果记录行动引用、状态、影响、证据与后续事项；承诺记录承诺方、受益方、范围、到期时间、状态和证据。

#### Scenario: 会议形成交付承诺
- **WHEN** 已确认会议纪要记录某主体在指定日期前交付某项成果
- **THEN** 系统建立与会议事件和责任主体关联的承诺对象，不将普通讨论意向自动提升为合同义务
