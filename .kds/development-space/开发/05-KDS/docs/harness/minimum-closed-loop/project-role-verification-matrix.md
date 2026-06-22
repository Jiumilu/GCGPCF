---
doc_id: GPCF-DOC-9096ABA44D
title: 项目角色验证矩阵
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/project-role-verification-matrix.md
source_path: docs/harness/minimum-closed-loop/project-role-verification-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# 项目角色验证矩阵

| 项目 | 角色 | L4 职责 | 当前门禁 |
|---|---|---|---|
| GFIS | 工厂执行运行层 | 工厂事实主账、运行层 SOP、生产执行、质检、库存、发货、POD 事实接收 | repair_required |
| GPC | 供应链平台 | 项目初始化、组织/伙伴接入、平台订单、客户协同主线 | ready_for_review |
| PVAOS | 门户与运营底座 | 门户、平台运营、用户入口和运营支撑 | ready_for_review |
| WAES | 治理与证据门禁 | WAES confirmation、状态门控、越权控制和证据审计 | ready_for_review |
| KDS | 知识主存事实层 | 知识主存、KDS source backlink、write receipt 和本地镜像 | ready_for_review |
| Brain | 知识编排层 | 知识编制、检索、推理和 UI 知识呈现 | ready_for_review |
| PKC | 个人知识驾驶舱 | 个人知识工作台与端到端用户闭环 | ready_for_review |
| MMC | 管理配置中心 | 资源能力、治理模板、配置基线和 contract dry-run | ready_for_review |
| XiaoC | AI 能力蚁后 | AI 能力生产、编排路由和模型协同 | ready_for_review |
| XGD | 长程智能体大象 | 长程任务、重分析、多端协同和复杂任务承载 | ready_for_review |
| XiaoG | 轻量执行蚂蚁 | 轻量执行入口、设备协同和运行触发 | ready_for_review |
| GPCF | 治理控制平面 | 项目群总控、文档治理、Loop evidence 和 L4 repair 收口 | repair_required |

本矩阵只声明 L4 控制面责任边界，不升级任何项目为 accepted/integrated。
