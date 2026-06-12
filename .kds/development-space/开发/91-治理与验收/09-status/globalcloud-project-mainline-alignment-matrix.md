---
doc_id: GPCF-DOC-6CE17269E9
title: GlobalCloud 项目群项目主线对齐矩阵
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-mainline-alignment-matrix.md
source_path: 09-status/globalcloud-project-mainline-alignment-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群项目主线对齐矩阵

日期：2026-06-12
状态：v1.0 — 全文档项目主线对齐基线
用途：以每一个项目为主线，约束全仓文档中的项目定位、主账边界、AI 分层、治理状态和下一步动作。任何文档出现项目定位冲突时，以本表和 `01-architecture/GlobalCloud绿色供应链体系总架构.md` 为准。

## 一、12 项目主线基线

| # | 项目 | 代号 | 主线定位 | 主责事实 / 主产物 | 明确不承担 | 当前治理状态 | 下一步 |
|---|---|---|---|---|---|---|---|
| 1 | GlobalCloud GFIS | GF | 工厂执行系统 / 工厂事实主账 | 工厂订单、工单、生产报工、质量检验、质量放行、库存事务、批次、设备维护、发货出库、工厂执行证据 | 平台订单主账、客户签收/POD 主账、治理审批主账 | not_started | 进入 Loop Engineering P1 初始化，补 loop-state 与运行证据 |
| 2 | GlobalCloud GPC | GP | 绿色供应链公共服务平台本体 | 平台订单、需求池、供应商协作、产能协同、工厂分配、ASN、预约、运输、POD、异常协同、绿色绩效、合规证据包、服务开放、生态接入 | 工厂执行主账、质量放行、库存扣减、治理审批主账 | not_started | 从 Odoo 原型抽取目标平台骨架，补 Manifest 和一期蓝图 |
| 3 | GlobalCloud PVAOS | PV | 平台运营与门户底座 | 租户、组织、用户、角色、权限、伙伴档案、项目空间、应用入口、门户菜单、平台运营配置 | 平台订单主账、工厂事实主账、治理审批主账 | not_started | 补 Manifest，固化组织/伙伴/项目入口样本 |
| 4 | GlobalCloud WAES | WA | 治理、证据确证、状态门控、合规、风险、审计、AI 越权控制系统 | 治理规则、证据确证、状态门控、合规校验、风险控制、审计追踪、模型授权、AI 越权拦截、异常升级、验收证据管理 | 平台订单主账、工厂执行主账、具体事务审批 | not_started | 补 Manifest，建立控制塔只读数据接入和 Evidence Ledger 样本 |
| 5 | GlobalCloud KDS | KD | 企业知识主存 | 知识真源、版本、发布、权限、归档、canonical source | 业务事实、AI 直接建议、治理审批 | not_started | 进入 Loop Engineering P1 初始化，继续压实 KDS/Brain 单向关系 |
| 6 | GlobalCloud Brain | BR | 知识编制与引擎 / 知识 UI 平台 | 编制视图、检索索引、RAG 服务、案例与 SOP 消费视图 | 知识主存替代、业务事实、治理审批 | not_started | 进入 Loop Engineering P1 初始化，补 remote/doctor/schema 证据 |
| 7 | GlobalCloud PKC | PK | 个人知识工作台 | 个人仪表盘、任务、通知、跨项目状态同步、个人侧协作视图 | 平台主账、工厂主账、治理审批 | not_started | 进入 Loop Engineering P1 初始化，补 Manifest 和用户闭环 |
| 8 | GlobalCloud XiaoC | XC | 蚁后：AI 能力生产与编排路由 | Prompt/MCP、模型路由、Agent 模板、任务拆解、评估、结果汇总 | 直接写业务主账、绕过 WAES 授权 | partial | 补 loop-state，补 Prompt/模型路由/任务拆解验证样本 |
| 9 | GlobalCloud XGD | XD | 大象：长程 Agent、重分析、多端交互和复杂任务承载 | 长程上下文、复杂分析、根因分析、桌面/语音/社交交互、重分析回执 | 质量放行、交期承诺、停线决策、业务主账写入 | not_started | 补 Manifest，定义深度分析接口和越权边界 |
| 10 | GlobalCloud XiaoG | XG | 轻量执行入口 / 蚂蚁 | 轻量查询、通知、后台任务、语音入口、受授权工具调用 | 未授权写接口、业务主账、治理审批 | not_started | 补 Manifest，预激活 ESP32/WebSocket 接入可靠性基线 |
| 11 | GlobalCloud MMC | MM | 管理配置中心 / 治理模板基线 | 治理模板、配置标准化、策略边界、项目群管理配置样板 | 业务主账、运行事实、项目完成状态裁决 | not_started | 进入 Loop Engineering P1 初始化，补 Manifest 和模板基线证据 |
| 12 | GlobalCoud GPCF | CF | 体系文档工作区 / 总控治理仓 | 统一口径、交叉分析、状态矩阵、证据索引、Harness 治理入口 | 业务运行主账、真实系统运行结果伪造 | not_started | 补 loop-state，维护全仓项目主线对齐 |

## 二、全仓对齐规则

1. 全仓只使用 `GPC`，不再使用旧的复合命名或历史后缀。
2. GPC 的正式定位是“绿色供应链公共服务平台本体”，不是临时中间层，也不是单厂 MES/WMS。
3. 当前 `/Users/lujunxiang/Projects/GlobalCloud GPC` 只能作为 Odoo 历史原型和流程样本，不能写成 GPC 目标平台完成态。
4. GFIS 负责工厂执行事实和发货出库；客户签收、POD、外部运输和平台协同事实归 GPC；Edge 是现场采集与边缘缓冲层，优先服务 GFIS，但不作为当前 12 项目之一单列。
5. WAES 负责治理、证据、状态门控、审计和 AI 授权；不承办质量放行、库存调整、发货、签收、交期承诺等具体业务事务。
6. KDS 是知识主存；Brain 是知识编制、检索和 UI/引擎层，不替代 KDS。
7. XiaoC 是蚁后；XGD 是大象；XiaoG/Hermes 是轻量执行入口。AI 建议不得直接写业务主账。
8. 配置通过、文档通过、控制塔可见，不等于业务闭环完成；状态升级必须有 evidence。

## 三、已执行的全仓对齐检查

| 检查项 | 结果 |
|---|---|
| 旧 GPC 命名残留 | 已清理旧复合命名和历史后缀口径 |
| GPC 定位残留 | 已将中台式口径对齐为公共服务平台口径 |
| AI 分层残留 | 已清理 XiaoC/XGD 的旧角色口径 |
| 文档格式 | `git diff --check` 已通过 |

## 四、后续同步要求

1. 新增或修订任何文档时，必须先对照本表确认项目主线和主责边界。
2. `07-acceptance` 的验收项必须引用本表中的主责系统，不能把 WAES 看板通过写成业务完成。
3. `03-data-ai-knowledge` 的对象、事件、连接器、数据库边界必须与本表一致。
4. `05-agent-team` 与 `06-workstreams` 的专项包命名必须与本表一致。
5. `09-status/gpcf-project-status-matrix.md` 是状态入口，本表是项目定位入口；两者必须同步更新。
