---
doc_id: GPCF-DOC-FIREQUOTE-STATUS-20261022
title: FireQuote 状态
project: FireQuote
related_projects: [FireQuote, GPCF]
domain: governance
status: controlled
version: v1.0
owner: FireQuote
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/firequote/STATUS.md
source_path: projects/firequote/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# FireQuote 状态

本文件只记录 FireQuote（消防定额测算平台）的当前项目节奏状态；功能级进度、证据与关闭状态由 features 目录承载。

## 基线

| 项 | 内容 |
|---|---|
| project_id | FireQuote |
| 定位 | 消防工程企业定额与精细化成本控制平台（六层定额 + 确定性测算引擎 + 偏差分解 + 审批/快照/图审 + Hermes AI 助手） |
| 仓 | `GlobalCloud FireQuote` |
| 当前阶段 | 「最小系统」（首期 §16 范围内导入、版本、计算、方案比较、审核已具备） |
| 项目群范围 | 2026-10-22 注册表登记为第 29 个项目（`current_project_count: 29`） |

## 已记录事实（来自仓内 README）

- 2026-10-18 一键门禁：后端 89 passed / 1 skipped；前端构建通过；E2E 1 passed。
- 在线 AI 评测 10/10 通过（人工执行，需本机 Hermes）。
- 真实客户图纸/清单/实绩尚未接入验证；生产 SSO/OIDC 未接。

## 缺口

- 项目群 GPCF 节奏文件此前缺失，本文件为补登（内容以仓内 README 为准，待属主复核）。
- 项目群 28→29 范围变更的登记/门禁/分母影响待单独确认。
- 真实业务验证（S4）未开始；不声明客户验收或生产就绪。

## 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明真实业务已验证；
- 不声明本项目已纳入项目群 28 项目口径的完成度分母（29 项目口径待确认）。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/firequote-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project firequote`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`
