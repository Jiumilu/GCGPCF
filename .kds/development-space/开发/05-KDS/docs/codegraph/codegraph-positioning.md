---
doc_id: GPCF-DOC-016C584865
title: CodeGraph 定位说明
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/codegraph/codegraph-positioning.md
source_path: docs/codegraph/codegraph-positioning.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph 定位说明

CodeGraph 在 GlobalCloud 项目群中的定位是 `Code Intelligence Fabric`：项目群代码事实图谱层。

它不替代 KDS、WAES、Harness 或 Loop：

| 层 | 职责 |
|---|---|
| KDS | 知识事实主存与受控镜像 |
| WAES | 风险、规则、门禁和阻断 |
| Harness | 执行、测试、验证和证据 |
| Loop | 持续改进闭环 |
| CodeGraph | 代码结构事实、调用路径、依赖影响、测试映射和证据定位 |

## 项目群范围

本定位覆盖当前 GPCF 项目状态矩阵中的 14 个项目：

GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF、GlobalCloud Studio、WAS。

## 非目标

- 不把 CodeGraph 当成普通 AI 编程辅助工具。
- 不把 CodeGraph 输出直接写成 KDS accepted fact。
- 不通过 CodeGraph 自动批准 WAES gate。
- 不通过 CodeGraph 自动声明 accepted、integrated 或 production_ready。
- 不进入项目内部业务开发。

## 成功标准

- 每个项目有独立 `.codegraph/` 本地图谱或受控例外。
- `.codegraph/` 不进入 Git。
- Loop evidence 记录 CodeGraph snapshot、query、impact 和风险。
- Harness 使用 CodeGraph 影响分析选择验证范围。
- WAES 对高风险变更要求 CodeGraph impact report。
- KDS/OKF 仅接收 CodeGraph candidate fact。
