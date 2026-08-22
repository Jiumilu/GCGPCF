---
doc_id: GPCF-DOC-GCWORLD-007
title: GCWORLD 运行边界规格
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, MMC, GFIS, Brain, Studio]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-runtime-boundary/spec.md
source_path: openspec/changes/gcworld-evidence-twin-foundation/specs/gcworld-runtime-boundary/spec.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: GCWORLD 系统边界
系统 SHALL 保持以下职责分离：WAS-Ontology 负责世界语义；KDS 负责来源、主张、事实、证据和事实生命周期；GCWORLD 负责世界投影、运行上下文与工作台视图；XWAIL 负责智能体认知和协同；WAES 负责规则、风险、权限和状态门禁裁决；KWE 负责编排工单、确认包和人工流转；MMC 负责模型、API、MCP 和连接器能力；GFIS、GPC、ERP 等业务系统负责现实执行和业务主账；Brain/PKC 提供知识与个人团队入口；LOOP/Harness 负责证据、验收、审计和持续治理。GCWORLD MUST NOT 绕过或复制任何责任系统的权威职责。

#### Scenario: 智能体提出合同相关动作
- **WHEN** 智能体在 GCWORLD 中提出合同相关动作
- **THEN** GCWORLD 记录提案和所需授权；在责任系统门禁未通过前，不执行动作，也不写入业务系统

### Requirement: 十二个受控工作中心
系统 SHALL 定义世界总览、组织资产、关系网络、项目世界、时间与事件、智能体、行动与协同、权限与身份、模拟实验室、事实治理、治理与审计、开发与运维十二个工作中心。第一阶段以只读视图为主，每个视图 MUST 显示派生记录的证据状态、世界状态类型、版本和权限裁剪依据。

#### Scenario: 用户打开关系网络视图
- **WHEN** 用户查看两个组织资产之间的关系
- **THEN** 视图显示关系类型、方向、有效时间范围、证据引用、可信度、冲突状态、可见范围和允许智能体使用的范围

### Requirement: 分阶段受控演进
系统 SHALL 按 P0 架构冻结与契约、P1 组织资产普查、P2 只读世界运行时、P3 内部辅助智能体、P4 GCWORLD-AUTH、P5 模拟实验室、P6 受控真实执行、P7 有限自治与扩域的顺序交付。每一阶段 MUST 具有独立退出条件，前一阶段完成 MUST NOT 自动授权下一阶段。

#### Scenario: 普查评估完成但仍有例外
- **WHEN** 普查评估完成时仍存在未决引用
- **THEN** 结果仅能以部分完成评估进入复核，不授权可写工作台或智能体执行
