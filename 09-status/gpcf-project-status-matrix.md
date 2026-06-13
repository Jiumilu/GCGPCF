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
| 1 | GlobalCloud GFIS | GF | 工厂执行系统 / 工厂事实主账 | 厂行 | 是 | 是 | 30 | 99% | partial | 现场真实样本尚未提交；业务 UAT 尚未由工厂/生产/质量/仓储/GPC/WAES 角色签收；生产环境确认和外部联调仍缺；`127.0.0.1:8080` 被本机 Python/uvicorn 占用；迁移窗口未授权；所有 received/signed/confirmed 均为 false | partial | 建立签收证据接收后的审计准备规则；仍不执行 `bench migrate`、schema sync、写 API 或外部联调 |
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
| 12 | GlobalCoud GPCF | CF | 体系文档工作区 / 总控治理仓 | 小即 | 是 | 是 | 2 | 70% | partial | KDS TOKEN 暂缓为上线同步门禁；Git dirty；多项目文档体系待补齐 | partial | 监督 GFIS 数据字典与接口契约生成，并补 GPCF command log / Git clean evidence |

## 状态分布统计

| 状态 | 项目数 | 项目 |
|---|---|---|
| not_started | 9 | GPC、PVAOS、WAES、KDS、Brain、PKC、XGD、XiaoG、MMC |
| loop_ready | 0 | - |
| loop_running | 0 | - |
| evidence_ready | 0 | - |
| audit_ready | 0 | - |
| harness_review | 0 | - |
| accepted | 0 | - |
| integrated | 0 | - |
| partial | 3 | GFIS、XiaoC、GPCF |
| blocked | 0 | - |

## 试点项目专项跟踪

| 项目 | 代号 | 首轮重点 | 目标轮次 | 当前轮次 |
|---|---|---|---|---|
| MMC | MM | 治理模板基线、配置标准化 | 3 | 0 |
| KDS | KD | 数据资产、指标、证据结构化 | 3 | 0 |
| Brain | BR | 知识 UI 层联邦闭环 | 3 | 0 |
| PKC | PK | 端到端用户闭环 | 3 | 0 |
| GFIS | GF | 工厂主链试点、工单/质量/库存闭环 | 31 | 30 |

## 更新记录

