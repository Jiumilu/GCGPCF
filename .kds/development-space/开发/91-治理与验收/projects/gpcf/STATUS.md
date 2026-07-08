---
doc_id: GPCF-DOC-3968FEF2EF
title: GPCF 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
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

## 当前状态

- GPCF 2.0 已进入 Feature 运行态。
- 当前出口验证 Feature：`F-002` 关闭到 `features/done/`。
- 第二个出口验证 Feature：`F-003` 关闭到 `features/done/`。
- 当前 active Feature：`F-004`、`F-005`。
- 调度状态写入 `runtime/queue.json` 和 `runtime/state.json`。
- 角色流转日志写入 `runtime/logs/F-xxx.jsonl`。
- `F-005` 已作为 GFIS 业务样本跑通完整角色链。
- 本阶段不授权自动 commit、push、deploy、真实 API、真实 KDS API 或状态提升。
