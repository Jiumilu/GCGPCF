---
doc_id: GPCF-DOC-GCWORLD-006
title: GCWORLD 职能智能体治理规格
project: GPCF
related_projects: [XWAIL, WAES, MMC, KDS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-role-agent-governance/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-role-agent-governance/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 职能智能体注册
系统 SHALL 区分真人主体、组织职能智能体、系统智能体和外部或合作伙伴智能体。每个 GCWORLD 智能体 SHALL 登记智能体标识、绑定资产、角色任用、上下文、责任人、监督人、来源范围、运行模式、能力、知识范围、记忆策略、工具和连接器范围、授权引用、允许动作、禁止动作、风险上限、委托规则、失效时间和撤销策略。职能智能体 MUST NOT 将自身表述为与角色关联的真实人员。

#### Scenario: 创建项目协调职能智能体
- **WHEN** 操作人员为项目协调角色提出智能体注册
- **THEN** 注册信息必须在智能体运行前明确项目角色、人工责任人、允许使用的证据范围和禁止的外部动作

#### Scenario: 查询镜像模式智能体
- **WHEN** 用户查询注册为 `mirror` 模式的智能体
- **THEN** 智能体仅返回与证据关联的画像和关系信息，不得创建任务、消息或业务动作

### Requirement: 行动信封与确认边界
系统 SHALL 要求每个超出只读观察范围的智能体动作都携带行动信封。信封 MUST 记录智能体标识、行动角色、目标、预期动作、证据引用、风险、授权状态、确认状态和结果。涉及对外沟通、资金、合同、权限、身份、政府沟通或业务状态的动作，在没有独立授权和人工确认时 MUST 保持阻断。

#### Scenario: 智能体起草外部合作伙伴消息
- **WHEN** 智能体为合作伙伴准备消息
- **THEN** 智能体可以保存带证据引用的草稿，但在记录所需授权和人工确认前不得发送消息

### Requirement: 可审计的智能体执行账本
系统 SHALL 为允许的智能体动作与结果保留只追加执行账本，包括无动作和被阻断动作。账本 MUST 区分建议、草稿、已批准执行、已拒绝执行和执行失败。

#### Scenario: 请求执行禁止动作
- **WHEN** 智能体收到超出其注册运行模式的请求
- **THEN** 系统记录带禁止原因的阻断执行条目，不产生任何外部副作用

### Requirement: 智能体输出声明与候选边界
每次智能体输出 SHALL 声明所涉及的资产维度、必要时的流类型、生命周期、可信等级、来源引用、证据引用和零写入声明。字段缺失、引用失效、证据不足或来源哈希过期时，输出 MUST 仅进入活动日志或候选池。

#### Scenario: 智能体生成缺少证据的项目结论
- **WHEN** 智能体输出项目结论但没有有效来源和证据引用
- **THEN** 系统将输出限制在候选池并禁止写入正式事实或业务台账

### Requirement: 五层智能体记忆治理
系统 SHALL 区分会话记忆、任务记忆、角色记忆、资产记忆和学习记忆。会话记忆应短期可清除；任务记忆随任务关闭归档；角色记忆随角色任用失效而冻结；资产记忆只引用 KDS 正式事实；学习记忆只形成待治理候选。

#### Scenario: 角色任用被撤销
- **WHEN** 与某职能智能体绑定的角色任用被撤销
- **THEN** 系统冻结其角色记忆和授权范围，撤销运行会话，并保留可审计历史记录

### Requirement: 智能体行动风险分级
系统 SHALL 将智能体行动分为 R0 观察、R1 建议、R2 内部执行、R3 受控外部执行和 R4 重大行动。R0 需要身份与资源校验；R1 需要零写入和来源声明；R2 需要明确授权、回执和可补偿性；R3 需要人工确认或双重审批；R4 需要不可绕过的硬门禁、多人治理和完整审计。

#### Scenario: 智能体提出政府正式沟通
- **WHEN** 智能体请求执行政府正式沟通
- **THEN** 系统将其归类为 R4，要求硬门禁和多人治理，不允许以辅助或自治模式直接执行
