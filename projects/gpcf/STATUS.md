---
doc_id: GPCF-DOC-3968FEF2EF
title: GPCF 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gpcf/STATUS.md
source_path: projects/gpcf/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# GPCF 状态

本文件只记录 GPCF 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`required`
- 中央入口：`openspec/changes/gpcf-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project gpcf`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`

## 当前状态

- GPCF 2.0 已进入 Feature 运行态。当前 Feature 和关闭状态以 `features/active/`、`features/done/` 与 `runtime/queue.json` 为准；本页不复制动态清单。
- 当前调度对象以 `runtime/state.json` 为准，角色流转记录在 `runtime/logs/F-xxx.jsonl`。
- 项目群纳管范围以 `config/project-group-projects.yaml` 为准。
- 发布、生产操作和业务状态提升遵循 `AGENTS.md` 的人工授权边界。
