---
doc_id: GPCF-DOC-9406A78FC6
title: WAS 状态
project: WAS
related_projects: [WAS]
domain: governance
status: controlled
version: v1.0
owner: WAS
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/was/STATUS.md
source_path: projects/was/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# WAS 状态

本文件只记录 WAS 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/was-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project was`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
