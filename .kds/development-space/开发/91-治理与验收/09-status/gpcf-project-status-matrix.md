---
doc_id: GPCF-DOC-C586488E67
title: GPCF Project Status Matrix
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/gpcf-project-status-matrix.md
source_path: 09-status/gpcf-project-status-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF Project Status Matrix

日期：2026-06-12
状态：v1.2 — 对齐项目主线定位
用途：GPCF 总控（小即）跨项目收口的唯一入口。每次中循环审计后更新。

## 项目群状态总表

| # | 项目 | 代号 | 主线定位 | 牵头智能体 | Manifest | loop-state | 微循环轮次 | evidence完整率 | 当前状态 | 阻塞项 | Harness判定 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GlobalCloud GFIS | GF | 工厂执行系统 / 工厂事实主账 | 厂行 | 是 | 否 | 0 | 0% | not_started | - | - | 试点项目，P1 初始化 |
| 2 | GlobalCloud GPC | GP | 绿色供应链公共服务平台本体 | 链同 | 否 | 否 | 0 | 0% | not_started | 目标平台骨架尚未形成可验收实现 | - | 补齐 Manifest 与一期蓝图 |
| 3 | GlobalCloud PVAOS | PV | 平台运营与门户底座 | 链同 | 否 | 否 | 0 | 0% | not_started | - | - | 补齐 Manifest（P2） |
| 4 | GlobalCloud WAES | WA | 治理 / 证据 / 状态门控 / AI 越权控制 | 宪衡 | 否 | 否 | 0 | 0% | not_started | - | - | 补齐 Manifest（P2） |
| 5 | GlobalCloud KDS | KD | 企业知识主存 | 数枢 | 基础 | 否 | 0 | 0% | not_started | - | - | 试点项目，P1 初始化 |
| 6 | GlobalCloud Brain | BR | 知识编制与引擎 / 知识 UI 平台 | 灵策 | 基础 | 否 | 0 | 0% | not_started | - | - | 试点项目，P1 初始化 |
| 7 | GlobalCloud PKC | PK | 个人知识工作台 | 链同 | 否 | 否 | 0 | 0% | not_started | - | - | 试点项目，P1 初始化 |
| 8 | GlobalCloud XiaoC | XC | 蚁后：AI 能力生产与编排路由 | 灵策 | partial | 否 | 0 | 0% | partial | UI 测试 / Wrangler / loop-state 缺口 | - | 补齐 loop-state.md |
| 9 | GlobalCloud XGD | XD | 大象：长程 Agent、重分析、多端交互和复杂任务承载 | 灵策 | 否 | 否 | 0 | 0% | not_started | Manifest 缺口 | - | 补齐 Manifest（P1） |
| 10 | GlobalCloud XiaoG | XG | 轻量执行入口 / 蚂蚁 | 接稳 | 否 | 否 | 0 | 0% | not_started | Manifest 缺口 | - | 补齐 Manifest（P1） |
| 11 | GlobalCloud MMC | MM | 管理配置中心 / 治理模板基线 | 宪衡 | 否 | 否 | 0 | 0% | not_started | Manifest 缺口 | - | 试点项目，P1 初始化 |
| 12 | GlobalCoud GPCF | CF | 体系文档工作区 / 总控治理仓 | 小即 | 是 | 否 | 0 | 0% | not_started | loop-state 缺口 | - | 补齐 loop-state.md |

## 状态分布统计

| 状态 | 项目数 | 项目 |
|---|---|---|
| not_started | 11 | GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XGD、XiaoG、MMC、GPCF |
| loop_ready | 0 | - |
| loop_running | 0 | - |
| evidence_ready | 0 | - |
| audit_ready | 0 | - |
| harness_review | 0 | - |
| accepted | 0 | - |
| integrated | 0 | - |
| partial | 1 | XiaoC |
| blocked | 0 | - |

## 试点项目专项跟踪

| 项目 | 代号 | 首轮重点 | 目标轮次 | 当前轮次 |
|---|---|---|---|---|
| MMC | MM | 治理模板基线、配置标准化 | 3 | 0 |
| KDS | KD | 数据资产、指标、证据结构化 | 3 | 0 |
| Brain | BR | 知识 UI 层联邦闭环 | 3 | 0 |
| PKC | PK | 端到端用户闭环 | 3 | 0 |
| GFIS | GF | 工厂主链试点、工单/质量/库存闭环 | 3 | 0 |

## 更新记录

| 日期 | 变更 |
|---|---|
| 2026-06-12 | 初始化：12 项目状态基线 |
| 2026-06-12 | v1.1：新增牵头智能体分配列，对齐12个交付包责任分解表 |
| 2026-06-12 | v1.2：按项目主线对齐 12 项目定位；Edge 保持为现场接入层，不作为当前 12 项目之一单列 |
