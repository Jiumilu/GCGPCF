---
doc_id: GPCF-DOC-F6D4D8B07A
title: 跨项目 Agent 长期记忆系统
project: GFIS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/.kunsdd/draft/f423b226-0141-4aac-8df6-728f615aa3a1/requirement.md
source_path: .kunsdd/draft/f423b226-0141-4aac-8df6-728f615aa3a1/requirement.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# 跨项目 Agent 长期记忆系统

## 背景

GlobalCloud 项目群包含 12 个项目（GFIS、GPC、WAES、KDS、Brain、PKC、MMC、PVAOS、XiaoC、XGD、XiaoG、GPCF），多个 AI Agent（Kun、Codex 等）在不同项目中独立工作。当前痛点：

1. Agent 会话上下文无法跨项目复用——在项目A中分析确认的事实、决策、模式，切换到项目B后需要重新推导或人工传递。
2. 已有 KDS 11池和 GC-Knowledge Fabric 底座，但缺少面向 Agent 工作流的「记忆层」——KDS 侧重业务事实治理，未覆盖 Agent 运行时上下文（决策链、分析中间产物、项目间引用关系）。
3. 跨项目分析（如交叉分析报告、主线对齐矩阵）依赖人工汇总，Agent 无法主动引用其他项目的已确认结论。
4. 长期来看，多 Agent 协作需要共享记忆以减少重复推导、提高一致性、支持审计回溯。

本项目群已有基础设施：KDS 分布式知识事实底座、OKF 知识契约、WAES 规则门禁、LOOP 治理闭环、Harness 证据留存。跨项目长期记忆应作为 Knowledge Fabric 的「Agent 记忆扩展层」设计，复用现有治理链路，不另起炉灶。

## 目标

1. **记忆存储**：为每个项目定义可被 Agent 读写的「长期记忆条目」schema，存入 KDS 对应资源池，遵循现有状态机（candidate → confirmed → deprecated）。
2. **跨项目检索**：Agent 在任意项目上下文中，可按项目、领域、关键词、时间范围检索其他项目的已确认记忆条目，作为当前会话的参考上下文。
3. **引用追溯**：每条记忆记录来源项目、关联 doc_id、确认人/Agent、确认时间和变更历史，支持跨项目引用审计。
4. **记忆生命周期**：定义记忆条目的创建（Agent 候选 → 人工确认）、更新、废弃、版本化的完整流程，与现有 WAES 门禁和人工确认队列对齐。
5. **边界控制**：遵守项目边界声明——记忆系统只读其他项目已确认条目，不写入其他项目仓库；密级和可见范围遵循分布式知识系统权限与密级矩阵。
6. **复用现有资产**：尽最大可能复用 KDS 11池、Knowledge Fabric 的确认队列/委员会机制、底座闭环率评分模型，以及 Agent 团队的交付包责任分解和 LOOP 治理。

## 验收标准

1. 有经过评审的「Agent 长期记忆条目」schema 定义文档，至少覆盖：条目ID、所属项目、领域标签、记忆类型（事实/决策/模式/引用）、内容摘要、来源 doc_id 列表、确认状态、密级、时间戳。
2. 有 1 个端到端示例：Agent 在项目A中产出并确认一条记忆条目，Agent 在项目B中成功检索并引用该条目，引用链路可审计。
3. 检索接口至少支持：按项目过滤、按领域过滤、关键词模糊匹配、按时间范围过滤。
4. 记忆条目遵循与 Knowledge Fabric 一致的状态机，candidate 状态条目不可被其他项目 Agent 检索（防止污染）。
5. 有至少 1 条人工确认流程记录，证明记忆条目从 candidate → confirmed 经过了 WAES 门禁或人工确认队列。
6. 底座可用知识闭环率评分模型纳入记忆条目维度——新增「记忆条目 candidate→confirmed 转化率」和「跨项目引用有效率」指标。
7. 本需求不要求：真实业务系统写入、积分/收益结算、全量项目覆盖。首批范围限定 GPCF + 1个关联项目（建议 GFIS 或 KDS）的 dry-run 验证。
