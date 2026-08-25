---
doc_id: GPCF-DOC-GCWORLD-047
title: GCWORLD受控运行时集成能力规格
project: GPCF
related_projects: [XWAIL, WAES, KWE, MMC, KDS, GFIS]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-controlled-runtime-integration/specs/gcworld-controlled-runtime-integration/spec.md
source_path: openspec/changes/gcworld-controlled-runtime-integration/specs/gcworld-controlled-runtime-integration/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 运行闭环不可跳步
系统 SHALL 按观察、解析、世界快照、推理、裁决、确认、执行、取证、提升和学习推进真实动作。需要写入或外部影响的动作在裁决与规定确认完成前 MUST NOT 调用执行系统。

#### Scenario: R3动作缺少人工确认
- **WHEN** 动作已经获得WAES条件允许但尚未取得规定的人工确认
- **THEN** 系统停留在待确认状态，不调用连接器，也不生成成功回执

### Requirement: 运行身份逐层收窄
真人会话、智能体调用、智能体运行身份、连接器凭据和业务动作 SHALL 使用相互独立且可撤销的身份。有效能力 MUST 取主体、角色、授权、智能体契约、资源策略、情境和风险门禁的交集。

#### Scenario: 智能体能力超过授权
- **WHEN** 智能体具备发送消息的工具能力但当前授权只允许形成建议
- **THEN** 系统只允许生成建议并阻断发送，记录能力与权限差异

### Requirement: 裁决绑定一致世界快照
每次裁决 SHALL 绑定世界快照、身份版本、策略版本、授权版本、资源版本、签发与失效时间和裁决摘要。高风险动作 MUST 在提交前再次验证这些版本。

#### Scenario: 裁决后角色被撤销
- **WHEN** R3动作提交前发现角色或授权版本已经变化
- **THEN** 系统拒绝旧裁决并要求基于最新快照重新计算

### Requirement: 可靠命令和补偿
所有写命令 SHALL 携带命令标识、幂等键、事件标识、因果标识、关联标识和契约版本，并使用去重、可控重试、死信和补偿处理部分失败。重复命令 MUST NOT 产生重复业务副作用。

#### Scenario: 连接器超时后收到重复命令
- **WHEN** 调用方以相同幂等键重试一个结果未知的命令
- **THEN** 系统返回既有处理结果或继续原处理，不再次执行目标动作

### Requirement: R0至R4阶段门禁
系统 SHALL 将观察、建议、内部写入、受控外部执行和重大行动分别归为R0至R4，并在阶段开关和单次裁决两层同时约束。较低阶段获准 MUST NOT 自动开启较高风险动作。

#### Scenario: R0镜像阶段请求内部写入
- **WHEN** 当前运行阶段只允许R0镜像而智能体提出R2内部写入
- **THEN** 系统阻断动作并记录缺少阶段授权，不因技术连接器可用而放行

### Requirement: 执行与责任回执完整
每次允许、拒绝、失败、撤销和补偿 SHALL 形成不可变回执，关联主体、代表关系、智能体、世界快照、裁决、确认、执行系统、结果和责任归属。缺少目标系统结果证据时 MUST NOT 标记成功。

#### Scenario: 目标系统部分完成后失败
- **WHEN** 动作在目标系统产生部分副作用后返回失败
- **THEN** 系统记录部分完成回执并按批准策略执行或请求补偿，不伪造成功

### Requirement: 故障时默认拒绝或只读
WAES不可用、事实版本不可验证、身份上下文不完整或撤销状态未知时，高风险动作 MUST 被阻断，低风险操作最多降级为只读。

#### Scenario: WAES在重大动作前不可用
- **WHEN** R4动作无法获得当前有效裁决
- **THEN** 系统阻断动作，不使用缓存允许或普通紧急开关绕过

### Requirement: 独立授权先于运行实现
在Release、后继Feature、目标仓库、责任人、服务范围、环境、凭据、数据范围、回滚和Harness门禁获得独立批准前，系统 MUST 保持零真实执行和零外部写入。

#### Scenario: 运行时规划通过结构校验
- **WHEN** 本变更规划产物全部完成但运行授权尚未签发
- **THEN** 系统不启动服务、不申请连接器凭据、不连接真实系统并保持状态未提升
