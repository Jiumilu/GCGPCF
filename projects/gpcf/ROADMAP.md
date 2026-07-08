---
doc_id: GPCF-DOC-1253D15498
title: GPCF 路线图
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gpcf/ROADMAP.md
source_path: projects/gpcf/ROADMAP.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# GPCF 路线图

本文件只记录 GPCF 在 GPCF 2.0 下的项目节奏和阶段方向。具体交付不在这里展开，统一进入功能工作区，避免重复过程文档。

## 近期路线

- Phase 1：保持历史文档受控，停止新增重复治理过程文档。
- Phase 2：所有新开发从 `features/active/F-xxx/` 进入。
- Phase 3：以 `runtime/queue.json` 驱动 Dispatcher 到 Recorder 的轻量流转。
- Phase 4：Evidence Gate 以本地可回放结果决定 Feature 是否可关闭。
- Phase 5：通过 `gpcf_dispatch.py` 推进角色状态机，并用 `runtime/logs/F-xxx.jsonl` 记录每轮角色输入、输出和证据。
