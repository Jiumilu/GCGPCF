---
doc_id: GPCF-DOC-GCWORLD-046
title: GCWORLD工作台界面基础能力规格
project: GPCF
related_projects: [Studio, Brain, KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-workbench-ui-foundation/specs/gcworld-workbench-ui-foundation/spec.md
source_path: openspec/changes/gcworld-workbench-ui-foundation/specs/gcworld-workbench-ui-foundation/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 十二工作中心共享世界上下文
工作台 SHALL 提供世界总览、组织资产、关系网络、项目世界、时间与事件、智能体、行动与协同、权限与身份、模拟实验室、事实治理、治理与审计、开发与运维十二个中心，并 MUST 在中心切换时保持同一资产、快照、租户、项目和权限上下文。

#### Scenario: 从关系网络进入项目世界
- **WHEN** 用户从某条项目关系进入项目世界
- **THEN** 工作台保持相同项目标识、世界快照和裁决引用，不重新创建项目对象

### Requirement: 单一资产档案保留未决状态
人员、组织、团队、项目、角色、智能体和系统 SHALL 使用统一档案骨架展示事实、历史、别名、关系、授权、任务、行动、结果、证据和冲突。未决身份 MUST 以候选呈现，禁止静默并入正式档案。

#### Scenario: 查看证据不足的同名人员
- **WHEN** 用户打开可能对应多个身份的人员提及
- **THEN** 工作台展示候选、来源和待复核状态，不选择其中一个作为正式人员

### Requirement: 世界状态可视且不可混淆
工作台 SHALL 使用中文文字、非颜色视觉标记和颜色共同区分事实、运行、目标、模拟、候选、冲突与受限状态。目标、模拟和候选 MUST NOT 采用与事实相同的主视觉语义。

#### Scenario: 查看模拟组织调整
- **WHEN** 用户打开模拟分支中的组织结构
- **THEN** 页面持续显示模拟分支、基线快照和假设标识，不将关系标注为当前事实

### Requirement: 全链路使用同一权限裁剪
字段、段落、图节点与边、搜索、时间线、统计、导出和智能体回答 SHALL 使用同一WAES裁决和世界快照。客户端隐藏 MUST NOT 代替服务端裁剪，受限内容不得通过数量、占位或跳转泄漏。

#### Scenario: 用户无权查看敏感合作关系
- **WHEN** 用户搜索涉及敏感合作关系的组织
- **THEN** 搜索结果、图谱、聚合、导出和智能体回答均应用同一限制并记录裁剪依据

### Requirement: 首期界面保持只读
在运行时集成和动作授权独立通过前，工作台 MUST 将真实写操作、跨租户共享和外部行动保持禁用。草稿或建议入口 SHALL 明确标注不会产生外部副作用。

#### Scenario: 用户尝试从只读档案发送消息
- **WHEN** 用户在未获得运行时授权的工作台中请求发送外部消息
- **THEN** 工作台阻断发送，最多允许保存本地草稿并显示所缺授权

### Requirement: 产品证据分级
Harness SHALL 分别记录静态设计、固定数据原型、只读集成、权限集成和真实运行证据。截图或可访问页面 MUST NOT 单独证明数据链、权限或动作执行已经完成。

#### Scenario: 十二个中心均可打开
- **WHEN** 演示环境能够导航十二个中心但仅使用固定样例数据
- **THEN** Harness最多确认原型结构，不标记已集成、生产就绪或完成

### Requirement: 独立授权先于产品实现
在产品仓库、后继Feature、责任人、数据范围、设计基线、测试环境和回滚获得独立批准前，系统 MUST 将本能力保持为规划状态。

#### Scenario: 规划文档通过严格校验
- **WHEN** 本变更的规划产物全部通过OpenSpec校验但产品授权尚未签发
- **THEN** 系统不修改Studio、Brain或其他产品仓库，也不启动界面实现

