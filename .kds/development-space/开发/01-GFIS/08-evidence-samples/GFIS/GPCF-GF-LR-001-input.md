---
doc_id: GPCF-DOC-82A2F06757
title: GPCF-GF-LR-001 输入定义
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/GPCF-GF-LR-001-input.md
source_path: 08-evidence-samples/GFIS/GPCF-GF-LR-001-input.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-GF-LR-001 输入定义

## 1. Round 信息

| 项 | 内容 |
|---|---|
| Round ID | `GPCF-GF-LR-001` |
| 项目 | GFIS |
| 主线定位 | 工厂执行系统 / 工厂事实主账 |
| 当前输入 | 现代精工工厂岗位培训学习资料 |
| 输入状态 | 受控 evidence 样本 |
| 目标状态 | 为 GFIS 进入 `loop_ready` 做业务抽取准备 |

## 2. 本轮目标

从现代精工工厂岗位培训资料中抽取 GFIS 一期最小闭环所需的：

- 岗位与职责
- 业务对象
- 单据与记录
- 数据采集项
- 质量、安全、财务红线
- 与 GPC、WAES、KDS、Brain 的边界和接口候选

## 3. 入口条件

| 条件 | 状态 |
|---|---|
| PDF 已纳入 GPCF evidence 区 | yes |
| PDF 已生成 SHA-256 | yes |
| Markdown 结构化分析已生成 | yes |
| GFIS 项目仓 loop-state 已补齐 | no |
| GFIS 项目仓真实微循环已开始 | no |

## 4. 不处理范围

本轮不处理：

- 不把 PDF 直接改写为完整 GFIS 需求规格。
- 不宣称 GFIS 已实现任何业务功能。
- 不把商务报价、合同、回款主责归入 GFIS。
- 不替代现场考察真实数据采集。

## 5. 建议动作

| 顺序 | 动作 | 输出 |
|---|---|---|
| 1 | 抽取岗位清单 | `gfis-role-map.md` |
| 2 | 抽取业务对象 | `gfis-business-object-candidates.md` |
| 3 | 抽取单据和记录 | `gfis-document-record-candidates.md` |
| 4 | 抽取质量和安全门禁 | `gfis-quality-gate-candidates.md` |
| 5 | 明确 GFIS/GPC 边界 | `gfis-gpc-boundary-notes.md` |
| 6 | 生成现场采集表 | `gfis-field-study-data-capture.md` |

## 6. 检查项

- 输出是否能追溯到 PDF 原文页/章节。
- 是否区分 GFIS 主责和 GPC/WAES/KDS/Brain 协同职责。
- 是否避免把培训材料当成实现完成证据。
- 是否更新 GPCF 状态矩阵和 KDS 文档台账。

## 7. 下一轮输入

下一轮建议：

```text
GPCF-GF-LR-001
目标：生成 GFIS 岗位-流程-数据-门禁抽取包，并作为 GFIS 项目仓 loop_ready 初始化依据。
```
