---
doc_id: GPCF-DOC-87DD7D79CD
title: GlobalCloud 项目群文档防污染规则
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, Brain, XiaoC, XGD, XiaoG, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群文档防污染规则.md
source_path: 02-governance/GlobalCloud项目群文档防污染规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群文档防污染规则

日期：2026-06-12
状态：v1.0
适用范围：GPCF 全仓文档、KDS `开发` 空间镜像、Loop evidence

## 1. 目标

防止旧命名、旧架构判断、旧 AI 定位、虚假完成状态和跨系统主责污染重新进入项目群文档体系。

## 2. 禁止旧命名

以下词汇不得出现在当前受控文档正文、文件名和 KDS 路径中：

| 禁止词 | 替代口径 |
|---|---|
| GPC-Native | GPC |
| gpc-native | gpc |
| GPC Native | GPC |
| Native | 历史后缀、目标平台骨架、公共服务平台，视上下文处理 |
| 协同中台 | 绿色供应链公共服务平台本体 |

## 3. 禁止旧 AI 定位

| 禁止口径 | 当前口径 |
|---|---|
| XiaoC 只是提示词工程服务 | XiaoC 是蚁后：AI 能力生产与编排路由 |
| XGD 是桌面/语音/社交 AI 入口 | XGD 是大象：长程 Agent、重分析、多端交互和复杂任务承载 |
| XiaoC + Hermes + XGD 泛化为一个服务包 | XiaoC、XGD、XiaoG/Hermes 分层治理 |

## 4. 禁止真实性污染

以下表达不得作为完成结论：

1. 设计完成 = 实现完成。
2. 文档通过 = 业务完成。
3. 控制台可见 = 业务闭环完成。
4. KDS 本地镜像 = 真实 KDS API 已同步。
5. 证据样本 = 真实生产证据。

## 5. 主责边界污染

| 错误写法 | 正确边界 |
|---|---|
| Brain 替代 KDS 主存 | KDS 是主存，Brain 是编制与引擎/UI 层 |
| WAES 执行业务审批 | WAES 做治理门控，不承办业务事务 |
| GPC 写工厂执行事实 | GFIS 是工厂事实主账 |
| AI 直接写业务主账 | AI 只能给建议，必须经授权与主责系统处理 |

## 6. 执行方式

污染检查通过 `tools/kds-sync/check_document_pollution.py` 执行。任何污染命中必须进入 `rework_required`。
