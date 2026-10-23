---
doc_id: GPCF-DOC-053F337921
title: XiaoG 状态
project: XiaoG
related_projects: [XiaoG]
domain: governance
status: controlled
version: v1.1
owner: XiaoG
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/xiaog/STATUS.md
source_path: projects/xiaog/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# XiaoG 状态

本文件只记录 XiaoG 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/xiaog-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project xiaog`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- 活跃 Feature：0（项目群侧无 Feature 载体）
- 当前阶段：全栈自 2026-10-16 起按用户指示暂停；live API / 设备验证未做
- 阻塞：暂停状态未正式裁定（恢复或挂起）；仓库 ahead 1065 / behind 2（性质待核）

## 已知证据

- `GlobalCoud GPCF/09-status/gpcf-project-status-matrix.md`：XiaoG L4 只读审计 mock 通过（`readonly_queries=3` 等，文档声明）
- `GlobalCloud XiaoG` 仓：ahead 1065 / behind 2（2026-10-22 实测，性质待核）

## 到下一状态门的关键缺口

- 明确恢复 / 挂起裁定，避免暂停态持续占用分母
- live API / 设备验证授权包与 BFF 契约
- 与 XGD 侧联调

## 本轮不做与非声明

- 不声明 accepted / integrated / production_ready / customer_accepted；
- 不声明 live API、设备 OTA、生产写入已完成；
- 不替代项目实施方案与 Feature 证据。
