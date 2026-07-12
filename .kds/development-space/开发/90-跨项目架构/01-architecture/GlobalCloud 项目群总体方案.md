---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-MASTER-PLAN-20260626
title: GlobalCloud 项目群总体方案
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, ICP]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud 项目群总体方案.md
source_path: 01-architecture/GlobalCloud 项目群总体方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
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

项目群当前纳入 18 个项目。2026-06-28 以前形成的17项目证据继续作为历史基线，不因新增 ICP 回写或重算：

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
| ICP | 24字产业模型、十一池只读资源投影、场景编排、产业匹配和控制决策候选 |

## 2.2 GC-ICP 产业控制平面边界

GC-ICP 是项目群产业控制中枢候选项目，拥有产业建模、资源投影、场景评估和产业控制决策候选职责，但不拥有业务事实写入权、治理批准权或生产执行权。

| 相邻项目 | 主责保持 | ICP 禁止越权 |
|---|---|---|
| KDS | 知识主存和十一池事实索引 | 不建立第二套资源事实主账 |
| WAES | 治理、证据、状态和人工确认 | 不自动批准或晋升状态 |
| GPC | 平台订单和跨组织协同 | 不创建订单、运输或 POD 事实 |
| GFIS | 工厂生产、质量、库存和设备 | 不排产、放行或控制设备 |
| PVAOS | 租户、组织、伙伴和门户 | 不管理身份或生态主数据 |

ICP 当前状态固定为 `candidate/partial/human_required`，本地契约、API 和 fixture 验证不得解释为真实业务接入、项目群集成或生产就绪。

## 2.1 武汉城市圈绿色供应链运营 SOP 场景链路

武汉城市圈绿色供应链运营 SOP 是项目群首个按“运营在前、投厂在后、订单先行、本地协同”进入受控内部试运行的场景链路。该链路覆盖武汉、应城、咸宁、武穴和 N 地区五个任务单元，目标是在 2026-06-29 至 2026-07-05 首轮 7 天内部试运行中跑通统一订单池、G0-G8 轻量闸门、红黄灯清单、周评分和补证队列。

项目群职责边界如下：

| 项目 | 场景职责 | 边界 |
|---|---|---|
| SOP | 输出场景规则、模板、评分口径、硬否决项和周评分报告 | 不制造业务事实，不替代 owner 确认 |
| KDS | 作为客户、订单、主体、合同、交付、回款和会议材料的唯一知识事实引用源 | 未授权前只读，不执行真实 KDS API 写入 |
| GFIS | 承接 G5-G7 以后生产、质检、仓储、发货、POD、财务凭证和运行层主键 | 无真实 source-of-record 时不得声明真实 SOP E2E |
| GPC | 承接订单池、红黄灯、签收、异常和周评分看板等后续页面需求 | 不以页面可见替代业务闭环 |
| GPCF | 纳入项目群门禁、证据、状态矩阵、依赖矩阵和 LOOP 闭环 | 不替代业务 owner、WAES 或客户验收 |
| WAES | 承接授权、审查、越权控制和状态裁决入口 | 未经人工确认不得 accepted、integrated 或 production_ready |

该链路的总体定位是 `controlled_internal_pilot`。它可以作为项目群真实运营补证和系统开发任务的输入，不得直接声明正式 SOP 发布、客户验收、生产运行完成、项目群集成完成或 1+8 全覆盖已达成。

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

## 6. GlobalCloud 宪法继承与治理归属

本方案继承 `GlobalCloud宪法`。宪法是产业模型的具体实践总纲和项目群最高规范性权威文件；本方案是其授权下的最高总体执行控制文件，不得反向覆盖宪法的产业模型、根本原则、体系边界和权威关系。

宪法治理的产业领域主责归 ICP，canonical 正本与版本保管归 KDS。SOP 负责修订程序与审计，GPCF 负责方案传导、冲突检测和 G00 继承门禁，WAES 与人工负责授权和状态裁决。任何单一项目不得完成自提、自审、自批、自发布闭环。
