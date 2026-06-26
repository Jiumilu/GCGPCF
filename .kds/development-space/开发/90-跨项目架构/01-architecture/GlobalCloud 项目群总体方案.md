---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-MASTER-PLAN-20260626
title: GlobalCloud 项目群总体方案
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud 项目群总体方案.md
source_path: 01-architecture/GlobalCloud 项目群总体方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群总体方案

## 1. 定位

本文是 GlobalCloud 项目群最高层总体控制性方案，负责项目群架构、术语、版本、兼容矩阵、方案传导、项目边界与协同控制。

本文与 `GlobalCloud 项目群实施方案.md` 共同构成项目群双总控：

| 总控体系 | 主文件 | 控制范围 |
|---|---|---|
| GlobalCloud 项目群总体方案体系 | `01-architecture/GlobalCloud 项目群总体方案.md` | 架构、术语、版本、兼容矩阵、方案传导、项目边界、协同控制 |
| GlobalCloud 项目群实施方案体系 | `GlobalCloud 项目群实施方案.md` | 真实进度、真实研发、真实运行、真实集成、真实交付、客户验收、任务包、命令、证据、门禁、回滚、LOOP 闭环 |

## 2. 项目群范围

项目群当前纳入 17 个项目：

| 项目 | 主职责 |
|---|---|
| WAS | 世界资产体系总体语义、架构和治理基线 |
| XWAIL | WAS 的机器建模语言、契约、Profile 和验证机制 |
| AaaS | 基于 XWAIL 契约的资产服务化、计量、SLA 和证据要求 |
| WAES | 基于 WAE 的业务实现，承担资产主账、浏览、编排、注册、授权和发布入口 |
| GFIS | 供应链真实业务事实源和运行记录输入 |
| GPC | 绿色供应链公共服务平台和场景协同入口 |
| PVAOS | 供应链价值联盟运营平台 |
| KDS | 知识主存、本地镜像、RAG 导出和证据知识化 |
| Brain | 企业知识治理、高级工作台、语义检索和智能分析 |
| Studio | 研发、治理和发布工作台 |
| MMC | 治理模板、模型管理和复用控制 |
| PKC | 个人知识、任务和 KDS/Brain 工作流协同 |
| XGD | Agent/TICK/Brain smoke 与长程协同能力 |
| XiaoC | 模型路由、Agent 团队和智能协作能力 |
| XiaoG | live API、通知、审计和设备验证授权包 |
| SOP | 绿色供应链场景 SOP 和对外材料候选 |
| GPCF | 项目群治理、文档、证据、门禁、状态传导和 LOOP 编排 |

## 3. 总体架构原则

| 原则 | 控制要求 |
|---|---|
| 一个总控体系 | 项目群总体方案和项目群实施方案为双主控，所有项目方案必须继承 |
| 多个受控项目 | 每个项目只能有一个唯一总体方案和一个唯一实施方案 |
| 真实证据驱动 | 运行、集成、交付和验收必须绑定命令、证据、门禁和回滚边界 |
| 双向传导 | 项目群主方案变化传导到项目；项目方案变化回传项目群主方案并影响关联项目 |
| 不越权升级 | 未经人工确认，不得声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted` |

## 4. 方案传导机制

| 变更来源 | 处理方式 | 必要证据 |
|---|---|---|
| 项目群总体方案变化 | 建立影响范围，传导到相关项目总体方案和实施方案 | 方案识别规则、影响矩阵、项目方案更新记录、validator |
| 项目群实施方案变化 | 传导到项目实施方案、任务包、证据门禁和 LOOP 状态 | 真实执行治理总控板、任务包、依赖矩阵、状态推进矩阵 |
| 项目级总体方案变化 | 回传 GPCF，判断是否影响术语、架构、边界或兼容矩阵 | 项目变更说明、影响项目清单、主方案修订或豁免记录 |
| 项目级实施方案变化 | 回传 GPCF，判断是否影响进度、任务、门禁、回滚或验收 | evidence、validator、任务包和状态矩阵更新 |

## 5. 当前基线

```text
project_group_master_plan = controlled
project_group_implementation_plan = controlled
scheme_recognition_scope = AGENTS.md + project master plans + project implementation plans
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

本文只建立项目群总体控制基线，不声明真实运行、真实集成、真实交付或客户验收完成。