| 日期 | 变更 |
|---|---|
| 2026-06-12 | 初始化：12 项目状态基线 |
| 2026-06-12 | v1.1：新增牵头智能体分配列，对齐12个交付包责任分解表 |
| 2026-06-12 | v1.2：按项目主线对齐 12 项目定位；Edge 保持为现场接入层，不作为当前 12 项目之一单列 |
| 2026-06-12 | v1.3：GPCF 总控仓建立 `docs/harness/loop-state.md` 与首轮 `GPCF-CF-LR-001`，状态调整为受限 partial |
| 2026-06-12 | v1.4：正式启动 GFIS 托管 Loop 开发，完成 `GPCF-GF-LR-001` 首轮开发输入包 |
| 2026-06-12 | v1.5：完成 GFIS `GPCF-GF-LR-003` 业务规则固化，形成生产需求到工单字段映射与工单状态机 |
| 2026-06-12 | v1.6：完成 GFIS `GPCF-GF-LR-004` 机器校验资产，形成规则 schema、fixture 与 validator |
| 2026-06-12 | v1.7：完成 GFIS `GPCF-GF-LR-005` API/Doctype 差距闭环，形成可执行 gap list 与 validator |
| 2026-06-12 | v1.8：完成 GFIS `GPCF-GF-LR-006` P0 contract-draft 闭合，形成受控 API/Doctype 草案与 fake-Frappe contract test |
| 2026-06-12 | v1.9：完成 GFIS `GPCF-GF-LR-007` WAES gate event 对齐，形成 fixture 与 validator |
| 2026-06-12 | v1.10：完成 GFIS `GPCF-GF-LR-008` 运行态验证准备包和人工确认清单 |
| 2026-06-12 | v1.11：完成 GFIS `GPCF-GF-LR-009` 本开发机运行态预检，确认 compose/image、旧路径挂载、Desk 404 与 asset 缺失阻塞 |
| 2026-06-12 | v1.12：完成 GFIS `GPCF-GF-LR-010` 本开发机运行态基线修复，Desk、runtime asset、prereq/app checks 通过 |
| 2026-06-13 | v1.13：完成 GFIS `GPCF-GF-LR-011` 运行态写 API dry-run，创建物已清理，并登记 Dispatch Suggestion schema 漂移 |
| 2026-06-13 | v1.14：完成 GFIS `GPCF-GF-LR-012` 运行态 schema 同步与持久化 dry-run 复验，运行态技术链路转入 UAT/现场证据阶段 |
| 2026-06-13 | v1.15：完成 GFIS `GPCF-GF-LR-013` 现场样本采集模板、UAT 确认包和机器校验脚本 |
| 2026-06-13 | v1.16：完成 GFIS `GPCF-GF-LR-014` 现场样本空白工作包、20 个样本槽位和提交校验器 |
| 2026-06-13 | v1.17：完成 GFIS `GPCF-GF-LR-015` 真实样本提交目录、脱敏规则和 ingest validator |
| 2026-06-13 | v1.18：完成 GFIS `GPCF-GF-LR-016` 现场样本字段差距映射模板，识别 12 个 gap，其中 P0 gap 8 个 |
| 2026-06-13 | v1.19：完成 GFIS `GPCF-GF-LR-017` P0 gap 受控实现任务包，8 个 P0 task 全量追溯 LR-016 gap |
| 2026-06-13 | v1.20：完成 GFIS `GPCF-GF-LR-018` 最小实现批次，3 个 P0 task 进入 Custom Field 代码草案并通过 validator |
| 2026-06-13 | v1.21：完成 GFIS `GPCF-GF-LR-019` Transition Ledger 异常/返工字段草案，保持 WAES 复工门禁边界 |
| 2026-06-13 | v1.22：完成 GFIS `GPCF-GF-LR-020` Stock Entry 入库字段草案，保持不写真实库存 |
| 2026-06-13 | v1.23：完成 GFIS `GPCF-GF-LR-021` 出库/POD 金融边界字段草案，金融事实保持 L4 阻断 |
| 2026-06-13 | v1.24：完成 GFIS `GPCF-GF-LR-022` P0 gap closure matrix，确认代码/边界草案覆盖与剩余 UAT/运行态阻塞 |
| 2026-06-13 | v1.25：完成 GFIS `GPCF-GF-LR-023` 运行态迁移前检查包，建立迁移前置、回滚、样本、人工确认和停止条件 |
| 2026-06-13 | v1.26：完成 GFIS `GPCF-GF-LR-024` 迁移窗口授权记录和 dry-run runbook，授权标志保持未授权 |
| 2026-06-13 | v1.27：完成 GFIS `GPCF-GF-LR-025` 授权前只读 evidence 包，确认 diff/runtime/sensitive checks 通过且迁移仍未授权 |
| 2026-06-13 | v1.28：完成 GFIS `GPCF-GF-LR-026` 迁移执行前确认台账和人工确认清单，`ready_to_execute` 保持 false |
| 2026-06-13 | v1.29：完成 GFIS `GPCF-GF-LR-027` UAT/现场样本签收请求包和跨项目确认分发表，所有 received/signed/confirmed 保持 false |
| 2026-06-13 | v1.30：完成 GFIS `GPCF-GF-LR-028` 样本回收跟踪台账和 UAT 问题分级模板，所有 received/signed/confirmed 保持 false |
| 2026-06-13 | v1.31：完成 GFIS `GPCF-GF-LR-029` 样本提交包验收规则和脱敏复核清单，所有 received/signed/confirmed 保持 false |
| 2026-06-13 | v1.32：完成 GFIS `GPCF-GF-LR-030` UAT 问题处置闭环和豁免复核规则，所有 received/signed/confirmed 保持 false |
