---
doc_id: GPCF-DOC-94532311B5
title: GPCF 2.0 治理文件收敛清单
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/governance/gpcf-2-governance-file-inventory.md
source_path: docs/governance/gpcf-2-governance-file-inventory.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# GPCF 2.0 治理文件收敛清单

本清单用于 Phase 1 治理减负。当前策略是先降级归档，不直接删除历史证据。

## 分类规则

| 分类 | 判定 | 处理 |
|---|---|---|
| 高频使用 | LOOP 主规范、文档门禁、项目群状态、能力注册、Feature Workspace | 保留 |
| 低频使用 | 历史阶段性报告、一次性复核、旧专项工作流 | 降级 |
| 无效使用 | 重复 progress、重复 review、重复 task、重复 status、重复 log、重复 notes、重复 decision | 归档候选 |
| 保留 | 架构约束、安全约束、测试证据、交付记录、风险记录 | 保留 |
| 降级 | 非阻塞审批、过细 action/step、开发前过度 spec、开发后重复复盘 | deprecated_candidate |
| 归档 | 历史 round、旧收据、低价值 checklist | archived_candidate |
| 待删除 | 仅在完成人工复核和 KDS 镜像确认后才能删除 | delete_candidate |

## 当前执行

- 不直接删除历史文档。
- 新开发只从 `features/active/F-xxx/` 进入。
- 项目节奏只写入 `projects/<project>/ROADMAP.md`、`STATUS.md`、`RISK.md`。
- 单个 Feature 不再创建 progress、review、task、status、log、notes 或 decision 文档。
